import { readFileSync } from "node:fs";
import { join } from "node:path";
import { z } from "zod";
import { evalExpr, exprNames } from "../components/labs/expr";

/** Safe virtual labs. Every lab is a short fictional exercise, one skill, driven entirely by data (content/labs/labs.json). */
const id = z.string().min(1);
const Base = z.object({
  id: z.string().regex(/^SAFE_LABS-\d{2}$/),
  title_ar: z.string().min(2), skill_ar: z.string().min(2), intro_ar: z.string().min(10),
  hook_ar: z.string().min(8),
  transfer_ar: z.string().min(8),
  /** "What this cannot prove": shown at the end of every lab. */
  boundary_ar: z.string().min(8),
  difficulty: z.number().int().min(1).max(3),
  minutes: z.number().int().min(1).max(15),
  ko_ids: z.array(z.string()).max(6).default([]),
  illustrative_ar: z.string().optional(),
});
const Why = z.object({ id, text_ar: z.string(), why_ar: z.string() });

export const ClassifyLab = Base.extend({
  kind: z.literal("classify"),
  categories: z.array(z.object({ id, label_ar: z.string() })).min(2).max(4),
  items: z.array(Why.extend({ answer: z.string() })).min(3).max(8),
}).superRefine((l, ctx) => {
  const ids = new Set(l.categories.map((c) => c.id));
  l.items.forEach((it, i) => { if (!ids.has(it.answer)) ctx.addIssue({ code: "custom", message: `item ${it.id}: unknown answer category`, path: ["items", i] }); });
  if (new Set(l.items.map((i) => i.answer)).size < 2) ctx.addIssue({ code: "custom", message: "all items share one category" });
});
export const OrderLab = Base.extend({
  kind: z.literal("order"),
  goal_ar: z.string(),
  /** The array order IS the correct order. The runner shows a fixed shuffle. */
  steps: z.array(Why).min(3).max(8),
});
export const MatchLab = Base.extend({
  kind: z.literal("match"),
  options: z.array(z.object({ id, label_ar: z.string() })).min(3).max(8),
  pairs: z.array(Why.extend({ answer: z.string() })).min(3).max(8),
}).superRefine((l, ctx) => {
  const ids = new Set(l.options.map((o) => o.id));
  l.pairs.forEach((p, i) => { if (!ids.has(p.answer)) ctx.addIssue({ code: "custom", message: `pair ${p.id}: unknown option`, path: ["pairs", i] }); });
  if (new Set(l.pairs.map((p) => p.answer)).size !== l.pairs.length) ctx.addIssue({ code: "custom", message: "match answers must be one-to-one" });
});
const Control = z.object({ id, label_ar: z.string(), min: z.number(), max: z.number(), step: z.number().positive(), value: z.number(), unit_ar: z.string().optional() });
const Output = z.object({
  id, label_ar: z.string(), expr: z.string(), decimals: z.number().int().min(0).max(4).default(1), unit_ar: z.string().optional(),
  /** Optional plain-language reading of the number: first band whose `max` is >= value. */
  read_ar: z.array(z.object({ max: z.number(), text_ar: z.string() })).optional(),
});
export const SliderLab = Base.extend({
  kind: z.literal("slider"),
  predict: z.object({ question_ar: z.string(), options: z.array(z.object({ id, label_ar: z.string() })).min(2).max(4), answer: z.string(), why_ar: z.string() }),
  controls: z.array(Control).min(1).max(3),
  outputs: z.array(Output).min(1).max(3),
  challenge: z.object({ prompt_ar: z.string(), output: z.string(), min: z.number(), max: z.number(), hint_ar: z.string() }),
  reveal: z.object({ formula_ar: z.string(), points_ar: z.array(z.string()).min(2).max(4) }),
}).superRefine((l, ctx) => {
  const cs = new Set(l.controls.map((c) => c.id));
  if (!l.predict.options.some((o) => o.id === l.predict.answer)) ctx.addIssue({ code: "custom", message: "predict.answer is not an option" });
  if (!l.outputs.some((o) => o.id === l.challenge.output)) ctx.addIssue({ code: "custom", message: "challenge.output unknown" });
  const env = Object.fromEntries(l.controls.map((c) => [c.id, c.value]));
  for (const o of l.outputs) {
    try { const n = exprNames(o.expr); for (const v of n.vars) if (!cs.has(v)) throw new Error(`unknown variable ${v}`); const r = evalExpr(o.expr, env); if (!Number.isFinite(r)) throw new Error("not finite"); }
    catch (e) { ctx.addIssue({ code: "custom", message: `output ${o.id}: ${(e as Error).message}` }); }
  }
});
export const SpotLab = Base.extend({
  kind: z.literal("spot"),
  doc_title_ar: z.string(),
  task_ar: z.string(),
  lines: z.array(z.object({ id, text_ar: z.string(), flaw: z.object({ label_ar: z.string(), why_ar: z.string() }).nullable(), ok_ar: z.string().optional() })).min(4).max(10),
}).superRefine((l, ctx) => { if (!l.lines.some((x) => x.flaw)) ctx.addIssue({ code: "custom", message: "spot lab needs at least one flaw" }); });
export const MeasureLab = Base.extend({
  kind: z.literal("measure"),
  setup_ar: z.string(),
  tasks: z.array(z.object({
    id, prompt_ar: z.string(), unit_ar: z.string(), answer: z.number(), tolerance: z.number().nonnegative(), why_ar: z.string(),
    /** Common wrong answers, each with a note explaining the slip. */
    traps: z.array(z.object({ value: z.number(), note_ar: z.string() })).default([]),
  })).min(2).max(5),
});
export const ConcludeLab = Base.extend({
  kind: z.literal("conclude"),
  scenarios: z.array(z.object({
    id, facts_ar: z.string(), question_ar: z.string(),
    options: z.array(z.object({ id, text_ar: z.string(), verdict: z.enum(["best", "overreach", "too_weak", "off_topic"]), why_ar: z.string() })).min(3).max(4),
  })).min(2).max(4),
}).superRefine((l, ctx) => l.scenarios.forEach((s, i) => { if (s.options.filter((o) => o.verdict === "best").length !== 1) ctx.addIssue({ code: "custom", message: `scenario ${s.id} needs exactly one best option`, path: ["scenarios", i] }); }));

