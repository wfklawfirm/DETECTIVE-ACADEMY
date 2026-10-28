#!/usr/bin/env python3
# Case c028 «الخطاب الذي بالغ في التوكيد» — document provenance. Archetype ARC-29 «الكتاب الذي بالغ في التوكيد» (library), rebuilt as an original
# ATHAR story at a fictional records house («دار السِّجِل»). Teaches: a document is judged by its provenance (is there an entry in the issuer's
# outgoing register? was the seal used? was the signer present?), not by how convincing it looks; tone and layout differences are WEAK alone and
# become useful only when compared with genuine samples AND corroborated by an independent record; a document's file data and a print log are
# records that can be cross-read without attributing anyone's handwriting (no handwriting attribution is offered: KO-FC-04B-004). Detection
# only: nothing explains how to make or hide a forged document. No-culprit-style convention: Firas (a friend who wanted to help) is recorded in
# culprit_ids; Wael, the beneficiary, honestly believed the letter came from the office. All names, institutions, seals and numbers are fictional.
# Time lab omitted (labs: []); timeline requirement used. Calendar (fictional): minute 0 = Monday 9 March 08:00; Wed 11 March 10:00 = 3000.
# Usage: gen_c028.py OUT_DIR
import json, sys, os
OUT = sys.argv[1]

def T(m, p="exact", end=None):
    d = {"start_min": m, "precision": p}
    if end is not None: d["end_min"] = end
    return d
def L(id, purpose, text, facts=None, claims=None):
    d = {"line_id": id, "purpose": purpose, "text_ar": text}
    if facts: d["fact_ids"] = facts
    if claims: d["claim_ids"] = claims
    return d
chars = []
def ch(id, name, role, age, persona, motives, lines, forbidden=None):
    chars.append({"id": id, "name_ar": name, "role": role, "age_descriptor_ar": age, "persona_ar": persona, "motives_ar": motives,
                  "speech_constraints": {"register": "msa", "max_sentences_per_turn": 3, "forbidden_topics_ar": forbidden or []}, "authored_lines": lines})
facts = []
def F(id, st, kind, subj, spoiler, time=None, loc=None, ko=None):
    d = {"id": id, "statement_ar": st, "kind": kind, "subject_ids": subj, "spoiler_level": spoiler}
    if time: d["time"] = time
    if loc: d["location_id"] = loc
    if ko: d["science_ko_refs"] = ko
    facts.append(d)
ev = []
def V(id, title, kind, content, acts, supports, rel, limits, contradicts=None, red=False, ko=None, loc=None):
    d = {"id": id, "title_ar": title, "kind": kind, "content_ar": content, "acquired_by_action_ids": acts, "supports_fact_ids": supports, "reliability": rel, "limits_ar": limits}
    if contradicts: d["contradicts_claim_ids"] = contradicts
    if red: d["is_red_herring"] = True
    if ko: d["forensic_ko_ref"] = ko
    if loc: d["location_id"] = loc
    ev.append(d)
def P(t, i): return {"ref_type": t, "ref_id": i}
inf = []
def I(id, prem, ct, concl, rel, strength, rule, ks):
    inf.append({"id": id, "premises": prem, "conclusion": {"ref_type": ct, "ref_id": concl}, "relation": rel, "strength": strength, "rule_ar": rule, "skill_ko_refs": ks})
E = lambda x: P("evidence", x)
Fa = lambda x: P("fact", x)
def H(id, lv, kind, text, trig, target=None, w=0.0):
    d = {"id": id, "level": lv, "kind": kind, "text_ar": text, "trigger": trig, "assessment_weight": w}
    if target: d["targets_inference_id"] = target
    return d
he = lambda e: {"has_evidence": e}
A = []
def Act(id, typ, label, pre, effects, target=None, tel=None, cost=1):
    d = {"id": id, "type": typ, "label_ar": label, "precondition": pre, "effects": effects, "time_cost_units": cost}
    if target: d["target_id"] = target
    if tel: d["telemetry_code"] = tel
    A.append(d)
G = lambda e: {"op": "grant_evidence", "ref_id": e}
U = lambda f: {"op": "unlock_fact", "ref_id": f}
al = {"always": True}
fu = lambda f: {"fact_unlocked": f}
K = lambda f, a="witnessed", c="certain": {"fact_id": f, "access": a, "certainty": c}
def levels(d): return [{"score": i, "descriptor_ar": t} for i, t in enumerate(d)]
def get(eid, label, gate, loc, tel=None):
    Act("a_get_" + eid[3:], "examine", label, gate, [G(eid)], loc, tel or ("GET_" + eid[3:].upper()))
def interviews(pairs):
    for cid, lab in pairs:
        Act(f"a_int_{cid}", "interview", f"ابدأ مقابلة {lab}", al, [{"op": "raise_trust", "ref_id": cid, "amount": 1}], cid, f"INT_{cid.upper()}")
def tail_actions(compare=None, present=None):
    Act("a_hint", "request_hint", "اطلب تلميحاً", al, [], None, "REQUEST_HINT", 0)
    Act("a_accuse", "final_accusation", "قدّم الرأي المعلّل النهائي", al, [{"op": "emit_event", "ref_id": "SUBMIT"}], None, "FINAL_ACCUSATION", 0)
def mirrors(topics, ck):
    _pre = {a["target_id"]: a["precondition"] for a in A if a["type"] == "interview"}
    _tf = set(f for t in topics for f in t["fact_ids"])
    for _c in chars:
        _ks = next((k for k in ck if k["character_id"] == _c["id"]), None)
        if not _ks: continue
        _voiced = set(f for l in _c["authored_lines"] if l["purpose"] in ("reveal", "break_down") for f in l.get("fact_ids", []))
        _hid = {h["fact_id"]: h for h in _ks["hides"]}
        for k in _ks["knows"]:
            f = k["fact_id"]
            if f in _hid or f not in _tf or f not in _voiced: continue
            Act(f"ask_{_c['id']}_{f}", "interview", f"[نموذج] {_c['id']} يذكر {f}", _pre[_c["id"]], [U(f)], _c["id"], f"ASK_{_c['id'].upper()}_{f.upper()}", 0)
        for f, h in _hid.items():
            if f not in _tf or f not in _voiced: continue
            Act(f"ask_{_c['id']}_{f}", "interview", f"[نموذج] {_c['id']} يكشف {f}", {"all": [_pre[_c["id"]], h["reveal_when"]]}, [U(f)], _c["id"], f"ASK_{_c['id'].upper()}_{f.upper()}", 0)

SRC_CLASSES = [
    {"id": "primary_record", "label_ar": "سجل أصلي", "help_ar": "يُنتجه نظام أو شخص لحظة الحدث دون وسيط، كسجل بوابة أو ورقة توقيع أو بطاقة."},
    {"id": "redisplay", "label_ar": "نسخة معروضة", "help_ar": "معلومة أُعيد عرضها أو نُقلت عن جهاز أو شخص آخر، كلقطة شاشة أو ملخص."},
    {"id": "claim", "label_ar": "قول أو تصريح", "help_ar": "إفادة أو شكوى أو رسالة؛ تُقاس بالسجلات لا بنبرة صاحبها."},
    {"id": "template", "label_ar": "قالب أو نموذج", "help_ar": "نص جاهز لا يصف الحدث الفعلي بذاته."},
    {"id": "public_document", "label_ar": "وثيقة منشورة", "help_ar": "وثيقة معلنة ومعروف ناشرها."}]
