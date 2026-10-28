/**
 * Per-skill learning estimate (LEARNER_MASTERY_MODEL, release-1 simplification).
 * Pure functions. Input is real play data only: one observation = how well a finished case's rubric criteria
 * (mapped to a skill) were met. No observations means no estimate. Nothing here is stored, ranked or shown as a number.
 *
 * Model: per skill, Beta(1 + sum(w*s), 1 + sum(w*(1-s))) over per-case scores s in [0,1] (several criteria of the
 * same case on the same skill are averaged first, so one case counts once). Older cases weigh less (half-life 120 days).
 * A 90% credible interval is read off the Beta CDF. Display value = mean x (0.6 + 0.4 x retention), so a skill left
 * untouched for months drifts down gently instead of vanishing.
 * Status uses the interval, not only the mean, so two lucky cases cannot show "secure".
 */
export interface Observation { ko_id: string; case_id: string; score: number; at: string }
export type MasteryStatus = "insufficient_evidence" | "emerging" | "developing" | "secure";
export interface SkillEstimate {
  ko_id: string;
  status: MasteryStatus;
  cases: string[];
  /** 0 low, 1 medium, 2 higher: how tight the 90% interval is. Never a probability. */
  certainty: 0 | 1 | 2;
  /** internal (not for display as a number) */
  mean: number; lo: number; hi: number; retention: number;
  last_at: string;
}

export const HALF_LIFE_DAYS = 120;
export const MIN_CASES = 2;

export const STATUS_AR: Record<MasteryStatus, string> = {
  insufficient_evidence: "لا دليل كافٍ بعد",
  emerging: "بدأت تظهر",
  developing: "تتطوّر",
  secure: "ثابتة مبدئياً",
};
export const CERTAINTY_AR = ["ثقة التقدير منخفضة", "ثقة التقدير متوسطة", "ثقة التقدير أعلى"] as const;

function lgamma(x: number): number {
  const g = [76.18009172947146, -86.50532032941677, 24.01409824083091, -1.231739572450155, 0.1208650973866179e-2, -0.5395239384953e-5];
  let y = x; const t = x + 5.5 - (x + 0.5) * Math.log(x + 5.5); let s = 1.000000000190015;
  for (const c of g) s += c / ++y;
  return -t + Math.log((2.5066282746310005 * s) / x);
}
/** Beta CDF by Simpson integration of the pdf (a,b >= 1 so the pdf is bounded). */
export function betaCdf(x: number, a: number, b: number): number {
  if (x <= 0) return 0; if (x >= 1) return 1;
  const n = 400; const h = x / n; const lc = lgamma(a + b) - lgamma(a) - lgamma(b);
  const f = (t: number) => (t <= 0 || t >= 1 ? (a === 1 && t <= 0 ? Math.exp(lc) : b === 1 && t >= 1 ? Math.exp(lc) : 0) : Math.exp(lc + (a - 1) * Math.log(t) + (b - 1) * Math.log(1 - t)));
  let s = f(0) + f(x);
  for (let i = 1; i < n; i++) s += f(i * h) * (i % 2 ? 4 : 2);
  return Math.min(1, (s * h) / 3);
}
export function betaQuantile(p: number, a: number, b: number): number {
  let lo = 0, hi = 1;
  for (let i = 0; i < 40; i++) { const m = (lo + hi) / 2; if (betaCdf(m, a, b) < p) lo = m; else hi = m; }
  return (lo + hi) / 2;
}

const DAY = 86_400_000;
export const retention = (days: number) => Math.pow(0.5, Math.max(0, days) / HALF_LIFE_DAYS);

export function estimate(ko_id: string, obs: Observation[], now: Date | string = new Date()): SkillEstimate | null {
  const mine = obs.filter((o) => o.ko_id === ko_id);
  if (!mine.length) return null;
  const t0 = new Date(now).getTime();
  // average criteria of the same case first
  const byCase = new Map<string, { sum: number; n: number; at: string }>();
  for (const o of mine) { const c = byCase.get(o.case_id) ?? { sum: 0, n: 0, at: o.at }; c.sum += Math.min(1, Math.max(0, o.score)); c.n++; if (o.at > c.at) c.at = o.at; byCase.set(o.case_id, c); }
  let a = 1, b = 1, last = "";
  for (const c of byCase.values()) {
    const age = Math.max(0, (t0 - new Date(c.at).getTime()) / DAY);
    const w = Math.pow(0.5, age / HALF_LIFE_DAYS);
    const s = c.sum / c.n;
    a += w * s; b += w * (1 - s);
    if (c.at > last) last = c.at;
  }
  const mean0 = a / (a + b);
  const lo = betaQuantile(0.05, a, b), hi = betaQuantile(0.95, a, b);
  const R = retention((t0 - new Date(last).getTime()) / DAY);
  const mean = mean0 * (0.6 + 0.4 * R);
  const n = byCase.size;
  const width = hi - lo;
  const status: MasteryStatus = n < MIN_CASES ? "insufficient_evidence" : lo * (0.6 + 0.4 * R) >= 0.45 && mean >= 0.62 ? "secure" : mean >= 0.5 ? "developing" : "emerging";
  const certainty: 0 | 1 | 2 = n < MIN_CASES ? 0 : width < 0.42 ? 2 : 1;
  return { ko_id, status, cases: [...byCase.keys()], certainty, mean, lo, hi, retention: R, last_at: last };
}

export function estimateAll(obs: Observation[], now: Date | string = new Date()): SkillEstimate[] {
  const ids = [...new Set(obs.map((o) => o.ko_id))];
  const order: Record<MasteryStatus, number> = { emerging: 0, developing: 1, insufficient_evidence: 2, secure: 3 };
  return ids.map((k) => estimate(k, obs, now)!).sort((x, y) => order[x.status] - order[y.status] || x.mean - y.mean);
}

/** A next step that is a suggestion only: it never locks or unlocks anything. */
export function nextStep(est: SkillEstimate[], lessonOf: (ko: string) => string | undefined): { ko_id: string; kind: "lesson" | "case"; lesson_id?: string } | null {
  const target = est.find((e) => e.status === "emerging") ?? est.find((e) => e.status === "insufficient_evidence") ?? est.find((e) => e.status === "developing");
  if (!target) return null;
  const lesson_id = lessonOf(target.ko_id);
  return lesson_id ? { ko_id: target.ko_id, kind: "lesson", lesson_id } : { ko_id: target.ko_id, kind: "case" };
}
