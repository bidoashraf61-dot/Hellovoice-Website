"""Key the flat white ground out of the HelloVoice logo animation.

A global colour key cannot be used: "Hello" is knocked out *white* inside the
red bubble, so keying on whiteness punches holes through the logotype. Instead
the background is found by flooding inward from the four corners — the ground is
one connected region, the letter interiors are enclosed by red and are never
reached.

The edge is then softened with the pixel's own distance from white, so the
source's antialiasing survives as partial alpha instead of a hard 1px stair.
"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

KEY = (255, 0, 255)      # sentinel the flood writes into the background
THRESH = 12              # how far from the seed colour the flood may wander

def cut(path_in, path_out):
    im = Image.open(path_in).convert("RGB")
    w, h = im.size
    probe = im.copy()
    for seed in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)):
        if probe.getpixel(seed) != KEY:
            ImageDraw.floodfill(probe, seed, KEY, thresh=THRESH)

    rgb = np.asarray(im, dtype=np.uint8)
    bg = (np.asarray(probe, dtype=np.uint8) == np.array(KEY, np.uint8)).all(axis=2)

    # distance from white, normalised so the logo's own solid red reads as fully
    # opaque rather than the 0.89 a naive 1-min/255 would give it
    soft = np.clip((255.0 - rgb.min(axis=2)) / 200.0, 0.0, 1.0)

    a = np.where(bg, 0.0, 1.0)
    # only the boundary ring takes the soft value; interiors stay solid
    ring = (~bg) & (soft < 1.0)
    a[ring] = soft[ring]

    out = np.dstack([rgb, (a * 255).astype(np.uint8)])
    img = Image.fromarray(out, "RGBA")
    # a half-pixel feather kills the residual stair without eating the mark
    alpha = img.getchannel("A").filter(ImageFilter.GaussianBlur(0.6))
    img.putalpha(alpha)
    img.save(path_out)




# --- driver -----------------------------------------------------------------
#
# Run from the repo root, with ffmpeg on PATH:
#
#   python3 build/alpha_logo.py "Client Logos/Blue logos/Main_Animation_logo.mp4" \
#           site/assets/brand/helv-logo-alpha
#
# Writes <stem>.webm (VP9 + alpha) and <stem>.webp (final frame, transparent).
#
# Two encoder flags are load-bearing and easy to lose:
#   -pix_fmt yuva420p   without it libvpx-vp9 silently drops the alpha plane
#   -auto-alt-ref 0     alt-ref frames and alpha do not coexist in libvpx
# Keying inside an ffmpeg filter chain does NOT work here: the format is
# flattened before it reaches the encoder and the result is 100% opaque. The
# frames have to carry real alpha on the way in, which is why this goes via
# RGBA PNGs.

import glob
import shutil
import subprocess
import tempfile
from multiprocessing import Pool

WIDTH, HEIGHT = 1280, 720
# the source settles into a static hold well before its 185th frame; trimming
# the tail keeps the loop tight instead of parking on a still logo
FRAMES = 152
CRF = 40


def _job(pair):
    cut(*pair)
    return 1


def build(src, out_stem):
    tmp = tempfile.mkdtemp(prefix="helv-alpha-")
    try:
        raw, keyed = tmp + "/raw", tmp + "/keyed"
        os.makedirs(raw); os.makedirs(keyed)
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-i", src,
             "-vf", f"scale={WIDTH}:{HEIGHT}", "-frames:v", str(FRAMES),
             raw + "/%04d.png"], check=True)

        fs = sorted(glob.glob(raw + "/*.png"))
        with Pool() as p:
            p.map(_job, [(f, keyed + "/" + os.path.basename(f)) for f in fs])

        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-framerate", "30000/1001",
             "-i", keyed + "/%04d.png",
             "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-auto-alt-ref", "0",
             "-b:v", "0", "-crf", str(CRF), "-row-mt", "1", "-deadline", "good",
             "-cpu-used", "2", "-an", "-metadata:s:v:0", "alpha_mode=1",
             out_stem + ".webm"], check=True)

        Image.open(fs[-1].replace(raw, keyed)).save(
            out_stem + ".webp", "WEBP", quality=90, method=6)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2])
