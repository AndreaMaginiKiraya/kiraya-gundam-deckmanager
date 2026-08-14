"""Parse chat-exported game logs into structured game records for data/games/.

The input format is the plain-text play-by-play that online GCG clients
(e.g. Mobile Suit Arena) produce: "Turn 3 started!", "Zaku Ⅱ deployed",
"Battle declared: ...". `parse_game_log` turns that into plain dicts/lists;
`dump_yaml` renders such a structure as YAML with no YAML library needed
(string scalars are emitted JSON-quoted, and JSON is a YAML subset).

This module is pure text processing: resolving card names against the card
database and writing files lives in tools.import_game_log_impl, not here.
"""
from __future__ import annotations

import json
import re

# Per the Comprehensive Rules (6-4-4/6-4-5): 6 shields + 1 EX Base each.
STARTING_SHIELDS = 6

_SETUP_CHOICES = {
    "Choose to play first": "choose_first_player",
    "Choose to play second": "choose_second_player",
    "Choose to keep starting hand": "keep_hand",
    "Choose to mulligan starting hand": "mulligan",
}
# Flow markers that carry no information beyond what the structure already
# captures (turn boundaries create turns; passes/priority are implicit).
_MARKERS = {
    "Game started!",
    "Game ended!",
    "Turn end phase started",
    "Turn ended!",
    "Action step",
    "Passed",
}

