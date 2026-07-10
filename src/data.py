"""Data access layer: load and query Gundam Card Game cards from local JSON."""
from __future__ import annotations

import html
import json
import re
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path

# data/cards/en/ relative to the project root (two parents up from this file)
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_DATA_DIR = _PROJECT_ROOT / "data" / "cards" / "en"
_BANLIST_PATH = _PROJECT_ROOT / "data" / "rules" / "banlist.json"
_DECKS_DIR = _PROJECT_ROOT / "data" / "decks"


@dataclass(frozen=True)
class Card:
    id: str
    name: str
    set_id: str
    set_name: str
    rarity: str | None = None
    color: str | None = None
    card_type: str | None = None
    level: int | None = None
    cost: int | None = None
    ap: int | None = None
    hp: int | None = None
    zone: str | None = None
    trait: str | None = None
    link: str | None = None
    effect: str | None = None
    source_title: str | None = None
    image_url: str | None = None


_BR_RE = re.compile(r"<br\s*/?>", re.IGNORECASE)
_TAG_RE = re.compile(r"<[^>]+>")


def _clean_effect(raw: str | None) -> str | None:
    if not raw:
        return None
    text = _BR_RE.sub("\n", raw)
    text = _TAG_RE.sub("", text)
    return html.unescape(text).strip() or None


def _to_int(value) -> int | None:
    if value in (None, "", "-"):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _normalize_color(raw) -> str | None:
    """Title-case English color names so 'green' and 'Green' don't both appear."""
    if raw is None or raw == "":
        return None
    s = str(raw).strip()
    if not s or s == "-":
        return None
    return s.title() if s.replace(" ", "").isalpha() else s


def _parse_card(raw: dict) -> Card:
    set_obj = raw.get("set") or {}
    images = raw.get("images") or {}
    return Card(
        id=raw["id"],
        name=raw.get("name", ""),
        set_id=set_obj.get("id", ""),
        set_name=set_obj.get("name", ""),
        rarity=raw.get("rarity") or None,
        color=_normalize_color(raw.get("color")),
        card_type=raw.get("cardType") or None,
        level=_to_int(raw.get("level")),
        cost=_to_int(raw.get("cost")),
        ap=_to_int(raw.get("ap")),
        hp=_to_int(raw.get("hp")),
        zone=raw.get("zone") or None,
        trait=raw.get("trait") or None,
        link=raw.get("link") or None,
        effect=_clean_effect(raw.get("effect")),
        source_title=raw.get("sourceTitle") or None,
        image_url=images.get("large") or images.get("small") or None,
    )


@lru_cache(maxsize=1)
def _load_all() -> tuple[Card, ...]:
    """Load every set file, deduping by id.

    Some sets overlap (e.g. the "Beta" edition reused ids that later shipped
    in official sets), so later files win. Sorting keeps this deterministic:
    filenames like beta.json sort before gd01.json/st01.json/etc, so the
    official printing overrides the beta placeholder.
    """
    if not _DATA_DIR.exists():
        return ()
    by_id: dict[str, Card] = {}
    for json_file in sorted(_DATA_DIR.glob("*.json")):
        with json_file.open(encoding="utf-8") as f:
            raw_list = json.load(f)
        for raw in raw_list:
            card = _parse_card(raw)
            by_id[card.id] = card
    return tuple(by_id.values())


def get_all_cards() -> list[Card]:
    return list(_load_all())


def card_to_dict(card: Card) -> dict:
    return asdict(card)


def find_cards(
    *,
    query: str | None = None,
    color: str | None = None,
    card_type: str | None = None,
    cost: int | None = None,
    cost_min: int | None = None,
    cost_max: int | None = None,
    trait: str | None = None,
    set_id: str | None = None,
    limit: int = 50,
) -> list[Card]:
    """Filter cards by any combination of criteria.

    `query` matches against name (case-insensitive substring).
    `trait` matches as substring (e.g. "Earth Federation").
    Returns up to `limit` cards.
    """
    cards = _load_all()
    needle = query.casefold() if query else None
    color_l = color.casefold() if color else None
    type_l = card_type.casefold() if card_type else None
    trait_l = trait.casefold() if trait else None
    set_l = set_id.casefold() if set_id else None

    out: list[Card] = []
    for c in cards:
        if needle and needle not in c.name.casefold():
            continue
        if color_l and (not c.color or c.color.casefold() != color_l):
            continue
        if type_l and (not c.card_type or c.card_type.casefold() != type_l):
            continue
        if cost is not None and c.cost != cost:
            continue
        if cost_min is not None and (c.cost is None or c.cost < cost_min):
            continue
        if cost_max is not None and (c.cost is None or c.cost > cost_max):
            continue
        if trait_l and (not c.trait or trait_l not in c.trait.casefold()):
            continue
        if set_l and (not c.set_id or c.set_id.casefold() != set_l):
            continue
        out.append(c)
        if len(out) >= limit:
            break
    return out


