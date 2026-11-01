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
      await run("INSERT OR IGNORE INTO case_versions(case_id, version, content_hash, status, core_json, ui_json, scoring_json, qa_json, created_by, created_at) VALUES (?,?,?,?,?,?,?,?,?,?)",
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

interface VersionMeta { case_id: string; version: string; content_hash: string; status: string }
type VersionRow = VersionMeta & { core_json: string; ui_json: string; scoring_json: string };

/**
 * Batch version of getPlayable: resolves many cases in TWO round trips instead of one per case.
 * (1) a tiny metadata query picks the version per case using the same rules as getPlayable
 *     (latest published wins; otherwise latest non-retired, only when preview is enabled);
 * (2) JSON blobs are fetched, in one query, only for versions not already in the process cache.
 * A warm worker therefore needs a single light query. Pass no ids to resolve every case.
 */
export async function getPlayableMany(caseIds?: string[]): Promise<Map<string, LoadedCase>> {
  const out = new Map<string, LoadedCase>();
  if (caseIds && caseIds.length === 0) return out;
  const chosen = await chooseVersions(caseIds);
  const keyOf = (m: VersionMeta & { preview: boolean }) => `${m.content_hash}:${m.status}:${m.preview}`;
  const missing = chosen.filter((m) => !cache().has(keyOf(m)));
  const fetched = new Map<string, VersionRow>();
  if (missing.length) {
    const rows = await q<VersionRow>(
      `SELECT case_id, version, content_hash, status, core_json, ui_json, scoring_json FROM case_versions WHERE (case_id || '@' || version) IN (${missing.map(() => "?").join(",")})`,
      missing.map((m) => `${m.case_id}@${m.version}`));
    for (const r of rows) fetched.set(`${r.case_id}@${r.version}`, r);
  }
  for (const m of chosen) {
    const hit = cache().get(keyOf(m));
    if (hit) { out.set(m.case_id, hit); continue; }
    const row = fetched.get(`${m.case_id}@${m.version}`);
    if (row) out.set(m.case_id, parseRow(row, m.preview));
  }
  return out;
}

/** Which version of each case is playable: same rules as getPlayable, for many cases in one light query. */
async function chooseVersions(caseIds?: string[]): Promise<(VersionMeta & { preview: boolean })[]> {
  const where = caseIds ? ` AND case_id IN (${caseIds.map(() => "?").join(",")})` : "";
  const metas = await q<VersionMeta>(
    `SELECT case_id, version, content_hash, status FROM case_versions WHERE status != 'retired'${where} ORDER BY created_at DESC`, caseIds ?? []);
  const chosen = new Map<string, VersionMeta & { preview: boolean }>();
  for (const m of metas) if (m.status === "published" && !chosen.has(m.case_id)) chosen.set(m.case_id, { ...m, preview: false });
  if (env.allowPreview) for (const m of metas) if (!chosen.has(m.case_id)) chosen.set(m.case_id, { ...m, preview: true });
  return [...chosen.values()];
}

/** What list screens need from a case: its card plus age band and evidence count. */
export interface LightCase { card: CaseCard; age_band: string; evidence_total: number }
const gl = globalThis as typeof globalThis & { __atharLight?: Map<string, LightCase> };
const lightCache = (): Map<string, LightCase> => (gl.__atharLight ??= new Map());
type LightRow = VersionMeta & { mins: number; diff: number; ab: string; cover: string; tut: unknown; skills: string | null; ev_n: number };

/**
 * Card-level data for many cases without downloading their full JSON (core + ui + scoring can be megabytes in total).
 * The database extracts only the few fields a card needs, and results are cached per version hash, so a cold worker pays
 * one small query instead of fetching every case in full.
 */
export async function getCardsLight(caseIds?: string[]): Promise<Map<string, LightCase>> {
  const out = new Map<string, LightCase>();
  if (caseIds && caseIds.length === 0) return out;
  const chosen = await chooseVersions(caseIds);
  const keyOf = (m: VersionMeta & { preview: boolean }) => `${m.content_hash}:${m.status}:${m.preview}`;
  const missing = chosen.filter((m) => !lightCache().has(keyOf(m)));
  if (missing.length) {
    const rows = await q<LightRow>(
      `SELECT case_id, version, content_hash, status,
         json_extract(core_json, '$.meta.estimated_minutes') AS mins, json_extract(core_json, '$.meta.difficulty') AS diff,
         json_extract(core_json, '$.meta.age_band') AS ab, json_extract(ui_json, '$.cover') AS cover,
         json_extract(ui_json, '$.tutorial') AS tut, json_extract(ui_json, '$.skills') AS skills,
         json_array_length(core_json, '$.evidence') AS ev_n
       FROM case_versions WHERE (case_id || '@' || version) IN (${missing.map(() => "?").join(",")})`,
      missing.map((m) => `${m.case_id}@${m.version}`));
    const byId = new Map(rows.map((r) => [`${r.case_id}@${r.version}`, r]));
    if (lightCache().size > 256) lightCache().clear();
    for (const m of missing) {
      const r = byId.get(`${m.case_id}@${m.version}`);
      if (!r) continue;
      const cover = JSON.parse(r.cover) as CaseUi["cover"];
      lightCache().set(keyOf(m), {
        age_band: r.ab, evidence_total: Number(r.ev_n),
        card: {
          case_id: m.case_id, title_ar: cover.title_ar, kicker_ar: cover.kicker_ar, tagline_ar: cover.tagline_ar, glyph: cover.glyph, accent: cover.accent,
          minutes: Number(r.mins), difficulty: Number(r.diff), age_band: r.ab, tutorial: !!r.tut, preview: m.preview,
          skills: r.skills ? (JSON.parse(r.skills) as CaseCard["skills"]) : [],
        },
      });
    }
  }
  for (const m of chosen) { const hit = lightCache().get(keyOf(m)); if (hit) out.set(m.case_id, hit); }
  return out;
}

export async function listPlayable(ageBand: "13-15" | "16-17" | "18+"): Promise<CaseCard[]> {
  const all = await getCardsLight();
  const cards: CaseCard[] = [];
  for (const c of all.values()) {
    if (!ageAllows(c.age_band, ageBand)) continue;
    cards.push(c.card);
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