# A player running low on their clock gets an auto-pass warning
# ("Timeout 1", "Timeout 2", ...) - no game information beyond that.
_TIMEOUT_RE = re.compile(r"^Timeout \d+$")
_TURN_START_RE = re.compile(r"^Turn (\d+) started!$")
_DEPLOYED_RE = re.compile(r"^(.+?) deployed$")
_PLAYED_BASE_RE = re.compile(r"^Played base: (.+)$")
# "Replaced EX Base base: X" (the starting EX Base) or "Replaced <old base>
# base: <new base>" (an in-play Base refreshed by deploying another copy).
_REPLACED_BASE_RE = re.compile(r"^Replaced (.+?) base: (.+)$")
# "action" = played during a battle's action step, "command" = main phase.
_PLAYED_ACTION_RE = re.compile(r"^Played (?:action|command): (.+)$")
_ACTIVATED_RE = re.compile(r"^Activated: (.+)$")
# "Linked" = the unit's link condition is met; "Paired" = a plain pairing.
_PAIR_PILOT_RE = re.compile(r"^(Linked|Paired) pilot: (.+?) on unit (.+)$")
_BATTLE_DECLARED_RE = re.compile(r"^Battle declared: (.+?) against (.+)$")
_BATTLE_STARTED_RE = re.compile(r"^Battle started: (.+?) against (.+)$")
_ASSIGNED_BLOCKER_RE = re.compile(r"^Assigned (.+?) to block$")
_CANT_BLOCK_RE = re.compile(r"^Can't block (.+)$")
# "Shield card(s): A[ and B...] revealed and discarded" - plural when a
# single hit (e.g. a multi-damage Breach) clears more than one shield at
# once; each named card counts toward shields_lost.
_SHIELD_DISCARDED_RE = re.compile(r"^Shield cards?: (.+?) revealed and discarded$")
_SHIELD_REVEALED_RE = re.compile(r"^Shield cards?: (.+?) revealed$")
_SHIELD_TO_HAND_RE = re.compile(r"^Shield card added to hand(?:: (.+))?$")
# A non-shield card fetched to hand by an effect (e.g. Garrod Ran & Tiffa
# Adill's When-Paired dig). Checked separately from shield lines since it
# isn't tied to the shield-area/tally bookkeeping at all.
_CARD_TO_HAND_RE = re.compile(r"^Card added to hand: (.+)$")
# Two-line variant of a lost shield: "revealed" then "moved to trash"
# (a Burst COMMAND resolves its effect before going to the trash).
_SHIELD_TO_TRASH_RE = re.compile(r"^Shield cards?: (.+?) moved to trash$")
# "Breach 3: : Isaribi received ..." (base hit, doubled colon as observed) or
# "Breach 3 Shield card: X revealed and discarded" (shield hit, no colon).
_BREACH_RE = re.compile(r"^Breach \d+\s*:?\s*:?\s*(.+)$")
# The optional ", reduced by N" clause appears when a damage-reduction
# effect (e.g. a Constant Effect capping incoming damage) partially
# blunts the hit - the final outcome (destroyed/remaining HP) already
# reflects the reduced amount, so it's tracked in the raw line but not
# separately parsed out.
_RECEIVED_RE = re.compile(
    r"^(.+?) received \d+ damage(?:, reduced by \d+)?,"
    r" (?:now destroyed|leaving \d+ HP remaining)$"
)
_DEALT_RE = re.compile(
    r"^(.+?): Dealt \d+ damage to:? .+?(?:, (?:now destroyed|leaving \d+ HP remaining))?$"
)
# Single-target effect damage that kills ("Guntank: Dealt 1 damage to X, now
# destroyed"; the "<source>: " prefix is absent on some deploy effects, e.g.
# Wing Gundam Zero's). The multi-target form uses "to:" and never carries a
# destroyed suffix, so requiring a non-colon after "to" keeps them apart.
_DEALT_DESTROYED_RE = re.compile(r"^(?:.+?: )?Dealt \d+ damage to ([^:].*?), now destroyed$")
_DEALT_NOSRC_RE = re.compile(r"^Dealt \d+ damage to:? .+$")
# Explicit battle-damage kill confirmation, distinct from "X received N
# damage, now destroyed" (same event, alternate client phrasing observed).
_DESTROYED_RE = re.compile(r"^(.+?): destroyed (.+)$")
# "<name> destroyed" with no source/colon and no damage line at all - a
# non-battle effect that destroys outright (e.g. Interwoven Blessings
# destroying a card in the shield area/on the field with no "received
# damage" step). Checked after _DESTROYED_RE so "SRC: destroyed TARGET"
# is never mistaken for this simpler, sourceless form.
_PLAIN_DESTROYED_RE = re.compile(r"^(.+?) destroyed$")
# "X turn end: N resource set as active" (end-of-turn refresh) or the
# terser "X: N resource set as active" (seen mid-battle, e.g. a Deploy-cost
# resource un-resting as part of declaring an attack).
_RESOURCE_ACTIVE_RE = re.compile(r"^.+?: \d+ resource set as active$")
_DRAW_RE = re.compile(r"^.+?: Draw (?:a card|\d+ cards?)$")
_MODIFIER_RE = re.compile(r"^.+?: Modifier applied to: .+$")
_CHOSE_RE = re.compile(r"^.+?: chose .+$")
_MILLED_RE = re.compile(r"^(.+?) milled \d+: (.+?) moved to trash$")
_EXILED_RE = re.compile(r"^(.+?) exiled from the game$")
# Destination captured: bounce-to-deck (Strike Freedom) and return-to-hand
# (Sazabi's recursion) are opposite mechanics for cross-game analysis.
_RETURNED_RE = re.compile(r"^(.+?) returned to (hand|deck)$")
# A "return to deck" effect (e.g. Strike Freedom Gundam's Attack ability)
# targeting a Unit token instead of a real card: tokens have nowhere to
# return to, so the client reports this outcome instead.
_REMOVED_FROM_PLAY_RE = re.compile(r"^(.+?) removed from play$")
_HEALED_RE = re.compile(r"^Healed \d+ damage to: .+$")
_REPAIRED_RE = re.compile(r"^.+? repaired \d+ from .+$")
_RESTED_RE = re.compile(r"^(?:Already rested|Rested) unit: .+$")
_RESTED_BASE_RE = re.compile(r"^Rested base: .+$")
_SET_ACTIVE_RE = re.compile(r"^Set Active: .+$")
# "Placed N Resource EX" (a player's own resource-phase play), the
# "<source>: Placed N EX Resource" variant (a unit ability placing one,
# reversed word order, e.g. Gundam Pharact's Link effect), or "...Placed
# N rested EX Resource" (placed already-rested, e.g. Suletta Mercury's
# During-Link effect).
_RESOURCE_EX_RE = re.compile(r"^(?:.+?: )?Placed \d+ (?:rested )?(?:Resource EX|EX Resource)$")
# Optional suffix when the cost also exiles an EX Resource (e.g. Destiny
# Gundam's own attack-boost cost).
_RESTED_RESOURCES_RE = re.compile(r"^Rested \d+ Resources?(?: \(Exiled \d+ Resource EX\))?$")
# A plain (non-EX) Resource, distinct from _RESOURCE_EX_RE above (e.g. Duo
# Maxwell's own cost paid as "Rested resource placed" / "Placed N
# Resource").
_RESTED_RESOURCE_PLACED_RE = re.compile(r"^Rested resource placed$")
_PLACED_RESOURCE_RE = re.compile(r"^Placed \d+ Resource$")
# A During-Link/Activate effect that would set a Resource active but has
# none available (e.g. Suletta Mercury), or an Activate ability that
# whiffs entirely for lack of a legal target (e.g. Cyclone Punch).
_NO_RESOURCES_ACTIVE_RE = re.compile(r"^.+?: no resources to set as active$")
_CANNOT_ACTIVATE_RE = re.compile(r"^Cannot activate .+?: No available targets$")
# "Activated <card>: <effect summary>" all on one line (e.g. Zaku I Sniper
# Type Support), distinct from the two-part "Activated: <card>" form
# handled by _ACTIVATED_RE (no name before the colon there).
_ACTIVATED_EFFECT_RE = re.compile(r"^Activated (.+?): .+$")
# A unit/pilot ability redirecting an in-progress attack to itself or
# another unit (e.g. Guel Jeturk's action card).
_ATTACK_TARGET_CHANGED_RE = re.compile(r"^.+?: attack target changed$")
_NO_TARGETS_RE = re.compile(r"^No targets for .+$")
_DAMAGE_PREVENTED_RE = re.compile(r"^Damage prevented$")
# "Returned to deck bottom/top": the target of this specific effect is
# never named by the client (unlike most other targeted effects), seen
# after abilities as varied as Kayra's Re-GZ's own Deploy, Gundam
# Heavyarms's Deploy, and pilot When-Linked effects (e.g. Amate Yuzuriha
# (Machu)) - there is no more identity to extract here, just the fact
# that an unnamed card was bounced.
_RETURNED_BOTTOM_RE = re.compile(r"^Returned to deck bottom$")
_RETURNED_TOP_RE = re.compile(r"^Returned to deck top$")
_NO_MORE_SHIELDS_RE = re.compile(r"^No more Shield cards to add to hand$")
_GAME_OVER_RE = re.compile(r"^No more shields available, game is over!$")
_SELECTING_RE = re.compile(r"^Selecting target for .+$")
_DISCARDED_RE = re.compile(r"^(.+?) discarded$")
# Reversed word order seen for some discard-cost/effect phrasings (e.g.
# "Selecting target for discard" / "Discarded Jegan"), distinct from the
# far more common "<card> discarded" trailing form above.
_DISCARDED_REVERSED_RE = re.compile(r"^Discarded (.+)$")
# A shield hit reduced to zero damage (e.g. by a prevention/reduction
# effect) - the shield itself isn't lost, just a damage-step outcome.
_SHIELD_ZERO_DAMAGE_RE = re.compile(r"^Shield received 0 damage$")

