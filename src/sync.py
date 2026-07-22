"""Refresh the local card database (data/cards/en/*.json) from upstream sources.

Two providers are merged:
- apitcg/gundam-tcg-data (GitHub): primary source, historically covers Beta,
  GD01-GD02, ST01-ST06.
- deckbuilder.egmanevents.com: a public API that fills in whatever sets
  apitcg doesn't have yet (newer GD/ST sets tend to land here first).

When both providers have a given set, apitcg wins.

Card art URLs are always rebuilt as "<card_code>.webp" against
gundam-gcg.com's own CDN (through the images.weserv.nl resize proxy),
regardless of what either upstream source suggests for the image path: both
have been observed pointing at filenames that 404 (wrong extension,
revision-hash suffixes baked into the path, etc). The plain webp path is the
only one verified against the live site's own markup to actually work.
"""
from __future__ import annotations

import json
import logging
import os
from collections import defaultdict
from pathlib import Path
from typing import Any

import httpx

logger = logging.getLogger(__name__)

_APITCG_REPO = "apitcg/gundam-tcg-data"
_APITCG_BRANCH = "main"
_EGMAN_API_URL = "https://deckbuilder.egmanevents.com/api/cards/gundam"
_EGMAN_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)
_LANG = "en"
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_DATA_DIR = _PROJECT_ROOT / "data" / "cards" / _LANG
_IMG_BASE = "https://images.weserv.nl/?url=www.gundam-gcg.com/en/images/cards/card"

_EGMAN_CATEGORY_TO_TYPE: dict[str, str] = {
    "unit": "UNIT",
    "pilot": "PILOT",
    "command": "COMMAND",
    "base": "BASE",
    "resource": "RESOURCE",
    "ex base": "EX BASE",
    "ex resource": "EX RESOURCE",
    "unit token": "UNIT TOKEN",
}


def _image_url(card_code: str) -> dict[str, str]:
    path = f"{card_code}.webp"
    return {"large": f"{_IMG_BASE}/{path}", "small": f"{_IMG_BASE}/{path}"}


def _github_headers() -> dict[str, str]:
    """Auth header for GitHub if GITHUB_TOKEN is set in the environment.

    Unauthenticated GitHub API calls are limited to 60/hour per IP; a full
    sync makes ~1 listing call (raw.githubusercontent.com downloads don't
    count), but repeated syncs plus other tooling on the same IP can still
    exhaust it. A token raises the limit to 5000/hour."""
    token = os.getenv("GITHUB_TOKEN")
    return {"Authorization": f"Bearer {token}"} if token else {}


def _fetch_apitcg_sets() -> dict[str, list[dict]]:
    """Fetch every per-set JSON file from the apitcg GitHub repo."""
    url = f"https://api.github.com/repos/{_APITCG_REPO}/contents/cards/{_LANG}?ref={_APITCG_BRANCH}"
    try:
        resp = httpx.get(url, timeout=30.0, headers=_github_headers())
        resp.raise_for_status()
    except httpx.HTTPStatusError as e:
        if e.response.status_code in (403, 429):
            raise RuntimeError(
                "GitHub API rate limit hit while listing apitcg sets. "
                "Wait for the limit to reset, or set GITHUB_TOKEN in the "
                "environment (see .env.example) to raise it to 5000/hour."
            ) from e
        raise
    filenames = [item["name"] for item in resp.json() if item["name"].endswith(".json")]

    sets: dict[str, list[dict]] = {}
    for filename in filenames:
        set_id = filename.removesuffix(".json").lower()
        raw_url = (
            f"https://raw.githubusercontent.com/{_APITCG_REPO}/{_APITCG_BRANCH}"
            f"/cards/{_LANG}/{filename}"
        )
        resp = httpx.get(raw_url, timeout=30.0)
        resp.raise_for_status()
        cards = resp.json()
        for card in cards:
            card_id = card.get("id")
            if card_id:
                card["images"] = _image_url(str(card_id))
        sets[set_id] = cards
    return sets


def _egman_format_trait(traits: Any) -> str | None:
    """Convert ['Earth Federation', 'White Base Team'] to '(Earth Federation) (White Base Team)'."""
    if not traits:
        return None
    if isinstance(traits, str):
        return traits or None
    if isinstance(traits, list):
        parts = [str(t).strip() for t in traits if str(t).strip()]
        return " ".join(f"({p})" for p in parts) if parts else None
    return None


def _egman_format_color(color: Any) -> str | None:
    if not color:
        return None
    if isinstance(color, str):
        return color or None
    if isinstance(color, list):
        parts = [str(c).strip() for c in color if str(c).strip()]
        if not parts:
            return None
        return parts[0] if len(parts) == 1 else "/".join(parts)
    return None


def _egman_format_zone(locations: Any) -> str | None:
    if not locations:
        return None
    if isinstance(locations, str):
        return locations or None
    if isinstance(locations, list):
        parts = [str(z).strip() for z in locations if str(z).strip()]
        return " / ".join(parts) if parts else None
    return None


def _egman_format_card_type(category: Any) -> str | None:
    if not category:
        return None
    return _EGMAN_CATEGORY_TO_TYPE.get(str(category).strip().lower(), str(category).upper())


