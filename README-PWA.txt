Codex Calcs v5.0 — The Warframe Tools Update (Full GitHub Pages release)

UPLOAD TO GITHUB:
1. Extract the ZIP into your existing GitHub Pages repository location.
2. Replace index.html, sw.js, manifest.json, icon-192.png,
   icon-512.png and apple-touch-icon.png (all six website files).
3. Keep any existing unrelated repository files.
4. Confirm the GitHub Pages deployment in Actions. If using an installed
   offline app, open it while online and accept the update prompt.

NEW IN v5.0 — THE WARFRAME TOOLS UPDATE:
- Codex Calcs officially moves beyond a standalone Riven Calculator into a
  unified Warframe tools site, with four tools accessible from one homepage:
  * Riven Calculator: stat ranges, F–S grade bands, spliced combinations,
    saved setups and copyable Riven stat cards.
  * Melee Duplicate Calculator: optimal critical chance and expected damage.
  * Weekly Tracker: weekly activities and purchases, hide/unhide, local saved
    progress, weekly reset and five shared Search Pulses.
  * Relic Probability Calculator: rare reward chances and Radiant relic
    Radsharing versus Staggering comparisons.
- Added the v5.0 generational release note to the full patch history, with
  translations of the new release summary for all 11 supported languages.
- The same offline support, homepage remember-option, themes, language choices,
  and Wally's Domain surprise are preserved.
- Site version markers, downloaded HTML filename, exported-card version, and
  offline service-worker cache have been bumped to 5.0.
- No formulas or existing user preference / saved progress keys were changed.

PREVIOUS v4.9.6 CHANGES:
- Removed Yuvan Peak — Cryobells as a separate weekly checklist activity.
- Icebind alone tracks the 3 weekly rewarded completions.
- Added a separate note below Icebind: "You can hold up to 6 Cryokeys at max".
- Note translated into all 11 languages. Overall weekly total is reduced by 1.
- Previous progress and hidden preferences for other activities are preserved.
- No changes to other tools or their calculations.

PREVIOUS v4.9.5 CHANGES:
- Every Weekly Tracker activity now has a Hide button.
- Hidden entries are omitted from main and category completion totals.
- An expandable Hidden section at the bottom lists hidden tasks with Unhide buttons.
- Hiding a task does not delete its saved completion, its weekly counter, or any
  shared Search Pulse spending. Restoring the task restores its current progress.
- Hidden choices survive weekly resets (including Friday Conclave resets) and
  are saved locally on each device, separately from regular weekly progress.
- New controls and descriptions are translated into all 11 languages.
- Existing calculators, themes, and other tracker features are unchanged.

PREVIOUS v4.9.4 CHANGES:
- New Flare Beating Heartstrings Kuva (14k per purchase, 3x per week).
- New Acrithis Scuttler Husk Kuva (14k per purchase, 3x per week).
- October 2026 values and individual counters for Nightcap (3), Zorba (7),
  Hunhow (3), and Melica (4); clarified Acrithis rotating Wares and
  Teshin's weekly rotation, with translated reward descriptions.
- Icebind now counts up to 3 weekly successful completions, with updated rewards.
- Netracells checkbox now spends ONLY the remaining Search Pulses: after
  ETA + EDA (4 used), one click marks Netracells 1/1 and pulses 5/5.
- Existing local progress remains saved; same weekly reset behavior.

PREVIOUS v4.9.3 CHANGES:
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

Codex Calcs v5.0.1: Home hub redesign
- Patch Notes, full HTML download, Discord and YouTube links are on the main Warframe Tools page.
- Each tool has a Set as default page checkbox; by default the site opens the hub.
- The mobile install button is available on the hub in mobile browsers and hidden inside installed apps.
- Upload index.html AND sw.js for the new offline cache version.
