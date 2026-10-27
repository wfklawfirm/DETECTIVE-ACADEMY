#!/usr/bin/env python3
# Tutorial case c000 «دفتر المختبر الضائع» — a short no-culprit-in-the-usual-sense case that teaches: spot a contradiction,
# separate a mistaken claim from a lie, and let a record (not a reputation) decide. The person who caused the unintended event
# (moving the notebook) is recorded as culprit_ids per the library convention for no-culprit cases.
import json, sys, os
OUT = sys.argv[1]
CID = "c000_lost_notebook"

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

ch("hadi", "هادي النجار", "suspect", "طالب في السنة الثالثة، عضو في نادي العلوم",
   "هادئ وحذر، يتكلم بسرعة حين يشعر أنه متّهم، ويصحّح نفسه إذا واجهته بسجل.",
   ["ألا يُتّهم بشيء لم يفعله", "أن يستعيد دفتر التجربة لأن نتائجه فيه"],
   [L("hd_greet", "greeting", "أنا لم آخذ الدفتر. اسألني ما شئت."),
    L("hd_left", "reveal", "وقّعت خروجي من المختبر في الثانية والعشر دقائق تقريباً، وكان الدفتر على الطاولة حين خرجت.", ["f_hadi_left_lab"]),
    L("hd_time", "reveal", "ظننت أنني غادرت المبنى في الثانية تماماً. لعلّي نسيت أنني بقيت أتحدث مع زميل عند البوابة.", None, ["cl_hadi_time"]),
    L("hd_unknown", "deflect_unknown", "لا أعرف، ولا أريد أن أخمّن."),
    L("hd_off", "deflect_offtopic", "هذا لا يخصّ الدفتر. اسألني عن وقت خروجي."),
    L("hd_bye", "farewell", "شكراً لأنك تسأل قبل أن تحكم.")])
ch("jamal", "د. جمال الأيوبي", "victim", "مشرف نادي العلوم",
   "مشغول ومتعجل، يتحدث بثقة من أمضى سنوات في الإشراف، ويميل إلى تصديق أول تفسير يخطر له.",
   ["استعادة دفتر التجربة قبل موعد التسليم"],
   [L("jm_greet", "greeting", "أهلاً. الدفتر مفقود منذ أمس، وأظن أنني أعرف من أخذه."),
    L("jm_saw", "reveal", "مررت بالمختبر قرابة الثانية والربع ورأيت الدفتر على الطاولة نفسها، ثم لم أنتبه إليه بعد ذلك.", ["f_jamal_saw_notebook"]),
    L("jm_last", "reveal", "ظننت أن هادي آخر من غادر المختبر، فهو دائماً آخر من يخرج.", None, ["cl_jamal_last"]),
    L("jm_unknown", "deflect_unknown", "لا أذكر ذلك."),
    L("jm_off", "deflect_offtopic", "ركّز على الدفتر لو سمحت."),
    L("jm_bye", "farewell", "أريد الدفتر بأسرع وقت.")])
ch("omar", "عمر الحارس", "witness", "حارس بوابة المبنى",
   "دقيق في تدوين الدخول والخروج، قليل الكلام، لا يحب التخمين.",
   ["أن يبقى سجل البوابة سليماً"],
   [L("om_greet", "greeting", "السجل أمامي. أقرأ ما فيه فقط."),
    L("om_gate", "reveal", "سجّلت خروج هادي من البوابة في الثالثة إلا عشرين دقيقة بعد الظهر، أي 14:40.", ["f_gate_exit_hadi"]),
    L("om_unknown", "deflect_unknown", "لا شيء عندي عن هذا."),
    L("om_off", "deflect_offtopic", "اسألني عن البوابة فقط."),
    L("om_bye", "farewell", "مع السلامة.")])
ch("samira", "سميرة الحلبي", "suspect", "فنية المختبر",
   "مجتهدة وتخشى أن تُلام على أي شيء في المختبر، فتقلّل من شأن ما فعلته.",
   ["ألا تُلام على انسكاب أو على فقدان شيء"],
   [L("sm_greet", "greeting", "تفضّل. أنا أنظّف المختبر عادةً بعد الظهر."),
    L("sm_spill", "reveal", "حدث انسكاب لمحلول التنظيف على الطاولة الأولى، فنظّفتها في الثانية والنصف تقريباً.", ["f_spill"]),
    L("sm_refuse", "refuse_secret", "لا أذكر شيئاً مهماً آخر."),
    L("sm_moved", "reveal", "نعم... كان الدفتر مبتلاً بالمحلول فوضعته على رف التجفيف في خزانة المستلزمات، وكتبت ورقة بذلك. لا بد أنها وقعت خلف الرف.", ["f_samira_moved", "f_closet_location"]),
    L("sm_unknown", "deflect_unknown", "لا أعرف."),
    L("sm_off", "deflect_offtopic", "اسألني عن المختبر والتنظيف."),
    L("sm_bye", "farewell", "أرجو أن يجد الدفتر مكانه.")])

locations = [{"id": "loc_office", "name_ar": "مكتب النادي", "description_ar": "ملفات النادي وطلبات الصيانة."},
             {"id": "loc_lab", "name_ar": "مختبر الكيمياء", "description_ar": "الطاولة الأولى حيث كان الدفتر."},
             {"id": "loc_gate", "name_ar": "بوابة المبنى", "description_ar": "سجل الدخول والخروج."},
             {"id": "loc_closet", "name_ar": "خزانة المستلزمات", "description_ar": "رف التجفيف في آخر المختبر."}]
