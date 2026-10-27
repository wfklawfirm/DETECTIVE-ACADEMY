import { route } from "@/server/api";
import { q1 } from "@/server/db";
import { HttpError, json } from "@/server/http";

export const GET = route<{ params: Promise<{ code: string }> }>(async (_req, ctx) => {
  const { code } = await ctx.params;
  if (!/^[A-Z0-9]{6,12}$/.test(code)) throw new HttpError(404, "no_ticket", "لا يوجد طلب مراجعة بهذا الرمز");
  const t = await q1<{ status: string; level: number | null; feedback_ar: string | null; created_at: string; reviewed_at: string | null }>(
    "SELECT status, level, feedback_ar, created_at, reviewed_at FROM review_tickets WHERE code = ?", [code]);
  if (!t) throw new HttpError(404, "no_ticket", "لا يوجد طلب مراجعة بهذا الرمز");
  return json({ ticket: t });
}, { limit: 60, key: "ticket" });
