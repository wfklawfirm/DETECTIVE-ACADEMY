import { readFileSync } from "node:fs";
import { join } from "node:path";
import { gunzipSync } from "node:zlib";
import { z } from "zod";

/**
 * Admin-only research library (read-only). Everything here is reference data from the research packs:
 * competitor intelligence, strategy and internal planning included. Access is decided by `libraryAccess`
 * and enforced again inside every reader, so a page that forgets the check still cannot leak a document.
 */
export const EntrySchema = z.object({
  path: z.string(), pack: z.string(), source_path: z.string(), size: z.number(), sha256: z.string().length(64), type: z.string(), folder: z.string(),
  status: z.enum(["copied", "duplicate-of", "skipped"]),
  duplicate_of: z.string().optional(), duplicate_pack: z.string().optional(), reason: z.string().optional(),
  stored_as: z.string().optional(), desc: z.string().optional(), rows: z.number().optional(), sensitive: z.boolean().optional(),
});
export type Entry = z.infer<typeof EntrySchema>;
const ManifestSchema = z.object({ version: z.number(), audience: z.literal("admin-only"), note: z.string(), stats: z.record(z.string(), z.unknown()), files: z.array(EntrySchema) });
export type Manifest = z.infer<typeof ManifestSchema>;

export type Access = "ok" | "login" | "forbidden";
/** Only the admin role may open the library. No user = ask to log in; any other role = forbidden. */
export function libraryAccess(actor: { user: { role: string } | null }): Access {
  if (!actor.user) return "login";
  return actor.user.role === "admin" ? "ok" : "forbidden";
}
export class LibraryAccessError extends Error {
  constructor(public readonly access: Exclude<Access, "ok">) { super(access === "login" ? "login_required" : "forbidden"); }
}
function assertAccess(actor: { user: { role: string } | null }) {
  const a = libraryAccess(actor);
  if (a !== "ok") throw new LibraryAccessError(a);
}

const g = globalThis as typeof globalThis & { __atharResearch?: { man: Manifest; byPath: Map<string, Entry> } };
function load(root = process.cwd()) {
  if (g.__atharResearch) return g.__atharResearch;
  const man = ManifestSchema.parse(JSON.parse(readFileSync(join(root, "content/research/manifest.json"), "utf8")));
  const byPath = new Map<string, Entry>();
  // one canonical row per path: the winning copy (copied/skipped-winner) is listed before older superseded duplicates
  for (const e of man.files) { const cur = byPath.get(e.path); if (!cur || (cur.status !== "copied" && e.status === "copied")) byPath.set(e.path, e); }
  g.__atharResearch = { man, byPath };
  return g.__atharResearch;
}

export const FOLDER_AR: Record<string, string> = {
  "00_PROJECT_CONTROL": "إدارة المشروع", "01_SOURCE_CATALOG": "فهرس المصادر", "02_DETECTIVE_LITERATURE": "أدب التحري", "03_NARRATIVE_AND_GAME_DESIGN": "السرد وتصميم اللعب",
  "04_FORENSIC_SCIENCE": "العلوم الجنائية", "05_INVESTIGATIVE_REASONING": "الاستدلال التحقيقي", "06_COGNITIVE_SCIENCE": "علم الإدراك", "07_LEARNING_SCIENCE": "علوم التعلّم",
  "08_ARAB_AUDIENCE_AND_CULTURE": "الجمهور العربي والثقافة", "09_COMPETITIVE_INTELLIGENCE": "الاستخبارات التنافسية", "10_TECHNICAL_ARCHITECTURE": "البنية التقنية",
  "11_RIGHTS_PRIVACY_AND_SAFETY": "الحقوق والخصوصية والسلامة", "12_KNOWLEDGE_OBJECTS": "كائنات المعرفة", "13_CASE_DESIGN_REFERENCE": "مرجع تصميم القضايا",
  "14_PRODUCT_RESEARCH_SYNTHESIS": "خلاصة أبحاث المنتج", "15_STORY_MEDIA_AND_ASSETS": "القصة والوسائط والأصول", "99_LEGAL_SOURCE_ASSETS": "الأصول القانونية للمصادر",
  packs: "حزم أخرى (غير مرقّمة)", _archives: "أرشيفات",
};
export const STATUS_AR: Record<Entry["status"], string> = { copied: "منسوخ", "duplicate-of": "نسخة مكررة", skipped: "غير منسوخ" };

export interface FolderSummary { folder: string; label: string; files: number; readable: number }

export function listLibrary(actor: { user: { role: string } | null }): { entries: Entry[]; stats: Manifest["stats"]; folders: FolderSummary[] } {
  assertAccess(actor);
  const { man } = load();
  const m = new Map<string, FolderSummary>();
  for (const e of man.files) {
    const f = m.get(e.folder) ?? { folder: e.folder, label: FOLDER_AR[e.folder] ?? e.folder, files: 0, readable: 0 };
    f.files++; if (e.status === "copied") f.readable++; m.set(e.folder, f);
  }
  return { entries: man.files, stats: man.stats, folders: [...m.values()].sort((a, b) => a.folder.localeCompare(b.folder)) };
}