objects = [{"id": "obj_notebook", "name_ar": "دفتر التجربة", "description_ar": "دفتر نتائج تجربة نمو النبات."}]
orgs = [{"id": "org_club", "name_ar": "نادي العلوم", "description_ar": "نادي طلابي في الجامعة."}]

facts = []
def F(id, st, kind, subj, spoiler, time=None, loc=None, ko=None):
    d = {"id": id, "statement_ar": st, "kind": kind, "subject_ids": subj, "spoiler_level": spoiler}
    if time: d["time"] = time
    if loc: d["location_id"] = loc
    if ko: d["science_ko_refs"] = ko
    facts.append(d)
F("f_notebook_missing", "اختفى دفتر التجربة من الطاولة الأولى في المختبر عصر الأربعاء.", "event", ["obj_notebook"], 0)
F("f_jamal_suspects", "يظن المشرف أن هادي هو من أخذ الدفتر لأنه آخر من غادر المختبر في ظنّه.", "attribute", ["jamal", "hadi"], 0)
F("f_hadi_denies", "ينفي هادي أنه أخذ الدفتر، ويقول إنه غادر المبنى في الثانية.", "event", ["hadi"], 0)
F("f_hadi_left_lab", "وقّع هادي خروجه من المختبر الساعة 14:10.", "event", ["hadi"], 1, T(10), "loc_lab")
F("f_gate_exit_hadi", "خرج هادي من بوابة المبنى الساعة 14:40.", "event", ["hadi", "loc_gate"], 1, T(40), "loc_gate")
F("f_jamal_saw_notebook", "رأى المشرف الدفتر على الطاولة الأولى الساعة 14:15 تقريباً.", "event", ["jamal", "obj_notebook"], 2, T(15, "approx"), "loc_lab")
F("f_spill", "انسكب محلول تنظيف على الطاولة الأولى ونظّفته سميرة نحو الساعة 14:25.", "event", ["samira", "obj_notebook"], 1, T(25, "approx"), "loc_lab")
F("f_closet_location", "وُضع الدفتر لتجفيفه على رف التجفيف في خزانة المستلزمات.", "state", ["obj_notebook", "loc_closet"], 1, None, "loc_closet")
F("f_hadi_left_before", "غادر هادي المختبر قبل انسكاب المحلول، وكان الدفتر ما زال على الطاولة بعد مغادرته.", "relation", ["hadi", "obj_notebook"], 3, T(10, "exact", 15), "loc_lab", ["KO-RS-06-017"])
F("f_samira_moved", "نقلت سميرة الدفتر المبتل إلى خزانة المستلزمات لتجفيفه بعد الانسكاب، دون أن تُبلغ أحداً.", "event", ["samira", "obj_notebook"], 3, T(30, "approx"), "loc_lab", ["KO-RS-05-014"])
claims = [
    {"id": "cl_hadi_time", "statement_ar": "غادرتُ المبنى في الثانية تماماً.", "kind": "honest_mistake", "held_by": ["hadi"], "true_fact_id": "f_gate_exit_hadi", "contradicted_by_evidence_ids": ["ev_gate_log"]},
    {"id": "cl_jamal_last", "statement_ar": "هادي آخر من غادر المختبر.", "kind": "honest_mistake", "held_by": ["jamal"], "true_fact_id": "f_samira_moved", "contradicted_by_evidence_ids": ["ev_cleaning_ticket", "ev_lab_sheet"]},
]
timeline = [
    {"id": "te_hadi_out", "description_ar": "هادي يوقّع خروجه من المختبر.", "time": T(10), "location_id": "loc_lab", "actor_ids": ["hadi"], "fact_ids": ["f_hadi_left_lab"], "motivated_by_ar": "حان موعد محاضرته"},
    {"id": "te_jamal_pass", "description_ar": "المشرف يمرّ ويرى الدفتر على الطاولة.", "time": T(15, "approx"), "location_id": "loc_lab", "actor_ids": ["jamal"], "fact_ids": ["f_jamal_saw_notebook"], "motivated_by_ar": "مرور عابر في طريقه إلى مكتبه"},
    {"id": "te_spill", "description_ar": "انسكاب محلول التنظيف وتنظيف الطاولة.", "time": T(25, "approx"), "location_id": "loc_lab", "actor_ids": ["samira"], "fact_ids": ["f_spill"], "motivated_by_ar": "واجب التنظيف بعد الظهر"},
    {"id": "te_move", "description_ar": "سميرة تنقل الدفتر المبتل إلى خزانة التجفيف.", "time": T(30, "approx"), "location_id": "loc_closet", "actor_ids": ["samira"], "fact_ids": ["f_samira_moved", "f_closet_location"], "motivated_by_ar": "خشيت أن يتلف الدفتر"},
    {"id": "te_gate", "description_ar": "هادي يخرج من بوابة المبنى.", "time": T(40), "location_id": "loc_gate", "actor_ids": ["hadi"], "fact_ids": ["f_gate_exit_hadi"], "motivated_by_ar": "بقي يتحدث مع زميل قبل أن يغادر"},
]

