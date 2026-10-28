#!/usr/bin/env python3
# Case c027 «الكأس التي غادرت قبل القفل» — archetype ARC-39 «تحدي القارئ في نادي الأثر» (library), age band 16-18, difficulty 3. A non-lethal
# «impossible» puzzle (a club cup vanishes from a locked glass cabinet) with all constraints stated up front. Teaches: when a puzzle says
# «impossible», test the PREMISE first (was the thing really there when the lock closed?); compare rival solutions by COVERAGE (does it explain every
# clue), CONSISTENCY (does any clue contradict it) and ECONOMY (how many extra assumptions); and weigh each clue by a likelihood ratio (نسبة الترجيح):
# how much more often would we see it if solution A were true than if B were. Two rival «clever» solutions (a copied key, a removable back wall)
# are refuted by key facts only. No-culprit convention: Yara (who took the cup to the storeroom for the dusting rota and forgot to tell anyone) is
# recorded in culprit_ids. DEVIATIONS from ARC-39 (honest list): the archetype's «you now hold everything you need» commitment gate (after which the
# evidence view closes) is NOT built — the engine has no such gate; the player simply opens the deduction view when ready. Scoring is deterministic
# (coverage/consistency/economy are carried by the evidence links and the rule-outs), the written argument stays human-scored. The newcomer-friendly
# rule explanations are placed in the intro card (ev_compare_card). Time lab omitted (labs: []); timeline requirement used.
# Replaces an earlier draft of c027 (a market-scale case) because c022 already builds that archetype. Calendar (fictional): minute 0 = Thursday 14:00.
# All names, places and records are fictional.
# Usage: gen_c027.py OUT_DIR
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

CID = "c027_cup_cabinet"
ch("kinan", "كنان الصباغ", "witness", "رئيس نادي الألغاز في مدرسة الأطلال",
   "واثق ومرح، يحب التحدي ويصرّ على أن الأمر مستحيل، لكنه يقبل أن يُراجع كل ما قاله. يعرف أن المفتاح معه ولم يفتح الخزانة قبل الاجتماع.",
   ["أن يبقى التحدي نزيهاً", "أن يجد أحدهم الحل بالدليل"],
   [L("kn_greet", "greeting", "أعلنت التحدي بنفسي: الخزانة مقفلة ومفتاحها معي والزجاج سليم."),
    L("kn_says", "reveal", "أغلقت الخزانة ظهراً ولم أفتحها حتى بدأ الاجتماع، وحين فتحتها بعد الخامسة والنصف كانت فارغة والزجاج سليم.", ["f_kinan_says"], ["cl_locked_room"]),
    L("kn_inspect", "reveal", "فحصنا الخزانة عند فتحها: الزجاج والقفل سليمان، والجدار الخلفي مثبّت بمسامير من الداخل ولم يمسّ، وسجلنا ذلك في ورقة.", ["f_inspection_exists"]),
    L("kn_unknown", "deflect_unknown", "لا أعرف أكثر."),
    L("kn_off", "deflect_offtopic", "اسألني عن التحدي."),
    L("kn_bye", "farewell", "إن ظهر حل مقنع فسأعترف به.")])
ch("yara", "يارا الحداد", "suspect", "أمينة مكتبة النادي",
   "منظمة وخجولة، تكره أن تُنسب إليها غلطة، فتؤجل الاعتراف حتى ترى أن السجلات قالتها. لا تقصد الإساءة لأحد.",
   ["ألا تُحرج أمام النادي", "أن تعود الكأس إلى مكانها"],
   [L("yr_greet", "greeting", "أنا أرتب كتب النادي وأغبّرها. لا أعرف شيئاً عن الكأس."),
    L("yr_deny", "reveal", "لم أفتح الخزانة يوم الخميس.", None, ["cl_yara_never"]),
    L("yr_refuse", "refuse_secret", "أفضّل ألا أتكلم الآن."),
    L("yr_moved", "reveal", "فتحت الخزانة بالمفتاح الثاني قبل الاجتماع لأنني كلّفت بتغبير الكأس، فنقلتها إلى المخزن لأغسلها وأتركها تجف، وأقفلت الخزانة وأنا أظن أن الرئيس يعلم؛ ثم نسيت أن أخبره أو أن أعيدها، وخفت أن أبدو مهملة.", ["f_yara_moved"]),
    L("yr_unknown", "deflect_unknown", "لا أذكر."),
    L("yr_off", "deflect_offtopic", "اسألني عن مكتبة النادي."),
    L("yr_bye", "farewell", "كان عليّ أن أكتب ورقة على الخزانة.")])
ch("basel", "باسل المنصور", "suspect", "عضو في النادي، هاوي أقفال",
   "متحمس بالأقفال ويحب الشرح، ويبدو مريباً لأنه يعرف كثيراً. يجيب بما فعله ويعطي الإيصالات.",
   ["أن يُصدَّق", "أن يُحل اللغز بحق"],
   [L("bs_greet", "greeting", "أعرف الأقفال، وهذا لا يجعلني فاعلاً."),
    L("bs_copy", "reveal", "قبل شهر نسخت مفتاح باب المخزن للنادي عند قفّال، وعندي الإيصال، ولم أنسخ مفتاح الخزانة.", ["f_copy_made"]),
    L("bs_says", "reveal", "كنت في الاجتماع من الرابعة إلى الخامسة والنصف ولم أقم من مكاني.", ["f_basel_says"]),
    L("bs_unknown", "deflect_unknown", "لا أعرف."),
    L("bs_off", "deflect_offtopic", "اسألني عن الأقفال."),
    L("bs_bye", "farewell", "افحص الإيصال بنفسك.")])
ch("talla", "تالا الخوري", "witness", "مصوّرة النشرة الشهرية للنادي",
   "دقيقة وتحتفظ بصورها بوقتها، وتقول إن ساعة هاتفها مضبوطة من الشبكة. لا تعرف شيئاً عن الكأس.",
   ["أن تبقى صورها سليمة"],
   [L("tl_greet", "greeting", "أصوّر للنشرة فقط."),
    L("tl_photo", "reveal", "صوّرت الخزانة لنشرة الشهر قبل الاجتماع بدقائق، وفي الصورة ساعة الحائط.", ["f_photo_exists"]),
    L("tl_unknown", "deflect_unknown", "لم أنتبه."),
    L("tl_off", "deflect_offtopic", "اسألني عن الصور."),
    L("tl_bye", "farewell", "الصورة كما التُقطت.")])
