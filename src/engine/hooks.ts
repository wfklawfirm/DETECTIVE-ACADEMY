// Entry hooks: one short, spoiler-safe, curiosity-driven prompt shown at EVERY entry to the platform.
// Pure and deterministic given its inputs (so it is testable). Ethics: no loss-aversion counters, no guilt for absence.

export type HookKind = "teaser" | "welcome_back" | "cliffhanger" | "skill" | "challenge";
export type HookSurface = "landing" | "home" | "case_open" | "case_return";

export interface HookDef {
  id: string;
  kind: HookKind;
  surfaces: HookSurface[];
  text_ar: string;
  cta_ar?: string;
  cta_href?: string;
  when?: { never_started?: boolean; has_open_case?: boolean; min_done?: number; max_done?: number };
}

export interface ProgressCase {
  case_id: string;
  title_ar: string;
  done: boolean;
  evidence_count: number;
  locked_count: number;
  updated_at: string;
}

export interface HookContext {
  surface: HookSurface;
  /** progress per case (empty for a brand-new visitor) */
  cases: ProgressCase[];
  /** ids shown recently on this device, newest first */
  recent_ids: string[];
  /** a counter that grows with each entry on this device, so rotation continues across visits */
  entry_counter: number;
  /** stable per-device random seed */
  seed: string;
  /** reduced-intensity mode: only calm kinds (skill / welcome_back) */
  gentle: boolean;
  /** case-specific: when opening/returning to a case, a stage cliffhanger from the case's own ui sidecar */
  case_stage_hook?: { case_id: string; text_ar: string } | null;
}

export interface ResolvedHook {
  id: string;
  kind: HookKind;
  text_ar: string;
  cta_ar?: string;
  cta_href?: string;
  personalised: boolean;
}

function h32(s: string): number {
  let h = 2166136261;
  for (let i = 0; i < s.length; i++) {
    h ^= s.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return h >>> 0;
}

function eligible(h: HookDef, ctx: HookContext): boolean {
  if (!h.surfaces.includes(ctx.surface)) return false;
  if (ctx.gentle && h.kind !== "skill" && h.kind !== "welcome_back") return false;
  const w = h.when;
  if (!w) return true;
  const done = ctx.cases.filter((c) => c.done);
  const open = ctx.cases.filter((c) => !c.done && c.evidence_count > 0);
  if (w.never_started && ctx.cases.length > 0) return false;
  if (w.has_open_case === true && open.length === 0) return false;
  if (w.has_open_case === false && open.length > 0) return false;
  if (w.min_done !== undefined && done.length < w.min_done) return false;
  if (w.max_done !== undefined && done.length > w.max_done) return false;
  return true;
}

const fill = (t: string, vars: Record<string, string | number>) => t.replace(/\{\{(\w+)\}\}/g, (_, k: string) => String(vars[k] ?? ""));

/** Choose exactly one hook for this entry. Never returns the immediately previous hook when an alternative exists. */
export function selectHook(hooks: HookDef[], ctx: HookContext): ResolvedHook {
  const pool = hooks.filter((h) => eligible(h, ctx));
  const open = ctx.cases.filter((c) => !c.done && c.evidence_count > 0).sort((a, b) => b.updated_at.localeCompare(a.updated_at))[0];
  const lastDone = ctx.cases.filter((c) => c.done).sort((a, b) => b.updated_at.localeCompare(a.updated_at))[0];

  // case stage cliffhanger takes priority on case surfaces
  if ((ctx.surface === "case_open" || ctx.surface === "case_return") && ctx.case_stage_hook && !ctx.gentle && ctx.entry_counter % 2 === 0) {
    const id = `case:${ctx.case_stage_hook.case_id}`;
    if (ctx.recent_ids[0] !== id) return { id, kind: "cliffhanger", text_ar: ctx.case_stage_hook.text_ar, personalised: true };
  }

  const notLast = pool.filter((h) => h.id !== ctx.recent_ids[0]);
  const candidates = notLast.length ? notLast : pool;
  const notRecent = candidates.filter((h) => !ctx.recent_ids.slice(0, 3).includes(h.id));
  const base = notRecent.length ? notRecent : candidates;
  // personalised hooks (those that use progress) get triple weight
  const weighted: HookDef[] = [];
  for (const h of base) {
    const personal = h.kind === "welcome_back" || /\{\{/.test(h.text_ar);
    const w = personal ? 3 : 1;
    for (let i = 0; i < w; i++) weighted.push(h);
  }
  if (!weighted.length) {
    return { id: "fallback", kind: "teaser", text_ar: "ملف جديد ينتظر من ينتبه للتفاصيل.", cta_ar: "ابدأ", cta_href: "/start", personalised: false };
  }
  const pick = weighted[h32(`${ctx.seed}:${ctx.entry_counter}:${ctx.surface}`) % weighted.length]!;
  const caseRef = open ?? lastDone;
  const vars = {
    case_title: open?.title_ar ?? lastDone?.title_ar ?? "",
    last_done_title: lastDone?.title_ar ?? "",
    n_locked: open?.locked_count ?? 0,
    n_evidence: open?.evidence_count ?? 0,
    case_href: open ? `/play/${open.case_id}` : caseRef ? `/case/${caseRef.case_id}` : "/cases",
  };
  return {
    id: pick.id,
    kind: pick.kind,
    text_ar: fill(pick.text_ar, vars),
    cta_ar: pick.cta_ar,
    cta_href: pick.cta_href ? fill(pick.cta_href, vars) : undefined,
    personalised: /\{\{/.test(pick.text_ar),
  };
}

/** Day index since epoch for the daily riddle (UTC). */
export const dayIndex = (d: Date) => Math.floor(d.getTime() / 86_400_000);

export interface RiddleDef {
  id: string;
  title_ar: string;
  prompt_ar: string;
  options: { id: string; text_ar: string }[];
  answer_id: string;
  explanation_ar: string;
  skill_ko_ref: string;
}

/** Deterministic order per device: the daily riddle never depends on server state. */
export function dailyRiddle(riddles: RiddleDef[], d: Date, seed: string): RiddleDef {
  const idx = (dayIndex(d) + (h32(seed) % riddles.length)) % riddles.length;
  return riddles[idx]!;
}

/** Shuffle options with a seed so the correct answer is not always in the same slot. */
export function shuffleOptions<T extends { id: string }>(opts: T[], seed: string): T[] {
  const a = [...opts];
  let s = h32(seed) || 1;
  for (let i = a.length - 1; i > 0; i--) {
    s = (Math.imul(s, 1664525) + 1013904223) >>> 0;
    const j = s % (i + 1);
    [a[i], a[j]] = [a[j]!, a[i]!];
  }
  return a;
}
