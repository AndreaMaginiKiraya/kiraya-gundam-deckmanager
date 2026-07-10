"""Wrapper for `mcp dev` — avoids relative import issues."""
from src.server import mcp

if __name__ == "__main__":
    mcp.run()
