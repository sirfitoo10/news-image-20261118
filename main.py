#!/usr/bin/env python3
"""make.fun news-image-20261118 entrypoint.

Copies the repository's bundled entry image to the graded output directory
unchanged. render_news.py draws that image with Pillow and the repository
stores the bytes, so both graded runs write identical files: no network, no
clock, no randomness. Python 3.13, standard library only."""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE_NAME = "entry.png"
OUTPUT_KEY = "MAKEFUN_OUTPUT_DIR"
DEFAULT_OUT = "/output"


def target_dir():
    return os.environ.get(OUTPUT_KEY, DEFAULT_OUT)


def main():
    out_dir = target_dir()
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, SOURCE_NAME)
    dst = os.path.join(out_dir, SOURCE_NAME)
    shutil.copyfile(src, dst)
    print("entry image written to", dst)


if __name__ == "__main__":
    main()
