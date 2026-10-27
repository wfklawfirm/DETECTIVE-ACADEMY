import { readFileSync } from "node:fs";
import { qaCase } from "../src/engine/validate";
const p = process.argv[2]!;
const c = JSON.parse(readFileSync(p, "utf8"));
const r = qaCase(c);
console.log(JSON.stringify({ ok: r.ok, errors: r.errors, warnings: r.warnings, proof_paths: r.proof_paths, sets: r.proof_sets, unreachable: r.unreachable_evidence }, null, 1));
process.exit(r.ok ? 0 : 1);
