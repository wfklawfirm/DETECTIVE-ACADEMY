import { describe, expect, it } from "vitest";
import { readFileSync } from "node:fs";
import { dailyRiddle, selectHook, shuffleOptions, type HookContext, type HookDef, type RiddleDef } from "@/engine/hooks";
import { staticLeakScan } from "@/engine/leak";
import { CASES_DIR, listFileCaseIds, readFileTriplet } from "@/server/content";
import type { CaseFile } from "@/engine/types";
import type { CaseUi } from "@/engine/ui-types";

const hooks = (JSON.parse(readFileSync("content/hooks/global.json", "utf8")) as { hooks: HookDef[] }).hooks;
const riddles = (JSON.parse(readFileSync("content/hooks/riddles.json", "utf8")) as { riddles: RiddleDef[] }).riddles;
const base: HookContext = { surface: "landing", cases: [], recent_ids: [], entry_counter: 1, seed: "seed-a", gentle: false };
const open = { case_id: "c001_last_observation", title_ar: "الرصد الأخير", done: false, evidence_count: 5, locked_count: 11, updated_at: "2026-10-01T00:00:00Z" };
const done = { case_id: "c000_lost_notebook", title_ar: "دفتر المختبر الضائع", done: true, evidence_count: 7, locked_count: 0, updated_at: "2026-09-01T00:00:00Z" };

describe("entry hooks", () => {
  it("returns a hook at every entry on every surface and for every progress state", () => {
    for (const surface of ["landing", "home", "case_open", "case_return"] as const)
      for (const cases of [[], [open], [done], [open, done]])
        for (let n = 0; n < 40; n++) { const h = selectHook(hooks, { ...base, surface, cases, entry_counter: n, seed: `s${n % 5}` }); expect(h.text_ar.length).toBeGreaterThan(8); expect(h.text_ar).not.toMatch(/\{\{/); }
  });
  it("never repeats the previous hook back-to-back", () => {
    let recent: string[] = [];
    for (let n = 0; n < 200; n++) { const h = selectHook(hooks, { ...base, entry_counter: n, recent_ids: recent }); if (recent[0]) expect(h.id).not.toBe(recent[0]); recent = [h.id, ...recent].slice(0, 6); }
  });
  it("shows variety across entries", () => {
    const seen = new Set<string>(); let recent: string[] = [];
    for (let n = 0; n < 60; n++) { const h = selectHook(hooks, { ...base, entry_counter: n, recent_ids: recent }); seen.add(h.id); recent = [h.id, ...recent].slice(0, 6); }
    expect(seen.size).toBeGreaterThanOrEqual(8);
  });
  it("gentle mode only uses calm kinds", () => {
    for (let n = 0; n < 80; n++) { const h = selectHook(hooks, { ...base, gentle: true, entry_counter: n, cases: [open] }); expect(["skill", "welcome_back"]).toContain(h.kind); }
  });
  it("personalises with real progress and points at the open case", () => {
    const hs = Array.from({ length: 60 }, (_, n) => selectHook(hooks, { ...base, surface: "home", cases: [open], entry_counter: n }));
    expect(hs.some((h) => h.text_ar.includes("الرصد الأخير"))).toBe(true);
    expect(hs.some((h) => h.cta_href === "/play/c001_last_observation")).toBe(true);
  });
  it("uses a case cliffhanger on case surfaces", () => {
    const h = selectHook(hooks, { ...base, surface: "case_return", cases: [open], entry_counter: 2, case_stage_hook: { case_id: "c001_last_observation", text_ar: "نص" } });
    expect(h.id).toBe("case:c001_last_observation");
  });
  it("contains no loss-aversion, streak or guilt language", () => {
    const bad = ["سلسلة", "ستخسر", "فاتك", "لا تفوّت", "لا تفوت", "آخر فرصة", "اشتقنا", "تأخرت", "خيّبت"];
    for (const h of hooks) for (const b of bad) expect(new RegExp(`(^|[^\\p{L}])${b}`, "u").test(h.text_ar), `${h.id}:${b}`).toBe(false);
  });
  it("is spoiler-free: no hook shares n-grams with any case's solution text", () => {
    for (const id of listFileCaseIds(CASES_DIR)) { const t = readFileTriplet(CASES_DIR, id)!; expect(staticLeakScan(t.core as CaseFile, t.ui as CaseUi, hooks.map((h) => ({ where: h.id, text: h.text_ar })))).toEqual([]); }
  });
});

describe("daily riddle", () => {
  it("is deterministic per day and seed, and cycles", () => {
    const d = new Date("2026-10-27T10:00:00Z");
    expect(dailyRiddle(riddles, d, "x").id).toBe(dailyRiddle(riddles, d, "x").id);
    const ids = new Set(Array.from({ length: riddles.length }, (_, i) => dailyRiddle(riddles, new Date(d.getTime() + i * 86_400_000), "x").id));
    expect(ids.size).toBe(riddles.length);
  });
  it("has valid answers and spreads the correct slot after shuffling", () => {
    const slots = new Set<number>();
    for (const r of riddles) { expect(r.options.some((o) => o.id === r.answer_id)).toBe(true); expect(r.options.length).toBeGreaterThanOrEqual(3); for (const s of ["a", "b", "c", "d", "e", "f", "g", "h"]) slots.add(shuffleOptions(r.options, `${s}:${r.id}`).findIndex((o) => o.id === r.answer_id)); }
    expect(slots.size).toBeGreaterThanOrEqual(3);
  });
});
