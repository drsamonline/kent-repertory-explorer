# Repertorium Publicum Explorer

An **offline, single-file** repertory explorer for **Repertorium Publicum** (2008) — an open,
**Kent-derived** repertory — with the printed three-grade system intact, a case builder, and
grade-weighted repertorisation.

**[Open the repertory →](https://drsamonline.github.io/kent-repertory-explorer/)** · no server,
no backend, no account, no API calls. Everything runs in the browser; nothing you type leaves the device.

---

## What it is, precisely

The data is **Repertorium Publicum** by **Vladimir Polony (2008)**, published as part of the
[OpenRep](https://github.com/nondeterministic/oorep) source code and licensed **GPL v3**.

It is **not** Kent's *Repertory of the Homoeopathic Materia Medica*, 1897 first edition. It has its
own chapter structure — separate *Clinical*, *Appetite*, *Blood* and *Heart & Circulation* chapters,
which Kent does not have — and its own additions. Earlier releases of this app described it as Kent
1897; that was wrong, and it has been corrected throughout.

## What's inside

| | |
|---|---|
| Rubrics | **74,480** |
| Graded remedy links | **735,460** |
| Remedies | **669** |
| Chapters | **41** |

Every link carries a grade, taken from the typography of the printed repertory:

| grade | meaning | links |
|---|---|---|
| **3** | strongest association | 71,582 |
| *2* | moderate | 198,591 |
| 1 | least | 465,287 |

## Features

- **Search in repertory language** — `anxiety night`, `thirstless`, `weeping consolation`. Results
  are ranked **narrowest first**, because the rubrics with three remedies are the ones that narrow a case.
- **Chapter browse** across all 41 chapters, with rubric counts.
- **Filters** — narrow-only with an adjustable threshold, sort by narrowest / broadest / A–Z / chapter.
- **Case builder** — add rubrics, attach a note to each, remove or clear.
- **Analysis** — remedies ranked by the sum of grades and rubrics covered; minimum-grade filter;
  "cover all rubrics"; exclude a remedy (it stays visible, struck through, and can be brought back).
- **Matrix** — remedy × rubric grid showing each grade.
- **Export** — plain text, CSV, JSON, copy to clipboard, and a clean print/PDF sheet.
- **Themes** — dark, light, high-contrast. **Keyboard-first** with `/`, `↑ ↓`, `Enter`, `c`, `a`, `m`, `t`, `Esc`.
- **Offline-first** — one self-contained HTML file, PWA manifest and a network-first service worker.
- **Case persists** in local storage; notes included.

## Using it

1. Search in **repertory language** — not the patient's words.
2. Prefer **narrow** rubrics; a rubric with 250 remedies tells you little, one with three is gold.
3. **Add** the rubrics that survive to your case.
4. Open **Analysis** to rank remedies across them.
5. Treat the ranking as a **shortlist to study in the materia medica** — the repertory narrows, the materia medica decides.

## Files

```
app.html                     the whole application (one self-contained file)
index.html                   landing page
docs/                        the same site, for a Pages source pointed at /docs
pipeline/extract.py          rebuilds kent.json from the OOReP database dump
pipeline/build_app.py        embeds the data (gzip + base64) into app.html
pipeline/app_template.html   the application source
```

`app.html` is built by `build_app.py`, which injects the repertory — gzipped and base64-encoded —
into the template. The browser decompresses it with `DecompressionStream`. The payload is ~1.9 MB.

## Data

Extracted from the OOReP PostgreSQL dump (repertory token `publicum`). The structured, graded JSON is
also published in
[`homoeopathic-materia-medica-repertory-json`](https://github.com/drsamonline/homoeopathic-materia-medica-repertory-json)
under `repertory/repertorium-publicum-2008/`.

## Licence

**GNU GPL v3** for the whole work. The app embeds the *Repertorium Publicum* dataset, which is
third-party material published under GPL v3, so the combined work is distributed under GPL v3.
GPL v3 permits commercial use; it requires that derivative works stay under GPL v3 and that the
source is made available.

- [`LICENSE`](LICENSE) · [`LICENSE-GPL-3.0.txt`](LICENSE-GPL-3.0.txt)
- Embedded data: Repertorium Publicum (2008), Vladimir Polony — GPL v3, part of the OpenRep source code.

Requests, not conditions: please credit Dr Sohil Momin and the source of the data.

## Disclaimer

A study and reference tool for practitioners and students. Not medical advice, and not a substitute
for the judgement of a qualified practitioner.
