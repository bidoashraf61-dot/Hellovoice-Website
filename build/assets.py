#!/usr/bin/env python3
"""Asset pipeline for the HelloVoice site."""

import base64
import io
import json
import re
import shutil
import unicodedata
import urllib.request
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
CAP = ROOT / "capture"
OUT = ROOT / "site" / "assets"
for s in ("brand", "clients", "work", "team", "fonts", "video"):
    (OUT / s).mkdir(parents=True, exist_ok=True)

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

# Where project thumbnails come from.
#   "site"  — the branded poster images used on the current hellovoice.co.uk
#   "vimeo" — the thumbnail selected on Vimeo for each film
POSTER_SOURCE = "site"


def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return re.sub(r"-{2,}", "-", s) or "item"


def webp(src, dest, w, q=76, alpha=False):
    im = Image.open(src)
    im = im.convert("RGBA" if alpha else "RGB")
    if im.width > w:
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    im.save(dest, "WEBP", quality=q, method=6)
    return dest.stat().st_size


report = {"work": [], "clients": [], "team": [], "notes": []}

# ------------------------------------------------------------------- fonts
FONTS = {"montserrat": "Montserrat:wght@700;800;900",
         "roboto": "Roboto:wght@400;500;700",
         "manrope": "Manrope:wght@500;600;700;800"}
for name, spec in FONTS.items():
    dest = OUT / "fonts" / f"{name}.woff2"
    if dest.exists():
        continue
    try:
        css = urllib.request.urlopen(urllib.request.Request(
            f"https://fonts.googleapis.com/css2?family={spec}&display=swap",
            headers=UA), timeout=40).read().decode()
        url = None
        for blk, body in re.findall(
                r"/\*\s*([a-z0-9-]+)\s*\*/\s*@font-face\s*\{(.*?)\}", css, re.S):
            if blk == "latin":
                m = re.search(r"url\((https://[^)]+\.woff2)\)", body)
                if m:
                    url = m.group(1)
                    break
        if url:
            dest.write_bytes(urllib.request.urlopen(
                urllib.request.Request(url, headers=UA), timeout=40).read())
    except Exception as e:
        report["notes"].append(f"font {name}: {e}")

# ------------------------------------------------------------------- brand
src = ROOT / "assets/brand/hellovoice-logo-full-transparent.png"
if src.exists():
    im = Image.open(src).convert("RGBA")
    for w, n in ((760, "logo.png"), (1520, "logo@2x.png")):
        c = im.copy(); c.thumbnail((w, w), Image.LANCZOS)
        c.save(OUT / "brand" / n, "PNG", optimize=True)
        c.save(OUT / "brand" / n.replace(".png", ".webp"), "WEBP",
               quality=90, method=6)
    # white knockout for dark grounds
    k = im.copy()
    px = k.load()
    for y in range(k.height):
        for x in range(k.width):
            r, g, b, a = px[x, y]
            if a > 8:
                px[x, y] = (255, 255, 255, a) if (r + g + b) < 380 else (r, g, b, a)
    k.thumbnail((760, 760), Image.LANCZOS)
    k.save(OUT / "brand" / "logo-knockout.png", "PNG", optimize=True)
    k.save(OUT / "brand" / "logo-knockout.webp", "WEBP", quality=90, method=6)
fav = ROOT / "assets/brand/hellovoice-favicon-source.png"
if fav.exists():
    f = Image.open(fav).convert("RGBA")
    for s in (32, 180, 512):
        g_ = f.copy(); g_.thumbnail((s, s), Image.LANCZOS)
        g_.save(OUT / "brand" / f"icon-{s}.png", "PNG", optimize=True)

# ------------------------------------------------------------------ video
v = ROOT / "build" / "reel.mp4"
if v.exists():
    shutil.copy(v, OUT / "video" / "reel.mp4")

