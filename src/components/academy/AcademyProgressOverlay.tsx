"use client";
import { useEffect, useState } from "react";

/**
 * Client wrapper that:
 * 1. Marks completed lessons with a ✓ indicator (via injected CSS).
 * 2. Shows per-track progress bars on the academy page.
 * 3. Highlights the next undone lesson with a "التالي" chip.
 */
export function AcademyProgressOverlay({
  lessonIds,
  trackMap,
  onStats,
}: {
  /** All lesson ids in display order (used to find the first undone) */
  lessonIds: string[];
  /** Map from track id → list of lesson ids in that track */
  trackMap?: Record<string, string[]>;
  /** Called once we know how many lessons are done */
  onStats?: (done: number, total: number) => void;
}) {
  const [done, setDone] = useState<Set<string>>(new Set());

  useEffect(() => {
    fetch("/api/academy/progress")
      .then((r) => r.ok ? r.json() : null)
      .then((d) => {
        if (d?.done) {
          const s = new Set<string>(d.done);
          setDone(s);
          onStats?.(s.size, lessonIds.length);
        }
      })
      .catch(() => {});
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Per-track progress injection
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

  // Find the first undone lesson (in lessonIds order)
  const nextId = lessonIds.find((id) => !done.has(id));

  // Next-lesson highlight styles
  const nextStyle = nextId
    ? `[data-lesson-id="${nextId}"] .row-link-title::before { content: "▶ "; color: var(--accent-amber); font-size: 0.8em; }\n` +
      `[data-lesson-id="${nextId}"] { position: relative; }\n` +
      `[data-lesson-id="${nextId}"]::after { content: "التالي"; font-size: 0.65rem; font-weight: 700; letter-spacing: 0.04em; ` +
      `color: var(--bg-base); background: var(--accent-amber); padding: 0.1rem 0.45rem; border-radius: 99px; ` +
      `margin-inline-start: 0.5rem; vertical-align: middle; display: inline-block; }\n`
    : "";

  // Nothing to show if no progress and no next lesson to highlight
  if (done.size === 0 && !nextId) return null;

  return (
    <style>{
      [...done]
        .map((id) =>
          `[data-lesson-id="${id}"] .row-link-title::after { content: " ✓"; color: var(--accent-amber); font-size: 0.85em; }`
        )
        .join("\n") +
      (trackStyles ? "\n" + trackStyles : "") +
      (nextStyle ? "\n" + nextStyle : "")
    }</style>
  );
}
