import { contentTokens, jaccard, ngrams, tokens } from "../lib/arabic";
import type { CaseFile } from "./types";
import type { CaseUi } from "./ui-types";

export interface LeakFinding { where: string; against: string; kind: "ngram" | "similar"; sample: string }

/**
 * Static answer-leak scan. Everything the player can read BEFORE the debrief (evidence, character lines, hints below the reveal levels,
 * cold open, hooks, labs, menus) is compared with solution-level text (spoiler-3 facts, solution summary, reference answer, ending steps).
 * A shared 4-gram or high Jaccard similarity is reported; the editor must reword or justify.
 */
export function staticLeakScan(c: CaseFile, ui: CaseUi, extraPlayerTexts: { where: string; text: string }[] = []): LeakFinding[] {
  const guard: { name: string; text: string }[] = [
    { name: "solution_summary", text: c.truth.solution.summary_ar },
    { name: "reference_answer", text: c.rubric.reference_answer_ar },
    ...c.ending_explanation.steps.map((s) => ({ name: `ending_step_${s.order}`, text: s.text_ar })),
    ...c.truth.facts.filter((f) => f.spoiler_level === 3).map((f) => ({ name: `fact:${f.id}`, text: f.statement_ar })),
  ];
  const visible: { where: string; text: string }[] = [
    ...c.evidence.flatMap((e) => [{ where: `evidence:${e.id}:content`, text: e.kind === "lab_result" ? "" : e.content_ar }, // lab results are earned findings, gated by the lab
    { where: `evidence:${e.id}:title`, text: e.title_ar }, { where: `evidence:${e.id}:limits`, text: e.limits_ar }]),
    ...c.entities.characters.flatMap((ch) => [{ where: `character:${ch.id}:persona`, text: ch.persona_ar }, ...(ch.authored_lines ?? []).filter((l) => l.purpose !== "break_down" && l.purpose !== "reveal").map((l) => ({ where: `line:${l.line_id}`, text: l.text_ar }))]),
    ...c.hint_ladder.filter((h) => h.kind !== "full_reveal" && h.kind !== "partial_reveal").map((h) => ({ where: `hint:${h.id}`, text: h.text_ar })),
    { where: "premise:hook", text: c.premise.hook_ar }, { where: "premise:setting", text: c.premise.setting_ar }, { where: "premise:role", text: c.premise.player_role_ar },
    ...ui.cold_open_ar.map((t, i) => ({ where: `ui:cold_open:${i}`, text: t })),
    ...Object.entries(ui.stage_hooks_ar).map(([k, t]) => ({ where: `ui:stage_hook:${k}`, text: t })),
    { where: "ui:tagline", text: ui.cover.tagline_ar },
    ...ui.labs.map((l) => ({ where: `lab:${l.id}:intro`, text: l.intro_ar })),
    ...c.hypotheses.map((h) => ({ where: `hypothesis:${h.id}`, text: h.statement_ar })),
    ...extraPlayerTexts,
  ];
  const out: LeakFinding[] = [];
  for (const g of guard) {
    const gt = tokens(g.text);
    const gg = ngrams(gt, 4);
    const gc = contentTokens(g.text);
    for (const v of visible) {
      if (!v.text) continue;
      // hypotheses are allowed to resemble the solution (they are the options); skip hypothesis-vs-solution comparisons
      if (v.where.startsWith("hypothesis:")) continue;
      const vt = tokens(v.text);
      const shared = [...ngrams(vt, 4)].filter((x) => gg.has(x));
      if (shared.length) out.push({ where: v.where, against: g.name, kind: "ngram", sample: shared[0]! });
      else if (gc.length >= 8 && jaccard(contentTokens(v.text), gc) > 0.5) out.push({ where: v.where, against: g.name, kind: "similar", sample: v.text.slice(0, 60) });
    }
  }
  return out;
}

const FORBIDDEN_KEYS = ["is_true", "culprit_ids", "solution", "reference_answer", "reference_answer_ar", "reveal_when", "hides", "knows", "believes", "inference", "inferences", "premises", "misdirection_plan", "scoring", "accepted_conclusions", "link_key", "source_key", "required_limits", "valid_mind_changers", "decisive_evidence", "transfer_key", "plausibility_at_start", "cover_claim_id", "true_fact_id"];

/** Runtime guard: a PlayerView must never contain server-only keys. Returns the offending key paths. */
export function forbiddenKeysIn(view: unknown, allow: string[] = []): string[] {
  const hits: string[] = [];
  const walk = (o: unknown, path: string) => {
    if (Array.isArray(o)) o.forEach((x, i) => walk(x, `${path}[${i}]`));
    else if (o && typeof o === "object") {
      for (const [k, v] of Object.entries(o)) {
        if (FORBIDDEN_KEYS.includes(k) && !allow.includes(`${path}.${k}`)) hits.push(`${path}.${k}`);
        walk(v, `${path}.${k}`);
      }
    }
  };
  walk(view, "$");
  return hits;
}
