#!/usr/bin/env python3
# Case c026 «الصندوق في الدرج الأيمن» — chain of custody (سلسلة العهدة). Archetype ARC-32 «الدليل المدسوس» (library), rebuilt as an original
# ATHAR story with humans only and no instruction on how to plant anything. Teaches: where an item is FOUND does not say who PUT it there;
# read the custody record entry by entry and find the span no signature covers; get an independent record for each person (door reader,
# gate, signed attendance sheet, night-round notebook); a finder with a grudge is a reason to look for evidence that does not depend on him.
# No-culprit-style convention: Hadi (a student who borrowed the box without signing and then panicked) is recorded in culprit_ids; nobody
# acted maliciously. Time lab omitted by instruction (labs: []); a timeline requirement is used. Calendar (fictional): minute 0 = Monday 14:00.
# Tue 07:30 = 1050. All names, places and records are fictional.
# Usage: gen_c026.py OUT_DIR
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
      "rubric": rubric(ref), "hint_ladder": hints,
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

# ---- header notes (kept at top of generated file)
CID = "c026_lens_box"
# ---------------------------------------------------------------- characters
ch("rashid", "رشيد الحداد", "suspect", "مشرف نادي المنظار الفلكي في المدرسة",
   "هادئ ودقيق ومتعب من كثرة المهام، يجيب عمّا يعرفه ويقول «لا أعرف» حين لا يعرف. يستاء من الاتهام لكنه لا يردّ عليه بالاتهام.",
   ["أن يبقى النادي مفتوحاً للطلاب", "ألا يُحكم عليه لأن الصندوق وُجد في مكتبه"],
   [L("rs_greet", "greeting", "أنا مشرف النادي منذ ثلاث سنوات. اسأل عمّا تشاء."),
    L("rs_away", "reveal", "قضيت ظهر الاثنين في يوم تدريب لمعلمي العلوم في مدرسة أخرى، وعدت إلى بيتي بعده، وجئت إلى مدرستنا صباح الثلاثاء.", ["f_rashid_says_away"]),
    L("rs_budget", "reveal", "نعم، كتبت للنادي أننا لن نشتري عدسات جديدة هذا الفصل، فالميزانية لا تكفي، ولم أقل إننا سنستغني عن القديمة.", ["f_budget_refusal"]),
    L("rs_unknown", "deflect_unknown", "لا أعرف أكثر من هذا."),
    L("rs_off", "deflect_offtopic", "اسألني عن النادي والعدسات."),
    L("rs_bye", "farewell", "أريد العدسات في مكانها أكثر مما تريد أنت.")])
ch("mazen", "مازن الصيرفي", "suspect", "طالب في الصف الحادي عشر، عضو في النادي",
   "حاد في كلامه ويسبق الأدلة بالأحكام، وكان قد اختلف مع المشرف على موعد الرصد. يصحّح قوله إذا رأى سجلاً يخالفه ولا يتمسك به عناداً.",
   ["أن تعود العدسات", "أن يُسمَع رأيه"],
   [L("mz_greet", "greeting", "أنا من وجد الصندوق. وأقول إن الأمر واضح."),
    L("mz_found", "reveal", "فتحت الدرج الأيمن لمكتب المشرف صباح الثلاثاء لأضع ورقة موعد الرصد، فرأيت الصندوق، وصوّرته بهاتفي قبل أن ألمسه.", ["f_mazen_photo", "f_mazen_says_found"]),
    L("mz_posts", "reveal", "هادي نشر مساء الاثنين صور معرض المدرسة على صفحة النادي، ولا أظن أن لذلك علاقة بالموضوع.", ["f_exhibit_posts_public"]),
    L("mz_rumour", "reveal", "المشرف هو الوحيد الذي يملك الدرج، فلا بد أنه أخذها ليتخلص من مشكلة تجديد العدسات.", None, ["cl_mazen_sup"]),
    L("mz_unknown", "deflect_unknown", "لم أكن هناك."),
    L("mz_off", "deflect_offtopic", "اسألني عن الدرج والصندوق."),
    L("mz_bye", "farewell", "إن ظهر ما يخالف قولي فسأقولها بلا تردد.")])
ch("hadi", "هادي الشامي", "suspect", "طالب في الصف العاشر، مصوّر النادي",
   "مجتهد وخجول، يخاف أن يُنسب إليه الخطأ فيسكت أو يؤجل. لا يكره أحداً، ويقول الحقيقة حين يرى أن السجلات قالتها.",
   ["أن يُنهي صور المعرض", "ألا يُحرَج أمام زملائه"],
   [L("hd_greet", "greeting", "أنا أصوّر للنادي فقط. لا أعرف لماذا استُدعيت."),
    L("hd_deny", "reveal", "لم أدخل المشغل بعد الثالثة، ولم ألمس صندوق العدسات يوم الاثنين.", None, ["cl_hadi_never"]),
    L("hd_refuse", "refuse_secret", "أفضّل ألا أجيب الآن."),
    L("hd_took", "reveal", "أخذت الصندوق كله بعد عدّ الاثنين لأكمل صور المعرض في بيتي، ونسيت أن أكتب في الاستمارة. وحين رأيت صباح الثلاثاء إعلان الجرد خفت أن يظنوا أنني أخذته، فتركته في درج المكتب المفتوح ولم أقصد أن يُتَّهم أحد.", ["f_hadi_had_box"]),
    L("hd_unknown", "deflect_unknown", "لا أذكر."),
    L("hd_off", "deflect_offtopic", "اسألني عن صور المعرض."),
    L("hd_bye", "farewell", "كان عليّ أن أكتب في الاستمارة.")])
ch("dana", "دانة الكيلاني", "witness", "مساعدة مختبر وأمينة عهدة النادي",
   "منظمة وتكتب كل شيء، وتميّز بين ما سجّلته وما افترضته. لا تتهم أحداً بلا سجل.",
   ["أن تبقى الاستمارة صحيحة", "ألا يُنسب إليها ما لم تسجّله"],
   [L("dn_greet", "greeting", "الاستمارة أمامي. أقرأ منها فقط."),
    L("dn_form", "reveal", "كل قطعة تخرج من الخزانة أو تعود إليها تُكتب في استمارة العهدة بالوقت والاسم والتوقيع، وعدد العدسات يُحصى عند كل تسليم.", ["f_custody_form_exists"]),
    L("dn_door", "reveal", "قارئ بطاقات باب المشغل يسجّل كل دخول وخروج، ويُقفل الباب تلقائياً بعد انتهاء الجلسة.", ["f_door_reader_exists"]),
    L("dn_unknown", "deflect_unknown", "هذا ليس في استمارتي."),
    L("dn_off", "deflect_offtopic", "اسألني عن العهدة والباب."),
    L("dn_bye", "farewell", "ما لم يُكتب لا أستطيع أن أشهد به.")])
