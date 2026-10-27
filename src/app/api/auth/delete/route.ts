import { cookies } from "next/headers";
import { z } from "zod";
import { route } from "@/server/api";
import { deleteAccount, getActor, SID_COOKIE, verifyPasswordFor } from "@/server/auth";
import { clientIpHash, HttpError, json, readJson } from "@/server/http";

const Body = z.object({ password: z.string().max(200), confirm: z.literal(true) });
export const POST = route(async (req) => {
  const b = await readJson(req, Body, 5_000);
  const actor = await getActor(req);
  if (!actor.user) throw new HttpError(401, "login_required", "يلزم تسجيل الدخول");
  if (!(await verifyPasswordFor(actor.user.id, b.password))) throw new HttpError(403, "bad_password", "كلمة المرور غير صحيحة");
  await deleteAccount(actor.user.id, clientIpHash(req));
  (await cookies()).delete(SID_COOKIE);
  return json({ ok: true });
}, { limit: 10, key: "delete" });
