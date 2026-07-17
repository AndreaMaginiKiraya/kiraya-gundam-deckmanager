"""Tests for the game-log parser (gamelog.py) and the import_game_log tool.

The fixture is a real, complete Mobile Suit Arena log (26 turns, finished
game), so these tests double as a regression suite for every line format
observed in the wild so far.
"""
from pathlib import Path

import pytest
import yaml

from src import data, gamelog, tools

LOG = (Path(__file__).parent / "fixtures" / "sample_game_log.txt").read_text(encoding="utf-8")
LOG2 = (Path(__file__).parent / "fixtures" / "sample_game_log2.txt").read_text(encoding="utf-8")
LOG3 = (Path(__file__).parent / "fixtures" / "sample_game_log3.txt").read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def parsed():
    return gamelog.parse_game_log(LOG)


@pytest.fixture(scope="module")
def parsed2():
    return gamelog.parse_game_log(LOG2)


@pytest.fixture(scope="module")
def parsed3():
    return gamelog.parse_game_log(LOG3)


def test_players_setup_and_winner(parsed):
    assert parsed["players"] == ["Tonii", "Kiraya"]
    assert parsed["first_player"] == "Tonii"
    assert parsed["mulligans"] == {"Tonii": True, "Kiraya": False}
    assert parsed["winner"] == "Kiraya"
    assert parsed["source_header"] == "Mobile Suit Arena - Battle logs"
    assert [s["action"] for s in parsed["setup"]] == [
        "choose_first_player",
        "keep_hand",
        "mulligan",
    ]


def test_turns_and_active_player_alternation(parsed):
    turns = parsed["turns"]
    assert [t["turn"] for t in turns] == list(range(1, 27))
    assert turns[0]["active_player"] == "Tonii"
    assert turns[1]["active_player"] == "Kiraya"
    assert turns[0]["actions"] == []  # turn 1 was a full pass


def test_deploy_effects_attach_to_the_deploy(parsed):
    turn4 = parsed["turns"][3]
    deploy = turn4["actions"][0]
    assert deploy["action"] == "deploy"
    assert deploy["card"] == "Ryusei-Go (Graze Custom Ⅱ)"
    assert any("Draw a card" in e for e in deploy["effects"])
    assert any("Sword Impulse Gundam discarded" in e for e in deploy["effects"])


def test_battle_against_ex_base(parsed):
    attack = parsed["turns"][4]["actions"][0]  # turn 5, Zaku Ⅱ attack
    assert attack["action"] == "attack"
    assert attack["player"] == "Tonii"
    assert attack["attacker"] == "Zaku Ⅱ"
    assert attack["declared_target"] == "player"
    assert attack["blockers"] == "none"
    assert attack["final_target"] == "EX Base"
    assert attack["modifiers"] == ["Zaku Ⅱ: Modifier applied to: Zaku Ⅱ"]
    assert "EX Base received 3 damage, now destroyed" in attack["outcome"]


def test_pair_pilot_linked_vs_paired(parsed):
    turn6 = parsed["turns"][5]
    pair = next(a for a in turn6["actions"] if a["action"] == "pair_pilot")
    assert pair["pilot"] == "Mikazuki Augus"
    assert pair["linked"] is True
    turn19 = parsed["turns"][18]
    pair = next(a for a in turn19["actions"] if a["action"] == "pair_pilot")
    assert pair["pilot"] == "Amuro Ray"
    assert pair["unit"] == "Guntank"
    assert pair["linked"] is False


def test_assigned_blocker_redirects_battle(parsed):
    turn13 = parsed["turns"][12]
    attacks = [a for a in turn13["actions"] if a["action"] == "attack"]
    blocked = attacks[1]
    assert blocked["attacker"] == "Nu Gundam"
    assert blocked["declared_target"] == "Gundam Barbatos 1st Form"
    assert blocked["blockers"] == "Gundam Gusion Rebake"
    assert blocked["final_target"] == "Gundam Gusion Rebake"
    # Breach hitting a shield is both recorded and tallied (see tally test).
    assert any("Breach 3 Shield card" in line for line in blocked["outcome"])


