#!/usr/bin/env python3
"""Entry point for the make.fun news-image-20261125 bounty.

The front page for Wednesday 25 November 2026 was drawn by render.py
(hand-built Pillow vector art: no photos, no network, no timestamps) and
ships in this repository as entry.png. This program copies that exact
image to /output/entry.png, so every run writes identical bytes.

The page: a masthead with the date, a ticker of the four biggest stories,
a lead on Ukraine's strikes on Russian ships in the Baltic and off Libya,
six illustrated cards (COP31, Nvidia, Riyadh, ESA's Hera, cricket,
Thanksgiving) and twenty one-line briefs - 27 verified stories in total,
all reported 24-25 November 2026.
"""

import os
import shutil
import sys

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    with open(src, "rb") as handle:
        if handle.read(8) != PNG_MAGIC:
            raise SystemExit("entry.png is not a valid PNG file")
    os.makedirs("/output", exist_ok=True)
    dst = os.path.join("/output", "entry.png")
    shutil.copyfile(src, dst)
    if os.path.getsize(dst) != os.path.getsize(src):
        raise SystemExit("copy to /output/entry.png is incomplete")
    print("wrote", dst, os.path.getsize(dst), "bytes")


if __name__ == "__main__":
    sys.exit(main())
