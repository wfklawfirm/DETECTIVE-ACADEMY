# BEFORE_AFTER_COMPARISON

Same 286 routes, same crawler, same viewports (desktop 1440 + mobile 390), same cookie (`athar_age=16-17`), against the published site. Before: 2026-11-01 21:30-21:50 (Asia/Beirut). After: 22:12-22:35, after the deployments listed in IMPLEMENTATION_REPORT.md. Raw numbers: `audit/before_age_all.json`, `audit/after_all.json`.

## Measured

| metric | before | after |
|---|---|---|
| routes with automatic flags | 4 | 0 |
| mobile horizontal overflow | `/reasoning` 444 px on 390 px | none on any route |
| `/glossary` desktop page height | 62487 px | 7915 px |
| `/atlas` | 33532 px | 10689 px |
| `/archetypes` | 20141 px | 12457 px |
| `/glossary` small touch targets, mobile (<32 px) | 1708 | 259 |
| `/home` visible text (chars) | 79 (skeleton) | 4957 |
| `/start` visible text (chars) | 0 (blank) | 55 |
| case pages stuck on skeleton (c017, c019, c022 in the crawl) | 3 | 0 |
| `POST /api/progress`, warm | 6.6-7.8 s | 0.14-0.7 s |
| first request on a new instance | 8.2-10.6 s | 3.1-4.3 s |

## Visual evidence

- Age dialog, production, no cookie: `audit/before_s2/screenshots/desktop/cases-e412d8ef2-full.jpg` (before: no dimmed backdrop, title touching the border, dialog pinned to the bottom) vs `audit/after_extra/agegate-prod-desktop.png` and `agegate-prod-mobile.png` (after: backdrop `rgba(0,0,0,0.6)`, padded header, centred on desktop, bottom sheet with handle on mobile). Committed local copies: `audit/local_check/`.

## Not compared

The other 280 routes were not visually compared screenshot-by-screenshot; the comparison above is by automated measurement. A visual review of each page type is still open (see UNRESOLVED_ISSUES.md).
