import { z } from "zod";
import { assess, scoreTransfer, validateSubmission, type AssessmentResult, type TransferResult } from "../engine/assess";
import { ask, matchTopic } from "../engine/dialogue";
import { addHypothesis, addJournal, linkEvidence, nextHint, placeOnTimeline, runLab, setConfidence, setStance, tagSource, type LabOutput } from "../engine/ops";
import { presentEvidence } from "../engine/present";
import { projectView, type PlayerView } from "../engine/project";
import { applyAction, EngineError, getAction, initState, sendEvent } from "../engine/state";
import type { PlayState } from "../engine/types";
import type { Actor } from "./auth";
import { randomId, signToken, verifyToken } from "./crypto";
import { q1, run } from "./db";
import { HttpError } from "./http";
import { getPlayable, ageAllows, type LoadedCase } from "./content";

const id = z.string().regex(/^[a-z][a-z0-9_]{1,63}$/);

export const PlaySchema = z.discriminatedUnion("op", [
  z.object({ op: z.literal("state") }),
  z.object({ op: z.literal("start") }),
  z.object({ op: z.literal("act"), action_id: id }),
  z.object({ op: z.literal("ask"), character_id: id, topic_id: id.nullable().optional(), text: z.string().max(300).optional() }),
  z.object({ op: z.literal("present"), evidence_id: id, character_id: id }),
  z.object({ op: z.literal("hyp_add"), hypothesis_id: id }),
  z.object({ op: z.literal("hyp_conf"), hypothesis_id: id, value: z.number().min(0).max(100) }),
  z.object({ op: z.literal("hyp_stance"), hypothesis_id: id, stance: z.enum(["open", "leading", "ruled_out"]), evidence_ids: z.array(id).max(12).optional() }),
  z.object({ op: z.literal("hyp_link"), hypothesis_id: id, evidence_id: id, dir: z.enum(["supports", "weakens", "neutral"]) }),
  z.object({ op: z.literal("tag"), evidence_id: id, cls: z.enum(["primary_record", "redisplay", "claim", "template", "public_document"]) }),
  z.object({ op: z.literal("timeline"), evidence_id: id, minute: z.number().int().min(-1440).max(20160), note: z.string().max(200).optional() }),
  z.object({ op: z.literal("lab"), lab_id: id, inputs: z.record(z.string().max(80), z.number().finite()).refine((o) => Object.keys(o).length <= 40, "too many inputs") }),
  z.object({ op: z.literal("hint") }),
  z.object({ op: z.literal("note"), text: z.string().min(1).max(1000) }),
  z.object({ op: z.literal("deduce"), open: z.boolean() }),
  z.object({
    op: z.literal("submit"),
    conclusion_hypothesis_id: id, confidence: z.number().min(0).max(100),
    cited: z.array(z.object({ evidence_id: id, role: z.enum(["supports", "limits", "rules_out"]) })).min(1).max(12),
    limit_choice_ids: z.array(id).max(12), would_change_mind_ids: z.array(id).max(12),
    justification: z.string().max(4000), share_for_review: z.boolean().optional(),
  }),
  z.object({ op: z.literal("transfer"), picked: z.array(id).max(16), free_text: z.string().max(1500).optional() }),
  z.object({ op: z.literal("close") }),
]);
export type PlayOp = z.infer<typeof PlaySchema>;

export interface PlayResponse {
  view: PlayerView;
  token: string | null; // device mode: the new signed state token (store in localStorage)
  extra: {
    lines?: { line_id: string; purpose: string; text_ar: string; speaker_id: string }[];
    unlocked_facts?: string[];
    granted_evidence?: string[];
    lab?: LabOutput & { granted: string[] };
    hint?: { id: string; level: number; kind: string; text_ar: string } | null;
    matched_action?: string | null;
  };
  assessment: AssessmentResult | null;
  transfer: TransferResult | null;
  review_ticket: string | null;
  preview: boolean;
}

const purpose = (caseId: string) => `state:${caseId}`;

