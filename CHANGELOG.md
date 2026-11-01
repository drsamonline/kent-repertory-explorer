# Changelog

## 1.2.0 — 2026-11-01 · *the enhancements release*

Everything in `ENHANCEMENTS.md` except two items, which that file names and explains. The work is one
additive layer at the end of the app (and in `pipeline/app_template.html`), so the shipped build and
its source stay in step.

### Added
- **Named cases.** A selector in the Case panel: switch, new, rename, delete. Each case keeps its own
  rubrics and notes. The pre-1.2 single case is migrated on first load.
- **Remedy → rubrics.** Click a remedy anywhere — a chip in a rubric, a row in the analysis — and see
  every rubric it appears in, with the grade split, the chapters, and the 40 narrowest.
- **Explain the ranking.** Click a remedy in the analysis for its score, its position, and every rubric
  of *this* case marked covers or misses at which grade.
- **Undo / redo** over add, remove, clear and note edits — `Ctrl+Z`, `Ctrl+Shift+Z`, 50 deep.
- **Chapter drill-down** — chapter → sub-branches with counts → search inside a branch.
- **"Did you mean"** — edit-distance-1 against the repertory's own vocabulary when a spelling finds
  nothing.
- **Deep links** `#rubric=<id>` and `#remedy=<abbr>`, joining `#q=`, `#tab=` and `#demo=`.
- **Offline indicator, update prompt and install prompt** — `Offline ready`, `New version — reload`,
  and `Install` when the browser offers it. `registration.update()` now runs on every load.
- **A build stamp in the app's footer** — `build 1.2.0 · 2026-11-01` — so "am I on the new one?" is
  answerable from inside the installed app, where there is no URL bar.
- **A print sheet that is the case, not the interface** — name, date, rubrics, notes, analysis, matrix.

### Changed
- **Search narrows incrementally.** While the query only grows and the filters do not change, a
  keystroke filters the previous result set instead of all 74,480 rubrics: the scan measured
  **9.1 ms → 1.5 ms**, and a keystroke late in a word is **1.2–1.9 ms**. The first keystroke of a
  broad word still costs ~35 ms, because that cost is sorting tens of thousands of matches — measured,
  written down, left open.
- **Results arrive 60 at a time** with `Show N more`, instead of 400 cards rendered at once.
- **The app follows the system theme on its first paint.** It used to open dark regardless; the
  toggle still overrides and is remembered.
- **The result list is a listbox** — `role`, `aria-activedescendant`, `aria-expanded`, and an
  accessible label on every grade chip.
- **The retrofit strip is theme-aware** and no longer sits on the status line on a phone.

### Fixed
- The app opened in dark mode even on a device set to light, because `themeName()` defaulted to
  `'dark'` instead of asking `prefers-color-scheme`.
- The landing page's guided scenes leaked state into each other: pressing “a one-remedy rubric” left
  the narrow-only filter on, so “build a case” afterwards built two rubrics instead of three. Each
  scene now resets the filters first.
- The floating tools strip hardcoded `#111` and stayed dark in the light and high-contrast themes.

### Measured
14/14 in the dependency-free suite · 24/24 in the browser suite · 74,480 rubrics · 735,460 graded
links · 669 remedies · 41 chapters · 0 runtime dependencies.

## 1.1.0 — 2026-11-01

- **◈ The offline claim is now true.** `Loom.pwa.register()` was defined and never called; the
  manifest's `start_url` was `./app.html`, which does not exist under `docs/play/`; and `sw.js`
  precached the same missing file, so `cache.addAll()` rejected and the catch swallowed it. The app
  never cached itself. Now: a manifest beside the app (`start_url: "./"`, `scope: "./"`), the worker
  registered at `../sw.js` for one site-wide scope, `CORE` listing files that exist,
  `Promise.allSettled`, and `CACHE` bumped to `rpe-v5`.
- **✚ Deep links** — `#q=`, `#tab=`, `#demo=` — applied after boot and on `hashchange`. No router, no
  dependency. The landing page's guided demo drives the app with them.
- **✚ A landing page of its own** — printed-register design (paper, ink, one vermilion accent), light
  as the base palette, system preference for the first paint, a toggle under its own storage key, and
  the real app embedded in a frame behind a poster screenshot.
- **✚ Badges and icons generated locally** — `scripts/badges.py`, `scripts/icons.mjs`,
  `scripts/ico.py`. The README no longer points at an image service.
- **✓ The last place the wrong attribution survived** — both manifests said *Kent's Repertory (1897)*.
  It is Repertorium Publicum (2008).
- **✓ The floating tools strip** covered the status line and hardcoded a dark background in every
  theme; it now sits above the line.
- **✎ The README** leads with badges, separates the two licences, and documents the real file layout.
- **⚑ Measured:** 14/14 tests passing · 74,480 rubrics · 735,460 links · 669 remedies · 41 chapters ·
  1.9 MB · 0 runtime dependencies.

## 1.0.0 — 2026-10-25

- **Licence: PolyForm Noncommercial 1.0.0.** Every repository now carries the canonical text
  from polyformproject.org with the Required Notice line, and the four places a repo states
  its licence agree: LICENSE, the SPDX headers, the README and package.json.
