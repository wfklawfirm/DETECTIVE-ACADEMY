#!/usr/bin/env python3
# Case c029 «شهادتان بكلمات واحدة» — witness memory and independence of witnesses. Archetype ARC-26 «فرّق بين الشهود» (library): only the practice
# of reading statements separately survives (the original's escalation, threats and homicide ending are NOT used; nobody is pressed to confess).
# Teaches: two eyewitness accounts that match WORD FOR WORD (including a wrong detail) are one account copied, not two; innocent differences
# between genuinely independent accounts are normal (angle, memory) and are not lies; settle it with a record that does not depend on any
# witness (a recovered signed sheet with times, photographs, a roster, a crate log). No-culprit convention: Reem (a volunteer who tidied the
# table and swept the sheet into a recycling crate by mistake) is recorded in culprit_ids; Omar is falsely accused; the two copying witnesses
# believed the message they read. Time lab omitted (labs: []); timeline requirement used.
# Calendar (fictional): minute 0 = Wednesday 09:00 (student-council vote day). 10:15 = 75; 11:07 = 127. All names are fictional.
# Usage: gen_c029.py OUT_DIR
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

CID = "c029_same_words"
SENT = "رأيت عمر الناصر الساعة العاشرة والربع يلتقط كشف الناخبين عن الطاولة ويخرج به مسرعاً نحو السلم."
ch("omar", "عمر الناصر", "suspect", "طالب في الصف العاشر، مرشح لمجلس الطلاب",
   "عصبي حين يُتهم بما لم يفعله ويتحدث بسرعة، لكنه يقدّم ما يملكه من أوراق ويقبل أن تُراجع. لا يخفي أنه اعترض على نشر الكشف.",
   ["أن يبرّئ نفسه", "أن يُجرى التصويت بنزاهة"],
   [L("om_greet", "greeting", "لم آخذ شيئاً. اسألني ما تريد."),
    L("om_says", "reveal", "كنت في مكتبة المدرسة أطبع ملصقات الحملة قرابة العاشرة، ثم عدت إلى القاعة بعد العاشرة والنصف ووقفت في الصف مع الناخبين.", ["f_omar_says"]),
    L("om_objected", "reveal", "نعم، اعترضت في الاجتماع السابق على تعليق الكشف علناً لأن فيه أسماء الطلاب، لكنني قبلت القرار.", ["f_omar_objected"]),
    L("om_unknown", "deflect_unknown", "لا أعرف."),
    L("om_off", "deflect_offtopic", "اسألني عن ذلك اليوم."),
    L("om_bye", "farewell", "أريد الكشف أن يعود كما أريد أن يُفحص كلامي.")])
ch("reem", "ريم الشامي", "suspect", "طالبة متطوعة في فريق التنظيم بسترة زرقاء",
   "نشيطة وسريعة، تعمل بما كُلّفت به وتثق بأن ما رمته كان مسودات. تتفاجأ إذا ظهر أن بين الأوراق ما هو مهم، وتتعاون.",
   ["أن تؤدي مهمتها", "ألا تُلام على سوء فهم"],
   [L("rm_greet", "greeting", "كلفتني الأستاذة بترتيب الطاولة بعد التصويت."),
    L("rm_stack", "reveal", "في الحادية عشرة جمعت الأوراق المتناثرة عن طاولة التسجيل ووضعتها في صندوق التدوير الأزرق، وقلت لنفسي إنها مسودات.", ["f_reem_stacked"]),
    L("rm_belief", "reveal", "أنا لا أرمي إلا المسودات، وتأكدت من ذلك.", None, ["cl_reem_only_scrap"]),
    L("rm_unknown", "deflect_unknown", "لا أذكر أكثر."),
    L("rm_off", "deflect_offtopic", "اسألني عن الترتيب."),
    L("rm_bye", "farewell", "سأفحص كل ورقة قبل أن أضعها في الصندوق بعد اليوم.")])
ch("karam", "كرم الداود", "witness", "طالب في الصف العاشر",
   "اجتماعي ويثق بما يصله من زملائه، ويظن أنه يتذكر ما قرأه كأنه شاهده. يتراجع إذا طُلب منه أن يفرّق بين ما رآه وما قرأه.",
   ["ألا يبدو كاذباً", "أن يُنصَف زملاؤه"],
   [L("kr_greet", "greeting", "أنا قلت ما رأيته."),
    L("kr_says", "reveal", "قلت للأستاذة: " + SENT, ["f_karam_says"]),
    L("kr_msg", "reveal", "قرأت رسالة في مجموعة الصف قبل أن أُستدعى للإفادة، ولا أذكر ما فيها بالضبط.", ["f_group_msg_exists"]),
    L("kr_unknown", "deflect_unknown", "لا أذكر أكثر."),
    L("kr_off", "deflect_offtopic", "اسألني عمّا رأيته."),
    L("kr_bye", "farewell", "ربما خلطت بين ما قرأته وما رأيته.")])
ch("dina", "دينا العبدالله", "witness", "طالبة في الصف العاشر",
   "هادئة وتميل إلى موافقة صديقتها، وتفتح الرسائل فور وصولها. لا تقصد الإساءة لأحد.",
   ["ألا تسبب مشكلة لأحد", "أن تنتهي القضية"],
   [L("dn_greet", "greeting", "أنا أجيب بما أذكر."),
    L("dn_says", "reveal", "قلت للأستاذة: " + SENT, ["f_dina_says"]),
    L("dn_receipts", "reveal", "المجموعة تُظهر لكل رسالة من فتحها ومتى، وقد فتحت أنا الرسالة صباح اليوم نفسه.", ["f_read_receipts_exist"]),
    L("dn_unknown", "deflect_unknown", "لا أذكر."),
    L("dn_off", "deflect_offtopic", "اسألني عن إفادتي."),
    L("dn_bye", "farewell", "لا أريد أن أظلم أحداً.")])
ch("lina", "لينا الحايك", "witness", "طالبة في الصف الحادي عشر",
   "دقيقة الوصف وصريحة بحدود ما رأته، وتقول إن تذكرها غير كامل. لم تقرأ رسائل المجموعة ذلك الصباح.",
   ["أن تقول ما رأته فقط"],
   [L("ln_greet", "greeting", "سأقول ما رأيته وأوضح ما لم أره."),
    L("ln_says", "reveal", "رأيت قرابة الحادية عشرة متطوعة بسترة زرقاء تجمع أوراقاً عن طاولة التسجيل، ولم أر وجهها ولا أعرف ماذا كانت تجمع.", ["f_lina_says"]),
    L("ln_unknown", "deflect_unknown", "لم أنتبه."),
    L("ln_off", "deflect_offtopic", "اسألني عمّا رأيته."),
    L("ln_bye", "farewell", "ذاكرتي ناقصة وأقولها.")])
ch("nadim", "نديم الخوري", "witness", "مصوّر نادي الإعلام",
   "منهجي، يحتفظ بصوره بوقتها ويصرّح بأن ساعة كاميرته مضبوطة صباح اليوم.",
   ["أن تبقى صوره سليمة"],
   [L("nd_greet", "greeting", "أصوّر للنادي وأحفظ كل شيء."),
    L("nd_photo", "reveal", "التقطت صورة للقاعة نحو العاشرة وأربعين دقيقة وفي خلفيتها ساعة الحائط، وتظهر فيها طاولة التسجيل.", ["f_photo_1040_exists"]),
    L("nd_unknown", "deflect_unknown", "ليس عندي."),
    L("nd_off", "deflect_offtopic", "اسألني عن صوري."),
    L("nd_bye", "farewell", "الصورة كما هي.")])
