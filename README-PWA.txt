Riven Calculator v3.6 — GitHub Pages deployment

Upload ALL of the following to the ROOT of your Riven-Calculator repository:
  index.html
  sw.js
  manifest.json
  icons/icon-192.png
  icons/icon-512.png
  icons/apple-touch-icon.png

Do not upload only index.html: offline installation needs the manifest, service worker and icons.
Keep the icons subfolder intact. After GitHub Pages publishes, load your site online first, then use the mobile-only Download Offline Version button.
On iPhone the button shows installation instructions; on compatible Android Chromium browsers it opens the native install prompt when available.
The mobile toggle has been removed: the base stat table uses Compact layout on phones.
The installed app checks for updates at startup, on reconnection and when focused, and every 30 minutes while open. When a new worker is ready it prompts to reload; users can defer to protect unsaved edits. On a fresh launch the newest version will be loaded online.

IMPORTANT FOR FUTURE RELEASES: Bump CACHE_VERSION in sw.js when updating the calculator. The service worker precaches all offline files for that release.
Offline navigation is cache-backed; external Discord/YouTube links require connectivity.
