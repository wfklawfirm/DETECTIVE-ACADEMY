import { route } from "@/server/api";
import { getActor } from "@/server/auth";
import { env } from "@/server/env";
import { json } from "@/server/http";

export const GET = route(async (req) => {
  const a = await getActor(req);
  return json({
    kind: a.kind, age_band: a.ageBand, preview_mode: env.allowPreview,
    user: a.user ? { id: a.user.id, display_name: a.user.display_name, role: a.user.role, gentle_hooks: !!a.user.gentle_hooks } : null,
  });
});
