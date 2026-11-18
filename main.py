#!/usr/bin/env python3
"""make.fun news-image-20261118 entrypoint (second revision).

Copies the repository's bundled entry image to the graded output directory,
unchanged and byte for byte. render_news.py draws that image with Pillow and
the repository stores its bytes, so both graded runs write identical files
with no network, no clock and no randomness. Python 3.13, stdlib only."""

import os
import shutil


def paths():
    here = os.path.dirname(os.path.abspath(__file__))
    return (
        os.path.join(here, "entry.png"),
        os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.png"),
    )


def run():
    src, dst = paths()
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copyfile(src, dst)
    print("entry image written to", dst)


run()
