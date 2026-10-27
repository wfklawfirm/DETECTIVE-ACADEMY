import { cookies } from "next/headers";
import { NextRequest } from "next/server";
import { hashPassword, randomId, sha256, verifyPassword } from "./crypto";
import { q1, run } from "./db";
import { env } from "./env";
import { HttpError } from "./http";
import { rateLimit } from "./ratelimit";
import { audit } from "./audit";

export type Role = "player" | "editor" | "reviewer" | "admin";
export interface UserRow { id: string; email: string; display_name: string | null; role: Role; adult_confirmed: number; gentle_hooks: number; created_at: string }
export type AgeBand = "13-15" | "16-17" | "18+";

export const SID_COOKIE = "athar_sid";
export const AGE_COOKIE = "athar_age";
const SESSION_DAYS = 30;

export const cookieOpts = (maxAgeS: number) => ({ httpOnly: true, sameSite: "lax" as const, secure: env.secureCookies, path: "/", maxAge: maxAgeS });

const EMAIL_RE = /^[^\s@]{1,64}@[^\s@]{1,190}\.[^\s@]{2,}$/;
const COMMON = new Set(["password123", "1234567890", "qwertyuiop", "0123456789", "password1234", "iloveyou123", "athar123456"]);

export async function register(input: { email: string; password: string; display_name?: string; adult: boolean }, ipH: string): Promise<UserRow> {
  const rl = rateLimit(`reg:${ipH}`, 5, 3_600_000);
  if (!rl.ok) throw new HttpError(429, "rate_limited", "محاولات كثيرة، حاول لاحقاً");
  if (!input.adult) throw new HttpError(403, "adult_only", "الحسابات في هذه النسخة للبالغين (18 عاماً فأكثر). يمكنك اللعب كضيف دون حساب.");
  const email = input.email.trim().toLowerCase();
  if (!EMAIL_RE.test(email)) throw new HttpError(422, "bad_email", "بريد إلكتروني غير صالح");
  if (input.password.length < 10 || input.password.length > 200) throw new HttpError(422, "weak_password", "كلمة المرور يجب أن تكون 10 أحرف على الأقل");
  if (COMMON.has(input.password.toLowerCase()) || (email.split("@")[0]!.length >= 4 && input.password.toLowerCase().includes(email.split("@")[0]!))) throw new HttpError(422, "weak_password", "كلمة مرور ضعيفة أو متوقعة");
  if (await q1("SELECT 1 AS x FROM users WHERE email = ? AND deleted_at IS NULL", [email])) throw new HttpError(409, "exists", "هذا البريد مسجّل مسبقاً");
  const id = randomId(12);
  const name = input.display_name?.trim().slice(0, 40) || null;
  await run("INSERT INTO users(id, email, pass_hash, display_name, role, adult_confirmed, created_at) VALUES (?,?,?,?,?,?,?)",
    [id, email, await hashPassword(input.password), name, "player", 1, new Date().toISOString()]);
  await audit(id, "user.register", id, null, ipH);
  return (await q1<UserRow>("SELECT id,email,display_name,role,adult_confirmed,gentle_hooks,created_at FROM users WHERE id = ?", [id]))!;
}

export async function login(emailIn: string, password: string, ipH: string): Promise<{ user: UserRow; sid: string }> {
  const email = emailIn.trim().toLowerCase();
  const rl = rateLimit(`login:${ipH}:${email}`, 8, 900_000);
  if (!rl.ok) throw new HttpError(429, "rate_limited", `محاولات كثيرة، حاول بعد ${Math.ceil(rl.retryAfterS / 60)} دقيقة`);
  const row = await q1<UserRow & { pass_hash: string; deleted_at: string | null }>("SELECT * FROM users WHERE email = ?", [email]);
  // constant-ish work even if the user does not exist
  const ok = row && !row.deleted_at ? await verifyPassword(password, row.pass_hash) : (await verifyPassword(password, "s1$16384$AAAAAAAAAAAAAAAAAAAAAA$AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"), false);
  if (!row || !ok) { await audit(null, "user.login_failed", null, null, ipH); throw new HttpError(401, "bad_credentials", "البريد أو كلمة المرور غير صحيحة"); }
  const sid = randomId(32);
  const exp = new Date(Date.now() + SESSION_DAYS * 86_400_000).toISOString();
  await run("INSERT INTO sessions(id_hash, user_id, created_at, expires_at, ip_hash) VALUES (?,?,?,?,?)", [sha256(sid), row.id, new Date().toISOString(), exp, ipH]);
  await audit(row.id, "user.login", row.id, null, ipH);
  const { pass_hash: _p, deleted_at: _d, ...user } = row;
  void _p; void _d;
  return { user, sid };
}

