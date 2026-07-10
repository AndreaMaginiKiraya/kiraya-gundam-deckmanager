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
    assert "blue_purple_rush" in names
    deck = data.load_deck("blue_purple_rush")
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
    deck = data.load_deck("blue_purple_rush")
    png_bytes = render.render_deck_image(deck)
    assert png_bytes[:8] == b"\x89PNG\r\n\x1a\n"
    assert len(png_bytes) > 1000


def test_render_deck_image_with_stats_is_taller(monkeypatch, tmp_path):
    monkeypatch.setattr(render, "_fetch_image_bytes", lambda url: None)
    monkeypatch.setattr(render, "_IMAGE_CACHE_DIR", tmp_path)
    deck = data.load_deck("blue_purple_rush")

    plain = render.render_deck_image(deck)
    with_stats = render.render_deck_image(deck, show_stats=True)
    assert with_stats[:8] == b"\x89PNG\r\n\x1a\n"

    import io

    from PIL import Image as PILImage
    h_plain = PILImage.open(io.BytesIO(plain)).height
    h_stats = PILImage.open(io.BytesIO(with_stats)).height
    assert h_stats > h_plain
