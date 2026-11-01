# QA Report

Honest status. Nothing here claims expert review, user testing, or full visual sign-off.

## Automated results (final run on this code)
- Unit tests: 340 pass. `tsc --noEmit` clean. `next build` passes.
- Full Playwright E2E suite (mobile + desktop projects): 35 passed, 3 failed, 2 skipped in the full run.
  - The 3 failures were desktop-only tests that assume mobile UI (menu button, bottom nav). After the full run these tests were changed to skip on desktop, and the 3 re-ran as skipped. **The full suite was not re-run end to end after that change.**
  - The whole-site axe test (all 40 routes, dark and light, both viewports), the 320px no-overflow test, the theme toggle, the play-tab a11y tests and the studio test all passed in the last runs.

## What was found and fixed (root causes)
| Problem | Root cause | Fix |
|---|---|---|
| Light-theme contrast failures across many pages | Light palette reused dark-theme semantic colours (amber, positive, warning, info) and a too-light muted/accent text colour | Light-specific tokens in `globals.css`; filled-amber controls given light text |
| Play tabs low contrast (light) | Amber/teal/muted text on tinted surface < 4.5:1 | Light overrides for tab label colours |
| Dark positive badge 4.19:1 | Green on teal card | Lighter green in dark theme |
| Skill-card dim rows 3.83:1 | `opacity: 0.7` diluted text | Solid muted colour |
| Season chips 1.83:1 (light) | Hardcoded colours | Themed tokens in light |
| Difficulty bar `aria-prohibited-attr` | `aria-label` on a plain div | `role="img"` |
| `/academy/*` never reached network-idle | `LessonProgressTracker` never read the 401 response body, leaving the request in flight | Body is drained |

## Stale tests updated (not site bugs)
Studio heading (now "مراجعة القضايا"), light background value (`rgb(245, 240, 232)`), theme radio click, and desktop-layout assumptions (no menu button / bottom nav on desktop).

## Not covered
- Menu sheet and bottom nav behaviour is tested on mobile only; desktop sidebar navigation has no equivalent E2E test.
- Automated axe cannot catch every issue (focus order, meaning of content, real screen-reader behaviour). No manual assistive-technology test was done.
- Visual review covers part of the scope only. See `UNRESOLVED_ISSUES.md`.
- Production still needs `ATHAR_DB_URL` confirmed as persistent storage; this was not verified.
