Riven Calculator v3.6.3 — Theme-matched copied Riven cards

FIXED: Your public GitHub repository has the three icon PNGs in the repository
root, but v3.6's service worker expected an /icons/ subfolder. That mismatch
prevented ALL offline files from caching. v3.6.1 corrects the paths and caches
the calculator independently of optional icons.

HOW TO INSTALL:
1. Extract this ZIP. Upload its contents together to the same ROOT of your
   Riven-Calculator repository that already has index.html.
2. Replace the existing index.html, sw.js, and manifest.json. The three PNG
   files should also be in the ROOT (as they currently appear in your repo).
3. Do not put these files inside an extra folder or upload the ZIP itself.
4. Check that https://unified-codex.github.io/Riven-Calculator/sw.js opens
   as readable JavaScript, rather than an error page.
5. Wait for GitHub Pages to finish publishing. On your iPhone, reconnect to
   internet, open your already-installed calculator, and close/reopen it once.
   If your installation predates PWA support, adding the app again from Safari
   may help, but try reopening it online first. IMPORTANT: before deleting an
   old Home Screen app, back up saved Riven setups using Share Setup URLs; on
   iPhone, deleting a web app may also remove its locally saved data.
6. With Wi-Fi and cellular both turned OFF, open the Home Screen app again.
   It should load and calculate normally. The first online visit is required.

SERVICE WORKER DESIGN:
- Essential offline HTML is precached and must succeed before installation.
- Manifest/icons are optional; a missing icon no longer breaks offline mode.
- Navigation fetches a fresh page online, falling back to cached HTML offline.
- New versions are checked at startup, reconnect, focus and periodically.
- No surprise reload: an update is offered, then applied only if accepted.
- External links and fresh API requests still require an internet connection.
- In iOS Settings, clearing website data or offloading storage may remove the
  offline cache. Reconnect and open the app online to repopulate it.

FUTURE RELEASES: update the version string in sw.js and upload both sw.js
and index.html. If you change app icons or their URLs, also update the manifest.

RELEASE 3.6.2: Renamed the mobile-only install button to "Get Mobile App Version".
The service-worker cache was incremented for existing installed users.
No changes were made to the calculator calculation features.

RELEASE 3.6.3: Copy Stats card colors now match the selected site theme.
The stat calculations, copied-card row layout, clipboard text fallback,
installer and offline behavior remain unchanged. The service worker cache was
updated so existing installed users can be offered the new release.
