# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

An MCP server (`kiraya-gundam-deckmanager-mcp`) that exposes card search,
deck validation, deck analysis, deck comparison, opening-hand odds, deck
image rendering, saved-decklist management, rules-text search, and live
card-database refresh for the Gundam Card Game (GCG), backed by a local
JSON dataset merged from two upstream sources. It's registered with this
Claude Code instance already (see `.mcp.json`) — `search_cards` (name,
effect text, cost/level/AP/HP bounds...), `get_card`, `validate_deck`,
`get_banlist`, `analyze_deck`, `compare_decks`, `opening_hand_odds`,
`suggest_synergies`, `render_deck_image`,
`list_decks`/`get_deck`/`save_deck`/`delete_deck`/`rename_deck`,
`search_rules`, `update_card_data`, `import_game_log`/`list_games`
(played-games knowledge base), etc. are available as tools directly,
no need to grep the data files by hand. Prefer these MCP tools over
reading `data/` directly for any Gundam-related request.

## Commands

```bash
# Setup
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

# Populate/refresh the card database (data/cards/en/*.json)
python -m src.update_cards               # merges apitcg + egmanevents
python -m src.update_cards --only gd05   # scope to one set

# Tests
pytest                              # full suite
pytest tests/test_smoke.py::test_validate_deck_rejects_more_than_two_colors  # single test

# Lint
ruff check .

# Run/inspect the server
mcp dev src/server.py                # MCP Inspector, interactive
python -m src   # raw stdio server (what .mcp.json launches)
```

## Architecture

- `data.py` — loads every `data/cards/en/*.json` set file into a single
  deduped-by-id tuple of `Card` dataclasses (`_load_all()`, `lru_cache`d).
  Owns all raw-field parsing/cleanup (HTML-escaped effect text, `"-"` →
  `None` for absent stats, color title-casing, rarity padding stripped to
  `C+`/`LR++`, zone folded to canonical `Space / Earth`) and all
  filtering/lookup logic (`find_cards`, `get_card_by_id`, `list_unique_*`).
  Name/effect search goes through `search_fold()` (NFKC + casefold) so an
  ASCII "Zaku II" query matches the printed roman-numeral "Zaku Ⅱ" — keep
  any new text matching on that path. Deck-file access goes through
  `_deck_path()`, which allows subfolder names (`meta/x`) but rejects
  anything escaping `data/decks/` (the name comes from the MCP client).
  `clear_cache()` drops every `lru_cache` in the module — called by the
  `update_card_data` tool after a sync so the running server sees fresh
  data immediately.
- `tools.py` — pure functions implementing each MCP tool (`search_cards_impl`,
  `validate_deck_impl`, `analyze_deck_impl`, `suggest_synergies_impl`, ...).
  This is where GCG deck-construction rules live (see below). No MCP-specific
  code here — these are plain functions, unit-tested directly in
  `tests/test_smoke.py` without spinning up the server.
- `server.py` — `FastMCP` instance; each `@mcp.tool()` function is a thin
  wrapper that calls the matching `tools.py`/`sync.py` impl. Docstrings here
  are what the MCP client (and its LLM) sees, so keep them accurate when the
  underlying rules change. Imports are dual-mode (`if __package__:` branch)
  so `mcp dev src/server.py` can load the file standalone (no parent
  package) as well as `python -m src`/the console script importing it
  normally — see the comment at the top of the file before changing its
  imports.
- `render.py` — the one exception to "tools.py does everything": deck image
  rendering (`render_deck_image`) returns PNG bytes, not JSON, so it lives in
  its own module and is wired into `server.py` via `mcp.server.fastmcp.Image`
  instead of through `tools.py`. Renders one continuous grid in canonical
  deck order (`data.deck_sort_key`: UNIT → PILOT → COMMAND → BASE, then
  ascending level, then cost — same order `save_deck` writes decklist
  lines in) with an optional centered title. Card art
  is disk-cached under `data/cards/images/<card_id>.png` (gitignored,
  regenerable) so re-renders across process restarts don't re-hit the
  network; falls back to a drawn placeholder tile if a fetch/cache miss
  fails. `show_stats=True` draws, below the grid: a row of 3 compact vertical
  histograms (cost curve, colors, types), then a full-width horizontal
  histogram of top 5 traits, then — if any apply — one more horizontal
  histogram of pilot_link_counts. All computed via `tools.analyze_deck_impl`
  — this is the one place `render.py` depends on `tools.py` rather than the
  reverse. Tests must monkeypatch both `render._fetch_image_bytes` and
  `render._IMAGE_CACHE_DIR` (to a tmp dir) to stay hermetic.
