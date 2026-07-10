"""FastMCP server: registers tools for the Gundam Card Game."""
from __future__ import annotations

from mcp.server.fastmcp import FastMCP, Image

from . import data, render, sync, tools

mcp = FastMCP("kiraya-gundam-deckmanager")


@mcp.tool()
def ping() -> str:
    """Health-check tool. Returns 'pong'."""
    return "pong"


@mcp.tool()
def search_cards(
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
    """Search Gundam Card Game cards with optional filters.

    Args:
        query: Substring of card name (case-insensitive). Example: "gundam".
        color: Exact color match. Use list_colors to see valid values.
        card_type: Exact type. Use list_card_types to see valid values.
        cost: Exact resource cost.
        cost_min: Minimum resource cost (inclusive).
        cost_max: Maximum resource cost (inclusive).
        trait: Substring of trait field, e.g. "Earth Federation", "Zeon".
        set_id: Filter by set: gd01, gd02, st01..st06, beta, promotion.
        limit: Maximum number of cards to return (default 50).
    """
    return tools.search_cards_impl(
        query=query, color=color, card_type=card_type, cost=cost,
        cost_min=cost_min, cost_max=cost_max, trait=trait, set_id=set_id, limit=limit,
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
) -> Image:
    """Render a deck as a PNG image for quick visual review.

    Cards are shown as one continuous grid, in the same order as the input
    dict (no grouping by type), each with a red circular badge in the
    top-right corner giving the copy count.

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
    """
    png_bytes = render.render_deck_image(
        main_deck, resource_deck, title=title, show_stats=show_stats
    )
    return Image(data=png_bytes, format="png")


@mcp.tool()
def list_decks() -> list[str]:
    """List saved decklist names available in data/decks/ (without extension).

    Use these names with get_deck to load a deck without re-typing it.
    """
    return data.list_deck_files()


@mcp.tool()
def get_deck(name: str) -> dict[str, int]:
    """Load a saved decklist by name from data/decks/<name>.txt.

    Returns a main_deck-shaped mapping of card id -> count, ready to pass
    into validate_deck, analyze_deck, suggest_synergies, or render_deck_image.
    """
    return data.load_deck(name)


@mcp.tool()
def save_deck(name: str, main_deck: dict[str, int]) -> str:
    """Save a deck to data/decks/<name>.txt, overwriting if it already exists.

    Uses the plain '<count> <card_id> <name...>' format (matches
    egmanevents.com's deckbuilder export/import format). Returns the saved
    file path.
    """
    path = data.save_deck(name, main_deck)
    return str(path)


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
