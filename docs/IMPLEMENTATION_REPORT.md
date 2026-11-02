# Implementation report — Detective Academy redesign (partial)

Branch `redesign/mobile-first` (not merged, production untouched).

## Honest scope
Requested: a full mobile-first rebuild of every surface using 21st.dev components.
Delivered: **Stages 1–2 plus a QA pass** — a single visual layer, not a page-by-page rebuild.

## Done
- One design system: charcoal + copper (dark) and paper + dark copper (light) tokens, AA-checked (docs/DESIGN_SYSTEM.md).
- Compact page heroes on phones, opaque bottom nav with safe-area padding, ≥44px touch targets, visible focus, reduced-motion support.
- Before/after screenshots (8 routes × 8 widths), docs: REDESIGN_AUDIT-equivalent findings in `audit/`, DESIGN_SYSTEM, MOBILE_UX_SPEC, ROUTE_COVERAGE, 21ST_COMPONENT_SELECTION, QA_RESULTS.
- No change to engine, case data, solutions, progress storage, or hidden-truth handling.

## Not done
- 21st.dev: tooling unavailable here; nothing imported (see 21ST_COMPONENT_SELECTION.md).
- Rebuilds of Home IA, case filter bottom sheet, investigation workspace layout, academy path-first view, labs tap-alternative, knowledge pages.
- `docs/REDESIGN_AUDIT.md` as a standalone file (earlier audits live in `audit/`).
- Performance measurement; Tajawal not bundled.

## Next
Review the branch's Vercel preview; then either merge as the visual foundation or continue Stage 3 page by page.
