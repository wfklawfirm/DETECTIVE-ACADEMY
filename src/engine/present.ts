import { interviewOpen, characterOf } from "./dialogue";
import { evalGuard } from "./guard";
import { applyAction, EngineError } from "./state";
import type { CaseFile, PlayState } from "./types";

/**
 * Show a piece of evidence to a character. The pair is always recorded (so reveal guards in the character's knowledge scope can fire on the
 * next question). If a catalogued present_evidence action matches the pair its effects are applied as well.
 */
export function presentEvidence(c: CaseFile, prev: PlayState, evidenceId: string, charId: string, now = new Date().toISOString()): { state: PlayState; matched_action: string | null } {
  if (prev.machine !== "investigating") throw new EngineError("not_investigating", "التحقيق غير مفتوح");
  characterOf(c, charId);
  if (!c.evidence.some((e) => e.id === evidenceId)) throw new EngineError("unknown_evidence", "دليل غير معروف");
  if (!prev.evidence.includes(evidenceId)) throw new EngineError("not_owned", "لا تملك هذا الدليل بعد");
  if (!interviewOpen(c, prev, charId)) throw new EngineError("interview_closed", "ابدأ المقابلة أولاً");
  const act = c.mechanics.actions.find((a) => a.type === "present_evidence" && "presented" in a.precondition && a.precondition.presented.evidence_id === evidenceId && a.precondition.presented.to_character === charId);
  if (act) {
    const r = applyAction(c, prev, act.id, { presented: { evidence_id: evidenceId, to: charId } }, now);
    return { state: r.state, matched_action: act.id };
  }
  const st = structuredClone(prev);
  if (!st.presented.some((p) => p.evidence_id === evidenceId && p.to === charId)) st.presented.push({ evidence_id: evidenceId, to: charId });
  st.seq += 1;
  st.log.push({ seq: st.seq, action: "present", target: `${evidenceId}:${charId}` });
  st.updated_at = now;
  void evalGuard;
  return { state: st, matched_action: null };
}
