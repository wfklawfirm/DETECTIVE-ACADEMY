import { existsSync, readdirSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { z } from "zod";
import { loadKnowledge, visibleKos, type Band, type Ko, type Source } from "./knowledge";

export * from "./reference-labels";

const ids = z.array(z.string());
const str = z.string();

export const GlossaryItem = z.object({
  id: z.string().regex(/^GL-\d{3}$/), term_en: str, term_ar: str.min(1), alts_ar: ids, def_ar: str.min(1), cat: str,
  level: z.enum(["13-15", "16-18", "18+"]), status: z.enum(["sourced", "variant", "proposed"]), tier: str, letter: str.length(1),
  src_ids: ids, ko_ids: ids,
});
export const GlossaryFile = z.object({
  version: str, hook_ar: str.min(1), categories: z.array(z.object({ id: str, label_ar: str, count: z.number() })), items: z.array(GlossaryItem),
});
export type GlossaryEntry = z.infer<typeof GlossaryItem>;

export const MethodItem = z.object({
  id: z.string().regex(/^M\d\d$/), name_en: str, name_ar: str.min(1), hook_ar: str.min(1), discipline_en: str, discipline_ar: str,
  tier: z.enum(["strong", "conditional", "open", "unsupported", "process", "analogue"]), min_band: z.enum(["all", "18+"]),
  can_ar: ids.min(1), cannot_ar: ids.min(1), errors_ar: ids.min(1), suitability_en: str, in_mvp: str, confidence: str, standards_en: str,
  original_en: z.object({ validity: str, error_rate: str, concerns: str }), src_ids: ids, ko_ids: ids,
});
export const MethodsFile = z.object({ version: str, hook_ar: str.min(1), tiers: z.record(z.string(), z.string()), items: z.array(MethodItem) });
export type MethodEntry = z.infer<typeof MethodItem>;

export const BiasItem = z.object({
  id: z.string().regex(/^B\d\d$/), name_ar: str.min(1), name_en: str, research_ar: str, debrief_ar: str, golden_rule_ar: str, example_ar: str.min(1), src_ids: ids, ko_ids: ids,
});
export const BiasesFile = z.object({ version: str, hook_ar: str.min(1), balance_ar: str.min(1), self_correcting_ar: ids, items: z.array(BiasItem) });
export type BiasEntry = z.infer<typeof BiasItem>;

export const ReasoningFile = z.object({
  version: str, hook_ar: str.min(1),
  errors: z.array(z.object({ n: z.number(), name_ar: str.min(1), name_en: str, definition_ar: str.min(1), limits_ar: str, strength_ar: str, practice_ar: str.min(1), src_ids: ids, ko_ids: ids })),
  evidence_types: z.array(z.object({ kind_ar: str, def_ar: str, example_ar: str })),
  criteria: z.array(z.object({ n: z.number(), name_ar: str.min(1), name_en: str, ask_ar: str.min(1), extra_ar: ids, pro_ar: str, src_ids: ids })),
  uncertainty: z.object({ ladder: z.array(z.object({ level: z.number(), phrase_ar: str, range: str })), teen_ar: str }),
  pocket_questions: ids,
  ethics: z.array(z.object({ n: z.number(), name_ar: str.min(1), name_en: str, learn_ar: str.min(1), commitments_ar: ids, src_ids: ids })),
  skills: z.array(z.object({ id: str, name_ar: str.min(1), name_en: str, area_ar: str, def_ar: str, mistakes_ar: str, src_ids: ids })),
  assessment_notes_ar: ids,
});
export type ReasoningData = z.infer<typeof ReasoningFile>;

export const RulebookFile = z.object({
  version: str, hook_ar: str.min(1),
  sections: z.array(z.object({
    letter: str, id: str, title_ar: str.min(1), plain_ar: str.min(1), icon: z.enum(["magnifier", "speech", "flask", "scale", "shield"]),
    rules: z.array(z.object({ code: str, rule_ar: str.min(1), breakable: z.boolean(), origin_ar: str })),
  })),
  breakable_ar: ids,
  hints: z.object({
    title_ar: str, ladder: z.array(z.object({ level: z.number(), name_ar: str, shows_ar: str })), rules_ar: ids, product_note_ar: str, src_ids: ids,
  }),
});
export type RulebookData = z.infer<typeof RulebookFile>;

export const AtlasFile = z.object({
  version: str, hook_ar: str.min(1), hooks: z.record(z.string(), z.string()), rights_note_ar: str,
  principles: z.array(z.object({ n: z.number(), title_ar: str.min(1), section_ar: str, principle_ar: str, basis_ar: str, why_ar: str, src_ids: ids })),
  expansion: z.array(z.object({ n: z.number(), title_ar: str.min(1), principle_ar: str, basis_ar: str, why_ar: str, src_ids: ids })),
  corpus: z.array(z.object({ work_ar: str.min(1), author_ar: str, era_ar: str, kind_ar: str, idea_ar: str, src_ids: ids })),
  heritage: z.array(z.object({ id: str, title_ar: str.min(1), basis_ar: str, src_ids: ids })),
  heritage_limits_ar: ids,
  patterns: z.array(z.object({ n: z.number(), name_ar: str.min(1), name_en: str, def_ar: str, pros_ar: str, cons_ar: str, diff: z.number(), a13: str, a16: str, a18: str })),
  avoid_ar: ids, myths_ar: ids,
  works: z.array(z.object({ title: str, author: str, year: str, rights_ar: str })),
});
export type AtlasData = z.infer<typeof AtlasFile>;

export const ArchetypeItem = z.object({
  id: z.string().regex(/^ARC-\d\d$/), name_ar: str.min(1), name_en: str, core_ar: str.min(1), teaches_ar: ids, concepts_ar: ids, pattern_ar: ids, observables_ar: str,
  narrative_pattern_kos: ids, age_band: z.enum(["13-15", "16-18", "18+"]), age_variant_ar: str, violence: z.enum(["V0", "V1", "V2", "V3"]), violence_ar: str, no_culprit: z.boolean(),
  warnings_ar: ids, settings_ar: ids, lab_ar: str, status: str, min_band: z.enum(["all", "18+"]),
});
export const ArchetypesFile = z.object({ version: str, hook_ar: str.min(1), items: z.array(ArchetypeItem) });
export type ArchetypeEntry = z.infer<typeof ArchetypeItem>;

export const ExcludedFile = z.object({ version: str, note_ar: str, items: z.array(z.object({ page: str, id: str, title: str, kind: str, reason: str.min(5) })) });
export const CountsFile = z.object({ version: str, counts: z.record(z.string(), z.record(z.string(), z.object({ in: z.number(), out: z.number() }))) });

const g = globalThis as typeof globalThis & { __atharRef?: Map<string, unknown> };
function load<T>(file: string, schema: z.ZodType<T>, root = process.cwd()): T {
  const cache = (g.__atharRef ??= new Map());
  const key = join(root, file);
  if (cache.has(key)) return cache.get(key) as T;
  const v = schema.parse(JSON.parse(readFileSync(join(root, "content/reference", file), "utf8")));
  cache.set(key, v);
  return v;
}
export const loadGlossary = (root?: string) => load("glossary.json", GlossaryFile, root);
export const loadMethods = (root?: string) => load("methods.json", MethodsFile, root);
export const loadBiases = (root?: string) => load("biases.json", BiasesFile, root);
export const loadReasoning = (root?: string) => load("reasoning.json", ReasoningFile, root);
export const loadRulebook = (root?: string) => load("rulebook.json", RulebookFile, root);
export const loadAtlas = (root?: string) => load("atlas.json", AtlasFile, root);
export const loadArchetypes = (root?: string) => load("archetypes.json", ArchetypesFile, root);
export const loadExcluded = (root?: string) => load("excluded.json", ExcludedFile, root);
export const loadCounts = (root?: string) => load("counts.json", CountsFile, root);

/** Adults (an account, or a device that declared 18+) see everything; a minor or an unknown age sees the conservative set. */
export const isAdult = (band: Band): boolean => band === "18+";
export function glossaryFor(items: GlossaryEntry[], band: Band): GlossaryEntry[] {
  return items.filter((i) => i.level !== "18+" || isAdult(band));
}
export function gated<T extends { min_band: "all" | "18+" }>(items: T[], band: Band): T[] {
  return items.filter((i) => i.min_band === "all" || isAdult(band));
}

/** Resolve knowledge-object ids to links the viewer may open (same visibility rule as /knowledge). */
export function koLinks(koIds: string[], band: Band): { id: string; name: string }[] {
  const { kos } = loadKnowledge();
  const vis = new Map(visibleKos(kos, band).map((k: Ko) => [k.ko_id, k.name_ar]));
  return koIds.filter((i) => vis.has(i)).map((i) => ({ id: i, name: vis.get(i)! }));
}

/** Source titles for a card's "sources" disclosure. Protected sources are listed as references only (the page never excerpts them). */
export function sourceRefs(srcIds: string[]): Source[] {
  const { src } = loadKnowledge();
  const byId = new Map(src.map((s) => [s.id, s]));
  return srcIds.map((i) => byId.get(i)).filter((s): s is Source => !!s);
}

export interface CaseUse { case_id: string; title_ar: string; age_band: string }
/**
 * Which existing cases already use each archetype. The case files carry no archetype tag, so a case "uses" an archetype
 * when its meta.knowledge_object_refs shares a narrative-pattern KO with the archetype (or the case lists the archetype
 * id in meta.tags / meta.archetype_ids if a future case declares it). This is a heuristic, shown to the player as such.
 */
export function archetypeCaseUse(arcs: ArchetypeEntry[], dir = join(process.cwd(), "content/cases")): Map<string, CaseUse[]> {
  const out = new Map<string, CaseUse[]>(arcs.map((a) => [a.id, []]));
  if (!existsSync(dir)) return out;
  for (const f of readdirSync(dir).sort()) {
    if (!f.endsWith(".json") || f.endsWith(".ui.json") || f.endsWith(".scoring.json")) continue;
    let meta: Record<string, unknown> | undefined, case_id = f.replace(/\.json$/, "");
    try { const d = JSON.parse(readFileSync(join(dir, f), "utf8")) as { case_id?: string; meta?: Record<string, unknown> }; meta = d.meta; case_id = d.case_id ?? case_id; } catch { continue; }
    if (!meta) continue;
    const refs = new Set(Array.isArray(meta.knowledge_object_refs) ? (meta.knowledge_object_refs as string[]) : []);
    const declared = new Set<string>([...(Array.isArray(meta.tags) ? (meta.tags as string[]) : []), ...(Array.isArray(meta.archetype_ids) ? (meta.archetype_ids as string[]) : [])]);
    for (const a of arcs) {
      if (declared.has(a.id) || a.narrative_pattern_kos.some((k) => refs.has(k))) {
        out.get(a.id)!.push({ case_id, title_ar: String(meta.title_ar ?? case_id), age_band: String(meta.age_band ?? "all") });
      }
    }
  }
  return out;
}

/** Letters present in the glossary, in Arabic alphabetical order. */
export const ARABIC_ORDER = "ابتثجحخدذرزسشصضطظعغفقكلمنهوي".split("");
export const sortLetters = (ls: string[]): string[] => [...new Set(ls)].sort((a, b) => ARABIC_ORDER.indexOf(a) - ARABIC_ORDER.indexOf(b));