def get_card_by_id(card_id: str) -> Card | None:
    needle = card_id.casefold()
    for c in _load_all():
        if c.id.casefold() == needle:
            return c
    return None


_TRAIT_TOKEN_RE = re.compile(r"\(([^)]+)\)")


def extract_traits(trait_field: str | None) -> list[str]:
    """Split a raw trait field like '(Earth Federation) (white Base Team)' into tokens."""
    if not trait_field:
        return []
    return [t.strip() for t in _TRAIT_TOKEN_RE.findall(trait_field) if t.strip()]


_LINK_NAME_RE = re.compile(r"\[([^\]]+)\]")
_PILOT_MODE_RE = re.compile(r"【Pilot】\s*\[([^\]]+)\]")


def pilot_identity(card: Card) -> tuple[str, str | None] | None:
    """Return (name, trait_field) this card can pair as a Pilot under, or
    None if it can't pair as a Pilot at all.

    Real PILOT cards use their own name/trait. Some COMMAND cards can also
    be paired as a Pilot instead of activating their command effect (rule
    3-4-6) — their Pilot-mode name is embedded in the effect text as
    "【Pilot】[Name]"; their Pilot-mode trait is not separately captured by
    the data source, so the Command's own `trait` field is used (in
    practice this field is only populated on Command cards that have a
    Pilot mode, so it lines up).
    """
    card_type = (card.card_type or "").upper()
    if card_type == "PILOT":
        return (card.name, card.trait)
    if card_type == "COMMAND" and card.effect:
        m = _PILOT_MODE_RE.search(card.effect)
        if m:
            return (m.group(1).strip(), card.trait)
    return None


def unit_linkable_by(unit_link: str | None, pilot_name: str, pilot_trait: str | None) -> bool:
    """Approximate whether a Unit's link condition is satisfied by a pilot.

    Handles the two observed condition shapes: a specific card name in
    brackets ('[Amuro Ray]', matched as a substring per rule 3-2-6-4) and a
    trait requirement in parens ('(Tekkadan) Trait'). Multiple bracket/paren
    tokens (joined by '/' or ',') are treated as OR'd alternatives — a rare
    few link conditions combine a trait and a name (e.g. '(Londo Bell),
    [Amuro Ray]') where the real rule may require both; this treats them as
    either being sufficient, so it can occasionally overcount. Good enough
    for a "how many bodies can this pilot link" overview, not for strict
    legality checking.
    """
    if not unit_link or unit_link == "-":
        return False
    names = _LINK_NAME_RE.findall(unit_link)
    if names and any(n.casefold() in pilot_name.casefold() for n in names):
        return True
    required_traits = extract_traits(unit_link)
    if required_traits:
        pilot_traits = {t.casefold() for t in extract_traits(pilot_trait)}
        if any(t.casefold() in pilot_traits for t in required_traits):
            return True
    return False


@lru_cache(maxsize=1)
def list_unique_sets() -> list[dict]:
    seen: dict[str, str] = {}
    for c in _load_all():
        if c.set_id and c.set_id not in seen:
            seen[c.set_id] = c.set_name
    return [{"id": sid, "name": name} for sid, name in sorted(seen.items())]


def _dedupe_canonical(values) -> list[str]:
    """Group strings by casefold and pick the variant with the most uppercase letters.

    Example: ['white Base Team', 'White Base Team'] -> ['White Base Team'].
    Acronyms like 'AEUG' are preserved over 'aeug' or 'Aeug' if present.
    """
    chosen: dict[str, str] = {}
    for v in values:
        if not v:
            continue
        key = v.casefold()
        current = chosen.get(key)
        if current is None or sum(c.isupper() for c in v) > sum(c.isupper() for c in current):
            chosen[key] = v
    return sorted(chosen.values(), key=str.casefold)


