"""Entrypoint for the news-image entry.

Copies the bundled ``entry.png`` next to this script into the output
directory requested by the ``MAKEFUN_OUTPUT_DIR`` environment variable
(``./out`` when unset), byte-for-byte, and reports what it did.
"""

from __future__ import annotations

import os
from pathlib import Path


def locate_source() -> Path:
    """Return the path of the entry image sitting beside this script."""
    here = Path(__file__).resolve().parent
    return here / "entry.png"


def locate_destination_dir() -> Path:
    """Return the output directory from the environment, defaulting to ./out."""
    raw = os.environ.get("MAKEFUN_OUTPUT_DIR") or "./out"
    return Path(raw).expanduser()


def main() -> int:
    source = locate_source()
    if not source.is_file():
        print(f"error: entry image not found: {source}")
        return 1

    dest_dir = locate_destination_dir()
    dest_dir.mkdir(parents=True, exist_ok=True)
    destination = dest_dir / source.name

    data = source.read_bytes()
    destination.write_bytes(data)

    print(f"copied {source} -> {destination} ({len(data)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
