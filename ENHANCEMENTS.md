# Enhancements

**Status: all nineteen applied** (17 in 1.2.0, the last two in 1.3.0). What remains is what
the work turned up along the way — listed honestly at the end.
Everything below is achievable offline, with no internet and no external dependency: no library, no
CDN, no service, no model. Where an item needed an algorithm, the algorithm is in the repo.

The work landed as one *enhancement layer* (`docs/play/index.html`, at the end of the file, and the
same block in `pipeline/app_template.html`) rather than as edits through the body of a 2 MB single
file — extending the app's own functions keeps the shipped build and its source in step.

## Applied

| # | Enhancement | What was actually built | Verified by |
|---|---|---|---|
| 1 | **Offline indicator + update prompt** | `Offline ready` chip once a worker controls the page; `New version — reload` when a new worker installs; `registration.update()` on every load | manual, over http |
| 2 | **Build stamp in the app** | `build 1.2.0 · 2026-11-01` in the app's footer, beside the source line | functional test |
| 3 | **Search stops rescanning everything** | Incremental narrowing: while the query only grows and the filters do not change, the next keystroke filters the previous result set instead of all 74,480 rubrics | measured, below |
| 4 | **"Did you mean"** | On a zero-result query of 4+ letters, edit-distance-1 against a word list built from the repertory's own vocabulary | functional test (`consolaton` → `consolation`) |
| 5 | **Remedy → rubrics** | Click any remedy chip, in a rubric or in the analysis, to see every rubric it appears in: count, grade split, chapters, and the 40 narrowest | functional test |
| 6 | **More than one case** | Named cases with a selector in the Case panel — switch, new, rename, delete; each keeps its own rubrics and notes; the pre-1.2 single case is migrated on first load | functional test |
| 7 | **Explain the ranking** | Click a remedy in the analysis to see the score, the position, and every rubric of *this* case marked covers or misses at which grade | functional test |
| 8 | **Undo / redo** | Snapshot stack (50 deep) over add, remove, clear and note edits; `Ctrl+Z` / `Ctrl+Shift+Z` | functional test |
| 9 | **Chapter drill-down** | Browse → chapter → its sub-branches with counts → search inside a branch | functional test (41 chapters, 384 Abdomen branches) |
| 10 | **Progressive results** | 60 cards, then `Show N more` in steps, instead of 400 at once | functional test (60 → 120) |
| 11 | **Accessible result list** | `role="listbox"` + `option`, `aria-activedescendant`, `aria-expanded`, and an accessible label on every grade chip | functional test |
| 12 | **Print sheet is the case** | A print stylesheet that drops the interface and prints the case: name, date, rubric list, notes, analysis, matrix | print-media render |
| 13 | **Install prompt** | `beforeinstallprompt` → an `Install` chip that disappears once used | manual |
| 14 | **Deep links** | `#q=`, `#tab=`, `#demo=` (1.1.0) plus `#rubric=<id>` and `#remedy=<abbr>` | functional test |
| 15 | **Theme on first paint** | Follows `prefers-color-scheme` until the reader chooses; the toggle still wins | functional test (light emulated) |
| 16 | **The retrofit strip** | Theme-aware from the app's own variables, and lifted clear of the status line on a phone | screenshots |
| 17 | **Releases with icons** | `icon.ico` for the EXE, PNG sizes for the APK and manifest, `og.png` social card, `RELEASES.md` | `scripts/ico.py`, `scripts/icons.mjs` |
| 18 | **Smaller payload** | The dataset re-encoded columnar (v2): parallel arrays, one concatenated link blob, no key names repeated on 98,000 nodes. **1,459,700 → 1,346,954 bytes gzipped (−7.7%)**; the page 2.04 MB → 1.90 MB | `pipeline/recompress.py` verifies all 74,480 rubrics decode identically before writing; the browser suite re-checks the counts |
| 19 | **Scoring methods** | Three weightings (3·2·1, 1·1·1, 9·4·1) and an eliminative filter (grade 2+ in every rubric), with the formula printed on the screen and in every export | browser suite: the score moves with the weights, the header names the method, the export states it |

## Measured, not asserted

Timed in the browser on the real 74,480 rubrics (headless Chromium, desktop):

| | before 1.2.0 | 1.2.0 |
|---|---|---|
| the scan for a two-word query | **9.1 ms** | **1.5 ms** |
| a keystroke late in a word (`weeping consolati…`) | 9.1 ms + sort | **1.2–1.9 ms** |
| the first keystroke of a broad word (`w`) | 9.1 ms + sort of ~60,000 | ~35 ms — **unchanged** |

That last row is honest and matters: the first letter of a broad word matches tens of thousands of
rubrics, and the cost there is *sorting them*, not scanning them. Fixing it needs a bounded top-k
selection — and that has to keep the full candidate set for the narrowing above, so it is not the
one-liner it looks like. Left open deliberately, with the number on the table.

## What is left, and why

**The scoring presets are named by arithmetic, not by a school.** 3·2·1, 1·1·1 and 9·4·1 are exactly
what they say they are, and the app prints which one produced a number. They are *not* labelled
"Kent", "Boger" or "Boenninghausen", because those are clinical conventions and I will not put a
school's name on arithmetic I cannot verify against its own literature. If you want those labels,
what is needed is the definition written down — the weights, the tie-breaks, and what "eliminated"
means for a remedy that fails one high-grade rubric — and the labels can then be added to `METHODS`
in the enhancement layer in an afternoon.

**The payload could go further.** v2 is 7.7% smaller. The remaining weight is the link blob: 735,460
pairs, 2 base36 characters for the remedy and 1 for the grade. Delta-encoding the indices was tried
and measured *worse* (1,496,245 bytes against 1,346,954) because the order is not ascending and the
bias needed to keep negatives costs more than it saves. Packing the index arrays into strings was
also tried: 25 KB better, not worth the decode complexity. The one real remaining win is serving the
data as a sibling `.json.gz` for the web build and keeping the embedded copy only for the portable
file — that needs two build outputs from `app-builder`, not a change in this repo.

## Still worth doing

- **Storage in IndexedDB.** Cases still live in `localStorage` (~5 MB, synchronous). Moving the store
  is a migration with a compatibility window, not a feature; `navigator.storage.persist()` — the part
  that actually stops eviction — is not yet wired either.
- **A bounded top-k for the first keystroke** (see the timing table above): ~35 ms, and the cost is
  sorting, not scanning.
- **Windowing rather than stepping.** `Show more` bounds the DOM; recycling a fixed window on scroll
  would be smoother, and needs the sort question above solved first.

## Deliberately not doing

- **No accounts, no sync, no telemetry.** Not a roadmap item that is waiting; a boundary.
- **No LLM repertorisation.** A model that ranks remedies is a model that invents them. The grades are
  the printed grades, and the reasoning stays visible — that is what item 7 above is for.
- **No CDN, ever, not even for a font.** A webfont is a network request; the type is the system's.
- **No auto-updating data.** The dataset is fixed and cited. A new edition is a new release with a new
  citation, not a silent refresh.
