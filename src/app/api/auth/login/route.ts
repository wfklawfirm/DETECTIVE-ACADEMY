import { cookies } from "next/headers";
import { z } from "zod";
import { route } from "@/server/api";
import { cookieOpts, login, SID_COOKIE } from "@/server/auth";
import { clientIpHash, json, readJson } from "@/server/http";

const Body = z.object({ email: z.string().max(254), password: z.string().max(200) });
export const POST = route(async (req) => {
  const b = await readJson(req, Body, 10_000);
  const { user, sid } = await login(b.email, b.password, clientIpHash(req));
  (await cookies()).set(SID_COOKIE, sid, cookieOpts(30 * 86400));
  return json({ user: { id: user.id, display_name: user.display_name, role: user.role } });
}, { limit: 40, key: "login" });