def test_action_step_command_play_recorded_inside_battle(parsed):
    turn23 = parsed["turns"][22]
    battle = next(a for a in turn23["actions"] if a["action"] == "attack")
    play = battle["action_step"][0]
    assert play == {
        "action": "play_command",
        "player": "Kiraya",
        "card": "Become a Shield",
        "effects": [
            "Become a Shield: Dealt 1 damage to: Gundam Barbatos 1st Form and Kayra's Jegan"
        ],
    }


def test_activate_and_exile(parsed):
    turn26 = parsed["turns"][25]
    activations = [a for a in turn26["actions"] if a["action"] == "activate"]
    assert len(activations) == 2
    assert activations[0]["card"] == "Gundam Barbatos Lupus"
    assert any("exiled from the game" in e for e in activations[0]["effects"])


def test_casualties_attributed_by_owner(parsed):
    cas = parsed["casualties"]
    kiraya = [(c["card"], c["turn"]) for c in cas["Kiraya"]]
    tonii = [(c["card"], c["turn"]) for c in cas["Tonii"]]
    assert ("Gundam Exia Repair", 6) in kiraya  # battle trade
    assert ("Gundam Exia Repair", 17) in kiraya  # killed by effect damage
    assert ("Isaribi", 9) in kiraya  # base destroyed by Breach
    assert ("Isaribi", 25) in kiraya
    assert ("Tallgeese", 26) in tonii  # killed by Lupus' activated effect
    assert ("Nu Gundam", 9) in tonii
    assert "unattributed" not in cas


def test_shields_tally(parsed):
    tally = parsed["shields_tally"]
    assert tally["Kiraya"]["ex_base"] == "destroyed (turn 5)"
    assert tally["Tonii"]["ex_base"] == "destroyed (turn 6)"
    # Kiraya: Hyakuren (t5), Barbatos Adapt via Breach (t13), Lupus (t23).
    assert tally["Kiraya"]["shields_lost"] == 3
    assert tally["Kiraya"]["shields_to_hand"] == 2  # Isaribi t6 and t24
    assert tally["Kiraya"]["shields_remaining"] == 1
    # Tonii ran out of shields ("No more Shield cards" on turn 25).
    assert tally["Tonii"]["shields_lost"] == 4
    assert tally["Tonii"]["shields_to_hand"] == 2  # Amuro Ray bursts t8/t18
    assert tally["Tonii"]["shields_remaining"] == 0


def test_every_line_recognized(parsed):
    assert parsed["unparsed"] == []


def test_cards_seen_owners(parsed):
    seen = parsed["cards_seen"]
    assert seen["Gundam Barbatos Adapt"]["owners"] == ["Kiraya"]
    assert seen["Nu Gundam"]["owners"] == ["Tonii"]
    assert "shield" in seen["Hyakuren"]["contexts"]
    assert "blocker" in seen["Gundam Gusion Rebake"]["contexts"]


def test_second_log_players_winner_and_full_coverage(parsed2):
    assert parsed2["players"] == ["Kiraya", "0622"]
    assert parsed2["first_player"] == "Kiraya"
    assert parsed2["winner"] == "0622"
    assert parsed2["unparsed"] == []
    assert [t["turn"] for t in parsed2["turns"]] == list(range(1, 25))


def test_main_phase_command_play(parsed2):
    turn2 = parsed2["turns"][1]
    play = turn2["actions"][0]
    assert play["action"] == "play_command"
    assert play["card"] == "Overflowing Affection"
    assert any("Draw 2 cards" in e for e in play["effects"])
    assert any("Rick Dias discarded" in e for e in play["effects"])


def test_multi_name_discard_notes_each_card(parsed2):
    seen = parsed2["cards_seen"]
    # "Rick Dias and Gundam Lfrith discarded" (turn 16, Strike Freedom cost)
    assert "discarded" in seen["Gundam Lfrith"]["contexts"]
    assert "discarded" in seen["Rick Dias"]["contexts"]
    assert "Rick Dias and Gundam Lfrith" not in seen
    # "X returned to deck/hand" is recognized, with the destination kept
    # apart (bounce-to-deck vs return-to-hand are opposite mechanics).
    assert "returned to deck" in seen["Gundam Barbatos Lupus"]["contexts"]
    assert "returned to hand" in seen["Gundam Barbatos 2nd Form"]["contexts"]


