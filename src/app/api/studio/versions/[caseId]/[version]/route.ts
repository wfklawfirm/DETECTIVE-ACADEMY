import { z } from "zod";
import { route } from "@/server/api";
import { getActor, requireRole } from "@/server/auth";
import { clientIpHash, HttpError, json, readJson } from "@/server/http";
import { getVersion, saveVersion } from "@/server/studio";

type Ctx = { params: Promise<{ caseId: string; version: string }> };
const ID = /^[a-z][a-z0-9_]{1,63}$/;
const Body = z.object({ core: z.unknown(), ui: z.unknown(), scoring: z.unknown() });

export const GET = route<Ctx>(async (req, ctx) => {
  requireRole(await getActor(req), ["editor", "reviewer", "admin"]);
  const { caseId, version } = await ctx.params;
  if (!ID.test(caseId)) throw new HttpError(404, "no_version", "غير موجود");
  const v = await getVersion(caseId, version);
  return json({ status: v.status, hash: v.content_hash, core: v.core, ui: v.ui, scoring: v.scoring, qa: v.qa, gates: v.gates });
}, { limit: 60, key: "studio" });

export const PUT = route<Ctx>(async (req, ctx) => {
  const b = await readJson(req, Body, 2_000_000);
  const u = requireRole(await getActor(req), ["editor", "admin"]);
  const { caseId, version } = await ctx.params;
  if (!ID.test(caseId)) throw new HttpError(404, "no_version", "غير موجود");
  return json(await saveVersion(u, caseId, version, b, clientIpHash(req)));
}, { limit: 30, key: "studio-save" });
