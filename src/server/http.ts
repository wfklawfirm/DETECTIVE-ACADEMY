import { NextRequest, NextResponse } from "next/server";
import { z, ZodError } from "zod";
import { EngineError } from "../engine/state";
import { ipHash } from "./crypto";

export class HttpError extends Error {
  constructor(public status: number, public code: string, message: string) { super(message); }
}

export const json = (data: unknown, init: ResponseInit & { headers?: Record<string, string> } = {}) =>
  NextResponse.json(data, { ...init, headers: { "Cache-Control": "no-store", ...(init.headers ?? {}) } });

export function fail(e: unknown): NextResponse {
  if (e instanceof HttpError) return json({ error: e.code, message: e.message }, { status: e.status });
  if (e instanceof EngineError) return json({ error: e.code, message: e.message }, { status: 400 });
  if (e instanceof ZodError) return json({ error: "invalid_input", message: "مدخلات غير صالحة", issues: e.issues.slice(0, 5).map((i) => ({ path: i.path.join("."), message: i.message })) }, { status: 422 });
  // Never leak internals or PII in errors/logs.
  console.error("[athar] unexpected error:", e instanceof Error ? e.name + ": " + e.message : String(e));
  return json({ error: "internal", message: "حدث خطأ غير متوقع" }, { status: 500 });
}

export function clientIp(req: NextRequest): string {
  const xf = req.headers.get("x-forwarded-for");
  return (xf?.split(",")[0]?.trim() || req.headers.get("x-real-ip") || "0.0.0.0").slice(0, 64);
}
export const clientIpHash = (req: NextRequest) => ipHash(clientIp(req));

/** CSRF: mutating requests must be JSON and (when an Origin header exists) same-origin. */
export function assertMutation(req: NextRequest): void {
  const ct = req.headers.get("content-type") ?? "";
  if (!ct.includes("application/json")) throw new HttpError(415, "bad_content_type", "نوع المحتوى غير مدعوم");
  const origin = req.headers.get("origin");
  if (origin) {
    const host = req.headers.get("host");
    let oh = "";
    try { oh = new URL(origin).host; } catch { /* ignore */ }
    if (!host || oh !== host) throw new HttpError(403, "cross_origin", "طلب من أصل غير مسموح");
  }
}

export async function readJson<S extends z.ZodTypeAny>(req: NextRequest, schema: S, maxBytes = 400_000): Promise<z.infer<S>> {
  assertMutation(req);
  const text = await req.text();
  if (text.length > maxBytes) throw new HttpError(413, "too_large", "الطلب أكبر من الحد المسموح");
  let raw: unknown;
  try { raw = JSON.parse(text); } catch { throw new HttpError(400, "bad_json", "JSON غير صالح"); }
  return schema.parse(raw);
}
