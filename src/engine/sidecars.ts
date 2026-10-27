import { z } from "zod";
import type { CaseFile } from "./types";
import type { CaseUi, ScoringSpec } from "./ui-types";

const id = z.string().regex(/^[a-z][a-z0-9_]{1,63}$/);
const s = z.string().min(1).max(2000);
const dir = z.enum(["supports", "weakens", "neutral"]);

export const UiSchema = z.object({
  case_id: id,
  tutorial: z.boolean().optional(),
  clock: z.object({ epoch_hhmm: z.string().regex(/^\d{2}:\d{2}$/), zone_label_ar: s }),
  cover: z.object({ title_ar: s, tagline_ar: s, kicker_ar: s, glyph: z.string().min(1).max(4), accent: z.enum(["amber", "cyan", "rose", "green"]) }),
  cold_open_ar: z.array(s).min(1).max(8),
  labs: z.array(z.object({
    id, type: z.literal("time_normalizer"), title_ar: s, intro_ar: s, tolerance_min: z.number().min(0).max(30), epoch_utc_minute_of_day: z.number().int().min(0).max(1439),
    day_labels_ar: z.array(s).min(1).max(8), grants_evidence_on_converge: id.optional(),
    items: z.array(z.object({ evidence_id: id, label_ar: s, day: z.number().int().min(0).max(7), hhmm: z.string().regex(/^\d{1,2}:\d{2}$/), end_hhmm: z.string().regex(/^\d{1,2}:\d{2}$/).optional(), basis_ar: s.optional() })).min(2).max(10),
  })).max(6),
  source_classes: z.array(z.object({ id: z.enum(["primary_record", "redisplay", "claim", "template", "public_document"]), label_ar: s, help_ar: s })).min(2),
  limit_menu: z.array(z.object({ id, label_ar: s })).max(16),
  mind_change_menu: z.array(z.object({ id, label_ar: s })).max(16),
  transfer: z.object({
    id, title_ar: s, scenario_ar: s, prompt_ar: s, free_text_prompt_ar: s,
    documents: z.array(z.object({ title_ar: s, body_ar: s })).max(6),
    options: z.array(z.object({ id, text_ar: s })).min(4).max(12),
  }).optional(),
  skills: z.array(z.object({ skill_id: z.string().regex(/^KO-[A-Z]{2}-\d{2}[A-Z]?-\d{3}$/), track: z.enum(["A", "B", "C", "D", "E", "F"]) })),
  stage_hooks_ar: z.record(z.string(), s),
  character_glyphs: z.record(z.string(), z.string().max(4)).optional(),
});

export const ScoringSchema = z.object({
  case_id: id,
  accepted_conclusions: z.record(id, z.object({ grade: z.number().min(0).max(1), note_ar: s })),
  confidence_band: z.record(id, z.tuple([z.number().min(0).max(100), z.number().min(0).max(100)])),
  source_key: z.record(id, z.enum(["primary_record", "redisplay", "claim", "template", "public_document"])),
  link_key: z.record(id, z.record(id, dir)),
  required_limits: z.array(id), valid_mind_changers: z.array(id), invalid_limits: z.array(id), decisive_evidence: z.array(id),
  lab_requirement: z.object({ lab_id: id, must_converge: z.boolean() }).nullable(),
  timeline_requirement: z.array(z.object({ evidence_id: id, utc_minute: z.number(), tol: z.number().min(0).max(60) })).optional(),
  refuted_hypotheses: z.array(id),
  criteria_map: z.record(id, z.enum(["source_typing", "conflict_resolution", "hypothesis_links", "uncertainty", "revision", "elimination", "justification_human"])),
  transfer_key: z.object({ valid: z.array(id), invalid: z.array(id) }).optional(),
  caps: z.object({ no_citations_max: z.number().min(0).max(100), no_conflict_resolution_max: z.number().min(0).max(100) }),
});

