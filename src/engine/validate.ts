import Ajv2020 from "ajv/dist/2020.js";
import addFormats from "ajv-formats";
import schema from "../../content/schema/case_schema.json";
import { guardRefs } from "./guard";
import type { CaseFile, Guard } from "./types";

const ajv = new Ajv2020({ allErrors: true, strict: false });
(addFormats as unknown as (a: unknown) => void)(ajv);
const validateSchema = ajv.compile(schema as object);

export interface QAReport {
  ok: boolean;
  errors: string[];
  warnings: string[];
  reachable_evidence: string[];
  unreachable_evidence: string[];
  proof_paths: number;
  proof_sets: string[][];
}

export function schemaErrors(c: unknown): string[] {
  if (validateSchema(c)) return [];
  return (validateSchema.errors ?? []).map((e) => `SCHEMA ${e.instancePath || "/"} ${e.message ?? ""}`);
}

/** Over-approximate guard satisfiability under a monotone set of owned evidence/facts. */
function guardOk(g: Guard | undefined, ev: Set<string>, facts: Set<string>): boolean {
  if (!g) return true;
  if ("always" in g) return true;
  if ("has_evidence" in g) return ev.has(g.has_evidence);
  if ("fact_unlocked" in g) return facts.has(g.fact_unlocked);
  if ("presented" in g) return ev.has(g.presented.evidence_id);
  if ("in_state" in g || "trust_at_least" in g) return true;
  if ("all" in g) return g.all.every((x) => guardOk(x, ev, facts));
  if ("any" in g) return g.any.some((x) => guardOk(x, ev, facts));
  if ("not" in g) return true; // over-approximation (can always be satisfied by not having it)
  return false;
}

export function reachableSets(c: CaseFile, startEvidence: string[] = []) {
  const ev = new Set<string>(startEvidence);
  const facts = new Set<string>(c.premise.public_fact_ids);
  let changed = true;
  while (changed) {
    changed = false;
    for (const a of c.mechanics.actions) {
      if (!guardOk(a.precondition, ev, facts)) continue;
      for (const e of a.effects) {
        if (e.op === "grant_evidence" && e.ref_id && !ev.has(e.ref_id)) { ev.add(e.ref_id); changed = true; }
        if (e.op === "unlock_fact" && e.ref_id && !facts.has(e.ref_id)) { facts.add(e.ref_id); changed = true; }
      }
    }
    // Dialogue can unlock facts: a fact is unlockable when the character is interviewable, a topic carries the fact and an authored
    // reveal line voices it (and, for hidden facts, the reveal guard is satisfiable). Over-approximation, like guardOk.
    for (const ch of c.entities.characters) {
      const ivActs = c.mechanics.actions.filter((a) => a.type === "interview" && a.target_id === ch.id);
      if (ivActs.length && !ivActs.some((a) => guardOk(a.precondition, ev, facts))) continue;
      const ks = c.character_knowledge.find((k) => k.character_id === ch.id);
      if (!ks) continue;
      const topicFacts = new Set((c.dialogue?.topics ?? []).flatMap((t) => t.fact_ids));
      const voiced = new Set((ch.authored_lines ?? []).filter((l) => l.purpose === "reveal" || l.purpose === "break_down").flatMap((l) => l.fact_ids ?? []));
      const hiddenIds = new Set(ks.hides.map((h) => h.fact_id));
      const add = (f: string) => { if (!facts.has(f)) { facts.add(f); changed = true; } };
      for (const k of ks.knows) if (!hiddenIds.has(k.fact_id) && topicFacts.has(k.fact_id) && voiced.has(k.fact_id)) add(k.fact_id);
      for (const h of ks.hides) if (topicFacts.has(h.fact_id) && voiced.has(h.fact_id) && guardOk(h.reveal_when, ev, facts)) add(h.fact_id);
    }
  }
  return { ev, facts };
}

/** Which facts/hypothesis-conclusions can be derived from a given evidence set via the inference graph. */
export function derive(c: CaseFile, evidence: Set<string>): { facts: Set<string>; inferences: Set<string> } {
  const facts = new Set<string>();
  const infs = new Set<string>();
  let changed = true;
  while (changed) {
    changed = false;
    for (const i of c.evidence_graph.inferences) {
      if (infs.has(i.id)) continue;
      const ok = i.premises.every((p) =>
        p.ref_type === "general_knowledge" ? true
        : p.ref_type === "evidence" ? evidence.has(p.ref_id)
        : p.ref_type === "fact" ? facts.has(p.ref_id)
        : infs.has(p.ref_id));
      if (!ok) continue;
      infs.add(i.id); changed = true;
      if (i.conclusion.ref_type === "fact") facts.add(i.conclusion.ref_id);
    }
  }
  return { facts, inferences: infs };
}

