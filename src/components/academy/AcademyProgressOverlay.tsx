"use client";
import { useEffect, useState } from "react";

/**
 * Client wrapper that:
 * 1. Marks completed lessons with a ✓ indicator (via injected CSS).
 * 2. Shows per-track progress bars on the academy page.
 */
export function AcademyProgressOverlay({
  lessonIds,
  trackMap,
}: {
  lessonIds: string[];
  /** Map from track id → list of lesson ids in that track */
  trackMap?: Record<string, string[]>;
}) {
  const [done, setDone] = useState<Set<string>>(new Set());

  useEffect(() => {
    fetch("/api/academy/progress")
      .then((r) => r.ok ? r.json() : null)
      .then((d) => { if (d?.done) setDone(new Set<string>(d.done)); })
      .catch(() => {});
  }, []);

  // Per-track progress injection: set CSS custom property --track-done / --track-total
  const trackStyles = trackMap
    ? Object.entries(trackMap)
        .map(([trackId, ids]) => {
          const n = ids.filter((id) => done.has(id)).length;
          const pct = ids.length > 0 ? Math.round((n / ids.length) * 100) : 0;
          return [
            `[data-track-id="${trackId}"] .track-progress-bar-fill { width: ${pct}%; }`,
            `[data-track-id="${trackId}"] .track-progress-count { --done: "${n}/${ids.length}"; }`,
            n === ids.length && ids.length > 0
              ? `[data-track-id="${trackId}"] .track-card-header::after { content: " ✓"; color: var(--accent-amber); font-weight: 700; margin-inline-start: 0.25rem; }`
              : "",
          ].filter(Boolean).join("\n");
        })
        .join("\n")
    : "";

  if (done.size === 0) return null;

  return (
    <style>{
      [...done]
        .map((id) =>
          `[data-lesson-id="${id}"] .row-link-title::after { content: " ✓"; color: var(--accent-amber); font-size: 0.85em; }`
        )
        .join("\n") +
      (trackStyles ? "\n" + trackStyles : "")
    }</style>
  );
}