ch("subhi", "صبحي النجار", "witness", "حارس المدرسة وعامل النظافة",
   "كبير في السن وشديد الانتظام، يمرّ على الأبواب في أوقات ثابتة ويدوّن ما رآه دون زيادة. لا يعرف شيئاً عن العدسات.",
   ["أن يبقى سجل جولاته سليماً"],
   [L("sb_greet", "greeting", "أمرّ على الأبواب وأكتب ما أراه."),
    L("sb_patrol", "reveal", "أشدّ باب المشغل في كل جولة ليلية وأكتب إن كان مقفلاً، وأدوّن كذلك من أراه في الممرات أول الصباح.", ["f_patrol_exists"]),
    L("sb_lock", "reveal", "قفل مكتب المشرف يسجّل كل فتح بالبطاقة، وأنا أفتحه ببطاقة الطوارئ للتنظيف قبل حضوره.", ["f_office_lock_exists"]),
    L("sb_unknown", "deflect_unknown", "لا أعرف."),
    L("sb_off", "deflect_offtopic", "اسألني عن الجولات والأبواب."),
    L("sb_bye", "farewell", "دفتري يتكلم عني.")])
ch("najla", "نجلاء الأسعد", "witness", "منسقة يوم التدريب لمعلمي العلوم",
   "رسمية ودقيقة، تحتفظ بأوراق الحضور الموقّعة وتجيب بما فيها.",
   ["أن تبقى أوراق الحضور محفوظة"],
   [L("nj_greet", "greeting", "أنسّق يوم التدريب وأحتفظ بأوراقه."),
    L("nj_sheet", "reveal", "كل مشارك يوقّع بيده عند الوصول وعند الانصراف على ورقة الحضور، وأنا أوقّع شهادة الإنهاء.", ["f_training_exists"]),
    L("nj_unknown", "deflect_unknown", "لا أعرف غير ما في الورقة."),
    L("nj_off", "deflect_offtopic", "اسألني عن يوم التدريب."),
    L("nj_bye", "farewell", "الورقة موقّعة.")])
ch("fares", "فارس العبدالله", "witness", "حارس بوابة المدرسة",
   "مباشر وصبور، يقرأ من سجل البوابة ولا يخمّن.",
   ["أن يبقى سجل البوابة صحيحاً"],
   [L("fr_greet", "greeting", "أحرس البوابة، وأقرأ لك سجلها."),
    L("fr_gate", "reveal", "بوابة المدرسة تسجّل بطاقة كل موظف وطالب عند الدخول بوقتها، ولا تسجّل الخروج.", ["f_gate_exists"]),
    L("fr_unknown", "deflect_unknown", "ليس عندي علم."),
    L("fr_off", "deflect_offtopic", "اسألني عن البوابة."),
    L("fr_bye", "farewell", "السجل كما هو.")])

locations = [{"id": "loc_workshop", "name_ar": "مشغل النادي", "description_ar": "غرفة فيها خزانة العدسات وباب بقارئ بطاقات."},
             {"id": "loc_office", "name_ar": "مكتب مشرف النادي", "description_ar": "مكتب فيه درج أيمن وقفل ببطاقة."},
             {"id": "loc_gate", "name_ar": "بوابة المدرسة", "description_ar": "مدخل المدرسة وسجل البطاقات."},
             {"id": "loc_hall", "name_ar": "قاعة التدريب", "description_ar": "قاعة في مدرسة أخرى أُقيم فيها يوم تدريب المعلمين."}]
objects = [{"id": "obj_box", "name_ar": "صندوق عدسات المعايرة", "description_ar": "صندوق مختوم فيه ست عدسات معايَرة لتلسكوب النادي."}]
orgs = [{"id": "org_school", "name_ar": "مدرسة المرصد", "description_ar": "مدرسة خيالية في مدينة «الأطلال»."}]

# ---------------------------------------------------------------- facts
F("f_box_missing", "فُقد صندوق عدسات المعايرة الستّ من مشغل النادي بعد جلسة الاثنين.", "event", ["obj_box"], 0)
F("f_box_in_drawer", "وُجد الصندوق صباح الثلاثاء في الدرج الأيمن لمكتب المشرف رشيد.", "event", ["obj_box", "rashid"], 0)
F("f_mazen_accuses", "يتهم مازن المشرف بأنه أخذ الصندوق.", "attribute", ["mazen", "rashid"], 0)
F("f_custody_form_exists", "للنادي استمارة عهدة تُكتب فيها كل حركة للعدسات، وتُحصى القطع عند كل تسليم.", "state", ["org_school"], 1, None, "loc_workshop")
F("f_door_reader_exists", "يسجّل قارئ باب المشغل كل دخول وخروج بالبطاقة، ويُقفل الباب تلقائياً بعد الجلسة.", "state", ["loc_workshop"], 1, None, "loc_workshop")
F("f_patrol_exists", "يدوّن حارس المدرسة جولاته الليلية على الأبواب وما يراه في الممرات أول الصباح.", "state", ["subhi"], 1)
F("f_office_lock_exists", "يسجّل قفل مكتب المشرف كل فتح بالبطاقة، ويملك الحارس بطاقة طوارئ للتنظيف.", "state", ["loc_office"], 1, None, "loc_office")
F("f_training_exists", "توقّع كل مشارك في يوم التدريب ورقة الحضور بيده عند الوصول وعند الانصراف.", "state", ["najla"], 1)
F("f_gate_exists", "تسجّل بوابة المدرسة بطاقة كل داخل بوقت الدخول.", "state", ["loc_gate"], 1, None, "loc_gate")
F("f_exhibit_posts_public", "نشر هادي مساء الاثنين صور معرض المدرسة على صفحة النادي.", "event", ["hadi"], 1, T(400))
F("f_mazen_photo", "صوّر مازن الدرج مفتوحاً وفيه الصندوق قبل أن يلمسه، بهاتف يضبط وقته من الشبكة.", "event", ["mazen", "obj_box"], 1, T(1066), "loc_office")
F("f_mazen_says_found", "يقول مازن إنه فتح الدرج ليضع ورقة موعد الرصد فوجد الصندوق.", "attribute", ["mazen"], 1)
F("f_rashid_says_away", "يقول رشيد إنه كان في يوم تدريب خارج المدرسة ظهر الاثنين ثم في بيته.", "attribute", ["rashid"], 1)
F("f_budget_refusal", "كتب رشيد للنادي أن الميزانية لا تكفي لشراء عدسات جديدة هذا الفصل.", "event", ["rashid"], 1)
F("f_sup_not_there", "كان المشرف خارج المدرسة من ظهر الاثنين ولم يصل إلى مكتبه إلا بعد أن صار الصندوق في الدرج، فلا تربطه سلسلة العهدة بوضعه هناك.", "relation", ["rashid", "obj_box"], 3, T(1066, "exact", 1072), "loc_office", ["KO-FC-04-026", "KO-RS-05-004"])
F("f_hadi_had_box", "غادر الصندوق المشغل في حوزة هادي بعد الإحصاء، وبقي خارج سجل العهدة إلى أن وُضع في الدرج قبيل العثور عليه.", "relation", ["hadi", "obj_box"], 3, T(72, "approx", 1060), "loc_workshop", ["KO-FC-04-026", "KO-FC-04B-002"])