def test_burst_deployed_shield_counts_in_tally(parsed2):
    tally = parsed2["shields_tally"]
    # 0622: Nahel Argama Burst-deployed from shields (t9), 4 shields to hand
    # (base deploys t6/t9 + Kira Yamato reveals t15/t17), Freedom discarded
    # (t17) -> 0 left, matching "No more Shield cards to add to hand" (t20).
    assert tally["0622"]["shields_deployed"] == 1
    assert tally["0622"]["shields_to_hand"] == 4
    assert tally["0622"]["shields_lost"] == 1
    assert tally["0622"]["shields_remaining"] == 0
    # Kiraya: 5 discarded + Mikazuki to hand -> lethal on turn 24.
    assert tally["Kiraya"]["shields_lost"] == 5
    assert tally["Kiraya"]["shields_to_hand"] == 1
    assert tally["Kiraya"]["shields_remaining"] == 0
    assert tally["Kiraya"]["ex_base"] == "destroyed (turn 18)"
    assert tally["0622"]["ex_base"] == "destroyed (turn 5)"


def test_numeric_player_name_stays_a_string_in_yaml():
    text = gamelog.dump_yaml({"0622": {"first_player": False}})
    assert yaml.safe_load(text) == {"0622": {"first_player": False}}


def test_deck_resolves_ambiguous_printings(tmp_path, monkeypatch):
    monkeypatch.setattr(data, "_GAMES_DIR", tmp_path)
    summary = tools.import_game_log_impl(LOG2, "g2", decks={"Kiraya": "aggro_mono_p"})
    # Multiple printings share these names, but only one is in the deck.
    assert summary["cards_resolved"]["Gundam Barbatos 1st Form"] == "GD02-054"
    assert summary["cards_resolved"]["Gundam Barbatos Lupus"] == "GD03-050"
    assert summary["cards_resolved"]["Gundam Gusion Rebake"] == "GD02-055"
    assert "Gundam Barbatos 1st Form" not in summary["cards_ambiguous"]
    # Token-only names resolve to the token (deployed by Justice's effect).
    assert summary["cards_resolved"]["Fatum-00"] == "T-011"
    assert summary["cards_not_found"] == []
    doc = yaml.safe_load(Path(summary["path"]).read_text(encoding="utf-8"))
    assert "resolved via saved deck" in doc["cards"]["Gundam Barbatos 1st Form"]["note"]


def test_third_log_new_formats(parsed3):
    assert parsed3["winner"] == "Kiraya"
    assert parsed3["unparsed"] == []
    # "Replaced EX Base base: Isaribi" (turn 5)
    replaced = next(
        a for a in parsed3["turns"][4]["actions"] if a["action"] == "play_base"
    )
    assert replaced["card"] == "Isaribi"
    assert replaced["replaced"] == "EX Base"
    assert parsed3["shields_tally"]["Kiraya"]["ex_base"] == "replaced with a base (turn 5)"
    # "Can't block High-maneuver" (turn 18)
    attack = parsed3["turns"][17]["actions"][0]
    assert attack["attacker"] == "Wing Gundam Zero"
    assert attack["blockers"] == "none (High-maneuver)"
    # Source-less "Dealt 3 damage to Graze Custom, now destroyed" (turn 18)
    deaths = [(c["card"], c["turn"]) for c in parsed3["casualties"]["Kiraya"]]
    assert ("Graze Custom", 18) in deaths
    # "Rested base:" / "Activated: Isaribi" (turn 9)
    activate = parsed3["turns"][8]["actions"][0]
    assert activate["action"] == "activate"
    assert any("Rested base: Isaribi" in e for e in activate["effects"])


def test_pilot_mode_command_resolves_and_subfolder_name(tmp_path, monkeypatch):
    monkeypatch.setattr(data, "_GAMES_DIR", tmp_path)
    summary = tools.import_game_log_impl(
        LOG3, "aggro_mono_p/g3", decks={"Kiraya": "aggro_mono_p"}
    )
    # "Linked pilot: Ride Mass" is Become a Shield played in Pilot mode.
    assert summary["cards_resolved"]["Ride Mass"] == "GD05-117"
    assert Path(summary["path"]) == tmp_path / "aggro_mono_p" / "g3.yaml"
    doc = yaml.safe_load(Path(summary["path"]).read_text(encoding="utf-8"))
    assert doc["cards"]["Ride Mass"]["note"] == "pilot mode of the COMMAND card 'Become a Shield'"


