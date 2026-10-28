import { describe, expect, it } from "vitest";
import { readdirSync } from "node:fs";
import { loadSeason, existingCaseIds } from "../../src/engine/seasons-load";
import { episodeState, recommendedEpisode, resolveRef, resolveSeason } from "../../src/engine/seasons";
import { betaCdf, estimate, estimateAll, nextStep, retention } from "../../src/engine/mastery";
import { effectiveHintWeight, hintCountsByTier, hintPenalty, pickHint, tierOf } from "../../src/engine/hints";
import { loadTracks } from "../../src/engine/tracks";
import type { Hint } from "../../src/engine/types";

describe("season", () => {
  const ids = existingCaseIds();
  const r = resolveSeason(loadSeason(), ids);
  it("resolves every non-optional case", () => { expect(r.episodes.flatMap((e) => e.missing)).toEqual([]); });
  it("tolerates optional ids that do not exist yet", () => {
    const only = ids.filter((i) => !i.startsWith("c022"));
    const x = resolveSeason({ ...loadSeason(), episodes: [{ id: "b9", kind: "bonus", title_ar: "x", hook_ar: "x", principle_ar: "x", cases: [{ case: "c022", optional: true }] }] }, only);
    expect(x.episodes[0]!.pending).toEqual(["c022"]); expect(x.episodes[0]!.missing).toEqual([]);
  });
  it("short code resolves by prefix, exact id wins", () => { expect(resolveRef("c000", ["c000_lost_notebook"])).toBe("c000_lost_notebook"); expect(resolveRef("c999", ids)).toBeNull(); });
  it("is a soft path: nothing is ever locked, done alternatives count, recommended skips done", () => {
    const e1 = r.episodes.find((e) => e.id === "e1")!;
    const playable = new Set(e1.case_ids);
    const f = { playable, done: new Set([e1.case_ids[0]!]), started: new Set<string>() };
    expect(episodeState(e1, f).state).toBe("done");
    expect(episodeState(e1, { playable: new Set(), done: new Set(), started: new Set() }).state).toBe("other_band");
    const all = { playable: new Set(ids), done: new Set<string>(), started: new Set<string>() };
    expect(recommendedEpisode(r.episodes, all)).toBe("e0");
    expect(recommendedEpisode(r.episodes, { ...all, done: new Set(["c000_lost_notebook"]) })).toBe("e1");
  });
});

describe("hints", () => {
  const h = (id: string, level: 1 | 2 | 3, w: number, t?: string): Hint => ({ id, level, kind: "pointer", text_ar: "x", trigger: { always: true }, assessment_weight: w, targets_inference_id: t });
  it("tiers: nudge free, question half, method full; capped at 0.2", () => {
    expect(tierOf(1)).toBe("nudge"); expect(effectiveHintWeight(1, 0.06)).toBe(0);
    expect(effectiveHintWeight(2, 0.04)).toBeCloseTo(0.02); expect(effectiveHintWeight(3, 0.1)).toBe(0.1);
    const ladder = [h("a", 1, 0.06), h("b", 2, 0.04), h("c", 3, 0.1), h("d", 3, 0.1), h("e", 3, 0.1)];
    expect(hintPenalty([{ seq: 1, hint_id: "a", level: 1 }, { seq: 2, hint_id: "b", level: 2 }], ladder)).toBeCloseTo(0.02);
    expect(hintPenalty(ladder.map((x, i) => ({ seq: i, hint_id: x.id, level: x.level })), ladder)).toBe(0.2);
    expect(hintCountsByTier([{ seq: 1, hint_id: "a", level: 1 }, { seq: 2, hint_id: "c", level: 3 }])).toEqual({ nudge: 1, question: 0, method: 1 });
  });
  it("never offers a higher level before a lower one of the same target", () => {
    const ladder = [h("m", 3, 0.1), h("n", 1, 0), h("q", 2, 0.04)];
    expect(pickHint(ladder, [], () => true)?.id).toBe("n");
    expect(pickHint(ladder, [{ seq: 1, hint_id: "n", level: 1 }], () => true)?.id).toBe("q");
    expect(pickHint(ladder, [{ seq: 1, hint_id: "n", level: 1 }, { seq: 2, hint_id: "q", level: 2 }], () => true)?.id).toBe("m");
    expect(pickHint(ladder, [], (x) => x.level === 3)?.id).toBe("m");
  });
});

describe("mastery", () => {
  const now = "2026-10-28T00:00:00Z";
  const ob = (case_id: string, score: number, at = "2026-10-27T00:00:00Z") => ({ ko_id: "K", case_id, score, at });
  it("no data gives no estimate", () => { expect(estimate("K", [], now)).toBeNull(); expect(estimateAll([], now)).toEqual([]); });
  it("one case is insufficient evidence whatever the score", () => { expect(estimate("K", [ob("a", 1)], now)!.status).toBe("insufficient_evidence"); });
  it("strong repeated performance becomes secure; weak stays emerging", () => {
    expect(estimate("K", [ob("a", 0.95), ob("b", 0.9), ob("c", 0.95), ob("d", 0.9)], now)!.status).toBe("secure");
    expect(estimate("K", [ob("a", 0.1), ob("b", 0.2)], now)!.status).toBe("emerging");
  });
  it("two lucky cases are not enough for secure (interval too wide)", () => { expect(estimate("K", [ob("a", 1), ob("b", 1)], now)!.status).not.toBe("secure"); });
  it("criteria of one case count once", () => { expect(estimate("K", [ob("a", 1), ob("a", 1), ob("a", 1)], now)!.status).toBe("insufficient_evidence"); });
  it("decay lowers the displayed mean over time", () => {
    const fresh = estimate("K", [ob("a", 0.9), ob("b", 0.9)], now)!;
    const old = estimate("K", [ob("a", 0.9, "2025-10-01T00:00:00Z"), ob("b", 0.9, "2025-10-01T00:00:00Z")], now)!;
    expect(old.mean).toBeLessThan(fresh.mean); expect(retention(0)).toBe(1); expect(retention(120)).toBeCloseTo(0.5);
  });
  it("beta cdf sanity", () => { expect(betaCdf(0.5, 1, 1)).toBeCloseTo(0.5, 2); expect(betaCdf(0.5, 3, 3)).toBeCloseTo(0.5, 2); });
  it("next step prefers emerging skills and links a lesson", () => {
    const e = estimateAll([ob("a", 0.1), ob("b", 0.1)], now);
    expect(nextStep(e, () => "A1")).toEqual({ ko_id: "K", kind: "lesson", lesson_id: "A1" });
    expect(nextStep([], () => undefined)).toBeNull();
  });
});

describe("tracks case links", () => {
  it("every case_link points at an existing case", () => {
    const ids = new Set(readdirSync("content/cases").filter((f) => /^c\d{3}_[a-z0-9_]+\.json$/.test(f) && !f.includes(".ui.") && !f.includes(".scoring.")).map((f) => f.replace(".json", "")));
    const links = loadTracks().tracks.flatMap((t) => t.lessons).map((l) => l.case_link).filter(Boolean) as string[];
    expect(links.length).toBeGreaterThan(10);
    for (const l of links) expect(ids.has(l), l).toBe(true);
  });
});
