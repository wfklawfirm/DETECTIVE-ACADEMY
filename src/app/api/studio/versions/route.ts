import { route } from "@/server/api";
import { getActor, requireRole } from "@/server/auth";
import { json } from "@/server/http";
import { listVersions } from "@/server/studio";

export const GET = route(async (req) => {
  requireRole(await getActor(req), ["editor", "reviewer", "admin"]);
  return json({ versions: await listVersions() });
}, { limit: 60, key: "studio" });
