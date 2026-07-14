"""MCP tool implementations.

Functions decorated by `@mcp.tool()` in server.py are exposed to clients.
Tools should be thin: parse args, delegate to data.py, return JSON-serializable data.
"""
from __future__ import annotations

import math
import re
from collections import Counter
from datetime import date

import yaml

from . import data, gamelog

# Official Gundam Card Game rules (Comprehensive Rules v1.8.0 / 2026-06-12,
# see data/rules/comprehensive_rules.md, section 6 "Preparing to Play")
MAIN_DECK_SIZE = 50
RESOURCE_DECK_SIZE = 10
MAX_COPIES_PER_ID = 4
MAX_DECK_COLORS = 2
RECOMMENDED_DISTRIBUTION = {
    "UNIT": (25, 28),
    "PILOT": (6, 8),
    "COMMAND": (8, 10),
    "BASE": (4, 6),
}

_PARALLEL_SUFFIX_RE = re.compile(r"-p\d+$", re.IGNORECASE)


def _canonical_card_number(card_id: str) -> str:
    """Strip parallel-print suffixes (e.g. 'GD01-004-p1' -> 'GD01-004').

    Alternate-art/parallel printings share the same card number and count
    together against the max-copies-per-deck limit.
    """
    return _PARALLEL_SUFFIX_RE.sub("", card_id)


def search_cards_impl(
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
) -> list[dict]:
    results = data.find_cards(
        query=query,
        effect=effect,
        color=color,
        card_type=card_type,
        cost=cost,
        cost_min=cost_min,
        cost_max=cost_max,
        level=level,
        level_min=level_min,
        level_max=level_max,
        ap_min=ap_min,
        ap_max=ap_max,
        hp_min=hp_min,
        hp_max=hp_max,
        trait=trait,
        set_id=set_id,
        limit=limit,
    )
    return [data.card_to_dict(c) for c in results]


def get_card_impl(card_id: str) -> dict | None:
    card = data.get_card_by_id(card_id)
    return data.card_to_dict(card) if card else None


def list_sets_impl() -> list[dict]:
    return list(data.list_unique_sets())


def list_traits_impl() -> list[str]:
    return list(data.list_unique_traits())


def list_card_types_impl() -> list[str]:
    return list(data.list_unique_card_types())


def list_colors_impl() -> list[str]:
    return list(data.list_unique_colors())


def _resolve_deck(deck: dict[str, int]) -> tuple[list[tuple[data.Card, int]], list[str]]:
    """Resolve a {card_id: count} dict to (resolved_cards, missing_ids)."""
    resolved: list[tuple[data.Card, int]] = []
    missing: list[str] = []
    for card_id, count in deck.items():
        card = data.get_card_by_id(card_id)
        if card is None:
            missing.append(card_id)
        else:
            resolved.append((card, count))
    return resolved, missing