claims = [
    {"id": "cl_mazen_sup", "statement_ar": "المشرف أخذ العدسات لأنه هو وحده من يملك الدرج.", "kind": "rumour", "held_by": ["mazen"], "true_fact_id": "f_sup_not_there",
     "contradicted_by_evidence_ids": ["ev_training_sheet", "ev_gate_log", "ev_office_lock_log", "ev_found_photo"]},
    {"id": "cl_hadi_never", "statement_ar": "لم أدخل المشغل بعد الثالثة ولم ألمس الصندوق.", "kind": "lie", "held_by": ["hadi"], "true_fact_id": "f_hadi_had_box",
     "contradicted_by_evidence_ids": ["ev_door_log", "ev_custody_form", "ev_exhibit_post"]},
]
timeline = [
    {"id": "te_training", "description_ar": "رشيد في يوم التدريب خارج المدرسة.", "time": T(-60, "exact", 240), "location_id": "loc_hall", "actor_ids": ["rashid"], "fact_ids": ["f_sup_not_there"], "motivated_by_ar": "حضور يوم تدريب المعلمين"},
    {"id": "te_count", "description_ar": "دانة تحصي العدسات وتختم الصندوق وتكتب القيد.", "time": T(55), "location_id": "loc_workshop", "actor_ids": ["dana"], "fact_ids": ["f_custody_form_exists"], "motivated_by_ar": "إجراء العهدة المعتاد بعد الجلسة"},
    {"id": "te_hadi_in", "description_ar": "هادي داخل المشغل بعد الإحصاء.", "time": T(72, "exact", 81), "location_id": "loc_workshop", "actor_ids": ["hadi"], "fact_ids": ["f_hadi_had_box"], "motivated_by_ar": "أراد إكمال صور المعرض بالعدسات"},
    {"id": "te_lock", "description_ar": "الباب يُقفل تلقائياً.", "time": T(120), "location_id": "loc_workshop", "actor_ids": [], "fact_ids": ["f_door_reader_exists"]},
    {"id": "te_post", "description_ar": "هادي ينشر صور المعرض.", "time": T(400), "actor_ids": ["hadi"], "fact_ids": ["f_exhibit_posts_public"], "motivated_by_ar": "أراد عرض صوره قبل المعرض"},
    {"id": "te_arrive_hadi", "description_ar": "هادي يدخل بوابة المدرسة صباح الثلاثاء.", "time": T(1044), "location_id": "loc_gate", "actor_ids": ["hadi"], "fact_ids": ["f_hadi_had_box"], "motivated_by_ar": "جاء قبل الحصة الأولى"},
    {"id": "te_cleaner", "description_ar": "صبحي يفتح المكتب للتنظيف.", "time": T(1050), "location_id": "loc_office", "actor_ids": ["subhi"], "fact_ids": ["f_office_lock_exists"], "motivated_by_ar": "تنظيف المكتب قبل حضور المشرف"},
    {"id": "te_found", "description_ar": "مازن يفتح الدرج ويصوّر الصندوق.", "time": T(1066), "location_id": "loc_office", "actor_ids": ["mazen"], "fact_ids": ["f_mazen_photo"], "motivated_by_ar": "أراد وضع ورقة موعد الرصد"},
    {"id": "te_rashid_in", "description_ar": "رشيد يدخل بوابة المدرسة.", "time": T(1072), "location_id": "loc_gate", "actor_ids": ["rashid"], "fact_ids": ["f_sup_not_there"], "motivated_by_ar": "بدء يوم العمل"},
]

# ---------------------------------------------------------------- evidence
V("ev_found_report", "تقرير مازن عن العثور على الصندوق", "documentary",
  "تقرير كتبه مازن الصيرفي — الثلاثاء 07:50\n«وجدت صندوق عدسات المعايرة في الدرج الأيمن لمكتب أ. رشيد. المكتب مكتبه والدرج درجه، ولا يدخله غيره عادةً. أطلب التحقيق مع المشرف.»",
  ["a_read_report"], ["f_box_in_drawer", "f_mazen_accuses"], "weak",
  "رواية طالب خالف المشرف قبل أيام؛ تقول أين وُجد الصندوق ولا تقول كيف وصل إليه، ولا تُثبت من وضعه.", contradicts=None, red=True, loc="loc_office")
V("ev_custody_form", "استمارة عهدة العدسات", "documentary",
  "نادي المنظار — استمارة عهدة صندوق العدسات (ختم S-14)\nالاثنين 14:55 — إحصاء دانة الكيلاني: 6 من 6 — الختم سليم — حُفظ في خزانة المشغل — التوقيع: د. الكيلاني\nالثلاثاء 07:36 — جولة صبحي النجار مع دانة: الخزانة فارغة، لا صندوق\nالثلاثاء 07:50 — استلام من م. الصيرفي: الصندوق في درج مكتب المشرف، الختم مكسور، 6 عدسات\nلا قيد آخر في الاستمارة بين هذه القيود.",
  ["a_get_custody_form"], ["f_custody_form_exists", "f_hadi_had_box"], "strong",
  "تسجّل ما كُتب وقتما كُتب فقط؛ فراغ الاستمارة يبيّن أن العهدة انقطعت ولا يسمّي من أخذ الصندوق ولا لماذا.", ko="KO-FC-04-026", loc="loc_workshop")
V("ev_door_log", "سجل قارئ بطاقات باب المشغل", "digital",
  "مشغل النادي — قارئ البطاقات — الاثنين\n14:50 دخول: د. الكيلاني\n15:00 خروج: د. الكيلاني\n15:12 دخول: ه. الشامي\n15:21 خروج: ه. الشامي\n16:00 إقفال تلقائي بانتهاء الجلسة\nلا دخول مسجّل بعد الإقفال حتى الثلاثاء 07:31 (بطاقة ص. النجار).",
  ["a_get_door_log"], ["f_door_reader_exists", "f_hadi_had_box"], "strong",
  "يسجّل مرور بطاقة لا شخصاً، وقد تُعار البطاقات؛ قوته أن ما قبله وما بعده في الاستمارة يتسق معه، وهو لا يرى ما حُمل خارج الغرفة.", loc="loc_workshop")
V("ev_exhibit_post", "منشور صور المعرض على صفحة النادي", "digital",
  "صفحة نادي المنظار — منشور بحساب ه. الشامي — الاثنين 20:40\nصورة زهرة على سور حديقة، والتعليق: «صورة من تجارب المعرض بالعدسة رقم 3 من عدسات النادي»\nبيانات ملف الصورة: رقم عدسة النادي L3 · وقت الالتقاط 20:31",
  ["a_get_exhibit_post"], ["f_exhibit_posts_public", "f_hadi_had_box"], "moderate",
  "يثبت أن عدسة النادي رقم 3 استُعملت خارج المشغل مساء الاثنين من حساب هادي؛ لا يثبت أنه أخذ الصندوق كله ولا كيف وصل إليه، ولا متى أعاده.", loc="loc_workshop")
V("ev_patrol_log", "دفتر جولات الحارس", "documentary",
  "دفتر جولات صبحي النجار — بخط اليد\nالاثنين 18:00 · 21:00 — باب المشغل مشدود ومقفل\nالثلاثاء 05:30 — باب المشغل مقفل\nالثلاثاء 07:40 — رأيت الطالب هادي في ممر الإدارة يحمل كيساً قماشياً، قال إنه ذاهب إلى غرفة النادي.",
  ["a_get_patrol_log"], ["f_patrol_exists", "f_hadi_had_box"], "moderate",
  "دفتر كاتبه حارس واحد وليس نظاماً آلياً، ويصف ما رآه ولا يقول ما في الكيس؛ قيمته في اتفاقه مع قارئ الباب.", loc="loc_gate")