ch("nadine", "نادين العلمي", "witness", "أمينة سر النادي",
   "منظمة وتكتب كل شيء، وتقرأ من الأوراق ولا تفسر. لا تتهم أحداً.",
   ["أن تبقى أوراق النادي صحيحة"],
   [L("nd_greet", "greeting", "أحتفظ بأوراق النادي."),
    L("nd_sheet", "reveal", "لخزانة الكؤوس مفتاحان: واحد مع الرئيس وآخر في صندوق النادي، وكل فتح للخزانة يُكتب في ورقة المفتاح باسم من فتحها.", ["f_key_sheet_exists"]),
    L("nd_rota", "reveal", "عندنا جدول مهام أسبوعي للتنظيف والتغبير، وفيه مهمة الخزانة والكأس يوم الخميس.", ["f_rota_exists"]),
    L("nd_unknown", "deflect_unknown", "ليس عندي علم."),
    L("nd_off", "deflect_offtopic", "اسألني عن الأوراق."),
    L("nd_bye", "farewell", "الورقة موقّعة.")])
ch("dawood", "داود العلمي", "witness", "أمين مخزن النادي",
   "كبير في السن ومنظم، يسجّل كل ما يدخل المخزن ويخرج، ويقرأ من إيصالاته.",
   ["أن يبقى المخزن مضبوطاً"],
   [L("dw_greet", "greeting", "أستلم الأغراض وأسجّلها."),
    L("dw_slip", "reveal", "كل غرض يدخل المخزن أكتب له إيصال استلام بوقته واسم من سلّمه.", ["f_slip_exists"]),
    L("dw_reader", "reveal", "باب المخزن بقارئ بطاقات يسجّل كل دخول وخروج بوقته.", ["f_store_reader_exists"]),
    L("dw_unknown", "deflect_unknown", "لا أعرف."),
    L("dw_off", "deflect_offtopic", "اسألني عن المخزن."),
    L("dw_bye", "farewell", "الإيصال لا يكذب.")])

locations = [{"id": "loc_club", "name_ar": "غرفة النادي", "description_ar": "غرفة فيها خزانة زجاجية للكؤوس تقفل بمفتاحين."},
             {"id": "loc_store", "name_ar": "مخزن النادي", "description_ar": "غرفة صغيرة بقارئ بطاقات على بابها."}]
objects = [{"id": "obj_cup", "name_ar": "الكأس الخضراء", "description_ar": "كأس بلاستيكية خضراء رمزية للنادي، لا قيمة مالية لها."}]
orgs = [{"id": "org_club", "name_ar": "نادي الألغاز", "description_ar": "نادٍ في مدرسة الأطلال الخيالية."}]

F("f_cup_vanished", "اختفت الكأس الخضراء من خزانة زجاجية مقفلة في غرفة النادي، واكتُشف ذلك عند فتح الخزانة بعد اجتماع الخميس.", "event", ["obj_cup"], 0)
F("f_challenge", "أعلن رئيس النادي أن الخزانة كانت مقفلة ومفتاحها معه وزجاجها سليم، وأن أحداً لن يفسّر ما جرى.", "attribute", ["kinan"], 0)
F("f_rules", "شروط التحدي المعلنة: يقدّم كل حل تفسيراً لكل القرائن، ولا يناقض أي قرينة، وبأقل الافتراضات.", "state", ["org_club"], 0)
F("f_kinan_says", "يقول الرئيس إنه أغلق الخزانة ظهراً ولم يفتحها حتى بدأ الاجتماع، وإنها كانت فارغة عند فتحها.", "attribute", ["kinan"], 1)
F("f_inspection_exists", "سجل النادي فحصاً عند فتح الخزانة: القفل والزجاج سليمان والجدار الخلفي لم يمسّ.", "state", ["loc_club"], 1, T(210), "loc_club")
F("f_copy_made", "نسخ باسل قبل شهر مفتاح باب المخزن لدى قفّال ويملك إيصال النسخ.", "event", ["basel"], 1)
F("f_basel_says", "يقول باسل إنه كان في الاجتماع طوال الوقت ولم يقم من مكانه.", "attribute", ["basel"], 1)
F("f_photo_exists", "التقطت مصوّرة النشرة صورة للخزانة قبل الاجتماع تظهر فيها ساعة الحائط.", "event", ["talla"], 1, T(110), "loc_club")
F("f_key_sheet_exists", "تُكتب كل مرة تفتح فيها خزانة الكؤوس في ورقة المفتاح باسم من فتحها.", "state", ["nadine"], 1, None, "loc_club")
F("f_rota_exists", "للنادي جدول تنظيف أسبوعي فيه مهمة الخزانة والكأس يوم الخميس.", "state", ["nadine"], 1)
F("f_slip_exists", "يكتب أمين المخزن إيصال استلام لكل غرض يدخل المخزن بوقته واسم مسلّمه.", "state", ["dawood"], 1, None, "loc_store")
F("f_store_reader_exists", "يسجّل قارئ باب المخزن كل دخول وخروج بالبطاقة.", "state", ["dawood"], 1, None, "loc_store")
F("f_empty_before", "كانت الخزانة فارغة قبل بدء الاجتماع، فلم تغادرها الكأس أثناء قفلها ولا يلزم لتفسير الغياب مفتاح ثالث ولا جدار متحرك.", "relation", ["obj_cup", "loc_club"], 3, T(100, "exact", 120), "loc_club", ["KO-RS-06-008", "KO-RS-05-004"])
F("f_yara_moved", "نقلت يارا الكأس إلى المخزن قبل الاجتماع ضمن مهمة التنظيف وأقفلت الخزانة دون إعلام الرئيس.", "event", ["yara", "obj_cup"], 3, T(90, "exact", 105), "loc_store", ["KO-RS-05-004", "KO-FC-04-026"])

