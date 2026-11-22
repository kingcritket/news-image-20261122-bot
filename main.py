#!/usr/bin/env python3
"""Ship the built entry image to the make.fun output directory.

Copies ``entry.png`` (produced by ``build_entry.py``) into the directory
named by the ``MAKEFUN_OUTPUT_DIR`` environment variable (default
``./out``), creating it if needed. The copy is byte-for-byte identical
to the built image, so the shipped file is deterministic too.

No network access, no randomness, no clock: only the standard library.

Usage:
    MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENTRY = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "./out")
    if not os.path.isfile(ENTRY):
        print(f"entry.png not found at {ENTRY}; run build_entry.py first",
              file=sys.stderr)
        return 1
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(ENTRY, dest)
    print(f"copied {ENTRY} -> {dest} ({os.path.getsize(dest)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
