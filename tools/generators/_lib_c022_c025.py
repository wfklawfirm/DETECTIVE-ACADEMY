# Shared builder used ONLY by gen_c022.py .. gen_c025.py (same output layout as gen_c020/gen_c021, less boilerplate per case).
# It holds no case content. Conventions enforced here: mirror actions `ask_<char>_<fact>`, interview actions `always`,
# source classes, standard rubric scaffold, expert_review pending, state machine, fairness requirements.
import json, os

def T(m, p="exact", end=None):
    d = {"start_min": m, "precision": p}
    if end is not None: d["end_min"] = end
    return d

def L(id, purpose, text, facts=None, claims=None):
    d = {"line_id": id, "purpose": purpose, "text_ar": text}
    if facts: d["fact_ids"] = facts
    if claims: d["claim_ids"] = claims
    return d

def P(t, i): return {"ref_type": t, "ref_id": i}
E_ = lambda x: P("evidence", x)
Fa = lambda x: P("fact", x)
K = lambda f, a="witnessed", c="certain": {"fact_id": f, "access": a, "certainty": c}

def levels(d): return [{"score": i, "descriptor_ar": t} for i, t in enumerate(d)]

class Case:
    def __init__(self, cid):
        self.cid = cid
        self.chars, self.facts, self.ev, self.inf, self.A = [], [], [], [], []
        self.claims, self.timeline, self.ck, self.hyps, self.mis, self.hints, self.topics = [], [], [], [], [], [], []
        self.gate = {}  # evidence id -> (action id, label, precondition)

    # ---- entities
    def ch(self, id, name, role, age, persona, motives, lines, forbidden=None):
        self.chars.append({"id": id, "name_ar": name, "role": role, "age_descriptor_ar": age, "persona_ar": persona, "motives_ar": motives,
                           "speech_constraints": {"register": "msa", "max_sentences_per_turn": 3, "forbidden_topics_ar": forbidden or []}, "authored_lines": lines})

    def F(self, id, st, kind, subj, spoiler, time=None, loc=None, ko=None):
        d = {"id": id, "statement_ar": st, "kind": kind, "subject_ids": subj, "spoiler_level": spoiler}
        if time: d["time"] = time
        if loc: d["location_id"] = loc
        if ko: d["science_ko_refs"] = ko
        self.facts.append(d)

    def V(self, id, title, kind, content, gate, supports, rel, limits, label, contradicts=None, red=False, ko=None, loc=None, tele=None):
        """gate: None -> always available; str -> fact id that must be unlocked (by an interview)."""
        act = "a_" + id[3:]
        d = {"id": id, "title_ar": title, "kind": kind, "content_ar": content, "acquired_by_action_ids": [act], "supports_fact_ids": supports, "reliability": rel, "limits_ar": limits}
        if contradicts: d["contradicts_claim_ids"] = contradicts
        if red: d["is_red_herring"] = True
        if ko: d["forensic_ko_ref"] = ko
        if loc: d["location_id"] = loc
        self.ev.append(d)
        pre = {"always": True} if gate is None else {"fact_unlocked": gate}
        self.A.append({"id": act, "type": "examine", "label_ar": label, "precondition": pre, "effects": [{"op": "grant_evidence", "ref_id": id}], "time_cost_units": 1,
                       "target_id": loc or "", "telemetry_code": act.upper()})
        if not loc: self.A[-1].pop("target_id")

    def I(self, id, prem, ct, concl, rel, strength, rule, ks):
        self.inf.append({"id": id, "premises": prem, "conclusion": {"ref_type": ct, "ref_id": concl}, "relation": rel, "strength": strength, "rule_ar": rule, "skill_ko_refs": ks})

    def H(self, id, lv, kind, text, trig, target=None, w=0.0):
        d = {"id": id, "level": lv, "kind": kind, "text_ar": text, "trigger": trig, "assessment_weight": w}
        if target: d["targets_inference_id"] = target
        self.hints.append(d)

    # ---- build
    def build(self, out_dir, *, meta, premise, solution, locations, objects, orgs, hyps, mis, los, reference_answer, ending, ui, sc, topics, extra_actions=None,
              fairness=None, date="2026-10-28"):
        A = self.A
        # interviews (always) for every character
        for c in self.chars:
            A.insert(0, {"id": f"a_int_{c['id']}", "type": "interview", "label_ar": f"ابدأ مقابلة {c['name_ar'].split()[0]}", "precondition": {"always": True},
                         "effects": [{"op": "raise_trust", "ref_id": c["id"], "amount": 1}], "time_cost_units": 1, "target_id": c["id"], "telemetry_code": f"INT_{c['id'].upper()}"})
        for a in (extra_actions or []): A.append(a)
        A.append({"id": "a_hint", "type": "request_hint", "label_ar": "اطلب تلميحاً", "precondition": {"always": True}, "effects": [], "time_cost_units": 0, "telemetry_code": "REQUEST_HINT"})
        A.append({"id": "a_accuse", "type": "final_accusation", "label_ar": "قدّم الرأي المعلّل النهائي", "precondition": {"always": True}, "effects": [{"op": "emit_event", "ref_id": "SUBMIT"}], "time_cost_units": 0, "telemetry_code": "FINAL_ACCUSATION"})
        # mirrors of dialogue unlocks
        pre = {a["target_id"]: a["precondition"] for a in A if a["type"] == "interview"}
        tf = set(f for t in topics for f in t["fact_ids"])
        for c in self.chars:
            ks = next((k for k in self.ck if k["character_id"] == c["id"]), None)
            if not ks: continue
            voiced = set(f for l in c["authored_lines"] if l["purpose"] in ("reveal", "break_down") for f in l.get("fact_ids", []))
            hid = {h["fact_id"]: h for h in ks["hides"]}
            for k in ks["knows"]:
                f = k["fact_id"]
                if f in hid or f not in tf or f not in voiced: continue
                A.append({"id": f"ask_{c['id']}_{f}", "type": "interview", "label_ar": f"[نموذج] {c['id']} يذكر {f}", "precondition": pre[c["id"]], "effects": [{"op": "unlock_fact", "ref_id": f}],
                          "time_cost_units": 0, "target_id": c["id"], "telemetry_code": f"ASK_{c['id'].upper()}_{f.upper()}"})
            for f, h in hid.items():
                if f not in tf or f not in voiced: continue
                A.append({"id": f"ask_{c['id']}_{f}", "type": "interview", "label_ar": f"[نموذج] {c['id']} يكشف {f}", "precondition": {"all": [pre[c["id"]], h["reveal_when"]]},
                          "effects": [{"op": "unlock_fact", "ref_id": f}], "time_cost_units": 0, "target_id": c["id"], "telemetry_code": f"ASK_{c['id'].upper()}_{f.upper()}"})
        rub = {"reference_answer_ar": reference_answer, "criteria": [
            {"id": "c_source", "name_ar": "تصنيف المصادر", "objective_ids": ["lo_source"], "scored_by": "deterministic", "weight": 0.15, "levels": levels(["لم يصنّف", "أخطأ في الأغلب", "نصف صحيح", "معظمه صحيح", "كله صحيح"])},
            {"id": "c_conflict", "name_ar": "ترتيب الأحداث على الخط الزمني", "objective_ids": ["lo_conflict"], "scored_by": "deterministic", "weight": 0.2, "levels": levels(["لم يرتّب شيئاً", "رتّب قليلاً", "رتّب نصفها", "معظمها", "كلها في موضعها"])},
            {"id": "c_links", "name_ar": "ربط الأدلة بالفرضيات", "objective_ids": ["lo_links"], "scored_by": "deterministic", "weight": 0.2, "levels": levels(["لا روابط", "قليلة", "نصفها صحيح", "معظمها", "كلها دقيقة"])},
            {"id": "c_uncertainty", "name_ar": "معايرة الثقة", "objective_ids": ["lo_calib"], "scored_by": "deterministic", "weight": 0.15, "levels": levels(["ثقة مفرطة", "حدود قليلة", "جزئية", "معقولة", "معايَرة كاملة"])},
            {"id": "c_revision", "name_ar": "مراجعة الرأي", "objective_ids": ["lo_revise"], "scored_by": "deterministic", "weight": 0.1, "levels": levels(["بقي على فرضية مرفوضة", "لم يعلن فرضية", "ثبت على فرضية سليمة", "غيّر بدليل", "غيّر بدليل ووثّق"])},
            {"id": "c_elimination", "name_ar": "استبعاد الفرضيات الخاطئة", "objective_ids": ["lo_elim"], "scored_by": "deterministic", "weight": 0.1, "levels": levels(["لم يستبعد", "استبعد خطأً", "فرضية بدليل", "فرضيتين", "كل الخاطئة"])},
            {"id": "c_justification", "name_ar": "جودة الحجة المكتوبة", "objective_ids": ["lo_just"], "scored_by": "human", "weight": 0.1, "levels": levels(["لا حجة", "ادعاء بلا سند", "أدلة دون ربط", "ربط الأدلة بالاستنتاج", "ربط مع الحدود والبدائل"])},
        ]}
        self.hyps, self.mis = hyps, mis
        core = {
            "schema_version": "0.1.0", "case_id": self.cid, "case_version": "0.1.0", "meta": meta, "premise": premise,
            "entities": {"characters": self.chars, "locations": locations, "objects": objects, "organizations": orgs},
            "truth": {"solution": solution, "facts": self.facts, "claims": self.claims},
            "timeline": self.timeline, "evidence": self.ev, "evidence_graph": {"inferences": self.inf},
            "character_knowledge": self.ck, "hypotheses": hyps, "misdirection_plan": mis, "learning_objectives": los,
            "mechanics": {"time_budget_units": 50, "actions": A},
            "state_machine": {"id": self.cid.split("_")[0], "initial": "briefing", "type": "compound", "states": {
                "briefing": {"description_ar": "الإحاطة", "type": "atomic", "on": {"START": {"target": "investigating"}}},
                "investigating": {"description_ar": "التحقيق", "type": "compound", "initial": "gathering",
                                  "states": {"gathering": {"type": "atomic", "on": {"OPEN_DEDUCTION": {"target": "deducing"}}}, "deducing": {"type": "atomic", "on": {"BACK": {"target": "gathering"}}}},
                                  "on": {"SUBMIT": {"target": "review"}}},
                "review": {"description_ar": "مراجعة", "type": "atomic", "on": {"CLOSE": {"target": "resolved"}}},
                "resolved": {"description_ar": "إغلاق", "type": "final"}}},
            "dialogue": {"max_turns_per_interview": 10, "llm_enabled": False, "topics": topics},
            "rubric": rub, "hint_ladder": self.hints,
            "fairness_test": {"requirements": {**{"min_disjoint_proof_paths": 2, "max_inference_depth": 3, "all_red_herrings_refutable": True, "culprit_uniquely_entailed": True, "no_hidden_fact_dependency": True, "max_required_actions": 50}, **(fairness or {})}, "runs": []},
            "ending_explanation": {"steps": [{"order": o, "text_ar": t, "uses_evidence_ids": u, "inference_id": i} for o, t, u, i in ending["steps"]],
                                   "alternative_paths_ar": ending["alt"], "what_evidence_could_not_show_ar": ending["limits"], "science_notes_ar": ending["notes"]},
            "expert_review": [{"role": r, "reviewer": "—", "status": "pending", "content_hash": "unbound", "date": date, "notes_ar": "بانتظار مراجعة بشرية؛ لم يُجرَ أي اعتماد."} for r in
                              ["narrative_editor", "scientific_reviewer", "learning_designer", "age_appropriateness", "cultural_reviewer", "legal_rights", "safety"]],
        }
        ui.setdefault("case_id", self.cid); ui.setdefault("labs", [])
        ui["source_classes"] = [
            {"id": "primary_record", "label_ar": "سجل أصلي", "help_ar": "يُنتجه نظام أو شخص لحظة الحدث دون وسيط، كسجل أو ورقة موقّعة أو نتيجة قياس مباشرة."},
            {"id": "redisplay", "label_ar": "نسخة معروضة", "help_ar": "معلومة أُعيد عرضها أو لُخّصت أو نُقلت عن مصدر آخر، فتتأثر بحدود ناقلها."},
            {"id": "claim", "label_ar": "قول أو تصريح", "help_ar": "إفادة أو شكوى أو ادعاء؛ يُقاس بالسجلات لا بنبرة صاحبه."},
            {"id": "template", "label_ar": "قالب أو نموذج", "help_ar": "نص جاهز لا يصف الحدث الفعلي بذاته."},
            {"id": "public_document", "label_ar": "وثيقة منشورة", "help_ar": "وثيقة معلنة ومعروف ناشرها، كدليل استعمال أو لائحة."}]
        os.makedirs(out_dir, exist_ok=True)
        for suf, obj in [("", core), (".ui", ui), (".scoring", sc)]:
            with open(os.path.join(out_dir, f"{self.cid}{suf}.json"), "w", encoding="utf8") as f:
                json.dump(obj, f, ensure_ascii=False, indent=2)
        print("ok", self.cid, "evidence", len(self.ev), "actions", len(A))
