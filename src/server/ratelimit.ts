// Fixed-window in-memory limiter (single-instance). For multi-instance deployments replace the store (see docs/DEPLOYMENT.md).
type Bucket = { n: number; reset: number };
const store = new Map<string, Bucket>();

export function rateLimit(key: string, limit: number, windowMs: number, now = Date.now()): { ok: boolean; retryAfterS: number } {
  const b = store.get(key);
  if (!b || b.reset <= now) {
    store.set(key, { n: 1, reset: now + windowMs });
    if (store.size > 20_000) for (const [k, v] of store) if (v.reset <= now) store.delete(k);
    return { ok: true, retryAfterS: 0 };
  }
  b.n += 1;
  return b.n <= limit ? { ok: true, retryAfterS: 0 } : { ok: false, retryAfterS: Math.ceil((b.reset - now) / 1000) };
}
export const _resetRateLimits = () => store.clear();