ev = []
def V(id, title, kind, content, acts, supports, rel, limits, contradicts=None, red=False, ko=None, loc=None):
    d = {"id": id, "title_ar": title, "kind": kind, "content_ar": content, "acquired_by_action_ids": acts, "supports_fact_ids": supports, "reliability": rel, "limits_ar": limits}
    if contradicts: d["contradicts_claim_ids"] = contradicts
    if red: d["is_red_herring"] = True
    if ko: d["forensic_ko_ref"] = ko
    if loc: d["location_id"] = loc
    ev.append(d)
V("ev_lab_sheet", "ورقة توقيع الدخول والخروج في المختبر", "documentary",
  "ورقة توقيع المختبر — الأربعاء\nالاسم | الدخول | الخروج\nهادي النجار | 13:20 | 14:10\nلينا حداد | 13:45 | 14:00\n(لا توقيعات أخرى بعد 14:10 حتى 15:00)",
  ["a_read_sheet"], ["f_hadi_left_lab"], "strong", "تثبت توقيعاً مكتوباً بخروج هادي، ولا تثبت أن الدفتر كان على الطاولة أو لم يكن؛ وهي لا تسجّل دخول الفنية أو المشرف إذ لا يوقّعان.", loc="loc_lab")
V("ev_gate_log", "سجل بوابة المبنى", "documentary",
  "سجل بوابة المبنى — الأربعاء\n13:05 دخول: هادي النجار\n14:40 خروج: هادي النجار\n14:42 خروج: لينا حداد",
  ["a_read_gate"], ["f_gate_exit_hadi"], "strong", "يثبت وقت خروج هادي من المبنى، لا ما فعله قبل ذلك داخله ولا مكان الدفتر.", contradicts=["cl_hadi_time"], red=True, loc="loc_gate")
V("ev_cleaning_ticket", "طلب تنظيف المختبر", "documentary",
  "طلب تنظيف — مختبر الكيمياء\nالوقت: 14:20\nالسبب: انسكاب محلول على الطاولة الأولى\nالمكلّفة: س. الحلبي\nأُنجز: 14:35",
  ["a_search_office"], ["f_spill"], "strong", "يثبت أن فنية المختبر كانت عند الطاولة الأولى بين 14:20 و14:35، لا ما فعلته بالدفتر.", contradicts=["cl_jamal_last"], loc="loc_office")
V("ev_jamal_statement", "إفادة د. جمال (ملخص)", "testimonial",
  "ملخص إفادة د. جمال الأيوبي:\n«مررت بالمختبر قرابة 14:15 ورأيت الدفتر على الطاولة الأولى، ثم لم أنتبه إليه. ظننت أن هادي آخر من غادر.»",
  ["a_note_jamal"], ["f_jamal_saw_notebook"], "moderate", "ذاكرة شخص عن وقت مرور عابر؛ تحتاج إلى سجل يؤيد الترتيب.", loc="loc_lab")
V("ev_hadi_statement", "إفادة هادي (ملخص)", "testimonial",
  "ملخص إفادة هادي النجار:\n«وقّعت خروجي من المختبر في الثانية والعشر دقائق، وكان الدفتر على الطاولة. وظننت أنني غادرت المبنى في الثانية تماماً.»",
  ["a_note_hadi"], ["f_hadi_left_lab"], "weak", "إفادة صاحب مصلحة، ويصحّح فيها وقتاً ظنّه؛ تُقاس بالسجلات.", loc="loc_lab")
V("ev_note_shelf", "ورقة خلف الرف", "physical",
  "ورقة صغيرة وُجدت خلف رف التجفيف:\n«الدفتر مبلل بالمحلول — وضعته هنا ليجفّ. س.»\nلا تاريخ على الورقة.",
  ["a_search_closet"], ["f_samira_moved"], "moderate", "ورقة غير مؤرّخة وحرف توقيعها واحد؛ تدل على فعل النقل لكن لا تثبت وقته، ويدعمها طلب التنظيف.", loc="loc_closet")
V("ev_notebook_closet", "دفتر التجربة على رف التجفيف", "physical",
  "الدفتر نفسه على رف التجفيف في الخزانة، صفحاته متموّجة قليلاً، وعلى غلافه بقعة محلول جافة.",
  ["a_search_closet"], ["f_closet_location"], "strong", "يثبت مكان الدفتر الآن لا من وضعه فيه ولا متى.", loc="loc_closet")

def P(t, i): return {"ref_type": t, "ref_id": i}
inf = []
def I(id, prem, ct, concl, rel, strength, rule, ks):
    inf.append({"id": id, "premises": prem, "conclusion": {"ref_type": ct, "ref_id": concl}, "relation": rel, "strength": strength, "rule_ar": rule, "skill_ko_refs": ks})
I("i_hadi_left", [P("evidence", "ev_lab_sheet"), P("evidence", "ev_jamal_statement")], "fact", "f_hadi_left_before", "establishes", "strong",
  "هادي وقّع خروجه 14:10، والمشرف رأى الدفتر 14:15 على الطاولة؛ فالدفتر كان موجوداً بعد خروج هادي.", ["KO-RS-06-017"])
