import { evalGuard } from "./guard";
import type { Action, CaseFile, PlayState, SmState } from "./types";

export function initState(c: CaseFile, now = new Date().toISOString()): PlayState {
  return {
    v: 1,
    case_id: c.case_id,
    case_version: c.case_version,
    machine: c.state_machine.initial,
    sub: null,
    evidence: [],
    facts: [...c.premise.public_fact_ids],
    trust: {},
    events: [],
    presented: [],
    seq: 0,
    log: [],
    hypotheses: {},
    source_tags: {},
    timeline: [],
    lab_runs: [],
    hints: [],
    journal: [],
    interviews: {},
    transcript: [],
    started_at: now,
    updated_at: now,
  };
}

export class EngineError extends Error {
  constructor(public code: string, message: string) {
    super(message);
  }
}

export function getAction(c: CaseFile, id: string): Action {
  const a = c.mechanics.actions.find((x) => x.id === id);
  if (!a) throw new EngineError("unknown_action", `الإجراء غير معروف: ${id}`);
  return a;
}

/** Actions currently available to the player (precondition true, effects would add something or are structural). */
export function availableActions(c: CaseFile, st: PlayState): Action[] {
  return c.mechanics.actions.filter((a) => evalGuard(a.precondition, st) && !isExhausted(a, st));
}

/** An action whose only effects are grant_evidence/unlock_fact already satisfied is exhausted. */
export function isExhausted(a: Action, st: PlayState): boolean {
  const grants = a.effects.filter((e) => e.op === "grant_evidence" || e.op === "unlock_fact");
  if (!grants.length) return false;
  if (a.effects.some((e) => e.op !== "grant_evidence" && e.op !== "unlock_fact" && e.op !== "raise_trust")) return false;
  return grants.every((e) => (e.op === "grant_evidence" ? st.evidence.includes(e.ref_id!) : st.facts.includes(e.ref_id!)));
}

/** Walk the (possibly nested) state machine and apply an event. Returns true if a transition fired. */
function fire(c: CaseFile, st: PlayState, event: string): boolean {
  const top = c.state_machine.states[st.machine];
  if (!top) return false;
  // nested first
  if (st.sub && top.states?.[st.sub]) {
    const t = top.states[st.sub]?.on?.[event];
    if (t && evalGuard(t.guard, st)) {
      st.sub = t.target;
      return true;
    }
  }
  const t = top.on?.[event];
  if (t && evalGuard(t.guard, st)) {
    st.machine = t.target;
    const next: SmState | undefined = c.state_machine.states[st.machine];
    st.sub = next?.initial ?? null;
    return true;
  }
  return false;
}

export function sendMachineEvent(c: CaseFile, st: PlayState, event: string): boolean {
  const before = `${st.machine}.${st.sub}`;
  fire(c, st, event);
  return `${st.machine}.${st.sub}` !== before;
}

export interface ApplyResult {
  state: PlayState;
  granted_evidence: string[];
  unlocked_facts: string[];
  events: string[];
}

/**
 * Apply a catalogued action. Pure: returns a new state (input not mutated).
 * Throws EngineError when the precondition is false (the server never trusts the client's view of availability).
 */
export function applyAction(
  c: CaseFile,
  prev: PlayState,
  actionId: string,
  ctx: { presented?: { evidence_id: string; to: string } } = {},
  now = new Date().toISOString(),
): ApplyResult {
  const st: PlayState = structuredClone(prev);
  const a = getAction(c, actionId);
  if (st.machine === "resolved" || st.machine === "review") {
    if (a.type !== "request_hint" && a.type !== "examine") throw new EngineError("closed", "الملف مغلق للتحقيق");
  }
  if (a.type === "present_evidence") {
    if (!ctx.presented) throw new EngineError("missing_presented", "يجب تحديد الدليل والشخصية");
    if (!st.evidence.includes(ctx.presented.evidence_id)) throw new EngineError("not_owned", "لا تملك هذا الدليل بعد");
    if (!st.presented.some((p) => p.evidence_id === ctx.presented!.evidence_id && p.to === ctx.presented!.to)) st.presented.push({ evidence_id: ctx.presented.evidence_id, to: ctx.presented.to });
  }
  if (!evalGuard(a.precondition, st)) throw new EngineError("precondition", "الشرط غير متحقق بعد");

  const granted: string[] = [];
  const unlocked: string[] = [];
  const events: string[] = [];
  for (const e of a.effects) {
    switch (e.op) {
      case "grant_evidence":
        if (e.ref_id && !st.evidence.includes(e.ref_id)) {
          st.evidence.push(e.ref_id);
          granted.push(e.ref_id);
        }
        break;
      case "unlock_fact":
        if (e.ref_id && !st.facts.includes(e.ref_id)) {
          st.facts.push(e.ref_id);
          unlocked.push(e.ref_id);
        }
        break;
      case "raise_trust":
        if (e.ref_id) st.trust[e.ref_id] = Math.min(5, (st.trust[e.ref_id] ?? 0) + (e.amount ?? 1));
        break;
      case "lower_trust":
        if (e.ref_id) st.trust[e.ref_id] = Math.max(0, (st.trust[e.ref_id] ?? 0) - (e.amount ?? 1));
        break;
      case "emit_event":
        if (e.ref_id) {
          events.push(e.ref_id);
          if (!st.events.includes(e.ref_id)) st.events.push(e.ref_id);
          sendMachineEvent(c, st, e.ref_id);
        }
        break;
      case "advance_time":
        break;
    }
  }
  st.seq += 1;
  st.log.push({ seq: st.seq, action: a.id, target: a.target_id });
  st.updated_at = now;
  return { state: st, granted_evidence: granted, unlocked_facts: unlocked, events };
}

/** Explicit machine events that the UI/server may send (START, OPEN_PRESENTATION, BACK, CLOSE...). */
export function sendEvent(c: CaseFile, prev: PlayState, event: string, now = new Date().toISOString()): PlayState {
  const st = structuredClone(prev);
  const ok = sendMachineEvent(c, st, event);
  if (!ok) throw new EngineError("no_transition", "الانتقال غير متاح الآن");
  st.seq += 1;
  st.log.push({ seq: st.seq, action: `event:${event}` });
  st.updated_at = now;
  return st;
}