ch("rula", "رولا الحلبي", "witness", "معلمة مشرفة على القاعة",
   "منظمة وتكتب كل ما تكلّف به، وتحتفظ بما استُرجع. لا تتهم أحداً قبل السجلات.",
   ["أن يُستعاد الكشف", "أن يُنصَف الجميع"],
   [L("rl_greet", "greeting", "أشرفت على القاعة وأحتفظ بأوراقها."),
    L("rl_roll", "reveal", "استُرجع الكشف ظهراً بتوقيعات الناخبين وأوقاتها، وهو عندي.", ["f_roll_recovered"]),
    L("rl_roster", "reveal", "وزّعت المتطوعين على مهام بورقة موقّعة، وكان على إحداهن ترتيب طاولة التسجيل بعد التصويت.", ["f_tidy_roster_exists"]),
    L("rl_photo", "reveal", "التقطت بهاتفي صورة للقاعة بعد الترتيب لأضيفها إلى تقرير الحدث.", ["f_photo_1110_exists"]),
    L("rl_unknown", "deflect_unknown", "لا أعرف."),
    L("rl_off", "deflect_offtopic", "اسألني عن القاعة."),
    L("rl_bye", "farewell", "الأوراق عندي كما هي.")])
ch("hamza", "حمزة النجار", "witness", "عامل النظافة المسؤول عن صناديق التدوير",
   "مباشر وصبور، يدوّن على بطاقة كل صندوق وقت جمعه وموضعه.",
   ["أن تبقى بطاقاته صحيحة"],
   [L("hm_greet", "greeting", "أجمع الصناديق وأكتب على بطاقاتها."),
    L("hm_crate", "reveal", "على كل صندوق تدوير بطاقة بالموضع ووقت الجمع، وعند الفرز أدوّن ما وُجد فيه.", ["f_crate_record_exists"]),
    L("hm_unknown", "deflect_unknown", "لا أعرف."),
    L("hm_off", "deflect_offtopic", "اسألني عن الصناديق."),
    L("hm_bye", "farewell", "البطاقة تتكلم.")])

locations = [{"id": "loc_hall", "name_ar": "قاعة التصويت ب", "description_ar": "قاعة فيها طاولة التسجيل وكشف الناخبين."},
             {"id": "loc_library", "name_ar": "مكتبة المدرسة", "description_ar": "مكتبة فيها طابعة."},
             {"id": "loc_yard", "name_ar": "فناء التدوير", "description_ar": "مكان فرز صناديق التدوير."}]
objects = [{"id": "obj_roll", "name_ar": "كشف الناخبين", "description_ar": "ورقتان عليهما أسماء الناخبين وتوقيعاتهم وأوقات الاقتراع."}]
orgs = [{"id": "org_school", "name_ar": "مدرسة القنطرة", "description_ar": "مدرسة خيالية تُجري انتخابات مجلس الطلاب."}]

F("f_roll_missing", "فُقد كشف الناخبين من طاولة التسجيل في قاعة التصويت ب أثناء يوم الانتخاب.", "event", ["obj_roll"], 0)
F("f_omar_accused", "قال طالبان إنهما رأيا عمر يأخذ الكشف عن الطاولة قرابة العاشرة والربع.", "attribute", ["omar", "karam", "dina"], 0)
F("f_karam_says", "قال كرم للمعلمة إنه رأى عمر يلتقط الكشف ويخرج به مسرعاً نحو السلم قرابة العاشرة والربع.", "attribute", ["karam"], 1, T(165))
F("f_dina_says", "قالت دينا للمعلمة بالصيغة نفسها إنها رأت عمر يلتقط الكشف ويخرج به مسرعاً نحو السلم قرابة العاشرة والربع.", "attribute", ["dina"], 1, T(160))
F("f_group_msg_exists", "نُشرت في مجموعة الصف رسالة عن عمر والكشف قبل أن يُدلي الطالبان بإفادتيهما.", "event", ["karam", "dina"], 1, T(118))
F("f_read_receipts_exist", "تُظهر المجموعة لكل رسالة من فتحها ومتى.", "state", ["dina"], 1)
F("f_lina_says", "قالت لينا إنها رأت قرابة الحادية عشرة متطوعة بسترة زرقاء تجمع أوراقاً عن الطاولة دون أن تعرف ماذا كانت.", "attribute", ["lina"], 1, T(120))
F("f_photo_1040_exists", "التقط مصوّر نادي الإعلام صورة للقاعة نحو 10:40 تظهر فيها طاولة التسجيل وساعة الحائط.", "event", ["nadim"], 1, T(100), "loc_hall")
F("f_photo_1110_exists", "التقطت المعلمة صورة للقاعة بعد الترتيب لتقرير الحدث.", "event", ["rula"], 1, T(127), "loc_hall")
F("f_roll_recovered", "استُرجع الكشف ظهراً وفيه توقيعات الناخبين وأوقاتها.", "event", ["rula", "obj_roll"], 1, T(190))
F("f_tidy_roster_exists", "وزّعت المعلمة المتطوعين على مهام بورقة موقّعة، ومنها ترتيب طاولة التسجيل.", "state", ["rula"], 1)
F("f_crate_record_exists", "تحمل صناديق التدوير بطاقات بموضع الجمع ووقته، ويدوّن عامل النظافة ما وُجد عند الفرز.", "state", ["hamza"], 1, None, "loc_yard")
F("f_omar_says", "يقول عمر إنه كان في المكتبة يطبع ملصقات الحملة قرابة العاشرة وعاد إلى القاعة بعد العاشرة والنصف.", "attribute", ["omar"], 1)
F("f_omar_objected", "اعترض عمر في اجتماع سابق على تعليق الكشف علناً ثم قبل القرار.", "event", ["omar"], 1)
F("f_reem_stacked", "جمعت ريم الأوراق المتناثرة عن طاولة التسجيل قرابة 11:00 ووضعتها في صندوق التدوير الأزرق.", "event", ["reem"], 1, T(120, "exact", 130), "loc_hall")
F("f_same_source", "الإفادتان المتطابقتان نُقلتا عن رسالة واحدة سبقتهما، فهما رواية واحدة نُسخت لا مشاهدتان مستقلتان.", "relation", ["karam", "dina"], 3, T(118, "exact", 165), None, ["KO-RS-05-004", "KO-RS-05-009"])
F("f_roll_swept", "ظل الكشف على الطاولة قيد الاستعمال بعد الوقت المنسوب إلى أخذه، ثم انتقل مع أوراق الترتيب إلى صندوق التدوير دون قصد من أحد.", "relation", ["obj_roll", "reem"], 3, T(110, "exact", 190), "loc_hall", ["KO-RS-05-014", "KO-RS-06-017"])

