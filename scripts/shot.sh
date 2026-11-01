#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2026 Dr Sohil Momin
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
# Screenshot the landing page and the app with headless Chromium.
#
#   scripts/shot.sh                 # landing page  -> docs/assets/landing-{desktop,mobile}.png
#   scripts/shot.sh app             # the app       -> docs/assets/app-{desktop,mobile}.png
#
# The app needs time to decompress and index 74,480 rubrics, so the shot waits
# for the loading overlay to clear. It opens a deep link (#demo=analysis) so the
# screenshot shows a populated screen rather than an empty search box.
#
# Needs: node + puppeteer-core + chromium. Development only — the app itself
# loads nothing, and none of this is shipped.
set -euo pipefail
cd "$(dirname "$0")/.."

KIND="${1:-landing}"
WAIT="document.getElementById('load').classList.contains('done')"
READY="document.getElementById('frame').classList.contains('ready')"

if [ "$KIND" = "app" ]; then
  node scripts/shot.mjs --url "docs/play/index.html#demo=analysis" --out docs/assets/app-desktop.png --w 1280 --h 820 --wait "$WAIT" --settle 3200
  node scripts/shot.mjs --url "docs/play/index.html#demo=analysis" --out docs/assets/app-mobile.png  --w 430  --h 860 --wait "$WAIT" --settle 3200
else
  node scripts/shot.mjs --url "docs/index.html" --out docs/assets/landing-desktop.png --w 1280 --h 1400 --full 1 --wait "$READY" --settle 3200
  node scripts/shot.mjs --url "docs/index.html" --out docs/assets/landing-mobile.png  --w 430  --h 900  --full 1 --wait "$READY" --settle 3200
fi
