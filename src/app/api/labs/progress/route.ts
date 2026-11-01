import { z } from "zod";
import { route } from "@/server/api";
import { getActor } from "@/server/auth";
import { q, run } from "@/server/db";
import { json, readJson, HttpError } from "@/server/http";

const PostBody = z.object({ lab_id: z.string().min(1).max(120) });

/** GET /api/labs/progress — list of lab_ids the authenticated user has completed. */
export const GET = route(async (req) => {
  const actor = await getActor(req);
  if (!actor.user) return json({ done: [] as string[] });
  const rows = await q<{ lab_id: string }>(
    "SELECT lab_id FROM lab_progress WHERE user_id = ?",
    [actor.user.id],
  );
  return json({ done: rows.map((r) => r.lab_id) });
}, { limit: 60, key: "labs-progress-get" });

/** POST /api/labs/progress — mark a lab done for the authenticated user. */
export const POST = route(async (req) => {
  const actor = await getActor(req);
  if (!actor.user) throw new HttpError(401, "auth_required", "يجب تسجيل الدخول لحفظ التقدم");
  const { lab_id } = await readJson(req, PostBody);
  await run(
    "INSERT OR IGNORE INTO lab_progress(user_id, lab_id, done_at) VALUES (?, ?, ?)",
    [actor.user.id, lab_id, new Date().toISOString()],
  );
  return json({ ok: true });
}, { limit: 30, key: "labs-progress-post" });
