# IMPLEMENTATION_REPORT

All changes are on `main`; Vercel deploys each push. Every fix below names the measured root cause. Nothing here changes case content, scoring, sources, copyright notes or the hidden-truth boundary.

## P0: platform slow / unusable

| commit | root cause (measured) | change |
|---|---|---|
| `fd07d79` | Every production deploy since the SEO work failed (`ERROR`): `LabsClient` (client component) imported `KIND_LABEL` from `engine/labs.ts`, which uses `node:fs`. None of the earlier SEO/perf commits reached users. Also 3 `tone="success"` (not a valid Tone) and a wrong `"all"` band in `sitemap.ts`. | client-safe `engine/lab-labels.ts`; `tone="positive"`; sitemap uses `null` band so only teen-facing, non-sensitive pages are public; `/api/me` returns the user's own email for the account page. |
| `48cc96e`, `7b8d31e` | `POST /api/progress` took 6.6-7.8 s (6 runs). `listPlayable()` ran one DB query per case (30, sequential, full JSON). `/home`, `/cases`, `/start` and case pages all wait on it. | `getPlayableMany()` and `getCardsLight()` (card fields extracted with `json_extract`, cached per version hash). Tests prove identical selection and identical cards for all 30 cases. Warm: 0.14-0.7 s. |
| `498d23a` | Next warned "Dynamic filesystem access causes tracing of the whole project": every function bundled about 99 MB (public/assets 52 MB, content/research 14 MB, tools/). | `turbopackIgnore` on the dynamic fs calls in `reference.ts`, `content.ts`, `db.ts` (content and migrations are already included explicitly). `/api/me` bundle 99 MB to 29 MB. Traced file lists re-checked for every route's data files. |
| `3d865ed`, `27477a2` | New instances awaited `migrate()` + `syncFileCases()` in `instrumentation.ts`: about 60 sequential round trips uploading all case JSON. Production runs in preview mode, so all 30 cases are drafts. | One listing query; skip published rows; write only draft rows whose content differs; `ensureAdmin` in parallel. Tests: idempotent, draft refresh, published never rewritten. First request on a new instance 8.2-10.6 s to 3.1-4.3 s. |

Earlier in this session (already reported): ISR (`revalidate = 86400`) on 11 content pages, `compress: true`, CDN `Cache-Control` for public routes, process-lifetime JSON cache for labs and tracks.

## P1: layout and states

| commit | finding | change |
|---|---|---|
| `737a05a` | `/reasoning` 444 px wide on a 390 px screen | `.badge` is `white-space: nowrap`; long evidence-strength badge could not wrap. Badges now cap at 100% and wrap below 520 px. |
| `7b8d31e` | `/glossary` 62,487 px (about 220 full cards), `/atlas` 33,532 px | shared `RefBrowser`: 24 items first, "عرض المزيد" and "عرض الكل"; search/filter reset the window; `#GL-id` deep links reveal the target. |
| `7c9bb65` | Age dialog: no backdrop, title touching the border, pinned to the bottom on desktop | `Sheet` used class names with no CSS (`sheet-scrim`, `sheet-grip`, `sheet-head`). Names aligned with the existing CSS; centred dialog from 640 px as the component comment already documented. |
| `7c9bb65` | `/start` blank (0 chars) while waiting | standard loading skeleton |