def test_set_active_and_repair_lines_recognized():
    # V2 Gundam's engine (rest 2 Parts -> set itself active) and end-phase
    # Repair lines, plus back-to-back setup choices with no actor line
    # between them (the same player chose first AND mulliganed).
    snippet = """Game started!
A
Choose to play first
Choose to mulligan starting hand
B
Choose to keep starting hand
Turn 1 started!
A
V2 Gundam deployed
Activated: V2 Gundam
Rested unit: Parts
Set Active: V2 Gundam
Turn end phase started
V2 Gundam repaired 1 from [Repair 2]
Turn ended!"""
    parsed = gamelog.parse_game_log(snippet)
    assert parsed["players"] == ["A", "B"]
    assert parsed["mulligans"] == {"A": True, "B": False}
    assert parsed["unparsed"] == []
    activate = parsed["turns"][0]["actions"][1]
    assert activate["action"] == "activate"
    assert "Set Active: V2 Gundam" in activate["effects"]
    assert any("repaired 1" in e for e in activate["effects"])


def test_burst_command_from_shield_and_prevention_lines():
    snippet = """Game started!
アスファルトの雑草
Choose to play first
B
Choose to keep starting hand
Turn 1 started!
Battle initiated
B
Battle declared: Graze Custom against Enemy Player
アスファルトの雑草
No blockers available
Battle started: Graze Custom against Enemy Shield
Shield card: Close Combat revealed
Shield card: Close Combat moved to trash
Close Combat: Dealt 2 damage to Graze Custom, now destroyed
Damage prevented
Returned to deck bottom
Battle ended"""
    parsed = gamelog.parse_game_log(snippet)
    assert parsed["players"] == ["アスファルトの雑草", "B"]
    assert parsed["unparsed"] == []
    # Burst command counts as a lost shield for the defender.
    assert parsed["shields_tally"]["アスファルトの雑草"]["shields_lost"] == 1
    # Japanese player names survive a YAML round-trip as mapping keys.
    assert yaml.safe_load(gamelog.dump_yaml(parsed["shields_tally"])) == parsed["shields_tally"]


def test_zero_width_chars_in_card_names_still_resolve():
    # GD05-111 is printed as "Airframe​ Seizure" upstream (zero-width
    # space); a log says "Airframe Seizure" and must still match.
    matches = tools._resolve_log_card_name("Airframe Seizure")
    assert [c.id for c in matches] == ["GD05-111"]


def test_dump_yaml_quotes_are_safe():
    text = gamelog.dump_yaml({"Kayra's \"Jegan\" Ⅱ": [{"a": None, "b": True, "c": 3}]})
    assert yaml.safe_load(text) == {"Kayra's \"Jegan\" Ⅱ": [{"a": None, "b": True, "c": 3}]}


def test_import_game_log_impl_writes_valid_record(tmp_path, monkeypatch):
    monkeypatch.setattr(data, "_GAMES_DIR", tmp_path)
    summary = tools.import_game_log_impl(LOG, "sample", decks={"Kiraya": "aggro_mono_p"})
    path = Path(summary["path"])
    assert path == tmp_path / "sample.yaml"
    assert summary["result"] == "win:Kiraya"
    assert summary["turns"] == 26
    # Unique printings resolve to an id; shared names come back as ambiguous.
    assert summary["cards_resolved"]["Gundam Barbatos Adapt"] == "GD03-056"
    assert summary["cards_resolved"]["Mikazuki Augus"] == "ST05-010"
    assert "Zaku Ⅱ" in summary["cards_ambiguous"]
    assert "Nu Gundam" in summary["cards_ambiguous"]
    assert summary["cards_not_found"] == []
    assert summary["unparsed_lines"] == []
    # The raw log is kept next to the record so it can be re-imported later.
    assert Path(summary["log_path"]).read_text(encoding="utf-8") == LOG

    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert doc["game"]["result"] == "win:Kiraya"
    assert doc["game"]["players"]["Kiraya"]["deck"] == "aggro_mono_p"
    assert doc["game"]["players"]["Kiraya"]["colors"] == ["Purple"]
    assert doc["game"]["source"] == "Mobile Suit Arena - Battle logs"
    assert len(doc["turns"]) == 26
    assert doc["cards"]["Zaku Ⅱ"]["id"] is None
    assert "ST03-008" in doc["cards"]["Zaku Ⅱ"]["candidates"]
    assert doc["study_notes"] == []

    # Overwrite guard: a second import must not silently clobber the record.
    with pytest.raises(FileExistsError):
        tools.import_game_log_impl(LOG, "sample")
    tools.import_game_log_impl(LOG, "sample", overwrite=True)


