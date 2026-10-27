import { contentTokens, jaccard, ngrams, tokens } from "../lib/arabic";
import { evalGuard } from "./guard";
import { EngineError } from "./state";
import type { AuthoredLine, CaseFile, Character, KnowledgeScope, PlayState, Topic } from "./types";

export interface DialogueLine { line_id: string; purpose: AuthoredLine["purpose"]; text_ar: string; speaker_id: string }
export interface DialogueResult { state: PlayState; lines: DialogueLine[]; unlocked_facts: string[]; topic_id: string | null }

const MAX_LINES = 3;

export function characterOf(c: CaseFile, id: string): Character {
  const ch = c.entities.characters.find((x) => x.id === id);
  if (!ch) throw new EngineError("unknown_character", "شخصية غير معروفة");
  return ch;
}
const scopeOf = (c: CaseFile, id: string): KnowledgeScope =>
  c.character_knowledge.find((k) => k.character_id === id) ?? { character_id: id, knows: [], hides: [], believes: [] };
const lineBy = (ch: Character, pred: (l: AuthoredLine) => boolean) => (ch.authored_lines ?? []).find(pred);

/** Has the player opened an interview with this character yet? (needed before topic questions) */
export function interviewOpen(c: CaseFile, st: PlayState, charId: string): boolean {
  const acts = c.mechanics.actions.filter((a) => a.type === "interview" && a.target_id === charId);
  if (!acts.length) return true;
  return st.log.some((l) => acts.some((a) => a.id === l.action));
}

/** Topics the player may raise with a character (only those where the character has something in scope). */
export function topicsFor(c: CaseFile, charId: string): Topic[] {
  const ks = scopeOf(c, charId);
  const f = new Set([...ks.knows.map((k) => k.fact_id), ...ks.hides.map((h) => h.fact_id)]);
  const cl = new Set(ks.believes.map((b) => b.claim_id));
  return (c.dialogue?.topics ?? []).filter((t) => t.fact_ids.some((x) => f.has(x)) || (t.claim_ids ?? []).some((x) => cl.has(x)));
}

export function matchTopic(c: CaseFile, charId: string, text: string): Topic | null {
  const q = contentTokens(text);
  if (q.length === 0) return null;
  let best: { t: Topic; s: number } | null = null;
  for (const t of topicsFor(c, charId)) {
    const hay = contentTokens([t.label_ar, ...(t.example_questions_ar ?? [])].join(" "));
    const s = jaccard(q, hay) + (q.filter((x) => hay.includes(x)).length >= 2 ? 0.2 : 0);
    if (!best || s > best.s) best = { t, s };
  }
  return best && best.s >= 0.18 ? best.t : null;
}

/** Deterministic, closed-world dialogue: only authored lines can be spoken; facts unlock only via the character's knowledge scope. */
export function ask(c: CaseFile, prev: PlayState, charId: string, topicId: string | null, now = new Date().toISOString()): DialogueResult {
  if (prev.machine !== "investigating") throw new EngineError("not_investigating", "التحقيق غير مفتوح");
  const ch = characterOf(c, charId);
  if (!interviewOpen(c, prev, charId)) throw new EngineError("interview_closed", "ابدأ المقابلة أولاً");
  const st = structuredClone(prev);
  const iv = (st.interviews[charId] ??= { turns: 0, asked: [] });
  const maxTurns = c.dialogue?.max_turns_per_interview ?? 12;
  if (iv.turns >= maxTurns) throw new EngineError("turn_limit", "انتهى وقت المقابلة؛ يمكنك العودة بعد جمع أدلة جديدة");
  const ks = scopeOf(c, charId);
  const lines: DialogueLine[] = [];
  const unlocked: string[] = [];
  const push = (l: AuthoredLine | undefined) => {
    if (!l || lines.some((x) => x.line_id === l.line_id) || lines.length >= MAX_LINES) return;
    lines.push({ line_id: l.line_id, purpose: l.purpose, text_ar: l.text_ar, speaker_id: charId });
  };
  const unlock = (ids?: string[]) => { for (const f of ids ?? []) if (!st.facts.includes(f)) { st.facts.push(f); unlocked.push(f); } };

  if (iv.turns === 0) push(lineBy(ch, (l) => l.purpose === "greeting"));
  const topic = topicId ? (c.dialogue?.topics ?? []).find((t) => t.id === topicId) ?? null : null;
  if (topicId && !topic) throw new EngineError("unknown_topic", "موضوع غير معروف");

  if (!topic) {
    push(lineBy(ch, (l) => l.purpose === "deflect_offtopic") ?? lineBy(ch, (l) => l.purpose === "deflect_unknown"));
  } else {
    let said = 0;
    // hidden facts first (cover or reveal)
    for (const h of ks.hides) {
      if (!topic.fact_ids.includes(h.fact_id)) continue;
      if (evalGuard(h.reveal_when, st)) {
        const rl = h.reveal_line_id ? lineBy(ch, (l) => l.line_id === h.reveal_line_id) : lineBy(ch, (l) => l.purpose === "reveal" && (l.fact_ids ?? []).includes(h.fact_id));
        if (rl) { push(rl); unlock(rl.fact_ids ?? [h.fact_id]); said++; }
      } else if (h.cover_claim_id) {
        const cl = lineBy(ch, (l) => l.purpose === "lie" && (l.claim_ids ?? []).includes(h.cover_claim_id!));
        if (cl) { push(cl); said++; }
      } else {
        const rf = lineBy(ch, (l) => l.purpose === "refuse_secret");
        if (rf) { push(rf); said++; }
      }
    }
    const hidden = new Set(ks.hides.map((h) => h.fact_id));
    for (const k of ks.knows) {
      if (!topic.fact_ids.includes(k.fact_id) || hidden.has(k.fact_id)) continue;
      if (k.available_from_state && !(st.machine === k.available_from_state || st.sub === k.available_from_state || st.events.includes(k.available_from_state))) continue;
      const l = lineBy(ch, (x) => x.purpose === "reveal" && (x.fact_ids ?? []).includes(k.fact_id));
      if (l) { push(l); unlock(l.fact_ids); said++; }
    }
    for (const b of ks.believes) {
      if (!(topic.claim_ids ?? []).includes(b.claim_id)) continue;
      const covered = lines.some((l) => (ch.authored_lines ?? []).find((x) => x.line_id === l.line_id)?.claim_ids?.includes(b.claim_id));
      if (covered) continue;
      const l = lineBy(ch, (x) => (x.purpose === "lie" || x.purpose === "reveal") && (x.claim_ids ?? []).includes(b.claim_id));
      if (l) { push(l); said++; }
    }
    if (!said) push(lineBy(ch, (l) => l.purpose === "deflect_unknown"));
    if (!iv.asked.includes(topic.id)) iv.asked.push(topic.id);
  }
  iv.turns += 1;
  st.seq += 1; st.updated_at = now;
  st.transcript.push({ seq: st.seq, char_id: charId, topic_id: topic?.id ?? "_free", line_ids: lines.map((l) => l.line_id) });
  st.log.push({ seq: st.seq, action: "ask", target: `${charId}:${topic?.id ?? "_free"}` });
  return { state: st, lines, unlocked_facts: unlocked, topic_id: topic?.id ?? null };
}