@lru_cache(maxsize=1)
def list_unique_traits() -> list[str]:
    return _dedupe_canonical(t for c in _load_all() for t in extract_traits(c.trait))


@lru_cache(maxsize=1)
def _trait_canonical_map() -> dict[str, str]:
    """Casefolded trait -> canonical display form, per list_unique_traits()."""
    return {t.casefold(): t for t in list_unique_traits()}


def canonicalize_trait(trait: str) -> str:
    """Fold casing variants of the same trait (e.g. 'white Base Team' vs
    'White Base Team', both present in the raw data) to one display form."""
    return _trait_canonical_map().get(trait.casefold(), trait)


@lru_cache(maxsize=1)
def list_unique_card_types() -> list[str]:
    return sorted({c.card_type for c in _load_all() if c.card_type})


@lru_cache(maxsize=1)
def load_banlist() -> dict:
    """Load the official banned/restricted/banned-pair list.

    See data/rules/banned_restricted_list.md for the human-readable source
    and reasoning behind each entry. Returns an empty structure if the file
    is missing, so callers don't need to special-case its absence.
    """
    if not _BANLIST_PATH.exists():
        return {"banned": {}, "restricted": {}, "banned_pairs": [], "banned_pair_groups": []}
    with _BANLIST_PATH.open(encoding="utf-8") as f:
        return json.load(f)


@lru_cache(maxsize=1)
def list_unique_colors() -> list[str]:
    return _dedupe_canonical(c.color for c in _load_all() if c.color)


_DECKLIST_LINE_RE = re.compile(r"^\s*(\d+)\s+(\S+)")


def parse_decklist_text(text: str) -> dict[str, int]:
    """Parse a plain-text decklist: one card per line as '<count> <card_id> <name...>'.

    The trailing name is for human readability only; only the count and id
    are read, so it doesn't need to match the card's actual name. Blank
    lines and lines starting with '#' are ignored.
    """
    deck: dict[str, int] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = _DECKLIST_LINE_RE.match(line)
        if not m:
            continue
        count, card_id = int(m.group(1)), m.group(2)
        deck[card_id] = deck.get(card_id, 0) + count
    return deck


def list_deck_files() -> list[str]:
    """List available deck names (filename without extension) in data/decks/."""
    if not _DECKS_DIR.exists():
        return []
    return sorted(p.stem for p in _DECKS_DIR.glob("*.txt"))


def load_deck(name: str) -> dict[str, int]:
    """Load and parse a plain-text decklist by name from data/decks/<name>.txt."""
    path = _DECKS_DIR / f"{name}.txt"
    if not path.exists():
        raise FileNotFoundError(f"No deck file named '{name}.txt' in {_DECKS_DIR}")
    return parse_decklist_text(path.read_text(encoding="utf-8"))


def save_deck(name: str, deck: dict[str, int]) -> Path:
    """Write {card_id: count} to data/decks/<name>.txt in the plain
    '<count> <card_id> <name...>' format (matches egmanevents.com's
    deckbuilder export/import format). Overwrites if the file already
    exists. Returns the written path."""
    _DECKS_DIR.mkdir(parents=True, exist_ok=True)
    lines = []
    for card_id, count in deck.items():
        card = get_card_by_id(card_id)
        label = card.name if card else card_id
        lines.append(f"{count} {card_id} {label}")
    path = _DECKS_DIR / f"{name}.txt"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def save_deck_image(name: str, png_bytes: bytes) -> Path:
    """Write PNG bytes to data/decks/<name>.png, overwriting if it already
    exists. Mirrors save_deck's naming convention so the matching
    decklist (<name>.txt) and rendered image (<name>.png) stay paired."""
    _DECKS_DIR.mkdir(parents=True, exist_ok=True)
    path = _DECKS_DIR / f"{name}.png"
    path.write_bytes(png_bytes)
    return path


def clear_cache() -> None:
    """Clear every lru_cache in this module so the next call re-reads from
    disk. Call after writing new data (e.g. sync.sync_all()) so a running
    server picks up fresh card/banlist data without needing a restart."""
    _load_all.cache_clear()
    list_unique_sets.cache_clear()
    list_unique_traits.cache_clear()
    _trait_canonical_map.cache_clear()
    list_unique_card_types.cache_clear()
    load_banlist.cache_clear()
    list_unique_colors.cache_clear()
