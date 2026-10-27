import { availableActions } from "./state";
import { topicsFor, interviewOpen } from "./dialogue";
import { shuffleOptions } from "./hooks";
import type { CaseFile, PlayState } from "./types";
import type { CaseUi } from "./ui-types";

/**
 * The ONLY shape of case data that may leave the server during play.
 * Hidden truth (solution, is_true, claim truth, knowledge scopes, rubric reference, inference graph, red herrings,
 * unreachable evidence) is never included. Evidence appears only after the player has obtained it.
 */
export interface PlayerView {
  case_id: string;
  case_version: string;
  title_ar: string;
  age_band: string;
  estimated_minutes: number;
  preview: boolean;
  machine: string;
  sub: string | null;
  premise: { hook_ar: string; player_role_ar: string; setting_ar: string };
  cold_open_ar: string[];
  stage_hook_ar: string | null;
  evidence: {
    id: string; title_ar: string; kind: string; content_ar: string; reliability: string; limits_ar: string;
    media?: { uri: string; alt_ar: string }[]; style?: string;
  }[];
  locked_evidence_count: number;
  facts: { id: string; statement_ar: string }[];
  characters: { id: string; name_ar: string; role_label: string; age_descriptor_ar?: string; persona_ar: string; glyph?: string; interview_open: boolean; turns_left: number; topics: { id: string; label_ar: string; examples_ar: string[]; asked: boolean }[] }[];
  locations: { id: string; name_ar: string; description_ar?: string }[];
  actions: { id: string; type: string; label_ar: string; target_id?: string }[];
  hypotheses: { id: string; statement_ar: string; entry: PlayState["hypotheses"][string] | null }[];
  source_tags: PlayState["source_tags"];
  timeline: PlayState["timeline"];
  labs: { id: string; type: string; title_ar: string; intro_ar: string; items: { evidence_id: string; label_ar: string; day: number; hhmm: string; end_hhmm?: string; basis_ar?: string }[]; tolerance_min: number; day_labels_ar: string[]; runs: { seq: number; inputs: Record<string, number | string>; output: unknown; converged: boolean }[] }[];
  hints_used: { hint_id: string; level: number; text_ar: string }[];
  journal: PlayState["journal"];
  transcript: { seq: number; char_id: string; topic_id: string; topic_label: string | null; lines: { purpose: string; text_ar: string }[] }[];
  source_classes: CaseUi["source_classes"];
  limit_menu: CaseUi["limit_menu"];
  mind_change_menu: CaseUi["mind_change_menu"];
  submission: PlayState["submission"] | null;
  debrief: { steps: CaseFile["ending_explanation"]["steps"]; alternative_paths_ar: string[]; what_evidence_could_not_show_ar: string[]; science_notes_ar: string[]; reference_answer_ar: string; solution_summary_ar: string; claims_resolved: { statement_ar: string; kind: string; truth_ar: string | null }[]; inferences: { id: string; rule_ar: string }[] } | null;
  clock: CaseUi["clock"];
  transfer_task: CaseUi["transfer"] | null;
  tutorial: boolean;
  stats: { evidence_count: number; actions_taken: number };
}

const ROLE_AR: Record<string, string> = { suspect: "شخص ذو صلة", witness: "شاهد", victim: "متضرر", expert: "خبير", assistant: "مساعد", authority: "مسؤول", bystander: "حاضر" };