claims = [
    {"id": "cl_locked_room", "statement_ar": "الكأس كانت في الخزانة المقفلة حتى بدأ الاجتماع، فاختفاؤها لغز.", "kind": "honest_mistake", "held_by": ["kinan"], "true_fact_id": "f_empty_before",
     "contradicted_by_evidence_ids": ["ev_newsletter_photo", "ev_store_slip", "ev_store_door_log"]},
    {"id": "cl_yara_never", "statement_ar": "لم أفتح الخزانة يوم الخميس.", "kind": "lie", "held_by": ["yara"], "true_fact_id": "f_yara_moved",
     "contradicted_by_evidence_ids": ["ev_key_sheet", "ev_dust_rota", "ev_store_slip"]},
]
timeline = [
    {"id": "te_open", "description_ar": "يارا تفتح الخزانة بالمفتاح الثاني.", "time": T(90), "location_id": "loc_club", "actor_ids": ["yara"], "fact_ids": ["f_yara_moved"], "motivated_by_ar": "مهمة التغبير في جدول النادي"},
    {"id": "te_store_in", "description_ar": "يارا في المخزن تسلّم الكأس لأمين المخزن.", "time": T(95, "exact", 102), "location_id": "loc_store", "actor_ids": ["yara", "dawood"], "fact_ids": ["f_yara_moved"], "motivated_by_ar": "غسل الكأس وتجفيفها"},
    {"id": "te_lock", "description_ar": "يارا تقفل الخزانة.", "time": T(105), "location_id": "loc_club", "actor_ids": ["yara"], "fact_ids": ["f_empty_before"], "motivated_by_ar": "إنهاء المهمة"},
    {"id": "te_photo", "description_ar": "تالا تصوّر الخزانة للنشرة.", "time": T(110), "location_id": "loc_club", "actor_ids": ["talla"], "fact_ids": ["f_photo_exists"], "motivated_by_ar": "نشرة الشهر"},
    {"id": "te_meeting", "description_ar": "يبدأ اجتماع النادي ويعلن الرئيس التحدي.", "time": T(120, "exact", 210), "location_id": "loc_club", "actor_ids": ["kinan", "basel"], "fact_ids": ["f_challenge"], "motivated_by_ar": "اجتماع النادي الأسبوعي"},
    {"id": "te_inspect", "description_ar": "فتح الخزانة وفحصها وتسجيل أنها فارغة.", "time": T(210), "location_id": "loc_club", "actor_ids": [], "fact_ids": ["f_inspection_exists"]},
]

V("ev_challenge", "ورقة التحدي", "documentary",
  "نادي الألغاز — ورقة التحدي (بخط الرئيس) — الخميس\nالمعطيات: الكأس الخضراء كانت في خزانة الزجاج. المفتاح الأول معي. الزجاج سليم. الخزانة فارغة عند فتحها 17:30.\nالشروط: أي حل يفسّر كل القرائن، ولا يناقض أيّاً منها، وبأقل الافتراضات.\nإعلان: لن يفسّر أحد كيف خرجت الكأس.",
  ["a_read_challenge"], ["f_cup_vanished", "f_challenge", "f_rules"], "weak",
  "ورقة تحدٍّ تعلن استحالة وتضع معطيات؛ وجود الكأس داخل الخزانة لحظة الإقفال معطى يحتاج إلى سجل يؤيده.", red=True, loc="loc_club")
V("ev_compare_card", "بطاقة مقارنة الحلول", "documentary",
  "بطاقة تدريب خيالية للمقارنة بين حلين متنافسين\nلكل قرينة اسأل: كم مرة أراها لو كان الحل (أ) صحيحاً؟ وكم مرة أراها لو كان الحل (ب) صحيحاً؟\nمثال بأرقام للتمرين: قرينة «إيصال استلام في المخزن» — تحت حل «نُقلت للتنظيف»: 9 من 10، وتحت حل «فُتحت بمفتاح مقلّد»: 1 من 20 → نسبة الترجيح نحو 18 لصالح الأول.\nقرينة «قفل سليم» — تحت الحلين نحو 9 من 10 → النسبة نحو 1، فلا تفرّق بين الحلين.\nتذكير: نسبة الترجيح تقارن تكرارين، وليست احتمال حل واحد.",
  ["a_read_card"], [], "moderate",
  "نموذج تعليمي بأرقام للتدريب لا تخص هذه الغرفة؛ يُظهر طريقة المقارنة ولا يقيس القرائن الحقيقية.", loc="loc_club")
V("ev_key_sheet", "ورقة مفتاح خزانة الكؤوس", "documentary",
  "نادي الألغاز — ورقة المفتاح (مفتاحان: الأول مع الرئيس، الثاني في صندوق النادي)\nالخميس 15:30 — فتح بالمفتاح الثاني — الاسم: ي. الحداد — السبب: مهمة الغبار\nالخميس 15:45 — قفل — ي. الحداد\nالخميس 16:00 — الرئيس يجرّب المقبض: مقفل (دون فتح)\nالخميس 17:30 — فتح بالمفتاح الأول — ك. الصباغ",
  ["a_get_key_sheet"], ["f_key_sheet_exists", "f_yara_moved", "f_empty_before"], "strong",
  "ورقة بخط أمينة السر وتوقيعات الفاتحين؛ تثبت فتحاً وقفلاً قبل الاجتماع، ولا تقول ماذا حُمل منها ولا إلى أين.", ko="KO-FC-04-026", loc="loc_club")
V("ev_dust_rota", "جدول مهام التنظيف", "documentary",
  "نادي الألغاز — جدول التنظيف الأسبوعي (بخط أمينة السر)\nالخميس قبل الاجتماع: خزانة الكؤوس وغسل الكأس الخضراء وتجفيفها — المكلّفة: ي. الحداد\nالجمعة: ترتيب الكراسي — م. القاسم",
  ["a_get_dust_rota"], ["f_rota_exists", "f_yara_moved"], "moderate",
  "جدول مهام يبيّن من كُلّف لا ما فُعل؛ يقوى حين يوافقه سجل لا يعتمد عليه.", loc="loc_club")
V("ev_newsletter_photo", "صورة الخزانة للنشرة", "digital",
  "هاتف مصوّرة النشرة — بيانات الصورة: الخميس 15:50 (وقت الشبكة)\nخزانة الكؤوس مقفلة، وعلى رفها العلوي أثر دائري باهت لقاعدة كأس ولا كأس فوقه؛ وفي الخلفية ساعة الحائط تشير إلى 15:50.",
  ["a_get_newsletter_photo"], ["f_photo_exists", "f_empty_before"], "strong",
  "لقطة واحدة قبل الاجتماع؛ تبيّن خلو الرف ولا تبيّن إلى أين ذهبت الكأس ولا من نقلها.", loc="loc_club")
V("ev_store_slip", "إيصال استلام المخزن", "documentary",
  "مخزن النادي — إيصال استلام — الخميس 15:40 (بخط أمين المخزن)\nالغرض: كأس خضراء للغسل والتجفيف\nالمسلِّم: ي. الحداد · المستلم: د. العلمي\nملاحظة: «ستعود قبل نهاية اليوم» — ولم يُسجَّل لها إرجاع.",
  ["a_get_store_slip"], ["f_slip_exists", "f_yara_moved", "f_empty_before"], "strong",
  "إيصال بخط أمين المخزن؛ يبيّن من سلّم الكأس ومتى، وعدم تسجيل الإرجاع لا يبيّن لماذا.", ko="KO-FC-04-026", loc="loc_store")
V("ev_store_door_log", "سجل قارئ باب المخزن", "digital",
  "مخزن النادي — قارئ البطاقات — الخميس\n15:35 دخول: ي. الحداد\n15:42 خروج: ي. الحداد\nلا دخول ولا خروج لأي بطاقة بين 16:00 و17:45 حين دخل أمين المخزن.",
  ["a_get_store_door_log"], ["f_store_reader_exists", "f_yara_moved", "f_empty_before"], "strong",
  "يسجّل مرور بطاقة لا شخصاً؛ قوته في اتفاقه مع الإيصال بخط أمين المخزن وهو نظام منفصل.", loc="loc_store")