_NAME_LIST_SPLIT_RE = re.compile(r",\s+|\s+and\s+")

# Multi-target effect damage ("SRC: Dealt N damage to: A and B"). Unlike the
# single-target form, the client never appends "now destroyed" to these, so
# lethal pings are invisible in the text — parse_multi_target_damage exposes
# them for HP-based death inference in tools.import_game_log_impl.
_MULTI_DEALT_RE = re.compile(r"^(?:.+?: )?Dealt (\d+) damage to: (.+)$")

# Canonical key order for a finished attack dict: effect lines arriving
# before "Battle started" would otherwise make `outcome` precede
# `blockers`/`final_target` in the emitted YAML.
_BATTLE_KEY_ORDER = (
    "action",
    "player",
    "attacker",
    "trigger",
    "declared_target",
    "blockers",
    "action_step",
    "modifiers",
    "final_target",
    "outcome",
)


def _split_names(joined: str) -> list[str]:
    """Split an 'A, B and C' card-name list. Best effort: a card name that
    itself contains ' and ' would be split wrongly, but none exist today."""
    return [n.strip() for n in _NAME_LIST_SPLIT_RE.split(joined) if n.strip()]


def parse_multi_target_damage(line: str) -> tuple[int, list[str]] | None:
    """'SRC: Dealt N damage to: A and B' -> (N, [A, B]); None otherwise."""
    m = _MULTI_DEALT_RE.match(line)
    if not m:
        return None
    return int(m.group(1)), _split_names(m.group(2))


