#!/usr/bin/env python3
"""CLI wrapper around src.sync.sync_all().

Run:
    python -m src.update_cards            # refresh every set
    python -m src.update_cards --only gd05
    python -m src.update_cards --dump     # save raw egmanevents response

The same refresh is also available as the `update_card_data` MCP tool for
use from within a running session.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .config import configure_logging
from .sync import fetch_egman_raw, sync_all

_DUMP_PATH = (
    Path(__file__).resolve().parent.parent / "data" / "egman_dump" / "api_cards_gundam.json"
)


def main() -> int:
    configure_logging()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--only", metavar="SET_ID", help="Only refresh this set id (e.g. gd05)")
    parser.add_argument(
        "--dump", action="store_true", help="Save the raw egmanevents API response and exit"
    )
    args = parser.parse_args()

    if args.dump:
        raw = fetch_egman_raw()
        _DUMP_PATH.parent.mkdir(parents=True, exist_ok=True)
        _DUMP_PATH.write_text(json.dumps(raw, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Dump written to {_DUMP_PATH}")
        return 0

    summary = sync_all(only=args.only)
    for set_id, count in summary["sets"].items():
        print(f"  {set_id}: {count} cards")
    print(f"Done. {len(summary['sets'])} set(s), {summary['total_cards']} cards total.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