I("i_moved", [P("evidence", "ev_cleaning_ticket"), P("evidence", "ev_note_shelf")], "fact", "f_samira_moved", "establishes", "strong",
  "طلب التنظيف يضع الفنية عند الطاولة 14:20–14:35، وورقتها خلف الرف تقول إنها وضعت الدفتر ليجف؛ فهي من نقله.", ["KO-RS-05-014"])
I("i_time_claim", [P("evidence", "ev_gate_log"), P("evidence", "ev_lab_sheet")], "claim", "cl_hadi_time", "contradicts_claim", "strong",
  "الخطأ في ساعة مغادرة المبنى (14:40) لا يغيّر ساعة مغادرة المختبر (14:10)؛ فهو خطأ ذاكرة لا كذبة تخدم إخفاء شيء.", ["KO-RS-05-007"])
I("i_last_claim", [P("evidence", "ev_cleaning_ticket"), P("evidence", "ev_lab_sheet")], "claim", "cl_jamal_last", "contradicts_claim", "strong",
  "الفنية كانت عند الطاولة بعد خروج هادي، وهي لا توقّع في الورقة؛ فالورقة لا تدل على من كان آخر من غادر.", ["KO-RS-05-001"])
I("i_support_samira", [P("fact", "f_samira_moved")], "hypothesis", "h_samira", "supports", "strong",
  "نقل الدفتر المبتل إلى الخزانة هو التفسير الذي يجمع الانسكاب والورقة ومكان الدفتر الآن.", ["KO-RS-05-002"])
I("i_rule_hadi", [P("fact", "f_hadi_left_before")], "hypothesis", "h_hadi", "rules_out", "conclusive",
  "إذا كان الدفتر على الطاولة بعد خروج هادي فلا يصح أن يكون هو من أخذه عند خروجه.", ["KO-RS-06-008"])
I("i_rule_loss", [P("evidence", "ev_notebook_closet")], "hypothesis", "h_loss", "rules_out", "strong",
  "الدفتر وُجد على رف التجفيف، فهو لم يضِع بين الأوراق بل نُقل إلى مكان محدد.", ["KO-RS-06-008"])

ck = [
    {"character_id": "hadi", "knows": [{"fact_id": "f_hadi_left_lab", "access": "witnessed", "certainty": "certain"}], "hides": [], "believes": [{"claim_id": "cl_hadi_time", "stance": "sincere"}]},
    {"character_id": "jamal", "knows": [{"fact_id": "f_jamal_saw_notebook", "access": "witnessed", "certainty": "fairly_sure"}], "hides": [], "believes": [{"claim_id": "cl_jamal_last", "stance": "sincere"}]},
    {"character_id": "omar", "knows": [{"fact_id": "f_gate_exit_hadi", "access": "witnessed", "certainty": "certain"}], "hides": [], "believes": []},
    {"character_id": "samira", "knows": [{"fact_id": "f_spill", "access": "witnessed", "certainty": "certain"}],
     "hides": [{"fact_id": "f_samira_moved", "reveal_when": {"presented": {"evidence_id": "ev_cleaning_ticket", "to_character": "samira"}}, "cover_claim_id": None, "reveal_line_id": "sm_moved"},
               {"fact_id": "f_closet_location", "reveal_when": {"presented": {"evidence_id": "ev_cleaning_ticket", "to_character": "samira"}}, "cover_claim_id": None, "reveal_line_id": "sm_moved"}], "believes": []},
]
hyps = [
    {"id": "h_samira", "statement_ar": "نقلت فنية المختبر الدفتر المبتل لتجفيفه بعد الانسكاب دون أن تُبلغ أحداً.", "is_true": True, "plausibility_at_start": "low", "suspect_id": "samira"},
    {"id": "h_hadi", "statement_ar": "أخذ هادي الدفتر عند خروجه من المختبر.", "is_true": False, "plausibility_at_start": "high", "suspect_id": "hadi"},
    {"id": "h_loss", "statement_ar": "لم يأخذ أحد الدفتر؛ ضاع بين الأوراق في المختبر.", "is_true": False, "plausibility_at_start": "medium"},
]
mis = [{"id": "rh_gate", "points_to_hypothesis_id": "h_hadi", "planted_via_ar": "سجل البوابة يُظهر أن هادي خرج 14:40 لا 14:00 كما قال.", "evidence_ids": ["ev_gate_log"], "refuted_by_inference_ids": ["i_rule_hadi", "i_time_claim"],
        "fairness_note_ar": "ورقة المختبر وإفادة المشرف يضعان الدفتر على الطاولة بعد خروج هادي؛ والخطأ في ساعة مغادرة المبنى لا يتعلق بمكان الدفتر."}]
