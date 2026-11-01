import { z } from "zod";
import { route } from "@/server/api";
import { getActor } from "@/server/auth";
import { q1, run } from "@/server/db";
import { HttpError, json, readJson } from "@/server/http";
import { hashPassword, verifyPassword } from "@/server/crypto";

const Body = z.object({
  display_name: z.string().max(40).optional(),
  current_password: z.string().max(200).optional(),
  new_password: z.string().min(10).max(200).optional(),
}).refine(
  (b) => b.display_name !== undefined || (b.current_password && b.new_password),
  "يجب تحديد اسم جديد أو كلمة مرور جديدة"
);

export const PATCH = route(async (req) => {
  const actor = await getActor(req);
  if (!actor.user) throw new HttpError(401, "auth_required", "يجب تسجيل الدخول");
  const b = await readJson(req, Body, 4_000);

  if (b.display_name !== undefined) {
    const name = b.display_name.trim() || null;
    await run("UPDATE users SET display_name = ? WHERE id = ?", [name, actor.user.id]);
  }

  if (b.current_password && b.new_password) {
    const row = await q1<{ pass_hash: string }>(
      "SELECT pass_hash FROM users WHERE id = ?", [actor.user.id]
    );
    if (!row) throw new HttpError(404, "not_found", "الحساب غير موجود");
    const ok = await verifyPassword(b.current_password, row.pass_hash);
    if (!ok) throw new HttpError(403, "wrong_password", "كلمة المرور الحالية غير صحيحة");
    const newHash = await hashPassword(b.new_password);
    await run("UPDATE users SET pass_hash = ? WHERE id = ?", [newHash, actor.user.id]);
  }

  return json({ ok: true });
});
