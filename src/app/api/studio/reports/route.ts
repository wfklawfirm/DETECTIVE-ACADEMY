import { route } from "@/server/api";
import { getActor, requireRole } from "@/server/auth";
import { q } from "@/server/db";
import { json } from "@/server/http";

export const GET = route(async (req) => {
  requireRole(await getActor(req), ["reviewer", "admin"]);
  return json({ reports: await q("SELECT id, case_id, kind, body, created_at FROM content_reports ORDER BY created_at DESC LIMIT 100") });
}, { limit: 60, key: "studio" });