def validate_deck_impl(
    main_deck: dict[str, int],
    resource_deck: dict[str, int] | None = None,
    enforce_banlist: bool = False,
) -> dict:
    """Validate a Gundam Card Game deck against the official format rules.

    `resource_deck` is optional: pass None (or omit it) to skip resource-deck
    checks entirely (useful when you only care about the main deck). Pass an
    explicit dict, including {}, to have it validated (must be exactly 10
    RESOURCE cards).

    If `enforce_banlist` is True, also checks the deck against the current
    official banned/restricted/banned-pair list (data/rules/banlist.json).
    This is off by default since the list is tournament-specific and
    changes over time; casual play may not care about it.
    """
    errors: list[str] = []
    warnings: list[str] = []

    main_resolved, main_missing = _resolve_deck(main_deck)
    for cid in main_missing:
        errors.append(f"Main deck contains unknown card id: {cid}")

    main_count = sum(c for _, c in main_resolved)
    if main_count != MAIN_DECK_SIZE:
        errors.append(f"Main deck has {main_count} cards, expected exactly {MAIN_DECK_SIZE}.")

    resource_resolved: list[tuple[data.Card, int]] = []
    resource_count: int | None = None
    if resource_deck is not None:
        resource_resolved, resource_missing = _resolve_deck(resource_deck)
        for cid in resource_missing:
            errors.append(f"Resource deck contains unknown card id: {cid}")
        resource_count = sum(c for _, c in resource_resolved)
        if resource_count != RESOURCE_DECK_SIZE:
            errors.append(
                f"Resource deck has {resource_count} cards, expected exactly {RESOURCE_DECK_SIZE}."
            )

    colors_used: dict[str, list[str]] = {}
    for card, _ in main_resolved:
        if card.color:
            colors_used.setdefault(card.color, []).append(card.id)
    if len(colors_used) > MAX_DECK_COLORS:
        errors.append(
            f"Main deck uses {len(colors_used)} colors ({', '.join(sorted(colors_used))}); "
            f"a deck must be built with only 1 or 2 colors."
        )

    copies_by_number: Counter[str] = Counter()
    names_by_number: dict[str, str] = {}
    for card, count in main_resolved:
        number = _canonical_card_number(card.id)
        copies_by_number[number] += count
        names_by_number[number] = card.name
        if (card.card_type or "").upper() == "RESOURCE":
            errors.append(
                f"{card.id} ({card.name}) is a RESOURCE card and cannot be in the main deck."
            )

    for number, total in copies_by_number.items():
        if total > MAX_COPIES_PER_ID:
            errors.append(
                f"{number} ({names_by_number[number]}) has {total} total copies "
                f"across printings in main deck (max {MAX_COPIES_PER_ID})."
            )

    banlist_info: dict = {"enforced": enforce_banlist}
    if enforce_banlist:
        banlist = data.load_banlist()
        present_numbers = set(copies_by_number)
        banlist_info["effective_date"] = banlist.get("effective_date")

        for number, count in copies_by_number.items():
            banned_name = banlist.get("banned", {}).get(number)
            if banned_name is not None:
                errors.append(
                    f"{number} ({banned_name}) is banned as of "
                    f"{banlist.get('effective_date', '?')} and cannot be used."
                )
            restriction = banlist.get("restricted", {}).get(number)
            if restriction and count > restriction["limit"]:
                errors.append(
                    f"{number} ({restriction['name']}) is restricted to "
                    f"{restriction['limit']} copies as of {banlist.get('effective_date', '?')} "
                    f"(has {count})."
                )

        for pair in banlist.get("banned_pairs", []):
            if pair["a"] in present_numbers and pair["b"] in present_numbers:
                errors.append(
                    f"{pair['a']} ({pair['a_name']}) and {pair['b']} ({pair['b_name']}) "
                    f"are a banned pair and cannot be used together."
                )

        for group in banlist.get("banned_pair_groups", []):
            members = group.get("members", {})
            present = sorted(n for n in members if n in present_numbers)
            if len(present) > 1:
                listed = ", ".join(f"{n} ({members[n]})" for n in present)
                errors.append(
                    f"Deck contains {len(present)} cards from a banned-pair group "
                    f"({group.get('description', 'restricted group')}): {listed}. "
                    f"Only one card number from this group is allowed."
                )

    for card, _ in resource_resolved:
        if (card.card_type or "").upper() != "RESOURCE":
            errors.append(
                f"{card.id} ({card.name}) is not a RESOURCE card "
                "and cannot be in the resource deck."
            )

    type_breakdown: Counter[str] = Counter()
    for card, count in main_resolved:
        type_breakdown[(card.card_type or "UNKNOWN").upper()] += count

    for card_type, (lo, hi) in RECOMMENDED_DISTRIBUTION.items():
        actual = type_breakdown.get(card_type, 0)
        if not (lo <= actual <= hi):
            warnings.append(
                f"{card_type}: {actual} cards (recommended {lo}-{hi})"
            )

    return {
        "is_legal": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "main_count": main_count,
        "resource_count": resource_count,
        "type_breakdown": dict(type_breakdown),
        "colors_used": sorted(colors_used),
        "banlist": banlist_info,
    }


