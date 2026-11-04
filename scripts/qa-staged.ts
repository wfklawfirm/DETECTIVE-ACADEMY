// Usage: npx tsx scripts/qa-staged.ts <dir> <case_id>  — QA a case triplet in any directory (e.g. staging).
import { readFileTriplet } from "../src/server/content";
import { runQa } from "../src/server/studio";
import type { CaseFile } from "../src/engine/types";
import type { CaseUi, ScoringSpec } from "../src/engine/ui-types";
const [dir, id] = process.argv.slice(2);
const t = readFileTriplet(dir!, id!);
if (!t) { console.log("MISSING triplet (need <id>.json, .scoring.json, .ui.json)"); process.exit(2); }
const r = await runQa(t.core as CaseFile, t.ui as CaseUi, t.scoring as ScoringSpec);
console.log(`${id}: ${r.ok ? "OK" : "FAIL"} proof_paths=${r.core.proof_paths} errors=${r.core.errors.length} warnings=${r.core.warnings.length} sidecar=${r.sidecar_errors.length} leaks=${r.leaks.length}`);
for (const e of [...r.core.errors, ...r.sidecar_errors]) console.log("  !", e);
for (const w of r.core.warnings) console.log("  ~", w);
for (const l of r.leaks) console.log("  leak", l.where, l.kind);
process.exit(r.ok ? 0 : 1);