// ---------- guard for any (future) generative provider ----------
export interface GeneratedTurn { text_ar: string; used_fact_ids: string[]; used_claim_ids?: string[] }
export interface GuardVerdict { ok: boolean; violations: string[] }

/** Validate a candidate line (from any provider) against the character's permitted knowledge. Fail => caller must fall back to the deterministic provider. */
export function guardGenerated(c: CaseFile, st: PlayState, charId: string, g: GeneratedTurn): GuardVerdict {
  const v: string[] = [];
  const ch = characterOf(c, charId);
  const ks = scopeOf(c, charId);
  const hiddenOpen = new Set(ks.hides.filter((h) => evalGuard(h.reveal_when, st)).map((h) => h.fact_id));
  const hiddenClosed = new Set(ks.hides.filter((h) => !evalGuard(h.reveal_when, st)).map((h) => h.fact_id));
  const allowed = new Set([...ks.knows.map((k) => k.fact_id).filter((f) => !hiddenClosed.has(f)), ...hiddenOpen, ...st.facts.filter((f) => c.premise.public_fact_ids.includes(f))]);
  for (const f of g.used_fact_ids) if (!allowed.has(f)) v.push(`fact_out_of_scope:${f}`);
  for (const cl of g.used_claim_ids ?? []) if (!ks.believes.some((b) => b.claim_id === cl)) v.push(`claim_not_held:${cl}`);
  const maxSent = ch.speech_constraints?.max_sentences_per_turn ?? 3;
  const sentences = g.text_ar.split(/[.!؟?\n]+/).filter((x) => x.trim()).length;
  if (sentences > maxSent) v.push(`too_long:${sentences}>${maxSent}`);
  const tk = tokens(g.text_ar);
  const grams = ngrams(tk, 4);
  // leakage: overlap with statements of facts the character may NOT voice, or the solution summary / reference answer
  const guardTexts: [string, string][] = [];
  for (const f of c.truth.facts) if (!allowed.has(f.id) && f.spoiler_level >= 1) guardTexts.push([`fact:${f.id}`, f.statement_ar]);
  guardTexts.push(["solution_summary", c.truth.solution.summary_ar], ["reference_answer", c.rubric.reference_answer_ar]);
  for (const [name, text] of guardTexts) {
    const t = tokens(text);
    const shared = [...ngrams(t, 4)].filter((x) => grams.has(x)).length;
    if (shared >= 1 || jaccard(contentTokens(g.text_ar), contentTokens(text)) > 0.55) v.push(`leak:${name}`);
  }
  for (const f of ch.speech_constraints?.forbidden_topics_ar ?? []) if (f && g.text_ar.includes(f)) v.push(`forbidden_topic:${f}`);
  return { ok: v.length === 0, violations: v };
}