function* subsets<T>(arr: T[], max: number): Generator<T[]> {
  const n = arr.length;
  for (let mask = 1; mask < 1 << n; mask++) {
    const s: T[] = [];
    let cnt = 0;
    for (let i = 0; i < n; i++) if (mask & (1 << i)) { s.push(arr[i]!); cnt++; }
    if (cnt <= max) yield s;
  }
}

/** Minimal evidence sets that derive ALL key facts (subset-minimal). Bounded to <=18 relevant evidence items. */
export function minimalProofSets(c: CaseFile, maxSize = 6): string[][] {
  const { ev } = reachableSets(c);
  const relevant = [...new Set(c.evidence_graph.inferences.flatMap((i) => i.premises.filter((p) => p.ref_type === "evidence").map((p) => p.ref_id)))].filter((e) => ev.has(e));
  if (relevant.length > 18) return [];
  const keys = c.truth.solution.key_fact_ids;
  const found: string[][] = [];
  for (const s of subsets(relevant, maxSize)) {
    const d = derive(c, new Set(s)).facts;
    if (keys.every((k) => d.has(k))) {
      if (!found.some((f) => f.every((x) => s.includes(x)))) found.push(s);
    }
  }
  return found.sort((a, b) => a.length - b.length);
}

export function maxDisjoint(sets: string[][]): number {
  let best = 0;
  const rec = (i: number, used: Set<string>, n: number) => {
    best = Math.max(best, n);
    for (let j = i; j < sets.length; j++) {
      if (sets[j]!.some((x) => used.has(x))) continue;
      const u = new Set(used); sets[j]!.forEach((x) => u.add(x));
      rec(j + 1, u, n + 1);
    }
  };
  rec(0, new Set(), 0);
  return best;
}

const ABSOLUTE_AR = ["تطابق 100%", "تطابق 100٪", "مستحيل أن يكون غيره", "دليل قاطع على الذنب", "يستبعد كل البشر"];
const DEMEANOUR_AR = ["فراسة", "ملامح", "قسمات", "لغة الجسد", "تجنب النظر", "تجنّب النظر", "ارتبك فهو", "بكى فهو"];
const RTL_BAD = /[ﭐ-﷿ﹰ-﻿‎‏‪-‮⁦-⁩]/;

function* strings(o: unknown, path = ""): Generator<[string, string]> {
  if (typeof o === "string") yield [path, o];
  else if (Array.isArray(o)) for (let i = 0; i < o.length; i++) yield* strings(o[i], `${path}[${i}]`);
  else if (o && typeof o === "object") for (const [k, v] of Object.entries(o)) yield* strings(v, `${path}/${k}`);
}