V("ev_training_sheet", "ورقة حضور يوم التدريب", "documentary",
  "يوم تدريب معلمي العلوم — ورقة الحضور الموقّعة بخط المشاركين\nالاثنين: وصول 12:58 — توقيع: ر. الحداد\nانصراف 18:05 — توقيع: ر. الحداد\nشهادة المنسقة: لم يغادر أي مشارك القاعة قبل ختام اليوم\nالتوقيع: ن. الأسعد",
  ["a_get_training_sheet"], ["f_training_exists", "f_sup_not_there"], "strong",
  "تثبت حضوره في الفترة المكتوبة فقط، ولا تغطي مساء الاثنين ولا ليلته.", loc="loc_hall")
V("ev_gate_log", "سجل بوابة المدرسة", "digital",
  "بوابة المدرسة — سجل بطاقات الدخول — الثلاثاء\n07:24 ه. الشامي\n07:41 م. الصيرفي\n07:52 ر. الحداد\nلا يسجّل الخروج. لا قيد للمشرف يوم الاثنين بعد 12:50.",
  ["a_get_gate_log"], ["f_gate_exists", "f_sup_not_there"], "strong",
  "يسجّل دخول البطاقة لا من حملها، ولا يسجّل الخروج؛ ويتسق مع ورقة يوم التدريب لأن مصدرَيهما منفصلان.", loc="loc_gate")
V("ev_office_lock_log", "سجل قفل مكتب المشرف", "digital",
  "قفل مكتب المشرف — سجل الفتح\nالاثنين 12:48 قفل: ر. الحداد\nالثلاثاء 07:30 فتح ببطاقة الطوارئ: ص. النجار (للتنظيف؛ الباب بقي مواربة للتهوية)\nالثلاثاء 07:55 فتح: ر. الحداد",
  ["a_get_office_lock_log"], ["f_office_lock_exists", "f_sup_not_there"], "strong",
  "يسجّل الفتح بالبطاقة فقط؛ الباب المواربة يعني أن الدخول إلى المكتب لم يمرّ بالقفل بين 07:30 و07:55.", loc="loc_office")
V("ev_found_photo", "صورة مازن للدرج", "digital",
  "صورة التقطها هاتف مازن — بيانات الصورة: الثلاثاء 07:46 (وقت الشبكة)\nدرج مفتوح، وفيه صندوق عدسات بختم مكسور؛ لا يظهر في الصورة أحد.",
  ["a_get_found_photo"], ["f_mazen_photo", "f_sup_not_there"], "moderate",
  "الصورة من هاتف صاحب الاتهام نفسه؛ وقتها مضبوط من الشبكة، وهي تثبت أن الصندوق كان في الدرج قبل 07:52 لا من وضعه.", loc="loc_office")
V("ev_sup_email", "رسالة المشرف عن الميزانية", "digital",
  "رسالة من ر. الحداد إلى أعضاء النادي — الخميس الماضي\n«بعد مراجعة الميزانية لن نستطيع شراء عدسات جديدة هذا الفصل، وسنستعمل المتوفر ونحافظ عليه.»",
  ["a_get_sup_email"], ["f_budget_refusal"], "moderate",
  "رسالة تثبت رفض الشراء لا إخفاء العدسات؛ والحرص على المتوفر مكتوب فيها، ولا تصلح سبباً للشك وحدها.", red=True, loc="loc_office")
V("ev_mazen_stmt", "إفادة مازن (ملخص)", "testimonial",
  "ملخص إفادة مازن الصيرفي:\n«فتحت الدرج لأضع ورقة الموعد فرأيت الصندوق وصوّرته. لا أعرف من وضعه، لكن المكتب مكتب المشرف.»",
  ["a_note_mazen"], ["f_mazen_says_found"], "weak",
  "إفادة من لا يعرف كيف وصل الصندوق إلى الدرج؛ يقيس رأيه بما في السجلات لا بنبرته.", loc="loc_office")
V("ev_rashid_stmt", "إفادة رشيد (ملخص)", "testimonial",
  "ملخص إفادة رشيد الحداد:\n«كنت في يوم التدريب ظهر الاثنين ثم في بيتي. وصلت صباح الثلاثاء ولم أرَ الصندوق قبل أن يُخبَرني به.»",
  ["a_note_rashid"], ["f_rashid_says_away"], "weak",
  "إفادة صاحب الشأن عن نفسه؛ تُقاس بأوراق وسجلات لا يكتبها هو.", loc="loc_office")
V("ev_hadi_stmt", "إفادة هادي بعد المواجهة (ملخص)", "testimonial",
  "ملخص إفادة هادي الشامي:\n«أخذت الصندوق بعد الإحصاء لأكمل الصور، ولم أكتب في الاستمارة. تركته في الدرج صباح الثلاثاء لأنني خفت. لم أقصد أن يُتَّهم أحد.»",
  ["a_note_hadi"], ["f_hadi_had_box"], "moderate",
  "إفادة اعتراف بعد عرض دليل عليه؛ تؤيد سجلات سبقتها ولا تغني عنها.", loc="loc_office")

# ---------------------------------------------------------------- inferences
I("i_hadi_a", [E("ev_door_log"), E("ev_custody_form")], "fact", "f_hadi_had_box", "establishes", "strong",
  "الاستمارة تضع الصندوق مختوماً وكاملاً في الخزانة عند الإحصاء وفارغاً عند جولة الصباح، وقارئ الباب لا يسجّل بين الوقتين غير بطاقة هادي؛ فخرج الصندوق معه ولم يرجع بقيد.", ["KO-FC-04-026", "KO-RS-05-004"])
I("i_hadi_b", [E("ev_exhibit_post"), E("ev_patrol_log")], "fact", "f_hadi_had_box", "establishes", "strong",
  "عدسة النادي رقم 3 التُقطت بها صورة في الساعة التي كان باب المشغل فيها مقفلاً بشهادة الجولات، وصاحب الحساب هو هادي؛ ورآه الحارس صباحاً يحمل كيساً في ممر الإدارة قبل العثور على الصندوق بست دقائق.", ["KO-FC-04-026", "KO-FC-04B-002"])
I("i_sup_a", [E("ev_training_sheet"), E("ev_gate_log")], "fact", "f_sup_not_there", "establishes", "strong",
  "الورقة بخط المشرف تضعه في قاعة التدريب إلى 18:05، وسجل البوابة لا يدخله إلى المدرسة إلا 07:52؛ وصورة الصندوق في الدرج أقدم من ذلك بست دقائق.", ["KO-RS-05-004", "KO-FC-04-024"])
I("i_sup_b", [E("ev_office_lock_log"), E("ev_found_photo")], "fact", "f_sup_not_there", "establishes", "strong",
  "قفل المكتب لا يسجّل فتحاً من المشرف بين الاثنين 12:48 والثلاثاء 07:55، والصورة بوقت الشبكة تضع الصندوق في الدرج 07:46؛ فلم يكن هو من وضعه.", ["KO-RS-05-004", "KO-FC-04-024"])
I("i_cl_mazen", [Fa("f_sup_not_there")], "claim", "cl_mazen_sup", "contradicts_claim", "strong",
  "مكان العثور لا يدل على من وضع الشيء فيه؛ والمشرف كان خارج المدرسة وخارج المكتب وقت الوضع.", ["KO-RS-05-014", "KO-RS-06-020"])