def _pilot_link_counts(resolved: list[tuple[data.Card, int]]) -> list[tuple[str, int]]:
    """For each pilot-capable card in the deck (PILOT cards, plus COMMAND
    cards with a Pilot mode), count total copies of Units in the deck whose
    link condition it satisfies. See data.unit_linkable_by for the matching
    approximation. Sorted descending by count."""
    units = [(card, count) for card, count in resolved if (card.card_type or "").upper() == "UNIT"]

    pilots: list[tuple[str, str, str | None]] = []  # (display_label, pilot_name, pilot_trait)
    for card, _ in resolved:
        identity = data.pilot_identity(card)
        if identity is None:
            continue
        pilot_name, pilot_trait = identity
        is_real_pilot = (card.card_type or "").upper() == "PILOT"
        label = card.name if is_real_pilot else f"{card.name} ({pilot_name})"
        pilots.append((label, pilot_name, pilot_trait))

    counts = [
        (
            label,
            sum(
                count
                for unit_card, count in units
                if data.unit_linkable_by(unit_card.link, name, trait)
            ),
        )
        for label, name, trait in pilots
    ]
    counts.sort(key=lambda kv: -kv[1])
    return counts


def analyze_deck_impl(main_deck: dict[str, int]) -> dict:
    """Compute statistics on a main deck: size, cost curve, color/type
    breakdown, top traits, and how many Units in the deck each pilot-capable
    card (PILOT, or COMMAND with a Pilot mode) can link with."""
    resolved, missing = _resolve_deck(main_deck)
    total = sum(c for _, c in resolved)

    cost_curve: Counter[int | str] = Counter()
    color_breakdown: Counter[str] = Counter()
    type_breakdown: Counter[str] = Counter()
    trait_counter: Counter[str] = Counter()

    weighted_cost_sum = 0
    counted_for_avg = 0
    for card, count in resolved:
        if card.cost is None:
            cost_curve["?"] += count
        else:
            cost_curve[card.cost] += count
            weighted_cost_sum += card.cost * count
            counted_for_avg += count
        color_breakdown[card.color or "?"] += count
        type_breakdown[(card.card_type or "?").upper()] += count
        for t in data.extract_traits(card.trait):
            trait_counter[data.canonicalize_trait(t)] += count

    avg_cost = round(weighted_cost_sum / counted_for_avg, 2) if counted_for_avg else None
    sorted_cost_curve = sorted(cost_curve.items(), key=lambda kv: (isinstance(kv[0], str), kv[0]))

    return {
        "total_cards": total,
        "average_cost": avg_cost,
        "cost_curve": dict(sorted_cost_curve),
        "color_breakdown": dict(color_breakdown),
        "type_breakdown": dict(type_breakdown),
        "top_traits": trait_counter.most_common(10),
        "pilot_link_counts": _pilot_link_counts(resolved),
        "missing_card_ids": missing,
    }


def suggest_synergies_impl(card_ids: list[str], limit: int = 10) -> list[dict]:
    """Suggest cards that share traits with the given card list.

    Ranking: cards are scored by the number of distinct traits they share
    with the input set. Seeds are excluded by *card number*, and results
    are deduped by card number too — parallel/alt-art printings (-p1/-p2)
    are the same card as their base print, so suggesting them adds noise,
    not options.
    """
    seed_traits: set[str] = set()
    seed_numbers = {_canonical_card_number(cid).casefold() for cid in card_ids}
    for cid in card_ids:
        c = data.get_card_by_id(cid)
        if c:
            seed_traits.update(t.casefold() for t in data.extract_traits(c.trait))
    if not seed_traits:
        return []

    # One candidate per card number, preferring the base (non-parallel) print.
    by_number: dict[str, tuple[int, data.Card]] = {}
    for c in data.get_all_cards():
        number = _canonical_card_number(c.id).casefold()
        if number in seed_numbers:
            continue
        card_traits = {t.casefold() for t in data.extract_traits(c.trait)}
        overlap = len(card_traits & seed_traits)
        if overlap <= 0:
            continue
        current = by_number.get(number)
        if current is None or len(c.id) < len(current[1].id):
            by_number[number] = (overlap, c)

    scored = sorted(by_number.values(), key=lambda x: (-x[0], x[1].id))
    return [
        {**data.card_to_dict(card), "shared_trait_count": score}
        for score, card in scored[:limit]
    ]


