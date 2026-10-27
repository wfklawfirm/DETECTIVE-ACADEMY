import { readFileSync } from "node:fs";
import { join } from "node:path";
import { TracksSchema } from "../src/engine/tracks";

const root = process.cwd();
const errors: string[] = [];
const fail = (m: string) => errors.push(m);

const raw = JSON.parse(readFileSync(join(root, "content/tracks/tracks.json"), "utf8"));
const parsed = TracksSchema.safeParse(raw);
if (!parsed.success) {
  for (const i of parsed.error.issues) fail(`schema: ${i.path.join(".")}: ${i.message}`);
  console.error(errors.join("\n"));
  process.exit(1);
}
const data = parsed.data;
const ko = JSON.parse(readFileSync(join(root, "content/knowledge/ko_names.json"), "utf8")) as Record<string, string>;

const BANNED = ["كشف الكذب", "احتمال الإدانة", "احتمال الذنب", "احتمال أن يكون مذنب", "لا تخطئ", "لا يخطئ أبدا", "لا يخطئ أبداً", "دليل قاطع على الكذب"];
const lessonIds = new Set<string>();
const slots: Record<string, number> = { a: 0, b: 0, c: 0, d: 0 };
const rows: Record<string, string | number>[] = [];

for (const t of data.tracks) {
  if (t.lessons.length !== 6) fail(`track ${t.id}: expected 6 lessons`);
  for (const l of t.lessons) {
    if (!l.id.startsWith(t.id)) fail(`${l.id}: id prefix mismatch with track ${t.id}`);
    if (lessonIds.has(l.id)) fail(`duplicate lesson id ${l.id}`);
    lessonIds.add(l.id);
    for (const k of l.ko_refs) if (!(k in ko)) fail(`${l.id}: unknown ko_ref ${k}`);
    if (new Set(l.ko_refs).size !== l.ko_refs.length) fail(`${l.id}: duplicate ko_refs`);
    slots[l.practice.answer_id] = (slots[l.practice.answer_id] ?? 0) + 1;
    const texts = l.practice.options.map((o) => o.text_ar);
    if (new Set(texts).size !== 4) fail(`${l.id}: duplicate option texts`);
    const all = JSON.stringify(l);
    for (const b of BANNED) if (all.includes(b)) fail(`${l.id}: banned phrase «${b}»`);
    const words = [l.intro_ar, ...l.body_ar, l.worked_example_ar, l.common_mistake_ar].join(" ").split(/\s+/).length;
    rows.push({ id: l.id, min: l.minutes, words, ko: l.ko_refs.length, ans: l.practice.answer_id, case: l.case_link ?? "-" });
  }
}
if (data.tracks.length !== 6) fail("expected 6 tracks");
if (lessonIds.size !== 36) fail(`expected 36 lessons, got ${lessonIds.size}`);
for (const [k, v] of Object.entries(slots)) if (v > 11) fail(`answer slot ${k} used ${v} times (>11)`);
for (const k of ["c000_lost_notebook", "c001_last_observation"])
  if (!data.tracks.some((t) => t.lessons.some((l) => l.case_link === k))) fail(`no lesson links to ${k}`);

console.table(rows);
console.log("answer slots:", slots);
if (errors.length) {
  console.error("FAIL\n" + errors.map((e) => " - " + e).join("\n"));
  process.exit(1);
}
console.log("OK: 6 tracks, 36 lessons");
