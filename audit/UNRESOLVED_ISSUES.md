# UNRESOLVED_ISSUES

## Needs a decision or access from you

1. **Persistent database.** In code the default DB on Vercel is `file:/tmp/athar.db` (erased with each instance) unless `ATHAR_DB_URL` is set. I tried to list the project's environment variable names to confirm and the request was denied, so I did not check. Please confirm `ATHAR_DB_URL` (and `ATHAR_DB_AUTH_TOKEN` if remote) point to a persistent database. Otherwise accounts and progress will not persist.
2. **Preview mode in production.** `/api/me` reports `preview_mode: true` and all 30 cases show `preview: true` (drafts, not published). Whether that is intended for the current stage is your call; it affects what the 3 s cold start still pays for.

## Not done (so the audit is not complete)

- Tablet 768 px: only 14 key pages were captured and measured (no overflow, all load). The remaining routes were not.
- Interaction states from the brief (filters, empty search results, lesson answers right/wrong, lab flows, gallery lightbox, a returning user with progress, case play states) were **not** exercised or photographed.
- Visual review: I looked at the screenshots for `/cases`, `/home`, `/start`, one case page, `/reasoning` and the age dialog. The other page types were measured automatically (height, overflow, touch targets, broken images, text length) but not reviewed one by one for hierarchy, density or alignment.
- Coverage: 286 routes, not every route. Concepts (30 of 483) and knowledge objects (21 of 377) are stratified samples; the rest share a template. 22 sampled routes return 404 by design (age/audience gates).
- Touch targets: 259 targets under 32 px remain on `/glossary` mobile, 765 on `/credits`, 141 on `/atlas` (32 px is a stricter proxy than WCAG 2.2's 24 px minimum). Not triaged.
- Very long pages not yet reduced: `/sounds` 25,878 px, `/books/BK-741` 21,412 px, `/knowledge` 20,754 px, `/sources` 18,413 px, `/icons` 18,271 px, `/heritage` 14,810 px.
- The P1 structural recommendations in `DETAILED_AUDIT_AR.md` (simplified navigation, lesson player, separating "ready to play" archetypes, moving authoring notes out of the index) were not started. They are design changes that should follow a visual review, not be guessed from measurements.
- Cold start is 3.1-4.3 s, not instant. Remaining cost is the draft comparison query plus function start; a stored content hash column would remove the comparison.
- Raw screenshots (about 160 MB) are not committed; only measurements, the index, findings and a few comparison images are.

## E2E failures present before this work (see QA_REPORT.md)
- Axe violations on some pages (dark and light), 320px networkidle timeout, theme-toggle radio overlay, light-theme contrast on the play "الملف" tab (mobile), stale studio heading test, desktop menu-sheet test assumption.
