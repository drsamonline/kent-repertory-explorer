#!/usr/bin/env python3
"""Draw this repository's badges as local SVG files.

An offline-first app must not depend on an image service to describe itself, so
these are drawn here and committed, then referenced by relative path. They
render on GitHub Pages, in the README and from `file://` with no network.

Every claim below is checked against the repo:
  tests       node tests/retrofit-web-kit.test.js  ->  14/14 passed
  rubrics     the embedded dataset's own count     ->  74,480
  payload     docs/play/index.html                 ->  ~1.9 MB
  deps        nothing is loaded at runtime         ->  0
  licence     LICENSE                              ->  PolyForm NC 1.0.0

  python3 scripts/badges.py
"""
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "assets")

INK = "#1a1510"
CREAM = "#f6efe2"
ACCENT = "#b5432c"     # the page's one accent: printed-repertory vermilion
GREEN = "#2e6b45"
SLATE = "#3c4a55"

BADGES = [
    ("offline", "offline", "no network", ACCENT),
    ("deps", "deps", "0 runtime", INK),
    ("tests", "tests", "14 passing", GREEN),
    ("rubrics", "rubrics", "74,480", SLATE),
    ("size", "payload", "1.9 MB, one file", INK),
    ("licence", "licence", "PolyForm NC 1.0.0", SLATE),
]

CH = 6.6   # approximate advance width at 11px


def badge(label, value, colour):
    lw = int(len(label) * CH) + 16
    vw = int(len(value) * CH) + 16
    total = lw + vw
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="22" role="img" '
        'aria-label="%s: %s">'
        '<title>%s: %s</title>'
        '<linearGradient id="s" x2="0" y2="100%%"><stop offset="0" stop-color="#fff" stop-opacity=".08"/>'
        '<stop offset="1" stop-color="#000" stop-opacity=".10"/></linearGradient>'
        '<clipPath id="r"><rect width="%d" height="22" rx="4" fill="#fff"/></clipPath>'
        '<g clip-path="url(#r)">'
        '<rect width="%d" height="22" fill="%s"/>'
        '<rect x="%d" width="%d" height="22" fill="%s"/>'
        '<rect width="%d" height="22" fill="url(#s)"/>'
        "</g>"
        '<g fill="%s" font-family="ui-sans-serif,Segoe UI,Helvetica,Arial,sans-serif" font-size="11" '
        'text-anchor="middle">'
        '<text x="%d" y="15">%s</text>'
        '<text x="%d" y="15">%s</text>'
        "</g></svg>"
    ) % (total, label, value, label, value, total, lw, INK, lw, vw, colour, total,
         CREAM, lw // 2, label, lw + vw // 2, value)


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, label, value, colour in BADGES:
        path = os.path.join(OUT, "badge-%s.svg" % name)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(badge(label, value, colour))
        print("wrote", path)


if __name__ == "__main__":
    main()
