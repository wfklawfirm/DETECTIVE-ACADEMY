# QA results — branch `redesign/mobile-first`

| Check | Result |
|---|---|
| Unit tests (vitest) | 345 / 345 pass |
| `tsc --noEmit`, `next build` | clean |
| Playwright E2E (mobile Pixel 7 + desktop 1366) | 39 passed, 0 failed, 7 skipped (layout-specific skips) |
| axe serious/critical, every page, dark + light | 0 violations (40 routes) |
| Horizontal overflow, 8 routes × 8 widths (320…1440) | 0 overflowing (`audit/screenshots/after/overflow.tsv`) |

## Regressions found and fixed during this pass
The first full run after the palette change had 5 failures (honest record):
copper-on-tinted badges 4.34:1 (light), info badge 4.48:1 (dark), muted text on
dark-tinted surface 4.29:1 (light), positive badge 4.33:1 (light), hard-coded season chip
colour (dark), and a theme test hard-coding the old paper colour. All fixed (tokens in
`redesign.css`; test updated and now reports the offending node).

## NOT tested / not claimed
- Lighthouse / LCP / CLS / INP: **not measured**; no performance claim is made.
- Visual regression diffing: only manual review of before/after PNGs for 8 routes.
- Rotation, offline, reload-resume, all-lab-types mobile tests: not added in this pass.
- Real devices, real screen readers: not tested.
- Workspace/lab/lesson pages: pass axe and E2E but were not visually re-reviewed under the new palette beyond a light-theme check of the case page.
