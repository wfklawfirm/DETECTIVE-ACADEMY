import { existsSync, readFileSync, readdirSync } from "node:fs";
import { join } from "node:path";
import { describe, expect, it } from "vitest";
import {
  archetypeCaseUse, gated, glossaryFor, koLinks, loadArchetypes, loadAtlas, loadBiases, loadCounts, loadExcluded, loadGlossary, loadMethods, loadReasoning, loadRulebook, sourceRefs,
} from "../../src/engine/reference";
import { loadKnowledge } from "../../src/engine/knowledge";

const files = ["glossary", "methods", "biases", "reasoning", "rulebook", "atlas", "archetypes"] as const;
const raw = (f: string) => readFileSync(join(process.cwd(), "content/reference", `${f}.json`), "utf8");
/** Every string value of a JSON tree, with its key path. */
function strings(x: unknown, path = ""): { path: string; v: string }[] {
  if (typeof x === "string") return [{ path, v: x }];
  if (Array.isArray(x)) return x.flatMap((v) => strings(v, path));
  if (x && typeof x === "object") return Object.entries(x).flatMap(([k, v]) => strings(v, `${path}/${k}`));
  return [];
}
const LEARNER_SKIP = /(?:^|\/)(?:src_ids|ko_ids|narrative_pattern_kos|original_en|term_en|name_en|id|generated_from|suitability_en|standards_en|discipline_en|title|author)$/;

describe("reference content: counts in vs counts out", () => {
  const g = loadGlossary(), m = loadMethods(), b = loadBiases(), r = loadReasoning(), rb = loadRulebook(), a = loadAtlas(), ar = loadArchetypes();
  it("covers every glossary term, method, bias, error and archetype of the library", () => {
    expect(g.items.length).toBe(248);
    expect(new Set(g.items.map((i) => i.id)).size).toBe(248);
    expect(m.items.length).toBe(24);
    expect(b.items.length).toBe(17);
    expect(r.errors.length).toBe(14);
    expect(r.criteria.length).toBe(5);
    expect(r.ethics.length).toBe(7);
    expect(r.skills.length).toBe(24);
    expect(ar.items.length).toBe(40);
    expect(new Set(ar.items.map((i) => i.id)).size).toBe(40);
    expect(a.principles.length).toBe(50);
    expect(a.expansion.length).toBe(24);
    expect(a.corpus.length).toBe(14);
    expect(a.heritage.length).toBe(20);
    expect(a.patterns.length).toBe(26);
    expect(rb.sections.flatMap((s) => s.rules).length).toBe(46);
  });
  it("counts.json: nothing dropped silently (register rows leave only via excluded.json)", () => {
    const c = loadCounts().counts, ex = loadExcluded().items;
    for (const [page, d] of Object.entries(c)) for (const [k, v] of Object.entries(d)) {
      if (k === "rights_register_rows") continue;
      if (k === "adult_gated") continue;
      expect(v.out, `${page}.${k}`).toBe(v.in);
    }
    const reg = c.atlas!.rights_register_rows!;
    expect(reg.out + ex.filter((e) => e.page === "atlas" && e.id.startsWith("REG-")).length).toBe(reg.in);
  });
  it("excluded.json explains every exclusion and every adult-only gate", () => {
    const ex = loadExcluded().items;
    for (const e of ex) { expect(e.reason.length).toBeGreaterThan(10); expect(e.title.length).toBeGreaterThan(0); }
    for (const mm of m.items.filter((x) => x.min_band === "18+")) expect(ex.some((e) => e.page === "methods" && e.id === mm.id), mm.id).toBe(true);
    for (const x of ar.items.filter((i) => i.min_band === "18+")) expect(ex.some((e) => e.page === "archetypes" && e.id === x.id), x.id).toBe(true);
  });
  it("every page opens with a hook", () => {
    for (const h of [g.hook_ar, m.hook_ar, b.hook_ar, r.hook_ar, rb.hook_ar, a.hook_ar, ar.hook_ar]) { expect(h.length).toBeGreaterThan(20); expect(h.length).toBeLessThan(200); }
  });
});

describe("reference content: references resolve", () => {
  const { kos, src } = loadKnowledge();
  const koIds = new Set(kos.map((k) => k.ko_id)), srcIds = new Set(src.map((s) => s.id));
  it("every cited source and knowledge object exists", () => {
    for (const f of files) {
      const walk = (x: unknown): void => {
        if (Array.isArray(x)) x.forEach(walk);
        else if (x && typeof x === "object") for (const [k, v] of Object.entries(x)) {
          if (k === "src_ids") for (const s of v as string[]) expect(srcIds.has(s), `${f}: ${s}`).toBe(true);
          else if (k === "ko_ids") for (const s of v as string[]) expect(koIds.has(s), `${f}: ${s}`).toBe(true);
          else walk(v);
        }
      };
      walk(JSON.parse(raw(f)));
    }
  });
  it("related knowledge links respect the viewer's age (18+ items never reach minors)", () => {
    const all = loadGlossary().items.flatMap((t) => t.ko_ids);
    const minor = koLinks(all, "16-17").map((k) => k.id), adult = koLinks(all, "18+").map((k) => k.id);
    for (const id of minor) expect(kos.find((k) => k.ko_id === id)!.age_band).not.toBe("18+");
    expect(adult.length).toBeGreaterThanOrEqual(minor.length);
    expect(sourceRefs(["ATH-SRC-1702"]).length).toBe(1);
  });
});

