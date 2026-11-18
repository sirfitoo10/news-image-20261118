#!/usr/bin/env python3
"""make.fun news-image-20261118 entrypoint.

Copies the repository's bundled entry image to the graded output directory
unchanged. The image itself is drawn by render_news.py (Pillow) and stored
in the repository, so both graded runs write identical bytes: no network,
no clock, no randomness. Python 3.13, standard library only."""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
TARGET = os.path.join(OUTPUT_DIR, "entry.png")

os.makedirs(OUTPUT_DIR, exist_ok=True)
shutil.copyfile(SOURCE, TARGET)
print("entry image written to", TARGET)
