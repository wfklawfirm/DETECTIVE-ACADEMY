import { readFileSync } from "node:fs";
import { crossCheck, ScoringSchema, UiSchema } from "../engine/sidecars";
import { staticLeakScan, type LeakFinding } from "../engine/leak";
import type { CaseFile } from "../engine/types";
import type { CaseUi, ScoringSpec } from "../engine/ui-types";
import { contentHash, qaCase, schemaErrors, type QAReport } from "../engine/validate";
import type { UserRow } from "./auth";
import { audit } from "./audit";
import { gateState, ROLES, type GateRole } from "./content";
import { q, q1, run } from "./db";
import { HttpError } from "./http";

export interface QaBundle { core: QAReport; sidecar_errors: string[]; leaks: LeakFinding[]; ok: boolean; checked_at: string; content_hash: string }

export async function runQa(core: CaseFile, ui: CaseUi, sc: ScoringSpec): Promise<QaBundle> {
  const coreQa = qaCase(core);
  const sidecar_errors: string[] = [];
  const u = UiSchema.safeParse(ui);
  if (!u.success) sidecar_errors.push(...u.error.issues.slice(0, 20).map((i) => `ui.${i.path.join(".")}: ${i.message}`));
  const s = ScoringSchema.safeParse(sc);
  if (!s.success) sidecar_errors.push(...s.error.issues.slice(0, 20).map((i) => `scoring.${i.path.join(".")}: ${i.message}`));
  let leaks: LeakFinding[] = [];
  if (coreQa.ok && u.success && s.success) {
    sidecar_errors.push(...crossCheck(core, ui, sc));
    const hooks = (JSON.parse(readFileSync("content/hooks/global.json", "utf8")) as { hooks: { id: string; text_ar: string }[] }).hooks;
    leaks = staticLeakScan(core, ui, hooks.map((h) => ({ where: `hook:${h.id}`, text: h.text_ar })));
  }
  return { core: coreQa, sidecar_errors, leaks, ok: coreQa.ok && sidecar_errors.length === 0 && leaks.length === 0, checked_at: new Date().toISOString(), content_hash: coreQa.ok ? await contentHash(core) : "" };
}

export async function listVersions() {
  const rows = await q<{ case_id: string; version: string; status: string; content_hash: string; created_by: string | null; created_at: string; qa_json: string | null }>(
    "SELECT case_id, version, status, content_hash, created_by, created_at, qa_json FROM case_versions ORDER BY case_id, created_at DESC");
  const out = [];
  for (const r of rows) {
    const gates = await gateState(r.case_id, r.version, r.content_hash);
    const qa = r.qa_json ? (JSON.parse(r.qa_json) as { ok?: boolean }) : null;
    out.push({ case_id: r.case_id, version: r.version, status: r.status, created_by: r.created_by, created_at: r.created_at, content_hash: r.content_hash, qa_ok: qa?.ok ?? null, gates: gates.roles, all_approved: gates.all_approved });
  }
  return out;
}

export async function getVersion(caseId: string, version: string) {
  const r = await q1<{ core_json: string; ui_json: string; scoring_json: string; status: string; content_hash: string; qa_json: string | null; created_by: string | null }>(
    "SELECT core_json, ui_json, scoring_json, status, content_hash, qa_json, created_by FROM case_versions WHERE case_id = ? AND version = ?", [caseId, version]);
  if (!r) throw new HttpError(404, "no_version", "إصدار غير موجود");
  return { ...r, core: JSON.parse(r.core_json), ui: JSON.parse(r.ui_json), scoring: JSON.parse(r.scoring_json), qa: r.qa_json ? JSON.parse(r.qa_json) : null, gates: await gateState(caseId, version, r.content_hash) };
}

