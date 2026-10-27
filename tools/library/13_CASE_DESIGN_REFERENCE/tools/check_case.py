"""ATHAR case pre-publication checker (13_CASE_DESIGN_REFERENCE/tools/check_case.py).

Wraps, without modifying, the library-10 prototype (vendored as fairness_check_proto.py) and adds:
  1. JSON Schema validation against 10_TECHNICAL_ARCHITECTURE/case_schema.json (read-only).
  2. Extended deterministic checks listed in 10_TECHNICAL_ARCHITECTURE/CASE_SCHEMA_PROPOSAL.md §6
     and testable rules of 02_DETECTIVE_LITERATURE/FAIR_PLAY_MYSTERY_RULEBOOK.md (FP/NR/SC/AG codes).
  3. An ASP (clingo) fairness encoding that, unlike the prototype ASP files, compiles compound guards
     (has_evidence / presented / fact_unlocked / all / any; other guard types over-approximated as true)
     and enumerates subset-minimal solving evidence sets with clingo's domain heuristic.
  4. A content hash (sha256 of canonical JSON without fairness_test.runs and expert_review), so
     reviews and runs can be bound to the exact content they checked.
  5. Wave-2 gates (2026-10-27; CASE_DESIGN_BIBLE §18): X24 terminology against
     04_FORENSIC_SCIENCE/ARABIC_FORENSIC_GLOSSARY.md (C13) + absolute-claim phrases (SC-B);
     X25 Arabic/RTL normalisation (10_TECHNICAL_ARCHITECTURE/RTL_AUTHORING_TOOL_TESTS.md §6);
     X26 media assets must resolve in the 15_STORY_MEDIA_AND_ASSETS registers (asset licensing gate);
     X27 bias-lab ethics gate reminder (04_FORENSIC_SCIENCE/BIAS_LAB_ETHICS_FOR_MINORS.md, C14);
     X28 physiognomy / demeanour cues inside inference rules (HER-02, SC-06); and the raw-file check
     for \\u06xx-escaped Arabic (D-T3). KO refs may also resolve in unmerged */_data/knowledge_objects_w2*.jsonl
     (warning, not error) until the wave-D merge.

Usage:  python3 -I check_case.py <case.json> [--mutation-tests] [--json]
Exit code: 0 = structurally publishable (human sign-off still required), 1 = blocking failure.
Status: research prototype [design assumption]; not production code.
"""
import copy
import csv
import glob
import hashlib
import importlib.util
import itertools
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
SCHEMA_PATH = os.path.join(ROOT, "10_TECHNICAL_ARCHITECTURE", "case_schema.json")
KO_DIR = os.path.join(ROOT, "12_KNOWLEDGE_OBJECTS")
MANDATORY_REVIEW_ROLES = ["narrative_editor", "scientific_reviewer", "learning_designer",
                          "age_appropriateness", "cultural_reviewer", "legal_rights", "safety"]
# FP-10 red-herring caps (rulebook values are provisional; mapped from case difficulty)
RED_HERRING_CAP = {1: 2, 2: 3, 3: 5, 4: 5, 5: 5}
# BI-02 watch-list (identity/health words that must not appear in suspect descriptions); heuristic only
WATCHLIST_AR = ["مريض نفسي", "مجنون", "معاق", "إعاقة", "لاجئ", "أجنبي", "غريب الأطوار", "لكنته", "لهجته", "طائفة", "قبيلة"]

# ---- wave-2 constants (CASE_DESIGN_BIBLE §18) ----
ASSET_DIR = os.path.join(ROOT, "15_STORY_MEDIA_AND_ASSETS")
# X24 deprecated terms -> glossary term (04_FORENSIC_SCIENCE/ARABIC_FORENSIC_GLOSSARY.md §2). Blocking.
TERM_DEPRECATED = [
    ("نسبة الأرجحية", "نسبة الترجيح (GL-158; odds ratio = نسبة الأرجحية, GL-159)", ("odds", "نسبة الترجيح")),
    ("سلسلة الحيازة", "سلسلة العهدة (GL-023)", ()),
    ("سلسلة حيازة", "سلسلة عهدة (GL-023)", ()),
]
# X24 discouraged terms (glossary §2.3). Warning only.
TERM_DISCOURAGED = [
    ("البصمة الوراثية", "ملف الحمض النووي (GL-077); mention the common name once, with a uniqueness caveat"),
    ("البصمة الرقمية", "القيمة التجزيئية (GL-116) for a hash value"),
]
# X24 absolute claims (SC-B; 04 checklist c6). Blocking.
ABSOLUTE_AR = ["تطابق 100%", "تطابق 100٪", "تطابق ١٠٠٪", "تطابق تام لا شك فيه", "مستحيل أن يكون غيره", "يستبعد كل البشر", "دليل قاطع على الذنب"]
# X25 presentation forms, BOM and bidi controls (10/RTL_AUTHORING_TOOL_TESTS §6). ZWNJ (U+200C) is allowed in text.
RTL_BAD = re.compile("[ﭐ-﷿ﹰ-﻿‎‏‪-‮⁦-⁩]")
# X27 context-bias concepts that make a case a "bias lab" (04/BIAS_LAB_ETHICS_FOR_MINORS)
BIAS_LAB_KOS = {"KO-FC-04-027", "KO-FC-04-028"}
# X28 physiognomy / demeanour cues that must not carry an inference (HER-02; SC-06; KO-RS-05-007)
DEMEANOUR_AR = ["فراسة", "الفراسة", "ملامح", "قسمات", "لغة الجسد", "تجنب النظر", "تجنّب النظر", "ارتبك فهو", "بكى فهو"]
LOUDJUMP_RE = re.compile(r"loudjump=([0-9.]+)")