describe("reference content: product terminology", () => {
  const g = loadGlossary();
  it("uses «سلسلة العهدة» and «نسبة الترجيح» as the standard terms", () => {
    expect(g.items.find((t) => t.term_en === "chain of custody")!.term_ar).toBe("سلسلة العهدة");
    expect(g.items.find((t) => t.term_en.startsWith("likelihood ratio"))!.term_ar).toBe("نسبة الترجيح");
  });
  it("never uses the rejected variants as a product term", () => {
    for (const f of files) {
      const text = raw(f);
      expect(text.includes("سلسلة الحيازة"), `${f} سلسلة الحيازة`).toBe(false);
      const odds = text.match(/نسبة الأرجحية/g)?.length ?? 0;
      // allowed once: the glossary entry for odds ratio (a different thing)
      expect(odds, `${f} نسبة الأرجحية`).toBe(f === "glossary" ? 1 : 0);
    }
    expect(g.items.filter((t) => t.term_ar.includes("نسبة الأرجحية")).map((t) => t.term_en)).toEqual(["odds ratio"]);
  });
});

describe("reference content: hygiene and safety", () => {
  it("no internal markers leak into learner-facing Arabic text", () => {
    const bad = /ATH-SRC|\.md\b|\bKO-[A-Z]|\bHS-\d|\[\d{3,4}\]|_data\/|الدفعة|`|\*\*|\bLO-\d|\(C\d{1,2}\)|§|المكتبة \d\d|(?:خبير|فريق) \d\d/;
    for (const f of files) for (const s of strings(JSON.parse(raw(f))).filter((x) => !LEARNER_SKIP.test(x.path))) expect(bad.test(s.v), `${f}${s.path}: ${s.v.slice(0, 80)}`).toBe(false);
  });
  it("no operational harm detail (doses, synthesis, weapon-making) in learner text", () => {
    const op = /جرعة (?:قاتلة|مميتة)|تصنيع|كيفية صنع|خطوات (?:الصنع|التحضير)|متفجر|سم قاتل|طريقة (?:الانتحار|إيذاء)/;
    for (const f of files) for (const s of strings(JSON.parse(raw(f))).filter((x) => !LEARNER_SKIP.test(x.path))) expect(op.test(s.v), `${f}${s.path}: ${s.v.slice(0, 80)}`).toBe(false);
  });
  it("adult-only items are hidden from minors and from unknown ages, shown to adults", () => {
    const g = loadGlossary().items, m = loadMethods().items, ar = loadArchetypes().items;
    for (const band of ["13-15", "16-17", null] as const) {
      expect(glossaryFor(g, band).every((t) => t.level !== "18+")).toBe(true);
      expect(gated(m, band).every((x) => x.min_band === "all")).toBe(true);
      expect(gated(ar, band).every((x) => x.min_band === "all")).toBe(true);
    }
    expect(glossaryFor(g, "18+").length).toBe(g.length);
    expect(gated(m, "18+").length).toBe(24);
    expect(gated(ar, "18+").length).toBe(40);
    expect(g.filter((t) => t.level === "18+").length).toBeGreaterThan(0);
  });
  it("protected literature is referenced only: works carry title, author, year and a rights label, nothing else", () => {
    const a = loadAtlas();
    expect(a.works.length).toBeGreaterThan(50);
    for (const w of a.works) { expect(Object.keys(w).sort()).toEqual(["author", "rights_ar", "title", "year"]); expect(w.rights_ar).toMatch(/يُشار إليه فقط/); }
    expect(a.works.some((w) => /^(?:Hercule Poirot|Sherlock Holmes & Dr Watson)/.test(w.title))).toBe(false); // characters are not reproduced
    // no long verbatim quotation marks in the cards: quoted spans stay short
    for (const s of strings(a.principles).concat(strings(a.expansion), strings(a.heritage))) for (const q of s.v.matchAll(/«([^»]+)»/g)) expect(q[1]!.split(/\s+/).length, q[1]).toBeLessThanOrEqual(15);
  });
});

describe("archetypes: which existing cases use each pattern", () => {
  it("maps every archetype and only to case files that exist", () => {
    const ar = loadArchetypes().items, use = archetypeCaseUse(ar);
    expect(use.size).toBe(40);
    const dir = join(process.cwd(), "content/cases");
    const ids = new Set(readdirSync(dir).filter((f) => f.endsWith(".json") && !f.endsWith(".ui.json") && !f.endsWith(".scoring.json")).map((f) => f.replace(/\.json$/, "")));
    for (const [, cases] of use) for (const c of cases) expect(ids.has(c.case_id) || existsSync(join(dir, `${c.case_id}.json`))).toBe(true);
  });
});