I("i_cl_hadi", [Fa("f_hadi_had_box")], "claim", "cl_hadi_never", "contradicts_claim", "strong",
  "بطاقته دخلت المشغل بعد الإحصاء وصورته بعدسة من الصندوق خارج المشغل، فلا يوافق ذلك قوله.", ["KO-RS-05-014"])
I("i_support_hadi", [Fa("f_hadi_had_box"), Fa("f_sup_not_there")], "hypothesis", "h_hadi", "supports", "strong",
  "الصندوق خرج من المشغل بيد هادي وبقي بلا قيد، ووُضع في الدرج والمشرف بعيد؛ فهذه الفرضية تفسّر الاستمارة والباب والدفتر معاً.", ["KO-RS-06-007"])
I("i_rule_sup", [Fa("f_sup_not_there"), Fa("f_hadi_had_box")], "hypothesis", "h_sup", "rules_out", "conclusive",
  "من كان خارج المدرسة والمكتب وقت الوضع لا يضع الصندوق في درجه، والصندوق نفسه كان بيد غيره؛ وعثوره في درجه لا يعدل شيئاً من ذلك.", ["KO-RS-06-008"])
I("i_rule_mazen", [Fa("f_hadi_had_box"), Fa("f_sup_not_there")], "hypothesis", "h_mazen", "rules_out", "strong",
  "لا قيد يدخل مازن المشغل ولا يضع الصندوق بيده قبل التصوير، والصندوق مرتبط بغيره من الاثنين؛ والخلاف السابق مع المشرف لا يكفي وحده.", ["KO-RS-06-008"])
I("i_rule_misfiled", [Fa("f_hadi_had_box"), Fa("f_sup_not_there")], "hypothesis", "h_misfiled", "rules_out", "strong",
  "الصندوق لم يبقَ في المشغل ليُنقل خطأً عند التنظيف؛ غادره بحوزة شخص معين وبلا قيد.", ["KO-RS-06-008"])

# ---------------------------------------------------------------- knowledge
ck = [
    {"character_id": "rashid", "knows": [K("f_rashid_says_away"), K("f_budget_refusal")], "hides": [], "believes": []},
    {"character_id": "mazen", "knows": [K("f_mazen_photo"), K("f_mazen_says_found"), K("f_exhibit_posts_public", "witnessed", "fairly_sure")], "hides": [], "believes": [{"claim_id": "cl_mazen_sup", "stance": "sincere"}]},
    {"character_id": "hadi", "knows": [], "hides": [{"fact_id": "f_hadi_had_box", "reveal_when": {"presented": {"evidence_id": "ev_exhibit_post", "to_character": "hadi"}}, "cover_claim_id": "cl_hadi_never", "reveal_line_id": "hd_took"}],
     "believes": [{"claim_id": "cl_hadi_never", "stance": "deliberate_lie"}]},
    {"character_id": "dana", "knows": [K("f_custody_form_exists", "professional"), K("f_door_reader_exists", "professional")], "hides": [], "believes": []},
    {"character_id": "subhi", "knows": [K("f_patrol_exists", "professional"), K("f_office_lock_exists", "professional")], "hides": [], "believes": []},
    {"character_id": "najla", "knows": [K("f_training_exists", "professional")], "hides": [], "believes": []},
    {"character_id": "fares", "knows": [K("f_gate_exists", "professional")], "hides": [], "believes": []},
]
hyps = [
    {"id": "h_sup", "statement_ar": "أخذ المشرف العدسات وأخفاها في درجه بنفسه.", "is_true": False, "plausibility_at_start": "high", "suspect_id": "rashid"},
    {"id": "h_mazen", "statement_ar": "وضع مازن الصندوق في الدرج قبل أن يصوّره ليُتَّهم المشرف.", "is_true": False, "plausibility_at_start": "medium", "suspect_id": "mazen"},
    {"id": "h_hadi", "statement_ar": "أخرج هادي الصندوق من المشغل دون قيد ثم تركه في الدرج، وليس للمشرف يد في ذلك.", "is_true": True, "plausibility_at_start": "low", "suspect_id": "hadi"},
    {"id": "h_misfiled", "statement_ar": "لم يأخذ أحد الصندوق عمداً، بل نُقل خطأً عند تنظيف المشغل ووُضع في الدرج.", "is_true": False, "plausibility_at_start": "medium"},
]
mis = [
    {"id": "rh_place", "points_to_hypothesis_id": "h_sup", "planted_via_ar": "الصندوق وُجد في درج المشرف، والدرج والمكتب له.", "evidence_ids": ["ev_found_report"],
     "refuted_by_inference_ids": ["i_sup_a", "i_sup_b", "i_rule_sup"],
     "fairness_note_ar": "ورقة التدريب وسجل البوابة وقفل المكتب وصورة مازن كلها في يد اللاعب، وتبيّن أن المشرف لم يكن حاضراً؛ ومكان العثور لا يحدد من وضع."},
    {"id": "rh_budget", "points_to_hypothesis_id": "h_sup", "planted_via_ar": "رفض المشرف شراء عدسات جديدة يبدو دافعاً لإخفاء القديمة.", "evidence_ids": ["ev_sup_email"],
     "refuted_by_inference_ids": ["i_rule_sup", "i_cl_mazen"],
     "fairness_note_ar": "الرسالة نفسها تطلب المحافظة على المتوفر، والدافع المحتمل لا يغني عن سجل يضع صاحبه في المكان."},
    {"id": "rh_finder", "points_to_hypothesis_id": "h_mazen", "planted_via_ar": "مازن هو من وجد الصندوق وكان قد اختلف مع المشرف.", "evidence_ids": ["ev_found_report", "ev_mazen_stmt"],
     "refuted_by_inference_ids": ["i_rule_mazen", "i_hadi_a", "i_hadi_b"],
     "fairness_note_ar": "الصورة بوقت الشبكة تبيّن أنه صوّر الصندوق قبل أن يلمسه، ولا سجل يقرّبه من المشغل؛ فالاختلاف مع المشرف دافع محتمل لا أكثر."},
]
los = std_los("يتتبع سلسلة العهدة لقطعة مادية: من سلّمها، ومن استلمها، ومتى، وأين ينقطع القيد؛ ولا يعدّ مكان العثور دليلاً على من وضعها.", "KO-FC-04-026",
              ["يحدد الفجوة في سلسلة العهدة", "يفرّق بين مكان العثور ومن وضع الشيء", "يطلب سجلاً مستقلاً عن المتهم"])