def get_banlist_impl() -> dict:
    """Return the current official banned/restricted/banned-pair list as
    parsed from data/rules/banlist.json (empty structure if missing)."""
    return dict(data.load_banlist())


def compare_decks_impl(
    deck_a: dict[str, int],
    deck_b: dict[str, int],
    label_a: str = "deck_a",
    label_b: str = "deck_b",
) -> dict:
    """Diff two decks card-by-card and side-by-side on the analytics that
    matter for archetype comparison (curve, colors, types, traits)."""

    def _entry(card_id: str) -> dict:
        card = data.get_card_by_id(card_id)
        return {"id": card_id, "name": card.name if card else "?"}

    only_a = [
        {**_entry(cid), "count": n} for cid, n in sorted(deck_a.items()) if cid not in deck_b
    ]
    only_b = [
        {**_entry(cid), "count": n} for cid, n in sorted(deck_b.items()) if cid not in deck_a
    ]
    shared_ids = sorted(set(deck_a) & set(deck_b))
    count_differs = [
        {**_entry(cid), "count_a": deck_a[cid], "count_b": deck_b[cid]}
        for cid in shared_ids
        if deck_a[cid] != deck_b[cid]
    ]
    shared_same_count = [
        {**_entry(cid), "count": deck_a[cid]} for cid in shared_ids if deck_a[cid] == deck_b[cid]
    ]

    def _summary(label: str, deck: dict[str, int]) -> dict:
        stats = analyze_deck_impl(deck)
        return {
            "label": label,
            "total_cards": stats["total_cards"],
            "average_cost": stats["average_cost"],
            "cost_curve": stats["cost_curve"],
            "color_breakdown": stats["color_breakdown"],
            "type_breakdown": stats["type_breakdown"],
            "top_traits": stats["top_traits"][:5],
        }

    return {
        "deck_a": _summary(label_a, deck_a),
        "deck_b": _summary(label_b, deck_b),
        "only_in_a": only_a,
        "only_in_b": only_b,
        "count_differs": count_differs,
        "shared_same_count": shared_same_count,
    }


def opening_hand_odds_impl(
    main_deck: dict[str, int],
    target_card_ids: list[str],
    min_copies: int = 1,
    hand_size: int = 5,
) -> dict:
    """Exact hypergeometric odds of drawing the target cards in the opening
    hand.

    `target_card_ids` defines the success group (e.g. every cost-1 Unit in
    the deck); copies of all listed ids are pooled together. Returns
    P(at least `min_copies` of the group in a `hand_size`-card hand) plus
    the full probability distribution. Deck size is whatever the deck sums
    to (no 50-card assumption), so this also works mid-build.
    """
    deck_size = sum(main_deck.values())
    if deck_size <= 0:
        raise ValueError("main_deck is empty")
    if hand_size <= 0 or hand_size > deck_size:
        raise ValueError(f"hand_size must be between 1 and deck size ({deck_size})")

    target_set = {cid.casefold() for cid in target_card_ids}
    successes = sum(n for cid, n in main_deck.items() if cid.casefold() in target_set)

    total_hands = math.comb(deck_size, hand_size)
    distribution: dict[int, float] = {}
    for k in range(0, min(successes, hand_size) + 1):
        ways = math.comb(successes, k) * math.comb(deck_size - successes, hand_size - k)
        distribution[k] = round(ways / total_hands, 4)

    p_at_least = sum(
        p for k, p in distribution.items() if k >= min_copies
    )
    return {
        "deck_size": deck_size,
        "target_copies_in_deck": successes,
        "hand_size": hand_size,
        "min_copies": min_copies,
        "probability_at_least": round(p_at_least, 4),
        "distribution": distribution,
    }


