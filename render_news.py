"""Render the make.fun news-image entry: one page that sums up 18 November 2026.

Pillow draws each story card once, flowing into the shorter column, then the
inter-card gaps are widened evenly so both columns end flush above the brief
band. Output is a 1024x1024 PNG well under 1 MiB, and the same bytes on every
run (no randomness, no clock, no fonts outside the fixed paths below).
"""

import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
WIDTH_COL = 486
LEFT_X, RIGHT_X = 24, 514
HEADER_H = 92
FOOTER_H = 44
BAND_H = 76
TOP_Y = 108

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

BG = (12, 16, 26)
HEAD = (8, 11, 20)
CARD = (26, 33, 46)
WHITE = (240, 244, 250)
GREY = (168, 178, 192)
RED = (229, 57, 53)
AMBER = (255, 196, 0)

STORIES = [
    ("GULF CONFLICT", (229, 57, 53), "US strikes Iran's Qeshm Island", [
        "US jets hit a missile launch site after Iranian",
        "drones struck a US radar in Bahrain — the 3rd",
        "attack in 5 days. Three US carriers now in the",
        "Gulf; tankers hit mines in the Strait of Hormuz.",
        "Trump warns Iran over a reported 'dirty bomb'",
    ]),
    ("UKRAINE", (255, 140, 0), "Crimean Bridge badly damaged", [
        "Ukrainian drones and missiles struck the span —",
        "Zelensky hails an 'unprecedented' operation",
        "using only Ukrainian-made weapons.",
        "Russia bombs Ukrainian cities ahead of winter.",
    ]),
    ("DIPLOMACY", (0, 150, 255), "Putin meets Xi before trilateral", [
        "APEC in Shenzhen: Trump-Xi-Putin summit set for",
        "Nov 19. Quad leaders met in Manila — first",
        "leader-level talks in over two years.",
        "Xi calls for an open Asia-Pacific trade zone.",
    ]),
    ("AMERICAS", (0, 200, 120), "US loses measles-free status", [
        "Elimination status lost after 26 years amid",
        "outbreaks. FAA, banks and Microsoft outages —",
        "officials: 'not a cyberattack'.",
        "Waymo suspends freeway robotaxis in Calif.",
    ]),
    ("US POLITICS", (160, 120, 255), "Democrats flip Alaska Senate seat", [
        "Mary Peltola defeats Sen. Dan Sullivan; Dems",
        "to hold 56-44 when Congress convenes.",
    ]),
    ("AFRICA", (255, 120, 180), "Mauritius ultimatum over Chagos", [
        "UK told to hand over the islands by Dec 2026",
        "or face legal action.",
    ]),
    ("CLIMATE", (0, 190, 190), "COP31 split over fossil fuels", [
        "Antalya talks divide on phase-out wording;",
        "Rockstrom warns of tipping points. $200M",
        "pledged to the adaptation fund.",
    ]),
    ("TECH", (120, 220, 80), "Nvidia revenue doubles", [
        "Board rules out Huang's return as CEO; forms",
        "a national-security oversight committee.",
    ]),
]

BRIEF = [
    "19 die as An-12 crashes in Siberia",
    "Thaci jailed 17 months for witness tampering",
    "FIFA: Diallo to challenge Infantino",
    "46 hurt as trains collide in Prague",
    "Cyclone Akvan nears India's coast",
]


def font(size, bold=True):
    return ImageFont.truetype(BOLD if bold else REG, size)


def card_height(n_lines):
    """Same arithmetic the drawing routine uses, so heights never drift."""
    return 12 + 26 + 27 + n_lines * 23 + 12


def draw_card(d, x, y, tag, colour, title, lines, f19, f15, f15b):
    h = card_height(len(lines))
    d.rounded_rectangle([x, y, x + WIDTH_COL, y + h], radius=10, fill=CARD)
    d.rectangle([x, y, x + 6, y + h], fill=colour)
    yy = y + 12
    tw = d.textlength(tag, font=f15b)
    d.rounded_rectangle([x + 16, yy, x + 16 + tw + 14, yy + 22], radius=6, fill=colour)
    d.text((x + 23, yy + 3), tag, font=f15b, fill=(10, 12, 16))
    yy += 27
    d.text((x + 16, yy), title, font=f19, fill=WHITE)
    yy += 27
    for line in lines:
        d.text((x + 16, yy), line, font=f15, fill=GREY)
        yy += 23
    return h


def render(path):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    d.rectangle([0, 0, W, HEADER_H], fill=HEAD)
    d.text((28, 14), "WORLD NEWS", font=font(46), fill=RED)
    d.text((28, 62), "WEDNESDAY \u00b7 18 NOVEMBER 2026", font=font(19), fill=WHITE)
    d.text((W - 336, 30), "THE DAY IN ONE PAGE", font=font(21), fill=AMBER)

    f19, f15, f15b = font(19), font(15, False), font(15)

    band_y = H - FOOTER_H - 12 - BAND_H
    bottom = band_y - 14

    # assign each story to the currently shorter column, remembering heights
    columns = {0: [], 1: []}
    filled = [TOP_Y, TOP_Y]
    for story in STORIES:
        c = 0 if filled[0] <= filled[1] else 1
        columns[c].append(story)
        filled[c] += card_height(len(story[3])) + 12

    for c in (0, 1):
        cards = columns[c]
        used = sum(card_height(len(s[3])) for s in cards) + 12 * len(cards)
        extra = (bottom - TOP_Y - used) / max(1, len(cards))
        x = LEFT_X if c == 0 else RIGHT_X
        y = TOP_Y
        for tag, colour, title, lines in cards:
            h = draw_card(d, x, y, tag, colour, title, lines, f19, f15, f15b)
            y += h + 12 + extra

    d.rounded_rectangle([24, band_y, W - 24, band_y + BAND_H], radius=10, fill=(20, 26, 38))
    d.text((40, band_y + 10), "IN BRIEF", font=font(15), fill=AMBER)
    d.text((40, band_y + 34), " \u00b7 ".join(BRIEF[:3]), font=font(14, False), fill=GREY)
    d.text((40, band_y + 56), " \u00b7 ".join(BRIEF[3:]), font=font(14, False), fill=GREY)

    d.rectangle([0, H - FOOTER_H, W, H], fill=HEAD)
    d.text((28, H - 32),
           "SOURCES: Reuters \u00b7 AP \u00b7 Al Jazeera \u00b7 The Hindu \u00b7 Anadolu \u00b7 ABC"
           " \u2014 events of 18 Nov 2026 (UTC)",
           font=font(13, False), fill=GREY)
    d.text((W - 120, H - 32), "18 NOV 2026", font=font(13), fill=AMBER)

    img.save(path, optimize=True)
    return path


if __name__ == "__main__":
    out = os.environ.get("OUT", "entry.png")
    print(render(out), os.path.getsize(out), "bytes")
