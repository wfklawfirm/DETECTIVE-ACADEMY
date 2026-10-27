# VENDORED COPY (unchanged logic) of 10_TECHNICAL_ARCHITECTURE/prototypes/fairness_check.py, copied 2026-10-27
# for use by 13_CASE_DESIGN_REFERENCE/tools/check_case.py. Do not edit here; fix upstream and re-copy.
"""Prototype: referential integrity + fairness check for an ATHAR case package (draft 0.1.0).
Monotonic over-approximation: 'not' guards are treated as satisfiable for reachability."""
import json, sys, itertools

def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)

def ids(case):
    out = {}
    for c in case["entities"]["characters"]: out[c["id"]] = "character"
    for k in ("locations", "objects", "organizations"):
        for e in case["entities"].get(k, []): out[e["id"]] = k
    for f in case["truth"]["facts"]: out[f["id"]] = "fact"
    for c in case["truth"].get("claims", []): out[c["id"]] = "claim"
    for e in case["evidence"]: out[e["id"]] = "evidence"
    for i in case["evidence_graph"]["inferences"]: out[i["id"]] = "inference"
    for h in case["hypotheses"]: out[h["id"]] = "hypothesis"
    for a in case["mechanics"]["actions"]: out[a["id"]] = "action"
    return out

def integrity(case):
    known, errs = ids(case), []
    def need(i, where):
        if i not in known: errs.append(f"{where}: unknown id '{i}'")
    for e in case["evidence"]:
        for a in e["acquired_by_action_ids"]: need(a, e["id"])
        for f in e["supports_fact_ids"]: need(f, e["id"])
        for c in e.get("contradicts_claim_ids", []): need(c, e["id"])
    for i in case["evidence_graph"]["inferences"]:
        for p in i["premises"]:
            if p["ref_type"] != "general_knowledge": need(p["ref_id"], i["id"])
        need(i["conclusion"]["ref_id"], i["id"])
    for ks in case["character_knowledge"]:
        need(ks["character_id"], "knowledge")
        for k in ks["knows"] + ks["hides"]: need(k["fact_id"], ks["character_id"])
    for c in case["truth"].get("claims", []):
        if not c["contradicted_by_evidence_ids"] and not c.get("unresolved_by_design"):
            errs.append(f"claim {c['id']}: no contradicting evidence and not marked unresolved")
    return errs

def reachable_evidence(case):
    """Fixpoint over actions; returns evidence the player can obtain."""
    have, facts, changed = set(), set(case["premise"]["public_fact_ids"]), True
    def ok(g):
        k = next(iter(g))
        if k == "always": return True
        if k == "has_evidence": return g[k] in have
        if k == "fact_unlocked": return g[k] in facts
        if k == "presented": return g[k]["evidence_id"] in have
        if k == "all": return all(ok(x) for x in g[k])
        if k == "any": return any(ok(x) for x in g[k])
        return True  # not / in_state / trust_at_least: over-approximate
    while changed:
        changed = False
        for a in case["mechanics"]["actions"]:
            if ok(a["precondition"]):
                for eff in a["effects"]:
                    if eff["op"] == "grant_evidence" and eff["ref_id"] not in have: have.add(eff["ref_id"]); changed = True
                    if eff["op"] == "unlock_fact" and eff["ref_id"] not in facts: facts.add(eff["ref_id"]); changed = True
    return have

def closure(case, ev):
    derived, changed = set(ev), True
    infs = case["evidence_graph"]["inferences"]
    while changed:
        changed = False
        for i in infs:
            if i["id"] in derived: continue
            if all(p["ref_type"] == "general_knowledge" or p["ref_id"] in derived for p in i["premises"]):
                derived.add(i["id"]); changed = True
                if i["relation"] in ("establishes",) and i["conclusion"]["ref_type"] == "fact":
                    derived.add(i["conclusion"]["ref_id"])
    return derived

def solved(case, ev):
    d = closure(case, ev)
    infs = [i for i in case["evidence_graph"]["inferences"] if i["id"] in d]
    for h in case["hypotheses"]:
        rel = {i["relation"] for i in infs if i["conclusion"]["ref_id"] == h["id"]}
        if h["is_true"] and not rel & {"supports", "establishes"}: return False
        if not h["is_true"] and not rel & {"rules_out", "refutes"}: return False
    return True

def fairness(case, max_ev=16):
    reach = sorted(reachable_evidence(case))
    report = {"reachable_evidence": reach, "unreachable_evidence": sorted({e["id"] for e in case["evidence"]} - set(reach))}
    if len(reach) > max_ev:
        report["note"] = "too many evidence items for brute force; use ASP encoding"; return report
    minimal = []
    for k in range(1, len(reach) + 1):
        for combo in itertools.combinations(reach, k):
            s = set(combo)
            if any(m <= s for m in minimal): continue
            if solved(case, s): minimal.append(s)
    disjoint = []
    for m in sorted(minimal, key=len):
        if all(not (m & d) for d in disjoint): disjoint.append(m)
    req = case["fairness_test"]["requirements"]
    report.update({
        "solvable": bool(minimal),
        "minimal_evidence_sets": [sorted(m) for m in minimal],
        "disjoint_paths": len(disjoint),
        "meets_min_disjoint_paths": len(disjoint) >= req["min_disjoint_proof_paths"],
    })
    return report

if __name__ == "__main__":
    case = load(sys.argv[1])
    print(json.dumps({"integrity_errors": integrity(case), "fairness": fairness(case)}, ensure_ascii=False, indent=1))