V("ev_cabinet_inspect", "ورقة فحص الخزانة عند فتحها", "documentary",
  "نادي الألغاز — فحص الخزانة — الخميس 17:30\nالزجاج سليم · القفل سليم · الجدار الخلفي مثبّت بأربعة مسامير من الداخل ولم يمسّ · الرف الأعلى فارغ",
  ["a_get_cabinet_inspect"], ["f_inspection_exists"], "moderate",
  "يثبت سلامة القفل والزجاج والجدار بعد الاجتماع، ولا يبيّن متى غادرت الكأس الخزانة.", loc="loc_club")
V("ev_copy_receipt", "إيصال القفّال", "documentary",
  "ورشة قفّال «الأطلال» — إيصال نسخ مفتاح\nمنذ شهر: نسخة واحدة لمفتاح باب المخزن — الطالب: باسل المنصور\nلا قيد بنسخ مفتاح آخر.",
  ["a_get_copy_receipt"], ["f_copy_made"], "moderate",
  "يثبت نسخ مفتاح المخزن لا مفتاح الخزانة؛ والإمكان ليس فعلاً.", red=True, loc="loc_club")
V("ev_kinan_stmt", "إفادة الرئيس (ملخص)", "testimonial",
  "ملخص إفادة كنان الصباغ:\n«أغلقت الخزانة ظهراً وفتحتها 17:30 فكانت فارغة. أنا متأكد أنها كانت فيها حتى بدأ الاجتماع.»",
  ["a_note_kinan"], ["f_kinan_says"], "weak",
  "إفادة صاحب التحدي؛ ثقته لا تغني عن سجل، وقد يقصد بالإغلاق حركة سابقة لم يرها بنفسه.", loc="loc_club")
V("ev_basel_stmt", "إفادة باسل (ملخص)", "testimonial",
  "ملخص إفادة باسل المنصور:\n«كنت في الاجتماع طوال الوقت ولم أقم. نسخت مفتاح المخزن لا الخزانة، وعندي الإيصال.»",
  ["a_note_basel"], ["f_basel_says"], "weak",
  "إفادة صاحب الشأن عن نفسه؛ تُقاس بالسجلات لا بمعرفته بالأقفال.", loc="loc_club")
V("ev_yara_stmt", "إفادة يارا بعد المواجهة (ملخص)", "testimonial",
  "ملخص إفادة يارا الحداد:\n«فتحت الخزانة قبل الاجتماع لأغبّر الكأس، فنقلتها إلى المخزن لأغسلها، ونسيت أن أخبر الرئيس. لم أقصد أي أذى.»",
  ["a_note_yara"], ["f_yara_moved"], "moderate",
  "اعتراف بعد عرض سجل عليها؛ يؤيد سجلات سبقته ولا يغني عنها.", loc="loc_club")

I("i_before_a", [E("ev_newsletter_photo"), E("ev_key_sheet")], "fact", "f_empty_before", "establishes", "strong",
  "الرف خالٍ في صورة بساعة ظاهرة قبل بدء الاجتماع، وورقة المفتاح تسجّل فتحاً وقفلاً في الفترة نفسها باسم غير الرئيس؛ فالاختفاء سابق للقفل الأخير.", ["KO-RS-06-008", "KO-RS-05-004"])
I("i_before_b", [E("ev_store_slip"), E("ev_store_door_log")], "fact", "f_empty_before", "establishes", "strong",
  "إيصال المخزن وقارئ بابه، وهما نظامان لا علاقة لهما بالنادي ولا بالصورة، يضعان الكأس في المخزن قبل الاجتماع بنحو ثلث ساعة.", ["KO-RS-05-004", "KO-FC-04-026"])
I("i_moved_a", [E("ev_key_sheet"), E("ev_dust_rota")], "fact", "f_yara_moved", "establishes", "strong",
  "من فتح الخزانة قبل الاجتماع هي المكلّفة في الجدول بالكأس والخزانة، فالفتح كان للمهمة وليس لإخراج الكأس خفية.", ["KO-RS-05-004", "KO-FC-04-026"])
I("i_moved_b", [E("ev_store_slip"), E("ev_store_door_log")], "fact", "f_yara_moved", "establishes", "strong",
  "الإيصال باسم المسلِّمة وبطاقتها وحدها دخلت المخزن وخرجت في ذلك الوقت؛ فهي التي نقلت الكأس.", ["KO-RS-05-004", "KO-FC-04-026"])
I("i_cl_kinan", [Fa("f_empty_before")], "claim", "cl_locked_room", "contradicts_claim", "strong",
  "الاعتقاد بأن الكأس كانت في الخزانة وقت الاجتماع لم يُفحص بسجل؛ والسجلات تضعها في مكان آخر قبله.", ["KO-RS-05-014"])
I("i_cl_yara", [Fa("f_yara_moved")], "claim", "cl_yara_never", "contradicts_claim", "strong",
  "اسمها في ورقة المفتاح وفي الإيصال وفي جدول المهام، فنفي فتح الخزانة لا يوافق السجلات.", ["KO-RS-05-014"])
I("i_support_dust", [Fa("f_empty_before"), Fa("f_yara_moved")], "hypothesis", "h_dusting", "supports", "strong",
  "هذا الحل يفسّر كل القرائن: الرف الخالي والورقة والإيصال والجدول وسلامة القفل والجدار، بافتراض واحد هو أن النقل لم يُعلَن؛ وهي القرائن التي تزيد ترجيحه على كل حل منافس بنسبة كبيرة.", ["KO-FC-04-009", "KO-RS-06-007"])
I("i_rule_copy", [Fa("f_empty_before"), Fa("f_yara_moved")], "hypothesis", "h_copykey", "rules_out", "conclusive",
  "من احتاج مفتاحاً مقلّداً لفتح الخزانة أثناء الاجتماع حلّ مشكلة لم تقع، فالرف كان خالياً قبله؛ ونسخ مفتاح المخزن لا يمسّ الخزانة.", ["KO-RS-06-008", "KO-FC-04-009"])
I("i_rule_panel", [Fa("f_empty_before"), Fa("f_yara_moved")], "hypothesis", "h_panel", "rules_out", "strong",
  "جدار متحرك يفسّر خروجاً أثناء القفل، والخروج حدث قبله؛ فالحل يضيف افتراضات ولا يضيف تفسيراً.", ["KO-RS-06-008", "KO-FC-04-009"])
