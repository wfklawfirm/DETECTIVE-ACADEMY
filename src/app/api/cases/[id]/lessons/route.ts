import { route } from "@/server/api";
import { json } from "@/server/http";
import { loadTracks } from "@/engine/tracks";

/** GET /api/cases/[id]/lessons — academy lessons linked to this case. */
export const GET = route(async (_req, ctx) => {
  const { id: caseId } = await (ctx as { params: Promise<{ id: string }> }).params;
  const file = loadTracks();
  const linked: { id: string; title_ar: string; track_id: string; track_title_ar: string; minutes: number }[] = [];
  for (const track of file.tracks) {
    for (const lesson of track.lessons) {
      if (lesson.case_link === caseId) {
        linked.push({
          id: lesson.id,
          title_ar: lesson.title_ar,
          track_id: track.id,
          track_title_ar: track.title_ar,
          minutes: lesson.minutes,
        });
      }
    }
  }
  return json({ lessons: linked });
}, { limit: 60, key: "case-lessons" });
