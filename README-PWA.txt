Warframe Calculators v4.7 — Complete GitHub Pages release

UPLOAD TO GITHUB:
1. Extract this ZIP and upload/replace ALL SIX website files in the same
   root folder as the current site: index.html, sw.js, manifest.json,
   icon-192.png, icon-512.png, apple-touch-icon.png.
2. Keep any other existing repository files. README-PWA.txt is optional.
3. Visit the existing GitHub Pages URL after Actions reports a deployment.
4. If an installed offline app is still showing v4.6, open it while online
   and accept its update prompt to refresh the service worker cache.

NEW IN v4.7:
- Added a Show Grade Ranges button inside each selected Riven stat result.
- On click, expands that stat's possible values into eleven grade bands:
  F, C-, C, C+, B-, B, B+, A-, A, A+, S.
- Cutoffs use deviations from the exact, UNROUNDED Riven midpoint:
  -10, -9.5, -7.5, -5.5, -3.5, -1.5, +1.5, +3.5,
  +5.5, +7.5, +9.5, +10 percent.
- Negative values are ordered by magnitude, including recoil reductions.
- Heavy Attack Critical Chance and Bow Fire Rate also show doubled values
  in the expanded grading table where the main Riven card doubles them.
- Table numbers use extra precision where necessary to distinguish narrow
  bands; card ranges remain exactly as before.
- Expansions stay open if you change stat, layout, language, or weapon type.
- All new user-facing strings translated into the existing 11 languages.
- Release notes added without deleting the previous history.
- Updated cache version to v4.7 for offline and installed-web-app updates.

IMPORTANT:
- This grading scale is community-derived from the supplied grading
  examples. It is NOT an official Digital Extremes / Warframe grade system,
  and it has NOT been proven to precisely match every community grading bot.
- A larger negative magnitude receives a higher roll-strength grade, but is
  not necessarily more desirable. Displayed numbers are rounded, so exact
  edge cases can be ambiguous.
- Every calculator remains self-contained inside index.html with no Python
  or additional service required. Existing Riven calculations, preferences,
  saved configurations, Melee Duplicate, chooser, and translations preserved.
