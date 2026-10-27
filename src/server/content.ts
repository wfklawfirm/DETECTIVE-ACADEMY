import { readdirSync, readFileSync, existsSync } from "node:fs";
import { join } from "node:path";
import type { CaseFile } from "../engine/types";
import type { CaseUi, ScoringSpec } from "../engine/ui-types";
import { contentHash, qaCase, type QAReport } from "../engine/validate";
import { q, q1, run } from "./db";
import { env } from "./env";

export const CASES_DIR = "content/cases";
export const ROLES = ["narrative_editor", "scientific_reviewer", "learning_designer", "age_appropriateness", "cultural_reviewer", "legal_rights", "safety"] as const;
export type GateRole = (typeof ROLES)[number];

export interface LoadedCase {
  core: CaseFile;
  ui: CaseUi;
  scoring: ScoringSpec;
  version: string;
  hash: string;
  status: string;
  preview: boolean;
}

export interface CaseCard {
  case_id: string;
  title_ar: string;
  kicker_ar: string;
  tagline_ar: string;
  glyph: string;
  accent: string;
  minutes: number;
  difficulty: number;
  age_band: string;
  tutorial: boolean;
  preview: boolean;
  skills: { skill_id: string; track: string }[];
}

type Cache = Map<string, LoadedCase>;
const g = globalThis as typeof globalThis & { __atharCases?: Cache };
const cache = (): Cache => (g.__atharCases ??= new Map());

export function readFileTriplet(dir: string, id: string): { core: unknown; ui: unknown; scoring: unknown } | null {
  const a = join(dir, `${id}.json`), b = join(dir, `${id}.ui.json`), c = join(dir, `${id}.scoring.json`);
  if (![a, b, c].every(existsSync)) return null;
  return { core: JSON.parse(readFileSync(a, "utf8")), ui: JSON.parse(readFileSync(b, "utf8")), scoring: JSON.parse(readFileSync(c, "utf8")) };
}

export function listFileCaseIds(dir = CASES_DIR): string[] {
  return readdirSync(dir).filter((f) => f.endsWith(".json") && !f.endsWith(".ui.json") && !f.endsWith(".scoring.json")).map((f) => f.replace(/\.json$/, "")).sort();
}

/** Import every file case into case_versions (idempotent). New versions arrive as drafts; nothing is auto-approved. */
export async function syncFileCases(dir = CASES_DIR): Promise<string[]> {
  const out: string[] = [];
  for (const id of listFileCaseIds(dir)) {
    const t = readFileTriplet(dir, id)!;
    const core = t.core as CaseFile;
    const exists = await q1("SELECT 1 AS x FROM case_versions WHERE case_id = ? AND version = ?", [core.case_id, core.case_version]);
    const hash = await contentHash(core);
    const qa = qaCase(core);
    if (exists) {
      await run("UPDATE case_versions SET core_json=?, ui_json=?, scoring_json=?, content_hash=?, qa_json=? WHERE case_id=? AND version=? AND status IN ('draft','in_review')",
        [JSON.stringify(core), JSON.stringify(t.ui), JSON.stringify(t.scoring), hash, JSON.stringify(qa), core.case_id, core.case_version]);
    } else {
      await run("INSERT INTO case_versions(case_id, version, content_hash, status, core_json, ui_json, scoring_json, qa_json, created_by, created_at) VALUES (?,?,?,?,?,?,?,?,?,?)",
        [core.case_id, core.case_version, hash, "draft", JSON.stringify(core), JSON.stringify(t.ui), JSON.stringify(t.scoring), JSON.stringify(qa), "seed", new Date().toISOString()]);
      out.push(`${core.case_id}@${core.case_version}`);
    }
  }
  return out;
}

export interface GateState { hash: string; roles: Record<GateRole, "pending" | "changes_requested" | "approved">; all_approved: boolean }