ref = ("لا يدل وجود الصندوق في درج المشرف على أنه أخذه. استمارة العهدة تثبت إحصاءً كاملاً ثم فراغاً في الخزانة، ثم ثغرة بلا أي قيد، ولا يظهر في قارئ باب المشغل بعد الإحصاء سوى بطاقة هادي. وعدسة من الصندوق استُعملت خارج المشغل في الليلة نفسها من حساب هادي، ورآه الحارس صباحاً قريباً من المكتب بكيس. أما المشرف فتثبت ورقة يوم التدريب وسجلات البوابة والقفل والصورة أنه لم يكن حاضراً عند الوضع. حدود الاستنتاج: لا تُظهر السجلات ما كان في الكيس ولا دافع هادي، ولا أن ما كتبه الحارس أو ما قاله هادي يغني عن القيود.")
hints = [
    H("hg1", 1, "metacognitive", "حين يوجد شيء في مكان ما، اسأل: كيف وصل إليه؟ ومن سلّمه لمن؟ وأين انقطع القيد؟", {"always": True}, None, 0.02),
    H("hg2", 2, "focus_area", "اقرأ استمارة العهدة قيداً قيداً وابحث عن الوقت الذي لا يغطيه أي توقيع.", he("ev_found_report"), None, 0.04),
    H("hg3", 3, "pointer", "ابحث عن سجلات لا يكتبها المشرف ولا الطلاب المتخاصمون: أبواب، وبوابات، وأوراق حضور، ودفتر حارس.", he("ev_found_report"), None, 0.08),
    H("hh1", 1, "metacognitive", "من دخل المشغل بعد الإحصاء وقبل الإقفال؟", he("ev_custody_form"), "i_hadi_a", 0.02),
    H("hh2", 2, "pointer", "قارن قيود الاستمارة بقارئ الباب: ما الذي تغيّر بين الوقتين؟", he("ev_custody_form"), "i_hadi_a", 0.06),
    H("hs1", 1, "metacognitive", "هل يمكن لمن هو خارج المدرسة أن يضع شيئاً في درج داخلها؟", he("ev_found_report"), "i_sup_a", 0.02),
    H("hs2", 2, "pointer", "ابحث عن سجلين مستقلين: ورقة يوم التدريب وسجل بوابة المدرسة.", he("ev_found_report"), "i_sup_a", 0.06),
]

# ---------------------------------------------------------------- actions
a = lambda: None
Act("a_read_report", "examine", "اقرأ تقرير مازن", al, [G("ev_found_report")], "loc_office", "READ_REPORT")
interviews([("rashid", "رشيد"), ("mazen", "مازن"), ("hadi", "هادي"), ("dana", "دانة"), ("subhi", "صبحي"), ("najla", "نجلاء"), ("fares", "فارس")])
get("ev_custody_form", "اطلب استمارة عهدة العدسات", fu("f_custody_form_exists"), "loc_workshop")
get("ev_door_log", "اطلب سجل قارئ باب المشغل", fu("f_door_reader_exists"), "loc_workshop")
get("ev_exhibit_post", "افتح منشور صور المعرض", fu("f_exhibit_posts_public"), "loc_workshop")
get("ev_patrol_log", "اطلب دفتر جولات الحارس", fu("f_patrol_exists"), "loc_gate")
get("ev_training_sheet", "اطلب ورقة حضور يوم التدريب", fu("f_training_exists"), "loc_hall")
get("ev_gate_log", "اطلب سجل بوابة المدرسة", fu("f_gate_exists"), "loc_gate")
get("ev_office_lock_log", "اطلب سجل قفل مكتب المشرف", fu("f_office_lock_exists"), "loc_office")
get("ev_found_photo", "اطلب صورة الدرج من هاتف مازن", fu("f_mazen_photo"), "loc_office")
get("ev_sup_email", "اطلب رسالة المشرف عن الميزانية", fu("f_budget_refusal"), "loc_office")
Act("a_note_mazen", "examine", "دوّن إفادة مازن", fu("f_mazen_says_found"), [G("ev_mazen_stmt")], "mazen", "NOTE_MAZEN")
Act("a_note_rashid", "examine", "دوّن إفادة رشيد", fu("f_rashid_says_away"), [G("ev_rashid_stmt")], "rashid", "NOTE_RASHID")
Act("a_note_hadi", "examine", "دوّن إفادة هادي", fu("f_hadi_had_box"), [G("ev_hadi_stmt")], "hadi", "NOTE_HADI")
Act("p_post_hadi", "present_evidence", "اعرض منشور الصور على هادي", {"presented": {"evidence_id": "ev_exhibit_post", "to_character": "hadi"}}, [{"op": "emit_event", "ref_id": "PRESENTED_POST"}], "hadi", "P_POST_HADI", 0)
tail_actions()

topics = [
    {"id": "t_away", "label_ar": "أين كنت ظهر الاثنين", "example_questions_ar": ["أين كنت ظهر الاثنين؟", "متى وصلت صباح الثلاثاء؟"], "fact_ids": ["f_rashid_says_away"]},
    {"id": "t_budget", "label_ar": "الميزانية والعدسات", "example_questions_ar": ["ماذا كتبت عن شراء العدسات؟"], "fact_ids": ["f_budget_refusal"]},
    {"id": "t_found", "label_ar": "العثور على الصندوق", "example_questions_ar": ["كيف وجدت الصندوق؟", "هل صوّرته؟"], "fact_ids": ["f_mazen_photo", "f_mazen_says_found"]},
    {"id": "t_posts", "label_ar": "صور المعرض", "example_questions_ar": ["هل نُشرت صور مساء الاثنين؟"], "fact_ids": ["f_exhibit_posts_public"]},
    {"id": "t_blame", "label_ar": "من أخذ العدسات برأيك", "example_questions_ar": ["من تظن أنه أخذها؟"], "fact_ids": [], "claim_ids": ["cl_mazen_sup"]},
    {"id": "t_monday", "label_ar": "يوم الاثنين في المشغل", "example_questions_ar": ["هل دخلت المشغل بعد الثالثة؟"], "fact_ids": [], "claim_ids": ["cl_hadi_never"]},
    {"id": "t_box", "label_ar": "ما فعلته بالصندوق", "example_questions_ar": ["ماذا حدث للصندوق بعد الإحصاء؟"], "fact_ids": ["f_hadi_had_box"]},
    {"id": "t_form", "label_ar": "استمارة العهدة", "example_questions_ar": ["كيف تُسجَّل حركة العدسات؟"], "fact_ids": ["f_custody_form_exists"]},
    {"id": "t_door", "label_ar": "باب المشغل", "example_questions_ar": ["ماذا يسجّل قارئ الباب؟"], "fact_ids": ["f_door_reader_exists"]},
    {"id": "t_patrol", "label_ar": "جولات الحارس", "example_questions_ar": ["ماذا تدوّن في جولاتك؟"], "fact_ids": ["f_patrol_exists"]},
    {"id": "t_office_lock", "label_ar": "قفل المكتب", "example_questions_ar": ["من يفتح المكتب ومتى؟"], "fact_ids": ["f_office_lock_exists"]},
    {"id": "t_training", "label_ar": "يوم التدريب", "example_questions_ar": ["كيف تثبتون حضور المشاركين؟"], "fact_ids": ["f_training_exists"]},
    {"id": "t_gate", "label_ar": "بوابة المدرسة", "example_questions_ar": ["ماذا تسجّل البوابة؟"], "fact_ids": ["f_gate_exists"]},
]
steps = [
    (1, "الاستمارة تروي القصة بصمتها: إحصاء كامل ثم خزانة فارغة ثم صندوق في الدرج، وبين القيود الثلاثة وقت لا يحمل توقيع أحد.", ["ev_custody_form"], "i_hadi_a"),
    (2, "في ذلك الوقت لم تمرّ ببوابة المشغل غير بطاقة واحدة، ثم أُقفل الباب حتى الصباح.", ["ev_door_log", "ev_custody_form"], "i_hadi_a"),
    (3, "مسار ثانٍ لا يشترك مع الأول: عدسة النادي ظهرت في صورة ليلية خارج المشغل المقفل، وشاهد الحارس صاحب الحساب قرب المكتب صباحاً.", ["ev_exhibit_post", "ev_patrol_log"], "i_hadi_b"),
    (4, "المشرف: ورقة بخطه في قاعة بعيدة وبوابة لا تدخله قبل الدقيقة 07:52، فلم يكن موجوداً حين دخل الصندوق الدرج.", ["ev_training_sheet", "ev_gate_log"], "i_sup_a"),
    (5, "مسار ثانٍ للمشرف: قفل مكتبه لا يسجّل فتحاً من بطاقته ليلاً، وصورة الدرج بوقت الشبكة أقدم من وصوله.", ["ev_office_lock_log", "ev_found_photo"], "i_sup_b"),
    (6, "بقية الأطراف: خلاف مازن مع المشرف ورسالة الميزانية يفسّران الشك ولا يقدمان قيداً؛ والإفادة المعترفة تؤيد سجلات سبقتها.", ["ev_sup_email", "ev_hadi_stmt"], "i_rule_sup"),
]
ending = dict(
  alt=["يمكن إثبات الحلقتين بالمسار الأول وحده: الاستمارة وقارئ الباب لما بعد الإحصاء، وورقة التدريب وسجل البوابة للمشرف.",
       "ويمكن إثباتهما بالمسار الثاني وحده: المنشور ودفتر الجولات، وقفل المكتب وصورة الدرج؛ والأقوى أن يتفق المساران."],
  notlimits=["لا تبيّن السجلات ما كان في الكيس القماشي ولا لماذا اختار هادي ذلك الدرج بالذات.",
             "قارئ الباب والبوابة يسجّلان البطاقة لا حاملها؛ قوتهما في اتفاقهما مع ورقة بخط المنسقة ودفتر الحارس.",
             "لا نعرف إن كان أحد غير هادي لمس الصندوق ليلاً؛ الأرجح أنه لم يفعل، وهذه نسبة ترجيح لا يقين."],
  notes=["سلسلة العهدة تُقرأ بالقيود لا بالأماكن: من سلّم؟ ومن استلم؟ وأين ينقطع القيد؟ والفجوة تُضعف قيمة الشيء كدليل، ولا تسمّي من تسبّب بها.",
         "العثور على شيء في مكان لا يعني أن صاحب المكان وضعه فيه؛ اسأل عن سجل مستقل يضع صاحب المكان في مكان آخر.",
         "تفحّص هذه القضية مصلحة كل من يدلي بدليل: مازن اختلف مع المشرف، لكن ذلك لا يجعل الدليل الذي قدمه كاذباً، وإنما يدفعنا للبحث عن دليل لا يعتمد عليه.",
         "لا أحد هنا شرير: هادي أخطأ بإجراء ثم خاف فأخطأ ثانية. والإصلاح المناسب تعليمي: كتابة كل استلام في الاستمارة، وتحية المشرف على صبره.",
         "بطاقة الأصل: القضية أصلية من ATHAR على بنية «الدليل المدسوس» من مكتبة الحالات، محوّلة إلى بشر وبلا أي تعليم لكيفية الدس."])

