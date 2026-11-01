import { z } from "zod";
import { route } from "@/server/api";
import { getActor } from "@/server/auth";
import { q, run } from "@/server/db";
import { json, readJson, HttpError } from "@/server/http";

const PostBody = z.object({ lesson_id: z.string().min(1).max(120) });

/** GET /api/academy/progress — list of lesson_ids the authenticated user has completed. */
export const GET = route(async (req) => {
  const actor = await getActor(req);
  if (!actor.user) return json({ done: [] as string[] });
  const rows = await q<{ lesson_id: string }>(
    "SELECT lesson_id FROM lesson_progress WHERE user_id = ?",
    [actor.user.id],
  );
  return json({ done: rows.map((r) => r.lesson_id) });
});

/** POST /api/academy/progress — mark a lesson done for the authenticated user. */
export const POST = route(async (req) => {
  const actor = await getActor(req);
  if (!actor.user) throw new HttpError(401, "auth_required", "يجب تسجيل الدخول لحفظ التقدم");
  const { lesson_id } = await readJson(req, PostBody);
  await run(
    "INSERT OR IGNORE INTO lesson_progress(user_id, lesson_id, done_at) VALUES (?, ?, ?)",
    [actor.user.id, lesson_id, new Date().toISOString()],
  );
  return json({ ok: true });
});