export async function loadState(actor: Actor, lc: LoadedCase, token: string | null | undefined): Promise<PlayState | null> {
  const caseId = lc.core.case_id;
  let st: PlayState | null = null;
  if (actor.kind === "account" && actor.user) {
    const row = await q1<{ state_json: string }>("SELECT state_json FROM play_states WHERE user_id = ? AND case_id = ?", [actor.user.id, caseId]);
    st = row ? (JSON.parse(row.state_json) as PlayState) : null;
  } else if (token) {
    st = verifyToken<PlayState>(token, purpose(caseId));
  }
  if (!st) return null;
  if (st.case_id !== caseId) return null;
  // A newer case version may have removed evidence that the stored state references: start over rather than serve a broken state.
  if (st.case_version !== lc.core.case_version) {
    const ev = new Set(lc.core.evidence.map((e) => e.id));
    if (st.evidence.some((e) => !ev.has(e))) return null;
    st.case_version = lc.core.case_version;
  }
  return st;
}

export async function saveState(actor: Actor, caseId: string, st: PlayState): Promise<string | null> {
  if (actor.kind === "account" && actor.user) {
    await run(
      "INSERT INTO play_states(user_id, case_id, state_json, machine, updated_at) VALUES (?,?,?,?,?) ON CONFLICT(user_id, case_id) DO UPDATE SET state_json = excluded.state_json, machine = excluded.machine, updated_at = excluded.updated_at",
      [actor.user.id, caseId, JSON.stringify(st), st.machine, st.updated_at]);
    return null;
  }
  return signToken(st, purpose(caseId));
}

const HIDDEN_ACTION_TYPES = new Set(["final_accusation", "compare_evidence", "place_on_timeline", "link_on_board", "submit_hypothesis", "rule_out", "request_hint"]);

export function assertAgeAllowed(actor: Actor, lc: LoadedCase) {
  if (!actor.ageBand) throw new HttpError(403, "age_required", "حدّد فئتك العمرية أولاً");
  if (!ageAllows(lc.core.meta.age_band, actor.ageBand)) throw new HttpError(403, "age_restricted", "هذه القضية غير متاحة لفئتك العمرية");
}

