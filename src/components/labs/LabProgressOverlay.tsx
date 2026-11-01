"use client";
import { useEffect, useState } from "react";

/**
 * Client wrapper that:
 * 1. Marks completed labs with a ✓ indicator (via injected CSS targeting data-lab-id).
 * 2. Reports completion count to the parent page via onStats callback.
 */
export function LabProgressOverlay({
  labIds,
  onStats,
}: {
  /** All lab ids in display order */
  labIds: string[];
  /** Called once we know how many are done */
  onStats?: (done: number, total: number) => void;
}) {
  const [done, setDone] = useState<Set<string>>(new Set());

  useEffect(() => {
    fetch("/api/labs/progress")
      .then((r) => r.ok ? r.json() : null)
      .then((d) => {
        if (d?.done) {
          const s = new Set<string>(d.done as string[]);
          setDone(s);
          onStats?.(s.size, labIds.length);
        }
      })
      .catch(() => {});
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  if (done.size === 0) return null;

  return (
    <style>{
      [...done]
        .map((id) =>
          `[data-lab-id="${id}"] .card-link-title::after,` +
          `[data-lab-id="${id}"] b { }` +
          `[data-lab-id="${id}"]::before { content: ""; }` +
          `[data-lab-id="${id}"] { --lab-done: 1; }` +
          `[data-lab-id="${id}"] .lab-done-chip { display: inline-flex !important; }`
        )
        .join("\n")
    }</style>
  );
}
