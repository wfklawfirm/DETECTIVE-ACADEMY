import { describe, expect, it } from "vitest";
import { KIND_LABEL, LabsFileSchema, loadKoNames, loadLabs } from "../../src/engine/labs";
import { evalExpr, exprNames } from "../../src/components/labs/expr";
import { parseNum, shuffled } from "../../src/components/labs/common";

describe("safe labs catalogue", () => {
  const f = loadLabs();
  it("reconciles the three source lists: every catalogue entry is playable", () => {
    expect(f.catalogue.length).toBeGreaterThanOrEqual(45);
    expect(f.playable.length).toBe(f.catalogue.length);
    expect(f.catalogue.every((c) => c.playable)).toBe(true);
    expect(new Set(f.catalogue.map((c) => c.id)).size).toBe(f.catalogue.length);
  });
  it("keeps the ids of the original 20 stable", () => {
    for (let i = 1; i <= 20; i++) expect(f.playable.some((l) => l.id === `SAFE_LABS-${String(i).padStart(2, "0")}`), `lab ${i}`).toBe(true);
  });
  it("uses every interaction kind", () => {
    expect(new Set(f.playable.map((l) => l.kind))).toEqual(new Set(Object.keys(KIND_LABEL)));
  });
  it("every lab has a hook, a cannot-prove note, a transfer question, difficulty and time", () => {
    for (const l of f.playable) {
      expect(l.hook_ar.length, l.id).toBeGreaterThan(10);
      expect(l.boundary_ar.length, l.id).toBeGreaterThan(10);
      expect(l.transfer_ar.length, l.id).toBeGreaterThan(10);
      expect([1, 2, 3]).toContain(l.difficulty);
      expect(l.minutes).toBeGreaterThan(0);
    }
  });
  it("related knowledge objects exist in ko_names.json", () => {
    const names = loadKoNames();
    for (const l of f.playable) for (const k of l.ko_ids) expect(names[k], `${l.id} → ${k}`).toBeTruthy();
  });
  it("answers are spread: no classify/conclude lab can be won by one repeated choice", () => {
    for (const l of f.playable) {
      if (l.kind === "classify") expect(new Set(l.items.map((i) => i.answer)).size, l.id).toBeGreaterThan(1);
      if (l.kind === "conclude") for (const s of l.scenarios) expect(s.options.filter((o) => o.verdict === "best").length, `${l.id}/${s.id}`).toBe(1);
    }
  });
  it("is safe: no operational words in any lab text", () => {
    const text = JSON.stringify(f.playable) + JSON.stringify(f.catalogue);
    for (const bad of ["سم قاتل", "متفجر", "تصنيع سلاح", "جرعة قاتلة", "انتحار", "جثة"]) expect(text.includes(bad), bad).toBe(false);
  });
  it("declined labs are recorded with a reason", () => {
    expect(f.declined.length).toBeGreaterThanOrEqual(4);
    for (const d of f.declined) expect(d.reason_ar.length).toBeGreaterThan(10);
  });
  it("rejects a broken lab (unknown classify category)", () => {
    const bad = JSON.parse(JSON.stringify(f));
    const c = bad.playable.find((l: { kind: string }) => l.kind === "classify");
    c.items[0].answer = "zzz";
    expect(LabsFileSchema.safeParse(bad).success).toBe(false);
  });
});

describe("slider-model labs", () => {
  const f = loadLabs();
  const sliders = f.playable.filter((l) => l.kind === "slider");
  it("each challenge is reachable but not met by the default setting, and predict answer is not trivially first", () => {
    expect(sliders.length).toBeGreaterThanOrEqual(6);
    for (const l of sliders) {
      const def = Object.fromEntries(l.controls.map((c) => [c.id, c.value]));
      const out = l.outputs.find((o) => o.id === l.challenge.output)!;
      const v0 = evalExpr(out.expr, def);
      expect(v0 >= l.challenge.min && v0 <= l.challenge.max, `${l.id} default already wins`).toBe(false);
      // brute-force the control grid for a winning point
      let won = false;
      const grid = (i: number, env: Record<string, number>) => {
        if (i === l.controls.length) { const v = evalExpr(out.expr, env); if (v >= l.challenge.min && v <= l.challenge.max) won = true; return; }
        const c = l.controls[i]!;
        for (let x = c.min; x <= c.max + 1e-9; x += c.step) grid(i + 1, { ...env, [c.id]: x });
      };
      grid(0, {});
      expect(won, `${l.id} challenge unreachable`).toBe(true);
    }
  });
});

describe("expression evaluator", () => {
  it("computes with precedence, powers, unary minus and functions", () => {
    expect(evalExpr("2 + 3 * 4", {})).toBe(14);
    expect(evalExpr("(2 + 3) * 4 ^ 2", {})).toBe(80);
    expect(evalExpr("-x + max(1, y)", { x: 2, y: 5 })).toBe(3);
    expect(evalExpr("h / tan(rad(45))", { h: 2 })).toBeCloseTo(2, 6);
  });
  it("refuses unknown names and anything that is not arithmetic", () => {
    expect(() => evalExpr("process", {})).toThrow();
    expect(() => evalExpr("constructor(1)", {})).toThrow();
    expect(() => evalExpr("a.b", { a: 1 })).toThrow();
    expect(() => evalExpr("1 +", {})).toThrow();
    expect(exprNames("ln(a) + b").vars.sort()).toEqual(["a", "b"]);
  });
});

describe("runner helpers", () => {
  it("parses Arabic-Indic digits and separators", () => {
    expect(parseNum("٢٫٥")).toBe(2.5);
    expect(parseNum(" 1,5 ")).toBe(1.5);
    expect(parseNum("abc")).toBeNull();
    expect(parseNum("")).toBeNull();
  });
  it("shuffles deterministically and never returns the original order", () => {
    const xs = ["a", "b", "c", "d", "e"];
    expect(shuffled(xs, "x")).toEqual(shuffled(xs, "x"));
    for (const s of ["a", "b", "c", "d", "e", "f", "g"]) expect(shuffled(xs, s)).not.toEqual(xs);
  });
  it("measure tasks: the reference answer falls inside its own tolerance and traps do not", () => {
    for (const l of loadLabs().playable) if (l.kind === "measure") for (const t of l.tasks) for (const tr of t.traps) expect(Math.abs(tr.value - t.answer) > t.tolerance, `${l.id}/${t.id}`).toBe(true);
  });
});