export const LabSchema = z.discriminatedUnion("kind", [ClassifyLab, OrderLab, MatchLab, SliderLab, SpotLab, MeasureLab, ConcludeLab]);
export type Lab = z.infer<typeof LabSchema>;
export type LabKind = Lab["kind"];
export type LabOf<K extends LabKind> = Extract<Lab, { kind: K }>;
export const KIND_LABEL: Record<LabKind, string> = {
  classify: "صنّف في خانات", order: "رتّب الخطوات", match: "طابق الأزواج", slider: "نموذج بمنزلقات", spot: "اكتشف الخلل في وثيقة", measure: "قِس واحسب", conclude: "اختر الاستنتاج المسوَّغ",
};

export const LabsFileSchema = z.object({
  version: z.string(),
  catalogue: z.array(z.object({
    id: z.string(), title_ar: z.string(), interaction_ar: z.string(), skill_ar: z.string(), boundary_ar: z.string(), playable: z.boolean(),
    kind: z.string().optional(), difficulty: z.number().int().min(1).max(3).optional(), minutes: z.number().int().optional(), ko_ids: z.array(z.string()).optional(),
    origin_ar: z.string().optional(),
  })),
  playable: z.array(LabSchema),
  /** Candidates reviewed and not built, with the reason. */
  declined: z.array(z.object({ title_ar: z.string(), source: z.string(), reason_ar: z.string() })).default([]),
});
export type LabsFile = z.infer<typeof LabsFileSchema>;

export function loadKoNames(root = process.cwd()): Record<string, string> {
  return JSON.parse(readFileSync(join(root, "content/knowledge/ko_names.json"), "utf8")) as Record<string, string>;
}
export function loadLabs(root = process.cwd()) {
  const f = LabsFileSchema.parse(JSON.parse(readFileSync(join(root, "content/labs/labs.json"), "utf8")));
  const ids = new Set(f.catalogue.map((c) => c.id));
  for (const l of f.playable) if (!ids.has(l.id)) throw new Error(`playable lab ${l.id} missing from catalogue`);
  return f;
}
