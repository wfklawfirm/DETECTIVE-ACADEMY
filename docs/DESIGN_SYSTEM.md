# Design system — Modern Noir × Cold Case Archive (+ editorial reading)

Implemented as one override layer: `src/styles/redesign.css` (loaded after `globals.css`).
`globals.css` still holds component rules; legacy aliases (`--accent-teal`, `--accent-amber`,
`--text-secondary`) now resolve to the new tokens, so all pages follow one palette.

## Tokens
| Token | Dark | Light (paper) |
|---|---|---|
| background | #111619 | #F3EEE3 |
| surface | #1D2528 | #EBE5D8 |
| surface-soft (elevated) | #273034 | #E2DBCB |
| foreground | #F3F0E9 | #2A2620 |
| secondary | #B6B9B8 | #4A443A |
| muted | #9AA2A3 | #645C4F |
| accent (copper) | #C9A16B | #6B4A1C |
| accent-contrast | #111619 | #FBF7EE |

Status colours (positive/negative/warning/info) unchanged from the previous AA-checked set.

## Contrast (computed, WCAG 2.x)
Dark: text/bg 16.0, text/surface 13.7, secondary/surface 7.9, muted/elevated 5.2, copper/bg 7.6, copper/elevated 5.6, dark-on-copper 7.6.
Light: text/bg 13.0, secondary/soft 7.0, muted/soft 4.8, copper(#6B4A1C)/bg ~7, copper/muted-surface >=4.5, light-on-copper >=7. (Copper darkened from #7A5521 and info lightened to #8FABF7 after axe flagged 4.34 and 4.48 on tinted badges.)
All ≥ 4.5:1. (Computed from hex pairs only — not a substitute for an axe run on every page.)

## Typography
IBM Plex Sans Arabic UI, Amiri display (unchanged). Body 16px/1.75. Tajawal is listed in the
stack as a fallback name only; it is **not bundled**.

## Rules in the layer
Touch targets ≥44px on coarse pointers; visible focus ring; `prefers-reduced-motion`;
`env(safe-area-inset-*)`; opaque bottom nav; compact page heroes < 768px.
