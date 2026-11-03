# Redesign audit

Method: before/after screenshots (8 routes × 8 widths), a 24-route × 2-theme phone review,
axe on 40 routes × 2 themes, Lighthouse (mobile profile) on 12 routes, a tap-target scan at
320/390/844×390, and a CLS observer. Baseline = `main` before this branch.

## Findings and what was done

| # | Finding (measured) | Action | Status |
|---|---|---|---|
| 1 | Palette was navy/teal; brief asks charcoal + copper (dark) and paper (light) | tokens in `redesign.css`, AA-checked, 5 contrast regressions caught by axe and fixed | done |
| 2 | Page heroes poster-sized on phones; Home CTA fell below the fold behind the nav | compact heroes; home hero compacted; CTA now in first viewport at 390×844 | done |
| 3 | Bottom nav semi-transparent (content read through it) | opaque, safe-area padded | done |
| 4 | Touch targets < 44px: header icon buttons 32×44/40×40, inline links 19px, search 42, sort select 33, filter chip 43 | CSS min sizes; scan now reports 0 small targets on 12 routes × 3 viewports | done |
| 5 | CLS up to 0.158 (labs), 0.156 (case), 0.116 (home): Arabic font swap, footer inside viewport on loading pages, hook card skeleton ≠ final height | `next/font/local` preload for the Arabic UI font, footer pushed below the fold, hook card height reserved | done: CLS 0 on all measured routes |
| 6 | LCP 2.3–4.0 s on the Lighthouse mobile profile (budget 2.5 s) | font preload, no fade-in on LCP card | **partly**: not met on most routes; see QA_RESULTS |
| 7 | Case filters were 4 chips + a select inline on a phone | one "تصفية وترتيب" button → bottom sheet on < 768px; inline from 768px | done |
| 8 | Academy listed all 36 lessons at once | 6 paths shown; only path A open, others fold (native `<details>`) | done |
| 9 | Labs: drag-only interaction? | none found — every lab kind is tap/button driven (order uses up/down buttons) | no change needed |
| 10 | Workspace tabs (7) | already in the requested order; no overflow, targets ≥ 44px | no change |

## Not changed (and why)
Investigation engine, solutions, hidden-truth handling, progress storage, encyclopedia/book
content, sources/rights notices: untouched by design (non-negotiables).
Info-architecture rewrites of Home/Knowledge beyond the above were judged not justified by
any measured defect; they would add risk without evidence of benefit.