export function projectView(c: CaseFile, ui: CaseUi, st: PlayState, opts: { preview: boolean }): PlayerView {
  const own = new Set(st.evidence);
  const ended = st.machine === "review" || st.machine === "resolved";
  const factMap = new Map(c.truth.facts.map((f) => [f.id, f]));
  const hintText = new Map(c.hint_ladder.map((h) => [h.id, h.text_ar]));
  const maxTurns = c.dialogue?.max_turns_per_interview ?? 12;
  return {
    case_id: c.case_id,
    case_version: c.case_version,
    title_ar: ui.cover.title_ar,
    age_band: c.meta.age_band,
    estimated_minutes: c.meta.estimated_minutes,
    preview: opts.preview,
    machine: st.machine,
    sub: st.sub,
    premise: { hook_ar: c.premise.hook_ar, player_role_ar: c.premise.player_role_ar, setting_ar: c.premise.setting_ar },
    cold_open_ar: ui.cold_open_ar,
    stage_hook_ar: ui.stage_hooks_ar[st.machine] ?? null,
    // evidence appears in the order the player obtained it (file order would leak structure)
    evidence: st.evidence.map((id) => c.evidence.find((e) => e.id === id)).filter((e): e is NonNullable<typeof e> => !!e).map((e) => ({
      id: e.id, title_ar: e.title_ar, kind: e.kind, content_ar: e.content_ar, reliability: e.reliability, limits_ar: e.limits_ar,
      media: e.media?.map((m) => ({ uri: m.uri, alt_ar: m.alt_ar })),
    })),
    locked_evidence_count: c.evidence.filter((e) => !own.has(e.id)).length,
    facts: st.facts.map((id) => factMap.get(id)).filter((f): f is NonNullable<typeof f> => !!f && f.spoiler_level <= 2).map((f) => ({ id: f.id, statement_ar: f.statement_ar })),
    characters: shuffleOptions(c.entities.characters, `${c.case_id}:${st.started_at}:chars`).map((ch) => ({
      id: ch.id, name_ar: ch.name_ar, role_label: ROLE_AR[ch.role] ?? ch.role, age_descriptor_ar: ch.age_descriptor_ar, persona_ar: ch.persona_ar,
      glyph: ui.character_glyphs?.[ch.id],
      interview_open: interviewOpen(c, st, ch.id),
      turns_left: Math.max(0, maxTurns - (st.interviews[ch.id]?.turns ?? 0)),
      topics: topicsFor(c, ch.id).map((t) => ({ id: t.id, label_ar: t.label_ar, examples_ar: t.example_questions_ar ?? [], asked: (st.interviews[ch.id]?.asked ?? []).includes(t.id) })),
    })),
    locations: c.entities.locations.map((l) => ({ id: l.id, name_ar: l.name_ar, description_ar: l.description_ar })),
    actions: st.machine === "investigating" ? availableActions(c, st).filter((a) => !a.telemetry_code?.startsWith("ASK_") && ["examine", "search_location", "interview", "request_lab_test", "present_evidence"].includes(a.type)).map((a) => ({ id: a.id, type: a.type, label_ar: a.label_ar, target_id: a.target_id })) : [],
    hypotheses: shuffleOptions(c.hypotheses, `${c.case_id}:${st.started_at}:hyps`).map((h) => ({ id: h.id, statement_ar: h.statement_ar, entry: st.hypotheses[h.id] ?? null })),
    source_tags: st.source_tags,
    timeline: st.timeline,
    labs: ui.labs.map((l) => ({ id: l.id, type: l.type, title_ar: l.title_ar, intro_ar: l.intro_ar, items: l.items.filter((i) => own.has(i.evidence_id)).map((i) => ({ ...i })), tolerance_min: l.tolerance_min, day_labels_ar: l.day_labels_ar,
      runs: st.lab_runs.filter((r) => r.lab_id === l.id).map((r) => ({ seq: r.seq, inputs: r.inputs, output: r.output, converged: r.converged })) })),
    hints_used: st.hints.map((h) => ({ hint_id: h.hint_id, level: h.level, text_ar: hintText.get(h.hint_id) ?? "" })),
    journal: st.journal,
    transcript: st.transcript.map((t) => {
      const ch = c.entities.characters.find((x) => x.id === t.char_id);
      return {
        seq: t.seq, char_id: t.char_id, topic_id: t.topic_id,
        topic_label: topicsFor(c, t.char_id).find((x) => x.id === t.topic_id)?.label_ar ?? null,
        lines: t.line_ids.map((lid) => (ch?.authored_lines ?? []).find((l) => l.line_id === lid)).filter((l): l is NonNullable<typeof l> => !!l).map((l) => ({ purpose: l.purpose, text_ar: l.text_ar })),
      };
    }),
    source_classes: ui.source_classes,
    limit_menu: ui.limit_menu,
    mind_change_menu: ui.mind_change_menu,
    submission: st.submission ?? null,
    debrief: ended ? {
      steps: c.ending_explanation.steps,
      alternative_paths_ar: c.ending_explanation.alternative_paths_ar ?? [],
      what_evidence_could_not_show_ar: c.ending_explanation.what_evidence_could_not_show_ar ?? [],
      science_notes_ar: c.ending_explanation.science_notes_ar ?? [],
      reference_answer_ar: c.rubric.reference_answer_ar,
      solution_summary_ar: c.truth.solution.summary_ar,
      claims_resolved: (c.truth.claims ?? []).map((cl) => ({ statement_ar: cl.statement_ar, kind: cl.kind, truth_ar: cl.true_fact_id ? factMap.get(cl.true_fact_id)?.statement_ar ?? null : null })),
      inferences: c.evidence_graph.inferences.map((i) => ({ id: i.id, rule_ar: i.rule_ar })),
    } : null,
    clock: ui.clock,
    transfer_task: ended ? ui.transfer ?? null : null,
    tutorial: !!ui.tutorial,
    stats: { evidence_count: st.evidence.length, actions_taken: st.seq },
  };
}
