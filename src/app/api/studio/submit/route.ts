import { z } from "zod";
import { route } from "@/server/api";
import { getActor, requireRole } from "@/server/auth";
import { audit } from "@/server/audit";
import { clientIpHash, json, readJson } from "@/server/http";
import { q1, run } from "@/server/db";

const Body = z.object({
  case_id: z.string().regex(/^[a-z][a-z0-9_]{1,63}$/),
  version: z.string().max(20),
});

/** POST /api/studio/submit — move a draft → in_review (editor or admin). */
export const POST = route(async (req) => {
  const b = await readJson(req, Body, 2_000);
  const u = requireRole(await getActor(req), ["editor", "admin"]);

  const row = await q1<{ status: string }>(
    "SELECT status FROM case_versions WHERE case_id = ? AND version = ?",
    [b.case_id, b.version]
  );
  if (!row) return json({ error: "not_found", message: "النسخة غير موجودة" }, { status: 404 });
  if (row.status !== "draft") return json({ error: "wrong_status", message: "يمكن إرسال المسودات فقط للمراجعة" }, { status: 409 });

  await run(
    "UPDATE case_versions SET status = 'in_review' WHERE case_id = ? AND version = ?",
    [b.case_id, b.version]
  );
  await audit(u.id, "case.submit_for_review", `${b.case_id}@${b.version}`, {}, clientIpHash(req));
  return json({ ok: true });
}, { limit: 20, key: "studio-submit" });
