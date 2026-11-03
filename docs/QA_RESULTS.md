# QA results — branch `redesign/mobile-first`

| Check | Result |
|---|---|
| Unit tests (vitest) | 345 / 345 pass |
| `tsc --noEmit`, `next build` | clean |
| Playwright E2E, full suite (mobile Pixel 7 + desktop 1366) | last full run: 56 passed, 7 failed, 7 skipped. The 7 failures were my new touch-target tests wrongly running on the mouse-driven desktop project; they are now skipped there (`isMobile` guard) and pass on the mobile project. After that edit only `mobile.spec.ts` on desktop was re-run (5 passed, 7 skipped); a final full run was not repeated. |
| axe serious/critical, 40 routes × dark/light | 0 violations (full run before the last UI changes; re-covered by the full run above) |
| Horizontal overflow, 8 routes × 8 widths (320…1440) | 0 overflowing (`audit/screenshots/after/overflow.tsv`) |
| Tap-target scan (12 routes × 320×640, 390×844, 844×390) | 0 targets < 44px after fixes (was 3–15 per page) |
| Mobile E2E (`tests/e2e/mobile.spec.ts`) | all 7 lab kinds at 320/390/landscape, rotation, reload, offline (open page stays usable, no blank screen), cases filter sheet, academy folding |
| Visual review | 24 extra routes × 2 themes at 390px reviewed by eye (contact sheets); no layout breakage or illegible text seen |

## Lighthouse (mobile profile, local production build, simulated throttling) — measured
Final figures after font preload / reserved-space fixes:

| Route | Perf | LCP | CLS | TBT |
|---|---|---|---|---|
| /home | 74–83 | 3.8–4.0 s | 0 | 290–540 ms |
| /cases | 95 | 2.4 s | 0 | 210 ms |
| /academy | 91 | 2.9 s | ~0 | 210 ms |
| /labs | 90 | 3.1 s | 0 | 220 ms |
| /knowledge | 87 | 3.4 s | 0 | 230 ms |
| /glossary | 83 | 3.5 s | 0 | 300 ms |
| /books, /profile | 95–97 | 2.3 s | ≤ 0.065 → 0.035 | 70–140 ms |
Accessibility score: 100 on all 12 measured routes.

**Budget status:** CLS ≤ 0.1 met on every measured route. LCP ≤ 2.5 s is **not met** on most routes
(2.3–4.0 s). Home's LCP element is the per-visit entry hook fetched after hydration (by design);
other pages are held back by ~100 KB render-blocking CSS + hydration under CPU/network
throttling. INP was **not** measured (Lighthouse lab runs do not report it). These are lab
numbers on one machine, not field data. Runner: `tools/perf-lighthouse.mjs`.

## LCP experiments (recorded, not shipped)
- `experimental.inlineCss: true` (CSS inlined in HTML): mixed single-run results — /knowledge 3.4→2.0 s,
  /academy 2.9→2.5 s, but /books 2.3→3.4 s and /glossary 3.5→3.9 s; HTML grows (≈104 KB gzipped on
  /knowledge) and repeat visitors lose the cached stylesheet. No reliable gain → reverted.
- Deduplicating `globals.css` (≈5,000 lines, many repeated rule layers): gzipped CSS is only ≈16 KB, so the
  expected LCP gain is small versus regression risk → not attempted.
- Server-rendering a neutral entry-hook line on /home (replaced after the API answers): LCP unchanged
  (4.0–4.3 s over 3 runs) → reverted. The LCP element on /home is actually the primary case card
  (`.home-primary-glyph`), which only appears after the client fetches the home data (render delay ≈1.4 s).
  Real fix = render the home shell/case cards on the server and apply progress client-side (as the Academy
  page already does). That is a larger refactor of `/home` and was not attempted.

## Regressions found and fixed in this effort
First post-palette E2E run: 5 failures (contrast on tinted badges 4.29–4.48:1, season chips with
hard-coded colours, a theme test pinned to the old paper colour) — all fixed. CLS 0.116–0.158 on
home/labs/case traced to font swap, footer position and hook-card height — fixed.

## NOT tested / not claimed
- Real devices, real screen readers (VoiceOver/TalkBack/NVDA): not possible here.
- Visual-regression diffing in CI: not added; review was manual.
- Offline test only covers an already-loaded page (no service worker/PWA caching exists).
- INP; field (real-user) performance.
