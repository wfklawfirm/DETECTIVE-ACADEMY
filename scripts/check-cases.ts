import { listFileCaseIds, readFileTriplet, CASES_DIR } from "../src/server/content";
import { runQa } from "../src/server/studio";
import type { CaseFile } from "../src/engine/types";
import type { CaseUi, ScoringSpec } from "../src/engine/ui-types";
let bad = 0;
for (const id of listFileCaseIds(CASES_DIR)) {
  const t = readFileTriplet(CASES_DIR, id)!;
  const r = await runQa(t.core as CaseFile, t.ui as CaseUi, t.scoring as ScoringSpec);
  console.log(`${id}: ${r.ok ? "OK" : "FAIL"} proof_paths=${r.core.proof_paths} errors=${r.core.errors.length} warnings=${r.core.warnings.length} sidecar=${r.sidecar_errors.length} leaks=${r.leaks.length}`);
  for (const e of [...r.core.errors, ...r.sidecar_errors]) console.log("  !", e);
  for (const l of r.leaks) console.log("  leak", l.where, l.kind);
  if (!r.ok) bad++;
}
process.exit(bad ? 1 : 0);
