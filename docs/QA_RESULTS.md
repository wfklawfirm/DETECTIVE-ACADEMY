# QA results — branch `redesign/mobile-first`

| Check | Result |
|---|---|
| Unit tests (vitest) | 345 / 345 pass |
| `tsc --noEmit`, `next build` | clean |
| Playwright E2E, full suite (mobile Pixel 7 + desktop 1366) | final full run on the last commit: **58 passed, 0 failed, 14 skipped** (skips are layout-specific: mobile-only tests on desktop and vice versa) |
| axe serious/critical, 40 routes × dark/light | 0 violations (full run before the last UI changes; re-covered by the full run above) |
| Horizontal overflow, 8 routes × 8 widths (320…1440) | 0 overflowing (`audit/screenshots/after/overflow.tsv`) |
| Tap-target scan (12 routes × 320×640, 390×844, 844×390) | 0 targets < 44px after fixes (was 3–15 per page) |
| Mobile E2E (`tests/e2e/mobile.spec.ts`) | all 7 lab kinds at 320/390/landscape, rotation, reload, offline (open page stays usable, no blank screen), cases filter sheet, academy folding |
| Visual review | 24 extra routes × 2 themes at 390px reviewed by eye (contact sheets); no layout breakage or illegible text seen |

## Lighthouse (mobile profile, local production build, simulated throttling) — measured
Final figures after font preload / reserved-space fixes:

| Route | Perf | LCP | CLS | TBT |
|---|---|---|---|---|
| /home | 85–90 | 2.9–3.3 s | 0 | 260–340 ms |  (after server-rendering cards + a neutral hook line; was 4.0 s)
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
- /home, hook line alone: no change (the case card was then the LCP element). Case cards alone: no change
  (the hook text became the LCP element). **Both together shipped**: `/home` is now a server component that
  renders `cards` + server-side progress, and the entry hook renders a neutral spoiler-safe line in the HTML
  that is replaced by the personalised hook when `/api/hook` answers. LCP 4.0 → 2.9–3.3 s (3 runs). Trade-off:
  a returning anonymous visitor whose progress lives in localStorage may briefly see "ملف جديد" before the
  card switches to "تابع التحقيق"; the neutral hook line also changes once.

## Regressions found and fixed in this effort
First post-palette E2E run: 5 failures (contrast on tinted badges 4.29–4.48:1, season chips with
hard-coded colours, a theme test pinned to the old paper colour) — all fixed. CLS 0.116–0.158 on
home/labs/case traced to font swap, footer position and hook-card height — fixed.

## NOT tested / not claimed
- Real devices, real screen readers (VoiceOver/TalkBack/NVDA): not possible here.
- Visual-regression diffing in CI: not added; review was manual.
- Offline: there is NO offline support (no service worker). The test only checks that an already-open page stays rendered; navigating while offline shows the browser's own error page.
- Field (real-user) performance; INP is only a lab proxy (see above).

## Lighthouse on the live production deployment (after merge, 2026-11-03, mobile profile, 1 run each)
| Route | Perf | A11y | LCP | CLS | TBT |
|---|---|---|---|---|---|
| /home | 87 | 100 | **2.0 s** | 0.01 | 460 ms |
| /cases | 88 | 100 | 2.9 s | 0 | 320 ms |
| /academy | 83 | 100 | 3.0 s | 0 | 430 ms |
| /labs | 94 | 100 | 2.6 s | 0 | 160 ms |
| /knowledge | 85 | 100 | 3.0 s | 0 | 370 ms |
| /play/c000_lost_notebook | 89 | 100 | 2.7 s | 0 | 260 ms |

LCP budget (≤ 2.5 s) is met on /home only; the others are 0.1–0.5 s over. CLS budget met everywhere.
Single runs on a simulated slow-4G/4× CPU profile — indicative, not field data. INP still unmeasured.
Tried and rejected: preloading only the 400 font face (next/font would create two families and
synthesise bold) — not shipped.

## Interaction latency (INP proxy) — measured on production, touch emulation, CPU throttled 4×
Worst event duration per interaction (PerformanceObserver `event`, single run, cold first use):

| Interaction | ms |
|---|---|
| open menu sheet | 272 |
| open cases filter sheet | 248 |
| lab: check answer | 184 |
| bottom nav → home | 128 |
| academy: expand path | 120 |
| pick filter chip | 120 |
| close sheet | 88 |
| lab: move step | 72 |

Budget INP ≤ 200 ms: met for 6 of 8 interactions; the two **sheet-opening** interactions exceed it
under 4× throttle (≈ a low-end phone). Likely cost: the sheet marks every other body child `inert` and
moves focus synchronously on open; not yet profiled or optimised. This is a lab proxy, not field INP.