claims = [
    {"id": "cl_omar_took", "statement_ar": "رأيت عمر يأخذ الكشف عن الطاولة ويخرج به قرابة العاشرة والربع.", "kind": "honest_mistake", "held_by": ["karam", "dina"], "true_fact_id": "f_roll_swept",
     "contradicted_by_evidence_ids": ["ev_roll_entries", "ev_crate_tag", "ev_photo_1040"]},
    {"id": "cl_reem_only_scrap", "statement_ar": "لم أضع في الصندوق إلا مسودات.", "kind": "honest_mistake", "held_by": ["reem"], "true_fact_id": "f_roll_swept",
     "contradicted_by_evidence_ids": ["ev_crate_tag", "ev_photo_1110"]},
]
timeline = [
    {"id": "te_vote", "description_ar": "بدء اقتراع قاعة ب وتوقيع الناخبين على الكشف.", "time": T(80, "exact", 110), "location_id": "loc_hall", "actor_ids": [], "fact_ids": ["f_roll_recovered"]},
    {"id": "te_omar_lib", "description_ar": "عمر في مكتبة المدرسة يطبع ملصقات حملته.", "time": T(60, "approx", 95), "location_id": "loc_library", "actor_ids": ["omar"], "fact_ids": ["f_omar_says"], "motivated_by_ar": "تجهيز ملصقات الحملة"},
    {"id": "te_photo1", "description_ar": "نديم يصوّر القاعة.", "time": T(100), "location_id": "loc_hall", "actor_ids": ["nadim"], "fact_ids": ["f_photo_1040_exists"], "motivated_by_ar": "توثيق يوم الانتخاب لنادي الإعلام"},
    {"id": "te_msg", "description_ar": "رسالة في مجموعة الصف تذكر عمر والكشف.", "time": T(118), "actor_ids": [], "fact_ids": ["f_group_msg_exists"]},
    {"id": "te_tidy", "description_ar": "ريم ترتّب طاولة التسجيل وتضع الأوراق في صندوق التدوير.", "time": T(120, "exact", 130), "location_id": "loc_hall", "actor_ids": ["reem"], "fact_ids": ["f_reem_stacked"], "motivated_by_ar": "المهمة الموكلة إليها في ورقة المعلمة"},
    {"id": "te_lina", "description_ar": "لينا ترى المتطوعة تجمع أوراقاً.", "time": T(121), "location_id": "loc_hall", "actor_ids": ["lina"], "fact_ids": ["f_lina_says"], "motivated_by_ar": "كانت تنتظر دورها في القاعة"},
    {"id": "te_photo2", "description_ar": "رولا تصوّر القاعة بعد الترتيب.", "time": T(127), "location_id": "loc_hall", "actor_ids": ["rula"], "fact_ids": ["f_photo_1110_exists"], "motivated_by_ar": "توثيق الحدث للتقرير"},
    {"id": "te_stmts", "description_ar": "كرم ودينا يدليان بإفادتيهما.", "time": T(160, "exact", 165), "actor_ids": ["karam", "dina"], "fact_ids": ["f_karam_says", "f_dina_says"], "motivated_by_ar": "استدعتهما المعلمة بعد البلاغ"},
    {"id": "te_found", "description_ar": "عند فرز الصندوق يُسترجع الكشف.", "time": T(190), "location_id": "loc_yard", "actor_ids": ["hamza"], "fact_ids": ["f_crate_record_exists"], "motivated_by_ar": "فرز صناديق التدوير"},
]

V("ev_incident_report", "بلاغ فقدان كشف الناخبين", "documentary",
  "بلاغ مشرفة القاعة ب — الأربعاء 11:20\nفُقد كشف الناخبين (ورقتان) من طاولة التسجيل. أبلغ طالبان أنهما رأيا الطالب عمر الناصر يأخذه قرابة العاشرة والربع. أُوقف التسجيل مؤقتاً.",
  ["a_read_report"], ["f_roll_missing", "f_omar_accused"], "weak",
  "بلاغ يسجّل ادعاءً لا واقعة؛ ولا يذكر كيف عُرف ما قاله الطالبان.", red=True, loc="loc_hall")
V("ev_stmt_karam", "إفادة كرم (نص كما دوّنته المعلمة)", "testimonial",
  "إفادة كرم الداود — الأربعاء 11:45\n«" + SENT + "»",
  ["a_note_karam"], ["f_karam_says"], "weak",
  "إفادة شاهد؛ تُقرأ مع غيرها بحروفها، فالتطابق الحرفي بين روايتين يستدعي السؤال عن مصدر مشترك.", loc="loc_hall")
V("ev_stmt_dina", "إفادة دينا (نص كما دوّنته المعلمة)", "testimonial",
  "إفادة دينا العبدالله — الأربعاء 11:40\n«" + SENT + "»",
  ["a_note_dina"], ["f_dina_says"], "weak",
  "إفادة شاهدة؛ دُوّنت قبل إفادة كرم بخمس دقائق، وهي مطابقة لها حرفاً بحرف.", loc="loc_hall")
V("ev_stmt_lina", "إفادة لينا (نص كما دوّنته المعلمة)", "testimonial",
  "إفادة لينا الحايك — الأربعاء 11:50\n«رأيت قرابة الحادية عشرة متطوعة بسترة زرقاء تجمع أوراقاً عن طاولة التسجيل. لم أر وجهها ولا أعرف ماذا كانت تجمع. لم أرَ عمر في تلك الدقائق.»",
  ["a_note_lina"], ["f_lina_says"], "moderate",
  "إفادة بوصف محدود وبوقت مختلف عن الإفادتين الأخريين؛ الاختلاف بريء ولا يعني كذباً، وتقاس بسجلات لا تعتمد عليها.", loc="loc_hall")
V("ev_group_msg", "رسالة مجموعة الصف", "digital",
  "مجموعة صف العاشر — رسالة س. القاسم — الأربعاء 10:58\n«سمعت من أحدهم أن عمر الناصر الساعة العاشرة والربع يلتقط كشف الناخبين عن الطاولة ويخرج به مسرعاً نحو السلم. انتبهوا له!»\nلم تكن س. القاسم في القاعة ب بحسب جدول الحصص.",
  ["a_get_group_msg"], ["f_group_msg_exists", "f_same_source"], "strong",
  "تثبت وجود الصياغة قبل الإفادتين، ولا تثبت أن الطالبين قرآها؛ وهي بدورها نقل عن «أحدهم» لا مشاهدة.", loc="loc_hall")
V("ev_read_receipts", "قائمة من فتح رسالة المجموعة", "digital",
  "مجموعة صف العاشر — معلومات الرسالة 10:58\nفُتحت من: ك. الداود 11:03 · د. العبدالله 11:06 · ل. الحايك: لم تُفتح\nاستُدعى كرم ودينا إلى الإفادة 11:35.",
  ["a_get_read_receipts"], ["f_read_receipts_exist", "f_same_source"], "strong",
  "تبيّن من فتح الرسالة ومتى لا ما فهمه كل منهما، ولا تثبت وحدها النسخ؛ تقوى بالتطابق الحرفي مع الإفادتين.", loc="loc_hall")
V("ev_roll_entries", "الكشف المسترجع: توقيعات الناخبين وأوقاتها", "documentary",
  "كشف الناخبين — ورقتان مسترجعتان ظهر الأربعاء\nتوقيعات الناخبين بأوقاتها بخط كاتبة التسجيل: 10:22 · 10:25 · 10:31 · 10:37 · 10:41 · 10:48\nلا توقيع بعد 10:48. على الهامش آثار ضغط كأن أوراقاً وُضعت فوقه.",
  ["a_get_roll_entries"], ["f_roll_recovered", "f_roll_swept"], "strong",
  "ورقة أصلية بخط كاتبة التسجيل؛ تثبت أن الكشف كان بيد كاتبة التسجيل لحظة الأخذ المزعوم وبعده، ولا تقول بيد من وصل إلى الصندوق.", loc="loc_hall")
