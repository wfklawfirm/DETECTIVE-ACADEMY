import { z } from "zod";
import { route } from "@/server/api";
import { getActor, requireRole } from "@/server/auth";
import { clientIpHash, json, readJson } from "@/server/http";
import { listTickets, reviewTicket } from "@/server/studio";

export const GET = route(async (req) => {
  requireRole(await getActor(req), ["reviewer", "admin"]);
  const s = new URL(req.url).searchParams.get("status");
  return json({ tickets: await listTickets(s === "reviewed" ? "reviewed" : "pending") });
}, { limit: 60, key: "studio" });

const Body = z.object({ code: z.string().regex(/^[A-Z0-9]{6,12}$/), level: z.number().int().min(0).max(4), feedback: z.string().min(3).max(2000) });
export const POST = route(async (req) => {
  const b = await readJson(req, Body, 6_000);
  const u = requireRole(await getActor(req), ["reviewer", "admin"]);
  await reviewTicket(u, b.code, b.level, b.feedback, clientIpHash(req));
  return json({ ok: true });
}, { limit: 60, key: "studio" });