export async function gateState(caseId: string, version: string, hash: string): Promise<GateState> {
  const rows = await q<{ role: GateRole; status: "pending" | "changes_requested" | "approved"; content_hash: string }>(
    "SELECT role, status, content_hash FROM case_reviews WHERE case_id = ? AND version = ? ORDER BY id", [caseId, version]);
  const roles = Object.fromEntries(ROLES.map((r) => [r, "pending"])) as GateState["roles"];
  for (const r of rows) if (r.content_hash === hash) roles[r.role] = r.status; // a review of an older hash does not count
  return { hash, roles, all_approved: ROLES.every((r) => roles[r] === "approved") };
}

function parseRow(row: { core_json: string; ui_json: string; scoring_json: string; version: string; content_hash: string; status: string }, preview: boolean): LoadedCase {
  const key = `${row.content_hash}:${row.status}:${preview}`;
  const hit = cache().get(key);
  if (hit) return hit;
  const lc: LoadedCase = { core: JSON.parse(row.core_json), ui: JSON.parse(row.ui_json), scoring: JSON.parse(row.scoring_json), version: row.version, hash: row.content_hash, status: row.status, preview };
  if (cache().size > 64) cache().clear();
  cache().set(key, lc);
  return lc;
}

/** The only entry point play uses to obtain case data. Published versions always win; preview only when explicitly enabled. */
export async function getPlayable(caseId: string): Promise<LoadedCase | null> {
  const pub = await q1<{ core_json: string; ui_json: string; scoring_json: string; version: string; content_hash: string; status: string }>(
    "SELECT core_json, ui_json, scoring_json, version, content_hash, status FROM case_versions WHERE case_id = ? AND status = 'published' ORDER BY created_at DESC LIMIT 1", [caseId]);
  if (pub) return parseRow(pub, false);
  if (!env.allowPreview) return null;
  const any = await q1<{ core_json: string; ui_json: string; scoring_json: string; version: string; content_hash: string; status: string }>(
    "SELECT core_json, ui_json, scoring_json, version, content_hash, status FROM case_versions WHERE case_id = ? AND status != 'retired' ORDER BY created_at DESC LIMIT 1", [caseId]);
  return any ? parseRow(any, true) : null;
}

export async function listPlayable(ageBand: "13-15" | "16-17" | "18+"): Promise<CaseCard[]> {
  const ids = (await q<{ case_id: string }>("SELECT DISTINCT case_id FROM case_versions WHERE status != 'retired'")).map((r) => r.case_id);
  const cards: CaseCard[] = [];
  for (const id of ids) {
    const c = await getPlayable(id);
    if (!c) continue;
    if (!ageAllows(c.core.meta.age_band, ageBand)) continue;
    cards.push(card(c));
  }
  return cards.sort((a, b) => Number(b.tutorial) - Number(a.tutorial) || a.difficulty - b.difficulty || a.case_id.localeCompare(b.case_id));
}

export const card = (c: LoadedCase): CaseCard => ({
  case_id: c.core.case_id, title_ar: c.ui.cover.title_ar, kicker_ar: c.ui.cover.kicker_ar, tagline_ar: c.ui.cover.tagline_ar, glyph: c.ui.cover.glyph, accent: c.ui.cover.accent,
  minutes: c.core.meta.estimated_minutes, difficulty: c.core.meta.difficulty, age_band: c.core.meta.age_band, tutorial: !!c.ui.tutorial, preview: c.preview, skills: c.ui.skills,
});

/** Age bands: the platform serves 16+. "13-15" players see only cases explicitly flagged for them (none yet). */
export function ageAllows(caseBand: string, user: "13-15" | "16-17" | "18+"): boolean {
  if (caseBand === "all") return true;
  if (user === "13-15") return caseBand === "13-15";
  if (user === "16-17") return caseBand === "16-18" || caseBand === "13-15";
  return true;
}

export async function qaOf(core: CaseFile): Promise<QAReport> {
  return qaCase(core);
}
