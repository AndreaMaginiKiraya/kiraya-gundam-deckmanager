"""Smoke tests for data layer + tool layer."""
from src import data, render, tools


def test_parse_decklist_text_reads_count_and_id_ignores_name():
    text = """
    # a comment, should be ignored
    4 ST01-005 GM

    2 ST02-016 Corsica Base
    """
    deck = data.parse_decklist_text(text)
    assert deck == {"ST01-005": 4, "ST02-016": 2}


def test_load_deck_reads_saved_file():
    names = data.list_deck_files()
    assert "meta/blue_purple_rush" in names  # reference decks live in data/decks/meta/
    deck = data.load_deck("meta/blue_purple_rush")
    assert sum(deck.values()) == 50
    assert deck["GD01-020"] == 3


def test_dataset_loaded():
    cards = data.get_all_cards()
    assert len(cards) > 100, f"expected real dataset, got {len(cards)} cards"
    assert all(c.id and c.name for c in cards)


def test_search_by_name_case_insensitive():
    a = tools.search_cards_impl(query="GUNDAM")
    b = tools.search_cards_impl(query="gundam")
    assert a == b
    assert any("Gundam" in r["name"] for r in a)


def test_search_by_color_and_type():
    blue_units = tools.search_cards_impl(color="Blue", card_type="UNIT", limit=200)
    assert len(blue_units) > 0
    assert all(r["color"] == "Blue" and r["card_type"] == "UNIT" for r in blue_units)


def test_search_by_cost_range():
    cheap = tools.search_cards_impl(cost_min=1, cost_max=2, limit=200)
    assert len(cheap) > 0
    assert all(1 <= r["cost"] <= 2 for r in cheap if r["cost"] is not None)


def test_search_by_trait():
    feds = tools.search_cards_impl(trait="Earth Federation", limit=200)
    assert len(feds) > 0
    assert all("earth federation" in (r["trait"] or "").casefold() for r in feds)


def test_get_card_by_id():
    card = tools.get_card_impl("GD01-001")
    assert card is not None
    assert card["id"] == "GD01-001"


def test_get_card_by_id_missing():
    assert tools.get_card_impl("DOES-NOT-EXIST") is None


def test_effect_text_is_cleaned():
    card = tools.get_card_impl("GD01-001")
    assert card is not None
    assert "<br>" not in (card["effect"] or "")
    assert "&lt;" not in (card["effect"] or "")


def test_list_sets_returns_known_sets():
    sets = tools.list_sets_impl()
    set_ids = {s["id"] for s in sets}
    assert {"gd01", "gd02", "st01"}.issubset(set_ids)


def test_list_traits_non_empty():
    traits = tools.list_traits_impl()
    assert len(traits) > 0
    assert any("earth federation" in t.casefold() for t in traits)


def test_list_card_types_includes_unit():
    types = tools.list_card_types_impl()
    assert "UNIT" in types
    assert "PILOT" in types


def test_validate_deck_rejects_wrong_size():
    """A deck with too few cards should be flagged illegal."""
    result = tools.validate_deck_impl({"GD01-001": 4}, {})
    assert result["is_legal"] is False
    assert any("50" in e for e in result["errors"])
    assert any("10" in e for e in result["errors"])


def test_validate_deck_rejects_too_many_copies():
    main = {"GD01-001": 5}
    rest_pool = [c for c in data.get_all_cards() if c.id != "GD01-001"][:45]
    for c in rest_pool:
        main[c.id] = 1
    result = tools.validate_deck_impl(main, {})
    assert result["is_legal"] is False
    assert any("max 4" in e for e in result["errors"])


