import { z } from "zod";

/** Pure season logic. No fs, no Next: safe for client and server. */
const caseRef = z.object({ case: z.string().regex(/^c\d{3}(_[a-z0-9_]+)?$/), optional: z.boolean().optional() });

export const EpisodeSchema = z.object({
  id: z.string().regex(/^[a-z]\d+$/),
  kind: z.enum(["tutorial", "episode", "break", "finale", "transfer", "side", "bonus"]),
  title_ar: z.string().min(1),
  hook_ar: z.string().min(1),
  principle_ar: z.string().min(1),
  optional: z.boolean().optional(),
  link: z.object({ href: z.string().startsWith("/"), label_ar: z.string().min(1) }).optional(),
  cases: z.array(caseRef),
});

export const SeasonSchema = z.object({
  version: z.string(),
  id: z.string(),
  title_ar: z.string().min(1),
  lead_ar: z.string().min(1),
  status: z.literal("proposal_unvalidated"),
  note_ar: z.string().min(1),
  episodes: z.array(EpisodeSchema).min(1),
});
export type Season = z.infer<typeof SeasonSchema>;
export type Episode = z.infer<typeof EpisodeSchema>;

/** A ref is a full id or a short code (c022) that matches the first existing id starting with "c022_". */
export function resolveRef(ref: string, existing: readonly string[]): string | null {
  if (existing.includes(ref)) return ref;
  return existing.find((id) => id.startsWith(ref + "_")) ?? null;
}

export interface ResolvedEpisode extends Omit<Episode, "cases"> {
  /** existing case ids for this episode, in author order (an episode lists alternatives per age band, or several bonus cases) */
  case_ids: string[];
  /** refs that do not exist yet and are not marked optional: a real authoring error */
  missing: string[];
  /** refs that do not exist yet but are optional: shown as "coming" */
  pending: string[];
}

export function resolveSeason(s: Season, existing: readonly string[]): { season: Omit<Season, "episodes">; episodes: ResolvedEpisode[] } {
  const { episodes, ...rest } = s;
  return {
    season: rest,
    episodes: episodes.map(({ cases, ...e }) => {
      const case_ids: string[] = [], missing: string[] = [], pending: string[] = [];
      for (const c of cases) {
        const id = resolveRef(c.case, existing);
        if (id) case_ids.push(id);
        else (c.optional || e.optional ? pending : missing).push(c.case);
      }
      return { ...e, case_ids, missing, pending };
    }),
  };
}

export type EpState = "done" | "in_progress" | "recommended" | "open" | "coming" | "other_band" | "practice";
export interface PlayerFacts { playable: ReadonlySet<string>; done: ReadonlySet<string>; started: ReadonlySet<string> }

/** Which case does this player see for the episode, and in which state? Soft path: nothing is ever locked. */
export function episodeState(ep: ResolvedEpisode, f: PlayerFacts): { state: EpState; case_ids: string[] } {
  if (ep.kind === "break") return { state: "practice", case_ids: [] };
  const mine = ep.case_ids.filter((id) => f.playable.has(id));
  if (ep.kind === "tutorial" || ep.kind === "episode" || ep.kind === "finale" || ep.kind === "transfer") {
    // alternatives per age band: the episode counts as done when any playable alternative is done
    if (mine.some((id) => f.done.has(id))) return { state: "done", case_ids: mine.filter((id) => f.done.has(id)).slice(0, 1) };
    const started = mine.find((id) => f.started.has(id));
    if (started) return { state: "in_progress", case_ids: [started] };
    if (mine.length) return { state: "open", case_ids: mine.slice(0, 1) };
  } else {
    // side / bonus: every playable case is its own entry
    if (mine.length) {
      const allDone = mine.every((id) => f.done.has(id));
      return { state: allDone ? "done" : mine.some((id) => f.started.has(id)) ? "in_progress" : "open", case_ids: mine };
    }
  }
  if (ep.case_ids.length) return { state: "other_band", case_ids: [] };
  return { state: "coming", case_ids: [] };
}

/** First not-done, playable, non-optional episode on the recommended path. Returns its id or null. */
export function recommendedEpisode(eps: ResolvedEpisode[], f: PlayerFacts): string | null {
  for (const ep of eps) {
    if (!["tutorial", "episode", "finale", "transfer"].includes(ep.kind)) continue;
    const s = episodeState(ep, f);
    if (s.state === "in_progress" || s.state === "open") return ep.id;
  }
  return null;
}
