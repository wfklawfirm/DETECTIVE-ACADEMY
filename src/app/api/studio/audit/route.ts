import { route } from "@/server/api";
import { getActor, requireRole } from "@/server/auth";
import { q } from "@/server/db";
import { json } from "@/server/http";

export const GET = route(async (req) => {
  requireRole(await getActor(req), ["admin"]);
  return json({ audit: await q("SELECT actor_id, action, target, detail, at AS created_at FROM audit_log ORDER BY id DESC LIMIT 200") });
}, { limit: 30, key: "studio" });