V("ev_crate_tag", "بطاقة صندوق التدوير الأزرق رقم 3", "documentary",
  "بطاقة الصندوق — بخط ح. النجار\nالموضع: قاعة التصويت ب · وقت الجمع: 11:30\nعند الفرز 12:10: مسودات ملونة، وورقتان من كشف الناخبين بين أوراق ملصقة معاً\nنُقل الكشف إلى المشرفة.",
  ["a_get_crate_tag"], ["f_crate_record_exists", "f_roll_swept"], "strong",
  "تبيّن أين وُجد الكشف ومتى جُمع الصندوق، ولا تبيّن من وضعه ولا لماذا.", loc="loc_yard")
V("ev_photo_1040", "صورة القاعة نحو 10:40", "digital",
  "كاميرا نادي الإعلام — بيانات الصورة: الأربعاء 10:40 (ضُبطت الساعة صباحاً)\nقاعة التصويت ب: ساعة الحائط تشير إلى 10:40، وعلى طاولة التسجيل ورقتان وقلم وكاتبة التسجيل تسجّل توقيع ناخب.\nلا يظهر عمر الناصر في الصورة.",
  ["a_get_photo_1040"], ["f_photo_1040_exists", "f_roll_swept"], "strong",
  "لقطة واحدة في لحظة واحدة؛ تثبت وجود ورقتين على الطاولة ولا تثبت أنهما الكشف نفسه إلا بمقارنتها بالتوقيعات.", loc="loc_hall")
V("ev_photo_1110", "صورة المعلمة للقاعة بعد الترتيب", "digital",
  "هاتف المعلمة — بيانات الصورة: الأربعاء 11:07\nطاولة التسجيل فارغة إلا من قلم؛ وفي طرف الصورة متطوعة بسترة زرقاء تحمل صندوقاً أزرق نحو الباب.",
  ["a_get_photo_1110"], ["f_photo_1110_exists", "f_roll_swept"], "moderate",
  "لقطة بعد الواقعة؛ تبيّن خلو الطاولة وحمل صندوق ولا ترى محتواه.", loc="loc_hall")
V("ev_tidy_roster", "ورقة توزيع المتطوعين", "documentary",
  "قاعة التصويت ب — مهام المتطوعين (بتوقيع ر. الحلبي)\n09:00–11:00 استقبال الناخبين\n11:00–11:10 ترتيب طاولة التسجيل وجمع الأوراق في صندوق التدوير: ريم الشامي\n11:10 إعادة ترتيب الكراسي",
  ["a_get_tidy_roster"], ["f_tidy_roster_exists", "f_roll_swept"], "moderate",
  "ورقة مهام لا تسجّل ما حدث فعلاً؛ تبيّن من كُلّف بالترتيب ووقته.", loc="loc_hall")
V("ev_motive_note", "محضر الاجتماع السابق", "documentary",
  "محضر لجنة الانتخاب — الاثنين\nعمر الناصر: «أعترض على تعليق كشف الناخبين علناً لأن فيه أسماء الطلاب.»\nقرار اللجنة: يُعلَّق الكشف في القاعة فقط. عمر: «أقبل القرار.»",
  ["a_get_motive_note"], ["f_omar_objected"], "moderate",
  "يبيّن اعتراضاً سابقاً وقبولاً للقرار؛ الاعتراض على سياسة ليس أخذاً لورقة.", red=True, loc="loc_hall")
V("ev_omar_stmt", "إفادة عمر (ملخص)", "testimonial",
  "ملخص إفادة عمر الناصر:\n«كنت في المكتبة أطبع ملصقاتي قرابة العاشرة، وعدت بعد العاشرة والنصف ووقفت في الصف. لم ألمس الكشف.»",
  ["a_note_omar"], ["f_omar_says"], "weak",
  "إفادة المتهم عن نفسه؛ لا يدل انفعاله ولا هدوؤه على شيء، وتُقاس بسجلات لا يكتبها.", loc="loc_hall")
V("ev_reem_stmt", "إفادة ريم (ملخص)", "testimonial",
  "ملخص إفادة ريم الشامي:\n«في الحادية عشرة جمعت الأوراق المتناثرة عن الطاولة ووضعتها في الصندوق الأزرق. ظننتها مسودات ولم أفحصها.»",
  ["a_note_reem"], ["f_reem_stacked"], "moderate",
  "إفادة صادقة بسوء تقدير؛ يؤيدها بطاقة الصندوق وصورة المعلمة ولا تغني عنهما.", loc="loc_hall")

I("i_source_a", [E("ev_stmt_karam"), E("ev_stmt_dina")], "fact", "f_same_source", "establishes", "strong",
  "روايتان من شاهدين منفصلين لا تتفقان عادة في كل كلمة، وهما هنا متطابقتان حرفاً بحرف بما فيهما وصف لا يتوقعه مشاهد (الاتجاه نحو السلم)؛ فهما نسخة واحدة لا شهادتان.", ["KO-RS-05-004", "KO-RS-05-009"])
I("i_source_b", [E("ev_group_msg"), E("ev_read_receipts")], "fact", "f_same_source", "establishes", "strong",
  "الصياغة نفسها نُشرت 10:58 ونقلاً عن «أحدهم»، وفتحها كرم 11:03 ودينا 11:06، ثم استُدعيا 11:35؛ فسبقت الصياغة الإفادتين وبلغتهما.", ["KO-RS-05-004", "KO-FC-04-024"])
I("i_swept_a", [E("ev_roll_entries"), E("ev_crate_tag")], "fact", "f_roll_swept", "establishes", "strong",
  "الكشف وُقّع عليه حتى 10:48، أي بعد الوقت المنسوب إلى أخذه، ثم وُجد في صندوق تدوير جُمع من القاعة 11:30 بين أوراق مسودات؛ فانتقل من الطاولة إلى الصندوق بين الوقتين.", ["KO-RS-05-014", "KO-RS-06-017"])
I("i_swept_b", [E("ev_photo_1040"), E("ev_photo_1110"), E("ev_tidy_roster")], "fact", "f_roll_swept", "establishes", "strong",
  "ورقتان على الطاولة بعد منتصف الصباح، ثم طاولة فارغة ومتطوعة تحمل صندوقاً، وورقة المهام تكلف متطوعة بجمع الأوراق في الصندوق في تلك الدقائق؛ ثلاث وثائق مستقلة عن الشاهدين.", ["KO-RS-05-004", "KO-RS-06-017"])
I("i_cl_omar", [Fa("f_same_source"), Fa("f_roll_swept")], "claim", "cl_omar_took", "contradicts_claim", "strong",
  "ما نُقل عن رسالة واحدة لا يُحسب مشاهدة، والكشف كان على الطاولة قيد الاستعمال بعد الوقت المنسوب إلى أخذه.", ["KO-RS-05-014", "KO-RS-06-020"])
I("i_cl_reem", [Fa("f_roll_swept")], "claim", "cl_reem_only_scrap", "contradicts_claim", "strong",
  "وُجد في الصندوق الذي وضعت فيه أوراقاً غير مسودات.", ["KO-RS-05-014"])
I("i_support_reem", [Fa("f_roll_swept"), Fa("f_same_source")], "hypothesis", "h_reem", "supports", "strong",
  "الكشف ظل قيد الاستعمال ثم انتقل إلى الصندوق في تلك الدقائق، وقصة الأخذ المنسوبة إلى عمر نبعت من رواية واحدة منسوخة.", ["KO-RS-06-007"])
