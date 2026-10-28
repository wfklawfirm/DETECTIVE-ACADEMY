import { loadSeason, existingCaseIds } from "../src/engine/seasons-load";
import { resolveSeason } from "../src/engine/seasons";

const errors: string[] = [];
const s = loadSeason();
const existing = existingCaseIds();
const r = resolveSeason(s, existing);
const ids = new Set<string>();
const used = new Map<string, string>();
for (const e of r.episodes) {
  if (ids.has(e.id)) errors.push(`duplicate episode id ${e.id}`);
  ids.add(e.id);
  for (const m of e.missing) errors.push(`${e.id}: case ${m} does not exist and is not optional`);
  for (const c of e.case_ids) {
    if (used.has(c)) errors.push(`${e.id}: case ${c} already used in ${used.get(c)}`);
    used.set(c, e.id);
  }
  if (e.kind !== "break" && e.kind !== "bonus" && e.case_ids.length === 0) errors.push(`${e.id}: no existing case`);
  if (e.kind === "break" && !e.link) errors.push(`${e.id}: break needs a link`);
}
const required = ["tutorial", "finale", "transfer"] as const;
for (const k of required) if (!r.episodes.some((e) => e.kind === k)) errors.push(`season has no ${k} episode`);
console.table(r.episodes.map((e) => ({ id: e.id, kind: e.kind, cases: e.case_ids.join(", "), pending: e.pending.join(", ") })));
console.log(`episodes: ${r.episodes.length}, distinct existing cases used: ${used.size}, not placed in season: ${existing.filter((x) => !used.has(x)).join(", ") || "-"}`);
if (errors.length) { console.error("FAIL\n" + errors.map((x) => " - " + x).join("\n")); process.exit(1); }
console.log("OK");
