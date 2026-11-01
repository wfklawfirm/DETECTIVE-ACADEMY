import { createHash } from "node:crypto";
import { z } from "zod";
import { route } from "@/server/api";
import { clientIpHash, json, readJson } from "@/server/http";
import { q1, run } from "@/server/db";
import { hashPassword } from "@/server/crypto";
import { HttpError } from "@/server/http";
import { rateLimit } from "@/server/ratelimit";

const Body = z.object({
  token: z.string().min(10).max(200),
  password: z.string().min(10).max(200),
});

export const POST = route(async (req) => {
  const b = await readJson(req, Body, 10_000);
  const ipH = clientIpHash(req);
  const rl = rateLimit(`reset:${ipH}`, 10, 900_000);
  if (!rl.ok) throw new HttpError(429, "rate_limited", "محاولات كثيرة، حاول لاحقاً");

  const tokenHash = createHash("sha256").update(b.token).digest("hex");
  const row = await q1<{ token_hash: string; user_id: string; expires_at: string; used_at: string | null }>(
    "SELECT token_hash, user_id, expires_at, used_at FROM password_resets WHERE token_hash = ?",
    [tokenHash]
  );

  if (!row) throw new HttpError(400, "invalid_token", "الرابط غير صالح أو منتهي الصلاحية");
  if (row.used_at) throw new HttpError(400, "token_used", "تم استخدام هذا الرابط مسبقاً");
  if (row.expires_at < new Date().toISOString()) throw new HttpError(400, "token_expired", "انتهت صلاحية الرابط، أعد طلب استرجاع كلمة المرور");

  const passHash = await hashPassword(b.password);
  await run("UPDATE users SET pass_hash = ? WHERE id = ?", [passHash, row.user_id]);
  await run("UPDATE password_resets SET used_at = ? WHERE token_hash = ?", [new Date().toISOString(), tokenHash]);

  return json({ ok: true });
}, { limit: 10, key: "reset" });