def _ordered_battle(battle: dict) -> dict:
    """Reorder a finished attack dict into _BATTLE_KEY_ORDER (unknown keys
    keep their arrival order at the end)."""
    ordered = {k: battle[k] for k in _BATTLE_KEY_ORDER if k in battle}
    for k, v in battle.items():
        if k not in ordered:
            ordered[k] = v
    return ordered


def parse_game_log(text: str) -> dict:
    """Parse a chat-exported game log into a structured dict.

    Returns players, first_player, mulligans, setup choices, per-turn action
    lists, every card name seen (with owners/contexts, for later database
    resolution), a per-player shield tally, the detected winner (if the log
    reaches "Winner!"), and any lines that didn't match a known pattern
    (`unparsed`) so nothing gets dropped silently.
    """
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]

    # Anything before "Game started!" is the client's header banner.
    source_header = None
    if "Game started!" in lines:
        start = lines.index("Game started!")
        if start > 0:
            source_header = " / ".join(lines[:start])
        lines = lines[start:]

    # Player names are the lines immediately preceding a setup-choice line,
    # skipping past any noise lines (flow markers, timeout warnings like
    # "Timeout 1") that the client can interleave between a speaker's name
    # and their actual choice.
    players: list[str] = []
    for i, ln in enumerate(lines):
        if ln in _SETUP_CHOICES and i > 0:
            j = i - 1
            while j >= 0 and (lines[j] in _MARKERS or _TIMEOUT_RE.match(lines[j])):
                j -= 1
            prev = lines[j] if j >= 0 else None
            if prev is not None and prev not in _SETUP_CHOICES and prev not in players:
                players.append(prev)

    def other(player: str | None) -> str | None:
        for p in players:
            if p != player:
                return p
        return None

    setup: list[dict] = []
    turns: list[dict] = []
    unparsed: list[str] = []
    deaths: list[tuple[str, int]] = []
    seen_cards: dict[str, dict] = {}
    mulligans: dict[str, bool] = {p: False for p in players}
    tally = {
        p: {
            "ex_base_destroyed_turn": None,
            "ex_base_replaced_turn": None,
            "shields_lost": 0,
            "shields_to_hand": 0,
            "shields_deployed": 0,
        }
        for p in players
    }
    first_player: str | None = None
    winner: str | None = None

    actor: str | None = None
    turn: dict | None = None
    last_action: dict | None = None
    battle: dict | None = None
    # Command played during a battle's action step: its effect lines attach
    # here instead of the battle outcome until the damage step starts.
    action_step_play: dict | None = None
    # Shield revealed but not yet resolved: a following "Played base: <same
    # name>" means it Burst-deployed out of the shield area (counted apart
    # from discarded/added-to-hand shields).
    pending_shield: tuple[str, str | None] | None = None

    def note_card(name: str, owner: str | None = None, context: str | None = None) -> None:
        entry = seen_cards.setdefault(name, {"owners": set(), "contexts": set()})
        if owner:
            entry["owners"].add(owner)
        if context:
            entry["contexts"].add(context)

    def add_action(action: dict) -> None:
        nonlocal last_action
        if turn is None:
            unparsed.append(json.dumps(action, ensure_ascii=False))
            return
        turn["actions"].append(action)
        last_action = action

    def add_effect(raw: str) -> None:
        if action_step_play is not None:
            action_step_play.setdefault("effects", []).append(raw)
        elif battle is not None:
            battle.setdefault("outcome", []).append(raw)
        elif last_action is not None:
            last_action.setdefault("effects", []).append(raw)
        elif turn is not None:
            turn["actions"].append({"action": "event", "player": actor, "text": raw})
        else:
            unparsed.append(raw)

    def defender() -> str | None:
        if battle is not None and battle.get("player"):
            return other(battle["player"])
        return actor

    def record_death(name: str) -> None:
        """Explicitly-logged destructions only: units killed by cumulative
        pings without a 'now destroyed' line stay implicit here too."""
        if name != "EX Base" and turn is not None:
            deaths.append((name, turn["turn"]))

    def handle_received_destroyed(name: str) -> None:
        """A '<name> received N damage, now destroyed' target: EX Base
        updates the shields tally instead of the casualties list (shared
        by the plain and Breach-prefixed damage lines)."""
        if name == "EX Base":
            owner = defender()
            if owner in tally and turn is not None:
                tally[owner]["ex_base_destroyed_turn"] = turn["turn"]
        else:
            record_death(name)

    def handle_shield_line(raw: str, inner: str) -> bool:
        """Shield reveals/discards/to-hand; `raw` may carry a Breach prefix.
        "Shield card(s):" can name more than one card at once (a single hit
        clearing multiple shields), each counting separately toward the
        tally."""
        nonlocal pending_shield
        m = _SHIELD_DISCARDED_RE.match(inner)
        if m:
            owner = defender()
            names = _split_names(m.group(1))
            if owner in tally:
                tally[owner]["shields_lost"] += len(names)
            for name in names:
                note_card(name, owner=owner, context="shield")
            add_effect(raw)
            return True
        m = _SHIELD_TO_HAND_RE.match(inner)
        if m:
            owner = defender()
            if owner in tally:
                tally[owner]["shields_to_hand"] += 1
            if m.group(1):
                note_card(m.group(1), owner=owner, context="shield")
            pending_shield = None
            add_effect(raw)
            return True
        m = _SHIELD_TO_TRASH_RE.match(inner)
        if m:
            owner = defender()
            names = _split_names(m.group(1))
            if owner in tally:
                tally[owner]["shields_lost"] += len(names)
            for name in names:
                note_card(name, owner=owner, context="shield")
            pending_shield = None
            add_effect(raw)
            return True
        m = _SHIELD_REVEALED_RE.match(inner)
        if m:
            # Reveal only; the following line says where the card went
            # (added to hand, or Burst-deployed via a "Played base" line).
            # Burst-resolution tracking only applies to the single-card
            # case: with multiple simultaneous reveals there's no way to
            # tell which (if any) gets played from the next line alone.
            names = _split_names(m.group(1))
            owner = defender()
            for name in names:
                note_card(name, owner=owner, context="shield")
            pending_shield = (names[0], owner) if len(names) == 1 else None
            add_effect(raw)
            return True
        return False

    def resolve_pending_shield_deploy(card_name: str) -> None:
        """A revealed shield that gets played was a Burst deploy: it left
        the shield area without being discarded or added to hand."""
        nonlocal pending_shield
        if pending_shield is not None and pending_shield[0] == card_name:
            owner = pending_shield[1]
            if owner in tally:
                tally[owner]["shields_deployed"] += 1
            pending_shield = None

    for ln in lines:
        if ln in players:
            actor = ln
            continue
        choice = _SETUP_CHOICES.get(ln)
        if choice:
            setup.append({"player": actor, "action": choice})
            if choice == "choose_first_player":
                first_player = actor
            elif choice == "choose_second_player":
                first_player = other(actor)
            elif choice == "mulligan" and actor in mulligans:
                mulligans[actor] = True
            continue
        m = _TURN_START_RE.match(ln)
        if m:
            number = int(m.group(1))
            if turn is None or turn["turn"] != number:
                turn = {"turn": number, "active_player": None, "actions": []}
                turns.append(turn)
            # else: the client restarted the same turn ("Turn N started!"
            # twice, seen after a mid-turn pass) — keep appending to the
            # existing entry instead of creating a spurious duplicate.
            last_action = None
            battle = None
            action_step_play = None
            pending_shield = None
            continue
        if ln == "Winner!":
            winner = actor
            continue
        if ln in _MARKERS or _TIMEOUT_RE.match(ln):
            continue
        if _SELECTING_RE.match(ln):
            continue

        # --- battle flow ---
        if ln == "Battle initiated":
            battle = {"action": "attack"}
            action_step_play = None
            continue
        m = _BATTLE_DECLARED_RE.match(ln)
        if m and battle is not None:
            battle["player"] = actor
            battle["attacker"] = m.group(1)
            target = m.group(2)
            battle["declared_target"] = "player" if target == "Enemy Player" else target
            note_card(m.group(1), owner=actor, context="attacker")
            continue
        if ln in ("No blockers available", "Assigned no blocker"):
            if battle is not None:
                battle["blockers"] = "none"
            continue
        m = _CANT_BLOCK_RE.match(ln)
        if m and battle is not None:
            battle["blockers"] = f"none ({m.group(1)})"
            continue
        m = _ASSIGNED_BLOCKER_RE.match(ln)
        if m and battle is not None:
            battle["blockers"] = m.group(1)
            note_card(m.group(1), owner=defender(), context="blocker")
            continue
        m = _BATTLE_STARTED_RE.match(ln)
        if m and battle is not None:
            target = m.group(2)
            battle["final_target"] = {"Enemy Player": "player", "Enemy Shield": "shield"}.get(
                target, target
            )
            action_step_play = None
            continue
        if m and battle is None:
            # An ability jumps straight to the damage step with no normal
            # declare/block flow (e.g. Nu Gundam LR's own When-Paired:
            # exile 3, then battle the chosen enemy, damage step only).
            target = m.group(2)
            battle = {
                "action": "attack",
                "player": actor,
                "attacker": m.group(1),
                "trigger": "ability",
                "final_target": {"Enemy Player": "player", "Enemy Shield": "shield"}.get(
                    target, target
                ),
            }
            note_card(m.group(1), owner=actor, context="attacker")
            action_step_play = None
            continue
        if ln == "Battle ended":
            if battle is not None:
                add_action(_ordered_battle(battle))
                battle = None
                action_step_play = None
            pending_shield = None
            continue

        # --- actions ---
        m = _PLAYED_ACTION_RE.match(ln)
        if m:
            resolve_pending_shield_deploy(m.group(1))
            note_card(m.group(1), owner=actor, context="command")
            play = {"action": "play_command", "player": actor, "card": m.group(1)}
            if battle is not None:
                battle.setdefault("action_step", []).append(play)
                action_step_play = play
            else:
                add_action(play)
            continue
        m = _ACTIVATED_RE.match(ln)
        if m:
            note_card(m.group(1), owner=actor, context="activated")
            add_action({"action": "activate", "card": m.group(1)})
            continue
        m = _DEPLOYED_RE.match(ln)
        if m:
            note_card(m.group(1), owner=actor, context="deployed")
            add_action({"action": "deploy", "card": m.group(1)})
            continue
        m = _PLAYED_BASE_RE.match(ln)
        if m:
            resolve_pending_shield_deploy(m.group(1))
            note_card(m.group(1), owner=actor, context="base")
            add_action({"action": "play_base", "card": m.group(1)})
            continue
        m = _REPLACED_BASE_RE.match(ln)
        if m:
            replaced, new_card = m.group(1), m.group(2)
            note_card(new_card, owner=actor, context="base")
            add_action({"action": "play_base", "card": new_card, "replaced": replaced})
            if replaced == "EX Base" and actor in tally and turn is not None:
                tally[actor]["ex_base_replaced_turn"] = turn["turn"]
            continue
        m = _PAIR_PILOT_RE.match(ln)
        if m:
            note_card(m.group(2), owner=actor, context="pilot")
            add_action(
                {
                    "action": "pair_pilot",
                    "pilot": m.group(2),
                    "unit": m.group(3),
                    "linked": m.group(1) == "Linked",
                }
            )
            continue

        # --- effects / damage / shields ---
        if handle_shield_line(ln, ln):
            continue
        m = _BREACH_RE.match(ln)
        if m:
            inner = m.group(1)
            if not handle_shield_line(ln, inner):
                inner_m = _RECEIVED_RE.match(inner)
                if inner_m and inner.endswith("now destroyed"):
                    handle_received_destroyed(inner_m.group(1))
                add_effect(ln)
            continue
        m = _RECEIVED_RE.match(ln)
        if m:
            if ln.endswith("now destroyed"):
                handle_received_destroyed(m.group(1))
            add_effect(ln)
            continue
        m = _DEALT_DESTROYED_RE.match(ln)
        if m:
            record_death(m.group(1))
            add_effect(ln)
            continue
        m = _DESTROYED_RE.match(ln)
        if m:
            note_card(m.group(1), owner=actor, context="attacker")
            record_death(m.group(2))
            add_effect(ln)
            continue
        m = _PLAIN_DESTROYED_RE.match(ln)
        if m:
            handle_received_destroyed(m.group(1))
            add_effect(ln)
            continue
        m = _MILLED_RE.match(ln)
        if m:
            for name in _split_names(m.group(2)):
                note_card(name, owner=actor, context="milled")
            add_effect(ln)
            continue
        m = _EXILED_RE.match(ln)
        if m:
            for name in _split_names(m.group(1)):
                note_card(name, owner=actor, context="exiled")
            add_effect(ln)
            continue
        m = _RETURNED_RE.match(ln)
        if m:
            note_card(m.group(1), owner=actor, context=f"returned to {m.group(2)}")
            add_effect(ln)
            continue
        m = _REMOVED_FROM_PLAY_RE.match(ln)
        if m:
            note_card(m.group(1), owner=actor, context="removed from play")
            add_effect(ln)
            continue
        m = _CARD_TO_HAND_RE.match(ln)
        if m:
            note_card(m.group(1), owner=actor, context="added to hand")
            add_effect(ln)
            continue
        if _MODIFIER_RE.match(ln):
            if battle is not None and action_step_play is None:
                battle.setdefault("modifiers", []).append(ln)
            else:
                add_effect(ln)
            continue
        m = _ACTIVATED_EFFECT_RE.match(ln)
        if m:
            note_card(m.group(1), owner=actor, context="activated")
            add_effect(ln)
            continue
        if (
            _DEALT_RE.match(ln)
            or _DEALT_NOSRC_RE.match(ln)
            or _DRAW_RE.match(ln)
            or _CHOSE_RE.match(ln)
            or _HEALED_RE.match(ln)
            or _REPAIRED_RE.match(ln)
            or _RESTED_RE.match(ln)
            or _RESTED_BASE_RE.match(ln)
            or _SET_ACTIVE_RE.match(ln)
            or _RESOURCE_ACTIVE_RE.match(ln)
            or _RESOURCE_EX_RE.match(ln)
            or _RESTED_RESOURCES_RE.match(ln)
            or _RESTED_RESOURCE_PLACED_RE.match(ln)
            or _PLACED_RESOURCE_RE.match(ln)
            or _NO_RESOURCES_ACTIVE_RE.match(ln)
            or _CANNOT_ACTIVATE_RE.match(ln)
            or _ATTACK_TARGET_CHANGED_RE.match(ln)
            or _NO_TARGETS_RE.match(ln)
            or _DAMAGE_PREVENTED_RE.match(ln)
            or _RETURNED_BOTTOM_RE.match(ln)
            or _RETURNED_TOP_RE.match(ln)
            or _SHIELD_ZERO_DAMAGE_RE.match(ln)
            or _NO_MORE_SHIELDS_RE.match(ln)
            or _GAME_OVER_RE.match(ln)
        ):
            add_effect(ln)
            continue
        m = _DISCARDED_REVERSED_RE.match(ln)
        if m:
            for name in _split_names(m.group(1)):
                note_card(name, owner=actor, context="discarded")
            add_effect(ln)
            continue
        m = _DISCARDED_RE.match(ln)
        if m:
            # Multiple cards can be discarded in one line ("A and B discarded").
            for name in _split_names(m.group(1)):
                note_card(name, owner=actor, context="discarded")
            add_effect(ln)
            continue

        # Turn context makes finding the line in the raw log (to design the
        # missing pattern) immediate.
        unparsed.append(ln if turn is None else f"[turn {turn['turn']}] {ln}")

    # A log truncated mid-battle still keeps what the battle recorded so far.
    if battle is not None:
        add_action(_ordered_battle(battle))

    if first_player in players:
        start = players.index(first_player)
        for t in turns:
            t["active_player"] = players[(start + t["turn"] - 1) % len(players)]

    # Attribute explicit destructions to the card's owner (known once the
    # whole log is read); names both players used end up unattributed.
    casualties: dict[str, list[dict]] = {p: [] for p in players}
    unattributed: list[dict] = []
    for name, turn_no in deaths:
        owners = seen_cards.get(name, {}).get("owners", set())
        entry = {"card": name, "turn": turn_no}
        if len(owners) == 1:
            casualties[next(iter(owners))].append(entry)
        else:
            unattributed.append(entry)
    if unattributed:
        casualties["unattributed"] = unattributed

    shields_tally: dict[str, dict] = {}
    for p in players:
        t = tally[p]
        destroyed_turn = t["ex_base_destroyed_turn"]
        replaced_turn = t["ex_base_replaced_turn"]
        if destroyed_turn is not None:
            ex_base = f"destroyed (turn {destroyed_turn})"
        elif replaced_turn is not None:
            ex_base = f"replaced with a base (turn {replaced_turn})"
        else:
            ex_base = "not destroyed in log"
        shields_tally[p] = {
            "ex_base": ex_base,
            "shields_lost": t["shields_lost"],
            "shields_to_hand": t["shields_to_hand"],
            "shields_deployed": t["shields_deployed"],
            "shields_remaining": max(
                STARTING_SHIELDS
                - t["shields_lost"]
                - t["shields_to_hand"]
                - t["shields_deployed"],
                0,
            ),
        }

    return {
        "source_header": source_header,
        "players": players,
        "first_player": first_player,
        "mulligans": mulligans,
        "winner": winner,
        "setup": setup,
        "turns": turns,
        "cards_seen": {
            name: {"owners": sorted(info["owners"]), "contexts": sorted(info["contexts"])}
            for name, info in seen_cards.items()
        },
        "casualties": casualties,
        "shields_tally": shields_tally,
        "unparsed": unparsed,
    }


