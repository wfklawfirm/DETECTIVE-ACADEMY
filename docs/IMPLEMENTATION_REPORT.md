# Implementation report — Detective Academy redesign (partial)

Branch `redesign/mobile-first` (not merged, production untouched).

## Honest scope
Requested: a full mobile-first rebuild of every surface using 21st.dev components.
Delivered: the shared visual layer plus targeted rebuilds backed by measurements. No 21st.dev code.

## Done
- One design system (charcoal+copper / paper tokens, AA-checked): docs/DESIGN_SYSTEM.md.
- Phone: compact heroes, home CTA in first viewport, opaque safe-area bottom nav, touch targets ≥44px (scan: 0 violations), reduced-motion, visible focus.
- Cases: filters + sort moved into a bottom sheet on phones (inline from 768px).
- Academy: paths first; first path open, others fold.
- Performance: CLS 0 on all measured routes (Arabic UI font via next/font with preload, reserved space for hook card, footer below the fold).
- Tests: tests/e2e/mobile.spec.ts (7 lab kinds × 3 viewports, rotation, reload, offline, filter sheet, academy folding); axe test now names the offending node.
- Docs: REDESIGN_AUDIT, DESIGN_SYSTEM, MOBILE_UX_SPEC, ROUTE_COVERAGE, 21ST_COMPONENT_SELECTION, QA_RESULTS. Screenshots in audit/screenshots/{before,after}.
- Unchanged by design: engine, solutions, hidden-truth handling, progress storage, content, sources/rights.

## Not done / open
- 21st.dev integration (tooling unavailable in this session).
- LCP ≤ 2.5 s on most routes (2.3–4.0 s measured); INP unmeasured. Next steps: trim/split the ~100 KB global CSS, server-render the home hook.
- Workspace, labs, knowledge pages were reviewed and measured but not restructured: no measured defect justified it. Labs are already tap-only (no drag).
- Real devices and screen readers untested; Tajawal not bundled.

## Next
Review the branch's Vercel preview, then merge as the visual foundation or continue on LCP.
