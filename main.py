"""Entrypoint for the news-image-20261122 entry.

Running this file rebuilds the front page image (entry.png) from the
dated story data and layout engine in build_entry.py, then verifies
the artifact exists and is a valid 1024x1024 PNG.
"""

import os

from PIL import Image

from build_entry import build

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")


def main():
    report = build(OUT)
    with Image.open(OUT) as im:
        assert im.size == (1024, 1024), f"unexpected size {im.size}"
        assert im.format == "PNG", f"unexpected format {im.format}"
    size = os.path.getsize(OUT)
    print(f"entry.png written: {size} bytes, 1024x1024")
    for name, bottom in report:
        print(f"  {name}: {bottom}")
    return OUT


if __name__ == "__main__":
    main()
