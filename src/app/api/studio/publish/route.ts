import { z } from "zod";
import { route } from "@/server/api";
import { getActor, requireRole } from "@/server/auth";
import { clientIpHash, json, readJson } from "@/server/http";
import { publish } from "@/server/studio";

const Body = z.object({ case_id: z.string().regex(/^[a-z][a-z0-9_]{1,63}$/), version: z.string().max(20) });
export const POST = route(async (req) => {
  const b = await readJson(req, Body, 2_000);
  const u = requireRole(await getActor(req), ["admin"]);
  return json(await publish(u, b.case_id, b.version, clientIpHash(req)));
}, { limit: 10, key: "studio-publish" });
