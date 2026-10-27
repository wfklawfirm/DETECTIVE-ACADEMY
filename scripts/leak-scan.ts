import { readFileSync } from "node:fs";
import { staticLeakScan } from "../src/engine/leak";
import { listFileCaseIds, readFileTriplet, CASES_DIR } from "../src/server/content";
import type { CaseFile } from "../src/engine/types";
import type { CaseUi } from "../src/engine/ui-types";

const hooks = JSON.parse(readFileSync("content/hooks/global.json", "utf8")).hooks as { id: string; text_ar: string }[];
let bad = 0;
for (const id of listFileCaseIds(CASES_DIR)) {
  const t = readFileTriplet(CASES_DIR, id)!;
  const f = staticLeakScan(t.core as CaseFile, t.ui as CaseUi, hooks.map((h) => ({ where: `hook:${h.id}`, text: h.text_ar })));
  console.log(`${id}: ${f.length} finding(s)`);
  for (const x of f) console.log("  -", x.where, "~", x.against, `[${x.kind}]`, x.sample);
  bad += f.length;
}
process.exit(bad ? 1 : 0);
