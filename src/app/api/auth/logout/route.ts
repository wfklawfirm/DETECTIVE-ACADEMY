import { cookies } from "next/headers";
import { route } from "@/server/api";
import { logout, SID_COOKIE } from "@/server/auth";
import { assertMutation, json } from "@/server/http";

export const POST = route(async (req) => {
  assertMutation(req);
  const c = await cookies();
  await logout(c.get(SID_COOKIE)?.value);
  c.delete(SID_COOKIE);
  return json({ ok: true });
});
