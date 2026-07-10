"""Entrypoint: `python -m kiraya_gundam_deckmanager` or the
`kiraya-gundam-deckmanager-mcp` console script."""
from __future__ import annotations

from .config import configure_logging
from .server import mcp


def main() -> None:
    configure_logging()
    mcp.run()


if __name__ == "__main__":
    main()
