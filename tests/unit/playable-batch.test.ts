import { beforeAll, describe, expect, it } from "vitest";
import { migrate } from "@/server/db";
import { card, getCardsLight, getPlayable, getPlayableMany, listFileCaseIds, listPlayable, syncFileCases } from "@/server/content";

beforeAll(async () => { await migrate(); await syncFileCases(); });

/** The batch resolver replaced a per-case query loop (about 7s on production). It must pick exactly what getPlayable picks. */
describe("getPlayableMany", () => {
  it("resolves every case to the same version/hash/status/preview as getPlayable", async () => {
    const ids = listFileCaseIds();
    const many = await getPlayableMany();
    for (const id of ids) {
      const one = await getPlayable(id);
      const batch = many.get(id) ?? null;
      expect(batch === null).toBe(one === null);
      if (one && batch) expect([batch.version, batch.hash, batch.status, batch.preview]).toEqual([one.version, one.hash, one.status, one.preview]);
    }
  });

  it("honours an explicit id list and returns nothing for an empty list or unknown ids", async () => {
    expect((await getPlayableMany([])).size).toBe(0);
    expect((await getPlayableMany(["no_such_case"])).size).toBe(0);
    const some = listFileCaseIds().slice(0, 2);
    const got = await getPlayableMany(some);
    for (const id of got.keys()) expect(some).toContain(id);
  });

  it("listPlayable still returns a sorted, age-filtered card list", async () => {
    const cards = await listPlayable("16-17");
    const sorted = [...cards].sort((a, b) => Number(b.tutorial) - Number(a.tutorial) || a.difficulty - b.difficulty || a.case_id.localeCompare(b.case_id));
    expect(cards.map((c) => c.case_id)).toEqual(sorted.map((c) => c.case_id));
  });
});

/** The cold-start fast path builds cards from json_extract fields; it must be indistinguishable from the full-JSON card. */
describe("getCardsLight", () => {
  it("returns, for every case, exactly the card/age band/evidence count the full case gives", async () => {
    const light = await getCardsLight();
    expect(light.size).toBeGreaterThan(0);
    for (const id of listFileCaseIds()) {
      const full = await getPlayable(id);
      const l = light.get(id);
      expect(l === undefined).toBe(full === null);
      if (!full || !l) continue;
      expect(l.card).toEqual(JSON.parse(JSON.stringify(card(full))));
      expect(l.age_band).toBe(full.core.meta.age_band);
      expect(l.evidence_total).toBe(full.core.evidence.length);
    }
  });
});