los = [
    {"id": "lo_claim", "statement_ar": "يفرّق بين قول خاطئ بحسن نية وقول يخفي شيئاً، ويقيس القول بسجل.", "skill_ko_ref": "KO-RS-05-001", "observable_behaviors_ar": ["يصنّف إفادات الشهود كأقوال", "يقابل القول بسجل"], "evidence_sources": ["evidence_board"]},
    {"id": "lo_timeline", "statement_ar": "يرتّب الأحداث على خط زمني ليكشف التعارض.", "skill_ko_ref": "KO-RS-05-005", "observable_behaviors_ar": ["يضع الأدلة في أزمنتها"], "evidence_sources": ["timeline_task", "action_log"]},
    {"id": "lo_hyp", "statement_ar": "يوازن بين فرضيتين على الأقل ويستبعد ما تنقضه الأدلة.", "skill_ko_ref": "KO-RS-05-002", "observable_behaviors_ar": ["يضيف فرضيات", "يستبعد بدليل"], "evidence_sources": ["hypothesis_ledger"]},
    {"id": "lo_diag", "statement_ar": "يقدّر ما يثبته الدليل وما لا يثبته.", "skill_ko_ref": "KO-RS-06-001", "observable_behaviors_ar": ["يربط الدليل بالفرضية باتجاه صحيح"], "evidence_sources": ["evidence_board", "final_justification"]},
    {"id": "lo_calib", "statement_ar": "يصوغ ثقته بحدودها.", "skill_ko_ref": "KO-RS-06-021", "observable_behaviors_ar": ["يختار ثقة معقولة", "يذكر حدوداً"], "evidence_sources": ["final_justification"]},
    {"id": "lo_revise", "statement_ar": "يراجع رأيه الأول حين يظهر ما يخالفه.", "skill_ko_ref": "KO-RS-06-009", "observable_behaviors_ar": ["يغيّر فرضيته الرائدة بدليل"], "evidence_sources": ["hypothesis_ledger"]},
]
def levels(d): return [{"score": i, "descriptor_ar": t} for i, t in enumerate(d)]
rub = {
    "reference_answer_ar": "هادي لم يأخذ الدفتر: وقّع خروجه من المختبر 14:10، ورآه المشرف على الطاولة 14:15 بعد خروجه. وخطؤه في ساعة مغادرة المبنى (14:40 لا 14:00) خطأ ذاكرة لا يتعلق بمكان الدفتر. الأرجح أن فنية المختبر نقلت الدفتر المبتل بعد الانسكاب إلى خزانة التجفيف ولم تُبلغ أحداً، وتدل على ذلك ورقتها وطلب التنظيف ووجود الدفتر هناك. حدود الاستنتاج: لا نعرف لماذا لم تُبلغ، ولا يثبت السجل وقت النقل بالدقيقة.",
    "criteria": [
        {"id": "c_source", "name_ar": "تصنيف المصادر", "objective_ids": ["lo_claim"], "scored_by": "deterministic", "weight": 0.15, "levels": levels(["لم يصنّف", "أخطأ في الأغلب", "نصف صحيح", "معظمه صحيح", "كله صحيح"])},
        {"id": "c_conflict", "name_ar": "كشف التعارض على الخط الزمني", "objective_ids": ["lo_timeline"], "scored_by": "deterministic", "weight": 0.25, "levels": levels(["لم يضع شيئاً", "وضع قليلاً", "وضع نصفها صحيحاً", "معظمها", "كلها في موضعها"])},
        {"id": "c_links", "name_ar": "ربط الأدلة بالفرضيات", "objective_ids": ["lo_diag"], "scored_by": "deterministic", "weight": 0.15, "levels": levels(["لا روابط", "قليلة", "نصفها صحيح", "معظمها", "كلها دقيقة"])},
        {"id": "c_uncertainty", "name_ar": "معايرة الثقة", "objective_ids": ["lo_calib"], "scored_by": "deterministic", "weight": 0.15, "levels": levels(["ثقة مفرطة", "حدود قليلة", "جزئية", "معقولة", "معايَرة كاملة"])},
        {"id": "c_revision", "name_ar": "مراجعة الرأي", "objective_ids": ["lo_revise"], "scored_by": "deterministic", "weight": 0.1, "levels": levels(["بقي على فرضية مرفوضة", "لم يعلن فرضية", "ثبت على فرضية سليمة", "غيّر بدليل", "غيّر بدليل ووثّق"])},
        {"id": "c_elimination", "name_ar": "استبعاد الفرضيات الخاطئة", "objective_ids": ["lo_hyp"], "scored_by": "deterministic", "weight": 0.1, "levels": levels(["لم يستبعد", "استبعد خطأً", "فرضية بدليل", "فرضيتين", "كل الخاطئة"])},
        {"id": "c_justification", "name_ar": "جودة الحجة المكتوبة", "objective_ids": ["lo_diag", "lo_hyp"], "scored_by": "human", "weight": 0.1, "levels": levels(["لا حجة", "ادعاء بلا سند", "أدلة دون ربط", "ربط الأدلة بالاستنتاج", "ربط مع البدائل والحدود"])},
    ],
}
def H(id, lv, kind, text, trig, target=None, w=0.0):
    d = {"id": id, "level": lv, "kind": kind, "text_ar": text, "trigger": trig, "assessment_weight": w}
    if target: d["targets_inference_id"] = target
    return d