def test_reimport_carries_over_hand_annotations(tmp_path, monkeypatch):
    monkeypatch.setattr(data, "_GAMES_DIR", tmp_path)
    tools.import_game_log_impl(LOG, "g", decks={"Kiraya": "aggro_mono_p"})

    # Simulate the post-import hand-editing pass: pin an ambiguous id with
    # an evidence note, annotate a still-ambiguous card, add study notes.
    record = tmp_path / "g.yaml"
    doc = yaml.safe_load(record.read_text(encoding="utf-8"))
    doc["cards"]["Zaku Ⅱ"]["id"] = "ST03-008"
    doc["cards"]["Zaku Ⅱ"]["note"] = "pinned: modifier AP+2"
    doc["cards"]["Guntank"]["note"] = "evidenze contrastanti"
    doc["study_notes"] = ["nota di studio"]
    record.write_text(gamelog.dump_yaml(doc), encoding="utf-8")

    summary = tools.import_game_log_impl(LOG, "g", overwrite=True)  # no decks passed
    doc2 = yaml.safe_load(record.read_text(encoding="utf-8"))
    zaku = doc2["cards"]["Zaku Ⅱ"]
    assert zaku["id"] == "ST03-008"
    assert zaku["note"] == "pinned: modifier AP+2"
    assert zaku["ap"] == 1  # stats re-derived from the database for the pinned id
    assert "candidates" not in zaku
    assert doc2["cards"]["Guntank"]["note"] == "evidenze contrastanti"
    assert doc2["cards"]["Guntank"]["id"] is None  # still ambiguous, note kept
    assert doc2["study_notes"] == ["nota di studio"]
    assert doc2["game"]["players"]["Kiraya"]["deck"] == "aggro_mono_p"
    assert "study_notes" in summary["annotations_carried_over"]
    assert "cards[Zaku Ⅱ].id" in summary["annotations_carried_over"]


def test_choose_second_and_base_replaced_by_itself():
    snippet = """Game started!
A
Choose to play second
B
Choose to keep starting hand
A
Choose to keep starting hand
Turn 1 started!
Turn end phase started
B
Passed
A
Passed
Turn ended!
Turn 2 started!
B
Played base: Archangel
Shield card added to hand
Turn end phase started
A
Passed
B
Passed
Turn ended!
Turn 3 started!
B
Replaced Archangel base: Archangel
Shield card added to hand
Turn end phase started"""
    parsed = gamelog.parse_game_log(snippet)
    assert parsed["unparsed"] == []
    # A chose to play second -> B is first player -> B is active on turn 1.
    assert parsed["first_player"] == "B"
    assert parsed["turns"][0]["active_player"] == "B"
    replace_action = next(
        a for a in parsed["turns"][2]["actions"] if a["action"] == "play_base"
    )
    assert replace_action["card"] == "Archangel"
    assert replace_action["replaced"] == "Archangel"
    assert "Shield card added to hand" in replace_action["effects"]
    # Replacing a plain Base (not "EX Base") doesn't touch the EX Base tally.
    assert parsed["shields_tally"]["B"]["ex_base"] == "not destroyed in log"


def test_card_added_to_hand_line_recognized():
    snippet = """Game started!
A
Choose to play first
B
Choose to keep starting hand
Turn 1 started!
A
Gundam Airmaster deployed
Linked pilot: Garrod Ran & Tiffa Adill on unit Gundam Airmaster
Selecting target for Garrod Ran & Tiffa Adill
Jamil Neate discarded
Selecting target for Garrod Ran & Tiffa Adill
Card added to hand: Gundam Leopard Destroy
Turn end phase started"""
    parsed = gamelog.parse_game_log(snippet)
    assert parsed["unparsed"] == []
    assert "Gundam Leopard Destroy" in parsed["cards_seen"]
    assert parsed["cards_seen"]["Gundam Leopard Destroy"]["owners"] == ["A"]
    assert parsed["cards_seen"]["Gundam Leopard Destroy"]["contexts"] == ["added to hand"]


