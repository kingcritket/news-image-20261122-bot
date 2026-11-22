#!/usr/bin/env python3
"""Ship entry.png to the make.fun output directory.

Standard library only. Reads entry.png sitting next to this file and
copies it into the directory named by the MAKEFUN_OUTPUT_DIR
environment variable (default: ./out).
"""

import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        print("entry.png not found next to main.py", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", os.path.join(here, "out"))
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("shipped", src, "->", dst, os.path.getsize(dst), "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
