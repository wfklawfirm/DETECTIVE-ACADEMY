import { route } from "@/server/api";
import { getActor } from "@/server/auth";
import { q } from "@/server/db";
import { json } from "@/server/http";
import { loadLabs } from "@/engine/labs";

/** GET /api/labs/next — returns the first undone lab for the user in content order. */
export const GET = route(async (req) => {
  const file = loadLabs();
  const ordered = file.playable.map((l) => ({
    id: l.id,
    title_ar: l.title_ar,
    skill_ar: l.skill_ar,
    minutes: l.minutes,
    kind: l.kind,
  }));

  const actor = await getActor(req);

  if (!actor.user) {
    // Guest: recommend first lab
    return json({ lab: ordered[0] ?? null, done_count: 0, total: ordered.length });
  }

  const rows = await q<{ lab_id: string }>(
    "SELECT lab_id FROM lab_progress WHERE user_id = ?",
    [actor.user.id],
  );
  const done = new Set(rows.map((r) => r.lab_id));
  const next = ordered.find((l) => !done.has(l.id)) ?? null;

  return json({ lab: next, done_count: done.size, total: ordered.length });
}, { limit: 60, key: "labs-next" });
