#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Dr Sohil Momin
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Pack the PNG icons into one Windows .ico, so the released EXE carries the app
icon instead of the default blank page.

A PNG-compressed ICO is just a header, one directory entry per image, then the
PNG bytes. No dependency needed.

  python3 scripts/ico.py     # docs/assets/icon.ico
"""
import os
import struct

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(HERE, "docs", "assets")
SIZES = [256, 64, 48, 32, 16]


def main():
    images = []
    for s in SIZES:
        p = os.path.join(ASSETS, "icon-%d.png" % s)
        with open(p, "rb") as fh:
            images.append((s, fh.read()))

    header = struct.pack("<HHH", 0, 1, len(images))       # reserved, type=icon, count
    offset = 6 + 16 * len(images)
    entries, blobs = b"", b""
    for s, data in images:
        dim = 0 if s >= 256 else s                        # 0 means 256 in the ICO spec
        entries += struct.pack("<BBBBHHII", dim, dim, 0, 0, 1, 32, len(data), offset)
        blobs += data
        offset += len(data)

    out = os.path.join(ASSETS, "icon.ico")
    with open(out, "wb") as fh:
        fh.write(header + entries + blobs)
    print("wrote %s (%d bytes, %s)" % (out, os.path.getsize(out), ", ".join("%dpx" % s for s in SIZES)))


if __name__ == "__main__":
    main()
