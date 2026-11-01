import { route } from "@/server/api";
import { loadLabs } from "@/engine/labs";
import { loadTracks } from "@/engine/tracks";
import { json } from "@/server/http";

/** GET /api/labs/[id] — returns linked academy lessons for a lab's ko_ids */
export const GET = route(async (_req, ctx) => {
  const { id: labId } = await (ctx as { params: Promise<{ id: string }> }).params;

  const f = loadLabs();
  const lab = f.playable.find((l) => l.id === labId);
  if (!lab) return json({ lessons: [] });

  // Build ko_ref → lesson map
  const file = loadTracks();
  const koMap = new Map<string, { id: string; title_ar: string; track_id: string; track_title_ar: string }>();
  for (const track of file.tracks) {
    for (const lesson of track.lessons) {
      for (const ko of lesson.ko_refs) {
        if (!koMap.has(ko)) {
          koMap.set(ko, { id: lesson.id, title_ar: lesson.title_ar, track_id: track.id, track_title_ar: track.title_ar });
        }
      }
    }
  }

  // Collect unique lessons matching this lab's ko_ids (first match per ko wins)
  const seen = new Set<string>();
  const lessons: { id: string; title_ar: string; track_id: string; track_title_ar: string }[] = [];
  for (const ko of lab.ko_ids) {
    const l = koMap.get(ko);
    if (l && !seen.has(l.id)) {
      seen.add(l.id);
      lessons.push(l);
    }
  }

  return json({ lessons });
}, { limit: 60, key: "lab-detail" });
