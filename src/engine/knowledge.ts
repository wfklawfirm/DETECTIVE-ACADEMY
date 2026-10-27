import { readFileSync } from "node:fs";
import { join } from "node:path";
import { z } from "zod";

export const KoSchema = z.object({
  ko_id: z.string().regex(/^KO-[A-Z0-9]+-\d{2}[A-Z]?-\d{3}$/),
  type: z.enum(["forensic_concept", "reasoning_skill", "narrative_pattern", "case_mechanic", "character_design_pattern", "learning_assessment", "product_opportunity"]),
  name: z.string(),
  name_ar: z.string().min(1),
  summary_ar: z.string().min(1),
  source_ids: z.array(z.string()),
  confidence: z.enum(["high", "medium", "low"]),
  status: z.enum(["evidence_based", "design_hypothesis", "expert_practice"]),
  tags: z.array(z.string()),
  age_band: z.enum(["all", "13-15", "16-18", "18+"]),
  library: z.string(),
  audience: z.enum(["player", "studio"]),
  extra: z.record(z.string(), z.unknown()),
});
export type Ko = z.infer<typeof KoSchema>;

export const SourceSchema = z.object({
  id: z.string(), title: z.string(), title_ar: z.string().nullable(), authors: z.array(z.string()), year: z.number().nullable(),
  type: z.string().nullable(), url: z.string().nullable(), rights: z.string().nullable(), license: z.string().nullable(),
  grade: z.string().nullable(), library: z.string().nullable(), cited: z.boolean(),
});
export type Source = z.infer<typeof SourceSchema>;

const g = globalThis as typeof globalThis & { __atharKo?: { kos: Ko[]; src: Source[] } };
export function loadKnowledge(root = process.cwd()): { kos: Ko[]; src: Source[] } {
  if (g.__atharKo) return g.__atharKo;
  const ko = z.object({ items: z.array(KoSchema) }).parse(JSON.parse(readFileSync(join(root, "content/knowledge/ko.json"), "utf8")));
  const sr = z.object({ items: z.array(SourceSchema) }).parse(JSON.parse(readFileSync(join(root, "content/knowledge/sources.json"), "utf8")));
  g.__atharKo = { kos: ko.items, src: sr.items };
  return g.__atharKo;
}

export type Band = "13-15" | "16-17" | "18+" | null;
/** What a viewer may see: the player-facing types only, and 18+ items only for adults. Unknown age sees the most conservative set. */
export function visibleKos(kos: Ko[], band: Band): Ko[] {
  return kos.filter((k) => k.audience === "player" && (k.age_band !== "18+" || band === "18+"));
}

export { TYPE_LABEL, CONF_LABEL, STATUS_LABEL, RIGHTS_LABEL } from "./knowledge-labels";