def _egman_format_effect(record: dict) -> str | None:
    """Prepend the 【Burst】 text egmanevents keeps in its own separate field.

    apitcg folds Burst into the main effect string (e.g. "【Burst】Add this
    card to your hand.\\n【When Paired】..."); egmanevents instead exposes it
    as a sibling "burst" field and leaves "effect" as just the rest of the
    card text. Naively mapping only "effect" silently drops this line for
    every card that has one (roughly a quarter of egmanevents' catalog:
    almost all Pilots, most Bases, many Commands) - reconstruct the apitcg
    shape here so nothing is lost.
    """
    burst = record.get("burst")
    effect = record.get("effect")
    burst_line = f"【Burst】{burst}" if burst else None
    if burst_line and effect:
        return f"{burst_line}\n{effect}"
    return burst_line or effect


def _egman_to_apitcg_shape(record: dict) -> dict | None:
    """Map one egmanevents card record to the per-set apitcg JSON shape."""
    card_code = record.get("card_code")
    if not card_code:
        return None
    set_code = record.get("set_code") or card_code.split("-", 1)[0]
    set_id = str(set_code).lower()
    set_name = record.get("set") or set_code
    card_type = _egman_format_card_type(record.get("category"))

    # egmanevents' ap/hp fields for Pilot cards represent the AP/HP modifier
    # a Pilot grants its paired Unit (rule 2-7-3/2-8-4) - but its API returns
    # 0/0 for effectively every Pilot regardless of the real printed value
    # (verified against card images: e.g. Zeheart Galette GD03-094 is a real
    # +2/+2, Ennil El GD04-096 is +1/+2, Kira Yamato GD05-081 is +2/+2, all
    # scraped here as 0/0). Since egmanevents never reliably has this number,
    # surface it as unknown (None) rather than a confidently-wrong 0 - this
    # only affects sets apitcg hasn't covered yet (GD03+, EB01), so if/when
    # apitcg adds them the merge in sync_all() already prefers apitcg's real
    # values over this.
    ap = None if card_type == "PILOT" else record.get("ap")
    hp = None if card_type == "PILOT" else record.get("hp")

    return {
        "id": str(card_code),
        "name": record.get("name") or "",
        "rarity": record.get("rarity"),
        "color": _egman_format_color(record.get("color")),
        "cardType": card_type,
        "level": record.get("level"),
        "cost": record.get("cost"),
        "ap": ap,
        "hp": hp,
        "zone": _egman_format_zone(record.get("locations")),
        "trait": _egman_format_trait(record.get("type")),
        "link": record.get("link_requirement"),
        "effect": _egman_format_effect(record),
        "sourceTitle": None,  # egmanevents does not include the source anime title
        "images": _image_url(str(card_code)),
        "set": {"id": set_id, "name": set_name},
    }


def fetch_egman_raw() -> list[dict]:
    """Fetch the raw (unmapped) egmanevents card list. Exposed for debugging."""
    headers = {"User-Agent": _EGMAN_USER_AGENT, "Accept": "application/json"}
    resp = httpx.get(_EGMAN_API_URL, headers=headers, timeout=60.0, follow_redirects=True)
    resp.raise_for_status()
    raw = resp.json()
    if not isinstance(raw, list):
        raise RuntimeError(f"Unexpected egmanevents API shape: {type(raw).__name__}")
    return raw


def _fetch_egman_sets() -> dict[str, list[dict]]:
    """Fetch every card from the egmanevents API, grouped and mapped by set id."""
    by_set: dict[str, list[dict]] = defaultdict(list)
    seen: set[str] = set()
    for record in fetch_egman_raw():
        mapped = _egman_to_apitcg_shape(record)
        if not mapped or mapped["id"] in seen:
            continue
        seen.add(mapped["id"])
        set_id = mapped["set"]["id"]
        if not set_id or set_id == "t":  # 'T' is egman's shorthand for token cards, not a real set
            continue
        by_set[set_id].append(mapped)
    return dict(by_set)


def sync_all(only: str | None = None) -> dict:
    """Refresh data/cards/en/*.json from both upstream sources.

    apitcg is the primary source; egmanevents fills any set apitcg doesn't
    have. When both have a set, apitcg wins. Pass `only` (a set id, e.g.
    "gd05") to refresh just that one set instead of everything. Always
    overwrites (this is a refresh operation, not a gap-filler).

    Returns {"sets": {set_id: card_count, ...}, "total_cards": N}.
    """
    logger.info("Fetching apitcg sets...")
    apitcg_sets = _fetch_apitcg_sets()
    logger.info("apitcg: %d sets", len(apitcg_sets))

    logger.info("Fetching egmanevents cards...")
    egman_sets = _fetch_egman_sets()
    logger.info("egmanevents: %d sets", len(egman_sets))

    merged: dict[str, list[dict]] = dict(egman_sets)
    merged.update(apitcg_sets)  # apitcg wins where both providers have a set

    only_id = only.lower() if only else None
    _DATA_DIR.mkdir(parents=True, exist_ok=True)

    written: dict[str, int] = {}
    for set_id, cards in sorted(merged.items()):
        if only_id and set_id != only_id:
            continue
        out = _DATA_DIR / f"{set_id}.json"
        out.write_text(json.dumps(cards, indent=2, ensure_ascii=False), encoding="utf-8")
        written[set_id] = len(cards)
        logger.info("Wrote %s (%d cards)", out.name, len(cards))

    total = sum(written.values())
    logger.info("Done. %d set(s), %d cards total.", len(written), total)
    return {"sets": written, "total_cards": total}
