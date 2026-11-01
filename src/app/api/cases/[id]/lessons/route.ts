import { route } from "@/server/api";
import { json } from "@/server/http";
import { loadTracks } from "@/engine/tracks";
import { loadLabs } from "@/engine/labs";
import { getPlayable } from "@/server/content";

/** GET /api/cases/[id]/lessons — academy lessons and labs linked to this case. */
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

  // Also find labs via learning objective KO refs from the case itself
  let labs: { id: string; title_ar: string; skill_ar: string; minutes: number; kind: string }[] = [];
  try {
    const lc = await getPlayable(caseId);
    if (lc) {
      const caseKos = new Set(lc.core.learning_objectives.map((o) => o.skill_ko_ref).filter(Boolean));
      if (caseKos.size > 0) {
        labs = loadLabs().playable
          .filter((lab) => lab.ko_ids.some((ko) => caseKos.has(ko)))
          .slice(0, 4)
          .map((lab) => ({ id: lab.id, title_ar: lab.title_ar, skill_ar: lab.skill_ar, minutes: lab.minutes, kind: lab.kind }));
      }
    }
  } catch {
    // getPlayable failure is non-fatal
  }

  return json({ lessons: linked, labs });
}, { limit: 60, key: "case-lessons" });
