import { readFileSync } from "node:fs";
import { join } from "node:path";
import { z } from "zod";
import { SKILLS } from "./books-labels";

const Age = z.enum(["all", "13-15", "16-18", "18+"]);
const Safety = z.enum(["safe", "conceptual", "sensitive"]);
const Skill = z.enum(SKILLS);

export const SectionSchema = z.object({
  id: z.string(), title_ar: z.string().min(1), line_start: z.number().int(), line_end: z.number().int(),
  inclusion: z.enum(["included", "excluded"]), reason_code: z.string(), reason_ar: z.string().min(1), note_count: z.number().int().min(0),
});
export const BookSchema = z.object({
  id: z.string().regex(/^BK-\d+$/), title_ar: z.string().min(1), authors_ar: z.array(z.string()), year: z.number().nullable(), edition_ar: z.string(),
  hook_ar: z.string().min(1), rights: z.literal("protected"), use: z.literal("concept-notes-only"), rights_note_ar: z.string().min(1),
  teen_facing: z.boolean(), sections: z.array(SectionSchema).min(1), section_count: z.number(), included_count: z.number(), excluded_count: z.number(), note_count: z.number(),
});
export type Book = z.infer<typeof BookSchema>;

export const ConceptSchema = z.object({
  id: z.string().regex(/^BKC-\d{3}$/), book_id: z.string().regex(/^BK-\d+$/), section_id: z.string(), section_title_ar: z.string(), ref_ar: z.string(),
  line_start: z.number().int().positive(), line_end: z.number().int().positive(),
  title_ar: z.string().min(1), summary_ar: z.string().min(1), investigation_use_ar: z.string().min(1), limits_ar: z.string().min(1),
  myth_ar: z.string().nullable(), age_band: Age, safety_level: Safety, skill: Skill,
  linked_ko_ids: z.array(z.string().regex(/^KO-[A-Z0-9]+-\d{2}[A-Z]?-\d{3}$/)), glossary: z.array(z.string()),
});
export type BookConcept = z.infer<typeof ConceptSchema>;

export const DrillSchema = z.object({
  id: z.string().regex(/^DRL-\d{3}$/), skill: Skill, scenario_ar: z.string().min(1), question_ar: z.string().min(1),
  options: z.array(z.object({ id: z.string(), text_ar: z.string().min(1) })).min(3).max(4), answer_id: z.string(),
  explanation_ar: z.string().min(1), age_band: Age, safety_level: Safety, linked_ko_ids: z.array(z.string()),
}).refine((d) => d.options.some((o) => o.id === d.answer_id), { message: "answer_id must match an option" });
export type Drill = z.infer<typeof DrillSchema>;

type Cache = { books: Book[]; concepts: BookConcept[]; drills: Drill[] };
const g = globalThis as typeof globalThis & { __atharBooks?: Cache };
const rd = (root: string, f: string) => JSON.parse(readFileSync(join(root, "content/knowledge/books", f), "utf8"));
export function loadBooks(root = process.cwd()): Cache {
  if (g.__atharBooks) return g.__atharBooks;
  const meta = { expert_review: z.literal("pending") };
  g.__atharBooks = {
    books: z.object({ ...meta, books: z.array(BookSchema) }).parse(rd(root, "books.json")).books,
    concepts: z.object({ ...meta, concepts: z.array(ConceptSchema) }).parse(rd(root, "concepts.json")).concepts,
    drills: z.object({ ...meta, drills: z.array(DrillSchema) }).parse(rd(root, "drills.json")).drills,
  };
  return g.__atharBooks;
}

export type Band = "13-15" | "16-17" | "18+" | null;
/** Age gate: unknown age sees the most conservative set; sensitive notes and non-teen-facing books are adults only. */
export function visibleConcepts(items: BookConcept[], books: Book[], band: Band): BookConcept[] {
  const adult = band === "18+";
  const ok = (a: BookConcept["age_band"]) => a === "all" || (a === "13-15" && true) || (a === "16-18" && (band === "16-17" || adult)) || (a === "18+" && adult);
  const teen = new Set(books.filter((b) => b.teen_facing).map((b) => b.id));
  return items.filter((c) => ok(c.age_band) && (adult || (c.safety_level !== "sensitive" && teen.has(c.book_id))));
}
export function visibleBooks(books: Book[], band: Band): Book[] {
  return books.filter((b) => b.teen_facing || band === "18+");
}
export function drillsFor(drills: Drill[], band: Band): Drill[] {
  return drills.filter((d) => d.age_band !== "18+" || band === "18+");
}
export * from "./books-labels";