STD_CRIT = [
    ("c_source", "تصنيف المصادر", ["lo_claim"], 0.15, ["لم يصنّف", "أخطأ في الأغلب", "نصف صحيح", "معظمه صحيح", "كله صحيح"], "source_typing"),
    ("c_conflict", "ترتيب الأحداث على الخط الزمني", ["lo_timeline"], 0.2, ["لم يرتّب شيئاً", "رتّب قليلاً", "رتّب نصفها", "معظمها", "كلها في موضعها"], "conflict_resolution"),
    ("c_links", "ربط الأدلة بالفرضيات", ["lo_diag", "lo_indep"], 0.2, ["لا روابط", "قليلة", "نصفها صحيح", "معظمها", "كلها دقيقة"], "hypothesis_links"),
    ("c_uncertainty", "معايرة الثقة", ["lo_calib"], 0.15, ["ثقة مفرطة", "حدود قليلة", "جزئية", "معقولة", "معايَرة كاملة"], "uncertainty"),
    ("c_revision", "مراجعة الرأي", ["lo_revise"], 0.1, ["بقي على فرضية مرفوضة", "لم يعلن فرضية", "ثبت على فرضية سليمة", "غيّر بدليل", "غيّر بدليل ووثّق"], "revision"),
    ("c_elimination", "استبعاد الفرضيات الخاطئة", ["lo_hyp"], 0.1, ["لم يستبعد", "استبعد خطأً", "فرضية بدليل", "فرضيتين", "كل الخاطئة"], "elimination"),
    ("c_justification", "جودة الحجة المكتوبة", ["lo_main"], 0.1, ["لا حجة", "ادعاء بلا سند", "أدلة دون ربط", "ربط الأدلة بالاستنتاج", "ربط مع الطرق البريئة والحدود"], "justification_human"),
]
def std_los(main_stmt, main_ko, main_beh, calib_stmt="يصوغ نسبة الترجيح بحدودها."):
    return [
      {"id": "lo_claim", "statement_ar": "يصنّف الأدلة بحسب نوع مصدرها ويعامل الأقوال ادعاءات تحتاج تأييداً.", "skill_ko_ref": "KO-RS-05-001", "observable_behaviors_ar": ["يصنّف الإفادات أقوالاً", "يميز السجل الأصلي من النسخة"], "evidence_sources": ["evidence_board"]},
      {"id": "lo_timeline", "statement_ar": "يرتّب الأحداث على خط زمني واحد ليكشف ما يتعارض.", "skill_ko_ref": "KO-RS-05-005", "observable_behaviors_ar": ["يضع الأدلة في أزمنتها"], "evidence_sources": ["timeline_task", "action_log"]},
      {"id": "lo_indep", "statement_ar": "يتحقق من استقلال الأدلة ويقدّم مسارين لا يشتركان في مصدر.", "skill_ko_ref": "KO-RS-05-004", "observable_behaviors_ar": ["يميز بين مصادر لا تشترك في أصل"], "evidence_sources": ["evidence_board", "final_justification"]},
      {"id": "lo_main", "statement_ar": main_stmt, "skill_ko_ref": main_ko, "observable_behaviors_ar": main_beh, "evidence_sources": ["evidence_board", "final_justification"]},
      {"id": "lo_hyp", "statement_ar": "يوازن بين فرضيتين على الأقل ويستبعد ما تنقضه الأدلة.", "skill_ko_ref": "KO-RS-05-002", "observable_behaviors_ar": ["يضيف فرضيات", "يستبعد بدليل"], "evidence_sources": ["hypothesis_ledger"]},
      {"id": "lo_diag", "statement_ar": "يقدّر ما يثبته كل دليل وما لا يثبته ويربطه بالفرضية باتجاه صحيح.", "skill_ko_ref": "KO-RS-06-001", "observable_behaviors_ar": ["يربط الدليل بالفرضية"], "evidence_sources": ["evidence_board", "final_justification"]},
      {"id": "lo_calib", "statement_ar": calib_stmt, "skill_ko_ref": "KO-RS-06-021", "observable_behaviors_ar": ["يختار ثقة معقولة", "يذكر حدوداً"], "evidence_sources": ["final_justification"]},
      {"id": "lo_revise", "statement_ar": "يراجع رأيه الأول حين يظهر ما يخالفه.", "skill_ko_ref": "KO-RS-06-009", "observable_behaviors_ar": ["يغيّر فرضيته الرائدة بدليل"], "evidence_sources": ["hypothesis_ledger"]}]
def rubric(ref):
    return {"reference_answer_ar": ref, "criteria": [
        {"id": i, "name_ar": n, "objective_ids": o, "scored_by": ("human" if i == "c_justification" else "deterministic"), "weight": w, "levels": levels(lv)} for i, n, o, w, lv, _ in STD_CRIT]}
def cover_los(r, los):
    cov = set(o for c in r["criteria"] for o in c["objective_ids"])
    for lo in los:
        if lo["id"] not in cov: next(c for c in r["criteria"] if c["id"] == "c_links")["objective_ids"].append(lo["id"])
    return r
