# Repertorium Publicum Explorer

An **offline, single-file** explorer for **Repertorium Publicum** (2008) — an open,
**Kent-derived** repertory — with the three grades intact, a case builder, and
grade-weighted repertorisation.

- **Live app:** https://drsamonline.github.io/kent-repertory-explorer/
- **No server, no backend, no account, no API calls.** Everything runs in the browser; nothing you type leaves the device.

> **What this is, exactly.** The data is *Repertorium Publicum* by **Vladimir Polony
> (2008)**, published as part of the [OpenRep](https://github.com/nondeterministic/oorep)
> source code and licensed **GPL v3**. It is **not** Kent's 1897 first edition: it has
> its own chapter structure (separate *Clinical*, *Appetite*, *Blood* and
> *Heart & Circulation* chapters) and its own additions. Earlier releases of this app
> described it as Kent 1897 — that was wrong, and the labelling has been corrected.

## What's inside

| | |
|---|---|
| Rubrics | **74,480** |
| Graded remedy links | **735,460** |
| Remedies | **669** |
| Chapters | **41** |
| Grades | 1 → 465,287 · 2 → 198,591 · 3 → 71,582 |

## Using it

1. Search in **repertory language** — `thirstless`, `anxiety night`, `weeping consolation`.
2. Prefer **narrow** rubrics; a rubric with 250 remedies tells you little, one with three is gold.
3. **Add** the rubrics that survive to your case.
4. Open **Analysis** to rank remedies by the sum of grades and rubrics covered.
5. Treat the ranking as a **shortlist to study in the materia medica** — the repertory narrows, the materia medica decides.

Keyboard: `/` search · `Enter` add highlighted · `↑` `↓` move · `Esc` close · `c` case · `a` analysis · `m` matrix.

## Downloads

The app is one self-contained HTML file — `app.html`. Save it and open it offline.

## Data

Extracted from the OOReP database dump (repertory token `publicum`).
`pipeline/extract.py` rebuilds `kent.json`; `pipeline/build_app.py` embeds it
(gzip + base64, decompressed client-side via `DecompressionStream`) into the single
HTML file.

The structured, graded JSON is also published in
[`homoeopathic-materia-medica-repertory-json`](https://github.com/drsamonline/homoeopathic-materia-medica-repertory-json)
under `repertory/repertorium-publicum-2008/`.

## Licence

- **App code** © Dr Sohil Momin. Free for study and practice; commercial use requires a licence; educational institutes free or at a discount.
- **Repertory data**: **GPL v3** (Repertorium Publicum, 2008, part of the OpenRep source code) — not public domain.

## Disclaimer

A study and reference tool for practitioners and students. Not medical advice, and not a substitute for a qualified practitioner.