_AMBIGUOUS_CARD_NOTE = (
    "ambiguous: multiple printings share this name; "
    "pin the id from the effects/stats observed in the log"
)


def _carry_over_annotations(old_doc: dict, doc: dict) -> list[str]:
    """Copy hand-made annotations from a previous version of a game record
    into a freshly imported one: pinned card ids (stats re-derived from the
    database, so they stay consistent), custom evidence notes on cards that
    remain ambiguous, study_notes, a result the parser couldn't detect, and
    per-player deck names not re-passed to this import. Returns what was
    carried, for the tool's summary."""
    carried: list[str] = []

    old_cards = old_doc.get("cards") or {}
    for name, entry in doc["cards"].items():
        old_entry = old_cards.get(name)
        if not isinstance(old_entry, dict) or entry.get("id") is not None:
            continue
        if old_entry.get("id"):
            card = data.get_card_by_id(old_entry["id"])
            if card is None:
                continue
            entry["id"] = card.id
            entry["type"] = card.card_type
            for field in ("level", "cost", "ap", "hp"):
                value = getattr(card, field)
                if value is not None:
                    entry[field] = value
            entry.pop("candidates", None)
            entry["note"] = old_entry.get("note") or "pinned in a previous import"
            carried.append(f"cards[{name}].id")
        else:
            old_note = old_entry.get("note")
            if old_note and old_note != _AMBIGUOUS_CARD_NOTE and old_note != entry.get("note"):
                entry["note"] = old_note
                carried.append(f"cards[{name}].note")

    old_notes = old_doc.get("study_notes")
    if old_notes:
        doc["study_notes"] = old_notes
        carried.append("study_notes")

    if doc["game"]["result"] == "unknown":
        old_result = (old_doc.get("game") or {}).get("result")
        if old_result and old_result != "unknown":
            doc["game"]["result"] = old_result
            carried.append("game.result")

    old_players = (old_doc.get("game") or {}).get("players") or {}
    for player, meta in doc["game"]["players"].items():
        old_meta = old_players.get(player)
        if "deck" not in meta and isinstance(old_meta, dict) and old_meta.get("deck"):
            meta["deck"] = old_meta["deck"]
            carried.append(f"game.players[{player}].deck")

    return carried


def _resolve_log_card_name(name: str) -> list[data.Card]:
    """Cards whose printed name exactly matches a name seen in a game log
    (NFKC-folded, so the log's 'Zaku Ⅱ' and an ASCII 'Zaku II' both work).
    Parallel prints and tokens are excluded: a log never distinguishes a
    -p1 from its base print, and tokens aren't deck cards."""
    folded = data.search_fold(name)
    return [
        c
        for c in data.get_all_cards()
        if data.search_fold(c.name) == folded
        and not _PARALLEL_SUFFIX_RE.search(c.id)
        and "TOKEN" not in (c.card_type or "").upper()
    ]