- `gamelog.py` — pure text processing for the played-games knowledge base
  (`data/games/`): `parse_game_log()` turns a chat-exported play-by-play
  (Mobile Suit Arena format: "Turn 3 started!", "X deployed", "Battle
  declared: ...") into structured dicts — setup choices, per-turn action
  lists, battles with blockers/action-step plays/outcomes, per-player
  shield tallies and casualties, winner — collecting unrecognized lines
  under `unparsed` instead of dropping them (a nonempty `unparsed_lines`
  in a saved record means the parser needs a new pattern here, plus
  fixture coverage; the raw log is kept as `data/games/<name>.log`
  precisely so records can be regenerated afterwards). `dump_yaml()` is a
  minimal YAML emitter (string scalars JSON-quoted). Card-name→id
  resolution and file writing live in `tools.import_game_log_impl` (names
  shared by multiple printings are saved with `id: null` + `candidates`
  for a human/LLM to pin afterwards — a log can't tell a vanilla Zaku Ⅱ
  from the AP+2 one, though the observed effects usually can);
  `data.save_game_file` guards the path like `_deck_path` and refuses
  overwrites unless asked. Re-importing with `overwrite=True` reads the
  old record back (PyYAML — this is why it's a runtime dependency) and
  carries hand annotations over: pinned ids (stats re-derived from the
  DB), custom card notes, study_notes, result, deck names. See
  `data/games/README.md` for the record schema and the import→pin
  ids→study_notes workflow.
- `sync.py` — merges the two upstream card-data sources into
  `data/cards/en/*.json` (`sync_all(only=None)`). apitcg wins where both
  providers have a set. Always rebuilds card art URLs as
  `<card_code>.webp` against `gundam-gcg.com` directly regardless of what
  either source suggests (see data quirks below). Backs both
  `update_cards.py` (CLI) and the `update_card_data` MCP tool —
  same function, two entrypoints. GitHub's anonymous API limit is
  60 req/hour per IP; on a 403/429 the sync raises a clear RuntimeError —
  set `GITHUB_TOKEN` (see `.env.example`) to raise the limit to 5000/hour.
- `update_cards.py` — thin CLI wrapper over `sync.sync_all()`, runnable as
  `python -m src.update_cards` (also exposed as the
  `update-cards` console script via `pyproject.toml`). `--only SET_ID` scopes
  to one set; `--dump` saves the raw egmanevents API response instead of
  syncing.
- `config.py` — env-driven `Settings` (currently just `log_level`) plus
  `configure_logging()`, called once at process startup
  (`__main__.py`, `update_cards.py`) to wire `LOG_LEVEL` to the
  root logger.

**Remember to reconnect the MCP server (`/mcp` in Claude Code) after editing
`src/*.py`** — the running server subprocess
doesn't hot-reload, so tool schema/behavior changes are invisible until
reconnected. (Card *data* changes are the one exception once
`update_card_data` exists — that tool clears caches in-process, no
reconnect needed for those.)

### Data quirks that matter for correctness

- **Card identity vs. card id**: the game's "card number" (e.g. `GD01-004`)
  is the unit of deck-legality (max 4 copies, banned/restricted lists), but
  parallel/alt-art reprints get a distinct id with a `-p1`/`-p2`/... suffix
  (e.g. `GD01-004-p1`) while representing the *same* card number. Anything
  doing copy-count enforcement must canonicalize via
  `tools._canonical_card_number()`, not compare raw ids.
- **Cross-set id collisions**: the "Beta" test edition reused card numbers
  that later shipped in official sets (`ST01-001` appears in both
  `beta.json` and `st01.json`). `data._load_all()` dedupes by id, keeping
  whichever file sorts last alphabetically — official sets sort after
  `beta.json`, so the real printing wins. If you add a new set file whose
  name would sort *before* `beta.json`, double check this still holds.
- Resource, Base, and token card types are colorless (`color` is `None`) —
  this is correct per the rules, not missing data.
- **`zone` (`Space`, `Earth`, `Space / Earth`) is completely inconsequential
  to gameplay right now, for every card, full stop.** The Comprehensive
  Rules (2-6) define it only as a card attribute that text *could*
  reference — but no card currently deployed in this game does, and no
  general rule gates deployment/attacking/blocking by zone. An
  Earth-only card plays exactly like a Space/Earth one in every matchup;
  there is no scenario today where a unit's zone restricts anything.
  Never flag zone (Earth-only, Space-only) as a playability risk or
  synergy concern in deck analysis or study notes — it's pure flavor
  text with no rules weight until/unless the game changes.
- **Never trust upstream image paths**: both apitcg and egmanevents have
  been observed suggesting card-art filenames that 404 on `gundam-gcg.com`
  (wrong extension, or a bogus `-r<revision>` suffix baked into the path).
  `sync.py` always rebuilds the URL as the plain `<card_code>.webp` instead
  of using whatever path either source provides — this is verified against
  the live site's own markup and is the only pattern that reliably works.
  If a newly-synced set's images render as placeholders in bulk (not just
  missing art for one or two cards), suspect a regression here first.
- **Pilot-capable COMMAND cards**: some COMMAND cards can be paired as a
  Pilot instead of activating their command effect (rule 3-4-6); their
  Pilot-mode name is embedded in the effect text as `【Pilot】[Name]` (not a
  separate field). `data.pilot_identity(card)` extracts this; `analyze_deck`'s
  `pilot_link_counts` (and `render_deck_image`'s "Pilot -> linkable Units"
  panel) use it alongside `data.unit_linkable_by()` to approximate how many
  Unit copies in a deck each pilot can link with. It's a best-effort text
  match (bracket name / trait-in-parens), not strict rules enforcement —
  see the docstrings for the rare cases it can overcount.
- **Game logs can display a Linked Unit under a different name than its
  printed card name**: Mobile Suit Arena renders some Units as
  `<base name> (<Pilot>'s Unit)` or `<base name> (<Pilot> Unit)` once a
  Pilot's Link condition is met, instead of the actual printed name
  (e.g. `Murasame (Andrew Waldfeld Unit)` is really "Waldfeld's Murasame",
  and `Strike Rouge (Kira's Unit)` is really "Kira's Strike Rouge") — seen
  in `data/games/aggro_tekkadan_mono_v1_1/2026-07-17_kiraya-vs-robotech.yaml`.
  `import_game_log` reports these as `cards_not_found` since the display
  name doesn't match any printed name; resolve them by hand from the
  paired Pilot's name in the preceding `Linked pilot:` line (search
  `search_cards` for the base name and check which printing's `link`
  field names that Pilot). Not (yet) worth a general parser heuristic —
  only two examples observed so far, and blindly stripping the
  parenthetical would misfire on real printed names like
  `Strike Rouge (Ootori)`.

