# Gundam Card Game — Banned & Restricted Card List

Source: official banned/restricted list update published **2026-07-10**,
effective **2026-07-24**. Re-run the extraction (see bottom of this file) if
a newer PDF is dropped in `data/rules/bannedlist.pdf`.

> GCG rules permit up to four copies of cards with the same card number in a
> deck. Banned/restricted status only applies in official or sanctioned
> tournaments:
> - **Banned**: not even one copy allowed in deck or sideboard.
> - **Restricted (N)**: at most N copies total across deck + sideboard combined.
> - **Banned pair**: cards A and B cannot both be used in the same deck at the same time.

## Banned cards (effective 2026-07-24)

| Card | Reason |
|---|---|
| GD01-020 Anksha | Blue-purple decks using Anksha's direct-damage-to-Units ability had an outsized win rate. |

## Restricted cards

| Card | Limit | Notes |
|---|---|---|
| ST02-016 Corsica Base | Restricted (2) | Carried over from a previous update, unchanged this cycle. |

No new restricted cards were added in this update.

## Banned pairs (new category, introduced this update)

Cards A and B below cannot both appear in the same deck.

| A | B | Reason |
|---|---|---|
| GD01-008 Guntank | GD05-015 M1 Astray Shrike | Same stats/abilities, designed for trait synergy; combined win rate with direct-damage-to-Units decks was too high. |
| ST01-010 Amuro Ray | ST05-010 Mikazuki Augus | Blue-purple decks combining these two were exceptionally strong. |

### Group banned pair: "vanilla" Lv.2 / cost 1 / 2 AP / 2 HP Units

Any two *distinct* card numbers from the list below are a banned pair with
each other — i.e. a deck can include at most **one** card number from this
entire group (still capped at 4 copies of that single number, as normal).
Future GD05+ cards matching the same description ("a Unit card that is Lv.2
with cost 1, 2 AP, and 2 HP, and without effects") are added to this group
automatically on release, per the official ruling.

- GD01-035 Zaku Ⅱ
- GD01-060 Zaku Mariner
- GD01-085 Demi Garrison
- GD02-013 Hizack
- GD02-080 Nemo
- GD03-032 Zaku (Four Snake Eyes') [YETI] (GQ)
- GD03-063 0 Gundam
- GD04-078 Borjarnon
- GD05-014 Javelin
- GD05-027 Jegan
- GD05-042 Shining Gundam
- GD05-062 Hobby Hizack
- GD05-077 Leo
- ST01-005 GM
- ST04-008 Ginn
- ST05-004 Graze Custom
- ST05-009 Graze
- ST06-004 Gelgoog (GQ)
- ST09-005 Zaku Warrior
- ST10-005 Nemo

Note: GD05-014 (Javelin), GD05-027 (Jegan), GD05-062 (Hobby Hizack), and
GD05-077 (Leo) are now present in the local synced dataset (GD05 was
re-synced in full, see `scripts/sync_egman.py` history) and all four have
been verified to match the "Lv.2/cost 1/2 AP/2 HP" description.

Note: the Iron Blooded Orphans starter deck [ST05] is explicitly grandfathered
in — it contains two matching cards (Graze Custom, Graze) but remains legal
for sanctioned tournaments as long as its stock lineup isn't modified.

## Context (from the official announcement)

The developers cited fast-paced, low-cost-Unit "rush" decks (blue-purple and
blue-green in particular) as the main meta concern. The banned-pair mechanism
is a new, more surgical tool introduced this cycle to curb specific
combinations without blanket-banning individual cards. They noted a possible
future fundamental rule change is under consideration, which would trigger a
re-evaluation of the whole banned/restricted list.

---
*Extracted from `bannedlist.pdf` via `pypdf`; source is a single-page PDF of
the official web announcement.*
