# QA Report

Honest status. Nothing here claims expert review, user testing, or full visual sign-off.

## Passed (current HEAD)
- Unit tests: 340 pass. `tsc` clean. `next build` passes.
- E2E tests that passed include: RTL, age gate, under-16 handling, entry hook, tutorial, no hidden truth leaked, reduced motion, CSRF, lab classify, play-workspace tabs (dark, and light on desktop).

## E2E failures: compared against baseline (commit fd07d79, before the later performance and audit changes)
The same targeted tests were run on fd07d79 and on HEAD. Result: **no regression detected in the tests compared**. Every test that fails on HEAD also fails on the baseline, except where noted.

| Test | Baseline | HEAD | Cause |
|---|---|---|---|
| a11y dark/light: every page (both projects) | fail | fail | Axe violations on some pages. Messages not yet triaged. OPEN |
| 320px no horizontal scroll (both) | fail | fail | Times out on `networkidle` on some page. Not shown to be real overflow. OPEN |
| Theme toggle (both) | fail | fail | The radio `.check()` is intercepted by the `<span>` label overlay. Likely test-side. OPEN |
| Studio closed to anonymous (both) | fail | fail | Stale test: heading renamed in `4bffa9c`. Needs test update |
| a11y age gate + menu sheet (desktop) | fail | fail | Desktop has no "القائمة" button. Test design. The age-gate dialog part passes |
| Play tabs light (mobile) | fail | fail | color-contrast on the "الملف" tab. Real a11y issue, pre-existing. OPEN |

The baseline run covered only these 16 test cases, not the whole suite. Passing status of other tests was observed on HEAD only.

## Not done
- These failures are not fixed. They are documented, not resolved.
- Only part of the audit scope was visually reviewed. See `UNRESOLVED_ISSUES.md`.
