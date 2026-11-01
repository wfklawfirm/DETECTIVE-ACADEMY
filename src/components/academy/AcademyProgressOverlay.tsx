"use client";
import { useEffect, useState } from "react";

/**
 * Client wrapper that marks completed lessons with a check indicator.
 * Fetches GET /api/academy/progress on mount (silently ignores errors / guests).
 */
export function AcademyProgressOverlay({ lessonIds }: { lessonIds: string[] }) {
  const [done, setDone] = useState<Set<string>>(new Set());

  useEffect(() => {
    fetch("/api/academy/progress")
      .then((r) => r.ok ? r.json() : null)
      .then((d) => { if (d?.done) setDone(new Set<string>(d.done)); })
      .catch(() => {});
  }, []);

  if (done.size === 0) return null;

  return (
    <style>{
      // Inject done-state styles for each completed lesson row
      [...done].map((id) =>
        `[data-lesson-id="${id}"] .row-link-title::after { content: " ✓"; color: var(--accent-amber); font-size: 0.85em; }`
      ).join("\n")
    }</style>
  );
}