I("i_rule_staged", [Fa("f_empty_before"), Fa("f_yara_moved")], "hypothesis", "h_staged", "rules_out", "strong",
  "الكأس نُقلت إلى المخزن بيد غير يد الرئيس وبإيصال موقّع، فلا يلزم أن يكون التحدي مدبراً ولا أن يكون الرئيس هو الناقل.", ["KO-RS-06-008"])

ck = [
    {"character_id": "kinan", "knows": [K("f_kinan_says"), K("f_inspection_exists", "witnessed")], "hides": [], "believes": [{"claim_id": "cl_locked_room", "stance": "sincere"}]},
    {"character_id": "yara", "knows": [], "hides": [{"fact_id": "f_yara_moved", "reveal_when": {"presented": {"evidence_id": "ev_store_slip", "to_character": "yara"}}, "cover_claim_id": "cl_yara_never", "reveal_line_id": "yr_moved"}],
     "believes": [{"claim_id": "cl_yara_never", "stance": "deliberate_lie"}]},
    {"character_id": "basel", "knows": [K("f_copy_made"), K("f_basel_says")], "hides": [], "believes": []},
    {"character_id": "talla", "knows": [K("f_photo_exists", "professional")], "hides": [], "believes": []},
    {"character_id": "nadine", "knows": [K("f_key_sheet_exists", "professional"), K("f_rota_exists", "professional")], "hides": [], "believes": []},
    {"character_id": "dawood", "knows": [K("f_slip_exists", "professional"), K("f_store_reader_exists", "professional")], "hides": [], "believes": []},
]
hyps = [
    {"id": "h_copykey", "statement_ar": "فتح أحد الأعضاء الخزانة أثناء الاجتماع بمفتاح مقلّد وأخذ الكأس.", "is_true": False, "plausibility_at_start": "high", "suspect_id": "basel"},
    {"id": "h_panel", "statement_ar": "خرجت الكأس أثناء القفل من جدار الخزانة الخلفي.", "is_true": False, "plausibility_at_start": "medium"},
    {"id": "h_dusting", "statement_ar": "نُقلت الكأس إلى المخزن قبل الاجتماع ضمن مهمة التنظيف ولم يعلم الرئيس.", "is_true": True, "plausibility_at_start": "low", "suspect_id": "yara"},
    {"id": "h_staged", "statement_ar": "دبّر الرئيس الاختفاء ليربح التحدي.", "is_true": False, "plausibility_at_start": "medium", "suspect_id": "kinan"},
]
mis = [
    {"id": "rh_copy", "points_to_hypothesis_id": "h_copykey", "planted_via_ar": "باسل هاوي أقفال ونسخ مفتاحاً قبل شهر.", "evidence_ids": ["ev_copy_receipt"],
     "refuted_by_inference_ids": ["i_rule_copy", "i_before_a", "i_before_b"],
     "fairness_note_ar": "الإيصال نفسه يذكر مفتاح المخزن لا الخزانة، والسجلات تضع الكأس خارج الخزانة قبل الاجتماع؛ فالمفتاح المقلّد حل لمشكلة لم تقع."},
    {"id": "rh_locked", "points_to_hypothesis_id": "h_panel", "planted_via_ar": "الخزانة بدت مقفلة وسليمة، فلا مفر من منفذ خفي.", "evidence_ids": ["ev_challenge", "ev_cabinet_inspect"],
     "refuted_by_inference_ids": ["i_rule_panel", "i_before_a"],
     "fairness_note_ar": "المعطى بأن الكأس كانت في الخزانة لم يُسند بسجل، وقد وفّرت السجلات ما يبيّن عكسه؛ وجدار سليم لا يفسّر شيئاً حدث قبل القفل."},
    {"id": "rh_staged", "points_to_hypothesis_id": "h_staged", "planted_via_ar": "الرئيس أعلن الاستحالة وهو من يملك المفتاح الأول.", "evidence_ids": ["ev_kinan_stmt", "ev_challenge"],
     "refuted_by_inference_ids": ["i_rule_staged", "i_moved_b"],
     "fairness_note_ar": "ورقة المفتاح تبيّن أنه لم يفتح الخزانة قبل 17:30، والإيصال باسم غيره؛ وإعلان التحدي ليس دليلاً على تدبيره."},
]
los = std_los("يختبر مقدمة «المستحيل» قبل البحث عن حل خفي، ويقارن الحلول المتنافسة بالتغطية والاتساق والاقتصاد، ويقدّر قوة كل قرينة بنسبة الترجيح: كم مرة تظهر لو صح حل ولو صح آخر.", "KO-FC-04-009",
              ["يسأل هل كانت الكأس في الخزانة حقاً", "يقارن حلين بنسبة بين تكرارين", "يفضّل الحل الأقل افتراضاً"],
              "يصوغ نسبة الترجيح بين الحلول المتنافسة بحدودها.")
