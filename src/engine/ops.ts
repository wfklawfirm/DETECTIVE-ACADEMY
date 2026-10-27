import { EngineError } from "./state";
import type { CaseFile, HypothesisEntry, LinkDirection, PlayState, SourceClass } from "./types";
import type { LabDef, TimeNormalizerLab } from "./ui-types";

const clone = <T,>(x: T): T => structuredClone(x);
const bump = (st: PlayState, now: string) => { st.seq += 1; st.updated_at = now; };

function ensureHyp(c: CaseFile, st: PlayState, hid: string): HypothesisEntry {
  if (!c.hypotheses.some((h) => h.id === hid)) throw new EngineError("unknown_hypothesis", "فرضية غير معروفة");
  if (!st.hypotheses[hid]) {
    st.hypotheses[hid] = { confidence: null, stance: "open", links: {}, revisions: [{ seq: st.seq + 1, kind: "added", detail: "added", evidence_count: st.evidence.length }] };
  }
  return st.hypotheses[hid]!;
}
const open = (st: PlayState) => {
  if (st.machine !== "investigating") throw new EngineError("not_investigating", "التحقيق غير مفتوح في هذه المرحلة");
};

export function addHypothesis(c: CaseFile, prev: PlayState, hid: string, now = new Date().toISOString()): PlayState {
  const st = clone(prev); open(st); ensureHyp(c, st, hid); bump(st, now); st.log.push({ seq: st.seq, action: "hyp_add", target: hid }); return st;
}

export function setConfidence(c: CaseFile, prev: PlayState, hid: string, value: number, now = new Date().toISOString()): PlayState {
  if (!Number.isFinite(value) || value < 0 || value > 100) throw new EngineError("bad_value", "قيمة الثقة يجب أن تكون بين 0 و100");
  const st = clone(prev); open(st); const h = ensureHyp(c, st, hid);
  bump(st, now);
  h.revisions.push({ seq: st.seq, kind: "confidence", detail: `${h.confidence ?? "-"}->${Math.round(value)}`, evidence_count: st.evidence.length });
  h.confidence = Math.round(value); st.log.push({ seq: st.seq, action: "hyp_conf", target: hid });
  return st;
}

export function setStance(c: CaseFile, prev: PlayState, hid: string, stance: "open" | "leading" | "ruled_out", ruledOutWith: string[] = [], now = new Date().toISOString()): PlayState {
  const st = clone(prev); open(st); const h = ensureHyp(c, st, hid);
  if (stance === "ruled_out") {
    if (!ruledOutWith.length) throw new EngineError("need_evidence", "لا يمكن استبعاد فرضية دون إرفاق دليل");
    for (const e of ruledOutWith) if (!st.evidence.includes(e)) throw new EngineError("not_owned", "دليل غير مملوك");
    h.ruled_out_with = ruledOutWith;
  }
  if (stance === "leading") for (const [k, o] of Object.entries(st.hypotheses)) if (k !== hid && o.stance === "leading") { o.stance = "open"; }
  bump(st, now);
  h.revisions.push({ seq: st.seq, kind: "stance", detail: `${h.stance}->${stance}`, evidence_count: st.evidence.length });
  h.stance = stance; st.log.push({ seq: st.seq, action: "hyp_stance", target: hid });
  return st;
}

export function linkEvidence(c: CaseFile, prev: PlayState, hid: string, eid: string, dir: LinkDirection, now = new Date().toISOString()): PlayState {
  const st = clone(prev); open(st); const h = ensureHyp(c, st, hid);
  if (!st.evidence.includes(eid)) throw new EngineError("not_owned", "لا تملك هذا الدليل بعد");
  bump(st, now);
  h.revisions.push({ seq: st.seq, kind: "link", detail: `${eid}:${h.links[eid] ?? "-"}->${dir}`, evidence_count: st.evidence.length });
  h.links[eid] = dir; st.log.push({ seq: st.seq, action: "link", target: `${hid}:${eid}` });
  return st;
}

export function tagSource(c: CaseFile, prev: PlayState, eid: string, cls: SourceClass, now = new Date().toISOString()): PlayState {
  const st = clone(prev); open(st);
  if (!st.evidence.includes(eid)) throw new EngineError("not_owned", "لا تملك هذا الدليل بعد");
  if (!["primary_record", "redisplay", "claim", "template", "public_document"].includes(cls)) throw new EngineError("bad_class", "تصنيف غير معروف");
  bump(st, now); st.source_tags[eid] = cls; st.log.push({ seq: st.seq, action: "tag", target: eid });
  return st;
}

export function placeOnTimeline(prev: PlayState, eid: string, utcMinute: number, note: string | undefined, now = new Date().toISOString()): PlayState {
  const st = clone(prev); open(st);
  if (!st.evidence.includes(eid)) throw new EngineError("not_owned", "لا تملك هذا الدليل بعد");
  if (!Number.isInteger(utcMinute) || Math.abs(utcMinute) > 60 * 24 * 14) throw new EngineError("bad_value", "قيمة زمنية غير صالحة");
  st.timeline = st.timeline.filter((t) => t.evidence_id !== eid);
  st.timeline.push({ evidence_id: eid, utc_minute: utcMinute, note: note?.slice(0, 200) });
  bump(st, now); st.log.push({ seq: st.seq, action: "timeline", target: eid });
  return st;
}