# ---------------------------------------------------------------- clients
seen = {}
for folder in ("clients-fy26", "clients-fy25", "clients"):
    d = ROOT / "assets" / folder
    if not d.exists():
        continue
    names = {}
    man = d / "clients.json"
    if man.exists():
        for row in json.loads(man.read_text()):
            names[row["file"]] = row["company"]
    for f in sorted(d.glob("*.png")):
        k = slug(f.stem)
        if k in seen:
            continue
        try:
            webp(f, OUT / "clients" / f"{k}.webp", 400, 88, alpha=True)
            seen[k] = names.get(f.name, f.stem.replace("-", " ").title())
            report["clients"].append({"slug": k, "company": seen[k]})
        except Exception as e:
            report["notes"].append(f"client {f.name}: {e}")

# ------------------------------------------------------------------- work
import urllib.parse
content = json.loads((CAP / "content.json").read_text())
FR = CAP / "frames"
MEDIA = CAP / "media"


def poster_for(p):
    """Return (path, source) for a project's thumbnail, honouring POSTER_SOURCE
    and falling back to the other set when the preferred one is unavailable."""
    site = None
    if p.get("poster"):
        rel = urllib.parse.urlparse(p["poster"]).path.split("/wp-content/uploads/")[-1]
        f = MEDIA / rel
        if f.exists():
            site = f
    vid = p.get("vimeo_id")
    frame = FR / f"{vid}.jpg" if vid else None
    frame = frame if (frame and frame.exists()) else None

    order = (site, frame) if POSTER_SOURCE == "site" else (frame, site)
    names = ("site", "vimeo") if POSTER_SOURCE == "site" else ("vimeo", "site")
    for f, n in zip(order, names):
        if f:
            return f, n
    return None, None


for p in content["portfolio_projects"]:
    s = slug(p["title"])
    rec = {"slug": s, "title": p["title"], "vimeo": p.get("vimeo_id")}
    src, kind = poster_for(p)
    if src:
        try:
            webp(src, OUT / "work" / f"{s}-1400.webp", 1400, 76)
            webp(src, OUT / "work" / f"{s}-700.webp", 700, 74)
            rec["img"] = f"assets/work/{s}"
            rec["poster_source"] = kind
            with Image.open(src) as _im:
                rec["w"], rec["h"] = _im.width, _im.height
                rec["portrait"] = _im.height > _im.width * 1.1
        except Exception as e:
            report["notes"].append(f"work {s}: {e}")
    else:
        report["notes"].append(f"work {s}: no poster in either set")
    report["work"].append(rec)

# ------------------------------------------------------------------- team
td = ROOT / "assets/team"
if td.exists():
    for f in sorted(td.glob("*.png")):
        try:
            webp(f, OUT / "team" / f"{slug(f.stem)}.webp", 360, 84, alpha=True)
            report["team"].append(slug(f.stem))
        except Exception as e:
            report["notes"].append(f"team {f.name}: {e}")

(ROOT / "build" / "assets-report.json").write_text(
    json.dumps(report, indent=2, ensure_ascii=False))

tot = sum(f.stat().st_size for f in OUT.rglob("*") if f.is_file())
print(f"fonts   : {len(list((OUT/'fonts').glob('*.woff2')))}")
print(f"clients : {len(report['clients'])}")
_site = sum(1 for r in report["work"] if r.get("poster_source") == "site")
_vim = sum(1 for r in report["work"] if r.get("poster_source") == "vimeo")
print(f"work    : {sum(1 for r in report['work'] if 'img' in r)}/{len(report['work'])}"
      f"  (site posters {_site}, vimeo frames {_vim})")
print(f"team    : {len(report['team'])}")
print(f"video   : {(OUT/'video'/'reel.mp4').stat().st_size/1024/1024:.2f} MB")
print(f"TOTAL   : {tot/1024/1024:.2f} MB")
for n in report["notes"][:6]:
    print("  !", n)
