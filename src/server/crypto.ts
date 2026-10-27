import { createHash, createHmac, randomBytes, scrypt as scryptCb, timingSafeEqual } from "node:crypto";
import { deflateRawSync, inflateRawSync } from "node:zlib";
import { promisify } from "node:util";
import { env } from "./env";

const scrypt = promisify(scryptCb) as (pw: string, salt: Buffer, len: number, opts: { N: number; r: number; p: number; maxmem: number }) => Promise<Buffer>;

export const sha256 = (s: string) => createHash("sha256").update(s).digest("hex");
export const randomId = (bytes = 16) => randomBytes(bytes).toString("base64url");

const b64u = (b: Buffer) => b.toString("base64url");
const mac = (payload: string, purpose: string) => createHmac("sha256", env.secret).update(`${purpose}\n${payload}`).digest();

/** Salted scrypt: "s1$N$salt$hash" */
export async function hashPassword(pw: string): Promise<string> {
  const salt = randomBytes(16);
  const N = 16384;
  const h = await scrypt(pw, salt, 32, { N, r: 8, p: 1, maxmem: 64 * 1024 * 1024 });
  return `s1$${N}$${b64u(salt)}$${b64u(h)}`;
}
export async function verifyPassword(pw: string, stored: string): Promise<boolean> {
  const [v, n, salt, hash] = stored.split("$");
  if (v !== "s1" || !n || !salt || !hash) return false;
  const h = await scrypt(pw, Buffer.from(salt, "base64url"), 32, { N: Number(n), r: 8, p: 1, maxmem: 64 * 1024 * 1024 });
  const want = Buffer.from(hash, "base64url");
  return want.length === h.length && timingSafeEqual(want, h);
}

/** Sign an arbitrary JSON object into a compact, tamper-evident token: base64url(deflate(json)).hmac */
export function signToken(obj: unknown, purpose: string): string {
  const payload = b64u(deflateRawSync(Buffer.from(JSON.stringify(obj), "utf8")));
  return `${payload}.${b64u(mac(payload, purpose))}`;
}
export function verifyToken<T>(token: string, purpose: string, maxBytes = 200_000): T | null {
  if (token.length > maxBytes) return null;
  const i = token.lastIndexOf(".");
  if (i < 1) return null;
  const payload = token.slice(0, i);
  const sig = Buffer.from(token.slice(i + 1), "base64url");
  const want = mac(payload, purpose);
  if (sig.length !== want.length || !timingSafeEqual(sig, want)) return null;
  try {
    return JSON.parse(inflateRawSync(Buffer.from(payload, "base64url"), { maxOutputLength: 2_000_000 }).toString("utf8")) as T;
  } catch {
    return null;
  }
}

/** Privacy: we only ever store a salted hash of the IP, never the address. */
export const ipHash = (ip: string) => sha256(`${env.secret}|ip|${ip}`).slice(0, 24);
