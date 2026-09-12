#!/usr/bin/env python3
"""Build the Workshop preview for Smooth Zoom Transitions.

A stutter cannot be photographed, so the preview shows its cause instead: the
twelve systems vanilla schedules on a single zoom step against the same twelve
spread over six steps by this mod.

Designed for 200x200, which is the size Steam actually renders a preview at in
listings. That rules out an axis, step numbers and any per-step labelling - at
that size the image has to be two words and one shape. What survives is a tall
red column next to a low green comb, and a title set large enough to fill the
full width of the canvas.

Bar heights are the real numbers, not decoration: 12 on step 9 in vanilla,
and 1/1/3/4/2/1 on steps 7..12 with the mod.

    thumbnail.png         1280x1280, the Workshop preview (must stay under 1 MB)
    thumbnail-200px.png   the legibility check, regenerated every run

Usage: tools/make_thumbnail.py
"""
import pathlib

from PIL import Image, ImageDraw, ImageFont

OUT = pathlib.Path(__file__).resolve().parent.parent

S = 1280
MARGIN = 96
BG = (9, 12, 18)
FG = (238, 240, 244)
MUTED = (128, 136, 150)
RED = (214, 78, 62)
GREEN = (78, 184, 148)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

VANILLA_ON_STEP_9 = 12
MODDED_PER_STEP = [1, 1, 3, 4, 2, 1]   # steps 7..12

UNIT = 44           # pixels of bar per system
BASELINE = 1120


def fit(d, text, path, avail, start=200, minimum=24):
    size = start
    while size > minimum and d.textlength(text, font=ImageFont.truetype(path, size)) > avail:
        size -= 2
    return ImageFont.truetype(path, size)


def spaced(text):
    return " ".join(text)


def group(d, cx, widths_heights, colour, gap):
    total = sum(w for w, _ in widths_heights) + gap * (len(widths_heights) - 1)
    x = cx - total / 2
    for w, h in widths_heights:
        d.rectangle([x, BASELINE - h, x + w, BASELINE], fill=colour)
        x += w + gap


def main():
    im = Image.new("RGB", (S, S), BG)
    d = ImageDraw.Draw(im)
    avail = S - 2 * MARGIN

    d.text((MARGIN, 78), spaced("CRUSADER KINGS III"),
           font=ImageFont.truetype(FB, 30), fill=MUTED)

    # Both lines are eleven characters, so filling the width gives them the
    # same size without any hand tuning.
    f1 = fit(d, "SMOOTH ZOOM", FB, avail)
    f2 = fit(d, "TRANSITIONS", FB, avail)
    d.text((MARGIN, 150), "SMOOTH ZOOM", font=f1, fill=FG)
    d.text((MARGIN, 150 + f1.size + 14), "TRANSITIONS", font=f2, fill=FG)

    left_cx, right_cx = 340, 884
    group(d, left_cx, [(210, VANILLA_ON_STEP_9 * UNIT)], RED, 0)
    group(d, right_cx, [(80, n * UNIT) for n in MODDED_PER_STEP], GREEN, 26)

    d.line([MARGIN, BASELINE, S - MARGIN, BASELINE], fill=(38, 44, 54), width=4)

    cap = ImageFont.truetype(FB, 38)
    d.text((left_cx, BASELINE + 24), "VANILLA", font=cap, fill=MUTED, anchor="ma")
    d.text((right_cx, BASELINE + 24), "WITH THIS MOD", font=cap, fill=MUTED, anchor="ma")

    im.save(OUT / "thumbnail.png", optimize=True)
    im.resize((200, 200), Image.LANCZOS).save(OUT / "thumbnail-200px.png")
    kb = (OUT / "thumbnail.png").stat().st_size / 1024
    print(f"thumbnail.png {im.size[0]}x{im.size[1]} {kb:.0f} KB")


if __name__ == "__main__":
    main()