def test_ability_triggered_battle_with_no_declare_phase():
    # Nu Gundam LR's own When-Paired ability jumps straight to "Battle
    # started" with no "Battle initiated"/"Battle declared"/blocker step.
    snippet = """Game started!
A
Choose to play first
B
Choose to keep starting hand
Turn 1 started!
A
Nu Gundam deployed
Linked pilot: Amuro Ray on unit Nu Gundam
Selecting target for Nu Gundam
Kayra Su, Jegan and Amuro Ray exiled from the game
Selecting target for Nu Gundam
Battle started: Nu Gundam against Graze Custom
B
Graze Custom received 7 damage, now destroyed
A
Nu Gundam received 2 damage, leaving 5 HP remaining
Healed 2 damage to: Nu Gundam
Battle ended
Turn end phase started"""
    parsed = gamelog.parse_game_log(snippet)
    assert parsed["unparsed"] == []
    battle = next(a for a in parsed["turns"][0]["actions"] if a["action"] == "attack")
    assert battle["player"] == "A"
    assert battle["attacker"] == "Nu Gundam"
    assert battle["trigger"] == "ability"
    assert battle["final_target"] == "Graze Custom"
    assert "declared_target" not in battle
    assert "blockers" not in battle
    assert any("now destroyed" in e for e in battle["outcome"])


def test_explicit_destroyed_line_and_resource_active_note():
    # Alternate client phrasing: an explicit "X: destroyed Y" kill
    # confirmation (alongside "X received N damage, now destroyed" elsewhere)
    # and an end-of-turn "X turn end: N resource set as active" note.
    snippet = """Game started!
A
Choose to play first
B
Choose to keep starting hand
Turn 1 started!
A
Gundam Exia Repair deployed
B
GN Armor Type-E deployed
Battle initiated
A
Battle declared: Gundam Exia Repair against Enemy Player
B
No blockers available
Battle started: Gundam Exia Repair against GN Armor Type-E
B
GN Armor Type-E received 2 damage, leaving 1 HP remaining
A
Gundam Exia Repair received 3 damage, now destroyed
Gundam Exia Repair: destroyed GN Armor Type-E
Battle ended
Turn end phase started
B
Passed
A
Passed
Gundam Exia turn end: 1 resource set as active
Turn ended!"""
    parsed = gamelog.parse_game_log(snippet)
    assert parsed["unparsed"] == []
    deaths = [c["card"] for c in parsed["casualties"]["B"]]
    assert "GN Armor Type-E" in deaths
    assert "attacker" in parsed["cards_seen"]["Gundam Exia Repair"]["contexts"]


def test_resource_active_terse_mid_battle_phrasing():
    # Same event as above but without "turn end:" -- seen mid-battle, e.g.
    # a Deploy-cost resource un-resting as part of declaring an attack.
    snippet = """Game started!
A
Choose to play first
B
Choose to keep starting hand
Turn 1 started!
A
Battle initiated
A
Battle declared: Shining Gundam against Enemy Player
Shining Gundam: 1 resource set as active
B
No blockers available
Battle ended"""
    parsed = gamelog.parse_game_log(snippet)
    assert parsed["unparsed"] == []


def test_rested_resources_line_recognized():
    snippet = """Game started!
A
Choose to play first
B
Choose to keep starting hand
Turn 1 started!
A
Played base: White Base
Shield card added to hand
Activated: White Base
Rested 2 Resources
Turn end phase started"""
    parsed = gamelog.parse_game_log(snippet)
    assert parsed["unparsed"] == []


def test_unit_ability_ex_resource_reversed_wording_recognized():
    # "<source>: Placed N EX Resource" (unit-ability wording, reversed word
    # order) is a variant of the player's own "Placed N Resource EX".
    snippet = """Game started!
A
Choose to play first
B
Choose to keep starting hand
Turn 1 started!
A
Battle initiated
Battle declared: Gundam Pharact against Enemy Player
B
No blockers available
Action step
B
Passed
A
Passed
Battle started: Gundam Pharact against Enemy Player
B
Gundam Pharact: Placed 1 EX Resource
Battle ended
Turn end phase started"""
    parsed = gamelog.parse_game_log(snippet)
    assert parsed["unparsed"] == []