def test_validate_deck_rejects_too_many_copies_across_parallel_prints():
    """Parallel/alt-art printings (e.g. '-p1') share the same card number and
    must count together against the 4-copy limit."""
    variants = [c for c in data.get_all_cards() if c.id.endswith("-p1")]
    base_id, variant = None, None
    for v in variants:
        candidate = v.id[: -len("-p1")]
        if data.get_card_by_id(candidate):
            base_id, variant = candidate, v.id
            break
    assert base_id is not None, "expected at least one base id + '-p1' variant pair in the dataset"

    main = {base_id: 4, variant: 4}
    rest_pool = [c for c in data.get_all_cards() if c.id not in main][:42]
    for c in rest_pool:
        main[c.id] = 1
    result = tools.validate_deck_impl(main, {})
    assert result["is_legal"] is False
    assert any("total copies across printings" in e for e in result["errors"])


def test_validate_deck_rejects_more_than_two_colors():
    by_color: dict[str, list[str]] = {}
    for c in data.get_all_cards():
        if c.color and (c.card_type or "").upper() != "RESOURCE":
            by_color.setdefault(c.color, []).append(c.id)
    assert len(by_color) >= 3, "expected at least 3 colors in the dataset"

    main: dict[str, int] = {}
    chosen_colors = list(by_color.items())[:3]
    for color, ids in chosen_colors:
        for cid in ids[:17]:  # spread across all 3 colors instead of exhausting the first
            main[cid] = 1
    remaining = [cid for _, ids in chosen_colors for cid in ids if cid not in main]
    i = 0
    while len(main) < 50:
        main[remaining[i]] = 1
        i += 1

    result = tools.validate_deck_impl(main, {})
    assert result["is_legal"] is False
    assert any("1 or 2 colors" in e for e in result["errors"])


def _filler_deck(exclude_ids, size):
    """Build a `size`-entry {id: 1} deck from the dataset, skipping RESOURCE
    cards and any id in `exclude_ids`. Used to pad out banlist tests."""
    out = {}
    for c in data.get_all_cards():
        if len(out) >= size:
            break
        if (c.card_type or "").upper() == "RESOURCE" or c.id in exclude_ids:
            continue
        out[c.id] = 1
    return out


def test_validate_deck_banlist_off_by_default():
    main = _filler_deck(exclude_ids={"GD01-020"}, size=49)
    main["GD01-020"] = 1
    result = tools.validate_deck_impl(main, {})
    assert result["banlist"]["enforced"] is False
    assert not any("banned" in e for e in result["errors"])


def test_validate_deck_banlist_flags_banned_card():
    main = _filler_deck(exclude_ids={"GD01-020"}, size=49)
    main["GD01-020"] = 1
    result = tools.validate_deck_impl(main, {}, enforce_banlist=True)
    assert result["banlist"]["enforced"] is True
    assert any("GD01-020" in e and "banned" in e for e in result["errors"])


def test_validate_deck_banlist_flags_restricted_overcount():
    main = _filler_deck(exclude_ids={"ST02-016"}, size=47)
    main["ST02-016"] = 3
    result = tools.validate_deck_impl(main, {}, enforce_banlist=True)
    assert any("restricted to 2 copies" in e for e in result["errors"])


def test_validate_deck_banlist_flags_banned_pair():
    main = _filler_deck(exclude_ids={"ST01-010", "ST05-010"}, size=48)
    main["ST01-010"] = 1
    main["ST05-010"] = 1
    result = tools.validate_deck_impl(main, {}, enforce_banlist=True)
    assert any("banned pair" in e for e in result["errors"])


def test_validate_deck_banlist_flags_group():
    main = _filler_deck(exclude_ids={"GD01-035", "GD02-013"}, size=48)
    main["GD01-035"] = 1
    main["GD02-013"] = 1
    result = tools.validate_deck_impl(main, {}, enforce_banlist=True)
    assert any("banned-pair group" in e for e in result["errors"])


def test_validate_deck_rejects_resource_in_main():
    """A RESOURCE card in main deck must be flagged."""
    resources = [c for c in data.get_all_cards() if (c.card_type or "").upper() == "RESOURCE"]
    if not resources:
        return  # dataset has no resource type, skip silently
    main = {resources[0].id: 4}
    for c in [c for c in data.get_all_cards() if (c.card_type or "").upper() != "RESOURCE"][:46]:
        main[c.id] = 1
    result = tools.validate_deck_impl(main, {})
    assert result["is_legal"] is False
    assert any("RESOURCE" in e for e in result["errors"])


