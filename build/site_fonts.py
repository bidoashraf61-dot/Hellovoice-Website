#!/usr/bin/env python3
"""WOFF2 cuts of the two brand faces the site sets in, from the files it ships.

The reference stylesheet loads DM Sans (variable, opsz + wght) and Bebas Neue
as TTF: 233KB and 56KB on every page. These are the same fonts — every axis
kept, layout features kept — subset to the characters the built site actually
uses plus Latin-1, general punctuation and arrows, and saved as WOFF2.

build_css() points @font-face at these when they exist. Rerun after adding
copy in a new script or with new symbols:  python3 build/site_fonts.py
"""
import glob, html, re
from pathlib import Path
from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
FACES = [("68f262b1b60fe57e398c9c09_DMSans-VariableFont_opsz,wght.ttf", "dm-sans-site.woff2"),
         ("68efdbc172d0ac625d40c65f_BebasNeue-Regular.ttf", "bebas-neue-site.woff2")]

text = ""
for p in glob.glob(str(SITE / "**" / "*.html"), recursive=True):
    if "-test" in p:
        continue
    s = Path(p).read_text(encoding="utf-8")
    s = re.sub(r"<script.*?</script>|<style.*?</style>", "", s, flags=re.S)
    text += html.unescape(re.sub(r"<[^>]+>", " ", s))
cps = {ord(c) for c in text if ord(c) >= 32}
cps |= set(range(0x20, 0x7F)) | set(range(0xA0, 0x100))
cps |= {0x2013, 0x2014, 0x2018, 0x2019, 0x201C, 0x201D, 0x2022, 0x2026, 0x2032,
        0x2190, 0x2191, 0x2192, 0x2193, 0x2197, 0x00D7, 0x20AC, 0x2122}

out_dir = SITE / "assets" / "fonts"
for src, dst in FACES:
    font = TTFont(SITE / "assets" / "ref" / src)
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["*"]
    opts.name_IDs = ["*"]
    opts.hinting = False
    opts.notdef_outline = True
    sub = subset.Subsetter(opts)
    sub.populate(unicodes=cps)
    sub.subset(font)
    font.flavor = "woff2"
    font.save(out_dir / dst)
    kept = TTFont(out_dir / dst)
    axes = [a.axisTag for a in kept["fvar"].axes] if "fvar" in kept else "static"
    print(f"{dst:24} {(out_dir / dst).stat().st_size/1024:6.1f}KB  axes {axes}  "
          f"missing {''.join(sorted(chr(c) for c in cps if c > 32 and c not in kept.getBestCmap() and chr(c).strip()))[:40]!r}")
