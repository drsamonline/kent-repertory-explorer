# Kent's Repertory Explorer

An **offline, single-file** explorer for *Kent's Repertory of the Homoeopathic Materia Medica* (1897, public domain) — with Kent's own three-grade typography intact, a case builder, and grade-weighted repertorisation.

- **Live app:** https://drsamonline.github.io/kent-repertory-explorer/
- **No server, no backend, no account, no API calls.** Everything runs in the browser; nothing you type leaves the device.

## What's inside

| | |
|---|---|
| Rubrics | **74,667** |
| Graded remedy links | **735,500** |
| Remedies | **669** |
| Chapters | **41** |
| Grades | 1 → 465,287 · 2 → 198,591 · 3 → 71,582 |

Kent marked a remedy's strength by typeface: **bold = grade 3**, *italic = grade 2*, plain = grade 1. Those grades are preserved here, which is what makes repertorisation meaningful.

## Using it

1. Search in **repertory language** — `thirstless`, `anxiety night`, `weeping consolation`.
2. Prefer **narrow** rubrics; a rubric with 250 remedies tells you little, one with three is gold.
3. **Add** the rubrics that survive to your case.
4. Open **Analysis** to rank remedies by the sum of Kent's grades and rubrics covered.
5. Treat the ranking as a **shortlist to study in the materia medica** — the repertory narrows, the materia medica decides.

Keyboard: `/` search · `Enter` add highlighted · `↑` `↓` move · `Esc` close · `c` case · `a` analysis · `m` matrix.

## Downloads

The app is one self-contained HTML file — `app.html`. Save it and open it offline, or use the installers from [Releases](../../releases).

## Data

Derived from the open-source [OOReP](https://github.com/nondeterministic/oorep) repertory database (repertory token `publicum` = English Kent 1897). Kent's text is public domain; the extraction and the app are the author's.

`pipeline/extract.py` rebuilds `kent.json` from the OOReP SQL dump; `pipeline/build_app.py` embeds it (gzip + base64, decompressed client-side via `DecompressionStream`) into the single HTML file.

## Licence

Free to use for study and practice. Code © Dr Sohil Momin — commercial use requires a licence; educational institutes may use it free or at a discount. The repertory text is public domain.

## Disclaimer

A study and reference tool for practitioners and students. Not medical advice, and not a substitute for a qualified practitioner.
