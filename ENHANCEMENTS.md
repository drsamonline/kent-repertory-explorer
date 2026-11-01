# Enhancements

Everything below is achievable **offline, with no internet and no external dependency**: no library,
no CDN, no service, no model. Where an item needs an algorithm, the algorithm is written in the repo.
Ordered by what it buys the practitioner, not by what is fun to build.

Effort is a rough guide for one careful pass: **S** ≈ an afternoon, **M** ≈ a day, **L** ≈ several days.

---

## P0 — the offline promise, and things that are visibly wrong

### 1. The service worker was never registered, and the manifest pointed at a file that does not exist · **S**
The app defined `Loom.pwa.register()` and never called it; the manifest's `start_url` was
`./app.html`, which does not exist under `docs/play/`; and `sw.js` precached `./app.html` too, so
`cache.addAll()` rejected and the catch swallowed it. **Net effect: an app called "offline-first" never
cached itself.** Fixed in 1.1.0 — `docs/play/manifest.webmanifest` with `start_url: "./"`,
`scope: "./"`, the worker registered at `../sw.js` (one scope for the whole site), `CORE` corrected,
`allSettled` instead of `addAll`, and `CACHE` bumped.

**Still to do:** an "Available offline" indicator, and an update prompt — when a new worker is
waiting, offer *reload to update* instead of letting `skipWaiting` swap it silently under the reader.

### 2. A build stamp in the app itself · **S**
The landing page prints `build 1.1.0 · 2026-11-01`; the app's footer prints the dataset line but not
the build. "Am I on the new one?" should be answerable from inside the app, especially in the
installed PWA where there is no URL bar.

### 3. Search is a linear scan on every keystroke · **M**
`runSearch()` walks all 74,480 rubrics and `indexOf`-es every term on each `input` event. It is fast
enough on a desktop because the data is in memory, but it is O(n) per key and it blocks the main
thread. A prebuilt **inverted index** — term → rubric ids, plus a prefix table — built once at boot
(offline, in the browser) would make each keystroke O(matches) and unlock the next two items.

### 4. Typo tolerance and abbreviation expansion · **M** (needs 3)
A practitioner types `thirstles`, `conciously`, `ameliorat`. Add edit-distance-1 matching against the
index and a small abbreviation table (`amel.` / `agg.` / `r.` / `l.` / `>`, `<`). No model, no
dependency: a Levenshtein pass over candidate terms from the prefix table is a few dozen lines.

### 5. Reverse lookup: "which rubrics is this remedy in?" · **M** (needs 3)
The dataset already holds remedy → links. The inverse index gives the other direction: pick `Ars.`
and see every rubric it appears in, by grade and chapter — the question a student asks most often
after an analysis, and the one thing the app cannot currently answer.

### 6. The floating retrofit strip overlaps the app and ignores the theme · **S**
`Save my data · Restore · Undo · ?` floats over the status line, hardcodes `background:#111` so it
stays dark in the light and high-contrast themes, and duplicates the app's own Export and `?`.
Dock it into the header (or behind the `?` sheet) and wire it to the theme variables. It has been
nudged above the status line in 1.1.0; the duplication is still there.

---

## P1 — clinical value

### 7. More than one case · **M**
Storage holds a single case under one key. A practitioner runs several. Give cases names, dates and a
list — still `localStorage` or IndexedDB, still nothing leaving the device — with the current case
kept as "today".

### 8. Explain the ranking · **M**
Analysis shows score and coverage. Add a per-remedy panel: which of the case's rubrics it covers, at
which grade, which it misses entirely, and how its rank moved as the last rubric was added. That is
what makes a shortlist defensible to a teacher — and it is all already in `caseList[].links`.

### 9. Elimination and the other methods · **L**
Kent's grade-sum is one method. Boenninghausen/Boger weighting, and the eliminative analysis that
drops remedies which fail a high-grade rubric, are the same data read differently. Offer the method as
a switch, and show the *difference* between them rather than a single number — this is the most
valuable thing the app could do that no book on the shelf can.

