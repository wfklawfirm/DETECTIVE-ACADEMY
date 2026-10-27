import { describe, expect, it } from "vitest";
import { readFileSync } from "node:fs";
import { staticLeakScan } from "@/engine/leak";
import { crossCheck } from "@/engine/sidecars";
import { qaCase } from "@/engine/validate";
import { CASES_DIR, listFileCaseIds, readFileTriplet } from "@/server/content";
import type { CaseFile } from "@/engine/types";
import type { CaseUi, ScoringSpec } from "@/engine/ui-types";

const ids = listFileCaseIds(CASES_DIR);
const hooks = (JSON.parse(readFileSync("content/hooks/global.json", "utf8")).hooks as { id: string; text_ar: string }[]).map((h) => ({ where: `hook:${h.id}`, text: h.text_ar }));

describe("content integrity", () => {
  it("has the tutorial and the flagship", () => { expect(ids).toContain("c000_lost_notebook"); expect(ids).toContain("c001_last_observation"); });
  for (const id of ids) {
    const t = readFileTriplet(CASES_DIR, id)!;
    const core = t.core as CaseFile, ui = t.ui as CaseUi, sc = t.scoring as ScoringSpec;
    describe(id, () => {
      const qa = qaCase(core);
      it("passes schema + fair-play QA", () => { expect(qa.errors).toEqual([]); expect(qa.ok).toBe(true); });
      it("meets the declared number of independent proof paths", () => { expect(qa.proof_paths).toBeGreaterThanOrEqual(Number(core.fairness_test.requirements.min_disjoint_proof_paths ?? 1)); });
      it("has no unreachable evidence", () => { expect(qa.unreachable_evidence).toEqual([]); });
      it("sidecars agree with core", () => { expect(crossCheck(core, ui, sc)).toEqual([]); });
      it("static leak scan is clean", () => { expect(staticLeakScan(core, ui, hooks)).toEqual([]); });
      it("never claims expert approval it does not have", () => { for (const r of core.expert_review) expect(r.status).not.toBe("approved"); });
      it("is original: no brand/protected names", () => { const s = JSON.stringify(core); for (const bad of ["شرلوك", "هولمز", "كونان", "Sherlock", "Conan"]) expect(s).not.toContain(bad); });
    });
  }
});