he = lambda e: {"has_evidence": e}
hints = [
    H("hg1", 1, "metacognitive", "حين يخالف قولٌ سجلاً، اسأل: هل الخطأ في الوقت نفسه الذي يخص الدفتر، أم في وقت آخر؟", {"always": True}, None, 0.02),
    H("hg2", 2, "focus_area", "قارن بين أوقات الورقة والبوابة وإفادة المشرف: أيها يخصّ الدفتر مباشرة؟", he("ev_gate_log"), None, 0.04),
    H("hm1", 1, "metacognitive", "من كان عند الطاولة الأولى بعد خروج هادي؟", he("ev_cleaning_ticket"), "i_moved", 0.02),
    H("hm2", 2, "pointer", "ابحث عن مكان يضع فيه شخصٌ ما أغراضاً مبتلة ليجف.", he("ev_cleaning_ticket"), "i_moved", 0.06),
    H("hm3", 3, "partial_reveal", "اعرض طلب التنظيف على الفنية وسترى كيف تتغير إجابتها.", he("ev_cleaning_ticket"), "i_moved", 0.1),
]
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
Act("a_read_sheet", "examine", "اقرأ ورقة توقيع المختبر", al, [G("ev_lab_sheet")], "loc_lab", "READ_SHEET")
Act("a_read_gate", "examine", "اطلب سجل بوابة المبنى", al, [G("ev_gate_log")], "loc_gate", "READ_GATE")
Act("a_search_office", "search_location", "ابحث في طلبات الصيانة بمكتب النادي", al, [G("ev_cleaning_ticket")], "loc_office", "SEARCH_OFFICE")
for cid, lab in [("hadi", "هادي"), ("jamal", "د. جمال"), ("omar", "عمر")]:
    Act(f"a_int_{cid}", "interview", f"ابدأ مقابلة {lab}", al, [{"op": "raise_trust", "ref_id": cid, "amount": 1}], cid, f"INT_{cid.upper()}")
Act("a_int_samira", "interview", "ابدأ مقابلة سميرة", he("ev_cleaning_ticket"), [{"op": "raise_trust", "ref_id": "samira", "amount": 1}], "samira", "INT_SAMIRA")
Act("a_note_jamal", "examine", "دوّن إفادة د. جمال", fu("f_jamal_saw_notebook"), [G("ev_jamal_statement")], "jamal", "NOTE_JAMAL")
Act("a_note_hadi", "examine", "دوّن إفادة هادي", fu("f_hadi_left_lab"), [G("ev_hadi_statement")], "hadi", "NOTE_HADI")
Act("a_search_closet", "search_location", "افتش خزانة المستلزمات", fu("f_closet_location"), [G("ev_note_shelf"), G("ev_notebook_closet")], "loc_closet", "SEARCH_CLOSET")
Act("p_ticket_samira", "present_evidence", "اعرض طلب التنظيف على سميرة", {"presented": {"evidence_id": "ev_cleaning_ticket", "to_character": "samira"}}, [{"op": "emit_event", "ref_id": "PRESENTED_TICKET"}], "samira", "P_TICKET_SAMIRA", 0)
Act("a_hint", "request_hint", "اطلب تلميحاً", al, [], None, "REQUEST_HINT", 0)
Act("a_accuse", "final_accusation", "قدّم الاستنتاج النهائي", al, [{"op": "emit_event", "ref_id": "SUBMIT"}], None, "FINAL_ACCUSATION", 0)

topics = [
    {"id": "t_leaving", "label_ar": "وقت المغادرة", "example_questions_ar": ["متى غادرت المختبر؟", "متى خرجت من المبنى؟"], "fact_ids": ["f_hadi_left_lab", "f_gate_exit_hadi"], "claim_ids": ["cl_hadi_time"]},
    {"id": "t_saw", "label_ar": "الدفتر على الطاولة", "example_questions_ar": ["هل رأيت الدفتر؟", "متى مررت بالمختبر؟"], "fact_ids": ["f_jamal_saw_notebook"], "claim_ids": ["cl_jamal_last"]},
    {"id": "t_spill", "label_ar": "الانسكاب والتنظيف", "example_questions_ar": ["ماذا حدث عند الطاولة الأولى؟", "هل رأيت الدفتر وقت التنظيف؟"], "fact_ids": ["f_spill", "f_samira_moved", "f_closet_location"]},
]
# declarative mirrors of dialogue unlocks (hidden from play; telemetry ASK_*)
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