ref = ("ليست الواقعة اختفاء من خزانة مقفلة، فالرف كان خالياً قبل الاجتماع. صورة بساعة ظاهرة تُظهر الرف بلا كأس وورقة المفتاح تسجّل فتحاً وقفلاً باسم يارا، وإيصال المخزن وقارئ بابه يضعان الكأس عندها هناك قبل الاجتماع بنحو ثلث ساعة، وجدول المهام يكلّفها بالتنظيف. المفتاح المقلّد والجدار الخلفي والتدبير المتعمّد حلول لا يلزمها شيء مما جرى، فتخسر أمام تفسير واحد بافتراض واحد هو أن النقل لم يُعلَن. حدود الاستنتاج: لا نعرف لماذا لم تُرجع الكأس ولا لماذا لم تخبر الرئيس، ولا تثبت السجلات ماذا قالت بالضبط، واعترافها لا يغني عنها.")
hints = [
    H("hg1", 1, "metacognitive", "حين يعلن لغز أنه مستحيل، اسأل أولاً: ما المعطى الذي لم يُثبَت بعد؟", {"always": True}, None, 0.02),
    H("hg2", 2, "focus_area", "اسأل: من فتح الخزانة قبل الاجتماع؟ وهل كانت الكأس فيها حقاً حين أُقفلت؟", he("ev_challenge"), None, 0.04),
    H("hg3", 3, "pointer", "ابحث عن أوراق لا يكتبها الرئيس: ورقة المفتاح، وصورة بساعة ظاهرة، وسجلات المخزن.", he("ev_challenge"), None, 0.08),
    H("hb1", 1, "metacognitive", "هل يمكن أن يكون ما جرى قد جرى قبل القفل لا بعده؟", he("ev_challenge"), "i_before_a", 0.02),
    H("hb2", 2, "pointer", "اسأل أمينة السر عن ورقة المفتاح، ومصوّرة النشرة عن صورتها.", he("ev_challenge"), "i_before_a", 0.06),
    H("hm1", 1, "metacognitive", "أي نظام آخر قد يكون سجّل مرور الكأس؟", he("ev_challenge"), "i_before_b", 0.02),
    H("hm2", 2, "pointer", "اسأل أمين المخزن عن إيصالاته وقارئ بابه.", he("ev_challenge"), "i_before_b", 0.06),
]
Act("a_read_challenge", "examine", "اقرأ ورقة التحدي", al, [G("ev_challenge")], "loc_club", "READ_CHALLENGE")
Act("a_read_card", "examine", "اقرأ بطاقة مقارنة الحلول", al, [G("ev_compare_card")], "loc_club", "READ_CARD")
interviews([("kinan", "كنان"), ("yara", "يارا"), ("basel", "باسل"), ("talla", "تالا"), ("nadine", "نادين"), ("dawood", "داود")])
get("ev_key_sheet", "اطلب ورقة مفتاح الخزانة", fu("f_key_sheet_exists"), "loc_club")
get("ev_dust_rota", "اطلب جدول مهام التنظيف", fu("f_rota_exists"), "loc_club")
get("ev_newsletter_photo", "اطلب صورة الخزانة للنشرة", fu("f_photo_exists"), "loc_club", "GET_PHOTO")
get("ev_store_slip", "اطلب إيصال استلام المخزن", fu("f_slip_exists"), "loc_store")
get("ev_store_door_log", "اطلب سجل قارئ باب المخزن", fu("f_store_reader_exists"), "loc_store", "GET_STORE_LOG")
get("ev_cabinet_inspect", "اطلب ورقة فحص الخزانة", fu("f_inspection_exists"), "loc_club", "GET_INSPECT")
get("ev_copy_receipt", "اطلب إيصال القفّال", fu("f_copy_made"), "loc_club", "GET_RECEIPT")
Act("a_note_kinan", "examine", "دوّن إفادة الرئيس", fu("f_kinan_says"), [G("ev_kinan_stmt")], "kinan", "NOTE_KINAN")
Act("a_note_basel", "examine", "دوّن إفادة باسل", fu("f_basel_says"), [G("ev_basel_stmt")], "basel", "NOTE_BASEL")
Act("a_note_yara", "examine", "دوّن إفادة يارا", fu("f_yara_moved"), [G("ev_yara_stmt")], "yara", "NOTE_YARA")
Act("p_slip_yara", "present_evidence", "اعرض إيصال المخزن على يارا", {"presented": {"evidence_id": "ev_store_slip", "to_character": "yara"}}, [{"op": "emit_event", "ref_id": "PRESENTED_SLIP"}], "yara", "P_SLIP_YARA", 0)
tail_actions()
topics = [
    {"id": "t_kinan", "label_ar": "متى أغلقت الخزانة", "example_questions_ar": ["متى أغلقت الخزانة؟", "هل فتحتها قبل الاجتماع؟"], "fact_ids": ["f_kinan_says"], "claim_ids": ["cl_locked_room"]},
    {"id": "t_inspect", "label_ar": "فحص الخزانة", "example_questions_ar": ["ماذا وجدتم عند فتحها؟"], "fact_ids": ["f_inspection_exists"]},
    {"id": "t_yara_open", "label_ar": "فتح الخزانة يوم الخميس", "example_questions_ar": ["هل فتحتِ الخزانة؟"], "fact_ids": [], "claim_ids": ["cl_yara_never"]},
    {"id": "t_yara_moved", "label_ar": "ما فعلتِه بالكأس", "example_questions_ar": ["ماذا فعلتِ بالكأس؟"], "fact_ids": ["f_yara_moved"]},
    {"id": "t_copy", "label_ar": "نسخ المفتاح", "example_questions_ar": ["هل نسخت مفتاحاً؟"], "fact_ids": ["f_copy_made"]},
    {"id": "t_basel_where", "label_ar": "أين كنت أثناء الاجتماع", "example_questions_ar": ["هل غادرت مكانك؟"], "fact_ids": ["f_basel_says"]},
    {"id": "t_photo", "label_ar": "صورة النشرة", "example_questions_ar": ["هل صوّرت الخزانة؟"], "fact_ids": ["f_photo_exists"]},
    {"id": "t_sheet", "label_ar": "ورقة المفتاح", "example_questions_ar": ["كيف تُسجَّل مفاتيح الخزانة؟"], "fact_ids": ["f_key_sheet_exists"]},
    {"id": "t_rota", "label_ar": "جدول المهام", "example_questions_ar": ["من كُلّف بتنظيف الكأس؟"], "fact_ids": ["f_rota_exists"]},
    {"id": "t_slip", "label_ar": "إيصالات المخزن", "example_questions_ar": ["كيف تسجّل ما يدخل المخزن؟"], "fact_ids": ["f_slip_exists"]},
    {"id": "t_reader", "label_ar": "قارئ باب المخزن", "example_questions_ar": ["ماذا يسجّل القارئ؟"], "fact_ids": ["f_store_reader_exists"]},
]
steps = [
    (1, "اختبر مقدمة اللغز: لا شيء في الورقة يثبت أن الكأس كانت في الخزانة وقت القفل الأخير؛ بل صورة بساعة ظاهرة تُظهر الرف خالياً قبل الاجتماع.", ["ev_newsletter_photo", "ev_key_sheet"], "i_before_a"),
    (2, "ومسار مستقل: إيصال المخزن وقارئ بابه، نظامان لا علاقة لهما بالنادي، يضعان الكأس في المخزن قبل الاجتماع.", ["ev_store_slip", "ev_store_door_log"], "i_before_b"),
    (3, "من نقلها: المكلّفة بالجدول وصاحبة الاسم في ورقة المفتاح، والإيصال وبطاقة الباب باسمها.", ["ev_key_sheet", "ev_dust_rota"], "i_moved_a"),
    (4, "قارن الحلول المتنافسة: المفتاح المقلّد والجدار المتحرك والتدبير تعالج خروجاً أثناء القفل لم يقع، فتحتاج افتراضات أكثر وتُفسّر قرائن أقل.", ["ev_copy_receipt", "ev_cabinet_inspect"], "i_rule_copy"),
    (5, "إفادة يارا تؤيد سجلات سبقتها، وسلامة القفل لا تفرّق بين الحلول لأن نسبة ظهورها واحدة تقريباً تحتها جميعاً.", ["ev_yara_stmt", "ev_compare_card"], "i_rule_panel"),
]
alt = ["يمكن إثبات الحلقتين بالمسار الأول: الصورة وورقة المفتاح وجدول المهام.",
       "ويمكن إثباتهما بالمسار الثاني: إيصال المخزن وسجل قارئ بابه؛ والأقوى أن يتفق المساران."]
