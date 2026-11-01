import { z } from "zod";
import { route } from "@/server/api";
import { getActor, requireRole } from "@/server/auth";
import { audit } from "@/server/audit";
import { clientIpHash, json, readJson } from "@/server/http";
import { q1, run } from "@/server/db";

const ALLOWED_FIELDS = new Set(["cover.title_ar", "cover.subtitle_ar", "cover.hook_ar", "cover.difficulty", "cover.setting_ar"]);

function setPath(obj: Record<string, unknown>, path: string, value: unknown): void {
  const parts = path.split(".");
  let cur: Record<string, unknown> = obj;
  for (let i = 0; i < parts.length - 1; i++) {
    const key = parts[i]!;
    if (typeof cur[key] !== "object" || cur[key] === null) cur[key] = {};
    cur = cur[key] as Record<string, unknown>;
  }
  cur[parts[parts.length - 1]!] = value;
}

function bumpVersion(v: string): string {
  // expects "v1.0" or "1.0" or "1.0.0"
  const m = v.match(/^(v?)(\d+)\.(\d+)(\.(\d+))?$/);
  if (!m) return v;
  const prefix = m[1] ?? "";
  const major = m[2] ?? "1";
  const minor = parseInt(m[3] ?? "0", 10);
  const patch = m[5] !== undefined ? `.${m[5]}` : "";
  return `${prefix}${major}.${minor + 1}${patch}`;
}

export const GET = route(async (req) => {
  requireRole(await getActor(req), ["editor", "admin"]);
  const caseId = new URL(req.url).searchParams.get("case_id");
  if (!caseId) return json({ error: "missing_case_id", message: "case_id مطلوب" }, { status: 422 });
  const row = await q1<{ case_id: string; version: string; ui_json: string; core_json: string; status: string }>(
    "SELECT case_id, version, ui_json, core_json, status FROM case_versions WHERE case_id = ? AND status = 'draft' ORDER BY created_at DESC LIMIT 1",
    [caseId]
  );
  if (!row) return json({ error: "not_found", message: "لا توجد مسودة لهذه القضية" }, { status: 404 });
  return json({ case_id: row.case_id, version: row.version, ui: JSON.parse(row.ui_json), core: JSON.parse(row.core_json) });
}, { limit: 120, key: "studio-draft-get" });

const PatchBody = z.object({
  case_id: z.string().min(1).max(80),
  field: z.string().refine((f) => ALLOWED_FIELDS.has(f), { message: "حقل غير مسموح به" }),
  value: z.union([z.string().max(500), z.number()]),
});

export const PATCH = route(async (req) => {
  const actor = await getActor(req);
  const user = requireRole(actor, ["editor", "admin"]);
  const b = await readJson(req, PatchBody, 4_000);

  const row = await q1<{ version: string; ui_json: string; core_json: string; scoring_json: string; content_hash: string }>(
    "SELECT version, ui_json, core_json, scoring_json, content_hash FROM case_versions WHERE case_id = ? AND status = 'draft' ORDER BY created_at DESC LIMIT 1",
    [b.case_id]
  );
  if (!row) return json({ error: "not_found", message: "لا توجد مسودة لهذه القضية" }, { status: 404 });

  const ui = JSON.parse(row.ui_json) as Record<string, unknown>;
  setPath(ui, b.field, b.value);
  const newVersion = bumpVersion(row.version);

  await run(
    "UPDATE case_versions SET ui_json = ?, version = ?, status = 'draft' WHERE case_id = ? AND version = ?",
    [JSON.stringify(ui), newVersion, b.case_id, row.version]
  );
  await audit(user.id, "case.edit_field", `${b.case_id}@${newVersion}`, { field: b.field, value: b.value }, clientIpHash(req));

  return json({ ok: true, version: newVersion });
}, { limit: 30, key: "studio-draft-patch" });