steps = [
    (1, "سجل البوابة (14:40) يخالف قول هادي (14:00)، لكن هذا التعارض في وقت مغادرة المبنى، لا في وقت مغادرة المختبر.", ["ev_gate_log", "ev_lab_sheet"], "i_time_claim"),
    (2, "ورقة المختبر تضع خروج هادي 14:10، والمشرف رأى الدفتر 14:15 على الطاولة: الدفتر كان موجوداً بعد خروجه.", ["ev_lab_sheet", "ev_jamal_statement"], "i_hadi_left"),
    (3, "طلب التنظيف (14:20–14:35) يضع الفنية عند الطاولة، وورقتها خلف الرف تقول إنها وضعت الدفتر ليجفّ.", ["ev_cleaning_ticket", "ev_note_shelf", "ev_notebook_closet"], "i_moved"),
    (4, "إذن لم يضِع الدفتر ولم يسرقه أحد: نُقل بحسن نية ولم يُبلَّغ بنقله.", ["ev_notebook_closet", "ev_note_shelf"], "i_support_samira"),
]
ending = {
    "steps": [{"order": o, "text_ar": t, "uses_evidence_ids": u, "inference_id": i} for o, t, u, i in steps],
    "alternative_paths_ar": ["يمكن الوصول إلى النتيجة من الخزانة مباشرة بعد معرفة موضعها، لكن إثبات براءة هادي يحتاج ورقة المختبر وإفادة المشرف."],
    "what_evidence_could_not_show_ar": ["لا تثبت الأدلة لماذا لم تُبلغ الفنية بنقل الدفتر.", "لا يثبت السجل وقت النقل بالدقيقة؛ الورقة غير مؤرّخة."],
    "science_notes_ar": ["الفرق بين قول خاطئ بحسن نية وقول كاذب لا يظهر من نبرة القائل، بل من مقابلة قوله بسجل.", "غياب توقيع في ورقة لا يعني غياب شخص؛ تحقق مما يسجّله النظام فعلاً."],
}
core = {
    "schema_version": "0.1.0", "case_id": CID, "case_version": "0.1.0",
    "meta": {"title_ar": "دفتر المختبر الضائع", "title_en": "The Lost Lab Notebook", "age_band": "all", "locale": "ar", "dialogue_register": "msa", "estimated_minutes": 12, "difficulty": 1,
             "content_flags": ["no_violence", "missing_person", "science_lab"], "authors": ["فريق أثر التحريري (مسودة بمساعدة الذكاء الاصطناعي، لم تُراجَع بشرياً بعد)"],
             "knowledge_object_refs": ["KO-RS-05-001", "KO-RS-05-005", "KO-RS-05-002", "KO-RS-06-001", "KO-RS-06-009", "KO-RS-06-021"]},
    "premise": {"hook_ar": "دفتر واحد اختفى، وكل الأصابع تشير إلى شخص واحد. لكن السجلات لا تقول ما يقوله الناس.",
                "player_role_ar": "أنت مراجع ملفات في نادي العلوم بالجامعة، وأول مهامك أن تحسم من أخذ دفتر التجربة.",
                "setting_ar": "مختبر الكيمياء في الجامعة، عصر يوم الأربعاء. توقيت المبنى المحلي هو توقيت كل السجلات.",
                "public_fact_ids": ["f_notebook_missing", "f_jamal_suspects", "f_hadi_denies"],
                "assumed_general_knowledge_ar": ["ورقة التوقيع تسجّل ما كتبه الموقّعون فقط"]},
    "entities": {"characters": chars, "locations": locations, "objects": objects, "organizations": orgs},
    "truth": {"solution": {"culprit_ids": ["samira"], "summary_ar": "لم يُسرق الدفتر. هادي غادر المختبر قبل الانسكاب والدفتر على الطاولة، ونقلته فنية المختبر المبتلّ إلى خزانة التجفيف دون أن تُبلغ أحداً. خطأ هادي في ساعة مغادرة المبنى لا يتعلق بمكان الدفتر.", "key_fact_ids": ["f_hadi_left_before", "f_samira_moved"]},
              "facts": facts, "claims": claims},
    "timeline": timeline, "evidence": ev, "evidence_graph": {"inferences": inf},
    "character_knowledge": ck, "hypotheses": hyps, "misdirection_plan": mis, "learning_objectives": los,
    "mechanics": {"time_budget_units": 30, "actions": A},
    "state_machine": {"id": "c000", "initial": "briefing", "type": "compound", "states": {
        "briefing": {"description_ar": "الإحاطة", "type": "atomic", "on": {"START": {"target": "investigating"}}},
        "investigating": {"description_ar": "التحقيق", "type": "compound", "initial": "gathering",
                          "states": {"gathering": {"type": "atomic", "on": {"OPEN_DEDUCTION": {"target": "deducing"}}}, "deducing": {"type": "atomic", "on": {"BACK": {"target": "gathering"}}}},
                          "on": {"SUBMIT": {"target": "review"}}},
        "review": {"description_ar": "مراجعة", "type": "atomic", "on": {"CLOSE": {"target": "resolved"}}},
        "resolved": {"description_ar": "إغلاق", "type": "final"}}},
    "dialogue": {"max_turns_per_interview": 10, "llm_enabled": False, "topics": topics},
    "rubric": rub, "hint_ladder": hints,
    "fairness_test": {"requirements": {"min_disjoint_proof_paths": 1, "max_inference_depth": 3, "all_red_herrings_refutable": True, "culprit_uniquely_entailed": True, "no_hidden_fact_dependency": True, "max_required_actions": 30}, "runs": []},
    "ending_explanation": ending,
    "expert_review": [{"role": r, "reviewer": "—", "status": "pending", "content_hash": "unbound", "date": "2026-10-27", "notes_ar": "بانتظار مراجعة بشرية؛ لم يُجرَ أي اعتماد."} for r in
                      ["narrative_editor", "scientific_reviewer", "learning_designer", "age_appropriateness", "cultural_reviewer", "legal_rights", "safety"]],
}
ui = {
    "case_id": CID, "tutorial": True,
    "clock": {"epoch_hhmm": "14:00", "zone_label_ar": "توقيت المبنى"},
    "cover": {"title_ar": "دفتر المختبر الضائع", "tagline_ar": "الجميع يشير إلى هادي… والسجلات تقول شيئاً آخر", "kicker_ar": "الملف الأول · تمهيدي", "glyph": "◐", "accent": "cyan"},
    "cold_open_ar": ["الأربعاء، الثالثة عصراً.", "دفتر واحد اختفى من طاولة المختبر، ومشرف النادي واثق من أن هادي هو من أخذه.", "هادي ينفي، ويقول إنه غادر المبنى في الثانية. لكن في ملفك سجلاً يخالف ذلك.", "ابدأ بتحديد التعارض. ثم اسأل: هل هو التعارض الذي يهم؟"],
    "labs": [],
    "source_classes": [
        {"id": "primary_record", "label_ar": "سجل أصلي", "help_ar": "يُنتجه نظام أو شخص لحظة الحدث دون وسيط، كورقة توقيع أو سجل بوابة."},
        {"id": "redisplay", "label_ar": "نسخة معروضة", "help_ar": "معلومة نُقلت من سجل آخر."},
        {"id": "claim", "label_ar": "قول أو تصريح", "help_ar": "إفادة شخص؛ تُقاس بالسجلات لا بنبرة صاحبها."},
        {"id": "template", "label_ar": "قالب أو نموذج", "help_ar": "نص جاهز لا يصف الحدث الفعلي بذاته."},
        {"id": "public_document", "label_ar": "وثيقة منشورة", "help_ar": "وثيقة معلنة ومعروف ناشرها."}],
    "limit_menu": [
        {"id": "l_why", "label_ar": "الأدلة لا تفسّر لماذا لم تُبلغ الفنية بنقل الدفتر"},
        {"id": "l_time", "label_ar": "ورقة الفنية غير مؤرّخة فلا تثبت وقت النقل"},
        {"id": "l_invalid_tone", "label_ar": "توتر هادي في المقابلة يدل على أنه يخفي شيئاً"},
        {"id": "l_invalid_gate", "label_ar": "خطأ هادي في ساعة الخروج يثبت أنه كاذب"}],
    "mind_change_menu": [
        {"id": "m_late_sign", "label_ar": "ظهور توقيع لهادي في المختبر بعد 14:30"},
        {"id": "m_notebook_gone", "label_ar": "ثبوت أن الدفتر لم يكن على الطاولة 14:15"},
        {"id": "m_popular", "label_ar": "كثرة من يظنون أن هادي هو الفاعل"}],
    "skills": [{"skill_id": "KO-RS-05-001", "track": "B"}, {"skill_id": "KO-RS-05-005", "track": "B"}, {"skill_id": "KO-RS-05-002", "track": "D"}],
    "stage_hooks_ar": {"briefing": "الجميع يشير إلى هادي… فهل يكفي أن يشير الجميع؟", "investigating": "تعارض واحد ظاهر، وآخر لم تنتبه له بعد.", "review": "قبل أن تُغلق الملف: ما الذي لا تعرفه؟", "resolved": "أول ملف أُغلق. الملف التالي أكبر."},
    "character_glyphs": {"hadi": "هـ", "jamal": "ج", "omar": "ع", "samira": "س"},
}
sc = {
    "case_id": CID,
    "accepted_conclusions": {"h_samira": {"grade": 1, "note_ar": "استنتاج متسق مع الأدلة."}, "h_hadi": {"grade": 0, "note_ar": "يخلط بين خطأ في ساعة خروج المبنى ومكان الدفتر."}, "h_loss": {"grade": 0, "note_ar": "الدفتر وُجد في مكان محدد، لم يضِع."}},
    "confidence_band": {"h_samira": [65, 90], "h_hadi": [0, 15], "h_loss": [0, 20]},
    "source_key": {"ev_lab_sheet": "primary_record", "ev_gate_log": "primary_record", "ev_cleaning_ticket": "primary_record", "ev_note_shelf": "primary_record", "ev_jamal_statement": "claim", "ev_hadi_statement": "claim"},
    "link_key": {"h_samira": {"ev_cleaning_ticket": "supports", "ev_note_shelf": "supports", "ev_notebook_closet": "supports", "ev_gate_log": "neutral"},
                 "h_hadi": {"ev_gate_log": "supports", "ev_lab_sheet": "weakens", "ev_jamal_statement": "weakens", "ev_notebook_closet": "weakens"},
                 "h_loss": {"ev_notebook_closet": "weakens", "ev_note_shelf": "weakens"}},
    "required_limits": ["l_why", "l_time"], "valid_mind_changers": ["m_late_sign", "m_notebook_gone"], "invalid_limits": ["l_invalid_tone", "l_invalid_gate"],
    "decisive_evidence": ["ev_lab_sheet", "ev_jamal_statement", "ev_cleaning_ticket", "ev_note_shelf"],
    "lab_requirement": None,
    "timeline_requirement": [{"evidence_id": "ev_lab_sheet", "utc_minute": 10, "tol": 3}, {"evidence_id": "ev_cleaning_ticket", "utc_minute": 20, "tol": 3}, {"evidence_id": "ev_gate_log", "utc_minute": 40, "tol": 3}],
    "refuted_hypotheses": ["h_hadi", "h_loss"],
    "criteria_map": {"c_source": "source_typing", "c_conflict": "conflict_resolution", "c_links": "hypothesis_links", "c_uncertainty": "uncertainty", "c_revision": "revision", "c_elimination": "elimination", "c_justification": "justification_human"},
    "caps": {"no_citations_max": 45, "no_conflict_resolution_max": 70},
}
os.makedirs(OUT, exist_ok=True)
for suf, obj in [("", core), (".ui", ui), (".scoring", sc)]:
    with open(os.path.join(OUT, f"{CID}{suf}.json"), "w", encoding="utf8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
print("ok")
