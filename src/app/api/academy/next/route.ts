import { route } from "@/server/api";
import { getActor } from "@/server/auth";
import { q } from "@/server/db";
import { json } from "@/server/http";
import { loadTracks } from "@/engine/tracks";

/** GET /api/academy/next — returns the first undone lesson for the user in track order. */
export const GET = route(async (req) => {
  const actor = await getActor(req);

  // Build ordered lesson list from content files
  const file = loadTracks();
  const ordered: { id: string; title_ar: string; track_id: string; track_title_ar: string }[] = [];
  for (const track of file.tracks) {
    for (const lesson of track.lessons) {
      ordered.push({
        id: lesson.id,
        title_ar: lesson.title_ar,
        track_id: track.id,
        track_title_ar: track.title_ar,
      });
    }
  }

  if (!actor.user) {
    // Guest: recommend first lesson
    const first = ordered[0];
    return json({ lesson: first ?? null, done_count: 0, total: ordered.length });
  }

  // Fetch done lessons
  const rows = await q<{ lesson_id: string }>(
    "SELECT lesson_id FROM lesson_progress WHERE user_id = ?",
    [actor.user.id],
  );
  const done = new Set(rows.map((r) => r.lesson_id));
  const next = ordered.find((l) => !done.has(l.id)) ?? null;

  return json({ lesson: next, done_count: done.size, total: ordered.length });
}, { limit: 60, key: "academy-next" });
