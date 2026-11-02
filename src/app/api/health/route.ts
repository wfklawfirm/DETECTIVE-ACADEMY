import { q1 } from "@/server/db";
import { env } from "@/server/env";
import { json } from "@/server/http";

export async function GET() {
  try {
    await q1("SELECT 1 AS ok");
    // Reports only the storage class, never the URL or credentials.
    return json({ ok: true, storage: env.dbEphemeral ? "ephemeral" : "persistent" });
  } catch {
    return json({ ok: false }, { status: 503 });
  }
}
