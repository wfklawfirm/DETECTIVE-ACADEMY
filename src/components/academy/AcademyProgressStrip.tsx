"use client";
import { useEffect, useState } from "react";

/**
 * Renders a compact progress strip on the academy list page
 * once the user has completed at least one lesson.
 * Fetches progress independently (no prop drilling required).
 */
export function AcademyProgressStrip({ total }: { total: number }) {
  const [done, setDone] = useState<number>(-1); // -1 = not yet loaded

  useEffect(() => {
    fetch("/api/academy/progress")
      .then((r) => r.ok ? r.json() : null)
      .then((d) => { if (d?.done) setDone((d.done as string[]).length); else setDone(0); })
      .catch(() => setDone(0));
  }, []);

  // Don't render until loaded, and hide if zero progress
  if (done <= 0) return null;

  const pct = Math.round((done / total) * 100);
  const allDone = done >= total;

  return (
    <div
      className="labs-progress-strip"
      role="status"
      aria-label={`أكملت ${done} من ${total} درساً`}
    >
      <span className="labs-progress-text">
        {allDone ? (
          <>أكملت <b>كل الدروس</b> 🎓</>
        ) : (
          <>أكملت <b>{done}</b> من <b>{total}</b> درساً</>
        )}
      </span>
      <div className="labs-progress-bar-wrap" aria-hidden>
        <div
          className="labs-progress-bar-fill"
          style={{ width: `${pct}%` }}
        />
      </div>
      <span className="labs-progress-pct small dim" aria-hidden>
        {pct}٪
      </span>
    </div>
  );
}