export async function saveVersion(user: UserRow, caseId: string, version: string, triplet: { core: unknown; ui: unknown; scoring: unknown }, ipH: string) {
  if (!/^\d+\.\d+\.\d+$/.test(version)) throw new HttpError(422, "bad_version", "رقم الإصدار يجب أن يكون x.y.z");
  const errs = schemaErrors(triplet.core);
  if (errs.length) throw new HttpError(422, "schema", `القضية لا تطابق المخطط: ${errs.slice(0, 5).join(" | ")}`);
  const core = triplet.core as CaseFile;
  if (core.case_id !== caseId || core.case_version !== version) throw new HttpError(422, "id_mismatch", "معرّف القضية أو الإصدار داخل الملف لا يطابق المسار");
  const existing = await q1<{ status: string }>("SELECT status FROM case_versions WHERE case_id = ? AND version = ?", [caseId, version]);
  if (existing && !["draft", "in_review"].includes(existing.status)) throw new HttpError(409, "locked", "هذا الإصدار معتمد أو منشور؛ أنشئ إصداراً جديداً");
  const qa = await runQa(core, triplet.ui as CaseUi, triplet.scoring as ScoringSpec);
  const hash = qa.content_hash || (await contentHash(core));
  const now = new Date().toISOString();
  if (existing) {
    await run("UPDATE case_versions SET core_json=?, ui_json=?, scoring_json=?, content_hash=?, qa_json=?, status='draft' WHERE case_id=? AND version=?",
      [JSON.stringify(core), JSON.stringify(triplet.ui), JSON.stringify(triplet.scoring), hash, JSON.stringify(qa), caseId, version]);
  } else {
    await run("INSERT INTO case_versions(case_id, version, content_hash, status, core_json, ui_json, scoring_json, qa_json, created_by, created_at) VALUES (?,?,?,?,?,?,?,?,?,?)",
      [caseId, version, hash, "draft", JSON.stringify(core), JSON.stringify(triplet.ui), JSON.stringify(triplet.scoring), JSON.stringify(qa), user.id, now]);
  }
  await audit(user.id, "case.save", `${caseId}@${version}`, { hash, qa_ok: qa.ok }, ipH);
  return { qa, hash };
}

export async function addReview(user: UserRow, caseId: string, version: string, role: GateRole, status: "pending" | "changes_requested" | "approved", notes: string | undefined, ipH: string) {
  if (!ROLES.includes(role)) throw new HttpError(422, "bad_role", "دور مراجعة غير معروف");
  const v = await q1<{ content_hash: string; created_by: string | null; status: string }>("SELECT content_hash, created_by, status FROM case_versions WHERE case_id = ? AND version = ?", [caseId, version]);
  if (!v) throw new HttpError(404, "no_version", "إصدار غير موجود");
  if (!["draft", "in_review", "approved"].includes(v.status)) throw new HttpError(409, "locked", "الإصدار منشور أو متقاعد");
  if (status === "approved" && v.created_by === user.id) throw new HttpError(403, "four_eyes", "لا يجوز لكاتب الإصدار أن يعتمد مراجعته بنفسه");
  await run("INSERT INTO case_reviews(case_id, version, role, reviewer_id, status, content_hash, notes, created_at) VALUES (?,?,?,?,?,?,?,?)",
    [caseId, version, role, user.id, status, v.content_hash, notes?.slice(0, 2000) ?? null, new Date().toISOString()]);
  const g = await gateState(caseId, version, v.content_hash);
  await run("UPDATE case_versions SET status = ? WHERE case_id = ? AND version = ? AND status IN ('draft','in_review','approved')", [g.all_approved ? "approved" : "in_review", caseId, version]);
  await audit(user.id, "case.review", `${caseId}@${version}`, { role, status }, ipH);
  return g;
}

export async function publish(user: UserRow, caseId: string, version: string, ipH: string) {
  const v = await getVersion(caseId, version);
  if (!v.gates.all_approved) throw new HttpError(409, "gates", "لم تكتمل موافقات البوابات السبع على المحتوى الحالي");
  const qa = await runQa(v.core as CaseFile, v.ui as CaseUi, v.scoring as ScoringSpec);
  if (!qa.ok) throw new HttpError(409, "qa_failed", "فحص الجودة لم ينجح؛ أصلح الأخطاء أولاً");
  if (v.created_by === user.id) throw new HttpError(403, "four_eyes", "لا يجوز لكاتب الإصدار أن ينشره بنفسه");
  await run("UPDATE case_versions SET status = 'retired' WHERE case_id = ? AND status = 'published'", [caseId]);
  await run("UPDATE case_versions SET status = 'published', qa_json = ? WHERE case_id = ? AND version = ?", [JSON.stringify(qa), caseId, version]);
  await audit(user.id, "case.publish", `${caseId}@${version}`, { hash: v.content_hash }, ipH);
  return { ok: true };
}

export async function listTickets(status = "pending") {
  return q("SELECT code, case_id, case_version, justification, deterministic_json, status, level, feedback_ar, created_at FROM review_tickets WHERE status = ? ORDER BY created_at LIMIT 100", [status]);
}

export async function reviewTicket(user: UserRow, code: string, level: number, feedback: string, ipH: string) {
  if (!Number.isInteger(level) || level < 0 || level > 4) throw new HttpError(422, "bad_level", "المستوى بين 0 و4");
  const r = await run("UPDATE review_tickets SET status='reviewed', reviewer_id=?, level=?, feedback_ar=?, reviewed_at=? WHERE code=? AND status='pending'", [user.id, level, feedback.slice(0, 2000), new Date().toISOString(), code]);
  if (!r.rowsAffected) throw new HttpError(404, "no_ticket", "الطلب غير موجود أو سبقت مراجعته");
  await audit(user.id, "ticket.review", code, { level }, ipH);
}
