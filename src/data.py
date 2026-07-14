"""Data access layer: load and query Gundam Card Game cards from local JSON."""
from __future__ import annotations

import html
import json
import re
import unicodedata
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path

# data/cards/en/ relative to the project root (two parents up from this file)
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_DATA_DIR = _PROJECT_ROOT / "data" / "cards" / "en"
_BANLIST_PATH = _PROJECT_ROOT / "data" / "rules" / "banlist.json"
_RULES_PATH = _PROJECT_ROOT / "data" / "rules" / "comprehensive_rules.md"
_DECKS_DIR = _PROJECT_ROOT / "data" / "decks"
_GAMES_DIR = _PROJECT_ROOT / "data" / "games"


def search_fold(s: str) -> str:
    """Fold a string for search comparison: NFKC-normalize (so the roman
    numeral 'Ⅱ' in card names matches an ASCII 'II' query and vice versa),
    then casefold."""
    return unicodedata.normalize("NFKC", s).casefold()


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


def _clean_rarity(raw) -> str | None:
    """Strip upstream padding: 'C                +' -> 'C+'. Every observed
    rarity is a single token plus an optional '+'/'++' parallel-print
    suffix, so removing all internal whitespace is safe."""
    if not raw:
        return None
    return re.sub(r"\s+", "", str(raw)) or None


def _normalize_zone(raw) -> str | None:
    """Fold the two upstream zone spellings ('Space Earth' from apitcg,
    'Space / Earth' from egmanevents) into one canonical 'Space / Earth'."""
    if not raw:
        return None
    s = str(raw).strip()
    if not s or s == "-":
        return None
    tokens = [t for t in re.split(r"[\s/]+", s) if t]
    return " / ".join(tokens) if tokens else None


def _parse_card(raw: dict) -> Card:
    set_obj = raw.get("set") or {}
    images = raw.get("images") or {}
    return Card(
        id=raw["id"],
        name=raw.get("name", ""),
        set_id=set_obj.get("id", ""),
        set_name=set_obj.get("name", ""),
        rarity=_clean_rarity(raw.get("rarity")),
        color=_normalize_color(raw.get("color")),
        card_type=raw.get("cardType") or None,
        level=_to_int(raw.get("level")),
        cost=_to_int(raw.get("cost")),
        ap=_to_int(raw.get("ap")),
        hp=_to_int(raw.get("hp")),
        zone=_normalize_zone(raw.get("zone")),
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
    effect: str | None = None,
    color: str | None = None,
    card_type: str | None = None,
    cost: int | None = None,
    cost_min: int | None = None,
    cost_max: int | None = None,
    level: int | None = None,
    level_min: int | None = None,
    level_max: int | None = None,
    ap_min: int | None = None,
    ap_max: int | None = None,
    hp_min: int | None = None,
    hp_max: int | None = None,
    trait: str | None = None,
    set_id: str | None = None,
    limit: int = 50,
) -> list[Card]:
    """Filter cards by any combination of criteria.

    `query` matches against name, `effect` against effect text (both
    case-insensitive substrings, NFKC-folded so 'Zaku II' matches the
    dataset's roman-numeral 'Zaku Ⅱ'). `trait` matches as substring
    (e.g. "Earth Federation"). Numeric min/max bounds are inclusive; cards
    missing that stat (None) never match a bound. Returns up to `limit`.
    """
    cards = _load_all()
    needle = search_fold(query) if query else None
    effect_l = search_fold(effect) if effect else None
    color_l = color.casefold() if color else None
    type_l = card_type.casefold() if card_type else None
    trait_l = trait.casefold() if trait else None
    set_l = set_id.casefold() if set_id else None

    def _in_bounds(value: int | None, lo: int | None, hi: int | None) -> bool:
        if lo is None and hi is None:
            return True
        if value is None:
            return False
        return (lo is None or value >= lo) and (hi is None or value <= hi)

    out: list[Card] = []
    for c in cards:
        if needle and needle not in search_fold(c.name):
            continue
        if effect_l and (not c.effect or effect_l not in search_fold(c.effect)):
            continue
        if color_l and (not c.color or c.color.casefold() != color_l):
            continue
        if type_l and (not c.card_type or c.card_type.casefold() != type_l):
            continue
        if cost is not None and c.cost != cost:
            continue
        if not _in_bounds(c.cost, cost_min, cost_max):
            continue
        if level is not None and c.level != level:
            continue
        if not _in_bounds(c.level, level_min, level_max):
            continue
        if not _in_bounds(c.ap, ap_min, ap_max):
            continue
        if not _in_bounds(c.hp, hp_min, hp_max):
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