def test_analyze_deck_curve():
    main = {"GD01-001": 4, "GD01-002": 4}
    result = tools.analyze_deck_impl(main)
    assert result["total_cards"] == 8
    assert "cost_curve" in result
    assert "color_breakdown" in result
    assert result["average_cost"] is not None


def test_analyze_deck_pilot_link_counts():
    """ST01-001 Gundam and GD03-001 Gundam NT-1 both link to Amuro Ray
    (4 + 2 copies); no other unit in this pair links to anyone."""
    main = {"ST01-010": 4, "ST01-001": 4, "GD03-001": 2}
    result = tools.analyze_deck_impl(main)
    counts = dict(result["pilot_link_counts"])
    assert counts["Amuro Ray"] == 6


def test_analyze_deck_merges_trait_casing_variants():
    """'white Base Team' and 'White Base Team' are the same trait in the raw
    data with inconsistent casing; analyze_deck must merge them."""
    main = {"GD01-008": 1, "ST01-001": 1}  # '(white Base Team)' vs '(White Base Team)'
    for c in [c for c in data.get_all_cards() if c.id not in main][:48]:
        main[c.id] = 1
    result = tools.analyze_deck_impl(main)
    trait_names = [name for name, _ in result["top_traits"]]
    assert len([n for n in trait_names if n.casefold() == "white base team"]) == 1


def test_suggest_synergies_returns_results():
    suggestions = tools.suggest_synergies_impl(["GD01-001"], limit=5)
    assert isinstance(suggestions, list)
    if suggestions:
        assert all("shared_trait_count" in s for s in suggestions)
        assert all(s["shared_trait_count"] > 0 for s in suggestions)


def test_render_deck_image_produces_valid_png(monkeypatch, tmp_path):
    """No network, no disk cache: force the placeholder-thumbnail path so
    this stays fast, deterministic, and doesn't touch data/cards/images/."""
    monkeypatch.setattr(render, "_fetch_image_bytes", lambda url: None)
    monkeypatch.setattr(render, "_IMAGE_CACHE_DIR", tmp_path)
    deck = data.load_deck("meta/blue_purple_rush")
    png_bytes = render.render_deck_image(deck)
    assert png_bytes[:8] == b"\x89PNG\r\n\x1a\n"
    assert len(png_bytes) > 1000


def test_render_deck_image_with_stats_is_taller(monkeypatch, tmp_path):
    monkeypatch.setattr(render, "_fetch_image_bytes", lambda url: None)
    monkeypatch.setattr(render, "_IMAGE_CACHE_DIR", tmp_path)
    deck = data.load_deck("meta/blue_purple_rush")

    plain = render.render_deck_image(deck)
    with_stats = render.render_deck_image(deck, show_stats=True)
    assert with_stats[:8] == b"\x89PNG\r\n\x1a\n"

    import io

    from PIL import Image as PILImage
    h_plain = PILImage.open(io.BytesIO(plain)).height
    h_stats = PILImage.open(io.BytesIO(with_stats)).height
    assert h_stats > h_plain


# --- validate_deck happy paths -------------------------------------------------


def _legal_main_deck() -> dict[str, int]:
    """Build a legal 50-card main deck from the real dataset: 1-2 colors,
    no RESOURCE cards, max 4 copies per card number (1 each is safest)."""
    main: dict[str, int] = {}
    for c in data.get_all_cards():
        if len(main) >= 50:
            break
        if (c.card_type or "").upper() == "RESOURCE":
            continue
        if c.color not in ("Blue", "Green"):
            continue
        if "-p" in c.id.lower():  # skip parallels so numbers stay unique
            continue
        main[c.id] = 1
    assert len(main) == 50, "dataset should have 50+ distinct Blue/Green cards"
    return main


def test_validate_deck_accepts_legal_deck():
    result = tools.validate_deck_impl(_legal_main_deck())
    assert result["is_legal"] is True, result["errors"]
    assert result["errors"] == []
    assert result["main_count"] == 50
    assert result["resource_count"] is None  # resource deck not passed -> skipped


