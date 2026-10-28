import { z } from "zod";
import { readFileSync } from "node:fs";
import { join } from "node:path";

const koId = z.string().regex(/^KO-[A-Z0-9]+-\d{2}[A-Z]?-\d{3}$/);

export const OptionSchema = z.object({
  id: z.enum(["a", "b", "c", "d"]),
  text_ar: z.string().min(1),
});

export const LessonSchema = z
  .object({
    id: z.string().regex(/^[A-F][1-9]$/),
    title_ar: z.string().min(1),
    minutes: z.number().int().min(3).max(7),
    ko_refs: z.array(koId),
    intro_ar: z.string().min(1),
    body_ar: z.array(z.string().min(1)).min(3).max(5),
    worked_example_ar: z.string().min(1),
    common_mistake_ar: z.string().min(1),
    practice: z.object({
      prompt_ar: z.string().min(1),
      options: z.array(OptionSchema).length(4),
      answer_id: z.enum(["a", "b", "c", "d"]),
      explanation_ar: z.string().min(1),
    }),
    case_link: z.string().regex(/^c\d{3}_[a-z0-9_]+$/).optional(),
  })
  .superRefine((l, ctx) => {
    const ids = l.practice.options.map((o) => o.id).sort().join("");
    if (ids !== "abcd") ctx.addIssue({ code: "custom", message: `${l.id}: options must be a,b,c,d` });
    if (!l.practice.options.some((o) => o.id === l.practice.answer_id))
      ctx.addIssue({ code: "custom", message: `${l.id}: answer_id not in options` });
  });

export const TrackSchema = z.object({
  id: z.enum(["A", "B", "C", "D", "E", "F"]),
  title_ar: z.string().min(1),
  summary_ar: z.string().min(1),
  glyph: z.string().min(1).max(4),
  lessons: z.array(LessonSchema).min(1),
});

export const TracksSchema = z.object({
  version: z.string(),
  tracks: z.array(TrackSchema).min(1),
});

export type TracksFile = z.infer<typeof TracksSchema>;
export type Track = z.infer<typeof TrackSchema>;
export type Lesson = z.infer<typeof LessonSchema>;

export function loadTracks(): TracksFile {
  const p = join(process.cwd(), "content", "tracks", "tracks.json");
  return TracksSchema.parse(JSON.parse(readFileSync(p, "utf8")));
}

export function lessonById(file: TracksFile, id: string): Lesson | undefined {
  for (const t of file.tracks) {
    const l = t.lessons.find((x) => x.id === id);
    if (l) return l;
  }
  return undefined;
}