premise = {"hook_ar": "ستة عدسات اختفت من نادي المنظار ثم ظهرت في درج المشرف. والكل يقول: الأمر محسوم. فمن وضعها هناك؟",
           "player_role_ar": "أنت طالب متدرب في لجنة الجرد بمدرسة المرصد، وطُلب منك رأي معلّل في فقدان صندوق عدسات المعايرة، دون اتهام أحد قبل أن تثبت السجلات شيئاً.",
           "setting_ar": "مدرسة المرصد في مدينة «الأطلال»، من ظهر الاثنين إلى صباح الثلاثاء. أوقات الأبواب والبوابة والقفل بساعة المدرسة.",
           "public_fact_ids": ["f_box_missing", "f_box_in_drawer", "f_mazen_accuses"],
           "assumed_general_knowledge_ar": ["مكان العثور على شيء لا يثبت من وضعه", "القيد الناقص في سجل العهدة لا يسمّي صاحبه", "الخلاف السابق مع شخص لا يجعل كل ما يقدمه كاذباً"]}
meta = {"title_ar": "الصندوق في الدرج الأيمن", "title_en": "The Box in the Right-Hand Drawer", "age_band": "13-15", "estimated_minutes": 30, "difficulty": 2,
        "content_flags": ["no_violence", "theft"],
        "knowledge_object_refs": ["KO-FC-04-026", "KO-FC-04B-002", "KO-RS-05-004", "KO-RS-05-001", "KO-RS-05-014", "KO-RS-06-001", "KO-RS-06-008", "KO-RS-06-021", "KO-RS-06-009", "KO-RS-05-002", "KO-RS-05-005"]}