_TYPE_ORDER = {"UNIT": 0, "PILOT": 1, "COMMAND": 2, "BASE": 3, "RESOURCE": 4}


def deck_sort_key(card: Card) -> tuple:
    """Canonical in-deck ordering key: card type (UNIT → PILOT → COMMAND →
    BASE → RESOURCE → anything else), then ascending level, then ascending
    cost, then id as a stable tiebreak. Cards missing level/cost sort after
    the ones that have it within their type group."""
    type_rank = _TYPE_ORDER.get((card.card_type or "").upper(), 5)
    return (
        type_rank,
        card.level if card.level is not None else 999,
        card.cost if card.cost is not None else 999,
        card.id,
    )


def sort_deck(deck: dict[str, int]) -> dict[str, int]:
    """Return a new {card_id: count} dict in canonical order (see
    deck_sort_key). Unknown card ids keep their input order, after all
    known cards — they can't be ranked without type/level data."""
    known: list[tuple[Card, str, int]] = []
    unknown: list[tuple[str, int]] = []
    for card_id, count in deck.items():
        card = get_card_by_id(card_id)
        if card is None:
            unknown.append((card_id, count))
        else:
            known.append((card, card_id, count))
    known.sort(key=lambda entry: deck_sort_key(entry[0]))
    out = {card_id: count for _, card_id, count in known}
    out.update(dict(unknown))
    return out


def _deck_path(name: str, suffix: str) -> Path:
    """Resolve a deck name (optionally with subfolders, e.g. 'meta/bg_oyw')
    to a path under data/decks/, rejecting anything that would escape it
    ('../evil', absolute paths). The name comes from the MCP client, so it
    can't be trusted to stay inside the decks directory on its own."""
    decks_root = _DECKS_DIR.resolve()
    path = (decks_root / f"{name}{suffix}").resolve()
    if not path.is_relative_to(decks_root):
        raise ValueError(f"Invalid deck name {name!r}: must stay inside data/decks/")
    return path


def list_deck_files() -> list[str]:
    """List available deck names in data/decks/, recursing into subfolders
    (e.g. 'meta/bg_oyw' for data/decks/meta/bg_oyw.txt). Names are relative
    posix-style paths without the .txt extension, usable directly with
    load_deck/save_deck."""
    if not _DECKS_DIR.exists():
        return []
    return sorted(
        p.relative_to(_DECKS_DIR).with_suffix("").as_posix()
        for p in _DECKS_DIR.rglob("*.txt")
    )


def load_deck(name: str) -> dict[str, int]:
    """Load and parse a plain-text decklist by name from data/decks/<name>.txt."""
    path = _deck_path(name, ".txt")
    if not path.exists():
        raise FileNotFoundError(f"No deck file named '{name}.txt' in {_DECKS_DIR}")
    return parse_decklist_text(path.read_text(encoding="utf-8"))


