Riven Calculator v4.4 — Complete GitHub Pages release

This folder contains the entire deployable GitHub Pages site (not the downloadable standalone HTML).

UPLOAD TO GITHUB:
1. Extract the ZIP on your computer.
2. Open the root of your existing Riven-Calculator GitHub repository.
3. Upload the SIX site files inside this archive to that root; replace matching files.
   Do NOT upload the enclosing folder or the ZIP itself as a single GitHub file.
4. Keep other repository files you may have; deleting them is not necessary.
5. Once GitHub Pages publishes, open https://unified-codex.github.io/Riven-Calculator/.

FILES:
- index.html: current v4.4 online calculator, Riven Codes, patch notes, view counter,
  and standalone HTML download generator.
- sw.js: v4.4 service worker for installed mobile app caching/updates.
- manifest.json: installed app settings.
- icon-192.png, icon-512.png, apple-touch-icon.png: installed app icons.

The 'Download Raw HTML Code' button on the published site generates a separate
self-contained offline HTML. It is NOT the same as index.html in this archive.

Existing app users may need to reopen the website while connected to refresh
their installed app cache. Do not remove the mobile app without first backing
up any locally stored settings.

VERSION 4.4 — PATCH NOTES HEADER & CLEANER MAIN PAGE:
- Moved the existing GoatCounter public total from the calculator main toolbar
  to the Patch Notes header, beside a compact X close button.
- Kept the same recording script and total endpoint, last-good-value cache and
  five-minute refresh. No duplicate tracker or new tracking added.
- Added translated Total Site Views tooltip for every supported language and
  theme-aware subdued colors. Tooltip makes clear totals may be delayed.
- Added a localized First Released (October 2026, month confirmed from initial
  website release period) and Current Version footer to Patch Notes.
- Included localized v4.4 notes in every supported language.
- Updated v4.4 identifiers, clipboard card version, HTML download filename and
  service worker shell cache name so installed mobile apps get the revision.

Earlier release history is preserved (including v4.3.4).
