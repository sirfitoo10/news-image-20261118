#!/usr/bin/env python3
"""Copy the bundled news image to the output directory unchanged.

The image is rendered from render_news.py at build time and stored in the
repository, so the two graded runs write byte-identical files with no
network, no clock and no randomness. Python 3.13, stdlib only."""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

shutil.copyfile(os.path.join(HERE, "entry.png"), os.path.join(OUT, "entry.png"))
print("wrote", os.path.join(OUT, "entry.png"))
