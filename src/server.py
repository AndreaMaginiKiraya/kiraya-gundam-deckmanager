"""FastMCP server: registers tools for the Gundam Card Game."""
from __future__ import annotations

from mcp.server.fastmcp import FastMCP, Image

if __package__:
    # Normal case: imported as part of the `src` package (`python -m src`,
    # the installed console script, or any other module importing us).
    from . import data, render, sync, tools
else:
    # `mcp dev src/server.py` loads this file standalone via
    # importlib.util.spec_from_file_location, with no parent package, so
    # the relative import above would fail. Fall back to an absolute import
    # after putting the repo root on sys.path.
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import data, render, sync, tools

mcp = FastMCP("kiraya-gundam-deckmanager")


@mcp.tool()
def ping() -> str:
    """Health-check tool. Returns 'pong'."""
    return "pong"


@mcp.tool()
def search_cards(
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
    """Search Gundam Card Game cards with optional filters.

    Args:
        query: Substring of card name (case-insensitive; roman numerals are
               normalized, so "Zaku II" matches the printed "Zaku Ⅱ").
        effect: Substring of effect text (case-insensitive). Example:
                "Blocker", "Breach", "Repair".
        color: Exact color match. Use list_colors to see valid values.
        card_type: Exact type. Use list_card_types to see valid values.
        cost: Exact resource cost.
        cost_min / cost_max: Inclusive resource-cost bounds.
        level: Exact card level.
        level_min / level_max: Inclusive level bounds (e.g. level_max=5 for
                               everything caught by "deal 3 damage to all
                               Units that are Lv.5 or lower").
        ap_min / ap_max / hp_min / hp_max: Inclusive stat bounds; cards
                                           without that stat never match.
        trait: Substring of trait field, e.g. "Earth Federation", "Zeon".
        set_id: Filter by set: gd01..gd05, st01..st10, eb01, beta, promotion.
        limit: Maximum number of cards to return (default 50).
    """
    return tools.search_cards_impl(
        query=query, effect=effect, color=color, card_type=card_type, cost=cost,
        cost_min=cost_min, cost_max=cost_max, level=level, level_min=level_min,
        level_max=level_max, ap_min=ap_min, ap_max=ap_max, hp_min=hp_min,
        hp_max=hp_max, trait=trait, set_id=set_id, limit=limit,
    )


@mcp.tool()
def get_card(card_id: str) -> dict | None:
    """Fetch a single card by its exact id (e.g. "GD01-001")."""
    return tools.get_card_impl(card_id)


@mcp.tool()
def list_sets() -> list[dict]:
    """List all available sets/expansions with their id and full name."""
    return tools.list_sets_impl()


@mcp.tool()
def list_traits() -> list[str]:
    """List all unique traits in the dataset (e.g. Earth Federation, Zeon, Newtype)."""
    return tools.list_traits_impl()


@mcp.tool()
def list_card_types() -> list[str]:
    """List all unique card types (UNIT, PILOT, COMMAND, BASE, RESOURCE)."""
    return tools.list_card_types_impl()


@mcp.tool()
def list_colors() -> list[str]:
    """List all unique colors used by cards (Blue, Red, Green, White)."""
    return tools.list_colors_impl()


@mcp.tool()
def validate_deck(
    main_deck: dict[str, int],
    resource_deck: dict[str, int] | None = None,
    enforce_banlist: bool = False,
) -> dict:
    """Validate a deck against official Gundam Card Game format rules.

    Args:
        main_deck: Mapping of card id -> count for the 50-card main deck.
                   Example: {"GD01-001": 4, "GD01-002": 2, ...}
        resource_deck: Mapping of card id -> count for the 10-card resource
                       deck. Optional: omit or pass null to skip resource-deck
                       checks entirely; pass an explicit dict (including {})
                       to have it validated (must be exactly 10 RESOURCE cards).
        enforce_banlist: If True, also check the deck against the current
                         official banned/restricted/banned-pair list. Off by
                         default (tournament-specific, changes over time).

    Returns:
        Dict with `is_legal`, `errors`, `warnings`, counts, type breakdown,
        colors used, and banlist status. `resource_count` is null when
        resource_deck wasn't validated. Rules enforced: 50 main / 10
        resource, max 4 copies per card number in main (parallel/alt-art
        printings share the same number), 1-2 colors per deck, only
        RESOURCE cards in resource deck, no RESOURCE cards in main deck.
        With enforce_banlist=True: no banned cards, restricted-card counts
        respected, no banned pairs/groups together.
    """
    return tools.validate_deck_impl(main_deck, resource_deck, enforce_banlist=enforce_banlist)


@mcp.tool()
def analyze_deck(main_deck: dict[str, int]) -> dict:
    """Compute deck statistics: cost curve, color/type breakdown, top traits,
    and pilot_link_counts (for each PILOT/Pilot-capable COMMAND card, how
    many copies of Units in the deck it can link with — approximate, see
    data.unit_linkable_by)."""
    return tools.analyze_deck_impl(main_deck)


@mcp.tool()
def suggest_synergies(card_ids: list[str], limit: int = 10) -> list[dict]:
    """Suggest cards that share traits with the given card ids.

    Useful when filling out a deck around a thematic core.
    Returned cards are scored by the number of overlapping traits.
    """
    return tools.suggest_synergies_impl(card_ids, limit=limit)


@mcp.tool()
def render_deck_image(
    main_deck: dict[str, int],
    resource_deck: dict[str, int] | None = None,
    title: str | None = None,
    show_stats: bool = False,
    save_as: str | None = None,
) -> Image:
    """Render a deck as a PNG image for quick visual review.

    Cards are shown as one continuous grid in canonical deck order —
    UNIT → PILOT → COMMAND → BASE, ascending level then cost within each
    type — each with a red circular badge in the top-right corner giving
    the copy count.

    Args:
        main_deck: Mapping of card id -> count.
        resource_deck: Optional mapping of card id -> count; omit to render
                       the main deck only.
        title: Optional deck name, drawn centered at the top of the image.
               When rendering a deck loaded from data/decks/<name>.txt, pass
               a human-readable version of <name> here.
        show_stats: If True, draw a row of 4 compact histograms below the
                    card grid: cost curve (with average cost in the title),
                    colors, types, and top 5 traits.
        save_as: Optional deck name. If given, also writes the PNG to
                 data/decks/<save_as>.png (overwriting if it already
                 exists) alongside the inline image returned below --
                 matches the saved-decklist naming convention, so passing
                 the same name used with save_deck keeps the .txt/.png
                 pair together.
    """
    png_bytes = render.render_deck_image(
        main_deck, resource_deck, title=title, show_stats=show_stats
    )
    if save_as is not None:
        data.save_deck_image(save_as, png_bytes)
    return Image(data=png_bytes, format="png")


@mcp.tool()
def list_decks() -> list[str]:
    """List saved decklist names in data/decks/, including subfolders
    (e.g. 'meta/bg_oyw' for reference decks kept under data/decks/meta/).

    Use these names with get_deck to load a deck without re-typing it.
    """
    return data.list_deck_files()


@mcp.tool()
def get_deck(name: str) -> dict[str, int]:
    """Load a saved decklist by name from data/decks/<name>.txt.

    Subfolder names work too (e.g. 'meta/bg_oyw'). Returns a
    main_deck-shaped mapping of card id -> count, ready to pass into
    validate_deck, analyze_deck, suggest_synergies, or render_deck_image.
    """
    return data.load_deck(name)


@mcp.tool()
def save_deck(name: str, main_deck: dict[str, int]) -> str:
    """Save a deck to data/decks/<name>.txt, overwriting if it already exists.

    Subfolder names are allowed and created as needed (e.g. 'meta/x').
    Uses the plain '<count> <card_id> <name...>' format (matches
    egmanevents.com's deckbuilder export/import format), with lines in
    canonical deck order (UNIT → PILOT → COMMAND → BASE, ascending
    level/cost). Returns the saved file path.
    """
    path = data.save_deck(name, main_deck)
    return str(path)


@mcp.tool()
def delete_deck(name: str) -> list[str]:
    """Delete a saved deck: removes data/decks/<name>.txt and its paired
    <name>.png render if present. Returns the paths removed. Errors if the
    deck doesn't exist."""
    return data.delete_deck(name)


@mcp.tool()
def rename_deck(old_name: str, new_name: str) -> list[str]:
    """Rename a saved deck (its .txt and paired .png, if any). Refuses to
    overwrite an existing deck. Subfolder names work on both sides, so this
    also moves decks between folders (e.g. 'bg_oyw' -> 'meta/bg_oyw').
    Returns the new paths."""
    return data.rename_deck(old_name, new_name)


@mcp.tool()
def get_banlist() -> dict:
    """Return the current official banned/restricted list as structured data:
    banned card numbers, restricted numbers with their copy limits, banned
    pairs, and banned-pair groups — with published/effective dates. Same
    data validate_deck's enforce_banlist flag checks against."""
    return tools.get_banlist_impl()


@mcp.tool()
def compare_decks(
    deck_a: dict[str, int],
    deck_b: dict[str, int],
    label_a: str = "deck_a",
    label_b: str = "deck_b",
) -> dict:
    """Compare two decks: card diff plus side-by-side analytics.

    Returns per-deck summaries (total, average cost, cost curve, colors,
    types, top 5 traits) and the card-level diff: only_in_a / only_in_b /
    count_differs / shared_same_count. Pass get_deck output for saved decks
    and set label_a/label_b to the deck names for readable output.
    """
    return tools.compare_decks_impl(deck_a, deck_b, label_a=label_a, label_b=label_b)


@mcp.tool()
def opening_hand_odds(
    main_deck: dict[str, int],
    target_card_ids: list[str],
    min_copies: int = 1,
    hand_size: int = 5,
) -> dict:
    """Exact hypergeometric odds of seeing target cards in the opening hand.

    Args:
        main_deck: Mapping of card id -> count (any size; uses actual sum).
        target_card_ids: Card ids forming the success group — copies of all
                         listed ids are pooled (e.g. every cost-1 Unit id to
                         ask "chance my turn-1 play shows up").
        min_copies: Minimum successes wanted (default 1).
        hand_size: Cards drawn (default 5, the game's opening hand).

    Returns:
        deck_size, target_copies_in_deck, probability_at_least, and the
        full distribution {k: P(exactly k)}. Useful for mulligan decisions:
        rules 6-2-1-5/6-2-1-6 allow one full-hand redraw.
    """
    return tools.opening_hand_odds_impl(
        main_deck, target_card_ids, min_copies=min_copies, hand_size=hand_size
    )


@mcp.tool()
def search_rules(query: str, limit: int = 10) -> list[str]:
    """Search the official Comprehensive Rules text for matching paragraphs.

    Case-insensitive substring search; each hit keeps its rule numbering
    (e.g. '6-2-1-6.') so answers can cite the exact rule. Examples:
    "redraw", "high-maneuver", "EX Resource", "breach".
    """
    return tools.search_rules_impl(query, limit=limit)


@mcp.tool()
def update_card_data(only: str | None = None) -> dict:
    """Refresh the local card database from upstream sources and pick up
    the changes immediately (no reconnect needed).

    Merges apitcg/gundam-tcg-data (primary) with deckbuilder.egmanevents.com
    (fills sets apitcg doesn't have yet), always rebuilding card art URLs
    against gundam-gcg.com's own CDN. Clears every in-memory cache
    afterward so subsequent tool calls in this same session see the new
    data right away.

    Args:
        only: Optional set id (e.g. "gd05") to refresh just that set instead
              of everything.

    Returns:
        {"sets": {set_id: card_count, ...}, "total_cards": N}
    """
    summary = sync.sync_all(only=only)
    data.clear_cache()
    return summary