def _load_register(fn):
    p = os.path.join(ASSET_DIR, fn)
    if not os.path.exists(p):
        return {}
    with open(p, encoding="utf-8-sig") as fh:
        return {r["asset_id"]: r for r in csv.DictReader(fh) if r.get("asset_id")}


def asset_registers():
    reg = {}
    reg.update(_load_register("IMAGE_ASSET_REGISTER.csv"))
    reg.update(_load_register("AUDIO_ASSET_REGISTER.csv"))
    return reg


def iter_strings(obj, path=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from iter_strings(v, f"{path}/{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from iter_strings(v, f"{path}[{i}]")
    elif isinstance(obj, str):
        yield path, obj


def raw_file_checks(raw):
    """D-T3 in 10/ARABIC_TOKEN_COST_MEASUREMENT: Arabic stored as raw UTF-8, never \\u06xx-escaped."""
    n = len(re.findall(r"\\u06[0-9a-fA-F]{2}", raw))
    return [f"RAW {n} \\u06xx-escaped Arabic sequences: store JSON with ensure_ascii=False (D-T3)"] if n else []


def _load_proto():
    spec = importlib.util.spec_from_file_location("fairness_check_proto", os.path.join(HERE, "fairness_check_proto.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def content_hash(case):
    c = copy.deepcopy(case)
    c.get("fairness_test", {}).pop("runs", None)
    c.pop("expert_review", None)
    return "sha256:" + hashlib.sha256(json.dumps(c, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def schema_errors(case):
    try:
        import jsonschema
    except ImportError:
        return ["jsonschema not installed (pip install --break-system-packages jsonschema)"]
    schema = json.load(open(SCHEMA_PATH, encoding="utf-8"))
    jsonschema.Draft202012Validator.check_schema(schema)
    v = jsonschema.Draft202012Validator(schema)
    return [f"{'/'.join(str(p) for p in e.absolute_path) or '<root>'}: {e.message}" for e in sorted(v.iter_errors(case), key=lambda e: list(e.absolute_path))]


def known_ko_ids():
    ids = set()
    for fn in os.listdir(KO_DIR):
        if fn.endswith(".jsonl") and fn != "rag_chunks.jsonl":
            for line in open(os.path.join(KO_DIR, fn), encoding="utf-8"):
                line = line.strip()
                if line:
                    ids.add(json.loads(line)["ko_id"])
    return ids


def wave2_ko_ids():
    """KOs written by wave-2 teams but not yet merged into 12_KNOWLEDGE_OBJECTS (wave D)."""
    ids = set()
    for fn in glob.glob(os.path.join(ROOT, "*", "_data", "knowledge_objects_w2*.jsonl")):
        for line in open(fn, encoding="utf-8"):
            line = line.strip()
            if line:
                ids.add(json.loads(line)["ko_id"])
    return ids


def ko_refs_in(obj):
    out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in ("knowledge_object_refs", "science_ko_refs", "skill_ko_refs") and isinstance(v, list):
                out += v
            elif k in ("forensic_ko_ref", "skill_ko_ref") and isinstance(v, str):
                out.append(v)
            else:
                out += ko_refs_in(v)
    elif isinstance(obj, list):
        for x in obj:
            out += ko_refs_in(x)
    return out


# ---------------------------------------------------------------- extended deterministic checks
def extended_checks(case, proto, reach):
    errs, warns = [], []
    facts = {f["id"]: f for f in case["truth"]["facts"]}
    claims = {c["id"]: c for c in case["truth"].get("claims", [])}
    evidence = {e["id"]: e for e in case["evidence"]}
    infs = {i["id"]: i for i in case["evidence_graph"]["inferences"]}
    hyps = {h["id"]: h for h in case["hypotheses"]}
    chars = {c["id"]: c for c in case["entities"]["characters"]}
    derived = proto.closure(case, set(reach))

    # X02 told_by needs a source character
    for ks in case["character_knowledge"]:
        for k in ks["knows"]:
            if k["access"] == "told_by" and not k.get("source_character_id"):
                errs.append(f"X02 {ks['character_id']}: fact {k['fact_id']} access=told_by without source_character_id")

    # X03 nobody in two places at overlapping times (timeline actors and witnesses)
    spans = {}
    for ev in case["timeline"]:
        if "location_id" not in ev:
            continue
        s = ev["time"]["start_min"]
        e = ev["time"].get("end_min", s)
        for p in set(ev.get("actor_ids", []) + ev.get("witness_ids", [])):
            spans.setdefault(p, []).append((s, e, ev["location_id"], ev["id"]))
    for p, lst in spans.items():
        for a, b in itertools.combinations(lst, 2):
            if a[2] != b[2] and a[0] <= b[1] and b[0] <= a[1]:
                if a[1] == b[0] or b[1] == a[0]:
                    continue  # touching endpoints = movement between places, allowed
                errs.append(f"X03 {p} in {a[2]} ({a[3]}) and {b[2]} ({b[3]}) at overlapping times")

    # X04 intentionality: every event with actors has motivated_by_ar
    for ev in case["timeline"]:
        if ev.get("actor_ids") and not ev.get("motivated_by_ar", "").strip():
            errs.append(f"X04 timeline {ev['id']}: actor event without motivated_by_ar (FP-03)")

    # X05 evidence shows observation, not the inference text
    for i in infs.values():
        for p in i["premises"]:
            if p["ref_type"] == "evidence" and p["ref_id"] in evidence and i["rule_ar"].strip() in evidence[p["ref_id"]]["content_ar"]:
                errs.append(f"X05 evidence {p['ref_id']} content contains rule_ar of {i['id']}")

    # X06 every red herring refutable by a derivable inference; fairness note present (FP-09)
    for rh in case.get("misdirection_plan", []):
        ok = [x for x in rh["refuted_by_inference_ids"] if x in derived]
        if not ok:
            errs.append(f"X06 red herring {rh['id']}: no refuting inference derivable from reachable evidence")
        if not rh["fairness_note_ar"].strip():
            errs.append(f"X06 red herring {rh['id']}: empty fairness_note_ar (innocent explanation)")
        if rh["points_to_hypothesis_id"] in hyps and hyps[rh["points_to_hypothesis_id"]]["is_true"]:
            errs.append(f"X06 red herring {rh['id']} points to the TRUE hypothesis")

    # X07 every learning objective covered by >=1 rubric criterion
    covered = {o for c in case["rubric"]["criteria"] for o in c["objective_ids"]}
    for lo in case["learning_objectives"]:
        if lo["id"] not in covered:
            errs.append(f"X07 learning objective {lo['id']} not covered by any rubric criterion")

    # X09 spoiler-3 facts never public, never unconditionally known
    for f in facts.values():
        if f["spoiler_level"] == 3:
            if f["id"] in case["premise"]["public_fact_ids"]:
                errs.append(f"X09 spoiler-3 fact {f['id']} is public")
            for ks in case["character_knowledge"]:
                for k in ks["knows"]:
                    if k["fact_id"] == f["id"] and not k.get("available_from_state"):
                        errs.append(f"X09 spoiler-3 fact {f['id']} unconditionally known by {ks['character_id']}")

    # X10 KO refs exist in 12_KNOWLEDGE_OBJECTS (or, with a warning, in an unmerged wave-2 KO file)
    kos = known_ko_ids()
    w2kos = wave2_ko_ids()
    for r in sorted(set(ko_refs_in(case))):
        if r not in kos:
            if r in w2kos:
                warns.append(f"X10 knowledge object {r} exists only in an unmerged wave-2 file; re-check after the wave-D merge")
            else:
                errs.append(f"X10 unknown knowledge object {r}")

    # X11 FP-10 red-herring cap
    cap = RED_HERRING_CAP.get(case["meta"]["difficulty"], 5)
    if len(case.get("misdirection_plan", [])) > cap:
        errs.append(f"X11 {len(case['misdirection_plan'])} red herrings > cap {cap} for difficulty {case['meta']['difficulty']} (FP-10)")

    # X12 inference depth
    depth = {}

    def d(iid, seen=()):
        if iid in depth:
            return depth[iid]
        if iid in seen:
            return 99
        inf = infs[iid]
        best = 1
        for p in inf["premises"]:
            if p["ref_type"] == "inference" and p["ref_id"] in infs:
                best = max(best, 1 + d(p["ref_id"], seen + (iid,)))
            if p["ref_type"] == "fact":
                producers = [j for j in infs.values() if j["relation"] == "establishes" and j["conclusion"]["ref_id"] == p["ref_id"]]
                if producers:
                    best = max(best, 1 + min(d(j["id"], seen + (iid,)) for j in producers))
        depth[iid] = best
        return best
    for iid in infs:
        d(iid)
    mx = case["fairness_test"]["requirements"]["max_inference_depth"]
    deep = {k: v for k, v in depth.items() if v > mx}
    if deep:
        errs.append(f"X12 inference depth above {mx}: {deep}")

    # X13 every claim contradicted by REACHABLE evidence or unresolved_by_design
    for c in claims.values():
        if not c.get("unresolved_by_design") and not (set(c["contradicted_by_evidence_ids"]) & set(reach)):
            errs.append(f"X13 claim {c['id']}: no reachable contradicting evidence (NR-03)")

    # X14 hint ladder: targets exist, levels contiguous from 1 per target (no skipping), weights non-decreasing
    by_t = {}
    for h in case["hint_ladder"]:
        t = h.get("targets_inference_id", "_general")
        if t != "_general" and t not in infs:
            errs.append(f"X14 hint {h['id']} targets unknown inference {t}")
        by_t.setdefault(t, []).append(h)
    for t, hs in by_t.items():
        if t == "_general":
            continue
        lv = sorted(h["level"] for h in hs)
        if lv != list(range(1, len(lv) + 1)):
            errs.append(f"X14 hints for {t}: levels {lv} not contiguous from 1")
        w = [h.get("assessment_weight", 0) for h in sorted(hs, key=lambda h: h["level"])]
        if any(b < a for a, b in zip(w, w[1:])):
            errs.append(f"X14 hints for {t}: assessment_weight decreases with level")

    # X15 FP-02 analogue: each solution key fact supported by reachable evidence or established by a derivable inference
    for fid in case["truth"]["solution"]["key_fact_ids"]:
        sup = any(fid in evidence[e]["supports_fact_ids"] for e in reach)
        est = any(i["id"] in derived and i["conclusion"]["ref_id"] == fid for i in infs.values())
        if not (sup or est):
            errs.append(f"X15 key fact {fid}: no reachable evidence or derivable inference supports it (FP-02)")

    # X16 FP-07 culprit inside declared suspect space; true hypothesis names a culprit
    for cid in case["truth"]["solution"]["culprit_ids"]:
        if cid in chars and chars[cid]["role"] != "suspect":
            errs.append(f"X16 culprit {cid} has role {chars[cid]['role']} (FP-07: must be a declared suspect)")
    for h in hyps.values():
        if h["is_true"] and h.get("suspect_id") and h["suspect_id"] not in case["truth"]["solution"]["culprit_ids"]:
            errs.append(f"X16 true hypothesis {h['id']} suspect not in culprit_ids")

    # X17 NR-07 assistant / expert / authority never the culprit
    for cid in case["truth"]["solution"]["culprit_ids"]:
        if cid in chars and chars[cid]["role"] in ("assistant", "expert", "authority"):
            errs.append(f"X17 culprit {cid} is {chars[cid]['role']} (NR-07)")

    # X18 SC-02/SC-03 lab results carry limits and a reviewed forensic KO
    for e in evidence.values():
        if e["kind"] == "lab_result" and (not e.get("forensic_ko_ref") or not e["limits_ar"].strip()):
            errs.append(f"X18 lab result {e['id']} lacks forensic_ko_ref or limits_ar (SC-02/SC-03)")
        if not e["limits_ar"].strip():
            errs.append(f"X18 evidence {e['id']} has empty limits_ar")

    # X19 08 AGE_APPROPRIATE_CONTENT_POLICY §3.1 (stricter than rulebook AG-01): 13-15 = no human victims of violence
    if case["meta"]["age_band"] == "13-15":
        flags = set(case["meta"]["content_flags"])
        if "non_graphic_crime" in flags or "no_violence" not in flags:
            errs.append("X19 13-15 case must be flagged no_violence and must not carry non_graphic_crime (08 policy §3.1)")
        if "missing_person" in flags:
            warns.append("X19 missing_person at 13-15 is allowed only with a safe return (08 policy §3.1) — age reviewer must confirm")

    # X20 BI-02 watch-list in suspect personas / motives (heuristic warning)
    for c in chars.values():
        blob = " ".join([c.get("persona_ar", "")] + c.get("motives_ar", []))
        hits = [w for w in WATCHLIST_AR if w in blob]
        if hits:
            warns.append(f"X20 {c['id']}: watch-list terms {hits} — editorial substitution test required (BI-01/BI-02)")

    # X21 SC-06: no inference that supports the TRUE hypothesis may rest on red-herring evidence
    rh_ev = {e for rh in case.get("misdirection_plan", []) for e in rh.get("evidence_ids", [])}
    for i in infs.values():
        if i["relation"] in ("supports", "establishes") and i["conclusion"]["ref_type"] == "hypothesis" \
                and hyps.get(i["conclusion"]["ref_id"], {}).get("is_true"):
            bad = [p["ref_id"] for p in i["premises"] if p["ref_id"] in rh_ev]
            if bad:
                errs.append(f"X21 {i['id']} supports the true hypothesis using red-herring evidence {bad}")

    # X22 ending explanation references exist and are derivable
    for s in case["ending_explanation"]["steps"]:
        if s["inference_id"] not in infs:
            errs.append(f"X22 ending step {s['order']}: unknown inference {s['inference_id']}")
        elif s["inference_id"] not in derived:
            errs.append(f"X22 ending step {s['order']}: inference {s['inference_id']} not derivable")
        for e in s["uses_evidence_ids"]:
            if e not in evidence:
                errs.append(f"X22 ending step {s['order']}: unknown evidence {e}")

    # X23 hypotheses: >=2, at least one non-incriminating ("innocent") explanation (KO-RS-05-002)
    if not any(not h.get("suspect_id") for h in hyps.values()):
        warns.append("X23 no hypothesis without a suspect (innocent / no-crime explanation) — KO-RS-05-002")

    # ---------------- wave-2 gates (CASE_DESIGN_BIBLE §18) ----------------
    strings = list(iter_strings({k: v for k, v in case.items() if k not in ("expert_review",)}))

    # X24 terminology gate: glossary is authoritative (C13); absolute claims forbidden (SC-B)
    for p, s in strings:
        for bad, good, exempt in TERM_DEPRECATED:
            if bad in s and not any(x in s for x in exempt):
                errs.append(f"X24 {p}: deprecated term «{bad}» → use {good}")
        for bad, good in TERM_DISCOURAGED:
            if bad in s:
                warns.append(f"X24 {p}: discouraged term «{bad}» → prefer {good}")
        for bad in ABSOLUTE_AR:
            if bad in s:
                errs.append(f"X24 {p}: absolute claim «{bad}» (SC-B)")

    # X25 Arabic/RTL normalisation: no presentation forms, BOM or bidi controls in any string
    for p, s in strings:
        m = RTL_BAD.findall(s)
        if m:
            errs.append(f"X25 {p}: {len(m)} presentation-form / BOM / bidi-control character(s) "
                        f"{sorted({'U+%04X' % ord(c) for c in m})} — normalise before compile (10/RTL §6)")

    # X26 asset licensing gate: every media item resolves to a register row (or a declared original)
    reg = None
    for e in case["evidence"]:
        for m in e.get("media", []):
            if not m.get("alt_ar", "").strip():
                errs.append(f"X26 {e['id']}: media without alt_ar (every visual/audio clue needs a written twin)")
            uri = m.get("uri", "")
            if uri.startswith("asset:"):
                reg = reg if reg is not None else asset_registers()
                aid = uri.split(":", 1)[1]
                row = reg.get(aid)
                if not row:
                    errs.append(f"X26 {e['id']}: {aid} not found in 15_STORY_MEDIA_AND_ASSETS registers")
                    continue
                lic = row.get("license", "")
                if "BY-SA" in lic or "by-sa" in lic:
                    warns.append(f"X26 {e['id']}: {aid} is {lic[:20]} — reference-only quarantine unless legal approves share-alike (VISUAL_REFERENCE_GUIDE §3)")
                if not row.get("safety_ok", "").startswith("y"):
                    errs.append(f"X26 {e['id']}: {aid} safety_ok={row.get('safety_ok', '')[:20]}")
                if "not auditioned" in row.get("safety_ok", "") or "caution" in row.get("safety_ok", ""):
                    warns.append(f"X26 {e['id']}: {aid} needs human audition (adhan, speech, startle peaks) before release (SOUND_DESIGN_GUIDE §5, §9)")
                lj = LOUDJUMP_RE.search(row.get("tags", ""))
                if lj and case["meta"]["age_band"] == "13-15":
                    v = float(lj.group(1))
                    if v > 18:
                        errs.append(f"X26 {e['id']}: {aid} loudness jump {v} LU > 18 — not allowed for 13-15 (SOUND_DESIGN_GUIDE §3)")
                    elif v > 12:
                        warns.append(f"X26 {e['id']}: {aid} loudness jump {v} LU — compress and audition before 13-15 use")
            elif uri.startswith("original:"):
                warns.append(f"X26 {e['id']}: original asset {uri} — record creator, contract and AI-generation disclosure in the asset log")
            else:
                errs.append(f"X26 {e['id']}: media uri «{uri[:60]}» is neither asset:<IMG|AUD-id> nor original:<slug> (unregistered asset)")

    # X27 bias-lab ethics gate (C14): context-bias concepts require the written ethics gate
    used = set(ko_refs_in(case)) | {e.get("forensic_ko_ref") for e in case["evidence"]}
    if used & BIAS_LAB_KOS:
        warns.append(f"X27 context-bias concept {sorted(used & BIAS_LAB_KOS)} used: attach the 5-question ethics gate, "
                     f"declare lab grade (A transparent / B authorized surprise / C deferred) and age rule "
                     f"(04/BIAS_LAB_ETHICS_FOR_MINORS §1, §5, §7; SCIENTIFIC_REVIEW_CHECKLIST ل)")

    # X28 physiognomy / demeanour cue inside an inference rule (HER-02; SC-06)
    for i in infs.values():
        hits = [w for w in DEMEANOUR_AR if w in i["rule_ar"]]
        if hits and i["relation"] in ("supports", "establishes"):
            errs.append(f"X28 {i['id']}: inference rule rests on demeanour/physiognomy cue {hits} (HER-02; SC-06)")

    # X08 publishing gate: mandatory roles approved on current hash
    h = content_hash(case)
    approved = {r["role"] for r in case.get("expert_review", []) if r["status"] == "approved" and r["content_hash"] == h}
    missing = [r for r in MANDATORY_REVIEW_ROLES if r not in approved]
    gate = {"content_hash": h, "missing_approvals": missing, "publish_allowed": not missing}
    return errs, warns, gate, depth


# ---------------------------------------------------------------- ASP encoding (clingo)
def _guard_facts(g, gid, out):
    k = next(iter(g))
    if k == "always":
        out.append(f"g_always({gid}).")
    elif k == "has_evidence":
        out.append(f"g_has({gid},{g[k]}).")
    elif k == "presented":
        out.append(f"g_has({gid},{g[k]['evidence_id']}).")
    elif k == "fact_unlocked":
        out.append(f"g_fact({gid},{g[k]}).")
    elif k in ("all", "any"):
        out.append(f"g_{k}({gid}).")
        for n, child in enumerate(g[k]):
            cid = f"{gid}_{n}"
            out.append(f"g_child({gid},{cid}).")
            _guard_facts(child, cid, out)
    else:  # not / in_state / trust_at_least: over-approximate as satisfiable (same policy as the prototype)
        out.append(f"g_always({gid}).")


def asp_facts(case):
    out = []
    for e in case["evidence"]:
        out.append(f"evidence({e['id']}).")
    for f in case["premise"]["public_fact_ids"]:
        out.append(f"public({f}).")
    for a in case["mechanics"]["actions"]:
        gid = f"g_{a['id']}"
        out.append(f"action({a['id']},{gid}).")
        _guard_facts(a["precondition"], gid, out)
        for eff in a["effects"]:
            if eff["op"] == "grant_evidence":
                out.append(f"grants({a['id']},{eff['ref_id']}).")
            if eff["op"] == "unlock_fact":
                out.append(f"unlocks({a['id']},{eff['ref_id']}).")
    for i in case["evidence_graph"]["inferences"]:
        for p in i["premises"]:
            if p["ref_type"] in ("evidence", "inference"):
                out.append(f"premise({i['id']},{p['ref_id']}).")
            elif p["ref_type"] == "fact":
                out.append(f"premise_fact({i['id']},{p['ref_id']}).")
        rel = {"supports": "supports", "establishes": "supports", "rules_out": "rules_out",
               "refutes": "rules_out", "contradicts_claim": "contradicts"}[i["relation"]]
        out.append(f"concl({i['id']},{i['conclusion']['ref_id']},{rel}).")
        if i["relation"] == "establishes" and i["conclusion"]["ref_type"] == "fact":
            out.append(f"establishes({i['id']},{i['conclusion']['ref_id']}).")
    for h in case["hypotheses"]:
        out.append(f"hyp({h['id']},{'true' if h['is_true'] else 'false'}).")
    return "\n".join(out)


ASP_CORE = r"""
% ---- reachability over the guard DSL (fixpoint; least model) ----
r_have(E) :- grants(A,E), enabled(A).
r_fact(F) :- public(F).
r_fact(F) :- unlocks(A,F), enabled(A).
enabled(A) :- action(A,G), r_sat(G).
r_sat(G) :- g_always(G).
r_sat(G) :- g_has(G,E), r_have(E).
r_sat(G) :- g_fact(G,F), r_fact(F).
r_sat(G) :- g_any(G), g_child(G,C), r_sat(C).
r_sat(G) :- g_all(G), r_sat(C) : g_child(G,C).
reachable(E) :- r_have(E).
"""

ASP_SUBSET = r"""
% ---- a candidate discovered set must be realisable: each item obtainable with a guard satisfied inside the set ----
{ found(E) : reachable(E) }.
f_fact(F) :- public(F).
f_fact(F) :- unlocks(A,F), f_enabled(A).
f_enabled(A) :- action(A,G), f_sat(G).
f_sat(G) :- g_always(G).
f_sat(G) :- g_has(G,E), found(E).
f_sat(G) :- g_fact(G,F), f_fact(F).
f_sat(G) :- g_any(G), g_child(G,C), f_sat(C).
f_sat(G) :- g_all(G), f_sat(C) : g_child(G,C).
obtainable(E) :- found(E), grants(A,E), f_enabled(A).
:- found(E), not obtainable(E).
% ---- inference closure over the discovered set ----
known(X) :- found(X).
known(F) :- public(F).            % unlocked (revealed) facts open guards only; they are never proof premises
known(F) :- establishes(I,F), derived(I).
derived(I) :- concl(I,_,_), known(P) : premise(I,P); known(F) : premise_fact(I,F).
known(I) :- derived(I).
supported(H) :- derived(I), concl(I,H,supports).
excluded(H)  :- derived(I), concl(I,H,rules_out).
"""

ASP_SOLVED = r"""
solved :- supported(H) : hyp(H,true); excluded(H) : hyp(H,false).
:- not solved.
#heuristic found(E) : reachable(E). [1,false]
#show found/1.
"""

ASP_FULL_PROBE = r"""
found(E) :- reachable(E).
f_fact(F) :- public(F).
known(X) :- found(X).
known(F) :- public(F).
known(F) :- establishes(I,F), derived(I).
derived(I) :- concl(I,_,_), known(P) : premise(I,P); known(F) : premise_fact(I,F).
known(I) :- derived(I).
supported(H) :- derived(I), concl(I,H,supports).
excluded(H)  :- derived(I), concl(I,H,rules_out).
unrefuted_false(H) :- hyp(H,false), not excluded(H).
true_unsupported(H) :- hyp(H,true), not supported(H).
unreachable(E) :- evidence(E), not reachable(E).
#show unrefuted_false/1. #show true_unsupported/1. #show unreachable/1. #show reachable/1.
"""

ASP_FALSE_STOP = r"""
false_stop(H) :- hyp(H,false), supported(H), not excluded(H).
:- not false_stop(_).
#heuristic found(E) : reachable(E). [1,false]
#show found/1. #show false_stop/1.
"""


def run_asp(case, max_models=500):
    try:
        import clingo
    except ImportError:
        return {"available": False, "note": "clingo not installed (pip install --break-system-packages clingo)"}
    facts = asp_facts(case)

    def solve(program, args):
        ctl = clingo.Control(args, logger=lambda code, msg: None)
        ctl.add("base", [], facts + "\n" + program)
        ctl.ground([("base", [])])
        models = []
        with ctl.solve(yield_=True) as h:
            for m in h:
                models.append([str(s) for s in m.symbols(shown=True)])
                if len(models) >= max_models:
                    break
        return models

    full = solve(ASP_CORE + ASP_FULL_PROBE, ["1"])[0]
    pick = lambda pref, syms: sorted(s[len(pref) + 1:-1] for s in syms if s.startswith(pref + "("))
    minimal = solve(ASP_CORE + ASP_SUBSET + ASP_SOLVED, ["0", "--heuristic=Domain", "--enum-mode=domRec"])
    minimal_sets = sorted([sorted(pick("found", m)) for m in minimal], key=lambda s: (len(s), s))
    stops = solve(ASP_CORE + ASP_SUBSET + ASP_FALSE_STOP, ["0", "--heuristic=Domain", "--enum-mode=domRec"])
    stop_sets = sorted([{"false_hypotheses": pick("false_stop", m), "evidence": sorted(pick("found", m))} for m in stops],
                       key=lambda s: (len(s["evidence"]), s["evidence"]))
    # exact maximum number of pairwise-disjoint minimal proof sets (small search)
    sets = [frozenset(s) for s in minimal_sets]
    best = []

    def search(i, chosen):
        nonlocal best
        if len(chosen) > len(best):
            best = list(chosen)
        for j in range(i, len(sets)):
            if all(not (sets[j] & c) for c in chosen):
                search(j + 1, chosen + [sets[j]])
    search(0, [])
    return {
        "available": True, "clingo": clingo.__version__,
        "reachable_evidence": pick("reachable", full),
        "unreachable_evidence": pick("unreachable", full),
        "unrefuted_false_hypotheses": pick("unrefuted_false", full),
        "true_hypotheses_unsupported": pick("true_unsupported", full),
        "subset_minimal_solving_sets": minimal_sets,
        "max_disjoint_proof_paths": len(best),
        "disjoint_paths_example": [sorted(s) for s in best],
        "false_stop_points": stop_sets,
    }


def max_disjoint(sets):
    """Exact maximum number of pairwise-disjoint sets (small exhaustive search)."""
    best = 0

    def search(i, chosen):
        nonlocal best
        best = max(best, len(chosen))
        for j in range(i, len(sets)):
            if all(not (sets[j] & c) for c in chosen):
                search(j + 1, chosen + [sets[j]])
    search(0, [])
    return best


# ---------------------------------------------------------------- driver
def check(case, proto=None):
    proto = proto or _load_proto()
    rep = {"schema_errors": schema_errors(case)}
    if rep["schema_errors"]:
        rep["result"] = "fail"
        return rep
    rep["prototype_integrity_errors"] = proto.integrity(case)
    reach = sorted(proto.reachable_evidence(case))
    rep["prototype_fairness"] = proto.fairness(case)
    pmin = [frozenset(x) for x in rep["prototype_fairness"].get("minimal_evidence_sets", [])]
    rep["prototype_sets_exact_max_disjoint"] = max_disjoint(pmin)
    errs, warns, gate, depth = extended_checks(case, proto, reach)
    rep["extended_errors"], rep["extended_warnings"], rep["publish_gate"] = errs, warns, gate
    rep["inference_depth"] = depth
    rep["asp"] = run_asp(case)
    req = case["fairness_test"]["requirements"]
    blocking = []
    pf = rep["prototype_fairness"]
    if rep["prototype_integrity_errors"]:
        blocking.append("prototype integrity errors")
    if not pf.get("solvable", False):
        blocking.append("prototype: case not solvable from reachable evidence")
    # The prototype's disjoint count is greedy (can under-count) and its subsets ignore guards (can over-count).
    # Blocking rule: guard-aware exact ASP count when clingo is available; otherwise exact count over prototype sets.
    a0 = rep.get("asp", {})
    if not a0.get("available") and rep["prototype_sets_exact_max_disjoint"] < req["min_disjoint_proof_paths"]:
        blocking.append("prototype sets: fewer disjoint proof paths than required")
    if pf.get("disjoint_paths", 0) < req["min_disjoint_proof_paths"]:
        rep.setdefault("advisories", []).append(
            f"prototype greedy disjoint count = {pf.get('disjoint_paths')} (< {req['min_disjoint_proof_paths']}); "
            f"exact over prototype sets = {rep['prototype_sets_exact_max_disjoint']}; see ASP for guard-aware count")
    if errs:
        blocking.append(f"{len(errs)} extended rule violation(s)")
    a = rep["asp"]
    if a.get("available"):
        if a["unrefuted_false_hypotheses"] or a["true_hypotheses_unsupported"]:
            blocking.append("ASP: unique entailment fails")
        if a["max_disjoint_proof_paths"] < req["min_disjoint_proof_paths"]:
            blocking.append("ASP: fewer disjoint proof paths than required")
        if a["unreachable_evidence"]:
            blocking.append("ASP: unreachable evidence")
    if "max_required_actions" in req and a.get("available") and a["subset_minimal_solving_sets"]:
        # approximation: one granting action per evidence item (+1 final presentation); exact action-level search is future work
        est = min(len(s) for s in a["subset_minimal_solving_sets"]) + 1
        rep["min_actions_estimate"] = est
        if est > req["max_required_actions"]:
            blocking.append(f"estimated minimum actions {est} > max_required_actions {req['max_required_actions']}")
    rep["blocking"] = blocking
    rep["result"] = "pass" if not blocking else "fail"
    return rep


def mutation_tests(case, proto):
    """Negative controls on SAMPLE_CASE_001: each mutant must FAIL, showing the checker detects that flaw class."""
    out = []

    def mut(name, fn):
        c = copy.deepcopy(case)
        fn(c)
        r = check(c, proto)
        out.append({"mutant": name, "result": r["result"], "blocking": (r.get("blocking") or r.get("schema_errors"))[:3]})

    def m1(c):  # server-time alerts become dependent on the lab result -> the two proof paths share an item
        for a in c["mechanics"]["actions"]:
            if a["id"] == "a_read_club_chat":
                a["precondition"] = {"has_evidence": "ev_lab_clock_offset"}
    mut("M1 gate the server-time alerts behind the lab result (paths no longer independent)", m1)

    def m2(c):
        c["hypotheses"].append({"id": "h_extra_unrefuted", "statement_ar": "مشتبه إضافي لا يدحضه شيء", "is_true": False,
                                "plausibility_at_start": "medium", "suspect_id": "ch_lama"})
        c["evidence_graph"]["inferences"].append({"id": "i_extra_lure", "premises": [{"ref_type": "evidence", "ref_id": "ev_wadad_testimony"}],
                                                  "conclusion": {"ref_type": "hypothesis", "ref_id": "h_extra_unrefuted"},
                                                  "relation": "supports", "strength": "suggestive", "rule_ar": "اختبار طفرة", "skill_ko_refs": []})
    mut("M2 add a supported-but-never-refuted false suspect", m2)

    def m3(c):
        for cl in c["truth"]["claims"]:
            if cl["id"] == "cl_majed_club_room":
                cl["contradicted_by_evidence_ids"] = []
    mut("M3 make a lie undetectable (no contradicting evidence)", m3)

    def m4(c):
        c["entities"]["characters"] = [dict(ch, role="assistant") if ch["id"] == "ch_majed" else ch for ch in c["entities"]["characters"]]
    mut("M4 make the culprit the assistant (NR-07)", m4)

    def m5(c):
        c["premise"]["public_fact_ids"].append("f_hose_majed")
    mut("M5 leak the solution-critical fact into public facts", m5)

    def m6(c):
        for e in c["evidence"]:
            if e["id"] == "ev_lab_clock_offset":
                e["limits_ar"] = ""
    mut("M6 strip the limits statement from the lab result (SC-03)", m6)

    # ---- wave-2 negative controls (CASE_DESIGN_BIBLE §18) ----
    def m7(c):
        for e in c["evidence"]:
            if e["id"] == "ev_lab_clock_offset":
                e["limits_ar"] += " ونسبة الأرجحية هنا كبيرة."
    mut("M7 use the deprecated term «نسبة الأرجحية» for a likelihood ratio (X24; C13)", m7)

    def m8(c):
        for e in c["evidence"]:
            if e["id"] == "ev_station_log":
                e["content_ar"] = "‫" + e["content_ar"] + "ﺍ"
    mut("M8 inject a bidi control and a presentation-form letter (X25; 10/RTL §6)", m8)

    def m9(c):
        for e in c["evidence"]:
            if e["id"] == "ev_roof_photo":
                e["media"] = [{"uri": "https://example.org/film_still.jpg", "alt_ar": "لقطة"}]
    mut("M9 attach an unregistered media asset (X26 asset licensing gate)", m9)

    def m10(c):
        for i in c["evidence_graph"]["inferences"]:
            if i["relation"] in ("supports", "establishes") and i["conclusion"]["ref_type"] == "hypothesis":
                i["rule_ar"] += " ولغة الجسد تؤكد ذلك."
                break
    mut("M10 let a supporting inference rest on body language (X28; HER-02)", m10)
    return out


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    raw = open(args[0], encoding="utf-8").read()
    case = json.loads(raw)
    proto = _load_proto()
    rep = check(case, proto)
    rf = raw_file_checks(raw)
    if rf:
        rep.setdefault("extended_errors", []).extend(rf)
        rep.setdefault("blocking", []).append("raw file: escaped Arabic (D-T3)")
        rep["result"] = "fail"
    if "--mutation-tests" in sys.argv:
        rep["mutation_tests"] = mutation_tests(case, proto)
    print(json.dumps(rep, ensure_ascii=False, indent=1))
    sys.exit(0 if rep["result"] == "pass" else 1)
