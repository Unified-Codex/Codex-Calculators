Codex Calcs v4.9.3 — Full GitHub Pages release

UPLOAD TO GITHUB:
1. Extract the ZIP into your existing GitHub Pages repository location.
2. Replace index.html, sw.js, manifest.json, icon-192.png,
   icon-512.png and apple-touch-icon.png (all six website files).
3. Keep any existing unrelated repository files.
4. Confirm the GitHub Pages deployment in Actions. If using an installed
   offline app, open it while online and accept the update prompt.

NEW IN v4.9.3:
- Corrected the URL printed on Riven Copy Stats cards to:
  https://unified-codex.github.io/Codex-Calculators/
- Copy Stats text fallback and share-link prompt now use the same address.
- Updated standalone HTML GitHub version checks to the new repository path.
- Exported card version is read from the current HTML version marker.
- No Riven, Melee Duplicate, Relic or Weekly Tracker calculations changed.

PREVIOUS v4.9.2 CHANGES:
- Removed minutes-per-mission and per-hour estimates; comparisons now focus on
  relic efficiency and number of runs.
- Expanded reward-overlap and filler-relic metrics: labels above, large numbers below.
- Clearer explanations of Radsharing vs staggering; removed redundant footer.
- Fixed double percent sign in the English drop-chance summary.
- The underlying probability formulas and all other tools remain unchanged.

FEATURES ADDED IN v4.9:
- Relic Probability: per-relic odds and squad results (Intact, Exceptional, Flawless, Radiant).
- Compare all-at-once Radshare versus per-player staggered relic openings with equal target-relic budgets.
- Compare expected target copies, chance of overlapping rare rolls, required mission runs, filler relics, and runs required (no minutes or per-hour math).
- Designed for offline use, mobile/desktop, all 11 supported languages, and previous theme options.
- Existing tools, Wally theme surprise, offline preferences, and weekly tracking unchanged.

FEATURES ADDED IN v4.8.1:
- Moved Themes menu from Riven calculator to the home screen, beside Language.
- Selected theme still applies across all three tools.
- Preserved Wallys Domain jumpscare imagery and its occasional visual trigger.
- Bumped service-worker cache version for offline updates.

FEATURES ADDED IN v4.8:
- New third homepage tool, WEEKLY TRACKER, alongside Rivens and Melee Duplicate.
- Existing Remember this option supports all three tools, without changing
  saved Riven configurations, preferences or calculated values.
- 35 individual weekly activity/vendor checklists, each describing rewards.
- Individual counters for 25 Kuva packs, 25 Void Relic packs, 5 Netracells,
  Steel Path Circuit's two Incarnon milestones and 3 Cryobells.
- All three Search Pulse uses share the same five-pulse allowance: 1 per
  Netracell, 2 each for Elite Deep and Elite Temporal Archimedea.
  Over-allocation is prevented.
- Offline localStorage progress persists across page visits without an
  account; progress resets on the first visit or each second after a reset.
- Warframe main weekly reset is Monday 00:00 UTC, which corresponds to
  Sunday 8 PM EDT in summer and Sunday 7 PM EST in winter. The app uses
  the device's system clock, so an incorrect local clock can affect resets.
- Conclave's separately timed Friday 00:00 UTC checkbox resets on Friday.
- Task filtering, progress indicator, manual clear and a live countdown.
- Mobile-friendly and keyboard-accessible controls; tool selection labels
  and all 35 reward descriptions translated for the existing 11 languages.
- v4.8 patch notes and offline cache version updated.

Notes: The tracker is a local user-maintained checklist. It cannot verify
activity completion from Warframe accounts or sync across different devices.
Not every offering is available to every player; prerequisites and rotation
conditions apply. Baro's visits and several open-world cycles are not weekly.
All original calculations remain unchanged.
