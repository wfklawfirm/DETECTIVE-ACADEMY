# QA Report

Honest status. Nothing here claims expert review, user testing, or full visual sign-off.

## Automated results (final run, commit 4ead221)
- Unit tests: 344 (340 + 4 storage-class tests). `tsc --noEmit` clean. `next build` passes.
- Full Playwright E2E suite (mobile + desktop): **39 passed, 0 failed, 7 skipped** (skips are layout-specific: mobile-only tests skip on desktop and the reverse).
- New tests: desktop sidebar navigation, `/api/health` shape (no config leak), and a document-structure check on every page (lang/dir, one `main`, one `h1`, no skipped heading levels, images have `alt`).

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

## Verified in production
- `/api/health` reports `storage: "persistent"`, so `ATHAR_DB_URL` is not a per-instance local file. It reports only the storage class; I did not read the actual URL or any environment value. Whether that remote database is backed up is not verified.

## Found by looking at real screenshots (new in this round)
- Profile hero on phones broke text letter by letter (an old duplicate CSS rule made the hero a flex row). Fixed.
- `.sr-only` was used in markup but never defined, so "hidden" headings and labels were visible. Defined it.
- Pages missing an `h1` (`/start`) or skipping heading levels (lessons, season). Fixed.

## Not covered
- No manual test with a real screen reader (NVDA/VoiceOver/TalkBack). Automated axe and structure checks cannot prove real assistive-technology behaviour.
- Visual review: I looked at screenshots of `/cases`, `/academy`, `/season`, `/profile` (mobile and, for some, desktop). Observations not fixed: the `/cases` hero has a floating folder icon, an isolated "0%" and wide empty areas; the featured case card is very wide on desktop; the counter says 30 while the filter says 29. Most other page types were not visually reviewed. See `UNRESOLVED_ISSUES.md`.