/** Resolve a URL path only through the manifest - user input never reaches the filesystem. */
export function findEntry(actor: { user: { role: string } | null }, segments: string[]): Entry | null {
  assertAccess(actor);
  if (segments.some((s) => !s || s === "." || s === ".." || s.includes("\\") || s.includes("\0"))) return null;
  return load().byPath.get(segments.join("/")) ?? null;
}

export function readDoc(actor: { user: { role: string } | null }, e: Entry): string | null {
  assertAccess(actor);
  const entry = load().byPath.get(e.path);
  if (!entry || entry.status !== "copied" || !entry.stored_as) return null;
  const p = join(process.cwd(), "content/research/docs", entry.stored_as);
  const buf = readFileSync(p);
  return (entry.stored_as.endsWith(".gz") ? gunzipSync(buf) : buf).toString("utf8");
}

/** Other manifest rows that share this path or this content (duplicates, superseded older versions). */
export function relatedRows(actor: { user: { role: string } | null }, e: Entry): Entry[] {
  assertAccess(actor);
  return load().man.files.filter((x) => x !== e && (x.path === e.path || x.duplicate_of === e.path || x.sha256 === e.sha256));
}

export interface SearchOpts { q?: string; folder?: string; type?: string; status?: string; deep?: boolean }
export function searchLibrary(actor: { user: { role: string } | null }, o: SearchOpts): { hits: Entry[]; deepHits: Map<string, string>; total: number } {
  assertAccess(actor);
  const { man } = load();
  const q = (o.q ?? "").trim().toLowerCase();
  let hits = man.files.filter((e) => (!o.folder || e.folder === o.folder) && (!o.type || e.type === o.type) && (!o.status || e.status === o.status));
  const deepHits = new Map<string, string>();
  if (q) {
    const terms = q.split(/\s+/);
    const meta = (e: Entry) => `${e.path} ${e.desc ?? ""} ${e.pack}`.toLowerCase();
    if (o.deep) {
      const out: Entry[] = [];
      for (const e of hits) {
        if (e.status !== "copied" || e.type !== "md") { if (terms.every((t) => meta(e).includes(t))) out.push(e); continue; }
        if (terms.every((t) => meta(e).includes(t))) { out.push(e); continue; }
        const txt = readDoc(actor, e)?.toLowerCase() ?? "";
        const i = txt.indexOf(terms[0] ?? "");
        if (i >= 0 && terms.every((t) => txt.includes(t))) { out.push(e); deepHits.set(e.path, txt.slice(Math.max(0, i - 60), i + 120).replace(/\s+/g, " ")); }
      }
      hits = out;
    } else hits = hits.filter((e) => terms.every((t) => meta(e).includes(t)));
  }
  return { hits, deepHits, total: man.files.length };
}

/* ───────── CSV / JSON helpers (pure) ───────── */
export function parseCsvPage(text: string, page: number, perPage: number): { header: string[]; rows: string[][]; total: number } {
  const header: string[] = []; const rows: string[][] = [];
  let row: string[] = []; let cell = ""; let q = false; let n = -1;
  const endRow = () => { row.push(cell); cell = ""; if (n === -1) header.push(...row); else if (n >= page * perPage && n < (page + 1) * perPage) rows.push(row); n++; row = []; };
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (q) { if (c === '"') { if (text[i + 1] === '"') { cell += '"'; i++; } else q = false; } else cell += c; }
    else if (c === '"') q = true;
    else if (c === ",") { row.push(cell); cell = ""; }
    else if (c === "\n") endRow();
    else if (c !== "\r") cell += c;
  }
  if (cell !== "" || row.length) endRow();
  return { header, rows, total: Math.max(0, n) };
}
export function firstJsonRecords(text: string, type: "json" | "jsonl", n: number): { count: number; records: unknown[]; keys: string[] } {
  if (type === "jsonl") {
    const lines = text.split("\n").filter((l) => l.trim());
    const records: unknown[] = [];
    for (const l of lines.slice(0, n)) { try { records.push(JSON.parse(l)); } catch { records.push(l.slice(0, 300)); } }
    const first = records[0];
    return { count: lines.length, records, keys: first && typeof first === "object" ? Object.keys(first as object).slice(0, 12) : [] };
  }
  const d: unknown = JSON.parse(text);
  if (Array.isArray(d)) return { count: d.length, records: d.slice(0, n), keys: [] };
  const o = d as Record<string, unknown>; const ks = Object.keys(o);
  return { count: ks.length, records: ks.slice(0, n).map((k) => ({ [k]: o[k] })), keys: ks.slice(0, 12) };
}
export const humanSize = (b: number) => (b < 1024 ? `${b} B` : b < 1048576 ? `${(b / 1024).toFixed(1)} KB` : `${(b / 1048576).toFixed(1)} MB`);