I("i_rule_omar", [Fa("f_roll_swept"), Fa("f_same_source")], "hypothesis", "h_omar", "rules_out", "conclusive",
  "لا شاهد مستقل على أخذه، والكشف بقي على الطاولة بعد الوقت المنسوب إليه؛ والتحذير المنشور في المجموعة لا يثبت فعلاً.", ["KO-RS-06-008"])
I("i_rule_sabotage", [Fa("f_roll_swept"), Fa("f_same_source")], "hypothesis", "h_sabotage", "rules_out", "strong",
  "الكشف لم يخرج من القاعة بل وُجد بين أوراق التدوير بعد الترتيب، فلا أثر لأخذ مقصود لتعطيل التصويت.", ["KO-RS-06-008"])
I("i_rule_conspiracy", [Fa("f_same_source"), Fa("f_roll_swept")], "hypothesis", "h_conspiracy", "rules_out", "suggestive",
  "تطابق إفادتين مع رسالة علنية يفسّره النسخ دون اتفاق مسبق، ولا قرينة على تواطؤ؛ والمهم أن الكشف لم يؤخذ أصلاً.", ["KO-RS-06-008"])

ck = [
    {"character_id": "omar", "knows": [K("f_omar_says"), K("f_omar_objected")], "hides": [], "believes": []},
    {"character_id": "reem", "knows": [K("f_reem_stacked")], "hides": [], "believes": [{"claim_id": "cl_reem_only_scrap", "stance": "sincere"}]},
    {"character_id": "karam", "knows": [K("f_karam_says"), K("f_group_msg_exists", "witnessed", "unsure")], "hides": [], "believes": [{"claim_id": "cl_omar_took", "stance": "sincere"}]},
    {"character_id": "dina", "knows": [K("f_dina_says"), K("f_read_receipts_exist", "professional")], "hides": [], "believes": [{"claim_id": "cl_omar_took", "stance": "sincere"}]},
    {"character_id": "lina", "knows": [K("f_lina_says", "witnessed", "fairly_sure")], "hides": [], "believes": []},
    {"character_id": "nadim", "knows": [K("f_photo_1040_exists", "professional")], "hides": [], "believes": []},
    {"character_id": "rula", "knows": [K("f_roll_recovered", "professional"), K("f_tidy_roster_exists", "professional"), K("f_photo_1110_exists", "professional")], "hides": [], "believes": []},
    {"character_id": "hamza", "knows": [K("f_crate_record_exists", "professional")], "hides": [], "believes": []},
]
hyps = [
    {"id": "h_omar", "statement_ar": "أخذ عمر الكشف عن الطاولة وخرج به كما قال الشاهدان.", "is_true": False, "plausibility_at_start": "high", "suspect_id": "omar"},
    {"id": "h_conspiracy", "statement_ar": "اتفق كرم ودينا عمداً على اتهام عمر بالكذب.", "is_true": False, "plausibility_at_start": "medium"},
    {"id": "h_reem", "statement_ar": "لم يأخذ أحد الكشف عمداً، بل جُمع مع أوراق الترتيب ووُضع في صندوق التدوير.", "is_true": True, "plausibility_at_start": "low", "suspect_id": "reem"},
    {"id": "h_sabotage", "statement_ar": "أخذ شخص ما الكشف عمداً ليعطّل التصويت.", "is_true": False, "plausibility_at_start": "medium"},
]
mis = [
    {"id": "rh_two", "points_to_hypothesis_id": "h_omar", "planted_via_ar": "شاهدان يقولان الشيء نفسه عن عمر.", "evidence_ids": ["ev_stmt_karam", "ev_stmt_dina", "ev_incident_report"],
     "refuted_by_inference_ids": ["i_source_a", "i_source_b", "i_rule_omar"],
     "fairness_note_ar": "نصّا الإفادتين متطابقان حرفاً، ورسالة المجموعة وقائمة الفتح بين يدي اللاعب؛ فهما مصدر واحد لا اثنان."},
    {"id": "rh_objection", "points_to_hypothesis_id": "h_omar", "planted_via_ar": "عمر اعترض على تعليق الكشف علناً.", "evidence_ids": ["ev_motive_note"],
     "refuted_by_inference_ids": ["i_rule_omar", "i_swept_a"],
     "fairness_note_ar": "المحضر نفسه يذكر أنه قبل القرار؛ والاعتراض على سياسة لا يدل على أخذ ورقة."},
    {"id": "rh_dispute", "points_to_hypothesis_id": "h_conspiracy", "planted_via_ar": "إفادة لينا تختلف عن إفادتي كرم ودينا في الوقت والمضمون.", "evidence_ids": ["ev_stmt_lina"],
     "refuted_by_inference_ids": ["i_rule_conspiracy", "i_swept_b"],
     "fairness_note_ar": "الاختلاف في الزاوية والوقت بين شاهدين مستقلين أمر عادي؛ إفادة لينا بريئة وتوافق ورقة المهام."},
]
los = std_los("يفرّق بين شهادتين مستقلتين وروايتين متطابقتين حرفياً: التطابق الكامل في الألفاظ وفي تفصيل خاطئ يدل على مصدر مشترك، والاختلاف البريء في الزاوية والوقت علامة استقلال.", "KO-RS-05-004",
              ["يقارن الإفادات كلمة بكلمة", "يبحث عن مصدر سابق للصياغة", "لا يعدّ كل اختلاف كذباً"])
