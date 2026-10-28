import { readFileSync } from "node:fs";
import { join } from "node:path";
import { describe, expect, it } from "vitest";
import { dirFor, excerptsFor, loadHeritage, safeUrl, showable } from "@/engine/heritage";

const { texts, excerpts } = loadHeritage();
const byId = new Map(texts.map((t) => [t.id, t]));
const wordsOf = (e: { text: string; lang: string }) => (e.lang === "ja" || e.lang === "zh" ? e.text.replace(/\s/g, "").length / 2 : e.text.split(/\s+/).filter(Boolean).length);
const hasArabic = (s: string) => /[؀-ۿ]/.test(s);

describe("heritage catalogue", () => {
  it("catalogues every text with unique ids and complete metadata", () => {
    expect(texts.length).toBe(82);
    expect(new Set(texts.map((t) => t.id)).size).toBe(texts.length);
    for (const t of texts) {
      expect(t.title_ar, t.id).toBeTruthy(); expect(t.author_ar, t.id).toBeTruthy(); expect(t.era_ar, t.id).toBeTruthy();
      expect(t.licence, t.id).toBeTruthy(); expect(t.source_url, t.id).toMatch(/^https:\/\//); expect(t.sha256).toMatch(/^[0-9a-f]{64}$/);
    }
  });
  it("counts: excerpted + reference-only = catalogued, and the summary matches the data", () => {
    const summary = JSON.parse(readFileSync(join(process.cwd(), "content/heritage/summary.json"), "utf8"));
    expect(summary.texts).toBe(texts.length);
    expect(summary.excerpted).toBe(texts.filter((t) => t.excerpt_count > 0).length);
    expect(summary.reference_only).toBe(texts.filter((t) => t.excerpt_count === 0).length);
    expect(summary.excerpts).toBe(excerpts.length);
  });
});

describe("heritage rights rules", () => {
  it("CC BY-NC (OpenITI) and unconfirmed-licence texts have NO excerpts", () => {
    const nc = texts.filter((t) => t.rights === "cc_by_nc_ref");
    expect(nc.length).toBe(11);
    for (const t of nc) { expect(t.excerptable).toBe(false); expect(t.excerpt_count).toBe(0); expect(excerpts.some((e) => e.text_id === t.id), t.id).toBe(false); expect(t.reference_reason_ar).toBeTruthy(); }
    // the page-level filter is a second line of defence
    const fake = { ...texts.find((t) => t.rights === "pd_verified")!, rights: "cc_by_nc_ref" as const };
    expect(showable(fake, [excerpts[0]!])).toEqual([]);
  });
  it("every excerpt belongs to an excerptable PD/CC0 text and is attributed", () => {
    for (const e of excerpts) {
      const t = byId.get(e.text_id)!;
      expect(t, e.id).toBeTruthy();
      expect(t.excerptable, e.id).toBe(true);
      expect(["pd_verified", "pd_cc0"]).toContain(t.rights);
      expect(e.attribution).toContain(t.asset_id);
      expect(e.lang).toBe(t.lang);
    }
  });
  it("each excerpted text has 2 to 6 excerpts of at most 120 words, each with an Arabic hook and gloss", () => {
    for (const t of texts.filter((x) => x.excerpt_count > 0)) {
      const ex = excerptsFor(excerpts, t.id);
      expect(ex.length, t.id).toBe(t.excerpt_count);
      expect(ex.length, t.id).toBeGreaterThanOrEqual(2); expect(ex.length, t.id).toBeLessThanOrEqual(6);
    }
    for (const e of excerpts) {
      expect(wordsOf(e), e.id).toBeLessThanOrEqual(120);
      expect(hasArabic(e.hook_ar), e.id).toBe(true); expect(hasArabic(e.gloss_ar), e.id).toBe(true);
    }
  });
  it("the quality/safety hold list stays catalogue-only", () => {
    for (const id of ["post-uncle-abner", "knatchbull-kalila-1819", "ranpo-d-zaka", "ranpo-yaneura"]) expect(byId.get(id)!.excerpt_count, id).toBe(0);
  });
  it("direction: only Arabic is rtl; foreign-language excerpts are ltr", () => {
    expect(dirFor("ar")).toBe("rtl");
    for (const l of ["en", "fr", "ja", "zh"]) expect(dirFor(l)).toBe("ltr");
  });
  it("only https source links are rendered as anchors", () => {
    expect(safeUrl("javascript:alert(1)")).toBeNull();
    expect(safeUrl("http://x.org")).toBeNull();
    expect(safeUrl("https://x.org/a")).toBe("https://x.org/a");
  });
});
