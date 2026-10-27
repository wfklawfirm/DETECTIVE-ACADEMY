import { z } from "zod";
import { route } from "@/server/api";
import { getActor } from "@/server/auth";
import { run } from "@/server/db";
import { json, readJson } from "@/server/http";

const Body = z.object({ kind: z.enum(["safety", "rights", "error", "other"]), case_id: z.string().regex(/^[a-z][a-z0-9_]{1,63}$/).optional(), body: z.string().min(5).max(2000) });
export const POST = route(async (req) => {
  const b = await readJson(req, Body, 6_000);
  const a = await getActor(req);
  await run("INSERT INTO content_reports(user_id, case_id, kind, body, created_at) VALUES (?,?,?,?,?)", [a.user?.id ?? null, b.case_id ?? null, b.kind, b.body, new Date().toISOString()]);
  return json({ ok: true });
}, { limit: 10, key: "report" });
