#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Dr Sohil Momin
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Re-encode the embedded repertory from the tree form (v1) to the columnar form (v2).

The app carries its whole dataset inside the page, gzipped and base64'd. The v1
shape repeats a key name on every one of ~98,000 nodes and stores each rubric's
links in its own quoted string; v2 stores the same information as parallel
arrays with one concatenated link blob, which gzips ~20% smaller and parses
faster.

Nothing about the content changes: the script re-reads the payload out of a
built file, converts it, and verifies the conversion before writing anything.

  python3 pipeline/recompress.py docs/play/index.html
  python3 pipeline/recompress.py docs/play/index.html app.html

The app's loader handles both shapes, so a build from pipeline/app_template.html
with the original kent.json still works.
"""
import base64
import gzip
import json
import os
import re
import sys

B36 = "0123456789abcdefghijklmnopqrstuvwxyz"
TAG = re.compile(r'(<script id="kentdata" type="application/gzip\+base64">)([^<]+)(</script>)')


def b36(v, width):
    out = ""
    for _ in range(width):
        out = B36[v % 36] + out
        v //= 36
    return out


def to_v2(d):
    names, nidx = [], {}
    name_of, children, counts, links = [], [], [], []

    def add(node):
        i = len(name_of)
        nm = node.get("n", "")
        if nm not in nidx:
            nidx[nm] = len(names)
            names.append(nm)
        name_of.append(nidx[nm])
        children.append([])
        counts.append(node.get("k", 0))
        links.append(node.get("r", ""))
        for ch in node.get("c") or []:
            children[i].append(add(ch))
        return i

    add(d["tree"])

    rx, gr = [], []
    for s in links:
        for i in range(0, len(s), 3):
            v = int(s[i:i + 3], 36)
            rx.append(b36(v >> 2, 2))
            gr.append(str(v & 3))

    # the arrays stay under "tree": the app calls flatten(d.tree), and keeping the
    # key means the loader needs no change beyond understanding the new shape.
    return {
        "v": 2,
        "book": d.get("book"),
        "remedies": d["remedies"],
        "counts": d["counts"],
        "tree": {
            "names": names,
            "n": name_of,
            "c": children,
            "k": counts,
            "rx": "".join(rx),
            "gr": "".join(gr),
        },
    }


def decode_v2(d):
    """Rebuild the v1-shaped list of (path, links) so the two can be compared."""
    t = d["tree"]
    names, n, c, k, rx, gr = t["names"], t["n"], t["c"], t["k"], t["rx"], t["gr"]
    parent = [-1] * len(n)
    for i in range(len(n)):
        for ch in c[i]:
            parent[ch] = i
    paths = [None] * len(n)
    for i in range(len(n)):
        nm = names[n[i]]
        up = paths[parent[i]] if parent[i] >= 0 else []
        paths[i] = up + [nm] if nm else list(up)
    out, off = [], 0
    for i in range(len(n)):
        if k[i]:
            links = []
            for j in range(k[i]):
                o = off + j
                links.append((int(rx[o * 2:o * 2 + 2], 36), int(gr[o])))
            out.append((tuple(paths[i]), tuple(links)))
            off += k[i]
    return out


def decode_v1(d):
    out = []

    def walk(node, path):
        p = path + [node["n"]] if node.get("n") else path
        if node.get("r"):
            links = []
            s = node["r"]
            for i in range(0, len(s), 3):
                v = int(s[i:i + 3], 36)
                links.append((v >> 2, v & 3))
            out.append((tuple(p), tuple(links)))
        for ch in node.get("c") or []:
            walk(ch, p)

    walk(d["tree"], [])
    return out


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    for path in sys.argv[1:]:
        html = open(path, encoding="utf-8").read()
        m = TAG.search(html)
        if not m:
            print("!! no kentdata block in %s" % path)
            sys.exit(1)

        old_gz = base64.b64decode(m.group(2).strip())
        d = json.loads(gzip.decompress(old_gz))
        if d.get("v") == 2:
            print("%-28s already v2, skipped" % path)
            continue

        before = decode_v1(d)
        v2 = to_v2(d)
        after = decode_v2(v2)
        if before != after:
            print("!! %s: v1 and v2 decode differently — not writing" % path)
            sys.exit(1)

        payload = json.dumps(v2, separators=(",", ":")).encode()
        new_gz = gzip.compress(payload, 9)
        new_b64 = base64.b64encode(new_gz).decode()

        html = html[:m.start(2)] + new_b64 + html[m.end(2):]
        open(path, "w", encoding="utf-8").write(html)

        print("%-28s %d rubrics identical · gz %d -> %d (%.1f%%) · base64 %d -> %d · file %d -> %d"
              % (path, len(after), len(old_gz), len(new_gz),
                 100 * (1 - len(new_gz) / len(old_gz)),
                 len(m.group(2).strip()), len(new_b64), len(m.string), len(html)))


if __name__ == "__main__":
    main()
