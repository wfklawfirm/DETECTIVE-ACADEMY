import { cookies } from "next/headers";
import { z } from "zod";
import { route } from "@/server/api";
import { AGE_COOKIE, cookieOpts } from "@/server/auth";
import { json, readJson } from "@/server/http";

const Body = z.object({ band: z.enum(["16-17", "18+", "under16"]) });
/** Soft age gate: stores only a coarse band in a cookie (no birth date, no identity). Under-16 is told the platform is not yet for them and nothing is stored. */
export const POST = route(async (req) => {
  const b = await readJson(req, Body, 1_000);
  if (b.band === "under16") return json({ allowed: false, message: "Detective Academy موجّهة حالياً لمن هم في السادسة عشرة فما فوق. نعمل على نسخة مناسبة لعمرك." });
  (await cookies()).set(AGE_COOKIE, b.band, { ...cookieOpts(180 * 86400), httpOnly: true });
  return json({ allowed: true, band: b.band });
});