ref = ("لا دليل مستقل على أن عمر أخذ الكشف. إفادتا كرم ودينا متطابقتان حرفاً بحرف، حتى في وصف الاتجاه نحو السلم، وهما تطابقان رسالة نُشرت قبلهما وفتحاها قبل الاستدعاء؛ فهما رواية واحدة نُسخت. والكشف المسترجع يحمل توقيعات ناخبين حتى 10:48، فكان على الطاولة بعد الوقت المنسوب إلى أخذه، وصورة 10:40 تؤيد ذلك، ثم جُمع مع أوراق الترتيب في صندوق تدوير وجد فيه بعد جمعه. ورقة المهام وصورة المعلمة وإفادة لينا تتفق على أن متطوعة رتبت الطاولة في ذلك الوقت. حدود الاستنتاج: لا نعرف بالضبط متى وضعته ريم، ولا نعرف من هو «أحدهم» في الرسالة، ولا يفيد الاعتراف عن شيء في غياب السجلات.")
hints = [
    H("hg1", 1, "metacognitive", "حين تتفق روايتان في كل كلمة، اسأل: هل رأى كل منهما الحدث وحده، أم قرأ كلاهما شيئاً واحداً؟", {"always": True}, None, 0.02),
    H("hg2", 2, "focus_area", "قارن إفادتي الشاهدين حرفاً بحرف، ثم قارن أوقات تدوينهما بأي رسالة سبقتهما.", he("ev_incident_report"), None, 0.04),
    H("hg3", 3, "pointer", "ابحث عن سجل لا يملكه الشاهدان: ورقة الكشف نفسها، وصورة بساعة ظاهرة، وبطاقة صندوق.", he("ev_incident_report"), None, 0.08),
    H("hs1", 1, "metacognitive", "هل أنهت الرسالة نصها قبل أن يُسأل الشاهدان؟", he("ev_stmt_karam"), "i_source_b", 0.02),
    H("hs2", 2, "pointer", "اسأل عن رسالة في مجموعة الصف، ثم عمّن فتحها ومتى.", he("ev_stmt_karam"), "i_source_b", 0.06),
    H("hw1", 1, "metacognitive", "لو أخذ عمر الكشف 10:15، فلماذا فيه توقيعات بعد ذلك؟", he("ev_incident_report"), "i_swept_a", 0.02),
    H("hw2", 2, "pointer", "اطلب الكشف المسترجع من المعلمة وانظر إلى أوقات التوقيع الأخيرة.", he("ev_incident_report"), "i_swept_a", 0.06),
]
Act("a_read_report", "examine", "اقرأ بلاغ فقدان الكشف", al, [G("ev_incident_report")], "loc_hall", "READ_REPORT")
interviews([("omar", "عمر"), ("reem", "ريم"), ("karam", "كرم"), ("dina", "دينا"), ("lina", "لينا"), ("nadim", "نديم"), ("rula", "رولا"), ("hamza", "حمزة")])
Act("a_note_karam", "examine", "دوّن إفادة كرم", fu("f_karam_says"), [G("ev_stmt_karam")], "karam", "NOTE_KARAM")
Act("a_note_dina", "examine", "دوّن إفادة دينا", fu("f_dina_says"), [G("ev_stmt_dina")], "dina", "NOTE_DINA")
Act("a_note_lina", "examine", "دوّن إفادة لينا", fu("f_lina_says"), [G("ev_stmt_lina")], "lina", "NOTE_LINA")
Act("a_note_omar", "examine", "دوّن إفادة عمر", fu("f_omar_says"), [G("ev_omar_stmt")], "omar", "NOTE_OMAR")
Act("a_note_reem", "examine", "دوّن إفادة ريم", fu("f_reem_stacked"), [G("ev_reem_stmt")], "reem", "NOTE_REEM")
get("ev_group_msg", "اطلب رسالة مجموعة الصف", fu("f_group_msg_exists"), "loc_hall")
get("ev_read_receipts", "اطلب قائمة من فتح الرسالة", fu("f_read_receipts_exist"), "loc_hall", "GET_RECEIPTS")
get("ev_roll_entries", "اطلب الكشف المسترجع", fu("f_roll_recovered"), "loc_hall", "GET_ROLL")
get("ev_crate_tag", "اطلب بطاقة صندوق التدوير", fu("f_crate_record_exists"), "loc_yard", "GET_CRATE")
get("ev_photo_1040", "اطلب صورة القاعة نحو 10:40", fu("f_photo_1040_exists"), "loc_hall", "GET_PHOTO1")
get("ev_photo_1110", "اطلب صورة المعلمة بعد الترتيب", fu("f_photo_1110_exists"), "loc_hall", "GET_PHOTO2")
get("ev_tidy_roster", "اطلب ورقة توزيع المتطوعين", fu("f_tidy_roster_exists"), "loc_hall", "GET_ROSTER")
get("ev_motive_note", "اطلب محضر الاجتماع السابق", fu("f_omar_objected"), "loc_hall", "GET_MOTIVE")
tail_actions()
topics = [
    {"id": "t_says_k", "label_ar": "ما رأيته", "example_questions_ar": ["ماذا رأيت؟", "ماذا قلت للمعلمة؟"], "fact_ids": ["f_karam_says"]},
    {"id": "t_msg", "label_ar": "رسالة في مجموعة الصف", "example_questions_ar": ["هل قرأت شيئاً قبل الإفادة؟"], "fact_ids": ["f_group_msg_exists"]},
    {"id": "t_says_d", "label_ar": "ما قلته للمعلمة", "example_questions_ar": ["ماذا قلتِ؟"], "fact_ids": ["f_dina_says"]},
    {"id": "t_receipts", "label_ar": "فتح الرسائل", "example_questions_ar": ["هل تُظهر المجموعة من فتح الرسالة؟"], "fact_ids": ["f_read_receipts_exist"]},
    {"id": "t_lina", "label_ar": "ما رأيته قرابة الحادية عشرة", "example_questions_ar": ["ماذا رأيتِ؟"], "fact_ids": ["f_lina_says"]},
    {"id": "t_omar_where", "label_ar": "أين كنت قرابة العاشرة", "example_questions_ar": ["أين كنت؟"], "fact_ids": ["f_omar_says"]},
    {"id": "t_objection", "label_ar": "اعتراضك السابق", "example_questions_ar": ["هل اعترضت على شيء؟"], "fact_ids": ["f_omar_objected"]},
    {"id": "t_tidy", "label_ar": "ترتيب الطاولة", "example_questions_ar": ["ماذا فعلتِ عند الترتيب؟"], "fact_ids": ["f_reem_stacked"]},
    {"id": "t_scrap", "label_ar": "ما رميتِه", "example_questions_ar": ["هل فحصتِ الأوراق؟"], "fact_ids": [], "claim_ids": ["cl_reem_only_scrap"]},
    {"id": "t_photo1", "label_ar": "صورة نحو 10:40", "example_questions_ar": ["هل صوّرت القاعة؟"], "fact_ids": ["f_photo_1040_exists"]},
    {"id": "t_roll", "label_ar": "الكشف المسترجع", "example_questions_ar": ["أين الكشف الآن؟"], "fact_ids": ["f_roll_recovered"]},
    {"id": "t_roster", "label_ar": "ورقة المهام", "example_questions_ar": ["من كُلّف بالترتيب؟"], "fact_ids": ["f_tidy_roster_exists"]},
    {"id": "t_photo2", "label_ar": "صورة بعد الترتيب", "example_questions_ar": ["هل صوّرت القاعة بعد الترتيب؟"], "fact_ids": ["f_photo_1110_exists"]},
    {"id": "t_crate", "label_ar": "بطاقات الصناديق", "example_questions_ar": ["ماذا تدوّن على البطاقة؟"], "fact_ids": ["f_crate_record_exists"]},
    {"id": "t_belief", "label_ar": "ما رأيك في الاتهام", "example_questions_ar": ["هل أنت متأكد مما رأيت؟"], "fact_ids": [], "claim_ids": ["cl_omar_took"]},
]
# claim "cl_omar_took" is voiced by none of the authored lines: add a line for Karam through the topic
for c in chars:
    if c["id"] == "karam":
        c["authored_lines"].insert(3, L("kr_belief", "reveal", "أنا متأكد أن عمر هو من أخذ الكشف.", None, ["cl_omar_took"]))