/** Port of the library's check_case.py rules that matter for the runtime Creator Studio. See docs/CASE_ENGINE.md. */
export function qaCase(c: CaseFile): QAReport {
  const errors: string[] = [];
  const warnings: string[] = [];
  const se = schemaErrors(c);
  errors.push(...se);
  if (se.length) return { ok: false, errors, warnings, reachable_evidence: [], unreachable_evidence: [], proof_paths: 0, proof_sets: [] };

  const ids = <T extends { id: string }>(a: T[] | undefined) => new Map((a ?? []).map((x) => [x.id, x]));
  const facts = ids(c.truth.facts), claims = ids(c.truth.claims), evid = ids(c.evidence), chars = ids(c.entities.characters);
  const hyps = ids(c.hypotheses), infs = ids(c.evidence_graph.inferences), actions = ids(c.mechanics.actions);
  const locs = ids(c.entities.locations), objs = ids(c.entities.objects), orgs = ids(c.entities.organizations);
  const dup = (name: string, arr: { id: string }[]) => { const s = new Set<string>(); for (const x of arr) { if (s.has(x.id)) errors.push(`DUP ${name} id ${x.id}`); s.add(x.id); } };
  dup("fact", c.truth.facts); dup("evidence", c.evidence); dup("character", c.entities.characters); dup("action", c.mechanics.actions); dup("inference", c.evidence_graph.inferences);
  const anyEntity = (id: string) => chars.has(id) || locs.has(id) || objs.has(id) || orgs.has(id);

  // R01 references resolve
  for (const f of c.truth.facts) for (const s of f.subject_ids) if (!anyEntity(s)) errors.push(`R01 fact ${f.id}: unknown subject ${s}`);
  for (const f of c.premise.public_fact_ids) if (!facts.has(f)) errors.push(`R01 public fact ${f} undefined`);
  for (const k of c.truth.solution.key_fact_ids) if (!facts.has(k)) errors.push(`R01 key fact ${k} undefined`);
  for (const e of c.evidence) {
    for (const a of e.acquired_by_action_ids) if (!actions.has(a)) errors.push(`R01 evidence ${e.id}: unknown action ${a}`);
    for (const f of e.supports_fact_ids) if (!facts.has(f)) errors.push(`R01 evidence ${e.id}: unknown fact ${f}`);
    for (const cl of e.contradicts_claim_ids ?? []) if (!claims.has(cl)) errors.push(`R01 evidence ${e.id}: unknown claim ${cl}`);
    if (!e.limits_ar.trim()) errors.push(`X18 evidence ${e.id} has empty limits_ar`);
    if (e.kind === "lab_result" && !e.forensic_ko_ref) warnings.push(`X18 lab result ${e.id} lacks forensic_ko_ref`);
  }
  for (const a of c.mechanics.actions) {
    for (const ef of a.effects) {
      if (ef.op === "grant_evidence" && !evid.has(ef.ref_id ?? "")) errors.push(`R01 action ${a.id}: grants unknown evidence ${ef.ref_id}`);
      if (ef.op === "unlock_fact" && !facts.has(ef.ref_id ?? "")) errors.push(`R01 action ${a.id}: unlocks unknown fact ${ef.ref_id}`);
    }
    const r = guardRefs(a.precondition);
    r.evidence.forEach((e) => !evid.has(e) && errors.push(`R01 action ${a.id}: guard evidence ${e} unknown`));
    r.facts.forEach((f) => !facts.has(f) && errors.push(`R01 action ${a.id}: guard fact ${f} unknown`));
  }
  for (const i of c.evidence_graph.inferences) {
    for (const p of i.premises) {
      if (p.ref_type === "evidence" && !evid.has(p.ref_id)) errors.push(`R01 inference ${i.id}: premise evidence ${p.ref_id} unknown`);
      if (p.ref_type === "fact" && !facts.has(p.ref_id)) errors.push(`R01 inference ${i.id}: premise fact ${p.ref_id} unknown`);
      if (p.ref_type === "inference" && !infs.has(p.ref_id)) errors.push(`R01 inference ${i.id}: premise inference ${p.ref_id} unknown`);
    }
    const t = i.conclusion;
    const okc = t.ref_type === "fact" ? facts.has(t.ref_id) : t.ref_type === "hypothesis" ? hyps.has(t.ref_id) : claims.has(t.ref_id);
    if (!okc) errors.push(`R01 inference ${i.id}: conclusion ${t.ref_type}:${t.ref_id} unknown`);
  }

  // Reachability (FP: no hidden-fact dependency)
  const { ev: reach } = reachableSets(c);
  const unreachable = c.evidence.filter((e) => !reach.has(e.id)).map((e) => e.id);
  for (const e of unreachable) errors.push(`FP unreachable evidence ${e}: no action path grants it`);
  for (const e of c.evidence) {
    if (!e.acquired_by_action_ids.some((a) => actions.get(a)?.effects.some((x) => x.op === "grant_evidence" && x.ref_id === e.id)))
      warnings.push(`evidence ${e.id}: declared acquired_by actions do not grant it`);
  }

  // Key facts established
  const sets = minimalProofSets(c);
  const paths = maxDisjoint(sets);
  const req = c.fairness_test.requirements as { min_disjoint_proof_paths?: number };
  if (sets.length === 0) errors.push("FP-02 no evidence subset derives all key facts through the inference graph");
  if (paths < (req.min_disjoint_proof_paths ?? 2)) errors.push(`FP proof paths ${paths} < required ${req.min_disjoint_proof_paths ?? 2}`);

  // Spoiler-3 never public / unconditionally known
  for (const f of c.truth.facts.filter((x) => x.spoiler_level === 3)) {
    if (c.premise.public_fact_ids.includes(f.id)) errors.push(`X09 spoiler-3 fact ${f.id} is public`);
  }
  // Knowledge scopes
  const hiddenByChar = new Map<string, Set<string>>();
  for (const k of c.character_knowledge) {
    if (!chars.has(k.character_id)) errors.push(`R01 knowledge scope for unknown character ${k.character_id}`);
    const hid = new Set(k.hides.map((h) => h.fact_id)); hiddenByChar.set(k.character_id, hid);
    for (const kn of k.knows) {
      if (!facts.has(kn.fact_id)) errors.push(`R01 ${k.character_id} knows unknown fact ${kn.fact_id}`);
      if (kn.access === "told_by" && !kn.source_character_id) errors.push(`X02 ${k.character_id}/${kn.fact_id}: told_by needs source_character_id`);
      if (facts.get(kn.fact_id)?.spoiler_level === 3 && !hid.has(kn.fact_id) && chars.get(k.character_id)?.role !== "expert")
        warnings.push(`X09 ${k.character_id} unconditionally knows spoiler-3 fact ${kn.fact_id}`);
    }
    for (const h of k.hides) {
      if (!facts.has(h.fact_id)) errors.push(`R01 ${k.character_id} hides unknown fact ${h.fact_id}`);
      if (h.cover_claim_id && !claims.has(h.cover_claim_id)) errors.push(`R01 ${k.character_id} cover claim ${h.cover_claim_id} unknown`);
      const r = guardRefs(h.reveal_when);
      r.evidence.forEach((e) => !reach.has(e) && errors.push(`FP reveal of ${h.fact_id} depends on unreachable evidence ${e}`));
    }
    for (const b of k.believes) if (!claims.has(b.claim_id)) errors.push(`R01 ${k.character_id} believes unknown claim ${b.claim_id}`);
  }
  // Authored lines must stay inside the character's knowledge
  for (const ch of c.entities.characters) {
    const ks = c.character_knowledge.find((k) => k.character_id === ch.id);
    const allowed = new Set([...(ks?.knows.map((x) => x.fact_id) ?? []), ...(ks?.hides.map((x) => x.fact_id) ?? [])]);
    const claimsOk = new Set(ks?.believes.map((b) => b.claim_id) ?? []);
    for (const l of ch.authored_lines ?? []) {
      for (const f of l.fact_ids ?? []) if (!allowed.has(f)) errors.push(`NR line ${l.line_id}: ${ch.id} voices fact ${f} outside its knowledge scope`);
      for (const cl of l.claim_ids ?? []) if (!claimsOk.has(cl)) errors.push(`NR line ${l.line_id}: ${ch.id} voices claim ${cl} it does not hold`);
    }
  }
  // Claims contradicted by reachable evidence
  for (const cl of c.truth.claims ?? []) {
    const ok = c.evidence.some((e) => reach.has(e.id) && (e.contradicts_claim_ids ?? []).includes(cl.id)) ||
      c.evidence_graph.inferences.some((i) => i.relation === "contradicts_claim" && i.conclusion.ref_id === cl.id);
    if (!ok && !cl.unresolved_by_design) errors.push(`X13 claim ${cl.id} is not contradicted by reachable evidence and not unresolved_by_design`);
  }
  // Red herrings refutable
  for (const r of c.misdirection_plan ?? []) {
    if (!hyps.has(r.points_to_hypothesis_id)) errors.push(`R01 red herring ${r.id}: unknown hypothesis`);
    for (const i of r.refuted_by_inference_ids) if (!infs.has(i)) errors.push(`R01 red herring ${r.id}: unknown inference ${i}`);
    if (!r.fairness_note_ar.trim()) errors.push(`FP-09 red herring ${r.id}: empty fairness note`);
  }
  // Hypotheses
  if (!c.hypotheses.some((h) => !h.suspect_id)) warnings.push("X23 no hypothesis without a suspect (innocent explanation)");
  if (c.hypotheses.filter((h) => h.is_true).length < 1) errors.push("hypotheses: none marked true");
  for (const h of c.hypotheses) if (h.is_true && h.suspect_id && !c.truth.solution.culprit_ids.includes(h.suspect_id)) errors.push(`X16 true hypothesis ${h.id}: suspect not in culprit_ids`);
  for (const cid of c.truth.solution.culprit_ids) {
    const ch = chars.get(cid);
    if (!ch) errors.push(`culprit ${cid} unknown`);
    else if (["assistant", "expert", "authority"].includes(ch.role)) errors.push(`X17 culprit ${cid} is ${ch.role} (NR-07)`);
  }
  // Hint ladders
  const byTarget = new Map<string, number[]>();
  for (const h of c.hint_ladder) { const k = h.targets_inference_id ?? "_general"; byTarget.set(k, [...(byTarget.get(k) ?? []), h.level]); if (h.targets_inference_id && !infs.has(h.targets_inference_id)) errors.push(`X14 hint ${h.id}: unknown inference`); }
  for (const [t, lv] of byTarget) { const s = [...new Set(lv)].sort(); if (s[0] !== 1 || s.some((x, i) => x !== i + 1)) errors.push(`X14 hint levels for ${t} not contiguous from 1: ${s.join(",")}`); }
  // Rubric coverage
  const covered = new Set(c.rubric.criteria.flatMap((r) => r.objective_ids));
  for (const lo of c.learning_objectives) if (!covered.has(lo.id)) errors.push(`X07 learning objective ${lo.id} not covered by any rubric criterion`);
  const wsum = c.rubric.criteria.reduce((s, r) => s + (r.weight ?? 0), 0);
  if (Math.abs(wsum - 1) > 0.001) warnings.push(`rubric weights sum to ${wsum.toFixed(2)}, expected 1.00`);
  // Ending references
  for (const s of c.ending_explanation.steps) {
    if (!infs.has(s.inference_id)) errors.push(`X22 ending step ${s.order}: unknown inference ${s.inference_id}`);
    for (const e of s.uses_evidence_ids) if (!evid.has(e)) errors.push(`X22 ending step ${s.order}: unknown evidence ${e}`);
  }
  // Timeline: same actor in two places at overlapping times
  const evs = c.timeline.filter((t) => t.location_id);
  for (let i = 0; i < evs.length; i++) for (let j = i + 1; j < evs.length; j++) {
    const a = evs[i]!, b = evs[j]!;
    if (a.location_id === b.location_id) continue;
    const ae = a.time.end_min ?? a.time.start_min, be = b.time.end_min ?? b.time.start_min;
    if (a.time.start_min <= be && b.time.start_min <= ae && a.actor_ids.some((x) => b.actor_ids.includes(x))) errors.push(`X03 ${a.id}/${b.id}: same actor in two places at overlapping times`);
  }
  for (const t of c.timeline) if (t.actor_ids.length && !t.motivated_by_ar) errors.push(`X04 timeline ${t.id}: actors but no motivated_by_ar`);
  // Age policy
  if (c.meta.age_band === "13-15") {
    const fl = new Set(c.meta.content_flags);
    if (fl.has("non_graphic_crime") || !fl.has("no_violence")) errors.push("X19 13-15 case must be flagged no_violence and not non_graphic_crime");
  }
  // Language gates
  for (const [p, s] of strings(c)) {
    if (p.includes("/fairness_test") || p.includes("/expert_review")) continue;
    if (RTL_BAD.test(s)) errors.push(`X25 ${p}: presentation form / bidi control char`);
    for (const a of ABSOLUTE_AR) if (s.includes(a)) errors.push(`X24 ${p}: absolute claim "${a}"`);
    if (s.includes("نسبة الأرجحية")) errors.push(`X24 ${p}: use "نسبة الترجيح"`);
    if (s.includes("سلسلة الحيازة")) errors.push(`X24 ${p}: use "سلسلة العهدة"`);
  }
  for (const i of c.evidence_graph.inferences) for (const d of DEMEANOUR_AR) if (i.rule_ar.includes(d)) errors.push(`X28 inference ${i.id}: demeanour/physiognomy cue "${d}"`);

  return { ok: errors.length === 0, errors, warnings, reachable_evidence: [...reach], unreachable_evidence: unreachable, proof_paths: paths, proof_sets: sets };
}

/** SHA-256 of canonical JSON without fairness runs/reviews (binds reviews to exact content). */
export async function contentHash(c: CaseFile): Promise<string> {
  const { createHash } = await import("node:crypto");
  const copy = structuredClone(c) as unknown as Record<string, unknown>;
  (copy.fairness_test as { runs?: unknown })?.runs !== undefined && delete (copy.fairness_test as { runs?: unknown }).runs;
  delete copy.expert_review;
  const canon = (o: unknown): unknown => Array.isArray(o) ? o.map(canon) : o && typeof o === "object" ? Object.fromEntries(Object.keys(o as object).sort().map((k) => [k, canon((o as Record<string, unknown>)[k])])) : o;
  return "sha256:" + createHash("sha256").update(JSON.stringify(canon(copy))).digest("hex");
}
