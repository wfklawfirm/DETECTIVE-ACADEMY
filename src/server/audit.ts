import { run } from "./db";

/** Audit trail: who did what. No message bodies, no addresses (only a salted IP hash). */
export async function audit(actorId: string | null, action: string, target: string | null, detail: unknown, ipH: string | null) {
  try {
    await run("INSERT INTO audit_log(at, actor_id, action, target, detail, ip_hash) VALUES (?,?,?,?,?,?)",
      [new Date().toISOString(), actorId, action, target, detail == null ? null : JSON.stringify(detail).slice(0, 2000), ipH]);
  } catch (e) {
    console.error("[athar] audit failed", e instanceof Error ? e.message : e);
  }
}