export async function userFromSid(sid: string | undefined): Promise<UserRow | null> {
  if (!sid || sid.length < 20 || sid.length > 100) return null;
  const r = await q1<UserRow & { expires_at: string }>(
    "SELECT u.id,u.email,u.display_name,u.role,u.adult_confirmed,u.gentle_hooks,u.created_at, s.expires_at FROM sessions s JOIN users u ON u.id = s.user_id WHERE s.id_hash = ? AND u.deleted_at IS NULL", [sha256(sid)]);
  if (!r) return null;
  if (r.expires_at < new Date().toISOString()) { await run("DELETE FROM sessions WHERE id_hash = ?", [sha256(sid)]); return null; }
  const { expires_at: _e, ...u } = r;
  void _e;
  return u;
}

export async function logout(sid: string | undefined) {
  if (sid) await run("DELETE FROM sessions WHERE id_hash = ?", [sha256(sid)]);
}

/** Account deletion = erase personal data. Play states cascade; tickets/reports keep only anonymised content. */
export async function deleteAccount(userId: string, ipH: string) {
  await run("UPDATE review_tickets SET user_id = NULL WHERE user_id = ?", [userId]);
  await run("UPDATE content_reports SET user_id = NULL WHERE user_id = ?", [userId]);
  await run("DELETE FROM users WHERE id = ?", [userId]); // cascades sessions, play_states, hook_events
  await audit(null, "user.delete", sha256(userId).slice(0, 12), null, ipH);
}

export interface Actor { kind: "account" | "device"; user: UserRow | null; ageBand: AgeBand | null }

/** Resolve who is calling. Accounts are adults; device-mode actors carry only a coarse age band (cookie) and no personal data. */
export async function getActor(req: NextRequest): Promise<Actor> {
  const sid = req.cookies.get(SID_COOKIE)?.value;
  const user = await userFromSid(sid);
  if (user) return { kind: "account", user, ageBand: "18+" };
  const band = req.cookies.get(AGE_COOKIE)?.value;
  return { kind: "device", user: null, ageBand: band === "16-17" || band === "18+" || band === "13-15" ? band : null };
}
export async function getActorFromCookies(): Promise<Actor> {
  const c = await cookies();
  const user = await userFromSid(c.get(SID_COOKIE)?.value);
  if (user) return { kind: "account", user, ageBand: "18+" };
  const band = c.get(AGE_COOKIE)?.value;
  return { kind: "device", user: null, ageBand: band === "16-17" || band === "18+" || band === "13-15" ? band : null };
}

export function requireRole(actor: Actor, roles: Role[]): UserRow {
  if (!actor.user) throw new HttpError(401, "login_required", "يلزم تسجيل الدخول");
  if (!roles.includes(actor.user.role)) throw new HttpError(403, "forbidden", "لا تملك الصلاحية لهذا الإجراء");
  return actor.user;
}

export async function ensureAdmin(): Promise<string | null> {
  if (!env.adminEmail || !env.adminPassword) return null;
  const email = env.adminEmail.toLowerCase();
  const ex = await q1<{ id: string }>("SELECT id FROM users WHERE email = ?", [email]);
  if (ex) return null;
  const id = randomId(12);
  await run("INSERT INTO users(id, email, pass_hash, display_name, role, adult_confirmed, created_at) VALUES (?,?,?,?,?,?,?)",
    [id, email, await hashPassword(env.adminPassword), "مدير النظام", "admin", 1, new Date().toISOString()]);
  return email;
}

export async function verifyPasswordFor(userId: string, password: string): Promise<boolean> {
  const row = await q1<{ pass_hash: string }>("SELECT pass_hash FROM users WHERE id = ?", [userId]);
  return row ? verifyPassword(password, row.pass_hash) : false;
}
