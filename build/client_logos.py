#!/usr/bin/env python3
"""Turn the client's `Client Logos/` artboards into web assets.

The source files are 63 PNG artboards named "Artboard N" — no brand names, a
lot of surrounding whitespace, and wildly different ink heights. Three things
have to happen before they can sit in a row together:

  * trim to the actual ink, or the padding baked into each artboard decides the
    spacing and the row looks arbitrary;
  * normalise by *optical* height rather than box height — a wordmark and a
    roundel with the same bounding box do not read as the same size;
  * emit 1x/2x webp on transparency so one file works on both the white
    marquee and the black wall.

NAMES is a hand-read map from artboard number to brand, taken off a contact
sheet. Where a mark could not be read with confidence the entry is None and the
logo still ships — it just gets a neutral alt rather than a guessed one.
"""
import pathlib
import re
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "Client Logos"
OUT = ROOT / "site" / "assets" / "clients"

NAMES = {
    1: "Enbrel", 2: None, 3: "Tabuk Pharmaceuticals", 4: "Pristiq",
    5: "Biotech Cigalah", 6: "Elsewedy Electric", 7: "Ego", 8: "Xeljanz",
    9: "NewEast", 10: "Qasser Al Saraya", 11: "Champix", 12: "CeraVe",
    13: "Mondelez International", 14: "JeddaDerm", 15: "Aisin",
    16: "Jamjoom Pharma", 17: "SkinCeuticals", 18: "IBSA", 19: "Litfulo",
    20: "La Roche-Posay", 21: "Zinforo", 22: "Isuzu", 23: "Qasser Al Saraya",
    24: "Merck", 25: "Molnlycke", 26: "Pfizer", 27: "Paxlovid",
    28: "L'Oreal Dermatological Beauty", 29: "Sanofi", 30: "Nurtec ODT",
    31: "MSD", 32: "Menarini Group", 33: "AstraZeneca", 34: None,
    35: "Xeljanz", 36: "Vyndamax", 37: "Vichy", 38: "Orchidia",
    39: "Tabuk Pharmaceuticals", 40: "Apex Pharma", 41: "SPC", 42: "Oxbryta",
    43: "Abbott", 44: "Automechanika Dubai", 45: "Alnaghi", 46: "Nahdi",
    47: "QV Face", 48: "Skintellectual Solutions", 49: "Bayer", 50: "Quadri",
    51: "Filorga", 52: "Hikma", 53: "Disc Derma", 54: "Bionnex", 55: "Whites",
    56: "Zoetis", 57: "Dr Sulaiman Al Habib", 58: "Alpha Plus", 59: "SVR",
    60: "QV Face", 61: "Uriage", 62: "Genpharm", 63: None,
}

# Marks that read at their full box height (roundels, stacked lockups) against
# ones that are a single line of type. Without this a wordmark is set to the
# same height as a circle and dwarfs it.
TARGET_H = 64          # optical height, in px, at 1x


# Logos that arrived as named files rather than as numbered artboards. The
# client sends these one at a time, so they cannot be folded into NAMES without
# renumbering somebody else's artboard.
#
# Each entry is (filename, brand, crop) where crop is an optional box applied
# before trimming — some of these are screenshots off a supplier's site rather
# than supplied artwork, and carry a watermark that trim() would otherwise keep
# because it is ink like any other.
EXTRA = [
    ("unnamed.png", "Care Outlet", None),
    # 800x800 on a near-white ground (248,250,247) with a site watermark in the
    # bottom-right. Cropped to the upper 78% so the mark is gone before trim
    # measures the ink.
    ("فروع-مخازن-العناية-بالسعودية-الموقع-و-ارقام-التواصلرر.jpeg",
     "Makhazen Alenayah", (0, 0, 800, 624)),
]

# Sources kept outside Client Logos — the FY26 set the roster was built from.
EXTRA_DIRS = [ROOT / "assets" / "clients-fy26", ROOT]
EXTRA_FROM_DIRS = [("parkville.png", "Parkville", None),
                   ("Novo_Nordisk_-_Logo.svg.webp", "Novo Nordisk", None)]