export async function handlePlay(actor: Actor, caseId: string, op: PlayOp, token: string | null | undefined): Promise<PlayResponse> {
  const lc = await getPlayable(caseId);
  if (!lc) throw new HttpError(404, "no_case", "القضية غير متاحة");
  assertAgeAllowed(actor, lc);
  const { core: c, ui, scoring: sc } = lc;
  let st = await loadState(actor, lc, token);
  const extra: PlayResponse["extra"] = {};
  const now = new Date().toISOString();

  if (!st) {
    if (op.op !== "start" && op.op !== "state") throw new HttpError(409, "not_started", "ابدأ القضية أولاً");
    st = initState(c, now);
  }

  switch (op.op) {
    case "state": break;
    case "start":
      if (st.machine === "briefing") st = sendEvent(c, st, "START", now);
      break;
    case "act": {
      const a = getAction(c, op.action_id);
      if (a.telemetry_code?.startsWith("ASK_") || HIDDEN_ACTION_TYPES.has(a.type) || a.type === "present_evidence") throw new EngineError("not_allowed", "هذا الإجراء غير متاح مباشرة");
      const r = applyAction(c, st, op.action_id, {}, now);
      st = r.state; extra.granted_evidence = r.granted_evidence; extra.unlocked_facts = r.unlocked_facts;
      break;
    }
    case "ask": {
      let topic = op.topic_id ?? null;
      if (!topic && op.text) topic = matchTopic(c, op.character_id, op.text)?.id ?? null;
      const r = ask(c, st, op.character_id, topic, now);
      st = r.state; extra.lines = r.lines; extra.unlocked_facts = r.unlocked_facts;
      break;
    }
    case "present": {
      const r = presentEvidence(c, st, op.evidence_id, op.character_id, now);
      st = r.state; extra.matched_action = r.matched_action;
      break;
    }
    case "hyp_add": st = addHypothesis(c, st, op.hypothesis_id, now); break;
    case "hyp_conf": st = setConfidence(c, st, op.hypothesis_id, op.value, now); break;
    case "hyp_stance": st = setStance(c, st, op.hypothesis_id, op.stance, op.evidence_ids ?? [], now); break;
    case "hyp_link": st = linkEvidence(c, st, op.hypothesis_id, op.evidence_id, op.dir, now); break;
    case "tag": st = tagSource(c, st, op.evidence_id, op.cls, now); break;
    case "timeline": st = placeOnTimeline(st, op.evidence_id, op.minute, op.note, now); break;
    case "lab": {
      const r = runLab(c, ui.labs, st, op.lab_id, op.inputs, now);
      st = r.state; extra.lab = { ...r.output, granted: r.granted };
      break;
    }
    case "hint": {
      if (st.machine !== "investigating") throw new EngineError("not_investigating", "لا تلميحات خارج التحقيق");
      const r = nextHint(c, st, now);
      st = r.state; extra.hint = r.hint;
      break;
    }
    case "note": st = addJournal(st, op.text, now); break;
    case "deduce": st = sendEvent(c, st, op.open ? "OPEN_DEDUCTION" : "BACK", now); break;
    case "submit": {
      if (st.machine !== "investigating") throw new EngineError("not_investigating", "الاستنتاج النهائي يُقدَّم أثناء التحقيق");
      const input = { conclusion_hypothesis_id: op.conclusion_hypothesis_id, confidence: op.confidence, cited: op.cited, limit_choice_ids: op.limit_choice_ids, would_change_mind_ids: op.would_change_mind_ids, justification: op.justification };
      validateSubmission(c, ui, st, input);
      const next = structuredClone(st);
      next.seq += 1; next.updated_at = now;
      next.submission = { ...input, seq: next.seq };
      next.log.push({ seq: next.seq, action: "submit" });
      st = next;
      st = sendEvent(c, st, "SUBMIT", now);
      if (op.share_for_review && st.submission && st.submission.justification.trim()) {
        const result = assess(c, ui, sc, st, st.submission);
        const code = randomId(6).toUpperCase().replace(/[-_]/g, "X");
        await run("INSERT INTO review_tickets(code, user_id, case_id, case_version, justification, deterministic_json, created_at) VALUES (?,?,?,?,?,?,?)",
          [code, actor.user?.id ?? null, caseId, c.case_version, st.submission.justification, JSON.stringify({ total_pct: result.total_pct, criteria: result.criteria.map((x) => ({ id: x.id, fraction: x.fraction })) }), now]);
        st.review_ticket = code;
      }
      break;
    }
    case "transfer": {
      if (st.machine !== "review" && st.machine !== "resolved") throw new EngineError("too_early", "اختبار النقل بعد تقديم الاستنتاج");
      if (!ui.transfer || !sc.transfer_key) throw new EngineError("no_transfer", "لا يوجد اختبار نقل لهذه القضية");
      const valid = new Set(ui.transfer.options.map((o) => o.id));
      for (const p of op.picked) if (!valid.has(p)) throw new EngineError("bad_option", "خيار غير معروف");
      st = { ...structuredClone(st), transfer: { picked: [...new Set(op.picked)], free_text: op.free_text ?? "", seq: st.seq + 1 }, seq: st.seq + 1, updated_at: now };
      break;
    }
    case "close": st = sendEvent(c, st, "CLOSE", now); break;
  }

  const newToken = await saveState(actor, caseId, st);
  const assessment = st.submission ? assess(c, ui, sc, st, st.submission) : null;
  const transfer = st.transfer && sc.transfer_key ? scoreTransfer(sc, st.transfer.picked) : null;
  return { view: projectView(c, ui, st, { preview: lc.preview }), token: newToken, extra, assessment, transfer, review_ticket: st.review_ticket ?? null, preview: lc.preview };
}
