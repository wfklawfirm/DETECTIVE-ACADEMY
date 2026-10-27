import { env } from "@/server/env";
import { z } from "zod";
import { route } from "@/server/api";
import { getActor } from "@/server/auth";
import { HttpError, json, readJson } from "@/server/http";
import { handlePlay, PlaySchema } from "@/server/play";
import { rateLimit } from "@/server/ratelimit";
import { clientIpHash } from "@/server/http";

const Body = z.object({ token: z.string().max(180_000).nullish(), req: PlaySchema });
const CaseId = /^[a-z][a-z0-9_]{1,63}$/;

export const POST = route<{ params: Promise<{ caseId: string }> }>(async (req, ctx) => {
  const { caseId } = await ctx.params;
  if (!CaseId.test(caseId)) throw new HttpError(404, "no_case", "القضية غير متاحة");
  const b = await readJson(req, Body, 250_000);
  const rl = rateLimit(`play:${clientIpHash(req)}`, env.playRate, 60_000);
  if (!rl.ok) throw new HttpError(429, "rate_limited", "طلبات كثيرة، تمهّل قليلاً");
  const actor = await getActor(req);
  return json(await handlePlay(actor, caseId, b.req, b.token));
}, { key: "playgate", limit: env.apiRate });
