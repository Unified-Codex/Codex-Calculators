Riven Calculator v4.5 — Complete GitHub Pages release

UPLOAD TO GITHUB:
1. Extract this ZIP locally.
2. Upload the SIX site files (index.html, sw.js, manifest.json and 3 icons)
   to the root of your existing Riven-Calculator GitHub repository.
3. Replace matching files. Keep any other repository files.
4. When GitHub Pages publishes, open https://unified-codex.github.io/Riven-Calculator/.

VERSION 4.5:
- Renamed the Patch Notes tracker tooltip from Total Site Views to Total Visits,
  localized for all 11 languages. No changes to GoatCounter tracking.
- Added a first-visit share prompt, with the requested Tenno/Kuva message,
  a Do not show again checkbox checked by default, and a Copy Link button.
- Uses localStorage to remember the prompt BEFORE showing it (not on Close),
  so refresh, quitting/reopening the browser, and PWA revisits do not retrigger it.
- Detects existing v4.4/earlier visitors via established local preference keys:
  they won't get an unexpected welcome prompt when upgrading.
- If users deliberately UNCHECK Do not show again before dismissing, they opt in
  to seeing the prompt on later visits. Otherwise it will never reappear
  while this browser profile's stored site data exists.
- If storage is blocked, the notice is suppressed completely (rather than
  appearing on every visit).
- This is browser/site storage, not hardware identity. Clearing site data,
  private tabs, a new browser profile, and some separately sandboxed installed
  PWAs can make a returning human look like a first-time visitor.
- Includes localized v4.5 release notes and updated sw.js PWA cache version.

The Download Raw HTML Code action still generates a separate, self-contained
single-file offline HTML. It is different from this website's index.html.
When using a previously installed mobile app, reconnect and visit the updated
site once for its service worker to detect/cache the new release.
