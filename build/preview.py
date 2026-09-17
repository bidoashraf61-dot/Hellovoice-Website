#!/usr/bin/env python3
"""Bundle the five pages into one self-contained file for sharing.

Every asset becomes a data URI and internal links become hash routes, so the whole
site works from a single HTML file with no server.
"""

import base64
import mimetypes
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
OUT = ROOT / "build" / "preview.html"

PAGES = [("home", "index.html"), ("work", "work/index.html"),
         ("services", "services/index.html"), ("about", "about/index.html"),
         ("contact", "contact/index.html")]

_cache = {}


def uri(path: Path):
    key = str(path)
    if key in _cache:
        return _cache[key]
    if not path.exists():
        return ""
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    if path.suffix == ".webp":
        mime = "image/webp"
    if path.suffix == ".woff2":
        mime = "font/woff2"
    u = "data:" + mime + ";base64," + base64.b64encode(path.read_bytes()).decode()
    _cache[key] = u
    return u


def resolve(ref: str, page_dir: Path):
    ref = ref.split("?")[0].split("#")[0]
    if not ref or ref.startswith(("http", "data:", "mailto:", "tel:")):
        return None
    base = SITE if ref.startswith("/") else page_dir
    return (base / ref.lstrip("/")).resolve()


# ---------------------------------------------------------------- stylesheet
css = (SITE / "assets" / "theme.css").read_text()
for m in set(re.findall(r'url\("([^"]+\.woff2)"\)', css)):
    f = (SITE / "assets" / m.replace("../assets/", "")).resolve()
    css = css.replace('url("' + m + '")', "url(" + uri(f) + ")")

js = (SITE / "assets" / "site.js").read_text()
vendor = "\n".join((SITE / "assets" / "vendor" / n).read_text()
                   for n in ("lenis.min.js", "gsap.min.js", "ScrollTrigger.min.js"))

# ------------------------------------------------------------------- pages
sections = []
for key, rel in PAGES:
    p = SITE / rel
    h = p.read_text()
    d = p.parent

    body = re.search(r'<main id="main">(.*?)</main>', h, re.S).group(1)
    head = re.search(r'<header class="nav">(.*?)</header>', h, re.S).group(0)
    canvas = re.search(r'<div class="canvas" id="canvas">(.*?)</div>\n', h, re.S)
    foot = re.search(r'<footer class="foot">(.*?)</footer>', h, re.S).group(0)
    chunk = head + (canvas.group(0) if canvas else "") + \
        '<main id="main">' + body + "</main>" + foot

    for attrname in ("src", "srcset", "poster"):
        for m in list(re.finditer(attrname + r'="([^"]+)"', chunk)):
            val = m.group(1)
            small = val.replace("-1400.webp", "-700.webp")
            f = resolve(small, d) or resolve(val, d)
            if not (f and f.exists()):
                f = resolve(val, d)
            if f and f.exists() and f.suffix in (".webp", ".png", ".jpg", ".mp4"):
                chunk = chunk.replace(m.group(0), attrname + '="' + uri(f) + '"')

    def link(m):
        href = m.group(1)
        if href.startswith(("http", "mailto:", "tel:", "#", "data:")):
            return m.group(0)
        clean = href.split("?")[0].rstrip("/")
        for k, r in PAGES:
            target = r.replace("index.html", "").rstrip("/")
            if target and clean.endswith(target):
                return 'href="#' + k + '"'
        return 'href="#home"'
    chunk = re.sub(r'href="([^"]+)"', link, chunk)

    sections.append('<section class="route" id="' + key + '" hidden>' + chunk +
                    "</section>")

html = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>HelloVoice</title>
<script>document.documentElement.classList.add("js")</script>
<style>
""" + css + """
.route[hidden]{display:none}
.pv{position:fixed;left:50%;bottom:18px;transform:translateX(-50%);z-index:180;
  display:flex;gap:2px;background:rgba(11,10,10,.94);backdrop-filter:blur(10px);
  padding:5px;border-radius:999px;box-shadow:0 10px 34px rgba(0,0,0,.34)}
.pv a{font-family:var(--t);font-weight:600;font-size:13px;color:#F4F1EE9e;
  padding:10px 17px;border-radius:999px;white-space:nowrap;
  transition:background .2s,color .2s}
.pv a:hover{color:#fff}
.pv a.on{background:var(--red);color:#fff}
@media (max-width:560px){.pv a{padding:9px 12px;font-size:12px}}
</style>
</head>
<body>
""" + "".join(sections) + """
<nav class="pv" aria-label="Preview pages">
  <a href="#home">Home</a><a href="#work">Work</a><a href="#services">Services</a>
  <a href="#about">About</a><a href="#contact">Contact</a>
</nav>
<div class="lb" id="lb" role="dialog" aria-modal="true" aria-label="Video player">
  <div class="box"><button class="x" type="button">Close</button></div>
</div>
<script>""" + vendor + """</script>
<script>
(function () {
  var routes = ["home","work","services","about","contact"];
  function show(id) {
    if (routes.indexOf(id) < 0) id = "home";
    routes.forEach(function (r) {
      var el = document.getElementById(r); if (el) el.hidden = (r !== id);
    });
    document.querySelectorAll(".pv a").forEach(function (a) {
      a.classList.toggle("on", a.getAttribute("href") === "#" + id);
    });
    window.scrollTo(0, 0);
    if (window.ScrollTrigger) { ScrollTrigger.getAll().forEach(function(s){s.kill()}); }
    if (window.__hvInit) window.__hvInit();
  }
  addEventListener("hashchange", function () { show(location.hash.slice(1)); });
  show(location.hash.slice(1) || "home");
})();
</script>
<script>
window.__hvInit = function () {
""" + js + """
};
window.__hvInit();
</script>
</body>
</html>
"""

OUT.write_text(html)
print("preview.html  %.2f MB" % (OUT.stat().st_size / 1024 / 1024))
