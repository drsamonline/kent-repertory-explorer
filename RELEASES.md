# Releases

Every release carries two things besides the download: **an icon for the artifact** (so a file in a
downloads folder is recognisable) and **a note whose sections are marked with icons** (so a reader can
scan it in three seconds). Both are local files in this repo — no image service, no badge API.

## The marks

Used consistently in every release note, and on the landing page:

| mark | means |
|---|---|
| ✚ | **added** — something new you can use |
| ✓ | **fixed** — it was wrong, now it is right, and the note says what was measured |
| ✎ | **changed** — same behaviour, different shape |
| ✕ | **removed** — deleted, and why |
| ⚑ | **measured** — a number, with the method that produced it |
| ◈ | **offline** — about the service worker, the manifest, the cache |

## The artifacts

| icon | artifact | file | icon source |
|---|---|---|---|
| ▣ | Windows, portable | `kent-repertory-explorer-portable.exe` | `docs/assets/icon.ico` (16–256 px) |
| ▲ | Android, signed | `kent-repertory-explorer.apk` | `docs/assets/icon-512.png` |
| ◍ | Web / PWA | `docs/play/index.html` | `docs/assets/icon.svg` + `icon-192/512.png` |
| ≡ | Source + data | the repo, and the graded JSON | — |

The `.ico` and the PNG sizes are generated, not drawn twice:

```bash
node scripts/icons.mjs     # icon.svg -> icon-{16,32,48,64,192,256,512}.png + og.png
python3 scripts/ico.py     # those PNGs -> icon.ico
```

## How a release is cut

- **Every push to `main`** builds the portable EXE and the signed APK and republishes the rolling
  [`app-latest`](https://github.com/drsamonline/kent-repertory-explorer/releases/tag/app-latest)
  release, then deploys `docs/` to Pages. All three come from the same commit, so the live demo and
  the released build can never disagree.
- **A tagged release** (`v1.1.0`) is the same build, kept, with the note below written from
  `CHANGELOG.md`.
- `VERSION` holds the current version and the app's footer and the landing page print it as a build
  stamp, so "am I on the new one?" is answerable from the page itself.

Always-current downloads:

- `https://github.com/drsamonline/kent-repertory-explorer/releases/latest/download/kent-repertory-explorer-portable.exe`
- `https://github.com/drsamonline/kent-repertory-explorer/releases/latest/download/kent-repertory-explorer.apk`

---

## v1.2.0 — 2026-11-01 · *the enhancements release*

Everything in `ENHANCEMENTS.md` except two items, and that file names both and says what each one
needs. The whole set is one additive layer at the end of the app — no rewriting of the 2 MB body, so
the shipped build and its source cannot drift.

✚ **Named cases.** A selector in the Case panel: switch, new, rename, delete. Each case keeps its own
rubrics and notes. The pre-1.2 single case is migrated on first load.

✚ **Remedy → rubrics.** Click a remedy anywhere — a chip in a rubric, a row in the analysis — and see
every rubric it appears in: the count, the grade split, the chapters, and the 40 narrowest.

✚ **Explain the ranking.** Click a remedy in the analysis for its score, its position, and every rubric
of *this* case marked covers or misses at which grade. The ranking stops being a number.

✚ **Undo / redo** over add, remove, clear and note edits — `Ctrl+Z`, `Ctrl+Shift+Z`, 50 deep.

✚ **Chapter drill-down**, **"did you mean"**, **`#rubric=` / `#remedy=` deep links**, an **offline
indicator**, an **update prompt**, an **install prompt**, and a **print sheet that is the case**.

✎ **Search narrows incrementally.** A keystroke late in a word filters the previous result set instead
of all 74,480 rubrics. ⚑ **Measured: the scan 9.1 ms → 1.5 ms; a keystroke late in a word 1.2–1.9 ms.**
The first keystroke of a broad word still costs ~35 ms — that is sorting tens of thousands of matches,
not scanning them, and it is written down rather than hidden.

✎ **Results arrive 60 at a time** with `Show N more`, instead of 400 cards rendered at once.
✎ **The app follows the system theme on first paint** — it used to open dark on a light device.
✎ **The result list is a listbox**: `role`, `aria-activedescendant`, `aria-expanded`, and an
accessible label on every grade chip.

✓ **The floating tools strip** hardcoded `#111` and stayed dark in the light and high-contrast themes;
it now reads the app's own variables and clears the status line on a phone.

⚑ **Measured:** 14/14 in the dependency-free suite · **24/24** in the new browser suite ·
74,480 rubrics · 735,460 graded links · 669 remedies · 41 chapters · 0 runtime dependencies.

---

## v1.1.0 — 2026-11-01 · *the offline release*

The version that made the offline claim true, and gave the project a face of its own.

◈ **The app now actually caches itself.** `Loom.pwa.register()` was defined and never called, the
manifest's `start_url` was `./app.html` — a file that does not exist under `docs/play/` — and `sw.js`
precached the same missing file, so `cache.addAll()` rejected and the catch swallowed it. The app
looked offline-first and was not. Now: `docs/play/manifest.webmanifest` with `start_url: "./"` and
`scope: "./"`, the worker registered at `../sw.js` with one scope for the whole site, `CORE` listing
the pages that exist, `Promise.allSettled` instead of `addAll`, and `CACHE` bumped to `rpe-v5`.

✚ **Deep links.** `#q=anxiety+night`, `#tab=analysis`, `#demo=case` — applied after boot and again on
every `hashchange`. No router, no dependency. This is what drives the live demo on the landing page.

✚ **A landing page with its own design.** Printed register: paper, ink, one vermilion accent, ruled
lines — deliberately unlike the app, which is a dark instrument panel in blue and violet. Light is the
base palette, the system preference decides the first paint, and a toggle overrides it under the
page's own storage key.

✚ **The demo is the app.** The real app in a browser frame, driven by four guided buttons, with the
screenshot behind it until the frame has actually booted — a blocked frame never looks broken.

✚ **Badges drawn locally.** `scripts/badges.py` writes `docs/assets/badge-*.svg`. The README used to
point at an image service; an offline-first repo that needs the network to describe itself has broken
its own rule.

✚ **Icons for the releases.** `icon.ico` (16–256 px) for the Windows EXE, `icon-192/512.png` for the
APK and the manifest, `icon.svg` for the web, and a generated social card.

✓ **The attribution.** The manifest still described the data as *Kent's Repertory (1897)*, the one
place the correction had not reached. It is Repertorium Publicum (2008).

✓ **The floating tools strip** covered the status line and hardcoded a dark background in every
theme. Nudged above the line in this release; docking it properly is in `ENHANCEMENTS.md`.

✎ **The README** now leads with the badges, states the two licences separately, and documents the
real file layout — including that `docs/play/index.html` is the app.

⚑ **Measured:** 14/14 tests passing · 74,480 rubrics · 735,460 graded links · 669 remedies ·
41 chapters · 1.9 MB single file · 0 runtime dependencies · 0 network requests.

---

## v1.0.0 — 2026-10-25

✎ **Licence.** Every repository in the fleet now carries the canonical PolyForm Noncommercial 1.0.0
text with its Required Notice line, and the four places a repo states its licence agree: `LICENSE`,
the SPDX headers, the README and `package.json`.

✎ **The public demo is the app.** A build now fails if `docs/play/index.html` is not the app, because a
demo running older code is two code paths for one program.

---

Earlier versions — 1.5.0, 1.4.0, 1.3.0 — are in [`CHANGELOG.md`](CHANGELOG.md), written before this
file existed and in a different order.
