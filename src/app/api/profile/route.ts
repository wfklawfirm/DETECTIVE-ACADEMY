import { z } from "zod";
import { route } from "@/server/api";
import { getActor } from "@/server/auth";
import { json, readJson } from "@/server/http";
import { skillProfile } from "@/server/progress";

const Body = z.object({ tokens: z.record(z.string().max(64), z.string().max(180_000)).optional() });
export const POST = route(async (req) => {
  const b = await readJson(req, Body, 3_000_000);
  return json(await skillProfile(await getActor(req), b.tokens));
});