export function addJournal(prev: PlayState, text: string, now = new Date().toISOString()): PlayState {
  const t = text.trim().slice(0, 1000);
  if (!t) throw new EngineError("empty", "نص فارغ");
  const st = clone(prev); if (st.journal.length >= 200) throw new EngineError("limit", "تجاوزت الحد الأقصى للملاحظات");
  bump(st, now); st.journal.push({ seq: st.seq, text: t }); return st;
}

// ---------- labs ----------
export function hhmmToMin(s: string): number {
  const m = /^(\d{1,2}):(\d{2})$/.exec(s);
  if (!m) throw new EngineError("bad_time", "صيغة وقت غير صالحة");
  return Number(m[1]) * 60 + Number(m[2]);
}
export function fmtUtc(totalMin: number, lab: TimeNormalizerLab): string {
  const abs = lab.epoch_utc_minute_of_day + totalMin;
  const day = Math.floor(abs / 1440);
  const m = ((abs % 1440) + 1440) % 1440;
  const hh = String(Math.floor(m / 60)).padStart(2, "0"), mm = String(m % 60).padStart(2, "0");
  return `${hh}:${mm} ${lab.day_labels_ar[day] ?? `يوم ${day}`}`;
}

export interface LabOutput { rows: { evidence_id: string; utc_min: number; utc_end_min?: number; label: string }[]; spread_min: number; converged: boolean }

/** Deterministic time-normaliser: normalised = shown (+ skew) - offset. Skew is the minutes the device is SLOW (positive => add). */
export function evalTimeNormalizer(lab: TimeNormalizerLab, inputs: Record<string, number>): LabOutput {
  const rows = lab.items.map((it) => {
    const off = Number(inputs[`${it.evidence_id}.offset_h`] ?? 0);
    const skew = Number(inputs[`${it.evidence_id}.skew_min`] ?? 0);
    if (![off, skew].every(Number.isFinite) || Math.abs(off) > 14 || Math.abs(skew) > 120) throw new EngineError("bad_value", "قيم المختبر خارج النطاق المقبول");
    const base = it.day * 1440 + hhmmToMin(it.hhmm) - lab.epoch_utc_minute_of_day;
    const adj = base - off * 60 + skew;
    const end = it.end_hhmm ? it.day * 1440 + hhmmToMin(it.end_hhmm) - lab.epoch_utc_minute_of_day - off * 60 + skew : undefined;
    return { evidence_id: it.evidence_id, utc_min: adj, utc_end_min: end, label: it.label_ar };
  });
  const starts = rows.map((r) => r.utc_min);
  const ends = rows.map((r) => r.utc_end_min).filter((x): x is number => x !== undefined);
  const spread = Math.max(Math.max(...starts) - Math.min(...starts), ends.length > 1 ? Math.max(...ends) - Math.min(...ends) : 0);
  return { rows, spread_min: spread, converged: spread <= lab.tolerance_min };
}

export function runLab(c: CaseFile, labs: LabDef[], prev: PlayState, labId: string, inputs: Record<string, number>, now = new Date().toISOString()): { state: PlayState; output: LabOutput; granted: string[] } {
  const st = clone(prev); open(st);
  const lab = labs.find((l) => l.id === labId);
  if (!lab) throw new EngineError("unknown_lab", "مختبر غير معروف");
  for (const it of lab.items) if (!st.evidence.includes(it.evidence_id)) throw new EngineError("lab_locked", "افتح الأدلة اللازمة للمختبر أولاً");
  if (st.lab_runs.filter((r) => r.lab_id === labId).length >= 60) throw new EngineError("limit", "تجاوزت عدد محاولات المختبر");
  const out = evalTimeNormalizer(lab, inputs);
  bump(st, now);
  st.lab_runs.push({ seq: st.seq, lab_id: labId, inputs, output: out as unknown as Record<string, unknown>, converged: out.converged });
  const granted: string[] = [];
  if (out.converged && lab.grants_evidence_on_converge && !st.evidence.includes(lab.grants_evidence_on_converge)) {
    st.evidence.push(lab.grants_evidence_on_converge); granted.push(lab.grants_evidence_on_converge);
  }
  st.log.push({ seq: st.seq, action: "lab", target: labId });
  void c;
  return { state: st, output: out, granted };
}

// ---------- hints ----------
import { evalGuard } from "./guard";
export function nextHint(c: CaseFile, prev: PlayState, now = new Date().toISOString()): { state: PlayState; hint: { id: string; level: number; kind: string; text_ar: string } | null } {
  const st = clone(prev);
  const given = new Set(st.hints.map((h) => h.hint_id));
  // choose the lowest-level not-yet-given hint whose trigger holds; prefer targeted hints for inferences the player has not yet mastered
  const cand = c.hint_ladder.filter((h) => !given.has(h.id) && evalGuard(h.trigger, st)).sort((a, b) => a.level - b.level || (a.targets_inference_id ? 0 : 1) - (b.targets_inference_id ? 0 : 1));
  const h = cand[0];
  if (!h) return { state: st, hint: null };
  bump(st, now); st.hints.push({ seq: st.seq, hint_id: h.id, level: h.level }); st.log.push({ seq: st.seq, action: "hint", target: h.id });
  return { state: st, hint: { id: h.id, level: h.level, kind: h.kind, text_ar: h.text_ar } };
}
