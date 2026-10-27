"use client";
// Browser-side helpers: JSON API calls and per-device storage (everything wrapped in try/catch: storage may be blocked).

export class ApiError extends Error {
  constructor(public status: number, public code: string, message: string) { super(message); }
}

export async function api<T = unknown>(path: string, body?: unknown, method?: "GET" | "POST" | "PUT"): Promise<T> {
  const m = method ?? (body === undefined ? "GET" : "POST");
  const res = await fetch(path, { method: m, headers: body === undefined ? undefined : { "content-type": "application/json" }, body: body === undefined ? undefined : JSON.stringify(body), credentials: "same-origin", cache: "no-store" });
  let j: unknown = null;
  try { j = await res.json(); } catch { /* empty */ }
  if (!res.ok) {
    const e = (j as { error?: { code?: string; message?: string } } | null)?.error;
    throw new ApiError(res.status, e?.code ?? "error", e?.message ?? "حدث خطأ غير متوقع، حاول مرة أخرى.");
  }
  return j as T;
}

export const ls = {
  get(k: string): string | null { try { return localStorage.getItem(k); } catch { return null; } },
  set(k: string, v: string) { try { localStorage.setItem(k, v); } catch { /* blocked */ } },
  del(k: string) { try { localStorage.removeItem(k); } catch { /* blocked */ } },
};
export const store = ls;

const rnd = () => Array.from(crypto.getRandomValues(new Uint8Array(9)), (b) => b.toString(36).padStart(2, "0")).join("").slice(0, 14);

export function deviceSeed(): string {
  let s = ls.get("athar.seed");
  if (!s || !/^[A-Za-z0-9_-]{4,64}$/.test(s)) { s = rnd(); ls.set("athar.seed", s); }
  return s;
}
export function nextEntry(): number { const n = Number(ls.get("athar.entry") ?? "0") + 1; ls.set("athar.entry", String(n)); return n; }
export function recentHooks(): string[] { try { return JSON.parse(ls.get("athar.recent") ?? "[]") as string[]; } catch { return []; } }
export function pushRecentHook(id: string) { ls.set("athar.recent", JSON.stringify([id, ...recentHooks().filter((x) => x !== id)].slice(0, 6))); }
export const gentleMode = () => ls.get("athar.gentle") === "1";
export const setGentle = (v: boolean) => (v ? ls.set("athar.gentle", "1") : ls.del("athar.gentle"));

export const getToken = (caseId: string) => ls.get(`athar.s.${caseId}`);
export const setToken = (caseId: string, t: string | null) => (t ? ls.set(`athar.s.${caseId}`, t) : undefined);
export const clearToken = (caseId: string) => ls.del(`athar.s.${caseId}`);
export function allTokens(): Record<string, string> {
  const out: Record<string, string> = {};
  try { for (let i = 0; i < localStorage.length; i++) { const k = localStorage.key(i)!; if (k.startsWith("athar.s.")) out[k.slice(8)] = localStorage.getItem(k)!; } } catch { /* blocked */ }
  return out;
}

export interface Me { kind: "account" | "device"; age_band: "13-15" | "16-17" | "18+" | null; preview_mode: boolean; user: { id: string; display_name: string | null; role: string; gentle_hooks: boolean } | null }