def assemble(CID, meta, premise, ents, culprit, summary, key_facts, claims, timeline, ck, hyps, mis, los, ref, hints, topics, steps, alt, notlimits, notes, ui, sc):
    mirrors(topics, ck)
    for t in timeline:
        if t.get("location_id") is None: t.pop("location_id", None)
    core = {
      "schema_version": "0.1.0", "case_id": CID, "case_version": "0.1.0",
      "meta": dict(meta, locale="ar", dialogue_register="msa", authors=["فريق أثر التحريري (مسودة بمساعدة الذكاء الاصطناعي، لم تُراجَع بشرياً بعد)"]),
      "premise": premise, "entities": ents,
      "truth": {"solution": {"culprit_ids": culprit, "summary_ar": summary, "key_fact_ids": key_facts}, "facts": facts, "claims": claims},
      "timeline": timeline, "evidence": ev, "evidence_graph": {"inferences": inf},
      "character_knowledge": ck, "hypotheses": hyps, "misdirection_plan": mis, "learning_objectives": los,
      "mechanics": {"time_budget_units": 50, "actions": A},
      "state_machine": {"id": CID[:4], "initial": "briefing", "type": "compound", "states": {
        "briefing": {"description_ar": "الإحاطة", "type": "atomic", "on": {"START": {"target": "investigating"}}},
        "investigating": {"description_ar": "التحقيق", "type": "compound", "initial": "gathering",
          "states": {"gathering": {"type": "atomic", "on": {"OPEN_DEDUCTION": {"target": "deducing"}}}, "deducing": {"type": "atomic", "on": {"BACK": {"target": "gathering"}}}},
          "on": {"SUBMIT": {"target": "review"}}},
        "review": {"description_ar": "مراجعة", "type": "atomic", "on": {"CLOSE": {"target": "resolved"}}},
        "resolved": {"description_ar": "إغلاق", "type": "final"}}},
      "dialogue": {"max_turns_per_interview": 10, "llm_enabled": False, "topics": topics},
      "rubric": cover_los(rubric(ref), los), "hint_ladder": hints,
      "fairness_test": {"requirements": {"min_disjoint_proof_paths": 2, "max_inference_depth": 3, "all_red_herrings_refutable": True, "culprit_uniquely_entailed": True, "no_hidden_fact_dependency": True, "max_required_actions": 50}, "runs": []},
      "ending_explanation": {"steps": [{"order": o, "text_ar": t, "uses_evidence_ids": u, "inference_id": i} for o, t, u, i in steps],
        "alternative_paths_ar": alt, "what_evidence_could_not_show_ar": notlimits, "science_notes_ar": notes},
      "expert_review": [{"role": r, "reviewer": "—", "status": "pending", "content_hash": "unbound", "date": "2026-10-28", "notes_ar": "بانتظار مراجعة بشرية؛ لم يُجرَ أي اعتماد."} for r in
                        ["narrative_editor", "scientific_reviewer", "learning_designer", "age_appropriateness", "cultural_reviewer", "legal_rights", "safety"]],
    }
    ui = dict(ui, case_id=CID, labs=[], source_classes=SRC_CLASSES)
    sc = dict(sc, case_id=CID, lab_requirement=None, criteria_map={i: m for i, _, _, _, _, m in STD_CRIT}, caps={"no_citations_max": 45, "no_conflict_resolution_max": 65})
    os.makedirs(OUT, exist_ok=True)
    for suf, obj in [("", core), (".ui", ui), (".scoring", sc)]:
        with open(os.path.join(OUT, f"{CID}{suf}.json"), "w", encoding="utf8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)
    print("ok", CID)

CID = "c028_emphatic_letter"
ch("wael", "وائل الحداد", "suspect", "طالب في الصف الثاني عشر يتقدم إلى ورشة الترميم",
   "متحمس ومجتهد وقليل الشك، تسلّم الخطاب من صديقه فصدّقه. يتألم من فكرة أن يكون مصدره غير ما ظن، ويتعاون في تقديم هاتفه وملفاته.",
   ["أن يُقبل في الورشة بجهده", "ألا يُتّهم بما لم يفعله"],
   [L("wl_greet", "greeting", "أنا قدّمت الخطاب كما استلمته. لم أكتب فيه حرفاً."),
    L("wl_office", "reveal", "أعطاني فراس الخطاب مساء الاثنين وقال إنه من مكتب المديرة، فطبعته نسخة أخرى وقدّمته للمنسقة يوم الأربعاء.", ["f_wael_says_office"]),
    L("wl_chat", "reveal", "عندي رسالة فراس على هاتفي، وسأريك إياها وأسمح لك بنسخها.", ["f_chat_exists"]),
    L("wl_file", "reveal", "وصلني الخطاب ملفاً إلكترونياً، وما زال عندي كما استلمته.", ["f_file_exists"]),
    L("wl_unknown", "deflect_unknown", "لا أعرف أكثر من هذا."),
    L("wl_off", "deflect_offtopic", "اسألني عن الورشة والخطاب."),
    L("wl_bye", "farewell", "أريد أن أعرف الحقيقة قبل أي شيء.")])
ch("nabil", "نبيل الحلبي", "suspect", "كاتب مكتب المديرة وحافظ سجل الصادر",
   "دقيق ومنظم ويحمل مفتاح خزنة الختم، ويتحرج إذا لمّح أحد إلى أنه فرّط. يجيب بما في السجل ويرفض التخمين.",
   ["أن يبقى السجل سليماً", "ألا يُنسب إليه خطاب لم يكتبه"],
   [L("nb_greet", "greeting", "سجل الصادر عندي، وكل ما يخرج يُرقَّم فيه."),
    L("nb_says", "reveal", "لم أكتب هذا الخطاب ولم أره قبل أن يُعرض علينا.", ["f_nabil_says"]),
    L("nb_register", "reveal", "كل كتاب يصدر من المكتب يُقيَّد في سجل الصادر برقمه وتاريخه وجهته قبل أن يخرج.", ["f_register_exists"]),
    L("nb_seal", "reveal", "الختم في الخزنة، وكل استعمال له يُكتب في سجل الختم مع رقم الكتاب والتوقيع.", ["f_seal_log_exists"]),
    L("nb_keys", "reveal", "مفتاح الخزنة معي ومع المديرة فقط.", ["f_safe_keys"]),
    L("nb_unknown", "deflect_unknown", "هذا خارج السجل."),
    L("nb_off", "deflect_offtopic", "اسألني عن السجل والختم."),
    L("nb_bye", "farewell", "السجل يتكلم عني.")])
ch("firas", "فراس الرفاعي", "suspect", "طالب في الصف الثاني عشر، صديق وائل، عضو نادي الطباعة",
   "ودود وسريع الحماس، يعمل بقلب طيب ويؤجل التفكير في العواقب. يسكت إذا خاف، ويقول الحقيقة حين يرى أن السجلات قالتها.",
   ["أن يساعد صديقه", "ألا يخسر ثقة النادي"],
   [L("fr_greet", "greeting", "أنا أحب أن أساعد أصدقائي."),
    L("fr_deny", "reveal", "أخذت الخطاب من مكتب المديرة وسلّمته لوائل كما هو.", None, ["cl_firas_office"]),
    L("fr_refuse", "refuse_secret", "أفضّل ألا أخوض في هذا الآن."),
    L("fr_made", "reveal", "كتبت الخطاب بنفسي في غرفة النادي وطبعته في مكتبة الدار، لأن وائل يستحق المقعد وأردت أن أساعده؛ ثم قلت له إنه من المكتب. لم أقصد أذى أحد، ولم أفكر أن اسم المديرة سيُسأل عنه.", ["f_firas_made"]),
    L("fr_unknown", "deflect_unknown", "لا أذكر."),
    L("fr_off", "deflect_offtopic", "اسألني عن النادي."),
    L("fr_bye", "farewell", "كان عليّ أن أسأل قبل أن أفعل.")])
ch("hana", "هناء الصباغ", "authority", "مديرة دار السِّجِل",
   "رصينة ومختصرة، تعتمد على أوراقها ولا تحكم على طالب. لا تذكر ما لم تكتبه.",
   ["أن تبقى كتب الدار موثوقة", "أن يُعامَل الطلاب بإنصاف"],
   [L("hn_greet", "greeting", "أجيب عمّا يخصّ كتبي وأوراقي."),
    L("hn_leave", "reveal", "كنت في مؤتمر خارج المدينة من مساء الأحد إلى ظهر الأربعاء، وتركت إشعاراً بأن لا يصدر شيء باسمي في غيابي.", ["f_leave_notice_exists"]),
    L("hn_samples", "reveal", "عند المكتب نسخ من آخر كتبي الصادرة قبل أسابيع، وأسلوبي فيها معروف: ترشيح هادئ ينتهي بعبارة تقدير ثابتة.", ["f_samples_exist"]),
    L("hn_unknown", "deflect_unknown", "لا أعرف."),
    L("hn_off", "deflect_offtopic", "اسألني عن كتبي."),
    L("hn_bye", "farewell", "ما لم يُقيَّد عندنا لم يصدر منا.")])
ch("sarah", "سارة العلي", "witness", "منسقة ورشة الترميم",
   "منصفة وحذرة، لاحظت أن نبرة الخطاب تختلف عن المعتاد لكنها تعرف أن النبرة وحدها لا تكفي. تريد قراراً مبنياً على سجل.",
   ["أن يُقبل المستحق", "ألا تظلم أحداً"],
   [L("sr_greet", "greeting", "أريد قراراً أستطيع الدفاع عنه."),
    L("sr_note", "reveal", "استلمت الخطاب من وائل الأربعاء، ولاحظت أن لغته أشد حماسة من كل ما أعرفه عن كتب المديرة، لكنني لا أعدّ ذلك دليلاً.", ["f_letter_doubted"]),
    L("sr_unknown", "deflect_unknown", "لا أعرف أكثر."),
    L("sr_off", "deflect_offtopic", "اسألني عن الورشة."),
    L("sr_bye", "farewell", "سأنتظر السجلات.")])
ch("labiba", "لبنى الدويك", "witness", "أمينة مكتبة الدار ومسؤولة الطباعة",
   "منظمة وتحتفظ بسجل الطباعة، لا تعرف أصحاب المستندات ولا تقرؤها.",
   ["أن يبقى سجل الطباعة سليماً"],
   [L("lb_greet", "greeting", "أقرأ من سجل الطباعة."),
    L("lb_log", "reveal", "طابعة المكتبة تسجّل حساب كل من يطبع واسم الملف وعدد الصفحات والوقت، ولا تسجّل نص المستند.", ["f_print_log_exists"]),
    L("lb_unknown", "deflect_unknown", "هذا ليس في السجل."),
    L("lb_off", "deflect_offtopic", "اسألني عن الطباعة."),
    L("lb_bye", "farewell", "السجل كما هو.")])
ch("adel", "عادل السقا", "witness", "مشرف نادي الطباعة",
   "عملي وهادئ، يقرأ من قارئ بطاقات الغرفة ولا يخمّن.",
   ["أن تبقى غرفة النادي منظمة"],
   [L("ad_greet", "greeting", "أشرف على غرفة النادي."),
    L("ad_log", "reveal", "باب غرفة النادي يسجّل بطاقة كل داخل وخارج بوقتها.", ["f_club_log_exists"]),
    L("ad_unknown", "deflect_unknown", "لا أعرف."),
    L("ad_off", "deflect_offtopic", "اسألني عن الغرفة."),
    L("ad_bye", "farewell", "القارئ لا ينسى.")])

locations = [{"id": "loc_office", "name_ar": "مكتب المديرة", "description_ar": "مكتب فيه سجل الصادر وخزنة الختم."},
             {"id": "loc_library", "name_ar": "مكتبة الدار", "description_ar": "فيها طابعة بسجل حسابات."},
             {"id": "loc_club", "name_ar": "غرفة نادي الطباعة", "description_ar": "غرفة بباب بقارئ بطاقات."},
             {"id": "loc_workshop", "name_ar": "ورشة الترميم", "description_ar": "ورشة تقبل طلاباً بترشيح وشروط."}]
objects = [{"id": "obj_letter", "name_ar": "خطاب الترشيح", "description_ar": "صفحة بتاريخ 10 آذار ورقم صادر 41/2026 باسم المديرة."}]
orgs = [{"id": "org_dar", "name_ar": "دار السِّجِل", "description_ar": "دار خيالية للسجلات والمخطوطات في مدينة «القنطرة»."}]

F("f_letter_received", "قدّم الطالب وائل إلى منسقة ورشة الترميم خطاب ترشيح بتاريخ 10 آذار ورقم 41/2026 باسم مديرة الدار.", "event", ["wael", "obj_letter"], 0, T(3000))
F("f_letter_doubted", "لاحظت المنسقة أن أسلوب الخطاب أشد حماسة من كتب المديرة المعتادة.", "attribute", ["sarah", "obj_letter"], 0)
F("f_wael_says_office", "يقول وائل إن صديقه فراس سلّمه الخطاب على أنه من مكتب المديرة.", "attribute", ["wael", "firas"], 1)
F("f_chat_exists", "عند وائل محادثة مع فراس على هاتفه تتضمن إرسال الملف.", "state", ["wael"], 1)
F("f_file_exists", "عند وائل الملف الإلكتروني كما وصله، وفيه بيانات الملف.", "state", ["wael", "obj_letter"], 1)
F("f_nabil_says", "ينفي نبيل أنه كتب الخطاب أو رآه قبل عرضه.", "attribute", ["nabil"], 1)
F("f_register_exists", "يُقيَّد كل كتاب صادر من الدار في سجل الصادر برقمه وتاريخه وجهته قبل خروجه.", "state", ["nabil"], 1, None, "loc_office")
F("f_seal_log_exists", "يُكتب كل استعمال لختم الدار في سجل الختم مع رقم الكتاب والتوقيع.", "state", ["nabil"], 1, None, "loc_office")
F("f_safe_keys", "مفتاح خزنة الختم مع كاتب المكتب ومع المديرة فقط.", "state", ["nabil", "hana"], 1, None, "loc_office")
F("f_leave_notice_exists", "علّقت المديرة إشعار غياب بأن لا يصدر شيء باسمها أثناء مؤتمرها.", "event", ["hana"], 1, T(-840, "exact", 3300))
F("f_samples_exist", "يحتفظ المكتب بنسخ من آخر كتب المديرة الصادرة، ولها قالب ثابت في الأسلوب والتخطيط.", "state", ["hana"], 1, None, "loc_office")
F("f_print_log_exists", "تسجّل طابعة المكتبة حساب الطابع واسم الملف وعدد الصفحات والوقت.", "state", ["labiba"], 1, None, "loc_library")
F("f_club_log_exists", "يسجّل باب غرفة نادي الطباعة بطاقة كل داخل وخارج بوقتها.", "state", ["adel"], 1, None, "loc_club")
F("f_not_issued", "لم يمرّ الخطاب بأي قناة رسمية في الدار، فهو ليس من إنتاج المكتب ولا بتفويض المديرة.", "relation", ["obj_letter", "hana", "nabil"], 3, T(-840, "exact", 3300), "loc_office", ["KO-RS-06-002", "KO-RS-05-004"])
F("f_firas_made", "أُعدّ الخطاب وطُبع من حساب فراس في غرفة النادي والمكتبة بينما كان وائل غائباً، ثم سلّمه فراس لوائل بوصفه خطاب المكتب.", "relation", ["firas", "obj_letter", "wael"], 3, T(450, "exact", 510), "loc_club", ["KO-RS-06-002", "KO-RS-05-004"])

claims = [
    {"id": "cl_firas_office", "statement_ar": "أخذت الخطاب من مكتب المديرة كما هو.", "kind": "lie", "held_by": ["firas"], "true_fact_id": "f_firas_made",
     "contradicted_by_evidence_ids": ["ev_print_log", "ev_file_properties", "ev_chat_log", "ev_club_room_log"]},
    {"id": "cl_letter_genuine", "statement_ar": "الخطاب سليم الشكل ويحمل رقماً وختماً، فهو من الدار.", "kind": "honest_mistake", "held_by": ["wael"], "true_fact_id": "f_not_issued",
     "contradicted_by_evidence_ids": ["ev_outgoing_register", "ev_seal_log", "ev_leave_notice"]},
]
timeline = [
    {"id": "te_leave", "description_ar": "المديرة في مؤتمر خارج المدينة.", "time": T(-840, "exact", 3300), "actor_ids": ["hana"], "fact_ids": ["f_leave_notice_exists"], "motivated_by_ar": "حضور مؤتمر السجلات"},
    {"id": "te_register", "description_ar": "نبيل يقيّد الكتاب 42 في سجل الصادر ويسجّل استعمال الختم.", "time": T(130), "location_id": "loc_office", "actor_ids": ["nabil"], "fact_ids": ["f_register_exists"], "motivated_by_ar": "إصدار تعميم الأسبوع"},
    {"id": "te_club", "description_ar": "فراس في غرفة النادي.", "time": T(450, "exact", 495), "location_id": "loc_club", "actor_ids": ["firas"], "fact_ids": ["f_firas_made"], "motivated_by_ar": "أراد مساعدة صديقه"},
    {"id": "te_print", "description_ar": "طباعة الخطاب من حساب فراس في المكتبة.", "time": T(482), "location_id": "loc_library", "actor_ids": [], "fact_ids": ["f_print_log_exists"]},
    {"id": "te_chat", "description_ar": "فراس يرسل الملف لوائل.", "time": T(510), "actor_ids": ["firas", "wael"], "fact_ids": ["f_wael_says_office"], "motivated_by_ar": "أراد أن يقدّم وائل الخطاب"},
    {"id": "te_wael_club", "description_ar": "وائل يدخل غرفة النادي بعد خروج فراس.", "time": T(550), "location_id": "loc_club", "actor_ids": ["wael"], "fact_ids": ["f_club_log_exists"], "motivated_by_ar": "جاء ليأخذ نسخة مطبوعة"},
    {"id": "te_submit", "description_ar": "وائل يقدّم الخطاب للمنسقة.", "time": T(3000), "location_id": "loc_workshop", "actor_ids": ["wael", "sarah"], "fact_ids": ["f_letter_received"], "motivated_by_ar": "موعد تقديم طلبات الورشة"},
]

V("ev_letter", "خطاب الترشيح المقدَّم", "documentary",
  "دار السِّجِل — مكتب المديرة\nالرقم: 41/2026 (أعلى الصفحة، يمين) · التاريخ: 10 آذار\nإلى: منسقة ورشة الترميم\n«أوصي بأشد العبارات وبأقصى ما تسمح به اللغة من حرارة بقبول الطالب وائل الحداد فوراً دون أي اختبار أو انتظار، وأتحمل المسؤولية الكاملة عن هذا الطلب.»\nأعلى الصفحة مسافة بيضاء كبيرة · الختم مطبوع فوق التوقيع · الاسم: د. هناء الصباغ",
  ["a_read_letter"], ["f_letter_received", "f_letter_doubted"], "weak",
  "وثيقة موضوع التحقيق نفسها؛ تبدو سليمة الشكل، وغرابة أسلوبها لا تقول من أنتجها ولا أنها غير سليمة قبل مقارنتها بسجلات.", red=True, loc="loc_workshop")
V("ev_file_properties", "بيانات الملف الإلكتروني للخطاب", "digital",
  "نسخة الملف من هاتف وائل — بيانات الملف\nالاسم: letter_wael.docx\nالمُنشئ: f_rifai · الحفظ الأخير: الاثنين 15:58 (وقت الجهاز المتصل بالشبكة)\nالقالب المستعمل: club_letterhead.dotx",
  ["a_get_file_properties"], ["f_file_exists", "f_firas_made"], "moderate",
  "بيانات الملف تُعدَّل ولا تثبت وحدها هوية الفاعل؛ تقوى حين يوافقها سجل طباعة لا يعتمد عليها.", loc="loc_club")
V("ev_chat_log", "محادثة فراس ووائل", "digital",
  "محادثة خاصة (نسخة من هاتف وائل بموافقته)\nالاثنين 16:30 — فراس: «جهّزت لك خطاب المديرة. اطبعه وقدّمه للمنسقة، لا تقل إنني أنا الذي أحضرته.»\n(مرفق ملف: letter_wael.docx)\nالاثنين 16:41 — وائل: «شكراً! سأطبعه الليلة.»",
  ["a_get_chat_log"], ["f_chat_exists", "f_wael_says_office", "f_firas_made"], "strong",
  "سجل مراسلة بين صديقين؛ يبيّن من أرسل الملف وبأي صيغة، ولا يبيّن من كتبه ولا أين.", loc="loc_workshop")
V("ev_club_room_log", "سجل باب غرفة نادي الطباعة", "digital",
  "غرفة نادي الطباعة — قارئ البطاقات — الاثنين\n15:30 دخول: ف. الرفاعي\n16:15 خروج: ف. الرفاعي\n17:10 دخول: و. الحداد\n17:25 خروج: و. الحداد\nلا بطاقات أخرى بين 15:30 و17:10.",
  ["a_get_club_room_log"], ["f_club_log_exists", "f_firas_made"], "strong",
  "يسجّل مرور البطاقة لا الشخص؛ وقوته أنه يتفق مع سجل الطباعة ومع وقت الرسالة.", loc="loc_club")
V("ev_print_log", "سجل طباعة المكتبة", "digital",
  "مكتبة الدار — سجل الطباعة — الاثنين\n16:02 الحساب: f_rifai · الملف: letter_wael.docx · صفحة واحدة · ملوّنة\nلا طباعة أخرى لهذا الملف في اليوم.",
  ["a_get_print_log"], ["f_print_log_exists", "f_firas_made"], "strong",
  "يسجّل الحساب والملف والوقت دون نص المستند؛ والحساب قد يُستعمل من غير صاحبه، فيحتاج إلى سجل ثانٍ يوافقه.", loc="loc_library")
V("ev_outgoing_register", "صفحة سجل الصادر", "documentary",
  "دار السِّجِل — سجل الصادر 2026 (صفحة آذار)\n40/2026 — 4 آذار — إلى الأقسام — تعميم الدوام\n41/2026 — 5 آذار — إلى المخزن — طلب أحبار\n42/2026 — 9 آذار — إلى الأقسام — تعميم الأسبوع\n43/2026 — 11 آذار — إلى مدرسة القنطرة — تأكيد زيارة\nالأرقام متسلسلة بتوقيع الكاتب، ولا قيد في آذار بخطاب إلى ورشة الترميم.",
  ["a_get_outgoing_register"], ["f_register_exists", "f_not_issued"], "strong",
  "سجل يحفظه كاتب واحد؛ يثبت ما قُيّد لا ما لم يُكتب خارجه، فيقوى حين يوافقه سجل الختم.", ko="KO-RS-06-002", loc="loc_office")
V("ev_seal_log", "سجل استعمال الختم", "documentary",
  "دار السِّجِل — سجل الختم — آذار\n9 آذار — الكتاب 42/2026 — توقيع: ن. الحلبي\n11 آذار — الكتاب 43/2026 — توقيع: ن. الحلبي\nلا استعمال للختم في 10 آذار.",
  ["a_get_seal_log"], ["f_seal_log_exists", "f_not_issued"], "strong",
  "سجل منفصل عن سجل الصادر، يكتبه الكاتب نفسه؛ ولا يمنع ختماً مصنوعاً خارج الخزنة، لكنه يبيّن أن الختم الحقيقي لم يُستعمل.", loc="loc_office")
V("ev_safe_keys", "قائمة حملة مفتاح الخزنة", "documentary",
  "مكتب المديرة — قائمة المفاتيح\nخزنة الختم: ن. الحلبي (الكاتب) · د. الصباغ (المديرة)",
  ["a_get_safe_keys"], ["f_safe_keys"], "moderate",
  "تبيّن من يستطيع فتح الخزنة لا من فتحها؛ والإمكان ليس فعلاً، ولا قيد في سجل الختم يوافقه.", red=True, loc="loc_office")
V("ev_leave_notice", "إشعار غياب المديرة", "documentary",
  "إشعار معلّق في لوحة الدار — بخط المديرة وتوقيعها\nأغيب في مؤتمر خارج المدينة من الأحد 18:00 إلى الأربعاء 14:00. لا يصدر باسمي أي كتاب أو ترشيح في غيابي؛ والمستعجل يحال إلى نائب المدير.\nشهادة الحضور من المؤتمر مرفقة.",
  ["a_get_leave_notice"], ["f_leave_notice_exists", "f_not_issued"], "strong",
  "يثبت غيابها وتعليمتها، ولا يستبعد وحده أن تكون فوّضت أحداً شفوياً؛ ويقوى بالمقارنة مع نماذج كتبها.", loc="loc_office")
V("ev_template_samples", "جدول مقارنة الخطاب بكتب المديرة الصادرة", "documentary",
  "مكتب المديرة — ثلاثة كتب ترشيح صادرة (شباط) مقابل الخطاب المتنازع عليه\nالعبارة الافتتاحية: «نرشّح للنظر في قبوله وفق الشروط المعتمدة» (الكتب الثلاثة) · «أوصي بأشد العبارات... فوراً دون أي اختبار» (الخطاب)\nعبارة الختام: «مع وافر التقدير» (الثلاثة) · غائبة (الخطاب)\nموضع رقم الصادر: أعلى اليسار (الثلاثة) · أعلى اليمين (الخطاب)\nموضع الختم: مربع أسفل اليسار بعيداً عن التوقيع (الثلاثة) · فوق التوقيع (الخطاب)\nالمسافة البيضاء أعلى الصفحة: 3 سم (الثلاثة) · 6 سم (الخطاب)",
  ["a_get_template_samples"], ["f_samples_exist", "f_not_issued"], "moderate",
  "مقارنة بنماذج يحتفظ بها المكتب نفسه، ولا تنسب الخطاب لخط أحد؛ وفروق الأسلوب والتخطيط وحدها قرائن ضعيفة، تقوى حين يوافقها غياب المديرة.", ko="KO-FC-04B-004", loc="loc_office")
V("ev_wael_stmt", "إفادة وائل (ملخص)", "testimonial",
  "ملخص إفادة وائل الحداد:\n«استلمت الملف من فراس وقال لي إنه صادر عن المكتب، وطبعته مرة ثانية وقدمته. لم أكتب فيه شيئاً ولم أسأل المكتب.»",
  ["a_note_wael"], ["f_wael_says_office"], "weak",
  "إفادة المستفيد من الخطاب؛ تُقاس بالمراسلة والسجلات لا بنبرتها.", loc="loc_workshop")
V("ev_nabil_stmt", "إفادة نبيل (ملخص)", "testimonial",
  "ملخص إفادة نبيل الحلبي:\n«لم أكتب هذا الخطاب ولم أره قبل أن يُعرض علينا. الختم لم يُفتح له.»",
  ["a_note_nabil"], ["f_nabil_says"], "weak",
  "إفادة صاحب الشأن عن نفسه؛ يؤيدها سجل الختم ولا تغني عنه.", loc="loc_office")
V("ev_firas_stmt", "إفادة فراس بعد المواجهة (ملخص)", "testimonial",
  "ملخص إفادة فراس الرفاعي:\n«كتبت الخطاب وطبعته بنفسي، وأخبرت وائل أنه من المكتب. أخطأت ولم أقصد إيذاء أحد.»",
  ["a_note_firas"], ["f_firas_made"], "moderate",
  "اعتراف بعد عرض سجل عليه؛ يؤيد سجلات سبقته ولا يغني عنها.", loc="loc_club")

I("i_issued_a", [E("ev_outgoing_register"), E("ev_seal_log")], "fact", "f_not_issued", "establishes", "strong",
  "رقم الصادر 41 مأخوذ لكتاب آخر في تاريخ آخر، ولا قيد لهذا الخطاب في سجل الصادر؛ وسجل الختم لا يذكر استعمالاً في يوم التاريخ المكتوب. سجلان منفصلان يتفقان.", ["KO-RS-06-002", "KO-RS-05-004"])
I("i_issued_b", [E("ev_template_samples"), E("ev_leave_notice")], "fact", "f_not_issued", "establishes", "strong",
  "اختلاف الافتتاح والختام وموضع الرقم والختم عن ثلاثة كتب سابقة، قرينة ضعيفة وحدها؛ ويقويها إشعار موقّع بأن لا يصدر شيء باسمها أيام التاريخ.", ["KO-RS-06-002", "KO-FC-04B-004"])
I("i_made_a", [E("ev_print_log"), E("ev_file_properties")], "fact", "f_firas_made", "establishes", "strong",
  "الطباعة جرت من حساب فراس بعد دقائق من حفظ ملف باسمه وبقالب النادي؛ مصدران منفصلان، أحدهما نظام المكتبة والآخر الملف نفسه.", ["KO-RS-05-004", "KO-FC-04-026"])
I("i_made_b", [E("ev_chat_log"), E("ev_club_room_log")], "fact", "f_firas_made", "establishes", "strong",
  "الرسالة التي أرسلت الملف خرجت بعد خروج فراس من غرفة لم يدخلها غيره، ووائل لم يدخلها إلا بعد الرسالة بساعة؛ فالملف لم يكن من عند وائل.", ["KO-RS-05-004", "KO-FC-04-024"])
I("i_cl_firas", [Fa("f_firas_made")], "claim", "cl_firas_office", "contradicts_claim", "strong",
  "كان الخطاب على حسابه في الغرفة وفي الطابعة، لا في المكتب.", ["KO-RS-05-014"])
I("i_cl_wael", [Fa("f_not_issued")], "claim", "cl_letter_genuine", "contradicts_claim", "strong",
  "الرقم والختم والاسم شكل يمكن نسخه؛ والأصالة تقاس بالقيد والسجل لا بالمظهر.", ["KO-RS-06-002", "KO-RS-05-014"])
I("i_support_firas", [Fa("f_not_issued"), Fa("f_firas_made")], "hypothesis", "h_firas", "supports", "strong",
  "الخطاب لم يخرج من الدار، وقد أُعدّ وأُرسل من حساب فراس وفي غرفته؛ فهذه الفرضية تفسّر السجلات الأربعة.", ["KO-RS-06-007"])
I("i_rule_genuine", [Fa("f_not_issued"), Fa("f_firas_made")], "hypothesis", "h_genuine", "rules_out", "conclusive",
  "خطاب لا قيد له ولا ختم ولا تفويض، أُعدّ خارج الدار؛ فمهما بدا حاراً لا يكون من المديرة.", ["KO-RS-06-008"])
I("i_rule_wael", [Fa("f_firas_made"), Fa("f_not_issued")], "hypothesis", "h_wael", "rules_out", "strong",
  "الملف خرج من حساب غيره وغرفة لم يكن فيها وقت الإعداد، ووصله على أنه من المكتب؛ فالاستفادة من الخطاب لا تجعله صانعه.", ["KO-RS-06-008"])
I("i_rule_nabil", [Fa("f_not_issued"), Fa("f_firas_made")], "hypothesis", "h_nabil", "rules_out", "strong",
  "من يملك مفتاح الخزنة لم يفتحها في تلك الأيام، والخطاب لم يمرّ بقيده ولا بختمه؛ والملف خرج من حساب آخر.", ["KO-RS-06-008"])

ck = [
    {"character_id": "wael", "knows": [K("f_wael_says_office"), K("f_chat_exists"), K("f_file_exists")], "hides": [], "believes": [{"claim_id": "cl_letter_genuine", "stance": "sincere"}]},
    {"character_id": "nabil", "knows": [K("f_nabil_says"), K("f_register_exists", "professional"), K("f_seal_log_exists", "professional"), K("f_safe_keys", "professional")], "hides": [], "believes": []},
    {"character_id": "firas", "knows": [], "hides": [{"fact_id": "f_firas_made", "reveal_when": {"presented": {"evidence_id": "ev_print_log", "to_character": "firas"}}, "cover_claim_id": "cl_firas_office", "reveal_line_id": "fr_made"}],
     "believes": [{"claim_id": "cl_firas_office", "stance": "deliberate_lie"}]},
    {"character_id": "hana", "knows": [K("f_leave_notice_exists"), K("f_samples_exist", "professional")], "hides": [], "believes": []},
    {"character_id": "sarah", "knows": [K("f_letter_doubted")], "hides": [], "believes": []},
    {"character_id": "labiba", "knows": [K("f_print_log_exists", "professional")], "hides": [], "believes": []},
    {"character_id": "adel", "knows": [K("f_club_log_exists", "professional")], "hides": [], "believes": []},
]
hyps = [
    {"id": "h_genuine", "statement_ar": "الخطاب سليم وصدر من المديرة، وكانت فقط شديدة الحماسة هذه المرة.", "is_true": False, "plausibility_at_start": "high"},
    {"id": "h_wael", "statement_ar": "كتب وائل الخطاب بنفسه ليُقبل في الورشة.", "is_true": False, "plausibility_at_start": "medium", "suspect_id": "wael"},
    {"id": "h_nabil", "statement_ar": "أصدر كاتب المكتب الخطاب خارج الأصول لأنه يملك الختم.", "is_true": False, "plausibility_at_start": "medium", "suspect_id": "nabil"},
    {"id": "h_firas", "statement_ar": "أعدّ فراس الخطاب خارج الدار وأعطاه لوائل على أنه من المكتب.", "is_true": True, "plausibility_at_start": "low", "suspect_id": "firas"},
]
mis = [
    {"id": "rh_form", "points_to_hypothesis_id": "h_genuine", "planted_via_ar": "الخطاب يحمل رقماً وتاريخاً واسماً وختماً.", "evidence_ids": ["ev_letter"],
     "refuted_by_inference_ids": ["i_issued_a", "i_issued_b", "i_rule_genuine"],
     "fairness_note_ar": "سجل الصادر وسجل الختم وإشعار الغياب كلها بيد اللاعب، وتبيّن أن الأصالة لا تؤخذ من المظهر."},
    {"id": "rh_keys", "points_to_hypothesis_id": "h_nabil", "planted_via_ar": "الكاتب يحمل مفتاح الخزنة ويستطيع فتحها.", "evidence_ids": ["ev_safe_keys"],
     "refuted_by_inference_ids": ["i_rule_nabil", "i_issued_a"],
     "fairness_note_ar": "سجل الختم لا يذكر فتحاً في تلك الأيام، والإمكان وحده لا يكفي لإثبات الفعل."},
    {"id": "rh_benefit", "points_to_hypothesis_id": "h_wael", "planted_via_ar": "وائل هو المستفيد المباشر من الخطاب.", "evidence_ids": ["ev_wael_stmt", "ev_letter"],
     "refuted_by_inference_ids": ["i_rule_wael", "i_made_a", "i_made_b"],
     "fairness_note_ar": "المراسلة وسجل الغرفة يبيّنان أن الملف وصله ولم يخرج منه، والمصلحة ليست دليلاً على الفعل."},
]
los = std_los("يحكم على أصالة الوثيقة بمسارها لا بمظهرها: قيد في سجل الصادر، واستعمال للختم، وحضور الموقِّع؛ ويعامل فروق الأسلوب والتخطيط قرائن ضعيفة تحتاج دليلاً مستقلاً.", "KO-RS-06-002",
              ["يقابل الوثيقة بسجل الصادر", "لا يعدّ النبرة وحدها دليلاً", "لا ينسب خطاً إلى كاتب"])
ref = ("الخطاب لا يثبت أنه صدر من الدار. رقم 41/2026 مقيّد لكتاب آخر بتاريخ آخر، ولا استعمال للختم في اليوم المكتوب، والمديرة كانت غائبة وتركت إشعاراً بعدم إصدار شيء باسمها، وأسلوبه وتخطيطه يخالفان ثلاثة كتب سابقة، وهذه الأخيرة قرينة ضعيفة تقوّيها الأولى. أما صانعه فملف يحمل اسم حساب فراس وطبع من حسابه بعد دقائق، وغرفة النادي لم تدخلها غير بطاقته قبل رسالته التي أرسلت الملف إلى وائل. حدود الاستنتاج: لا نعرف إن كان فراس وحده أم بمساعدة، ولا تنسب السجلات خطاً لأحد، ولا يغني اعترافه عن السجلات.")
hints = [
    H("hg1", 1, "metacognitive", "قبل أن تحكم على وثيقة بنبرتها، اسأل: أين قيدها عند من يُفترض أنه أصدرها؟", {"always": True}, None, 0.02),
    H("hg2", 2, "focus_area", "قارن الرقم والتاريخ المكتوبين بسجل الصادر وسجل الختم، لا بالمظهر.", he("ev_letter"), None, 0.04),
    H("hg3", 3, "pointer", "اسأل كاتب المكتب عن سجليه، واسأل من يملك السجلات الأخرى: الطباعة والباب.", he("ev_letter"), None, 0.08),
    H("hi1", 1, "metacognitive", "هل الاختلاف في الأسلوب كافٍ وحده أم يلزمه دليل ثانٍ من نوع آخر؟", he("ev_letter"), "i_issued_b", 0.02),
    H("hi2", 2, "pointer", "ابحث عن ما يخص غياب المديرة في تلك الأيام وعن نماذج كتبها السابقة.", he("ev_letter"), "i_issued_b", 0.06),
    H("hm1", 1, "metacognitive", "من أين خرج الملف قبل أن يصل إلى وائل؟", he("ev_letter"), "i_made_a", 0.02),
    H("hm2", 2, "pointer", "اسأل مسؤولة الطباعة عن حساب الطابع، ثم قارنه ببيانات الملف.", he("ev_letter"), "i_made_a", 0.06),
]
Act("a_read_letter", "examine", "اقرأ الخطاب المقدَّم", al, [G("ev_letter")], "loc_workshop", "READ_LETTER")
interviews([("wael", "وائل"), ("nabil", "نبيل"), ("firas", "فراس"), ("hana", "هناء"), ("sarah", "سارة"), ("labiba", "لبنى"), ("adel", "عادل")])
get("ev_chat_log", "اطلب نسخة محادثة وائل وفراس", fu("f_chat_exists"), "loc_workshop")
get("ev_file_properties", "اطلب بيانات الملف الإلكتروني", fu("f_file_exists"), "loc_club")
get("ev_outgoing_register", "اطلب صفحة سجل الصادر", fu("f_register_exists"), "loc_office", "GET_REGISTER")
get("ev_seal_log", "اطلب سجل استعمال الختم", fu("f_seal_log_exists"), "loc_office")
get("ev_safe_keys", "اطلب قائمة حملة مفتاح الخزنة", fu("f_safe_keys"), "loc_office")
get("ev_leave_notice", "اطلب إشعار غياب المديرة", fu("f_leave_notice_exists"), "loc_office")
get("ev_template_samples", "اطلب مقارنة الخطاب بكتب المديرة السابقة", fu("f_samples_exist"), "loc_office", "GET_SAMPLES")
get("ev_print_log", "اطلب سجل طباعة المكتبة", fu("f_print_log_exists"), "loc_library")
get("ev_club_room_log", "اطلب سجل باب غرفة النادي", fu("f_club_log_exists"), "loc_club", "GET_CLUB_LOG")
Act("a_note_wael", "examine", "دوّن إفادة وائل", fu("f_wael_says_office"), [G("ev_wael_stmt")], "wael", "NOTE_WAEL")
Act("a_note_nabil", "examine", "دوّن إفادة نبيل", fu("f_nabil_says"), [G("ev_nabil_stmt")], "nabil", "NOTE_NABIL")
Act("a_note_firas", "examine", "دوّن إفادة فراس", fu("f_firas_made"), [G("ev_firas_stmt")], "firas", "NOTE_FIRAS")
Act("p_print_firas", "present_evidence", "اعرض سجل الطباعة على فراس", {"presented": {"evidence_id": "ev_print_log", "to_character": "firas"}}, [{"op": "emit_event", "ref_id": "PRESENTED_PRINT"}], "firas", "P_PRINT_FIRAS", 0)
tail_actions()
topics = [
    {"id": "t_office", "label_ar": "من أعطاك الخطاب", "example_questions_ar": ["من أعطاك الخطاب؟", "ماذا قيل لك عنه؟"], "fact_ids": ["f_wael_says_office"]},
    {"id": "t_chat", "label_ar": "الرسائل بينك وبين فراس", "example_questions_ar": ["هل عندك محادثة معه؟"], "fact_ids": ["f_chat_exists"]},
    {"id": "t_file", "label_ar": "الملف الإلكتروني", "example_questions_ar": ["هل عندك الملف كما وصلك؟"], "fact_ids": ["f_file_exists"]},
    {"id": "t_denial", "label_ar": "نفي الكتابة", "example_questions_ar": ["هل كتبت الخطاب؟"], "fact_ids": ["f_nabil_says"]},
    {"id": "t_register", "label_ar": "سجل الصادر", "example_questions_ar": ["كيف تقيّدون الكتب؟"], "fact_ids": ["f_register_exists"]},
    {"id": "t_seal", "label_ar": "الختم وسجله", "example_questions_ar": ["كيف يُستعمل الختم؟"], "fact_ids": ["f_seal_log_exists"]},
    {"id": "t_keys", "label_ar": "مفتاح الخزنة", "example_questions_ar": ["من يملك مفتاح الخزنة؟"], "fact_ids": ["f_safe_keys"]},
    {"id": "t_source", "label_ar": "من أين الخطاب", "example_questions_ar": ["من أين حصلت على الخطاب؟"], "fact_ids": [], "claim_ids": ["cl_firas_office"]},
    {"id": "t_made", "label_ar": "ما فعلته بالخطاب", "example_questions_ar": ["هل كتبت الخطاب أو طبعته؟"], "fact_ids": ["f_firas_made"]},
    {"id": "t_leave", "label_ar": "غياب المديرة", "example_questions_ar": ["أين كنت في تلك الأيام؟"], "fact_ids": ["f_leave_notice_exists"]},
    {"id": "t_samples", "label_ar": "كتب المديرة السابقة", "example_questions_ar": ["هل عندكم نماذج من كتبك؟"], "fact_ids": ["f_samples_exist"]},
    {"id": "t_tone", "label_ar": "أسلوب الخطاب", "example_questions_ar": ["ما الذي لاحظتِه في الخطاب؟"], "fact_ids": ["f_letter_doubted"]},
    {"id": "t_print", "label_ar": "سجل الطباعة", "example_questions_ar": ["ماذا يسجّل نظام الطباعة؟"], "fact_ids": ["f_print_log_exists"]},
    {"id": "t_club", "label_ar": "باب غرفة النادي", "example_questions_ar": ["ماذا يسجّل قارئ الباب؟"], "fact_ids": ["f_club_log_exists"]},
]
steps = [
    (1, "الخطاب بلا قيد: الرقم 41 محجوز لكتاب غيره، والختم لم يُستعمل في اليوم المكتوب؛ سجلان منفصلان يكفيان لنفي صدوره من الدار.", ["ev_outgoing_register", "ev_seal_log"], "i_issued_a"),
    (2, "مسار ثانٍ: غياب المديرة وتعليمتها المكتوبة، ثم فروق الأسلوب والتخطيط عن ثلاثة نماذج؛ والفروق وحدها ضعيفة، وإشعار الغياب هو الذي يقوّيها.", ["ev_leave_notice", "ev_template_samples"], "i_issued_b"),
    (3, "الصانع: ملف بحساب فراس وقالب ناديه طُبع من حسابه بعد دقائق.", ["ev_print_log", "ev_file_properties"], "i_made_a"),
    (4, "مسار ثانٍ: رسالة إرسال الملف بعد خروجه من غرفة لم يدخلها غيره، ووائل لم يدخلها إلا بعدها بساعة.", ["ev_chat_log", "ev_club_room_log"], "i_made_b"),
    (5, "بقية الأطراف: مفتاح الخزنة إمكان بلا فتح مسجّل، ومصلحة وائل ليست فعلاً؛ وإفادة فراس تؤيد سجلات سبقتها.", ["ev_safe_keys", "ev_firas_stmt"], "i_rule_nabil"),
]
alt = ["يمكن إثبات الحلقتين بالمسار الأول: سجل الصادر وسجل الختم لنفي الصدور، وسجل الطباعة وبيانات الملف لتحديد الصانع.",
       "ويمكن إثباتهما بالمسار الثاني: إشعار الغياب مع مقارنة النماذج، ثم المراسلة مع سجل باب الغرفة؛ والأقوى أن يتفق المساران."]
notlimits = ["لا نعرف إن كان فراس وحده أو بمساعدة، ولا لماذا اختار هذه الصيغة الحارة.",
             "سجل الطباعة وبيانات الملف يربطان الحساب لا الشخص؛ قوتهما في اتفاقهما مع المراسلة وسجل الباب.",
             "لا تُنسب النتيجة إلى خط أحد؛ لا معدلات خطأ مقيسة هنا، وما استُعمل هو القيد والسجل لا شكل الحروف."]
notes = ["الوثيقة تُحكم بمسارها: هل قيدها عند من يُفترض أنه أصدرها؟ وهل استُعمل ختمه؟ وهل كان موقّعها حاضراً؟ والمظهر الكامل لا يكفي، والمظهر المريب لا يكفي أيضاً.",
         "فروق النبرة والتخطيط عن نماذج معروفة قرائن ضعيفة وحدها، وقد يكتب الشخص بغير عادته؛ تُعتمد حين يوافقها دليل مستقل كغياب القيد.",
         "الشاهدان اللذان «يتذكران» الصيغة نفسها بعد تلقين صاحب المصلحة يشبهان كتاباً يقلّد كتاباً؛ ابحث عن سجل لا يعتمد على أي منهما.",
         "لم يتعمد وائل شيئاً: صدّق صديقه. وفراس أراد المساعدة بطريق خاطئ. والإصلاح تعليمي ومؤسسي: يُسحب الخطاب، ويُتاح لوائل التقدم بالطريق الصحيح، ويتعلم فراس كلفة الاسم الذي ليس له.",
         "بطاقة الأصل: القضية أصلية من ATHAR على بنية «الكتاب الذي بالغ في التوكيد» في مكتبة الحالات، وتعرض الكشف فقط لا الصنع."]
premise = {"hook_ar": "خطاب ترشيح سليم الشكل، لكن لغته أشد حماسة من كل ما كتبته المديرة. فهل يكفي الشك في النبرة؟",
           "player_role_ar": "أنت طالب متدرب في لجنة التحقق بدار السِّجِل، وطُلب منك رأي معلّل في أصالة خطاب ترشيح، دون اتهام أحد قبل أن تثبت السجلات شيئاً.",
           "setting_ar": "دار السِّجِل في مدينة «القنطرة»، من الاثنين إلى الأربعاء. الأوقات بساعة الدار.",
           "public_fact_ids": ["f_letter_received", "f_letter_doubted"],
           "assumed_general_knowledge_ar": ["الوثيقة السليمة الشكل قد لا تكون صادرة عن الجهة المنسوبة إليها", "اختلاف الأسلوب قرينة ضعيفة وحده", "لا يُنسب خط عربي إلى كاتب بلا معدلات خطأ مقيسة"]}
meta = {"title_ar": "الخطاب الذي بالغ في التوكيد", "title_en": "The Over-Emphatic Letter", "age_band": "16-18", "estimated_minutes": 30, "difficulty": 3,
        "content_flags": ["no_violence", "fraud"],
        "knowledge_object_refs": ["KO-RS-06-002", "KO-FC-04B-004", "KO-FC-04-026", "KO-FC-04-024", "KO-RS-05-004", "KO-RS-05-001", "KO-RS-05-014", "KO-RS-06-001", "KO-RS-06-008", "KO-RS-06-021", "KO-RS-06-009", "KO-RS-05-002", "KO-RS-05-005"]}
ui = {
    "clock": {"epoch_hhmm": "08:00", "zone_label_ar": "ساعة الدار"},
    "cover": {"title_ar": "الخطاب الذي بالغ في التوكيد", "tagline_ar": "رقم وختم واسم… أين القيد؟", "kicker_ar": "الملف الثامن والعشرون · أصل الوثيقة", "glyph": "✉", "accent": "rose"},
    "cold_open_ar": ["الأربعاء، 10:00.", "قدّم وائل خطاب ترشيح باسم المديرة إلى ورشة الترميم: رقم وتاريخ وختم واسم.", "تقول المنسقة إن لغته أشد حماسة من كل ما عرفته عن كتب المديرة، لكنها لا تعدّ ذلك دليلاً.",
                    "قبل أي حكم: أين قيد هذا الخطاب؟ وأين كانت المديرة؟ ومن أين خرج الملف؟"],
    "limit_menu": [
        {"id": "l_who_alone", "label_ar": "لا نعرف إن كان فراس وحده أو بمساعدة، ولا لماذا اختار هذه الصيغة"},
        {"id": "l_account_person", "label_ar": "سجل الطباعة وبيانات الملف يربطان الحساب لا الشخص، وقوتهما في اتفاقهما مع المراسلة وسجل الباب"},
        {"id": "l_no_handwriting", "label_ar": "لم يُنسب الخطاب إلى خط أحد، فلا معدلات خطأ مقيسة هنا"},
        {"id": "l_invalid_tone", "label_ar": "حرارة الأسلوب وحدها تكفي لإثبات التزوير"},
        {"id": "l_invalid_benefit", "label_ar": "استفادة وائل من الخطاب تدل على أنه صانعه"},
        {"id": "l_invalid_keys", "label_ar": "حمل نبيل مفتاح الخزنة يدل على أنه استعمل الختم"}],
    "mind_change_menu": [
        {"id": "m_register_entry", "label_ar": "ظهور قيد للخطاب في سجل الصادر أو في سجل الختم"},
        {"id": "m_delegation", "label_ar": "ظهور تفويض مكتوب من المديرة بإصدار الخطاب"},
        {"id": "m_account_shared", "label_ar": "ثبوت أن حساب فراس كان بيد غيره وقت الطباعة"},
        {"id": "m_popular", "label_ar": "اتفاق أكثر الطلاب على أن وائل هو الصانع"}],
    "transfer": {
        "id": "tr_permit", "title_ar": "اختبار نقل المهارة: تصريح الرحلة",
        "scenario_ar": "قدّم طالب تصريح رحلة باسم مدير مدرسة، رقمه 17 وتاريخه الخميس. أمامك وثيقتان من واقعة خيالية لا علاقة لها بالقضية.",
        "documents": [
            {"title_ar": "سجل الصادر", "body_ar": "الرقم 16 — الأربعاء — إلى الأولياء\nالرقم 17 — الجمعة — إلى المقصف\nالرقم 18 — الجمعة — إلى المكتبة\nلا تصريح رحلة في الخميس."},
            {"title_ar": "مقارنة بنماذج", "body_ar": "التصريح المتنازع عليه يبدأ بعبارة مختلفة عن ثلاثة تصاريح سابقة، والختم فيه في موضع آخر."}],
        "prompt_ar": "اختر الخطوات الصالحة للحكم على أصالة التصريح (يمكنك اختيار أكثر من خطوة).",
        "options": [
            {"id": "o1", "text_ar": "البحث عن قيد التصريح في سجل الصادر قبل أي شيء"},
            {"id": "o2", "text_ar": "البحث عن سجل ثانٍ مستقل كسجل الختم أو سجل غياب المدير"},
            {"id": "o3", "text_ar": "مقارنة الأسلوب والتخطيط بنماذج معروفة واعتبارها قرينة ضعيفة تحتاج دعماً"},
            {"id": "o4", "text_ar": "ترك نسبة الخط إلى كاتب معيّن لأن ذلك غير مقيس هنا"},
            {"id": "o5", "text_ar": "الحكم بأن التصريح مزوّر لأن أسلوبه مختلف"},
            {"id": "o6", "text_ar": "اعتبار التصريح سليماً لأن عليه رقماً وختماً"},
            {"id": "o7", "text_ar": "اتهام الطالب الذي قدمه لأنه المستفيد"}],
        "free_text_prompt_ar": "اكتب في ثلاثة أسطر كيف تقدّر نسبة الترجيح بأن التصريح غير صادر من المدير.",
    },
    "skills": [{"skill_id": "KO-RS-06-002", "track": "C"}, {"skill_id": "KO-FC-04B-004", "track": "E"}, {"skill_id": "KO-FC-04-026", "track": "E"}, {"skill_id": "KO-RS-05-004", "track": "B"}, {"skill_id": "KO-RS-05-002", "track": "D"}],
    "stage_hooks_ar": {"briefing": "رقم وختم واسم… فأين القيد؟", "investigating": "الوثيقة تُسأل عن مسارها قبل أن تُسأل عن مظهرها.", "review": "قبل أن تغلق الملف: ما الذي لا تستطيع السجلات أن تقوله عن الخط؟", "resolved": "أُغلق الملف. سُحب الخطاب، وفُتح لوائل باب التقدم الصحيح."},
    "character_glyphs": {"wael": "و", "nabil": "ن", "firas": "ف", "hana": "ه", "sarah": "س", "labiba": "ل", "adel": "ع"},
}
sc = {
    "accepted_conclusions": {
        "h_firas": {"grade": 1, "note_ar": "استنتاج متسق مع الأدلة ويتطلب ذكر حدوده."},
        "h_genuine": {"grade": 0, "note_ar": "يأخذ الأصالة من المظهر ويتجاهل غياب القيد والختم والمديرة."},
        "h_wael": {"grade": 0, "note_ar": "يبني على المصلحة وحدها، والملف وصله من غيره."},
        "h_nabil": {"grade": 0, "note_ar": "إمكان فتح الخزنة ليس استعمالاً لها، وسجل الختم يخلو من أي استعمال."}},
    "confidence_band": {"h_firas": [65, 90], "h_genuine": [0, 15], "h_wael": [0, 20], "h_nabil": [0, 15]},
    "source_key": {"ev_letter": "claim", "ev_file_properties": "redisplay", "ev_chat_log": "redisplay", "ev_club_room_log": "primary_record", "ev_print_log": "primary_record",
                   "ev_outgoing_register": "primary_record", "ev_seal_log": "primary_record", "ev_safe_keys": "primary_record", "ev_leave_notice": "primary_record",
                   "ev_template_samples": "template", "ev_wael_stmt": "claim", "ev_nabil_stmt": "claim", "ev_firas_stmt": "claim"},
    "link_key": {
        "h_firas": {"ev_print_log": "supports", "ev_file_properties": "supports", "ev_chat_log": "supports", "ev_club_room_log": "supports", "ev_outgoing_register": "supports", "ev_seal_log": "supports",
                    "ev_leave_notice": "supports", "ev_template_samples": "supports", "ev_firas_stmt": "supports"},
        "h_genuine": {"ev_letter": "supports", "ev_outgoing_register": "weakens", "ev_seal_log": "weakens", "ev_leave_notice": "weakens", "ev_template_samples": "weakens"},
        "h_wael": {"ev_wael_stmt": "supports", "ev_letter": "neutral", "ev_chat_log": "weakens", "ev_club_room_log": "weakens", "ev_print_log": "weakens", "ev_file_properties": "weakens"},
        "h_nabil": {"ev_safe_keys": "supports", "ev_nabil_stmt": "neutral", "ev_seal_log": "weakens", "ev_outgoing_register": "weakens", "ev_print_log": "weakens"},
    },
    "required_limits": ["l_who_alone", "l_account_person"], "valid_mind_changers": ["m_register_entry", "m_delegation", "m_account_shared"],
    "invalid_limits": ["l_invalid_tone", "l_invalid_benefit", "l_invalid_keys"],
    "decisive_evidence": ["ev_outgoing_register", "ev_seal_log", "ev_template_samples", "ev_leave_notice", "ev_print_log", "ev_file_properties", "ev_chat_log", "ev_club_room_log"],
    "timeline_requirement": [{"evidence_id": "ev_outgoing_register", "utc_minute": 130, "tol": 8}, {"evidence_id": "ev_club_room_log", "utc_minute": 450, "tol": 5}, {"evidence_id": "ev_print_log", "utc_minute": 482, "tol": 4},
                             {"evidence_id": "ev_chat_log", "utc_minute": 510, "tol": 4}, {"evidence_id": "ev_letter", "utc_minute": 3000, "tol": 30}],
    "refuted_hypotheses": ["h_genuine", "h_wael", "h_nabil"],
    "transfer_key": {"valid": ["o1", "o2", "o3", "o4"], "invalid": ["o5", "o6", "o7"]},
}
assemble(CID, meta, premise, {"characters": chars, "locations": locations, "objects": objects, "organizations": orgs}, ["firas"],
         "لم يصدر الخطاب من الدار. أعدّه فراس وطبعه بحسابه في غرفة ناديه ليساعد صديقه، وسلّمه لوائل على أنه من المكتب، فصدّق وائل وقدّمه، ولم يتعمد أحدهما أذى.",
         ["f_not_issued", "f_firas_made"], claims, timeline, ck, hyps, mis, los, ref, hints, topics, steps, alt, notlimits, notes, ui, sc)