# --- minimal YAML emitter -------------------------------------------------

# A leading letter/underscore is required: purely numeric-looking keys
# ("0622" as a player name) would otherwise be parsed back as integers.
_PLAIN_KEY_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _scalar(value) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, (int, float)):
        return str(value)
    # JSON string quoting is valid YAML and sidesteps every YAML quoting rule.
    return json.dumps(str(value), ensure_ascii=False)


def _key(k) -> str:
    s = str(k)
    return s if _PLAIN_KEY_RE.match(s) else json.dumps(s, ensure_ascii=False)


def _emit_mapping(mapping: dict, indent: int, lines: list[str]) -> None:
    pad = "  " * indent
    for k, v in mapping.items():
        if isinstance(v, dict) and v:
            lines.append(f"{pad}{_key(k)}:")
            _emit_mapping(v, indent + 1, lines)
        elif isinstance(v, list) and v:
            lines.append(f"{pad}{_key(k)}:")
            _emit_sequence(v, indent + 1, lines)
        elif isinstance(v, dict):
            lines.append(f"{pad}{_key(k)}: {{}}")
        elif isinstance(v, list):
            lines.append(f"{pad}{_key(k)}: []")
        else:
            lines.append(f"{pad}{_key(k)}: {_scalar(v)}")


def _emit_sequence(seq: list, indent: int, lines: list[str]) -> None:
    pad = "  " * indent
    for item in seq:
        if isinstance(item, dict) and item:
            sub: list[str] = []
            _emit_mapping(item, indent + 1, sub)
            lines.append(f"{pad}- {sub[0].lstrip()}")
            lines.extend(sub[1:])
        elif isinstance(item, list) and item:
            lines.append(f"{pad}-")
            _emit_sequence(item, indent + 1, lines)
        elif isinstance(item, dict):
            lines.append(f"{pad}- {{}}")
        elif isinstance(item, list):
            lines.append(f"{pad}- []")
        else:
            lines.append(f"{pad}- {_scalar(item)}")


def dump_yaml(value) -> str:
    """Render nested dicts/lists/scalars as YAML text. Strings are emitted
    JSON-quoted (valid YAML), so arbitrary card names are always safe."""
    if isinstance(value, dict):
        if not value:
            return "{}\n"
        lines: list[str] = []
        _emit_mapping(value, 0, lines)
    elif isinstance(value, list):
        if not value:
            return "[]\n"
        lines = []
        _emit_sequence(value, 0, lines)
    else:
        return _scalar(value) + "\n"
    return "\n".join(lines) + "\n"