def slug(name, n):
    if not name:
        return f"client-{n:02d}"
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def trim(im):
    """Crop to the ink, ignoring near-white and fully transparent pixels."""
    rgba = im.convert("RGBA")
    a = rgba.split()[-1]
    if a.getextrema()[0] < 255:            # has real transparency
        box = a.getbbox()
    else:                                   # opaque artboard on white
        # 246, not 244: one of the named sources sits on a (248,250,247)
        # ground rather than pure white, and at 244 the whole plate counted as
        # ink so the trim did nothing.
        g = rgba.convert("L").point(lambda v: 0 if v > 246 else 255)
        box = g.getbbox()
    return rgba.crop(box) if box else rgba


def main():
    # Rebuilt from scratch every run: the client's instruction is that these 63
    # files are the client list, so anything left from an earlier pipeline must
    # not survive alongside them.
    if OUT.exists():
        for old in OUT.glob("*.webp"):
            old.unlink()
    OUT.mkdir(parents=True, exist_ok=True)
    files = sorted(SRC.glob("*.png"),
                   key=lambda p: int(re.sub(r"\D", "", p.stem) or 0))
    made = []
    for p in files:
        n = int(re.sub(r"\D", "", p.stem) or 0)
        name = NAMES.get(n)
        s = slug(name, n)
        im = trim(Image.open(p))
        # Scale purely by height. An earlier version capped the width at 460
        # and let the height fall out of it, which quietly shrank wide lockups
        # to 32px of real pixels — then CSS scaled them back up to the row
        # height and they were visibly soft. Width is a layout problem and
        # belongs in CSS (max-width on the cell), not in the asset.
        h = TARGET_H * 2                    # author at 2x, downscale for 1x
        w = round(im.width * h / im.height)
        big = im.resize((w, h), Image.LANCZOS)
        big.save(OUT / f"{s}@2x.webp", "WEBP", quality=92, method=6)
        big.resize((max(1, w // 2), max(1, h // 2)), Image.LANCZOS).save(
            OUT / f"{s}.webp", "WEBP", quality=92, method=6)
        made.append((s, name or "Client", w // 2, h // 2))
    # the named extras, through the same trim-and-scale so they sit correctly
    # in a row beside the artboards rather than at whatever size they arrived
    for fname, brand, crop in EXTRA:
        src = SRC / fname
        if not src.exists():
            print(f"  ! missing extra logo: {fname}")
            continue
        im = Image.open(src)
        if crop:
            im = im.convert("RGBA").crop(crop)
        im = trim(im)
        s2 = slug(brand, 0)
        h = TARGET_H * 2
        w = round(im.width * h / im.height)
        big = im.resize((w, h), Image.LANCZOS)
        big.save(OUT / f"{s2}@2x.webp", "WEBP", quality=92, method=6)
        big.resize((max(1, w // 2), max(1, h // 2)), Image.LANCZOS).save(
            OUT / f"{s2}.webp", "WEBP", quality=92, method=6)
        made.append((s2, brand, w // 2, h // 2))

    for fname, brand, crop in EXTRA_FROM_DIRS:
        for d in EXTRA_DIRS:
            src = d / fname
            if not src.exists():
                continue
            im = Image.open(src)
            if crop:
                im = im.convert("RGBA").crop(crop)
            im = trim(im)
            s2 = slug(brand, 0)
            h = TARGET_H * 2
            w = round(im.width * h / im.height)
            big = im.resize((w, h), Image.LANCZOS)
            big.save(OUT / f"{s2}@2x.webp", "WEBP", quality=92, method=6)
            big.resize((max(1, w // 2), max(1, h // 2)), Image.LANCZOS).save(
                OUT / f"{s2}.webp", "WEBP", quality=92, method=6)
            made.append((s2, brand, w // 2, h // 2))
            break
        else:
            print(f"  ! missing extra logo: {fname}")

    print(f"{len(made)} logos -> site/assets/clients")
    return made


if __name__ == "__main__":
    main()
