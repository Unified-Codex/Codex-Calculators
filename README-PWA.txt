Warframe Calculators v4.6 — Complete GitHub Pages release

UPLOAD TO GITHUB:
1. Extract this ZIP.
2. Upload / replace all SIX site files (index.html, sw.js, manifest.json,
   icon-192.png, icon-512.png, apple-touch-icon.png) in the SAME root
   folder of your existing Riven-Calculator GitHub repository.
3. Keep any other repository files. README-PWA.txt is optional.
4. Visit https://unified-codex.github.io/Riven-Calculator/ when GitHub Pages deploys.

VERSION 4.6:
- New "Which calculator do you need?" launcher with Rivens and Melee Duplicate.
- "Remember this option" checkbox on the launcher (unchecked by default for
  users without a saved choice). Checking it stores the calculator you open.
- Returning to the main selection screen is always possible from BOTH tools,
  even if you remembered a preference. To stop automatic opening, return to
  the launcher and uncheck "Remember this option".
- Both calculators run within the SAME index.html file; no new HTML pages
  or external JavaScript files are required.
- The Melee Duplicate calculator preserves the supplied Python model, searching
  100%-200% critical chance in 1% increments. Only yellow crits duplicate.
- Launcher, navigation, and new calculator have translations for the existing
  11 languages and share the existing saved language / theme preferences.
- All original Riven calculator features, data, saved setups, patch notes,
  download, theme controls, share prompt, and analytics remain in place.
- Riven's welcome/share prompt opens when a new visitor actually enters Rivens,
  rather than covering the calculator chooser.
- Service-worker cache version updated so PWA/offline users receive the update.
- The "Download Raw HTML Code" button still exports a self-contained HTML
  containing both calculators, without service-worker / install components.

IMPORTANT:
- The choice uses localStorage for THIS site in THIS browser profile. Clearing
  site data or using another browser/device resets it. Saving a preference may
  be unavailable when a browser blocks storage; the chooser still works.
- For previously installed mobile apps, connect to the internet and open the
  updated site to let the service worker detect and cache the release.