ui = {
    "clock": {"epoch_hhmm": "14:00", "zone_label_ar": "ساعة المدرسة"},
    "cover": {"title_ar": "الصندوق في الدرج الأيمن", "tagline_ar": "وُجد في درجه… فهل هذا يكفي؟", "kicker_ar": "الملف السادس والعشرون · سلسلة العهدة", "glyph": "▣", "accent": "amber"},
    "cold_open_ar": ["الثلاثاء، 07:50.", "ستة عدسات معايرة خرجت من مشغل نادي المنظار، وظهرت في الدرج الأيمن لمكتب المشرف.", "مازن يقول إن الأمر واضح. والمشرف يقول إنه لم يرَ الصندوق قبل الصباح.",
                    "قبل أي حكم: من سلّم الصندوق لمن؟ وفي أي لحظة انقطع القيد؟"],
    "limit_menu": [
        {"id": "l_content_unknown", "label_ar": "السجلات لا تبيّن ما كان في الكيس القماشي ولا سبب اختيار ذلك الدرج"},
        {"id": "l_card_not_person", "label_ar": "البطاقة والبوابة تسجّلان المرور لا الشخص، وقوتهما في اتفاقهما مع ورقة المنسقة ودفتر الحارس"},
        {"id": "l_night_unknown", "label_ar": "لا نعرف إن لمس أحد الصندوق ليلاً، ويبقى هذا احتمالاً ضئيلاً لا يقيناً"},
        {"id": "l_invalid_place", "label_ar": "وجود الصندوق في درج المشرف يدل على أنه من وضعه"},
        {"id": "l_invalid_feud", "label_ar": "خلاف مازن مع المشرف يكفي لاعتباره الفاعل"},
        {"id": "l_invalid_shy", "label_ar": "خجل هادي وصمته يدلان على أنه أخذ الصندوق"}],
    "mind_change_menu": [
        {"id": "m_sup_card", "label_ar": "ظهور قيد لبطاقة المشرف في المكتب أو البوابة قبل 07:46"},
        {"id": "m_door_lent", "label_ar": "ثبوت أن بطاقة هادي كانت بيد غيره وقت دخول المشغل"},
        {"id": "m_photo_time", "label_ar": "ثبوت أن وقت صورة الدرج غير صحيح"},
        {"id": "m_popular", "label_ar": "اتفاق أكثر الطلاب على أن المشرف هو الفاعل"}],
    "transfer": {
        "id": "tr_trophy", "title_ar": "اختبار نقل المهارة: كأس الصف",
        "scenario_ar": "اختفى كأس صف من خزانة الإدارة، ثم وُجد في سلة مكتب معلمة. أمامك وثيقتان من واقعة خيالية لا علاقة لها بالقضية.",
        "documents": [
            {"title_ar": "سجل استعارة الكأس", "body_ar": "الأربعاء 10:00 — سُلّم الكأس لمشرف الفعالية مختوماً — توقيع المشرف.\nالأربعاء 13:00 — لا قيد بعده.\nالخميس 08:00 — وُجد الكأس في سلة مكتب المعلمة، دون ختم."},
            {"title_ar": "بيان المعلمة", "body_ar": "«كنت في رحلة ميدانية من الأربعاء 09:00 إلى الخميس 09:30 ولم أدخل المدرسة.» وبجانبه ورقة الرحلة الموقّعة من المنظّم."}],
        "prompt_ar": "اختر الخطوات الصالحة لتقدير من وضع الكأس في السلة (يمكنك اختيار أكثر من خطوة).",
        "options": [
            {"id": "o1", "text_ar": "تحديد الوقت الذي لا يغطيه أي قيد في سجل الاستعارة"},
            {"id": "o2", "text_ar": "البحث عن سجل مستقل يبيّن أين كانت المعلمة في ذلك الوقت"},
            {"id": "o3", "text_ar": "السؤال عمّن سُلِّم إليه الكأس آخر مرة بقيد موقّع"},
            {"id": "o4", "text_ar": "عدّ ما يعرفه كل شاهد عن مصلحة المعلمة قبل الحكم"},
            {"id": "o5", "text_ar": "الحكم على المعلمة لأن الكأس وُجد في مكتبها"},
            {"id": "o6", "text_ar": "اعتبار غياب القيد دليلاً على أن المشرف كذب"},
            {"id": "o7", "text_ar": "الاكتفاء بقول أكثر الطلاب"}],
        "free_text_prompt_ar": "اكتب في ثلاثة أسطر كيف تقدّر نسبة الترجيح بأن المعلمة هي من وضعته.",
    },
    "skills": [{"skill_id": "KO-FC-04-026", "track": "E"}, {"skill_id": "KO-FC-04B-002", "track": "E"}, {"skill_id": "KO-RS-05-004", "track": "B"}, {"skill_id": "KO-RS-05-002", "track": "D"}],
    "stage_hooks_ar": {"briefing": "الصندوق في الدرج… والسؤال: من وضعه هناك؟", "investigating": "كل قيد ناقص يسأل: بيد من كان الصندوق؟", "review": "قبل أن تغلق الملف: ما الذي لا تستطيع الاستمارة أن تقوله؟", "resolved": "أُغلق الملف. عادت العدسات إلى الخزانة، وصارت الاستمارة تُكتب في كل مرة."},
    "character_glyphs": {"rashid": "ر", "mazen": "م", "hadi": "ه", "dana": "د", "subhi": "ص", "najla": "ن", "fares": "ف"},
}
sc = {
    "accepted_conclusions": {
        "h_hadi": {"grade": 1, "note_ar": "استنتاج متسق مع الأدلة ويتطلب ذكر حدوده."},
        "h_sup": {"grade": 0, "note_ar": "يجعل مكان العثور دليلاً على من وضع، ويتجاهل السجلات المستقلة التي تبعد المشرف."},
        "h_mazen": {"grade": 0, "note_ar": "يبني على خلاف سابق وعلى كونه من وجد الصندوق، ولا قيد يقرّبه من المشغل."},
        "h_misfiled": {"grade": 0, "note_ar": "الصندوق غادر المشغل في حوزة شخص بعينه ولم يُنقل خطأً عند التنظيف."}},
    "confidence_band": {"h_hadi": [65, 90], "h_sup": [0, 15], "h_mazen": [0, 20], "h_misfiled": [0, 20]},
    "source_key": {"ev_found_report": "claim", "ev_custody_form": "primary_record", "ev_door_log": "primary_record", "ev_exhibit_post": "primary_record", "ev_patrol_log": "primary_record",
                   "ev_training_sheet": "primary_record", "ev_gate_log": "primary_record", "ev_office_lock_log": "primary_record", "ev_found_photo": "redisplay", "ev_sup_email": "primary_record",
                   "ev_mazen_stmt": "claim", "ev_rashid_stmt": "claim", "ev_hadi_stmt": "claim"},
    "link_key": {
        "h_hadi": {"ev_custody_form": "supports", "ev_door_log": "supports", "ev_exhibit_post": "supports", "ev_patrol_log": "supports", "ev_training_sheet": "supports", "ev_gate_log": "supports",
                   "ev_office_lock_log": "supports", "ev_found_photo": "neutral", "ev_hadi_stmt": "supports", "ev_sup_email": "neutral"},
        "h_sup": {"ev_found_report": "supports", "ev_sup_email": "supports", "ev_training_sheet": "weakens", "ev_gate_log": "weakens", "ev_office_lock_log": "weakens", "ev_found_photo": "weakens",
                  "ev_custody_form": "weakens", "ev_door_log": "weakens"},
        "h_mazen": {"ev_found_report": "supports", "ev_mazen_stmt": "supports", "ev_found_photo": "weakens", "ev_door_log": "weakens", "ev_custody_form": "weakens", "ev_gate_log": "neutral"},
        "h_misfiled": {"ev_door_log": "weakens", "ev_custody_form": "weakens", "ev_exhibit_post": "weakens", "ev_patrol_log": "weakens"},
    },
    "required_limits": ["l_content_unknown", "l_card_not_person"], "valid_mind_changers": ["m_sup_card", "m_door_lent", "m_photo_time"],
    "invalid_limits": ["l_invalid_place", "l_invalid_feud", "l_invalid_shy"],
    "decisive_evidence": ["ev_custody_form", "ev_door_log", "ev_exhibit_post", "ev_patrol_log", "ev_training_sheet", "ev_gate_log", "ev_office_lock_log", "ev_found_photo"],
    "timeline_requirement": [{"evidence_id": "ev_custody_form", "utc_minute": 55, "tol": 3}, {"evidence_id": "ev_door_log", "utc_minute": 72, "tol": 3},
                             {"evidence_id": "ev_exhibit_post", "utc_minute": 400, "tol": 5}, {"evidence_id": "ev_found_photo", "utc_minute": 1066, "tol": 3}, {"evidence_id": "ev_gate_log", "utc_minute": 1072, "tol": 4}],
    "refuted_hypotheses": ["h_sup", "h_mazen", "h_misfiled"],
    "transfer_key": {"valid": ["o1", "o2", "o3", "o4"], "invalid": ["o5", "o6", "o7"]},
}
assemble(CID, meta, premise, {"characters": chars, "locations": locations, "objects": objects, "organizations": orgs}, ["hadi"],
         "لم يأخذ المشرف الصندوق. أخرجه هادي من المشغل بعد الإحصاء ولم يكتب في الاستمارة، ثم تركه في الدرج المفتوح صباح الثلاثاء قبل وصول المشرف خوفاً من الجرد، ولم يقصد اتهام أحد.",
         ["f_sup_not_there", "f_hadi_had_box"], claims, timeline, ck, hyps, mis, los, ref, hints, topics, steps, ending["alt"], ending["notlimits"], ending["notes"], ui, sc)