def test_validate_deck_rejects_non_resource_in_resource_deck():
    main = _legal_main_deck()
    non_resource = next(iter(main))  # any main-deck card is not a RESOURCE
    result = tools.validate_deck_impl(main, {non_resource: 10})
    assert result["is_legal"] is False
    assert any("cannot be in the resource deck" in e for e in result["errors"])


# --- search: new filters and normalization -------------------------------------


def test_search_by_effect_text():
    blockers = tools.search_cards_impl(effect="Blocker", limit=200)
    assert len(blockers) > 0
    assert all("blocker" in (r["effect"] or "").casefold() for r in blockers)


def test_search_normalizes_roman_numerals():
    ascii_query = tools.search_cards_impl(query="Zaku II", limit=50)
    assert len(ascii_query) > 0, "ASCII 'II' should match the printed roman numeral 'Ⅱ'"
    assert any("Zaku" in r["name"] for r in ascii_query)


def test_search_by_level_and_stat_bounds():
    lv5_or_less = tools.search_cards_impl(card_type="UNIT", level_max=5, limit=300)
    assert len(lv5_or_less) > 0
    assert all(r["level"] is not None and r["level"] <= 5 for r in lv5_or_less)

    beefy = tools.search_cards_impl(card_type="UNIT", ap_min=5, hp_min=5, limit=300)
    assert len(beefy) > 0
    assert all(r["ap"] >= 5 and r["hp"] >= 5 for r in beefy)


def test_search_by_set_id():
    st05_cards = tools.search_cards_impl(set_id="st05", limit=100)
    assert len(st05_cards) > 0
    assert all(r["set_id"] == "st05" for r in st05_cards)


def test_list_colors_non_empty():
    colors = tools.list_colors_impl()
    assert {"Blue", "Green", "Red", "White", "Purple"}.issubset(set(colors))


def test_rarity_has_no_upstream_padding():
    assert not any("  " in (c.rarity or "") for c in data.get_all_cards())


def test_zone_is_normalized():
    zones = {c.zone for c in data.get_all_cards() if c.zone}
    assert "Space Earth" not in zones  # apitcg spelling folded to 'Space / Earth'


# --- suggest_synergies: parallel prints ----------------------------------------


def test_suggest_synergies_excludes_parallel_prints():
    res = tools.suggest_synergies_impl(["GD02-054"], limit=10)
    ids = [r["id"] for r in res]
    assert "GD02-054-p1" not in ids and "GD02-054-p2" not in ids  # seed's own reprints
    assert not any(i.lower().rsplit("-p", 1)[-1].isdigit() for i in ids)  # no parallels at all


# --- deck files: subfolders, traversal guard, delete/rename ---------------------


def test_deck_name_traversal_rejected(tmp_path, monkeypatch):
    monkeypatch.setattr(data, "_DECKS_DIR", tmp_path)
    import pytest

    with pytest.raises(ValueError):
        data.save_deck("../evil", {"ST01-001": 4})
    with pytest.raises(ValueError):
        data.load_deck("../../etc/passwd")


def test_save_load_list_deck_with_subfolder(tmp_path, monkeypatch):
    monkeypatch.setattr(data, "_DECKS_DIR", tmp_path)
    data.save_deck("meta/sample", {"ST01-001": 4, "ST01-005": 2})
    assert data.list_deck_files() == ["meta/sample"]
    assert data.load_deck("meta/sample") == {"ST01-001": 4, "ST01-005": 2}


def test_save_deck_image_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setattr(data, "_DECKS_DIR", tmp_path)
    payload = b"\x89PNG\r\n\x1a\nfake"
    path = data.save_deck_image("sample", payload)
    assert path.read_bytes() == payload


