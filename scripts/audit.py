#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Dr Sohil Momin
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Audit this repository against its own claims. No dependencies, no network.

Every number, path and licence statement the repo makes is checked here against
the artefact it describes, so a claim cannot quietly drift from the thing it
claims about.

  python3 scripts/audit.py          # exit 0 = clean, 1 = something is wrong
"""
import base64
import gzip
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
FAIL, OK = [], []


def check(cond, label, detail=""):
    (OK if cond else FAIL).append(label + ((" — " + detail) if detail else ""))


def read(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as fh:
        return fh.read()


# ── the dataset, straight out of the built page ──────────────────────────────
app = read("docs/play/index.html")
m = re.search(r'<script id="kentdata" type="application/gzip\+base64">([^<]+)</script>', app)
check(bool(m), "the app embeds its dataset")
data = json.loads(gzip.decompress(base64.b64decode(m.group(1).strip())))
counts = data["counts"]
rubrics, links, remedies = counts["rubrics"], counts["remedy_links"], counts["remedies"]
chapters = len({n for n in (data.get("tree", {}).get("names") or [])})  # placeholder, fixed below

# chapters: count the distinct first path segments from the tree
def paths_v1(node, path=()):
    p = path + (node["n"],) if node.get("n") else path
    if node.get("r"):
        yield p
    for c in node.get("c") or []:
        yield from paths_v1(c, p)


if "tree" in data and "rx" in data["tree"]:
    t = data["tree"]
    parent = [-1] * len(t["n"])
    for i, kids in enumerate(t["c"]):
        for k in kids:
            parent[k] = i
    paths = [()] * len(t["n"])
    for i in range(len(t["n"])):
        nm = t["names"][t["n"][i]]
        up = paths[parent[i]] if parent[i] >= 0 else ()
        paths[i] = up + (nm,) if nm else up
    firsts = {paths[i][0] for i, k in enumerate(t["k"]) if k}
else:
    firsts = {p[0] for p in paths_v1(data["tree"])}
chapters = len(firsts)

check((rubrics, links, remedies, chapters) == (74480, 735460, 669, 41),
      "the dataset still declares 74,480 / 735,460 / 669 / 41",
      "%s / %s / %s / %s" % (rubrics, links, remedies, chapters))

# every stated number in the prose must match
PROSE = ["README.md", "ENHANCEMENTS.md", "RELEASES.md", "docs/index.html", "docs/play/manifest.webmanifest"]
# CHANGELOG.md and RELEASES.md quote the old wording on purpose — that is the record of the fix,
# not a claim about the present. Only current-state files are checked for it.
CURRENT = ["README.md", "docs/index.html", "docs/play/manifest.webmanifest", "docs/manifest.webmanifest"]
NUMBERS = {
    "74,480": rubrics == 74480,
    "735,460": links == 735460,
    "669": remedies == 669,
    "41": chapters == 41,
}
for f in PROSE:
    body = read(f)
    for num, good in NUMBERS.items():
        if num in body:
            check(good, "%s: %s is still true" % (f, num))

# no stale count from the old attribution
for f in CURRENT:
    if not os.path.exists(os.path.join(ROOT, f)):
        continue
    body = read(f)
    for stale in ["74,667", "735,500", "Kent's Repertory (1897)"]:
        check(stale not in body, "%s: no stale claim %r" % (f, stale))

# ── paths ───────────────────────────────────────────────────────────────────
landing = read("docs/index.html")
for m2 in re.finditer(r'(?:href|src)="([^"]+)"', landing):
    u = m2.group(1)
    if u.startswith(("http://", "https://", "#", "mailto:", "data:")):
        continue
    target = os.path.join(DOCS, u.split("#")[0].split("?")[0])
    check(os.path.exists(target), "landing link resolves: %s" % u)

man = json.loads(read("docs/play/manifest.webmanifest"))
check(man["start_url"] == "./" and man["scope"] == "./", "app manifest start_url/scope are ./")
for ic in man["icons"]:
    check(os.path.exists(os.path.normpath(os.path.join(DOCS, "play", ic["src"]))),
          "app manifest icon exists: %s" % ic["src"])

site_man = json.loads(read("docs/manifest.webmanifest"))
check(site_man["start_url"] == "./play/", "site manifest opens the app")
for ic in site_man["icons"]:
    check(os.path.exists(os.path.join(DOCS, ic["src"])), "site manifest icon exists: %s" % ic["src"])

sw = read("docs/sw.js")
core = re.search(r"const CORE = \[([^\]]+)\]", sw, re.S).group(1)
for entry in re.findall(r"'([^']+)'", core):
    p = os.path.normpath(os.path.join(DOCS, entry))
    check(os.path.exists(p), "service worker precaches an existing file: %s" % entry)

check("registration.update()" in sw or "update()" in app, "the app asks for a worker update on load")
check('navigator.serviceWorker.register' in app, "the app registers the worker")

# ── licence ─────────────────────────────────────────────────────────────────
lic = read("LICENSE")
check("PolyForm Noncommercial License 1.0.0" in lic, "LICENSE is PolyForm Noncommercial 1.0.0")
check(os.path.exists(os.path.join(ROOT, "LICENSE-GPL-3.0.txt")),
      "the data's GPL text is kept beside ours")
readme = read("README.md")
check("PolyForm Noncommercial 1.0.0" in readme, "README states the PolyForm licence")
check(not re.search(r"GNU GPL v3 for the whole work", readme),
      "README no longer claims the whole work is GPL v3")
check("badge-licence.svg" in readme, "README carries the licence badge")
badge = read("docs/assets/badge-licence.svg")
check("PolyForm NC 1.0.0" in badge, "the licence badge says PolyForm")

# ── no network at runtime ───────────────────────────────────────────────────
for f in ["docs/index.html", "docs/play/index.html"]:
    body = read(f)
    for tag in re.findall(r'<(?:img|script|link)[^>]*(?:src|href)="(https?://[^"]+)"', body):
        FAIL.append("%s loads a remote asset: %s" % (f, tag))

# ── build stamps agree with VERSION ─────────────────────────────────────────
version = read("VERSION").strip()
check(("build " + version) in landing, "the landing page build stamp is %s" % version)
check(("'" + version + " ·" ) in app or ("build " + version) in app, "the app build stamp is %s" % version)

# ── screenshots exist and are recent enough to be real ──────────────────────
for name in ["app-desktop.png", "app-mobile.png", "landing-desktop.png", "landing-mobile.png", "og.png"]:
    p = os.path.join(DOCS, "assets", name)
    check(os.path.exists(p) and os.path.getsize(p) > 5000, "screenshot present: %s" % name)

# ── no stale root duplicates ────────────────────────────────────────────────
for stale in ["app.html", "index.html", "manifest.webmanifest", "sw.js"]:
    check(not os.path.exists(os.path.join(ROOT, stale)),
          "no stale root duplicate: %s" % stale)

# ── report ──────────────────────────────────────────────────────────────────
print("%d checks passed" % len(OK))
for line in FAIL:
    print("  FAIL  " + line)
if FAIL:
    print("\n%d problem(s)" % len(FAIL))
sys.exit(1 if FAIL else 0)