- **The public demo is the app.** A build now fails if `docs/play/index.html` is not the app,
  because a demo running older code is two code paths for one program.


## [1.5.0] — 2026-10-22
### Fixed
- **Mobile had two levels of tabs, and switching the top one hid the inner strip** — so features
  looked lost. There is now a **single strip of five tabs on mobile** (Search · Browse · Case ·
  Analysis · Matrix); nothing is ever hidden, and every view is one tap away. Desktop keeps its
  two panels with their own tab rows.
- **A stray ✕ floated in the toolbar at all times.** The filter chip used the `hidden` attribute,
  which `.chip{display:inline-flex}` overrode — so it rendered an empty ✕ when no chapter filter
  was set. It now uses a class and is genuinely hidden.
- **"loading…" sat in the toolbar forever** until you typed something. It now reads
  "41 chapters · search to begin" on load.
- **The five tabs overflowed horizontally at 320 px** (page scrolled sideways). The strip now
  scrolls itself and the labels tighten on very small screens.
### Changed
- Tab state is centralised (`mview` + `showPanel`/`syncMtabs`) so the desktop panels and the
  mobile strip can never disagree.
- Keyboard shortcuts `c` / `a` / `m` now switch the view on mobile as well as desktop.

## [1.4.0] — 2026-10-22
### Fixed
- **The Matrix tab showed the Analysis.** `renderMatrix()` was defined but never called — the
  one branch that would have invoked it was missing from `refreshRight()`. Switching tabs really
  did lose a feature. Now wired up.
- **Browsing hid the whole toolbar**, taking the sort control, the filter and the status line with
  it. The toolbar now stays put in Browse; only the search-only controls (sort, narrow) hide.
- **The chapter filter was invisible.** Clicking a chapter silently restricted every later search
  with no indication and no obvious way out. There is now a **Chapter: … ✕** chip in the toolbar
  that shows the active filter and clears it in one click.
### Changed
- **Minified CSS, JS and HTML markup at build time** — 43,413 → 40,731 bytes of code (−6%). The
  readable template stays in `pipeline/app_template.html`; only the shipped `app.html` is minified.
  Verified by comparing 36 elements × 28 computed CSS properties against an unminified twin: no
  differences except a focus ring and a toast mid-animation.
### Removed
- Dead code: the unused `recent` variable, the orphaned `.sr-only` rule, and the now-unused
  inline `style="color:var(--dim2)"` spans (replaced by a `.mut` class).
- The status line is now a proper `role="status" aria-live="polite"` region.

## [1.3.0] — 2026-10-22
### Added
- **Polished UI**: refined type scale and spacing, richer rubric cards with highlighted matches,
  hover/focus states, smoother transitions, and a proper three-step loading screen.
- **Sort options** — narrowest / broadest / A–Z / by chapter.
- **Narrow-only with an adjustable threshold** instead of a fixed cut-off.
- **Per-rubric notes** in the case, saved with the case and included in every export.
- **Exclude a remedy** from the analysis — it stays visible, struck through and sorted last, with a
  ↺ button to bring it back. Excluded remedies are kept out of the exports.
- **Copy to clipboard** for the analysis, alongside text / CSV / JSON / print.
- **Three themes** — dark, light and high-contrast — cycled with the header button or `t`.
- **Welcome screen** on first visit, and a fuller help panel with the shortcut list.
- Honest empty states, and the footer now reports the true dataset counts.
- **New landing page**: hero, stats, features, five-step how-to, a grades explainer, the
  precise provenance note, FAQ and licence.
### Fixed
- The header/footer counts no longer disagree with the indexed data (74,480 rubrics / 735,460 links).
- The footer now sits at the foot of the layout on phones instead of mid-page.

## [1.2.0] — 2026-10-22
### Changed
- **Licence corrected to GNU GPL v3**, and the contradiction removed. The app embeds
  the *Repertorium Publicum* dataset, which is third-party material under **GPL v3**,
  so the combined work is GPL v3. The previous licence claimed the repertory text was
  public domain and that commercial use required a licence — both contradicted the
  licence of the embedded data. GPL v3 permits commercial use and forbids adding
  restrictions, so those clauses are gone.
- Added the full GPL v3 text (`LICENSE-GPL-3.0.txt`).
- README and landing page licence sections now match.

## [1.1.0] — 2026-10-22
### Fixed
- **Corrected the data attribution.** The repertory was labelled "Kent's Repertory
  1897"; it is in fact **Repertorium Publicum (2008)** by Vladimir Polony, an open
  Kent-derived repertory published with the OpenRep source code under **GPL v3**.
  The title, subtitle, help, footer, exports and landing page now say so, and the
  GPL v3 licence of the data is stated.

## [1.0.0] — 2026-10-22
### Added
- First release: 74,480 rubrics, 735,460 graded remedy links, 669 remedies, 41 chapters.
- Search over rubric paths (narrowest first), chapter browse, narrow-only filter.
- Case builder with grade-weighted **Analysis** and a remedy × rubric **Matrix**.
- Filters: minimum grade, "cover all rubrics". Export: text, CSV, JSON, print/PDF.
- Offline-first: single self-contained HTML file, PWA manifest and service worker.
- Dark/light theme, keyboard shortcuts, screen-reader friendly.
