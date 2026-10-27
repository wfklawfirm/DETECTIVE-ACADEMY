import { q1 } from "@/server/db";
import { json } from "@/server/http";

export async function GET() {
  try {
    await q1("SELECT 1 AS ok");
    return json({ ok: true });
  } catch {
    return json({ ok: false }, { status: 503 });
  }
}
