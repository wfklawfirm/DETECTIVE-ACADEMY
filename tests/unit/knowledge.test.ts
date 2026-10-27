import { describe, expect, it } from "vitest";
import { loadKnowledge, visibleKos } from "../../src/engine/knowledge";
import { loadLabs } from "../../src/engine/labs";
import { loadTracks } from "../../src/engine/tracks";

describe("knowledge base", () => {
  const { kos, src } = loadKnowledge();
  it("holds every knowledge object of the library with unique ids", () => {
    expect(kos.length).toBe(377);
    expect(new Set(kos.map((k) => k.ko_id)).size).toBe(377);
  });
  it("every cited source exists in the source register", () => {
    const ids = new Set(src.map((s) => s.id));
    for (const k of kos) for (const s of k.source_ids) expect(ids.has(s), `${k.ko_id} cites unknown ${s}`).toBe(true);
  });
  it("lessons only reference known knowledge objects", () => {
    const ids = new Set(kos.map((k) => k.ko_id));
    for (const t of loadTracks().tracks) for (const l of t.lessons) for (const r of l.ko_refs) expect(ids.has(r), `${l.id} → ${r}`).toBe(true);
  });
  it("shows players only player-facing types, and 18+ items only to adults", () => {
    const minor = visibleKos(kos, "16-17"), none = visibleKos(kos, null), adult = visibleKos(kos, "18+");
    for (const k of minor) { expect(k.audience).toBe("player"); expect(k.age_band).not.toBe("18+"); }
    expect(none.length).toBe(minor.length);
    expect(adult.length).toBeGreaterThan(minor.length);
    expect(minor.some((k) => k.type === "product_opportunity")).toBe(false);
  });
});

describe("safe labs", () => {
  it("catalogue has 20 entries and every playable lab validates", () => {
    const f = loadLabs();
    expect(f.catalogue.length).toBe(20);
    expect(f.playable.length).toBeGreaterThanOrEqual(6);
    for (const l of f.playable) expect(new Set(l.items.map((i) => i.answer)).size, `${l.id} uses one category only`).toBeGreaterThan(1);
  });
});
