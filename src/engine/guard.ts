import type { Guard, PlayState } from "./types";

/** Evaluate the declarative guard DSL against a play state. Pure, no side effects. */
export function evalGuard(g: Guard | undefined, st: PlayState): boolean {
  if (!g) return true;
  if ("always" in g) return g.always === true;
  if ("has_evidence" in g) return st.evidence.includes(g.has_evidence);
  if ("fact_unlocked" in g) return st.facts.includes(g.fact_unlocked);
  if ("presented" in g)
    return st.presented.some((p) => p.evidence_id === g.presented.evidence_id && p.to === g.presented.to_character);
  if ("in_state" in g) return st.machine === g.in_state || st.sub === g.in_state || `${st.machine}.${st.sub}` === g.in_state;
  if ("trust_at_least" in g) return (st.trust[g.trust_at_least.character_id] ?? 0) >= g.trust_at_least.level;
  if ("all" in g) return g.all.every((x) => evalGuard(x, st));
  if ("any" in g) return g.any.some((x) => evalGuard(x, st));
  if ("not" in g) return !evalGuard(g.not, st);
  return false;
}

/** Collect evidence/fact ids referenced by a guard (used by static analysis). */
export function guardRefs(g: Guard | undefined, out: { evidence: Set<string>; facts: Set<string> } = { evidence: new Set(), facts: new Set() }) {
  if (!g || "always" in g) return out;
  if ("has_evidence" in g) out.evidence.add(g.has_evidence);
  else if ("fact_unlocked" in g) out.facts.add(g.fact_unlocked);
  else if ("presented" in g) out.evidence.add(g.presented.evidence_id);
  else if ("all" in g) g.all.forEach((x) => guardRefs(x, out));
  else if ("any" in g) g.any.forEach((x) => guardRefs(x, out));
  else if ("not" in g) guardRefs(g.not, out);
  return out;
}
