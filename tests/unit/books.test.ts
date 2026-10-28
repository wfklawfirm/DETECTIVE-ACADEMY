import { existsSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { describe, expect, it } from "vitest";
import { loadBooks, visibleConcepts, SKILLS } from "@/engine/books";

const root = process.cwd();
const kos = new Set(Object.keys(JSON.parse(readFileSync(join(root, "content/knowledge/ko_names.json"), "utf8"))));
const { books, concepts, drills } = loadBooks(root);

describe("book concept notes", () => {
  it("meets volume targets", () => {
    expect(concepts.length).toBeGreaterThanOrEqual(250);
    expect(drills.length).toBeGreaterThanOrEqual(60);
    expect(books).toHaveLength(4);
  });
  it("has unique ids", () => {
    expect(new Set(concepts.map((c) => c.id)).size).toBe(concepts.length);
    expect(new Set(drills.map((d) => d.id)).size).toBe(drills.length);
  });
  it("links only to existing knowledge objects", () => {
    for (const c of concepts) for (const k of c.linked_ko_ids) expect(kos.has(k), `${c.id} -> ${k}`).toBe(true);
  });
  it("keeps line ranges inside the outline and counts consistent", () => {
    for (const b of books) {
      expect(b.sections.reduce((n, s) => n + s.note_count, 0)).toBe(b.note_count);
      for (const s of b.sections) expect(s.line_end).toBeGreaterThanOrEqual(s.line_start);
    }
    for (const c of concepts) {
      const s = books.find((b) => b.id === c.book_id)?.sections.find((x) => x.id === c.section_id);
      expect(s, c.id).toBeTruthy();
      expect(c.line_start).toBeGreaterThanOrEqual(s!.line_start);
      expect(c.line_end).toBeGreaterThanOrEqual(c.line_start);
    }
  });
  it("covers every skill with at least 10 drills and valid options", () => {
    for (const s of SKILLS) expect(drills.filter((d) => d.skill === s).length).toBeGreaterThanOrEqual(10);
    const pos = new Set(drills.map((d) => d.options.findIndex((o) => o.id === d.answer_id)));
    expect(pos.size).toBeGreaterThan(1);
  });
  it("hides sensitive notes and the excluded book from minors", () => {
    const v = visibleConcepts(concepts, books, "16-17");
    expect(v.some((c) => c.safety_level === "sensitive" || c.book_id === "BK-04425")).toBe(false);
    expect(visibleConcepts(concepts, books, null).every((c) => c.age_band === "all" || c.age_band === "13-15")).toBe(true);
  });
  it("does not copy 8-word runs from the protected sources (skipped if sources are absent)", () => {
    const dir = "/mnt/user-data/uploads/game learning/";
    if (!existsSync(dir)) return;
    const norm = (s: string) => s.replace(/[ً-ٰٟـ]/g, "").replace(/[أإآٱ]/g, "ا").replace(/ى/g, "ي").replace(/ة/g, "ه").replace(/[^\p{L}\p{N}\s]/gu, " ").replace(/\s+/g, " ").trim().split(" ");
    const sh = (w: string[]) => { const o = new Set<string>(); for (let i = 0; i + 8 <= w.length; i++) o.add(w.slice(i, i + 8).join(" ")); return o; };
    const src = new Set<string>();
    for (const f of ["741 الطب الشرعي ومسرح الجريمة والبحث الجنائي (أحمد بسيوني أبو الروس، مديحة الخضري).txt", "853 الطب الشرعي العملي (الياس الصائغ).txt", "843 الأسلحة النارية في الطب الشرعي - حسين شحرور.txt", "04425_طرق الإنجاب في الطب الحديث وحكمها الشرعي.txt"]) {
      const p = join(dir, f);
      if (existsSync(p)) for (const s of sh(norm(readFileSync(p, "utf8")))) src.add(s);
    }
    const hits: string[] = [];
    for (const c of concepts) for (const s of sh(norm([c.title_ar, c.summary_ar, c.investigation_use_ar, c.limits_ar, c.myth_ar ?? ""].join(" ")))) if (src.has(s)) hits.push(c.id);
    for (const d of drills) for (const s of sh(norm([d.scenario_ar, d.question_ar, d.explanation_ar, ...d.options.map((o) => o.text_ar)].join(" ")))) if (src.has(s)) hits.push(d.id);
    expect(hits).toEqual([]);
  });
});
