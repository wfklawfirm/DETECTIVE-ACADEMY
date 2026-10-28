import type { Hint, PlayState } from "./types";

/**
 * Hint ladder policy (HINT_AND_DIFFICULTY_SYSTEM), pure functions.
 *   tier 1  nudge     narrative / metacognitive nudge. Free: never lowers the score.
 *   tier 2  question  targeted question that points at an area. Half of the authored weight.
 *   tier 3+ method    names the method or points to a specific item. Full authored weight.
 * The total penalty is capped (0.2) and, as before, hints cost independence of solving, never the skill estimate.
 */
export type HintTier = "nudge" | "question" | "method";
export const HINT_CAP = 0.2;

export const tierOf = (level: number): HintTier => (level <= 1 ? "nudge" : level === 2 ? "question" : "method");
export const TIER_AR: Record<HintTier, string> = { nudge: "تلميح حر", question: "سؤال موجِّه", method: "تلميح منهجي" };
export const TIER_COST_AR: Record<HintTier, string> = { nudge: "بلا خصم", question: "خصم صغير", method: "خصم أكبر" };
const TIER_FACTOR: Record<HintTier, number> = { nudge: 0, question: 0.5, method: 1 };

export function effectiveHintWeight(level: number, authoredWeight: number | undefined): number {
  return Math.max(0, authoredWeight ?? 0) * TIER_FACTOR[tierOf(level)];
}

export function hintPenalty(given: PlayState["hints"], ladder: Hint[]): number {
  const total = given.reduce((s, g) => {
    const h = ladder.find((x) => x.id === g.hint_id);
    return s + effectiveHintWeight(h?.level ?? g.level, h?.assessment_weight);
  }, 0);
  return Math.min(HINT_CAP, total);
}

export function hintCountsByTier(given: PlayState["hints"]): Record<HintTier, number> {
  const out: Record<HintTier, number> = { nudge: 0, question: 0, method: 0 };
  for (const g of given) out[tierOf(g.level)]++;
  return out;
}

/**
 * Next hint from the ladder. Rules:
 *  - never a hint already given, and only if its trigger holds (passed in as `holds`);
 *  - within one target (an inference, or "general") a level is offered only after every lower level of that target was given
 *    or none exists that currently applies (no skipping the nudge to reach the reveal);
 *  - lowest level first; hints aimed at a specific inference come before general ones of the same level.
 */
export function pickHint(ladder: Hint[], given: PlayState["hints"], holds: (h: Hint) => boolean): Hint | null {
  const givenIds = new Set(given.map((g) => g.hint_id));
  const applicable = ladder.filter((h) => !givenIds.has(h.id) && holds(h));
  const ok = applicable.filter((h) => {
    const key = h.targets_inference_id ?? "_general";
    return !applicable.some((o) => (o.targets_inference_id ?? "_general") === key && o.level < h.level);
  });
  ok.sort((a, b) => a.level - b.level || (a.targets_inference_id ? 0 : 1) - (b.targets_inference_id ? 0 : 1));
  return ok[0] ?? null;
}
