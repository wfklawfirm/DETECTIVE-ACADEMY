import { assess } from "../engine/assess";
import type { PlayState } from "../engine/types";
import type { Actor } from "./auth";
import { listPlayable, getPlayable, ageAllows, type CaseCard } from "./content";
import { q } from "./db";
import { verifyToken } from "./crypto";
import koNames from "../../content/knowledge/ko_names.json";

export interface CaseProgress {
  case_id: string; title_ar: string; machine: string; done: boolean; submitted: boolean;
  evidence_count: number; locked_count: number; updated_at: string;
}

async function statesFor(actor: Actor, tokens: Record<string, string> | undefined): Promise<Map<string, PlayState>> {
  const out = new Map<string, PlayState>();
  if (actor.kind === "account" && actor.user) {
    const rows = await q<{ case_id: string; state_json: string }>("SELECT case_id, state_json FROM play_states WHERE user_id = ?", [actor.user.id]);
    for (const r of rows) out.set(r.case_id, JSON.parse(r.state_json) as PlayState);
  } else {
    for (const [caseId, tok] of Object.entries(tokens ?? {}).slice(0, 40)) {
      if (!/^[a-z][a-z0-9_]{1,63}$/.test(caseId)) continue;
      const st = verifyToken<PlayState>(tok, `state:${caseId}`);
      if (st && st.case_id === caseId) out.set(caseId, st);
    }
  }
  return out;
}

export async function progressFor(actor: Actor, tokens: Record<string, string> | undefined): Promise<{ cases: CaseProgress[]; cards: CaseCard[] }> {
  const band = actor.ageBand ?? "16-17";
  const cards = await listPlayable(band);
  const states = await statesFor(actor, tokens);
  const cases: CaseProgress[] = [];
  for (const [caseId, st] of states) {
    const lc = await getPlayable(caseId);
    if (!lc || !ageAllows(lc.core.meta.age_band, band)) continue;
    cases.push({
      case_id: caseId, title_ar: lc.ui.cover.title_ar, machine: st.machine,
      done: st.machine === "resolved" || st.machine === "review",
      submitted: !!st.submission,
      evidence_count: st.evidence.length, locked_count: Math.max(0, lc.core.evidence.length - st.evidence.length), updated_at: st.updated_at,
    });
  }
  return { cases, cards };
}

export interface SkillRow { ko_id: string; name_ar: string; level: number; cases: string[]; track: string | null }

/** Skill profile is derived (never stored) from deterministic assessments: a level 0-4 per skill, always "provisional". */
export async function skillProfile(actor: Actor, tokens: Record<string, string> | undefined): Promise<{ skills: SkillRow[]; disclaimer_ar: string; submitted_cases: number }> {
  const states = await statesFor(actor, tokens);
  const acc = new Map<string, { sum: number; n: number; cases: Set<string>; track: string | null }>();
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
        const a = acc.get(ko) ?? { sum: 0, n: 0, cases: new Set<string>(), track: lc.ui.skills.find((s) => s.skill_id === ko)?.track ?? null };
        a.sum += cr.fraction * 4; a.n += 1; a.cases.add(lc.ui.cover.title_ar);
        acc.set(ko, a);
      }
    }
  }
  const names = koNames as Record<string, string>;
  const skills = [...acc.entries()].map(([ko, a]) => ({ ko_id: ko, name_ar: names[ko] ?? ko, level: Math.round((a.sum / a.n) * 10) / 10, cases: [...a.cases], track: a.track })).sort((x, y) => y.level - x.level);
  return { skills, submitted_cases: submitted, disclaimer_ar: "ملف المهارات تقدير تعليمي مبدئي مبني على سلوكك في القضايا المنجزة وقواعد معلنة. ليس مقياساً نفسياً مقنناً، ولا يصلح للمفاضلة بين الأشخاص." };
}
