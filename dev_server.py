"""Wrapper for `mcp dev` — avoids relative import issues."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from kiraya_gundam_deckmanager.server import mcp  # noqa: E402

if __name__ == "__main__":
    mcp.run()