def save_deck(name: str, deck: dict[str, int]) -> Path:
    """Write {card_id: count} to data/decks/<name>.txt in the plain
    '<count> <card_id> <name...>' format (matches egmanevents.com's
    deckbuilder export/import format). Lines are written in canonical
    order (sort_deck: UNIT → PILOT → COMMAND → BASE, then ascending
    level/cost). Subfolder names ('meta/x') are created as needed.
    Overwrites if the file already exists. Returns the written path."""
    path = _deck_path(name, ".txt")
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    for card_id, count in sort_deck(deck).items():
        card = get_card_by_id(card_id)
        label = card.name if card else card_id
        lines.append(f"{count} {card_id} {label}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def save_deck_image(name: str, png_bytes: bytes) -> Path:
    """Write PNG bytes to data/decks/<name>.png, overwriting if it already
    exists. Mirrors save_deck's naming convention so the matching
    decklist (<name>.txt) and rendered image (<name>.png) stay paired."""
    path = _deck_path(name, ".png")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(png_bytes)
    return path


def delete_deck(name: str) -> list[str]:
    """Delete data/decks/<name>.txt and its paired <name>.png if present.
    Returns the paths that were actually removed; raises FileNotFoundError
    if not even the .txt exists (so typos don't silently 'succeed')."""
    txt = _deck_path(name, ".txt")
    if not txt.exists():
        raise FileNotFoundError(f"No deck file named '{name}.txt' in {_DECKS_DIR}")
    removed = []
    for path in (txt, _deck_path(name, ".png")):
        if path.exists():
            path.unlink()
            removed.append(str(path))
    return removed


def rename_deck(old_name: str, new_name: str) -> list[str]:
    """Rename a saved deck (and its paired .png, if any) from old_name to
    new_name. Refuses to overwrite an existing target. Returns the new
    paths written."""
    old_txt = _deck_path(old_name, ".txt")
    if not old_txt.exists():
        raise FileNotFoundError(f"No deck file named '{old_name}.txt' in {_DECKS_DIR}")
    new_txt = _deck_path(new_name, ".txt")
    if new_txt.exists():
        raise FileExistsError(f"Deck '{new_name}' already exists; delete or pick another name")
    new_txt.parent.mkdir(parents=True, exist_ok=True)
    moved = []
    old_txt.rename(new_txt)
    moved.append(str(new_txt))
    old_png = _deck_path(old_name, ".png")
    if old_png.exists():
        new_png = _deck_path(new_name, ".png")
        old_png.rename(new_png)
        moved.append(str(new_png))
    return moved


def _game_path(name: str, suffix: str = ".yaml") -> Path:
    """Resolve a game-record name (optionally with subfolders) to a path
    under data/games/, rejecting anything that would escape it — same
    guard as _deck_path, and for the same reason: the name comes from the
    MCP client."""
    games_root = _GAMES_DIR.resolve()
    path = (games_root / f"{name}{suffix}").resolve()
    if not path.is_relative_to(games_root):
        raise ValueError(f"Invalid game name {name!r}: must stay inside data/games/")
    return path


def save_game_file(name: str, text: str, overwrite: bool = False) -> Path:
    """Write a game-record YAML to data/games/<name>.yaml. Refuses to
    replace an existing record unless overwrite=True — game records are a
    knowledge base, often hand-annotated after import (pinned card ids,
    study notes), so silent clobbering would lose work."""
    path = _game_path(name)
    if path.exists() and not overwrite:
        raise FileExistsError(
            f"Game record '{name}' already exists; pass overwrite=True to replace it"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def save_game_log(name: str, text: str) -> Path:
    """Write the raw source log next to the YAML record (<name>.log), so
    records can be regenerated when the parser or record format evolves.
    No overwrite guard: it's paired with save_game_file, which has one."""
    path = _game_path(name, ".log")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def load_game_text(name: str) -> str | None:
    """Raw text of a saved game record (data/games/<name>.yaml), or None
    if it doesn't exist."""
    path = _game_path(name)
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


def list_game_files() -> list[str]:
    """List saved game-record names in data/games/, recursing into
    subfolders — same naming convention as list_deck_files."""
    if not _GAMES_DIR.exists():
        return []
    return sorted(
        p.relative_to(_GAMES_DIR).with_suffix("").as_posix()
        for p in _GAMES_DIR.rglob("*.yaml")
    )


@lru_cache(maxsize=1)
def load_rules_text() -> str:
    """Full text of the Comprehensive Rules (data/rules/comprehensive_rules.md).
    Empty string if the file is missing."""
    if not _RULES_PATH.exists():
        return ""
    return _RULES_PATH.read_text(encoding="utf-8")


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
    load_rules_text.cache_clear()
