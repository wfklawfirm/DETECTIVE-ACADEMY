import { z } from "zod";
import { assess } from "@/engine/assess";
import { estimateAll, nextStep, type Observation } from "@/engine/mastery";
import { loadTracks } from "@/engine/tracks";
import type { PlayState } from "@/engine/types";
import { route } from "@/server/api";
import { getActor } from "@/server/auth";
import { verifyToken } from "@/server/crypto";
import { getPlayable } from "@/server/content";
import { q } from "@/server/db";
import { json, readJson } from "@/server/http";
import koNames from "../../../../content/knowledge/ko_names.json";

const Body = z.object({ tokens: z.record(z.string().max(64), z.string().max(180_000)).optional() });

/** Mastery is derived on every request from the player's own submitted cases. Nothing is stored and nothing is fabricated. */
export const POST = route(async (req) => {
  const b = await readJson(req, Body, 3_000_000);
  const actor = await getActor(req);
  const states = new Map<string, PlayState>();
  if (actor.kind === "account" && actor.user) {
    const rows = await q<{ case_id: string; state_json: string }>("SELECT case_id, state_json FROM play_states WHERE user_id = ?", [actor.user.id]);
    for (const r of rows) states.set(r.case_id, JSON.parse(r.state_json) as PlayState);
  } else {
    for (const [caseId, tok] of Object.entries(b.tokens ?? {}).slice(0, 40)) {
      if (!/^[a-z][a-z0-9_]{1,63}$/.test(caseId)) continue;
      const st = verifyToken<PlayState>(tok, `state:${caseId}`);
      if (st && st.case_id === caseId) states.set(caseId, st);
    }
  }
  const obs: Observation[] = [];
  const meta = new Map<string, { track: string | null; titles: Set<string> }>();
  let submitted = 0;
  for (const [caseId, st] of states) {
    if (!st.submission) continue;
    const lc = await getPlayable(caseId);
    if (!lc) continue;
    submitted++;
    const res = assess(lc.core, lc.ui, lc.scoring, st, st.submission);
    const objSkill = new Map(lc.core.learning_objectives.map((o) => [o.id, o.skill_ko_ref]));
    for (const cr of res.criteria) {
      if (cr.fraction === null) continue;
      const crit = lc.core.rubric.criteria.find((x) => x.id === cr.id);
      for (const oid of crit?.objective_ids ?? []) {
        const ko = objSkill.get(oid);
        if (!ko) continue;
        obs.push({ ko_id: ko, case_id: caseId, score: cr.fraction, at: st.updated_at });
        const m = meta.get(ko) ?? { track: lc.ui.skills.find((s) => s.skill_id === ko)?.track ?? null, titles: new Set<string>() };
        m.titles.add(lc.ui.cover.title_ar);
        meta.set(ko, m);
      }
    }
  }
  const { tracks } = loadTracks();
  const lessonOf = (ko: string) => tracks.flatMap((t) => t.lessons).find((l) => l.ko_refs.includes(ko))?.id;
  const names = koNames as Record<string, string>;
  const est = estimateAll(obs);
  const next = nextStep(est, lessonOf);
  const lessonTitle = next?.lesson_id ? tracks.flatMap((t) => t.lessons).find((l) => l.id === next.lesson_id)?.title_ar : undefined;
  return json({
    submitted_cases: submitted,
    skills: est.map((e) => ({ ko_id: e.ko_id, name_ar: names[e.ko_id] ?? e.ko_id, status: e.status, certainty: e.certainty, cases: [...(meta.get(e.ko_id)?.titles ?? [])], track: meta.get(e.ko_id)?.track ?? null, lesson_id: lessonOf(e.ko_id) ?? null })),
    next: next ? { ...next, name_ar: names[next.ko_id] ?? next.ko_id, lesson_title_ar: lessonTitle ?? null } : null,
  });
});
