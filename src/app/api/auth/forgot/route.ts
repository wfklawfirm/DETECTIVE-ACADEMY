import { randomBytes, createHash } from "node:crypto";
import { z } from "zod";
import { route } from "@/server/api";
import { clientIpHash, json, readJson } from "@/server/http";
import { q1, run } from "@/server/db";
import { rateLimit } from "@/server/ratelimit";

const Body = z.object({ email: z.string().max(254) });

export const POST = route(async (req) => {
  const b = await readJson(req, Body, 10_000);
  const ipH = clientIpHash(req);
  const rl = rateLimit(`forgot:${ipH}`, 5, 900_000);
  if (!rl.ok) return json({ ok: true }); // silently rate-limit

  const email = b.email.trim().toLowerCase();
  const user = await q1<{ id: string }>("SELECT id FROM users WHERE email = ? AND deleted_at IS NULL", [email]);

  if (!user) {
    // Do not leak whether email exists — just return ok
    return json({ ok: true });
  }

  const token = randomBytes(32).toString("hex");
  const tokenHash = createHash("sha256").update(token).digest("hex");
  const now = new Date();
  const expires = new Date(now.getTime() + 3_600_000); // 1 hour

  await run(
    "INSERT INTO password_resets(token_hash, user_id, created_at, expires_at) VALUES (?, ?, ?, ?)",
    [tokenHash, user.id, now.toISOString(), expires.toISOString()]
  );

  if (process.env.NODE_ENV !== "production") {
    return json({ ok: true, dev_token: token });
  }
  return json({ ok: true });
}, { limit: 20, key: "forgot" });
