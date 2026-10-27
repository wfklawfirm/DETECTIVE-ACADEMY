import { NextRequest, NextResponse } from "next/server";
import { clientIpHash, fail, HttpError } from "./http";
import { env } from "./env";
import { rateLimit } from "./ratelimit";

type Handler<C> = (req: NextRequest, ctx: C) => Promise<Response>;

/** Wrap a route handler: global per-IP limiter + uniform error mapping (no stack traces / PII leak). */
export function route<C = unknown>(fn: Handler<C>, opts: { limit?: number; windowMs?: number; key?: string } = {}) {
  return async (req: NextRequest, ctx: C): Promise<Response> => {
    try {
      const rl = rateLimit(`api:${opts.key ?? "all"}:${clientIpHash(req)}`, opts.limit ?? env.apiRate, opts.windowMs ?? 60_000);
      if (!rl.ok) throw new HttpError(429, "rate_limited", "طلبات كثيرة، حاول بعد قليل");
      return await fn(req, ctx);
    } catch (e) {
      return fail(e) as NextResponse;
    }
  };
}
