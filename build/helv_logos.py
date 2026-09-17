#!/usr/bin/env python3
"""Prepare HelloVoice's brand and client marks for the site.

Three jobs:
  * copy the wordmark, its knockout and the icons into site/assets/helv
  * copy the client marks the page actually uses
  * build the ten tiles the Trusted-by-Leaders fan needs — that section crops
    each slot to a rounded square and tilts it, so a bare logo floating on
    white reads as nothing. Each mark is centred on a solid ground drawn from
    the site's own palette.
"""
from PIL import Image
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
SRC_CLIENTS = SITE / "assets" / "clients"
OUT = SITE / "assets" / "helv"
TILES = OUT / "tiles"

# The palette, straight from the reference stylesheet's :root.
LINEN, SMOKE, WHITE = (233, 220, 210), (240, 240, 240), (255, 255, 255)
PALETTE = [LINEN, WHITE, SMOKE, LINEN, WHITE, SMOKE, LINEN, WHITE, SMOKE, LINEN]

# the fan: ten of the largest accounts
FAN = ["astrazeneca", "pfizer", "bayer", "abbvie", "abbott",
       "boston-scientific", "gilead", "loreal-dermatological-beauty",
       "la-roche-posay", "mondelez-international"]

# the marquee under the hero
BANNER = ["astrazeneca", "pfizer", "bayer", "abbvie", "abbott", "gilead",
          "boston-scientific", "hikma", "menarini", "fresenius"]

# the knocked-out wall on black
WALL = ["molnlycke", "spimaco", "zoetis", "nahdi", "eva-pharma", "avalon-pharma"]

BRAND = ["logo.webp", "logo@2x.webp", "logo-knockout.webp",
         "icon-32.png", "icon-180.png", "icon-512.png"]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    TILES.mkdir(parents=True, exist_ok=True)

    for f in BRAND:
        p = SITE / "assets" / "brand" / f
        if p.exists():
            shutil.copy2(p, OUT / f)
    print(f"brand marks: {len(BRAND)}")

    used = sorted(set(BANNER + WALL + FAN))
    missing = [c for c in used if not (SRC_CLIENTS / f"{c}.webp").exists()]
    for c in used:
        src = SRC_CLIENTS / f"{c}.webp"
        if src.exists():
            shutil.copy2(src, OUT / f"{c}.webp")
    print(f"client marks: {len(used) - len(missing)} copied"
          + (f", MISSING {missing}" if missing else ""))

    # ---- the fan tiles
    SIZE, INSET = 640, 0.66
    for i, name in enumerate(FAN):
        src = SRC_CLIENTS / f"{name}.webp"
        if not src.exists():
            print(f"  ! no mark for {name}")
            continue
        ground = PALETTE[i % len(PALETTE)]
        tile = Image.new("RGB", (SIZE, SIZE), ground)
        mark = Image.open(src).convert("RGBA")
        box = round(SIZE * INSET)
        scale = min(box / mark.width, box / mark.height)
        mark = mark.resize((max(1, round(mark.width * scale)),
                            max(1, round(mark.height * scale))), Image.LANCZOS)
        tile.paste(mark, ((SIZE - mark.width) // 2, (SIZE - mark.height) // 2), mark)
        tile.save(TILES / f"{name}.webp", quality=92, method=6)
    print(f"fan tiles: {len(FAN)} -> {TILES.relative_to(SITE)}")


if __name__ == "__main__":
    main()
