import { z } from "zod";
import { route } from "@/server/api";
import { dailyRiddle, shuffleOptions } from "@/engine/hooks";
import { hookData } from "@/server/hookdata";
import { loadTracks } from "@/engine/tracks";
import { loadLabs } from "@/engine/labs";
import { HttpError, json, readJson } from "@/server/http";

type LessonRef = { id: string; title_ar: string; track_id: string; track_title_ar: string };
type LabRef    = { id: string; title_ar: string; skill_ar: string; minutes: number; kind: string };

/** Build ko_ref → lesson lookup once per cold start */
function buildKoLessonMap(): Map<string, LessonRef> {
  const map = new Map<string, LessonRef>();
  const file = loadTracks();
  for (const track of file.tracks) {
    for (const lesson of track.lessons) {
      for (const ko of lesson.ko_refs) {
        if (!map.has(ko)) {
          map.set(ko, { id: lesson.id, title_ar: lesson.title_ar, track_id: track.id, track_title_ar: track.title_ar });
        }
      }
    }
  }
  return map;
}
let _koMap: Map<string, LessonRef> | null = null;
function koLessonMap() { return (_koMap ??= buildKoLessonMap()); }

/** Build ko_ref → labs lookup once per cold start */
function buildKoLabsMap(): Map<string, LabRef[]> {
  const map = new Map<string, LabRef[]>();
  const labs = loadLabs().playable;
  for (const lab of labs) {
    for (const ko of lab.ko_ids) {
      if (!map.has(ko)) map.set(ko, []);
      map.get(ko)!.push({ id: lab.id, title_ar: lab.title_ar, skill_ar: lab.skill_ar, minutes: lab.minutes, kind: lab.kind });
    }
  }
  return map;
}
let _labsMap: Map<string, LabRef[]> | null = null;
function koLabsMap() { return (_labsMap ??= buildKoLabsMap()); }

const seedOk = (s: string | null) => (s && /^[A-Za-z0-9_-]{4,64}$/.test(s) ? s : null);

export const GET = route(async (req) => {
  const seed = seedOk(new URL(req.url).searchParams.get("seed"));
  if (!seed) throw new HttpError(400, "bad_seed", "معرّف الجهاز غير صالح");
  const r = dailyRiddle(hookData().riddles, new Date(), seed);
  return json({ riddle: { id: r.id, title_ar: r.title_ar, prompt_ar: r.prompt_ar, options: shuffleOptions(r.options, `${seed}:${r.id}`) } });
});

const Body = z.object({ riddle_id: z.string().regex(/^r\d{2}$/), option_id: z.string().max(4) });
export const POST = route(async (req) => {
  const b = await readJson(req, Body, 1_000);
  const r = hookData().riddles.find((x) => x.id === b.riddle_id);
  if (!r) throw new HttpError(404, "no_riddle", "لغز غير معروف");
  if (!r.options.some((o) => o.id === b.option_id)) throw new HttpError(422, "bad_option", "خيار غير معروف");
  const lesson = r.skill_ko_ref ? (koLessonMap().get(r.skill_ko_ref) ?? null) : null;
  // Find labs that share the same ko_ref as the riddle
  const labs: LabRef[] = r.skill_ko_ref ? (koLabsMap().get(r.skill_ko_ref) ?? []).slice(0, 3) : [];
  return json({ correct: b.option_id === r.answer_id, answer_id: r.answer_id, explanation_ar: r.explanation_ar, lesson, labs });
}, { limit: 60, key: "riddle" });