### Deck legality rules (`validate_deck_impl`)

Enforced per the official Comprehensive Rules (see `data/rules/`, section 6
"Preparing to Play"): main deck exactly 50 cards, resource deck exactly 10
(only if `resource_deck` is passed — it's optional), max 4 copies per *card
number* (parallel prints share the count), deck built from **1 or 2 colors
only**, no RESOURCE-type cards in the main deck, only RESOURCE-type cards in
the resource deck. `RECOMMENDED_DISTRIBUTION` in `tools.py` is a soft
heuristic (warnings, not errors) — not an official rule.

Banned cards, restricted-count limits, and banned-pair/banned-group
combinations are opt-in via `validate_deck`'s `enforce_banlist` flag (off by
default — it's tournament-specific and changes over time). Sourced from
`data/rules/banlist.json`; keep that file and `banned_restricted_list.md` in
sync when a new list is published.

## Saved decklists

`data/decks/*.txt` holds saved decklists, one per file, in the plain
"`<count> <card_id> <name...>`" per-line format (matches egmanevents.com's
deckbuilder export/import format — keep it exactly that shape, don't add
sections/headers). Only count and id are parsed (`data.parse_decklist_text`,
`data.load_deck`); the trailing name is for human readability. No resource
deck section — resource-deck validation is opt-in via `validate_deck`'s
`resource_deck` param and isn't tracked in these files. Matching `.png`
files alongside each `.txt` are `render_deck_image` output (pass
`save_as=<deck name>` to write the PNG next to the decklist — the MCP
`Image` return type isn't visible in every client's chat UI).

Subfolders are supported everywhere deck names are accepted:
`data/decks/meta/` holds reference decks (official Bandai showcase lists,
meta decks transcribed from tournament sites) as `meta/<name>`, kept apart
from the user's own brews at the top level. `list_decks` recurses;
`rename_deck` moves between folders.

## Game log imports

When the user pastes a game chat log to convert (Mobile Suit Arena
play-by-play), import it with `import_game_log` into `data/games/` — and
**always ask which saved deck they played** if they didn't say (the user
plays as "Kiraya"; see `list_decks` for names, e.g. `aggro_mono_p`), then
pass it as `decks={"Kiraya": "<deck name>"}` and name the record
`<deck name>/YYYY-MM-DD_kiraya-vs-<opponent>` — records are indexed by
the user's deck, one folder per deck. The deck matters beyond
bookkeeping: the importer intersects ambiguous card printings with the
decklist to auto-pin ids. After importing: pin any remaining
`cards_ambiguous` from observed effects/stats (update each `note` with
the evidence), and fill in `study_notes` — the workflow is documented in
`data/games/README.md`.

## Rules reference

`data/rules/` holds the source-of-truth game rules (not derivable from card
data alone):

- `comprehensive_rules.md` — full Comprehensive Rules text (converted from
  `comprehensiverules_en.pdf`).
- `banned_restricted_list.md` / `banlist.json` — current banned/restricted/
  banned-pair list (converted from `bannedlist.pdf`), dated; re-extract if a
  newer PDF is dropped in, and keep the `.md` and `.json` in sync.

Consult these before asserting how a rule works instead of guessing from TCG
conventions in general — this game's specifics (e.g. no color-restricted
resource cards, 1-2 color deck limit, card-number-based copy limit) don't
all match other trading card games. The `search_rules` MCP tool does a
paragraph-level full-text search over `comprehensive_rules.md` and keeps
rule numbering in the results — prefer it over grepping the file by hand;
`get_banlist` returns `banlist.json` parsed.

## Testing conventions

`tests/test_smoke.py` exercises `data.py` + `tools.py` + `render.py` directly
against the real synced dataset (no mocking of card data) — tests assume
`data/cards/en/` is populated. Image-fetch tests monkeypatch
`render._fetch_image_bytes` and `render._IMAGE_CACHE_DIR` to stay hermetic
(no network, no touching the real cache dir).
