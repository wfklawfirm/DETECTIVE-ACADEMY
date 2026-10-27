import { z } from "zod";
import { route } from "@/server/api";
import { getActor } from "@/server/auth";
import { run } from "@/server/db";
import { HttpError, json, readJson } from "@/server/http";

const Body = z.object({ gentle_hooks: z.boolean() });
export const POST = route(async (req) => {
  const b = await readJson(req, Body, 2_000);
  const actor = await getActor(req);
  if (!actor.user) throw new HttpError(401, "login_required", "يلزم تسجيل الدخول");
  await run("UPDATE users SET gentle_hooks = ? WHERE id = ?", [b.gentle_hooks ? 1 : 0, actor.user.id]);
  return json({ ok: true });
});