steps = [
    (1, "قارن الإفادتين حرفاً بحرف: الجملة نفسها بالألفاظ نفسها، بما فيها وصف الاتجاه نحو السلم؛ شاهدان مستقلان لا يتفقان في كل كلمة.", ["ev_stmt_karam", "ev_stmt_dina"], "i_source_a"),
    (2, "ثم ابحث عمّا سبقهما: رسالة المجموعة 10:58 نصّها هو نصّ الإفادتين، وقد فتحها كرم 11:03 ودينا 11:06 قبل أن يُستدعيا.", ["ev_group_msg", "ev_read_receipts"], "i_source_b"),
    (3, "الكشف نفسه يروي: توقيعات الناخبين حتى 10:48 بعد الوقت المنسوب إلى أخذه، ثم وُجد في صندوق التدوير بين المسودات.", ["ev_roll_entries", "ev_crate_tag"], "i_swept_a"),
    (4, "مسار ثانٍ: صورة 10:40 فيها ورقتان على الطاولة، وصورة 11:07 فيها طاولة فارغة ومتطوعة بصندوق، وورقة المهام تكلف ريم بجمع الأوراق.", ["ev_photo_1040", "ev_photo_1110", "ev_tidy_roster"], "i_swept_b"),
    (5, "إفادة لينا تختلف زمناً ومضموناً وهي بريئة؛ واعتراض عمر السابق على السياسة لا يعني أخذ الورقة.", ["ev_stmt_lina", "ev_motive_note"], "i_rule_omar"),
]
alt = ["يمكن إثبات حلقة المصدر المشترك بالإفادتين وحدهما بعد مقارنتهما، أو برسالة المجموعة وقائمة الفتح وحدهما؛ والأقوى أن يتفقا.",
       "ويمكن إثبات بقاء الكشف على الطاولة ثم انتقاله بالكشف المسترجع وبطاقة الصندوق، أو بالصورتين وورقة المهام؛ والأقوى أن يتفق المساران."]
notlimits = ["لا نعرف بدقة متى وضعت ريم الكشف في الصندوق ولا هل رأته؛ تكفي إفادتها وبطاقة الصندوق والصورتان لترجيح أنه وُضع مع أوراق الترتيب.",
             "لا نعرف من هو «أحدهم» الذي نقلت عنه الرسالة، ولا إن كان قصد الإساءة.",
             "لا يثبت تطابق الإفادتين أن الطالبين كذبا؛ الأرجح أنهما صدّقا ما قرآه وظنّا أنهما شاهداه."]
notes = ["إفادتان تتطابقان في كل كلمة، وفي تفصيل لا يتوقعه المشاهد، تدلان على مصدر واحد لا على مشاهدتين. المشاهدات المستقلة تختلف في الزاوية والوقت والألفاظ، وهذا الاختلاف علامة استقلال لا كذب.",
         "الذاكرة تمتزج بما نقرؤه بعد الحدث: قد يتذكر الشخص جملة قرأها كأنه رآها، ولا يعني ذلك أنه يكذب؛ ولهذا نسأل أولاً: أي مصدر سبق هذه الصياغة؟",
         "الحسم هنا بسجلات لا تعتمد على أي شاهد: ورقة الكشف بأوقات توقيعاتها، وصورتان بساعتين ظاهرتين، وبطاقة صندوق، وورقة مهام.",
         "لا أحد يضغط على أحد في هذه القضية ولا يُنتزع اعتراف؛ تُقرأ الإفادات كل على حدة وبعد ذلك تُقارن، وهذه ممارسة حديثة سليمة.",
         "لا أحد مذنب بقصد: ريم أخطأت التقدير، وكرم ودينا صدّقا رسالة، وعمر دفع ثمن شائعة. والإصلاح تعليمي: يُفحص ما يوضع في صناديق التدوير، وتُسأل المشاهدة قبل أن تُردد.",
         "بطاقة الأصل: القضية أصلية من ATHAR على بنية «فرّق بين الشهود» في مكتبة الحالات، وتُستعار منها قراءة الإفادات المنفصلة فقط."]
premise = {"hook_ar": "شاهدان يقولان الجملة نفسها بالحرف عن عمر. هل هذا يعني أنهما صادقان، أم أنهما سمعاها من مكان واحد؟",
           "player_role_ar": "أنت عضو في لجنة الطعون بمجلس الطلاب في مدرسة القنطرة، وطُلب منك رأي معلّل في فقدان كشف الناخبين، دون اتهام أحد قبل أن تثبت السجلات شيئاً.",
           "setting_ar": "مدرسة القنطرة، صباح الأربعاء يوم انتخاب مجلس الطلاب. الأوقات بساعة المدرسة.",
           "public_fact_ids": ["f_roll_missing", "f_omar_accused"],
           "assumed_general_knowledge_ar": ["الشاهدان المستقلان لا يتفقان عادة في كل كلمة", "الاختلاف البريء في التفاصيل لا يعني الكذب", "ما نقرؤه بعد الحدث قد يختلط في الذاكرة بما رأيناه"]}
meta = {"title_ar": "شهادتان بكلمات واحدة", "title_en": "Two Statements in the Same Words", "age_band": "13-15", "estimated_minutes": 30, "difficulty": 2,
        "content_flags": ["no_violence"],
        "knowledge_object_refs": ["KO-RS-05-004", "KO-RS-05-009", "KO-RS-05-014", "KO-RS-06-017", "KO-RS-06-020", "KO-FC-04-024", "KO-RS-05-001", "KO-RS-06-001", "KO-RS-06-008", "KO-RS-06-021", "KO-RS-06-009", "KO-RS-05-002", "KO-RS-05-005"]}
