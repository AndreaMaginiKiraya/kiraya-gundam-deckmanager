"""MCP tool implementations.

Functions decorated by `@mcp.tool()` in server.py are exposed to clients.
Tools should be thin: parse args, delegate to data.py, return JSON-serializable data.
"""
from __future__ import annotations

import re
from collections import Counter

from . import data

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
    color: str | None = None,
    card_type: str | None = None,
    cost: int | None = None,
    cost_min: int | None = None,
    cost_max: int | None = None,
    trait: str | None = None,
    set_id: str | None = None,
    limit: int = 50,
) -> list[dict]:
    results = data.find_cards(
        query=query,
        color=color,
        card_type=card_type,
        cost=cost,
        cost_min=cost_min,
        cost_max=cost_max,
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
    with the input set. Cards already in `card_ids` are excluded.
    """
    seed_traits: set[str] = set()
    seed_ids = {cid.casefold() for cid in card_ids}
    for cid in card_ids:
        c = data.get_card_by_id(cid)
        if c:
            seed_traits.update(t.casefold() for t in data.extract_traits(c.trait))
    if not seed_traits:
        return []

    scored: list[tuple[int, data.Card]] = []
    for c in data.get_all_cards():
        if c.id.casefold() in seed_ids:
            continue
        card_traits = {t.casefold() for t in data.extract_traits(c.trait)}
        overlap = len(card_traits & seed_traits)
        if overlap > 0:
            scored.append((overlap, c))

    scored.sort(key=lambda x: (-x[0], x[1].id))
    return [
        {**data.card_to_dict(card), "shared_trait_count": score}
        for score, card in scored[:limit]
    ]