/** Cross-reference checks between core, ui and scoring. Returns human-readable errors (empty = consistent). */
export function crossCheck(core: CaseFile, ui: CaseUi, sc: ScoringSpec): string[] {
  const e: string[] = [];
  if (ui.case_id !== core.case_id) e.push(`ui.case_id ${ui.case_id} != ${core.case_id}`);
  if (sc.case_id !== core.case_id) e.push(`scoring.case_id ${sc.case_id} != ${core.case_id}`);
  const ev = new Set(core.evidence.map((x) => x.id)), hy = new Set(core.hypotheses.map((x) => x.id)), crit = new Set(core.rubric.criteria.map((x) => x.id));
  const labs = new Set(ui.labs.map((l) => l.id));
  const lim = new Set(ui.limit_menu.map((x) => x.id)), mc = new Set(ui.mind_change_menu.map((x) => x.id));
  const chk = (ok: boolean, m: string) => { if (!ok) e.push(m); };
  for (const l of ui.labs) {
    for (const it of l.items) chk(ev.has(it.evidence_id), `ui lab ${l.id}: unknown evidence ${it.evidence_id}`);
    if (l.grants_evidence_on_converge) chk(ev.has(l.grants_evidence_on_converge), `ui lab ${l.id}: grants unknown evidence`);
  }
  for (const k of Object.keys(ui.stage_hooks_ar)) chk(["briefing", "investigating", "review", "resolved"].includes(k) || k in core.state_machine.states, `ui stage hook for unknown state ${k}`);
  for (const k of Object.keys(sc.accepted_conclusions)) chk(hy.has(k), `scoring accepted_conclusions: unknown hypothesis ${k}`);
  for (const h of core.hypotheses) chk(h.id in sc.accepted_conclusions, `scoring: hypothesis ${h.id} lacks accepted_conclusions entry`);
  for (const h of core.hypotheses) chk(h.id in sc.confidence_band, `scoring: hypothesis ${h.id} lacks confidence band`);
  for (const k of Object.keys(sc.source_key)) chk(ev.has(k), `scoring source_key: unknown evidence ${k}`);
  for (const [h, m] of Object.entries(sc.link_key)) { chk(hy.has(h), `scoring link_key: unknown hypothesis ${h}`); for (const k of Object.keys(m)) chk(ev.has(k), `scoring link_key ${h}: unknown evidence ${k}`); }
  for (const k of [...sc.required_limits, ...sc.invalid_limits]) chk(lim.has(k), `scoring: limit ${k} not in ui.limit_menu`);
  for (const k of sc.valid_mind_changers) chk(mc.has(k), `scoring: mind-changer ${k} not in ui.mind_change_menu`);
  for (const k of sc.decisive_evidence) chk(ev.has(k), `scoring decisive: unknown evidence ${k}`);
  for (const k of sc.refuted_hypotheses) chk(hy.has(k), `scoring refuted: unknown hypothesis ${k}`);
  if (sc.lab_requirement) chk(labs.has(sc.lab_requirement.lab_id), `scoring lab_requirement: unknown lab`);
  for (const t of sc.timeline_requirement ?? []) chk(ev.has(t.evidence_id), `scoring timeline: unknown evidence ${t.evidence_id}`);
  for (const k of Object.keys(sc.criteria_map)) chk(crit.has(k), `scoring criteria_map: unknown criterion ${k}`);
  for (const k of crit) chk(k in sc.criteria_map, `scoring: rubric criterion ${k} missing from criteria_map`);
  if (sc.transfer_key) {
    const opts = new Set((ui.transfer?.options ?? []).map((o) => o.id));
    chk(!!ui.transfer, "scoring has transfer_key but ui has no transfer task");
    for (const k of [...sc.transfer_key.valid, ...sc.transfer_key.invalid]) chk(opts.has(k), `scoring transfer_key: unknown option ${k}`);
    chk(sc.transfer_key.valid.length > 0 && sc.transfer_key.invalid.length > 0, "transfer_key needs both valid and invalid options");
  }
  // limit_menu items in neither list are valid-but-optional limits: neither required nor penalised.
  // answer positions: the true conclusion must not be identifiable by position alone
  const trueIds = core.hypotheses.filter((h) => h.is_true).map((h) => h.id);
  if (trueIds.length === 1 && core.hypotheses.length > 1 && core.hypotheses[0]!.id === trueIds[0] && core.hypotheses.length < 3) e.push("true hypothesis is listed first among <3 options");
  return e;
}
