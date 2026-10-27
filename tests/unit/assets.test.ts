import { describe, expect, it } from "vitest";
import { existsSync } from "node:fs";
import { loadAssets } from "../../src/engine/assets";

describe("shipped assets", () => {
  const all = loadAssets();
  it("every registered file exists and carries attribution + source", () => {
    expect(all.length).toBe(22);
    for (const a of all) { expect(existsSync(`public${a.file}`), a.id).toBe(true); expect(a.attribution.length).toBeGreaterThan(10); expect(a.source).toMatch(/^https?:\/\//); }
  });
});
