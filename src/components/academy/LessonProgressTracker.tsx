"use client";
import { useEffect, useState } from "react";

interface Props { lessonId: string }

/**
 * Fire-and-forget: marks the lesson as done on mount, shows a brief confirmation badge.
 * Guest users see nothing (the API returns 401 which we silently ignore).
 */
export function LessonProgressTracker({ lessonId }: Props) {
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    let cancelled = false;
    fetch("/api/academy/progress", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ lesson_id: lessonId }),
    })
      .then((r) => { if (r.ok && !cancelled) setTimeout(() => { if (!cancelled) setSaved(true); }, 1000); })
      .catch(() => { /* silent — guests or network errors */ });
    return () => { cancelled = true; };
  }, [lessonId]);

  if (!saved) return null;

  return (
    <p
      className="lesson-saved-badge"
      role="status"
      aria-live="polite"
    >
      ✓ تم حفظ تقدمك
    </p>
  );
}