def test_rested_ex_resource_and_attack_target_changed_recognized():
    # "Placed N rested EX Resource" (Suletta Mercury's During-Link effect)
    # and "<source>: attack target changed" (an action-card redirect, e.g.
    # Guel Jeturk) are both effect lines with no dedicated action of their
    # own.
    snippet = """Game started!
A
Choose to play first
B
Choose to keep starting hand
Turn 1 started!
A
Battle initiated
Battle declared: Hyakuren against Enemy Player
B
No blockers available
Action step
B
Played action: Guel Jeturk
Guel Jeturk: attack target changed
Suletta Mercury: Placed 1 rested EX Resource
A
Passed
B
Passed
Battle started: Hyakuren against Guel's Dilanza
Battle ended
Turn end phase started"""
    parsed = gamelog.parse_game_log(snippet)
    assert parsed["unparsed"] == []


def test_timeout_warning_line_ignored():
    snippet = """Game started!
A
Choose to play first
B
Choose to keep starting hand
Turn 1 started!
A
Battle initiated
Battle declared: Gundam Pharact against Enemy Player
B
No blockers available
Action step
B
Timeout 1
Passed
A
Passed
Turn end phase started"""
    parsed = gamelog.parse_game_log(snippet)
    assert parsed["unparsed"] == []


def test_ex_base_destroyed_via_breach_updates_tally():
    # Regression test: "Breach N: : EX Base received N damage, now
    # destroyed" was only ever recorded via record_death (which explicitly
    # ignores "EX Base"), so a Breach-inflicted EX Base kill silently
    # vanished instead of updating shields_tally.ex_base.
    snippet = """Game started!
A
Choose to play first
B
Choose to keep starting hand
Turn 1 started!
A
Battle initiated
Battle declared: Gundam Barbatos Lupus against Enemy Player
B
No blockers available
Action step
B
Passed
A
Passed
Battle started: Gundam Barbatos Lupus against Enemy Player
B
Breach 3: : EX Base received 3 damage, now destroyed
Battle ended
Turn end phase started"""
    parsed = gamelog.parse_game_log(snippet)
    assert parsed["unparsed"] == []
    assert parsed["shields_tally"]["B"]["ex_base"] == "destroyed (turn 1)"


def test_duplicate_turn_start_merges_into_one_turn():
    # The client sometimes restarts a turn ("Turn N started!" twice, seen
    # after a mid-turn pass in the loklee game): the two blocks must land
    # in a single turn entry, not a spurious empty duplicate.
    snippet = """Game started!
A
Choose to play first
B
Choose to keep starting hand
Turn 1 started!
A
Passed
Turn ended!
Turn 1 started!
A
Zaku Ⅱ deployed
Turn end phase started
B
Passed
A
Passed
Turn ended!"""
    parsed = gamelog.parse_game_log(snippet)
    assert [t["turn"] for t in parsed["turns"]] == [1]
    assert [a["card"] for a in parsed["turns"][0]["actions"]] == ["Zaku Ⅱ"]


def test_battle_keys_ordered_with_pre_battle_effects():
    # An effect line landing between the declare and the damage step (e.g.
    # "No targets for X") must not push `outcome` ahead of `blockers` /
    # `final_target` in the finished attack dict.
    snippet = """Game started!
A
Choose to play first
B
Choose to keep starting hand
Turn 1 started!
A
Battle initiated
Battle declared: Gundam Flauros (Ryusei-Go) against Enemy Player
No targets for Gundam Flauros (Ryusei-Go)
B
No blockers available
Action step
B
Passed
A
Passed
Battle started: Gundam Flauros (Ryusei-Go) against EX Base
B
EX Base received 2 damage, leaving 1 HP remaining
Battle ended
Turn end phase started"""
    parsed = gamelog.parse_game_log(snippet)
    attack = parsed["turns"][0]["actions"][0]
    assert list(attack) == [
        "action",
        "player",
        "attacker",
        "declared_target",
        "blockers",
        "final_target",
        "outcome",
    ]
    assert attack["outcome"][0] == "No targets for Gundam Flauros (Ryusei-Go)"