ui = {
    "clock": {"epoch_hhmm": "09:00", "zone_label_ar": "ساعة المدرسة"},
    "cover": {"title_ar": "شهادتان بكلمات واحدة", "tagline_ar": "إذا اتفق الشاهدان في كل كلمة، فهل رأيا معاً؟", "kicker_ar": "الملف التاسع والعشرون · استقلال الشهود", "glyph": "❝", "accent": "cyan"},
    "cold_open_ar": ["الأربعاء، 11:20.", "اختفى كشف الناخبين من طاولة التسجيل. قال طالبان إنهما رأيا عمر يأخذه، وبالجملة نفسها حرفاً بحرف.", "وعمر يقول إنه كان في المكتبة. والمجموعة كلها تهمس: لا دخان بلا نار.",
                    "قبل أي حكم: هل هما شاهدان أم شاهد واحد مرتين؟ وما الورقة التي لا تملكها أي شهادة؟"],
    "limit_menu": [
        {"id": "l_when_put", "label_ar": "لا نعرف بدقة متى وضعت ريم الكشف في الصندوق ولا هل رأته"},
        {"id": "l_who_said", "label_ar": "لا نعرف من هو «أحدهم» الذي نقلت عنه الرسالة"},
        {"id": "l_not_lie", "label_ar": "التطابق الحرفي لا يعني أن الطالبين كذبا، فالأرجح أنهما صدّقا ما قرآه"},
        {"id": "l_invalid_two", "label_ar": "اتفاق شاهدين على الجملة نفسها يقوّي الاتهام"},
        {"id": "l_invalid_diff", "label_ar": "اختلاف لينا عن الآخرين يدل على أنها كاذبة"},
        {"id": "l_invalid_angry", "label_ar": "انفعال عمر يدل على أنه أخذ الكشف"}],
    "mind_change_menu": [
        {"id": "m_independent", "label_ar": "ظهور أن كرم ودينا لم يفتحا الرسالة قبل الإفادة وأنهما كتبا ما رأياه وحدهما"},
        {"id": "m_roll_before", "label_ar": "ظهور أن توقيعات الكشف انتهت قبل 10:15"},
        {"id": "m_crate_other", "label_ar": "ظهور أن الكشف وُجد في موضع آخر لا علاقة له بالترتيب"},
        {"id": "m_popular", "label_ar": "كثرة من يرددون أن عمر هو الفاعل"}],
    "transfer": {
        "id": "tr_two_notes", "title_ar": "اختبار نقل المهارة: ورقة المسابقة",
        "scenario_ar": "اختفت ورقة نتائج مسابقة، وقالت طالبتان إنهما رأتا زميلاً يأخذها. أمامك وثيقتان من واقعة خيالية لا علاقة لها بالقضية.",
        "documents": [
            {"title_ar": "إفادتان مدونتان", "body_ar": "الطالبة الأولى: «رأيت زياد يطوي ورقة النتائج ويضعها في حقيبته الصفراء ويمضي نحو الباب الخلفي.»\nالطالبة الثانية: «رأيت زياد يطوي ورقة النتائج ويضعها في حقيبته الصفراء ويمضي نحو الباب الخلفي.»"},
            {"title_ar": "سجل المجموعة", "body_ar": "رسالة 12:05 في مجموعة الصف: «قيل لي إن زياداً طوى ورقة النتائج ووضعها في حقيبته الصفراء ومضى نحو الباب الخلفي.»\nأُدلي بالإفادتين 12:30."}],
        "prompt_ar": "اختر الخطوات الصالحة لتقدير قيمة الإفادتين (يمكنك اختيار أكثر من خطوة).",
        "options": [
            {"id": "o1", "text_ar": "ملاحظة أن الإفادتين متطابقتان حرفاً بحرف في وصف لا يتوقعه شاهد مستقل"},
            {"id": "o2", "text_ar": "مقارنة وقت الرسالة بوقت الإفادتين ومعرفة من فتحها"},
            {"id": "o3", "text_ar": "البحث عن سجل لا يعتمد على الطالبتين: ورقة النتائج أو صورة أو سجل باب"},
            {"id": "o4", "text_ar": "عدّ الإفادتين رواية واحدة منسوخة حتى يثبت العكس"},
            {"id": "o5", "text_ar": "اعتبار اتفاق الطالبتين دليلاً قاطعاً على أخذ زياد"},
            {"id": "o6", "text_ar": "الحكم بأن الطالبتين كاذبتان لأن الصياغة واحدة"},
            {"id": "o7", "text_ar": "ضغط المعلمة عليهما لتغيير كلامهما"}],
        "free_text_prompt_ar": "اكتب في ثلاثة أسطر كيف تقدّر نسبة الترجيح بأن زياداً أخذ الورقة.",
    },
    "skills": [{"skill_id": "KO-RS-05-004", "track": "B"}, {"skill_id": "KO-RS-05-009", "track": "B"}, {"skill_id": "KO-RS-06-017", "track": "B"}, {"skill_id": "KO-RS-05-002", "track": "D"}],
    "stage_hooks_ar": {"briefing": "جملة واحدة بحروفها من فمين… فأين مصدرها؟", "investigating": "اقرأ كل إفادة وحدها، ثم قارنها بحرفها.", "review": "قبل أن تغلق الملف: ما الذي لا تعرفه عن صاحب الرسالة؟", "resolved": "أُغلق الملف. عاد الكشف، وبقي درس عن الجملة التي تُنقل بلا مصدر."},
    "character_glyphs": {"omar": "ع", "reem": "ر", "karam": "ك", "dina": "د", "lina": "ل", "nadim": "ن", "rula": "ر", "hamza": "ح"},
}
sc = {
    "accepted_conclusions": {
        "h_reem": {"grade": 1, "note_ar": "استنتاج متسق مع الأدلة ويتطلب ذكر حدوده."},
        "h_omar": {"grade": 0, "note_ar": "يعدّ شهادتين منسوختين شهادتين مستقلتين، ويتجاهل أن الكشف كان قيد الاستعمال بعد الوقت المنسوب إليه."},
        "h_conspiracy": {"grade": 0, "note_ar": "يفترض اتفاقاً عمدياً بلا قرينة؛ الأرجح أنهما صدّقا رسالة قرآها."},
        "h_sabotage": {"grade": 0, "note_ar": "الكشف لم يخرج من القاعة بل وُجد بين أوراق التدوير."}},
    "confidence_band": {"h_reem": [65, 90], "h_omar": [0, 15], "h_conspiracy": [0, 20], "h_sabotage": [0, 20]},
    "source_key": {"ev_incident_report": "claim", "ev_stmt_karam": "claim", "ev_stmt_dina": "claim", "ev_stmt_lina": "claim", "ev_group_msg": "primary_record", "ev_read_receipts": "primary_record",
                   "ev_roll_entries": "primary_record", "ev_crate_tag": "primary_record", "ev_photo_1040": "primary_record", "ev_photo_1110": "primary_record", "ev_tidy_roster": "primary_record",
                   "ev_motive_note": "primary_record", "ev_omar_stmt": "claim", "ev_reem_stmt": "claim"},
    "link_key": {
        "h_reem": {"ev_roll_entries": "supports", "ev_crate_tag": "supports", "ev_photo_1040": "supports", "ev_photo_1110": "supports", "ev_tidy_roster": "supports", "ev_stmt_lina": "supports",
                   "ev_reem_stmt": "supports", "ev_group_msg": "neutral", "ev_read_receipts": "neutral"},
        "h_omar": {"ev_incident_report": "supports", "ev_stmt_karam": "supports", "ev_stmt_dina": "supports", "ev_motive_note": "supports", "ev_roll_entries": "weakens", "ev_crate_tag": "weakens",
                   "ev_photo_1040": "weakens", "ev_group_msg": "weakens", "ev_read_receipts": "weakens"},
        "h_conspiracy": {"ev_stmt_karam": "supports", "ev_stmt_dina": "supports", "ev_group_msg": "weakens", "ev_read_receipts": "weakens", "ev_stmt_lina": "neutral"},
        "h_sabotage": {"ev_incident_report": "supports", "ev_crate_tag": "weakens", "ev_roll_entries": "weakens", "ev_photo_1110": "weakens", "ev_tidy_roster": "weakens"},
    },
    "required_limits": ["l_when_put", "l_not_lie"], "valid_mind_changers": ["m_independent", "m_roll_before", "m_crate_other"],
    "invalid_limits": ["l_invalid_two", "l_invalid_diff", "l_invalid_angry"],
    "decisive_evidence": ["ev_stmt_karam", "ev_stmt_dina", "ev_group_msg", "ev_read_receipts", "ev_roll_entries", "ev_crate_tag", "ev_photo_1040", "ev_photo_1110", "ev_tidy_roster"],
    "timeline_requirement": [{"evidence_id": "ev_photo_1040", "utc_minute": 100, "tol": 4}, {"evidence_id": "ev_group_msg", "utc_minute": 118, "tol": 4}, {"evidence_id": "ev_photo_1110", "utc_minute": 127, "tol": 4},
                             {"evidence_id": "ev_crate_tag", "utc_minute": 150, "tol": 8}, {"evidence_id": "ev_stmt_dina", "utc_minute": 160, "tol": 6}],
    "refuted_hypotheses": ["h_omar", "h_conspiracy", "h_sabotage"],
    "transfer_key": {"valid": ["o1", "o2", "o3", "o4"], "invalid": ["o5", "o6", "o7"]},
}
assemble(CID, meta, premise, {"characters": chars, "locations": locations, "objects": objects, "organizations": orgs}, ["reem"],
         "لم يأخذ عمر الكشف. إفادتا كرم ودينا نسخة من رسالة واحدة سبقتهما، وبقي الكشف على الطاولة قيد الاستعمال بعد الوقت المنسوب إلى أخذه، ثم جمعته ريم مع أوراق الترتيب ووضعته في صندوق التدوير دون قصد.",
         ["f_same_source", "f_roll_swept"], claims, timeline, ck, hyps, mis, los, ref, hints, topics, steps, alt, notlimits, notes, ui, sc)
