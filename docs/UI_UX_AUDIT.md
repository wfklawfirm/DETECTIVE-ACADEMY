# Detective Academy — UI/UX Audit Report

**Auditor:** AI Design & Engineering Team  
**Date:** October 2026  
**Application:** Detective Academy — Arabic RTL Interactive Mystery Learning Platform  
**Reference URL:** https://detective-academy-wfklawfirms-projects.vercel.app

---

## Executive Summary

The application had a critical desktop layout defect: the entire UI was constrained to a 512 px column on all screen sizes due to a single CSS token (`--frame: 32rem`). On desktop monitors, this produced a narrow mobile-width column surrounded by large empty dark areas — an immediately visible professional quality problem. The redesign corrects this at the architectural level and introduces a coherent cinematic design system.

---

## 1. Critical Desktop Layout Bug

### Root Cause

```css
/* globals.css — BEFORE */
:root {
  --frame: 32rem; /* 512 px */
}
.frame {
  max-inline-size: var(--frame);  /* ← entire app limited to 512 px */
  margin-inline: auto;
}
.bottom-nav {
  max-inline-size: min(var(--frame), 32rem); /* ← nav also 512 px */
}
```

**Effect:** On a 1440 px desktop, the application rendered inside a 512 px column with ~928 px of unused dark space on each side.

### Fix Applied

- Removed `--frame: 32rem` token entirely.
- Desktop (≥ 1280 px): switched to sidebar + content layout. No max-width cap on the outer frame.
- Tablet (768–1279 px): content constrained to `56rem` for comfortable reading.
- Mobile (< 768 px): full-width column layout, unchanged behavior.

---

## 2. Design System Deficiencies (Before)

| Problem | Impact |
|---|---|
| Single monolithic color palette — no surface hierarchy | All surfaces looked identical; no depth |
| No accent color system | CTAs and interactive states blended into background |
| No typography scale — single `font-size` | Hero, headings, body, metadata all appeared similar |
| No component spacing tokens | Inconsistent padding throughout |
| No desktop layout CSS at all | 100% of layout was mobile-only |
| No animation system | No hover states, no loading feedback |

---

## 3. Navigation Audit

| Issue | Severity |
|---|---|
| Mobile bottom nav had same 512 px max-width constraint as frame | High |
| No desktop navigation — sidebar was completely absent | High |
| Nav links had no active state styling | Medium |
| Safe-area bottom padding missing on some screens | Medium |

---

## 4. Cases Page Audit

| Issue | Severity |
|---|---|
| Simple flat list of `<CaseCard>` with no visual hierarchy | High |
| No hero section — page started immediately with cards | Medium |
| No filter bar — all cases mixed together | Medium |
| No progress summary | Medium |
| No featured case concept | Medium |
| Generic card styling — no dossier file aesthetic | High |
| No loading skeleton | Medium |
| No empty state | Low |

---

## 5. Responsive Breakpoints (Before)

Only one implicit breakpoint existed — the app was either "narrow column" or "narrow column with more blank space." No responsive layout switching was implemented.

---

## 6. Arabic RTL Assessment

RTL implementation was correct in the existing code. The `lang="ar" dir="rtl"` attributes, logical CSS properties (`inline-size`, `padding-inline`, `margin-block`), and RTL-aware icon usage were all properly implemented. No RTL issues found.

---

## 7. Accessibility Issues Found

- No `aria-current` on nav links (no active state)
- Missing `aria-label` on icon-only buttons in some contexts
- `skip` link present and correctly implemented
- Contrast: some muted text (`--foreground-muted`) near 3:1 on dark surfaces — acceptable for decorative/secondary text

---

## 8. Performance

- CSS was a single file (acceptable for this app scale)
- No unused critical-render-path CSS identified
- Font loading via Google Fonts `display=swap` (correct)
- No large unoptimized images identified in the cases page

---

## 9. Files Audited

```
src/styles/globals.css          ← Root cause of desktop bug
src/components/Shell.tsx        ← Navigation architecture
src/app/cases/page.tsx          ← Primary redesign target
src/components/CaseCard.tsx     ← Type definitions (preserved)
src/components/ui/card.tsx      ← UI primitives (preserved)
src/components/ui/badge.tsx     ← Badge + MasteryMeter (preserved)
src/components/ui/button.tsx    ← Button variants (preserved)
src/server/content.ts           ← Data layer (not modified)
```