notlimits = ["لا نعرف لماذا لم تُرجع يارا الكأس ولا لماذا لم تخبر الرئيس، ولا نعرف ما قالته لأمين المخزن.",
             "قارئ الباب يسجّل البطاقة لا حاملها؛ قوته في اتفاقه مع إيصال بخط أمين المخزن.",
             "الحل الأقل افتراضاً ليس مضموناً صحيحاً؛ هو الأرجح بالسجلات الموجودة، ويتغير إذا ظهر سجل جديد."]
notes = ["قبل أن تبحث عن حيلة، اختبر المقدمة: «الكأس كانت في الخزانة المقفلة». كثير من الألغاز المستحيلة تنحل حين يتبين أن المعطى لم يكن صحيحاً.",
         "قارن الحلول المتنافسة بثلاثة أسئلة: هل يفسّر كل القرائن؟ وهل تناقضه قرينة؟ وكم افتراضاً يحتاج؟ والحل الأقل افتراضاً مع تغطية أكبر هو الأرجح.",
         "نسبة الترجيح تقارن تكرارين: كم مرة تظهر القرينة لو صح حل، وكم مرة لو صح آخر. قرينة «القفل سليم» تظهر تحت الحلين فلا تفرّق بينهما، وقرينة «إيصال المخزن» تظهر تحت حل واحد غالباً فتفرّق كثيراً.",
         "لا أحد هنا يريد إيذاء أحد: يارا أرادت إنجاز مهمتها ثم خافت من الاعتراف. والإصلاح بسيط: تُكتب ورقة على الخزانة كلما نُقل منها شيء.",
         "بطاقة الأصل: القضية أصلية من ATHAR على بنية «تحدي القارئ» في مكتبة الحالات، وتستعير وعي القواعد المعلنة دون عنف."]
premise = {"hook_ar": "كأس اختفت من خزانة زجاجية مقفلة، ورئيس النادي يراهن أن أحداً لن يفسّر كيف. فما المعطى الذي لم يتحقق منه أحد؟",
           "player_role_ar": "أنت عضو جديد في نادي الألغاز، وتحدّيت الرئيس أن تقدّم حلاً معلّلاً للغز الكأس، دون اتهام أحد قبل أن تثبت السجلات شيئاً.",
           "setting_ar": "مدرسة الأطلال، بعد ظهر الخميس. الأوقات بساعة المدرسة.",
           "public_fact_ids": ["f_cup_vanished", "f_challenge", "f_rules"],
           "assumed_general_knowledge_ar": ["الحل الأفضل يفسّر كل القرائن ولا يناقض أيّاً منها", "الحل الأقل افتراضات أرجح عند تساوي التغطية", "ما يُعلن معطى قد لا يكون مثبتاً بسجل"]}
meta = {"title_ar": "الكأس التي غادرت قبل القفل", "title_en": "The Cup That Left Before the Lock", "age_band": "16-18", "estimated_minutes": 30, "difficulty": 3,
        "content_flags": ["no_violence"],
        "knowledge_object_refs": ["KO-FC-04-009", "KO-RS-06-008", "KO-FC-04-026", "KO-RS-05-004", "KO-RS-05-001", "KO-RS-05-014", "KO-RS-06-001", "KO-RS-06-021", "KO-RS-06-009", "KO-RS-05-002", "KO-RS-05-005"]}
