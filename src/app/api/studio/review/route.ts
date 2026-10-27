import { z } from "zod";
import { route } from "@/server/api";
import { getActor, requireRole } from "@/server/auth";
import { ROLES } from "@/server/content";
import { clientIpHash, json, readJson } from "@/server/http";
import { addReview } from "@/server/studio";

const Body = z.object({ case_id: z.string().regex(/^[a-z][a-z0-9_]{1,63}$/), version: z.string().max(20), role: z.enum(ROLES), status: z.enum(["pending", "changes_requested", "approved"]), notes: z.string().max(2000).optional() });
export const POST = route(async (req) => {
  const b = await readJson(req, Body, 8_000);
  const u = requireRole(await getActor(req), ["reviewer", "admin"]);
  return json({ gates: await addReview(u, b.case_id, b.version, b.role, b.status, b.notes, clientIpHash(req)) });
}, { limit: 30, key: "studio-review" });
