/** Arabic text normalisation used for topic matching and leak scanning (not for display). */
export function normalizeAr(s: string): string {
  return s
    .replace(/[ً-ٰٟـ]/g, "") // diacritics + tatweel
    .replace(/[آأإٱ]/g, "ا") // alef variants -> ا
    .replace(/ى/g, "ي") // ى -> ي
    .replace(/ة/g, "ه") // ة -> ه
    .replace(/[ی]/g, "ي")
    .replace(/[٠-٩]/g, (d) => String(d.charCodeAt(0) - 0x660)) // Arabic-Indic digits
    .replace(/[۰-۹]/g, (d) => String(d.charCodeAt(0) - 0x6f0))
    .toLowerCase();
}
export function tokens(s: string): string[] {
  return normalizeAr(s).split(/[^\p{L}\p{N}]+/u).filter((t) => t.length > 1);
}
const STOP = new Set(["في", "من", "على", "الى", "عن", "هل", "ما", "ماذا", "كان", "كانت", "هذا", "هذه", "ان", "او", "ثم", "قد", "لا", "لم", "لن", "انت", "انا", "هو", "هي", "كل", "مع", "الذي", "التي", "كيف", "متى", "اين", "لماذا", "ولا", "وما", "الا", "بعد", "قبل"]);
export function contentTokens(s: string): string[] {
  return tokens(s).map((t) => t.replace(/^(ال|وال|بال|لل|و)(?=.{3,})/, "")).filter((t) => !STOP.has(t) && t.length > 1);
}
export function jaccard(a: string[], b: string[]): number {
  const A = new Set(a), B = new Set(b);
  if (!A.size || !B.size) return 0;
  let i = 0; for (const x of A) if (B.has(x)) i++;
  return i / (A.size + B.size - i);
}
export function ngrams(t: string[], n: number): Set<string> {
  const out = new Set<string>(); for (let i = 0; i + n <= t.length; i++) out.add(t.slice(i, i + n).join(" ")); return out;
}