### 10. The case as a document · **M**
One printable sheet: the case's rubrics in path order with their notes, the analysis table, the matrix,
and the remedies struck through that were excluded — then print to PDF, or download as a self-contained
HTML file. No PDF library: `window.print()` with a print stylesheet, which is what the "print sheet"
already half-does.

### 11. Storage that survives · **S**
Ask for `navigator.storage.persist()` once the first case is saved, and move cases to IndexedDB
(`localStorage` is ~5 MB and synchronous). A clinical note that a browser evicts is worse than no app.

### 12. Undo/redo in the app's own UI · **S**
The retrofit strip has a global `__undo`; the case editor does not. Wrap `caseList` mutations in a
small command stack with `Ctrl+Z` / `Ctrl+Shift+Z` — the app already rebinds every other key.

---

## P2 — reach and polish

### 13. Drill-down by chapter · **S**
`d.tree` is a real hierarchy, but the app flattens it to paths and only offers a chapter filter.
A breadcrumb — chapter → sub-rubric → rubric — would let someone browse the way the book is read.

### 14. Windowing the result list · **M**
`renderList()` writes up to 400 rubric cards into the DOM at once, each with up to 60 remedy chips.
Render a window of ~40 and recycle on scroll: fewer nodes, no layout storms on a phone.

### 15. Accessibility of the result list · **M**
The results are `div`s with click handlers. Make the list a `listbox` with `aria-activedescendant`,
announce the result count on each search (`role="status"` already exists for the status line), and
give the grade chips an accessible label ("grade 3, strongest") rather than relying on colour.

### 16. Light theme on first paint · **S**
The app defaults to `LS.get('theme','dark')` — dark, regardless of the system preference. Follow
`prefers-color-scheme` for the first paint and keep the toggle as the override; the landing page
already does this.

### 17. Deep links, extended · **S**
`#q=`, `#tab=` and `#demo=` shipped in 1.1.0. Two more are cheap and useful: `#rubric=<id>` to open a
single rubric, and `#remedy=<abbr>` once item 5 exists — so a teacher can send a link to a case, a
rubric or a remedy, and it opens on the device with no network.

### 18. Smaller payload · **M**
The payload is 1.9 MB of gzipped JSON, base64'd (which inflates it by a third). A column-oriented
form — separate arrays for paths, link targets and link grades, and a path-prefix dictionary —
should cut the JSON meaningfully before gzip, and the base64 layer could go entirely if the data were
served as a sibling `.json.gz` for the web build (keeping the single file for the portable one).

### 19. Install prompt · **S**
`beforeinstallprompt` → a quiet "install this on your device" line, only when the browser offers it.
On Android the APK already exists; in the browser, installing is the difference between a website and
an app that opens with the radio off.

---

## Releases, with icons

The release surface has its own set of improvements, and they are all local files:

- **Icons for the binaries.** `scripts/icons.mjs` rasterises `docs/assets/icon.svg` to 16/32/48/64/192/256/512,
  and `scripts/ico.py` packs the small ones into `docs/assets/icon.ico` for the Windows EXE — so the
  download is not a blank page icon in Explorer. The APK takes `icon-512.png`; the PWA takes `icon.svg`
  plus the PNGs in its manifest.
- **A social card.** `docs/assets/og.png` (1200×630) generated from the same icon and wordmark, wired
  to `og:image`, so a shared link shows the app rather than a grey rectangle. Generated locally — no
  image service.
- **Release notes that read the same every time.** `RELEASES.md` fixes an icon per kind of change
  (added, fixed, changed, measured, removed) so a reader can scan a release in three seconds. See it
  there; it is also the template for the next one.

---

## Deliberately not doing

- **No accounts, no sync, no telemetry.** Not a roadmap item that is waiting; a boundary.
- **No LLM repertorisation.** A model that ranks remedies is a model that invents them. The grades are
  the printed grades, and the reasoning stays visible.
- **No CDN, ever, not even for a font.** A webfont is a network request; the type is the system's.
- **No auto-updating data.** The dataset is fixed and cited. A new edition is a new release with a new
  citation, not a silent refresh.