def test_unparsed_lines_carry_turn_number():
    snippet = """Game started!
A
Choose to play first
B
Choose to keep starting hand
Turn 1 started!
A
Some brand new line format
Turn end phase started"""
    parsed = gamelog.parse_game_log(snippet)
    assert parsed["unparsed"] == ["[turn 1] Some brand new line format"]


def test_inferred_ping_casualties(tmp_path, monkeypatch):
    # "SRC: Dealt N damage to: A and B" never logs a destruction, so a ping
    # covering a unit's full printed HP (Zakrello: 1) must yield an
    # inferred casualty — while the 5-HP source of the same ping must not.
    monkeypatch.setattr(data, "_GAMES_DIR", tmp_path)
    snippet = """Game started!
A
Choose to play first
B
Choose to keep starting hand
Turn 1 started!
A
Zakrello deployed
Turn ended!
Turn 2 started!
B
Gundam Gusion Rebake deployed
Selecting target for Gundam Gusion Rebake
Gundam Gusion Rebake: Dealt 1 damage to: Gundam Gusion Rebake and Zakrello
Turn end phase started
A
Passed
B
Passed
Turn ended!"""
    summary = tools.import_game_log_impl(
        snippet, "g-ping", decks={"B": "aggro_mono_p"}
    )
    assert summary["casualties_inferred"] == {
        "A": [{"card": "Zakrello", "turn": 2, "inferred": True}]
    }
    doc = yaml.safe_load(Path(summary["path"]).read_text(encoding="utf-8"))
    assert {"card": "Zakrello", "turn": 2, "inferred": True} in doc["casualties"]["A"]
    assert all(c["card"] != "Gundam Gusion Rebake" for c in doc["casualties"]["B"])


def test_inferred_ping_skips_paired_units(tmp_path, monkeypatch):
    # A pilot can raise HP past the printed value, so a unit ever seen
    # paired is excluded from the inference even when the ping matches its
    # printed HP.
    monkeypatch.setattr(data, "_GAMES_DIR", tmp_path)
    snippet = """Game started!
A
Choose to play first
B
Choose to keep starting hand
Turn 1 started!
A
Zakrello deployed
Paired pilot: Char Aznable on unit Zakrello
Turn ended!
Turn 2 started!
B
Gundam Gusion Rebake deployed
Selecting target for Gundam Gusion Rebake
Gundam Gusion Rebake: Dealt 1 damage to: Gundam Gusion Rebake and Zakrello
Turn end phase started
A
Passed
B
Passed
Turn ended!"""
    summary = tools.import_game_log_impl(
        snippet, "g-paired", decks={"B": "aggro_mono_p"}
    )
    assert summary["casualties_inferred"] == {}


def test_reimport_recomputes_colors_from_carried_over_ids(tmp_path, monkeypatch):
    # Regression test: a color contributed ONLY by a card that starts
    # ambiguous and is pinned by hand must survive a re-import. Coloring
    # was previously computed before annotation carry-over ran, so a
    # re-import silently dropped any color that had no other, already-
    # unambiguous card to back it up.
    monkeypatch.setattr(data, "_GAMES_DIR", tmp_path)
    snippet = """Game started!
A
Choose to play first
B
Choose to keep starting hand
Turn 1 started!
A
Zaku Ⅱ deployed
Turn end phase started
B
Passed
A
Passed
Turn ended!
Winner!
Game ended!"""
    tools.import_game_log_impl(snippet, "g")
    record = tmp_path / "g.yaml"
    doc = yaml.safe_load(record.read_text(encoding="utf-8"))
    assert "colors" not in doc["game"]["players"]["A"]  # still ambiguous, no color yet

    doc["cards"]["Zaku Ⅱ"]["id"] = "ST03-008"  # the Green printing
    doc["cards"]["Zaku Ⅱ"].pop("candidates", None)
    record.write_text(gamelog.dump_yaml(doc), encoding="utf-8")

    tools.import_game_log_impl(snippet, "g", overwrite=True)
    doc2 = yaml.safe_load(record.read_text(encoding="utf-8"))
    assert doc2["game"]["players"]["A"]["colors"] == ["Green"]


def test_game_path_rejects_escape():
    with pytest.raises(ValueError):
        data._game_path("../evil")