def test_delete_and_rename_deck(tmp_path, monkeypatch):
    monkeypatch.setattr(data, "_DECKS_DIR", tmp_path)
    import pytest

    data.save_deck("one", {"ST01-001": 1})
    data.save_deck_image("one", b"png")
    moved = data.rename_deck("one", "meta/two")
    assert len(moved) == 2 and data.list_deck_files() == ["meta/two"]

    with pytest.raises(FileExistsError):
        data.save_deck("three", {"ST01-001": 1}) and data.rename_deck("three", "meta/two")

    removed = data.delete_deck("meta/two")
    assert len(removed) == 2 and data.list_deck_files() == ["three"]

    with pytest.raises(FileNotFoundError):
        data.delete_deck("nope")


# --- new tools: banlist, compare, odds, rules -----------------------------------


def test_get_banlist_structure():
    banlist = tools.get_banlist_impl()
    assert "banned" in banlist and "restricted" in banlist
    assert "GD01-020" in banlist["banned"]


def test_compare_decks_diff_and_summaries():
    a = {"ST01-001": 4, "ST01-005": 4, "GD01-030": 2}
    b = {"ST01-001": 4, "ST01-005": 2, "ST03-008": 4}
    result = tools.compare_decks_impl(a, b, label_a="mine", label_b="meta")
    assert result["deck_a"]["label"] == "mine"
    assert [e["id"] for e in result["only_in_a"]] == ["GD01-030"]
    assert [e["id"] for e in result["only_in_b"]] == ["ST03-008"]
    assert [e["id"] for e in result["count_differs"]] == ["ST01-005"]
    assert [e["id"] for e in result["shared_same_count"]] == ["ST01-001"]


def test_opening_hand_odds_exact_value():
    # P(>=1 of 4 copies in a 5-card hand from 50) = 1 - C(46,5)/C(50,5) ~= 0.3531
    odds = tools.opening_hand_odds_impl({"A": 4, "B": 46}, ["A"])
    assert odds["deck_size"] == 50 and odds["target_copies_in_deck"] == 4
    assert abs(odds["probability_at_least"] - 0.3531) < 0.001
    assert abs(sum(odds["distribution"].values()) - 1.0) < 0.01


def test_opening_hand_odds_rejects_bad_input():
    import pytest

    with pytest.raises(ValueError):
        tools.opening_hand_odds_impl({}, ["A"])
    with pytest.raises(ValueError):
        tools.opening_hand_odds_impl({"A": 4}, ["A"], hand_size=10)


def test_search_rules_finds_redraw_rule():
    hits = tools.search_rules_impl("redraw", limit=5)
    assert hits and any("6-2-1-6" in h for h in hits)


def test_sort_deck_canonical_order():
    """Type order UNIT -> PILOT -> COMMAND -> BASE, ascending level then
    cost within each type; unknown ids go last."""
    deck = {
        "ST05-015": 4,   # BASE Lv3
        "ST05-010": 4,   # PILOT Lv4
        "GD03-050": 2,   # UNIT Lv7 cost 6
        "GD05-117": 1,   # COMMAND Lv3
        "ST05-004": 4,   # UNIT Lv2 cost 1
        "GD02-054": 4,   # UNIT Lv3 cost 2
        "FAKE-999": 1,   # unknown -> last
        "ST05-011": 1,   # PILOT Lv3
    }
    ordered = list(data.sort_deck(deck))
    assert ordered == [
        "ST05-004", "GD02-054", "GD03-050",  # UNITs by level
        "ST05-011", "ST05-010",              # PILOTs by level
        "GD05-117",                          # COMMAND
        "ST05-015",                          # BASE
        "FAKE-999",                          # unknown last
    ]


def test_save_deck_writes_canonical_order(tmp_path, monkeypatch):
    monkeypatch.setattr(data, "_DECKS_DIR", tmp_path)
    data.save_deck("ordered", {"ST05-015": 4, "ST05-010": 4, "ST05-004": 4})
    lines = (tmp_path / "ordered.txt").read_text().strip().splitlines()
    ids = [line.split()[1] for line in lines]
    assert ids == ["ST05-004", "ST05-010", "ST05-015"]  # UNIT, PILOT, BASE
