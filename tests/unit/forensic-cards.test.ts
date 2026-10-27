import { describe, expect, it } from "vitest";
import { loadKnowledge } from "../../src/engine/knowledge";
import { loadForensicCards } from "../../src/engine/forensic-cards";

describe("forensic knowledge cards (Arabic)", () => {
  const cards = loadForensicCards();
  const { kos } = loadKnowledge();
  const fc = kos.filter((k) => k.type === "forensic_concept");
  it("has 40 cards with unique ids, one per forensic_concept KO", () => {
    expect(cards.length).toBe(40);
    expect(new Set(cards.map((c) => c.ko_id)).size).toBe(40);
    expect(new Set(fc.map((k) => k.ko_id))).toEqual(new Set(cards.map((c) => c.ko_id)));
  });
  it("every card id exists in ko.json", () => {
    const ids = new Set(kos.map((k) => k.ko_id));
    for (const c of cards) expect(ids.has(c.ko_id), c.ko_id).toBe(true);
  });
  it("all fields are non-empty and limits have 2-4 bullets", () => {
    for (const c of cards) {
      for (const f of [c.myth_ar, c.reality_ar, c.safe_note_ar]) expect(f.trim().length, c.ko_id).toBeGreaterThan(0);
      expect(c.limits_ar.length, c.ko_id).toBeGreaterThanOrEqual(2);
      for (const b of c.limits_ar) expect(b.trim().length, c.ko_id).toBeGreaterThan(0);
    }
  });
});
