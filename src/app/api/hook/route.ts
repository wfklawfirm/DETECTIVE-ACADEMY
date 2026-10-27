import { z } from "zod";
import { route } from "@/server/api";
import { getActor } from "@/server/auth";
import { run } from "@/server/db";
import { selectHook, type HookContext } from "@/engine/hooks";
import { getPlayable } from "@/server/content";
import { hookData } from "@/server/hookdata";
import { json, readJson } from "@/server/http";
import { progressFor } from "@/server/progress";

const Body = z.object({
  surface: z.enum(["landing", "home", "case_open", "case_return"]),
  case_id: z.string().regex(/^[a-z][a-z0-9_]{1,63}$/).optional(),
  entry_counter: z.number().int().min(0).max(1_000_000),
  recent_ids: z.array(z.string().max(80)).max(8),
  seed: z.string().min(1).max(64),
  gentle: z.boolean().optional(),
  tokens: z.record(z.string().max(64), z.string().max(180_000)).optional(),
});

/** One hook per entry. Titles and counts come from the server's own state/registry; nothing from the client is rendered unverified. */
export const POST = route(async (req) => {
  const b = await readJson(req, Body, 3_000_000);
  const actor = await getActor(req);
  const { cases } = await progressFor(actor, b.tokens);
  let stage: HookContext["case_stage_hook"] = null;
  if (b.case_id) {
    const lc = await getPlayable(b.case_id);
    const st = cases.find((c) => c.case_id === b.case_id);
    if (lc) stage = { case_id: b.case_id, text_ar: lc.ui.stage_hooks_ar[st?.machine ?? "briefing"] ?? lc.ui.cover.tagline_ar };
  }
  const gentle = actor.user ? !!actor.user.gentle_hooks : !!b.gentle;
  const hook = selectHook(hookData().hooks, {
    surface: b.surface, cases: cases.map((c) => ({ ...c })), recent_ids: b.recent_ids, entry_counter: b.entry_counter, seed: b.seed, gentle, case_stage_hook: stage,
  });
  if (actor.user) await run("INSERT INTO hook_events(user_id, hook_id, surface, shown_at) VALUES (?,?,?,?)", [actor.user.id, hook.id, b.surface, new Date().toISOString()]);
  return json({ hook });
});
