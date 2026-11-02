# Mobile UX spec (as implemented)

- Navigation: 5-item bottom nav < 1280px, persistent sidebar ≥ 1280px (pre-existing; kept). Nav is opaque and pads for the home indicator.
- Page heroes are compact on phones (badge glyph hidden, smaller title) so the first card is visible above the fold.
- `main` reserves nav height + safe area at the bottom, so CTAs never hide beneath the nav.
- Targets ≥ 44px for coarse pointers; no hover-only interactions were added.
- Bottom sheets (`ui/sheet.tsx`, filter/menu) already exist and were not modified.

## Not redesigned in this pass
Investigation workspace layout, lab tap-alternatives, academy path-first restructure, case
filter bottom sheet changes, home information architecture. See IMPLEMENTATION_REPORT.md.