ui = {
    "clock": {"epoch_hhmm": "14:00", "zone_label_ar": "ساعة المدرسة"},
    "cover": {"title_ar": "الكأس التي غادرت قبل القفل", "tagline_ar": "هل كانت الكأس في الخزانة حقاً؟", "kicker_ar": "الملف السابع والعشرون · مقارنة الحلول", "glyph": "♜", "accent": "green"},
    "cold_open_ar": ["الخميس، 17:30.", "فُتحت الخزانة الزجاجية فلم تكن الكأس الخضراء فيها. القفل سليم والزجاج سليم، والمفتاح الأول مع الرئيس.", "قال كنان: لن يفسّر أحد كيف خرجت. ويهمس باسل بأن عنده خبرة بالأقفال، ويقول أحدهم إن للخزانة جداراً خلفياً.",
                    "قبل أن تقارن الحلول: ما المعطى الذي أخذناه على أنه صحيح دون أن نسأل عن سجله؟"],
    "limit_menu": [
        {"id": "l_why_not_told", "label_ar": "لا نعرف لماذا لم تُرجع يارا الكأس ولا لماذا لم تخبر الرئيس"},
        {"id": "l_card_not_person", "label_ar": "قارئ الباب يسجّل البطاقة لا حاملها، وقوته في اتفاقه مع إيصال بخط أمين المخزن"},
        {"id": "l_new_record", "label_ar": "الحل الأقل افتراضاً هو الأرجح بالسجلات الحالية، ويتغير إذا ظهر سجل جديد"},
        {"id": "l_invalid_lock", "label_ar": "سلامة القفل والزجاج تؤيد حل الجدار المتحرك"},
        {"id": "l_invalid_skill", "label_ar": "خبرة باسل بالأقفال تدل على أنه الفاعل"},
        {"id": "l_invalid_sure", "label_ar": "ثقة الرئيس بأن الكأس كانت في الخزانة تثبت ذلك"}],
    "mind_change_menu": [
        {"id": "m_store_other", "label_ar": "ظهور أن الإيصال أو قارئ المخزن يخصان غرضاً آخر"},
        {"id": "m_photo_later", "label_ar": "ثبوت أن وقت صورة الخزانة بعد بدء الاجتماع"},
        {"id": "m_key_other", "label_ar": "ظهور فتح للخزانة أثناء الاجتماع في ورقة المفتاح"},
        {"id": "m_popular", "label_ar": "اتفاق أكثر الأعضاء على أن الجدار الخلفي هو المنفذ"}],
    "transfer": {
        "id": "tr_two_solutions", "title_ar": "اختبار نقل المهارة: ميدالية الغرفة المقفلة",
        "scenario_ar": "اختفت ميدالية من درج مقفل في غرفة الأنشطة. اقترح عضو حلّاً بمفتاح احتياطي، واقترحت عضوة حلاً بأن الميدالية نُقلت قبل الإقفال. الواقعة خيالية ولا علاقة لها بالقضية.",
        "documents": [
            {"title_ar": "قرائن الواقعة", "body_ar": "1) الدرج سليم وقفله سليم. 2) ورقة تسليم تبيّن أن الميدالية سُلّمت لمكتب الاعتماد قبل الإقفال بساعة. 3) المفتاح الاحتياطي في صندوق مختوم لم يُفتح."},
            {"title_ar": "بطاقة المقارنة", "body_ar": "القرينة 1: تظهر 9 مرات من 10 تحت الحلين. القرينة 2: تظهر 9 من 10 تحت «نُقلت قبل الإقفال» و1 من 20 تحت «مفتاح احتياطي». القرينة 3: تظهر 9 من 10 تحت «نُقلت قبل الإقفال» و1 من 10 تحت «مفتاح احتياطي»."}],
        "prompt_ar": "اختر الخطوات الصالحة للمقارنة بين الحلين (يمكنك اختيار أكثر من خطوة).",
        "options": [
            {"id": "o1", "text_ar": "ملاحظة أن القرينة 1 لا تفرّق بين الحلين لأن نسبة ظهورها واحدة تحتهما"},
            {"id": "o2", "text_ar": "حساب نسبة الترجيح للقرينة 2: قسمة 9 من 10 على 1 من 20"},
            {"id": "o3", "text_ar": "الانتباه إلى أن الحل الذي يفسّر القرائن كلها بافتراض أقل هو الأرجح"},
            {"id": "o4", "text_ar": "ذكر أن النسب تقديرية وتتغير بسجل جديد"},
            {"id": "o5", "text_ar": "اختيار الحل الذي يبدو أذكى وأكثر إثارة"},
            {"id": "o6", "text_ar": "اعتبار الرقم 9 من 10 احتمالاً بأن الحل صحيح"},
            {"id": "o7", "text_ar": "اتهام صاحب المفتاح الاحتياطي لأنه يملك الإمكان"}],
        "free_text_prompt_ar": "اكتب في ثلاثة أسطر كيف تقارن الحلين بنسبة الترجيح، وما الذي قد يغيّر رأيك.",
    },
    "skills": [{"skill_id": "KO-FC-04-009", "track": "D"}, {"skill_id": "KO-RS-06-008", "track": "C"}, {"skill_id": "KO-FC-04-026", "track": "E"}, {"skill_id": "KO-RS-05-004", "track": "B"}, {"skill_id": "KO-RS-05-002", "track": "D"}],
    "stage_hooks_ar": {"briefing": "قفل سليم وزجاج سليم… فهل كانت الكأس هناك؟", "investigating": "اسأل عن سجل كل معطى قبل أن تفتّش عن حيلة.", "review": "قبل أن تغلق الملف: أي حل يفسّر أكثر بافتراض أقل؟ وما الذي يغيّر رأيك؟", "resolved": "أُغلق الملف. عادت الكأس إلى الخزانة، وكُتبت ورقة على بابها."},
    "character_glyphs": {"kinan": "ك", "yara": "ي", "basel": "ب", "talla": "ت", "nadine": "ن", "dawood": "د"},
}
sc = {
    "accepted_conclusions": {
        "h_dusting": {"grade": 1, "note_ar": "استنتاج متسق مع الأدلة ويتطلب ذكر حدوده."},
        "h_copykey": {"grade": 0, "note_ar": "يعالج خروجاً أثناء الاجتماع، والكأس كانت خارج الخزانة قبله؛ ونسخ مفتاح المخزن لا يمسّ الخزانة."},
        "h_panel": {"grade": 0, "note_ar": "سلامة الجدار لا تؤيد حلاً لواقعة لم تقع داخل القفل؛ ويحتاج افتراضات إضافية."},
        "h_staged": {"grade": 0, "note_ar": "ورقة المفتاح والإيصال تبعدان الرئيس؛ وإعلان التحدي ليس تدبيراً."}},
    "confidence_band": {"h_dusting": [65, 90], "h_copykey": [0, 15], "h_panel": [0, 15], "h_staged": [0, 20]},
    "source_key": {"ev_challenge": "claim", "ev_compare_card": "template", "ev_key_sheet": "primary_record", "ev_dust_rota": "primary_record", "ev_newsletter_photo": "primary_record",
                   "ev_store_slip": "primary_record", "ev_store_door_log": "primary_record", "ev_cabinet_inspect": "primary_record", "ev_copy_receipt": "primary_record",
                   "ev_kinan_stmt": "claim", "ev_basel_stmt": "claim", "ev_yara_stmt": "claim"},
    "link_key": {
        "h_dusting": {"ev_key_sheet": "supports", "ev_dust_rota": "supports", "ev_newsletter_photo": "supports", "ev_store_slip": "supports", "ev_store_door_log": "supports", "ev_yara_stmt": "supports",
                      "ev_cabinet_inspect": "neutral", "ev_copy_receipt": "neutral", "ev_compare_card": "neutral"},
        "h_copykey": {"ev_copy_receipt": "supports", "ev_basel_stmt": "neutral", "ev_cabinet_inspect": "neutral", "ev_newsletter_photo": "weakens", "ev_store_slip": "weakens", "ev_store_door_log": "weakens", "ev_key_sheet": "weakens"},
        "h_panel": {"ev_challenge": "supports", "ev_cabinet_inspect": "weakens", "ev_newsletter_photo": "weakens", "ev_store_slip": "weakens", "ev_store_door_log": "weakens"},
        "h_staged": {"ev_kinan_stmt": "supports", "ev_challenge": "supports", "ev_key_sheet": "weakens", "ev_store_slip": "weakens", "ev_store_door_log": "weakens", "ev_newsletter_photo": "weakens"},
    },
    "required_limits": ["l_why_not_told", "l_card_not_person"], "valid_mind_changers": ["m_store_other", "m_photo_later", "m_key_other"],
    "invalid_limits": ["l_invalid_lock", "l_invalid_skill", "l_invalid_sure"],
    "decisive_evidence": ["ev_key_sheet", "ev_dust_rota", "ev_newsletter_photo", "ev_store_slip", "ev_store_door_log"],
    "timeline_requirement": [{"evidence_id": "ev_key_sheet", "utc_minute": 90, "tol": 4}, {"evidence_id": "ev_store_slip", "utc_minute": 100, "tol": 4},
                             {"evidence_id": "ev_newsletter_photo", "utc_minute": 110, "tol": 3}, {"evidence_id": "ev_cabinet_inspect", "utc_minute": 210, "tol": 5}],
    "refuted_hypotheses": ["h_copykey", "h_panel", "h_staged"],
    "transfer_key": {"valid": ["o1", "o2", "o3", "o4"], "invalid": ["o5", "o6", "o7"]},
}
assemble(CID, meta, premise, {"characters": chars, "locations": locations, "objects": objects, "organizations": orgs}, ["yara"],
         "لم تُسرق الكأس ولم تخرج من خزانة مقفلة. نقلتها يارا إلى المخزن للتنظيف قبل الاجتماع وأقفلت الخزانة دون إعلام الرئيس ثم نسيت إرجاعها، فكان المعطى الذي بُني عليه التحدي غير صحيح.",
         ["f_empty_before", "f_yara_moved"], claims, timeline, ck, hyps, mis, los, ref, hints, topics, steps, alt, notlimits, notes, ui, sc)
