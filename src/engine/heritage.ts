import { readFileSync } from "node:fs";
import { join } from "node:path";
import { z } from "zod";

/**
 * Public heritage library: a catalogue of public-domain detective/reasoning texts with short attributed excerpts.
 * Excerpts exist ONLY for texts whose rights verdict is public-domain / CC0 (see tools/generators/build_heritage.py).
 * CC BY-NC material (OpenITI etc.) and anything unconfirmed is catalogue-only, with a clear label.
 */
export const RIGHTS = ["pd_verified", "pd_cc0", "cc_by_nc_ref"] as const;
export const TextSchema = z.object({
  id: z.string().regex(/^[a-z0-9-]+$/), asset_id: z.string(), source_id: z.string().nullable(), kind: z.string(),
  title: z.string(), title_ar: z.string(), author: z.string(), author_ar: z.string(), era_ar: z.string(), year: z.number().nullable(),
  lang: z.enum(["en", "fr", "ja", "zh", "ar"]), lang_ar: z.string(), licence: z.string(), licence_basis: z.string(), source_url: z.string(), digitization: z.string(),
  rights: z.enum(RIGHTS), rights_ar: z.string(), excerptable: z.boolean(), reference_reason_ar: z.string().nullable(), ebook_no: z.string().nullable(),
  file: z.string(), sha256: z.string(), excerpt_count: z.number(), edit_note_ar: z.string().optional(),
});
export type HText = z.infer<typeof TextSchema>;
export const ExcerptSchema = z.object({
  id: z.string(), text_id: z.string(), n: z.number(), lang: z.enum(["en", "fr", "ja", "zh", "ar"]), text: z.string(), words: z.number(), locator: z.string(),
  skill: z.string(), skill_ar: z.string(), hook_ar: z.string(), gloss_ar: z.string(), attribution: z.string(),
});
export type HExcerpt = z.infer<typeof ExcerptSchema>;

const g = globalThis as typeof globalThis & { __atharHeritage?: { texts: HText[]; excerpts: HExcerpt[] } };
export function loadHeritage(root = process.cwd()): { texts: HText[]; excerpts: HExcerpt[] } {
  if (g.__atharHeritage) return g.__atharHeritage;
  const rd = (n: string) => JSON.parse(readFileSync(join(root, "content/heritage", n), "utf8"));
  const texts = z.object({ items: z.array(TextSchema) }).parse(rd("catalog.json")).items;
  const excerpts = z.object({ items: z.array(ExcerptSchema) }).parse(rd("excerpts.json")).items;
  g.__atharHeritage = { texts, excerpts };
  return g.__atharHeritage;
}

export const RIGHTS_LABEL: Record<HText["rights"], string> = {
  pd_verified: "ملك عام موثّق", pd_cc0: "ملك عام + CC0", cc_by_nc_ref: "مرجع فقط: ترخيص غير تجاري (CC BY-NC-SA)",
};
export const LANG_ORDER: HText["lang"][] = ["ar", "en", "fr", "ja", "zh"];
export const LANG_NAME: Record<HText["lang"], string> = { ar: "العربية", en: "الإنجليزية", fr: "الفرنسية", ja: "اليابانية", zh: "الصينية" };
/** `ar` is a text DIRECTION decision: only Arabic-script excerpts may be rtl. */
export const dirFor = (lang: string) => (lang === "ar" ? "rtl" : "ltr");

export function excerptsFor(excerpts: HExcerpt[], textId: string): HExcerpt[] {
  return excerpts.filter((e) => e.text_id === textId).sort((a, b) => a.n - b.n);
}
/** Invariant used by tests and the page: an excerpt is shown only for an excerptable PD/CC0 text. */
export function showable(t: HText, ex: HExcerpt[]): HExcerpt[] {
  return t.excerptable && (t.rights === "pd_verified" || t.rights === "pd_cc0") ? ex : [];
}
export function safeUrl(u: string): string | null {
  return /^https:\/\/[^\s<>"']+$/i.test(u) ? u : null;
}
