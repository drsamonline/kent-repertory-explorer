# Changelog

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
