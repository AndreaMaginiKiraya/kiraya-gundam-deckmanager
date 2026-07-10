# kiraya-gundam-deckmanager-mcp

An MCP server for the Gundam Card Game: search the card database, validate
and analyze decks against the official rules (including the current
banned/restricted list), render decks as images with stat breakdowns, and
manage saved decklists — all as tools callable from an MCP client.

## Tools

| Tool | Purpose |
|------|---------|
| `ping` | health check |
| `search_cards` | filter by name, color, type, cost, trait, set |
| `get_card` | fetch a single card by id |
| `list_sets` / `list_traits` / `list_card_types` / `list_colors` | discovery |
| `validate_deck` | enforce official construction rules (50/10, 1-2 colors, max 4 copies per card number, optional banned/restricted list) |
| `analyze_deck` | cost curve, color/type breakdown, top traits, pilot-to-linkable-Unit counts |
| `suggest_synergies` | trait-overlap-based card suggestions |
| `render_deck_image` | PNG render of a deck (card grid + optional stat panels) |
| `list_decks` / `get_deck` / `save_deck` | manage saved decklists under `data/decks/` |
| `update_card_data` | refresh the local card database from upstream sources, live |

## Card data

Card text/stats are merged from two upstream sources at sync time
(`apitcg` wins where both have a set; the other fills gaps):

- [`apitcg/gundam-tcg-data`](https://github.com/apitcg/gundam-tcg-data) (GitHub)
- [`deckbuilder.egmanevents.com`](https://deckbuilder.egmanevents.com) (public API)

Card art is always fetched directly from `gundam-gcg.com`'s own CDN via a
deterministic `<card_code>.webp` path (through the `images.weserv.nl` resize
proxy) — never trusted from either upstream source, both of which have been
observed suggesting image paths that don't actually resolve.

Official game rules and the current banned/restricted list live in
`data/rules/` (`comprehensive_rules.md`, `banned_restricted_list.md`,
`banlist.json`); `validate_deck`'s `enforce_banlist` flag reads
`banlist.json`. Re-derive these from a fresh PDF if the rules or list ever
change.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Populate the card database (data/cards/en/*.json)
python scripts/update_cards.py

# Run tests
pytest

# Lint
ruff check .

# Try it interactively with the MCP Inspector
mcp dev server.py

# Or run the server directly (waits for an MCP client on stdio)
python -m kiraya_gundam_deckmanager
```

## Connecting to an MCP client

The repo ships with a `.mcp.json` pointing at this venv's Python. From a
Claude Code session opened in this directory, the server is auto-suggested;
accept it once, then use `/mcp` to confirm it's loaded and to reconnect
after editing the server's source (the running process doesn't hot-reload).

To register it globally (available from any directory):

```bash
claude mcp add kiraya-gundam-deckmanager --scope user \
  /path/to/kiraya-gundam-deckmanager-mcp/.venv/bin/python -- -m kiraya_gundam_deckmanager
```

## Layout

```
.mcp.json                     # how an MCP client spawns the server
pyproject.toml                # project metadata + deps
scripts/
  update_cards.py             # CLI wrapper over sync.sync_all() (also an MCP tool)
data/
  cards/en/                   # synced card JSON, one file per set
  cards/images/                # on-disk card-art cache (gitignored, regenerable)
  rules/                       # official rules + banned/restricted list
  decks/                       # saved decklists (plain text) + rendered PNGs
src/kiraya_gundam_deckmanager/
  __main__.py                  # entrypoint
  server.py                    # FastMCP instance + @mcp.tool() registrations
  tools.py                     # tool implementations (pure functions, JSON-serializable)
  render.py                    # deck image rendering (returns PNG bytes, not JSON)
  sync.py                      # merges the two upstream card-data sources
  data.py                      # data loading, parsing, queries, disk-cache
  config.py                    # env-driven settings + logging setup
tests/
  test_smoke.py                 # unit tests over data.py + tools.py + render.py
```

## License

The code in this repo is for personal/educational use. Card data is property
of Bandai; the upstream datasets are fan-curated and not officially
licensed. Do not use this for commercial products.