def import_game_log_impl(
    log_text: str,
    name: str,
    result: str | None = None,
    decks: dict[str, str] | None = None,
    overwrite: bool = False,
) -> dict:
    """Convert a chat-exported game log into a YAML record in data/games/.

    Parses the log (see gamelog.parse_game_log), resolves every card name
    seen against the database, and writes data/games/<name>.yaml. Names
    shared by multiple printings can't be auto-resolved from a log — they
    get id: null plus a candidates list, reported back as cards_ambiguous
    so a human (or LLM) can pin the right id by the effects/stats the log
    shows. `decks` optionally maps player -> saved deck name (data/decks/)
    to record which deck each player was on.
    """
    parsed = gamelog.parse_game_log(log_text)
    players = parsed["players"]
    if not players:
        raise ValueError(
            "No players detected in the log; expected setup lines like "
            "'<player>' / 'Choose to play first'."
        )

    cards_index: dict[str, dict] = {}
    ambiguous: dict[str, list[str]] = {}
    not_found: list[str] = []
    colors: dict[str, set[str]] = {p: set() for p in players}
    for card_name, info in sorted(parsed["cards_seen"].items()):
        matches = _resolve_log_card_name(card_name)
        entry: dict = {}
        if len(matches) == 1:
            card = matches[0]
            entry["id"] = card.id
            entry["type"] = card.card_type
            for field in ("level", "cost", "ap", "hp"):
                value = getattr(card, field)
                if value is not None:
                    entry[field] = value
            if card.color and len(info["owners"]) == 1:
                colors[info["owners"][0]].add(card.color)
        elif matches:
            entry["id"] = None
            entry["candidates"] = sorted(c.id for c in matches)
            entry["note"] = _AMBIGUOUS_CARD_NOTE
            ambiguous[card_name] = entry["candidates"]
        else:
            entry["id"] = None
            entry["note"] = "not found in card database"
            not_found.append(card_name)
        if len(info["owners"]) == 1:
            entry["owner"] = info["owners"][0]
        elif info["owners"]:
            entry["owner"] = info["owners"]
        entry["seen"] = info["contexts"]
        cards_index[card_name] = entry

    if result is None:
        result = f"win:{parsed['winner']}" if parsed["winner"] else "unknown"

    doc: dict = {
        "game": {
            "id": name,
            "date_imported": date.today().isoformat(),
            "source": parsed["source_header"] or "chat log",
            "result": result,
            "players": {
                p: {
                    "first_player": p == parsed["first_player"],
                    "mulligan": parsed["mulligans"].get(p, False),
                    **({"colors": sorted(colors[p])} if colors[p] else {}),
                    **({"deck": decks[p]} if decks and p in decks else {}),
                }
                for p in players
            },
        },
        "cards": cards_index,
        "setup": parsed["setup"],
        "turns": parsed["turns"],
        "casualties": parsed["casualties"],
        "shields_tally": parsed["shields_tally"],
        "study_notes": [],
    }
    if parsed["unparsed"]:
        doc["unparsed_lines"] = parsed["unparsed"]

    carried: list[str] = []
    if overwrite:
        old_text = data.load_game_text(name)
        if old_text is not None:
            try:
                old_doc = yaml.safe_load(old_text)
            except yaml.YAMLError:
                old_doc = None
            if isinstance(old_doc, dict):
                carried = _carry_over_annotations(old_doc, doc)

    path = data.save_game_file(name, gamelog.dump_yaml(doc), overwrite=overwrite)
    log_path = data.save_game_log(name, log_text)
    return {
        "path": str(path),
        "log_path": str(log_path),
        "annotations_carried_over": carried,
        "players": players,
        "first_player": parsed["first_player"],
        "result": result,
        "turns": len(parsed["turns"]),
        "actions": sum(len(t["actions"]) for t in parsed["turns"]),
        "cards_resolved": {
            n: e["id"] for n, e in cards_index.items() if e.get("id") is not None
        },
        "cards_ambiguous": ambiguous,
        "cards_not_found": not_found,
        "unparsed_lines": parsed["unparsed"],
        "shields_tally": parsed["shields_tally"],
    }


def search_rules_impl(query: str, limit: int = 10) -> list[str]:
    """Search the Comprehensive Rules text for paragraphs containing `query`
    (case-insensitive, NFKC-folded). Returns up to `limit` matching
    paragraphs, each with its rule numbering intact, so answers can cite
    the exact rule."""
    text = data.load_rules_text()
    if not text:
        return []
    needle = data.search_fold(query)
    matches = []
    for paragraph in re.split(r"\n\s*\n", text):
        paragraph = paragraph.strip()
        if paragraph and needle in data.search_fold(paragraph):
            matches.append(paragraph)
            if len(matches) >= limit:
                break
    return matches
