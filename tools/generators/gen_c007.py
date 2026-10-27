#!/usr/bin/env python3
# Case c007 «مذكّرة المختبر الناقصة» — measurement, unit conversion and the limits of inference. A school-lab headline compares two
# conductivity readings recorded in different units and at different water temperatures. After converting, a small residual remains
# that the evidence cannot explain. No-culprit convention: the press officer who copied the unit-less summary (unintended exaggeration)
# is in culprit_ids. All figures are INVENTED and representative (simulation constants), not scientific reference values.
# Usage: gen_c007.py OUT_DIR
import json, sys, os
OUT = sys.argv[1]
CID = "c007_incomplete_lab_note"

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

ch("rana", "رنا السعدي", "witness", "باحثة متدربة في مختبر المدرسة",
   "متحمسة ودقيقة في تدوين ما تفعله، وتقلق من أن يُظن أنها أخطأت في القياس.",
   ["ألا يُنسب إليها خطأ في القياس", "أن يُفهم ما دوّنته كما كتبته"],
   [L("rn_greet", "greeting", "أهلاً. كل قياس دوّنته بيدي في ورقته."),
    L("rn_samples", "reveal", "أخذت العينة الأولى صباحاً من حافة الحوض الشمالية، والثانية عصراً من الحافة الجنوبية قرب فتحة التدوير. وقست حرارة كل عينة قبل قراءتها.", ["f_sample1_taken", "f_sample2_taken"], ["cl_rana_same"]),
    L("rn_refuse", "refuse_secret", "دوّنت كل شيء في الورقتين."),
    L("rn_mode", "reveal", "نعم... بعد الظهر فعّلت نمط المدى العالي، فصار الجهاز يعرض بالملّي سيمنز لكل متر. كتبت الوحدة في الورقة الثانية، لكن الملخص المختصر لم يتسع لها.", ["f_display_mode_changed"]),
    L("rn_unknown", "deflect_unknown", "لا أعرف أكثر من ذلك."),
    L("rn_off", "deflect_offtopic", "اسألني عن القياس وكيف جرى."),
    L("rn_bye", "farewell", "أتمنى أن تُفهم القراءتان كما كُتبتا.")])
ch("haitham", "د. هيثم الفارس", "expert", "مشرف المختبر",
   "منهجي وحذر، يفرّق بين ما قيس وما فُسّر، ولا يجزم فوق ما تسمح به الأرقام.",
   ["أن يبقى الجهاز موثوقاً", "ألا يخرج بيان يتجاوز الأرقام"],
   [L("ht_greet", "greeting", "تفضّل. أحب أن أرى الأرقام قبل أي عنوان."),
    L("ht_margin", "reveal", "هامش خطأ الجهاز المعتمد خمسة بالمئة من القراءة بعد التعويض الحراري إلى 25 درجة. هذا ما تقوله ورقة الجهاز عندنا.", ["f_device_margin"]),
    L("ht_cal", "reveal", "عايرت الجهاز قبل تسعة أيام بمحلول معياري، ولم أعايره بين الجلستين.", ["f_calibrated"]),
    L("ht_calc", "reveal", "حسبت القراءتين مساء اليوم نفسه بعد توحيد الوحدة والحرارة، وهي في الورقة التي أعطيك إياها. ما يتبقى صغير، ولا أجزم بسببه.", ["f_super_calc"]),
    L("ht_unknown", "deflect_unknown", "لا أستطيع أن أجزم بما لم يُقَس."),
    L("ht_off", "deflect_offtopic", "اسألني عن الجهاز والأرقام."),
    L("ht_bye", "farewell", "راجع الأرقام قبل أن تحكم.")])
ch("yasser", "ياسر العلوي", "suspect", "مسؤول النشر في المدرسة",
   "مشغول ويكتب بسرعة، يثق بالملخصات القصيرة، ويخشى أن يُقال إن خبره بالغ.",
   ["ألا يُنسب إليه تضخيم الخبر", "نشر الخبر في موعده"],
   [L("ys_greet", "greeting", "أهلاً. نشرنا الخبر كما وصلنا."),
    L("ys_read", "reveal", "كتبت الخبر من الملخص الذي وصلني: العينة الأولى 410 والثانية 54، فبدا لي الفارق كبيراً جداً.", ["f_officer_read_summary"], ["cl_press_big"]),
    L("ys_refuse", "refuse_secret", "الملخص هو المعتمد عندنا."),
    L("ys_units", "reveal", "لم أفتح ورقتي القياس ولا جدول الوحدات، وظننت أن الرقمين بوحدة واحدة.", ["f_no_unit_table"]),
    L("ys_unknown", "deflect_unknown", "لا علم لي بذلك."),
    L("ys_off", "deflect_offtopic", "اسألني عن كتابة الخبر فقط."),
    L("ys_bye", "farewell", "سأراجع الخبر قبل أي تحديث.")])

locations = [{"id": "loc_lab", "name_ar": "مختبر المدرسة", "description_ar": "جهاز قياس التوصيلية وأوراق القياس."},
             {"id": "loc_fountain", "name_ar": "نافورة ساحة المدرسة", "description_ar": "حوض له حافتان شمالية وجنوبية، وفتحة تدوير في الجنوب."},
             {"id": "loc_press", "name_ar": "مكتب النشر", "description_ar": "الأخبار والملخصات الواردة إلى المدرسة."},
             {"id": "loc_records", "name_ar": "ملفات المختبر", "description_ar": "سجل الظروف وسجل المعايرة وورقة بيانات الجهاز."}]
objects = [{"id": "obj_meter", "name_ar": "جهاز قياس التوصيلية", "description_ar": "جهاز مدرسي يعرض التوصيلية بوحدتين بحسب النمط."},
           {"id": "obj_water", "name_ar": "ماء النافورة", "description_ar": "عينتان أُخذتا من حوض النافورة."}]
orgs = [{"id": "org_lab", "name_ar": "مختبر المدرسة", "description_ar": "مختبر طلابي يشرف عليه معلّم."}]

facts = []
def F(id, st, kind, subj, spoiler, time=None, loc=None, ko=None):
    d = {"id": id, "statement_ar": st, "kind": kind, "subject_ids": subj, "spoiler_level": spoiler}
    if time: d["time"] = time
    if loc: d["location_id"] = loc
    if ko: d["science_ko_refs"] = ko
    facts.append(d)
F("f_announce", "أعلن المختبر المدرسي أن بين عينتين من ماء النافورة فارقاً كبيراً.", "event", ["org_lab", "obj_water"], 0)
F("f_press_claim", "نشر تقرير صحفي أن توصيلية ماء النافورة هبطت من 410 إلى 54 وعدّ ذلك تغيراً جوهرياً.", "event", ["yasser", "obj_water"], 0)
F("f_sample1_taken", "أُخذت العينة الأولى الساعة 07:30 من حافة الحوض الشمالية، وحرارة الماء 15.0 درجة مئوية، وقراءتها 410 ميكروسيمنز لكل سنتيمتر.", "event", ["rana", "obj_water"], 1, T(30), "loc_fountain", ["KO-RS-06-003"])
F("f_sample2_taken", "أُخذت العينة الثانية الساعة 15:00 من حافة الحوض الجنوبية قرب فتحة التدوير، وحرارة الماء 25.0 درجة مئوية، وقراءتها 54.0 ملّي سيمنز لكل متر.", "event", ["rana", "obj_water"], 1, T(480), "loc_fountain", ["KO-RS-06-003"])
F("f_display_mode_changed", "فعّلت الباحثة نمط المدى العالي قبل القياس الثاني، فتحوّل عرض الجهاز إلى ملّي سيمنز لكل متر.", "event", ["rana", "obj_meter"], 1, T(470, "approx"), "loc_lab")
F("f_device_margin", "هامش خطأ الجهاز المعتمد خمسة بالمئة من القراءة بعد التعويض الحراري إلى 25 درجة، بمعامل تعويض 2.0 بالمئة لكل درجة.", "attribute", ["obj_meter"], 1, None, "loc_lab", ["KO-RS-06-003"])
F("f_calibrated", "عُوير الجهاز قبل تسعة أيام ولم يُعايَر بين الجلستين.", "state", ["obj_meter"], 1, None, "loc_lab")
F("f_super_calc", "أعدّ المشرف مساءً ورقة حساب توحّد الوحدة والحرارة للقراءتين.", "event", ["haitham"], 1, T(660), "loc_lab")
F("f_officer_read_summary", "كتب مسؤول النشر الخبر من ملخص يذكر الرقمين دون وحدتيهما.", "event", ["yasser"], 1, None, "loc_press")
F("f_no_unit_table", "لم يفتح مسؤول النشر ورقتي القياس ولا جدول الوحدات قبل النشر.", "state", ["yasser"], 2, None, "loc_press")
F("f_unit_mismatch", "سُجلت القراءتان بوحدتين مختلفتين، ميكروسيمنز لكل سنتيمتر ثم ملّي سيمنز لكل متر، والقراءة الثانية تعادل 540 بوحدة الأولى.", "relation", ["obj_water", "obj_meter"], 2, None, "loc_lab", ["KO-RS-05-010"])
F("f_temp_differ", "أُخذت العينتان في درجتي حرارة مختلفتين، 15.0 ثم 25.0 درجة مئوية.", "relation", ["obj_water"], 2, None, "loc_fountain", ["KO-RS-06-003"])
F("f_within_margin", "بعد توحيد الوحدة والتعويض الحراري تقترب القراءتان من 512.5 و540، ويبقى فارق اسمي صغير تتسع له فترتا الخطأ المتداخلتان؛ فلا يكفي لإثبات تغير ولا لنفيه، وسببه غير محسوم.", "relation", ["obj_water", "obj_meter"], 3, None, "loc_lab", ["KO-RS-05-010", "KO-RS-06-003"])
claims = [
    {"id": "cl_press_big", "statement_ar": "التوصيلية هبطت من 410 إلى 54، وهذا تغير جوهري مثبت.", "kind": "honest_mistake", "held_by": ["yasser"], "true_fact_id": "f_within_margin", "contradicted_by_evidence_ids": ["ev_sheet2", "ev_super_calc"]},
    {"id": "cl_rana_same", "statement_ar": "قست العينتين بالطريقة نفسها.", "kind": "half_truth", "held_by": ["rana"], "true_fact_id": "f_unit_mismatch", "contradicted_by_evidence_ids": ["ev_sheet2", "ev_conditions"]},
]
timeline = [
    {"id": "te_s1", "description_ar": "الباحثة تأخذ العينة الأولى وتقيسها.", "time": T(30), "location_id": "loc_fountain", "actor_ids": ["rana"], "fact_ids": ["f_sample1_taken"], "motivated_by_ar": "جدول القياس الصباحي في المختبر"},
    {"id": "te_mode", "description_ar": "الباحثة تفعّل نمط المدى العالي في الجهاز.", "time": T(470, "approx"), "location_id": "loc_lab", "actor_ids": ["rana"], "fact_ids": ["f_display_mode_changed"], "motivated_by_ar": "أرادت قراءة أوسع لعينة العصر"},
    {"id": "te_s2", "description_ar": "الباحثة تأخذ العينة الثانية وتقيسها.", "time": T(480), "location_id": "loc_fountain", "actor_ids": ["rana"], "fact_ids": ["f_sample2_taken"], "motivated_by_ar": "جدول القياس بعد الظهر"},
    {"id": "te_calc", "description_ar": "المشرف يحسب القراءتين بعد التوحيد.", "time": T(660), "location_id": "loc_lab", "actor_ids": ["haitham"], "fact_ids": ["f_super_calc"], "motivated_by_ar": "أراد أن يراجع الأرقام قبل أي بيان"},
]

ev = []
def V(id, title, kind, content, acts, supports, rel, limits, contradicts=None, red=False, ko=None, loc=None):
    d = {"id": id, "title_ar": title, "kind": kind, "content_ar": content, "acquired_by_action_ids": acts, "supports_fact_ids": supports, "reliability": rel, "limits_ar": limits}
    if contradicts: d["contradicts_claim_ids"] = contradicts
    if red: d["is_red_herring"] = True
    if ko: d["forensic_ko_ref"] = ko
    if loc: d["location_id"] = loc
    ev.append(d)
V("ev_sheet1", "ورقة القياس الأولى", "lab_result",
  "ورقة قياس 1 — جهاز التوصيلية\nالوقت: 07:30 | الموضع: حافة الحوض الشمالية\nحرارة الماء: 15.0 °م\nالقراءة: 410\nالوحدة المعروضة: ميكروسيمنز لكل سنتيمتر\nالمدوِّنة: ر. السعدي",
  ["a_read_sheet1"], ["f_sample1_taken"], "strong", "قياس واحد لعينة واحدة عند لحظة واحدة؛ لا يصف ماء النافورة في بقية اليوم، ولا يقارن بنفسه بقياس بوحدة أخرى.", ko="KO-RS-06-003", loc="loc_lab")
V("ev_sheet2", "ورقة القياس الثانية", "lab_result",
  "ورقة قياس 2 — جهاز التوصيلية\nالوقت: 15:00 | الموضع: حافة الحوض الجنوبية قرب فتحة التدوير\nحرارة الماء: 25.0 °م\nالقراءة: 54.0\nالوحدة المعروضة: ملّي سيمنز لكل متر\nالمدوِّنة: ر. السعدي",
  ["a_read_sheet2"], ["f_sample2_taken"], "strong", "قياس واحد لعينة واحدة عند لحظة واحدة، بوحدة غير وحدة الورقة الأولى وفي موضع آخر.", contradicts=["cl_press_big", "cl_rana_same"], ko="KO-RS-06-003", loc="loc_lab")
V("ev_press_report", "الخبر الصحفي", "documentary",
  "خبر في موقع محلي (نسخة)\nالعنوان: «ماء نافورة المدرسة يتغيّر كثيراً!»\nالمتن: «أظهرت قياسات مختبر المدرسة أن توصيلية ماء النافورة هبطت من 410 إلى 54 خلال يوم واحد، أي بنسبة تتجاوز 86%، في نتيجة قاطعة لا تحتمل التأويل.»",
  ["a_read_press"], ["f_press_claim", "f_announce"], "weak", "نص صحفي يعرض رقمين بلا وحدات ولا ظروف أخذ العينات؛ هو ادعاء عن القياس لا قياس.", loc="loc_press")
V("ev_summary_sheet", "ملخص النتائج في صفحة واحدة", "documentary",
  "ملخص نتائج مختبر المدرسة\nالعينة | الرقم\n1 | 410\n2 | 54\nملاحظة: التفاصيل في ورقتي القياس.",
  ["a_read_summary"], ["f_officer_read_summary"], "weak", "جدول مختصر بلا عمود للوحدات ولا للحرارة؛ لا يغني عن ورقتي القياس.", loc="loc_press")
V("ev_conditions", "سجل ظروف أخذ العينات", "documentary",
  "سجل ظروف أخذ العينات (ورقة مشتركة)\n1 — 07:30، ظل الصباح، ماء 15.0 °م، الحافة الشمالية.\n2 — 15:00، شمس مباشرة، ماء 25.0 °م، الحافة الجنوبية قرب فتحة التدوير.\nلا قراءات أخرى في اليوم.",
  ["a_read_conditions"], ["f_temp_differ"], "strong", "يصف ظروف أخذ كل عينة، ولا يقول شيئاً عن تأثير هذه الظروف في القراءة.", contradicts=["cl_rana_same"], loc="loc_records")
V("ev_device_sheet", "ورقة بيانات الجهاز (مرجع تعليمي)", "documentary",
  "ورقة بيانات جهاز التوصيلية — مرجع تعليمي لهذه المحاكاة\n- التحويل: 1 ملّي سيمنز لكل متر = 10 ميكروسيمنز لكل سنتيمتر.\n- المرجع الحراري 25 °م؛ القراءة عند 25 = القراءة ÷ (1 + 0.02 × (الحرارة − 25)).\n- معامل التعويض هنا: 2.0% لكل درجة.\n- هامش الخطأ: ±5% من القراءة بعد التعويض.\n- نمط المدى العالي يعرض بالملّي سيمنز لكل متر.",
  ["a_read_device"], ["f_device_margin"], "moderate", "ثوابت تمثيلية لغرض المحاكاة التعليمية؛ لا تُستعمل خارجها دون مراجعة علمية.", loc="loc_records")
V("ev_cal_log", "سجل معايرة الجهاز", "documentary",
  "سجل معايرة الجهاز\nآخر معايرة: قبل تسعة أيام بمحلول معياري؛ الانحراف ضمن الحد المقبول.\nلا معايرة بين جلستي الثلاثاء.",
  ["a_get_cal"], ["f_calibrated"], "strong", "يثبت حال الجهاز لا حال الماء؛ ومعايرة سليمة لا تجعل مقارنة رقمين بوحدتين مختلفتين صحيحة.", loc="loc_records")
V("ev_trainee_note", "إفادة الباحثة المتدربة", "testimonial",
  "ملخص إفادة رنا السعدي:\n«بعد الظهر فعّلت نمط المدى العالي، فصار الجهاز يعرض بالملّي سيمنز لكل متر، وكتبت الوحدة في الورقة الثانية. أما الورقة الأولى فكانت بالميكروسيمنز لكل سنتيمتر.»",
  ["a_note_rana"], ["f_display_mode_changed"], "moderate", "ذاكرة صاحبة الفعل عن إعداد جهاز؛ تتفق مع الورقتين لكنها تحتاج إليهما لتأكيد القيم.", loc="loc_lab")
V("ev_officer_stmt", "إفادة مسؤول النشر", "testimonial",
  "ملخص إفادة ياسر العلوي:\n«كتبت الخبر من الملخص ذي الرقمين، ولم أفتح جدول الوحدات. ظننت أن الرقمين بوحدة واحدة.»",
  ["a_note_yasser"], ["f_no_unit_table"], "weak", "إفادة صاحب علاقة بالخبر؛ تفسّر كيف وُلد الخبر ولا تقيس الماء.", contradicts=["cl_press_big"], loc="loc_press")
V("ev_super_calc", "ورقة حساب المشرف", "documentary",
  "ورقة حساب د. هيثم الفارس (مساء الثلاثاء، 18:00)\nتوحيد الوحدة: 54.0 ملّي سيمنز لكل متر تعادل 540 ميكروسيمنز لكل سنتيمتر.\nالتعويض إلى 25 °م: العينة 1 = 410 ÷ (1 + 0.02 × (15 − 25)) = 512.5؛ العينة 2 = 540 (حرارتها 25 أصلاً).\nالفارق الاسمي: 27.5.\nالهامش ±5%: العينة 1 بين 486.9 و538.1؛ العينة 2 بين 513.0 و567.0.\nملاحظة: الموضعان مختلفان والوقتان مختلفان.",
  ["a_get_calc"], ["f_super_calc"], "moderate", "حساب مشتق من الورقتين وليس قياساً جديداً؛ يقوم على الثوابت التمثيلية نفسها، فيُقاس بالورقتين وبورقة الجهاز.", contradicts=["cl_press_big"], loc="loc_lab")

def P(t, i): return {"ref_type": t, "ref_id": i}
inf = []
def I(id, prem, ct, concl, rel, strength, rule, ks):
    inf.append({"id": id, "premises": prem, "conclusion": {"ref_type": ct, "ref_id": concl}, "relation": rel, "strength": strength, "rule_ar": rule, "skill_ko_refs": ks})
E = lambda x: P("evidence", x)
Fa = lambda x: P("fact", x)
GK = P("general_knowledge", "milli_micro_unit_conversion")
# path A: the two measurement sheets + the instrument data sheet
I("i_units_a", [E("ev_sheet1"), E("ev_sheet2"), GK], "fact", "f_unit_mismatch", "establishes", "strong",
  "الورقة الأولى بالميكروسيمنز لكل سنتيمتر والثانية بالملّي سيمنز لكل متر؛ والمضاعفة بين الوحدتين تجعل 54.0 تعادل 540 بوحدة الأولى.", ["KO-RS-05-010"])
I("i_temp_a", [E("ev_sheet1"), E("ev_sheet2")], "fact", "f_temp_differ", "establishes", "strong",
  "الورقتان تسجلان حرارتي الماء 15.0 و25.0 درجة؛ فالعينتان لم تُقاسا في الظرف الحراري نفسه.", ["KO-RS-06-003"])
I("i_margin_a", [Fa("f_unit_mismatch"), Fa("f_temp_differ"), E("ev_device_sheet")], "fact", "f_within_margin", "establishes", "strong",
  "بتوحيد الوحدة ثم الحرارة بحسب ورقة الجهاز يصبح الفرق صغيراً، وتتداخل فترتا الخطأ المحسوبتان من الهامش المعتمد.", ["KO-RS-05-010"])
# path B: the trainee's account + the conditions log + the supervisor's worked calculation
I("i_units_b", [E("ev_trainee_note"), GK], "fact", "f_unit_mismatch", "establishes", "strong",
  "الباحثة تقرّ بتبديل نمط العرض بين الجلستين، فالقراءتان بوحدتين مختلفتين وتحتاجان إلى تحويل قبل المقارنة.", ["KO-RS-05-010"])
I("i_temp_b", [E("ev_conditions")], "fact", "f_temp_differ", "establishes", "strong",
  "سجل الظروف يذكر حرارة كل عينة، 15.0 و25.0 درجة.", ["KO-RS-06-003"])
I("i_margin_b", [E("ev_super_calc")], "fact", "f_within_margin", "establishes", "strong",
  "ورقة المشرف توحّد الوحدة والحرارة ثم تضع فترتي الخطأ، وتبيّن أنهما تتداخلان.", ["KO-RS-05-010"])
I("i_support_units", [Fa("f_unit_mismatch"), Fa("f_temp_differ"), Fa("f_within_margin")], "hypothesis", "h_units", "supports", "strong",
  "اختلاف الوحدة واختلاف الحرارة يفسران معظم الفارق الظاهر، وما يتبقى يقع ضمن هامش الجهاز.", ["KO-RS-05-002"])
I("i_rule_change", [Fa("f_within_margin")], "hypothesis", "h_change", "rules_out", "strong",
  "فارق صغير تتسع له فترتا الخطأ لا يثبت تغيراً؛ فدعوى «التغير المثبت» غير مسنودة.", ["KO-RS-06-009"])
I("i_rule_none", [Fa("f_within_margin")], "hypothesis", "h_none", "rules_out", "strong",
  "الفارق الاسمي لا يساوي صفراً، وفترتا الخطأ تتسعان لفارق حقيقي صغير؛ فنفي كل فرق إطلاقاً غير مسنود.", ["KO-RS-06-009"])
I("i_press_claim", [E("ev_summary_sheet"), E("ev_sheet2")], "claim", "cl_press_big", "contradicts_claim", "strong",
  "الملخص بلا وحدات، وورقة القياس الثانية بوحدة أخرى؛ فالمقارنة المباشرة بين 410 و54 غير صحيحة.", ["KO-RS-05-001"])
I("i_rana_claim", [E("ev_sheet1"), E("ev_sheet2")], "claim", "cl_rana_same", "contradicts_claim", "suggestive",
  "الطريقة واحدة لكن الوحدة المعروضة والحرارة والموضع تغيّرت بين الجلستين.", ["KO-RS-05-001"])

ck = [
    {"character_id": "rana", "knows": [{"fact_id": "f_sample1_taken", "access": "witnessed", "certainty": "certain"}, {"fact_id": "f_sample2_taken", "access": "witnessed", "certainty": "certain"}],
     "hides": [{"fact_id": "f_display_mode_changed", "reveal_when": {"presented": {"evidence_id": "ev_press_report", "to_character": "rana"}}, "cover_claim_id": None, "reveal_line_id": "rn_mode"}],
     "believes": [{"claim_id": "cl_rana_same", "stance": "sincere"}]},
    {"character_id": "haitham", "knows": [{"fact_id": "f_device_margin", "access": "professional", "certainty": "certain"}, {"fact_id": "f_calibrated", "access": "witnessed", "certainty": "certain"}, {"fact_id": "f_super_calc", "access": "witnessed", "certainty": "certain"}], "hides": [], "believes": []},
    {"character_id": "yasser", "knows": [{"fact_id": "f_officer_read_summary", "access": "witnessed", "certainty": "certain"}],
     "hides": [{"fact_id": "f_no_unit_table", "reveal_when": {"presented": {"evidence_id": "ev_sheet2", "to_character": "yasser"}}, "cover_claim_id": None, "reveal_line_id": "ys_units"}],
     "believes": [{"claim_id": "cl_press_big", "stance": "sincere"}]},
]
hyps = [
    {"id": "h_change", "statement_ar": "حدث تغير جوهري مثبت في ماء النافورة بين العينتين.", "is_true": False, "plausibility_at_start": "high"},
    {"id": "h_units", "statement_ar": "الفارق الظاهر الضخم جاء من قراءتين بوحدتين وحرارتين مختلفتين؛ وبعد التوحيد يبقى فارق صغير ضمن هامش الخطأ لا يكفي للجزم بتغير ولا بنفيه.", "is_true": True, "plausibility_at_start": "low"},
    {"id": "h_none", "statement_ar": "لا يمكن أن يوجد أي فرق بين العينتين إطلاقاً.", "is_true": False, "plausibility_at_start": "low"},
]
mis = [
    {"id": "rh_press", "points_to_hypothesis_id": "h_change", "planted_via_ar": "الخبر والملخص يعرضان 410 ثم 54 بلا وحدات، فيبدو الهبوط هائلاً.", "evidence_ids": ["ev_press_report", "ev_summary_sheet"], "refuted_by_inference_ids": ["i_press_claim", "i_rule_change"],
     "fairness_note_ar": "ورقتا القياس وورقة الجهاز متاحتان بالإجراءات العادية، وفيهما الوحدات والحرارة وجدول التحويل."},
    {"id": "rh_units_only", "points_to_hypothesis_id": "h_change", "planted_via_ar": "بعد تحويل الوحدة وحدها يظهر ارتفاع من 410 إلى 540، فقد يظن القارئ أن التغير حقيقي لكن باتجاه معاكس.", "evidence_ids": ["ev_sheet1", "ev_sheet2"], "refuted_by_inference_ids": ["i_rule_change"],
     "fairness_note_ar": "الورقتان تذكران حرارة الماء، وورقة الجهاز تعطي صيغة التعويض والهامش، فالخطوة التالية للتحويل متاحة."},
    {"id": "rh_cal", "points_to_hypothesis_id": "h_none", "planted_via_ar": "سجل المعايرة سليم، فقد يُظن أن القراءتين لا بد أن تتطابقا.", "evidence_ids": ["ev_cal_log"], "refuted_by_inference_ids": ["i_rule_none"],
     "fairness_note_ar": "سجل المعايرة يصف الجهاز لا الماء، والفارق الاسمي المتبقي ظاهر في ورقة الحساب."},
]
los = [
    {"id": "lo_claim", "statement_ar": "يفرّق بين الرقم المقاس وبين ما نُقل عنه في الخبر أو الملخص، ويصنّف المصدر.", "skill_ko_ref": "KO-RS-05-001", "observable_behaviors_ar": ["يصنّف الأوراق والأخبار", "يقابل القول بالسجل"], "evidence_sources": ["evidence_board"]},
    {"id": "lo_timeline", "statement_ar": "يرتّب القياسات على خط زمني ليربط كل قراءة بظرفها.", "skill_ko_ref": "KO-RS-05-005", "observable_behaviors_ar": ["يضع الأدلة في أزمنتها"], "evidence_sources": ["timeline_task", "action_log"]},
    {"id": "lo_hyp", "statement_ar": "يوازن بين فرضيتين على الأقل ويستبعد ما تنقضه الأدلة.", "skill_ko_ref": "KO-RS-05-002", "observable_behaviors_ar": ["يضيف فرضيات", "يستبعد بدليل"], "evidence_sources": ["hypothesis_ledger"]},
    {"id": "lo_diag", "statement_ar": "يحوّل الوحدات ويوحّد الظروف قبل أن يقارن قياسين.", "skill_ko_ref": "KO-RS-06-003", "observable_behaviors_ar": ["يربط الدليل بالفرضية باتجاه صحيح"], "evidence_sources": ["evidence_board", "final_justification"]},
    {"id": "lo_calib", "statement_ar": "يصوغ ثقته بحدود هامش الخطأ.", "skill_ko_ref": "KO-RS-05-010", "observable_behaviors_ar": ["يختار ثقة معقولة", "يذكر حدوداً"], "evidence_sources": ["final_justification"]},
    {"id": "lo_revise", "statement_ar": "يراجع رأيه الأول حين يظهر ما يخالفه.", "skill_ko_ref": "KO-RS-06-009", "observable_behaviors_ar": ["يغيّر فرضيته الرائدة بدليل"], "evidence_sources": ["hypothesis_ledger"]},
]
def levels(d): return [{"score": i, "descriptor_ar": t} for i, t in enumerate(d)]
rub = {
    "reference_answer_ar": "الملف لا يثبت تغيراً جوهرياً في ماء النافورة. القراءتان مكتوبتان بوحدتين مختلفتين، 410 بالميكروسيمنز للسنتيمتر الواحد و54.0 بالملّي سيمنز للمتر الواحد، أي 540 بوحدة الأولى، وقد أُخذتا عند حرارتين مختلفتين، 15 و25 درجة. وبعد التوحيد تقترب القراءتان من 512.5 و540 وتتداخل فترتا الخطأ، فالمبالغة جاءت من مقارنة رقمين ظاهرهما واحد. ويبقى فارق اسمي صغير لا نجزم بسببه، لاختلاف الوقت والموضع ولأن ثابتي التعويض والهامش تمثيليان. حدود الاستنتاج: عينتان فقط في يوم واحد، دون قياسات متكررة.",
    "criteria": [
        {"id": "c_source", "name_ar": "تصنيف المصادر", "objective_ids": ["lo_claim"], "scored_by": "deterministic", "weight": 0.15, "levels": levels(["لم يصنّف", "أخطأ في الأغلب", "نصف صحيح", "معظمه صحيح", "كله صحيح"])},
        {"id": "c_conflict", "name_ar": "ربط القياسات بأزمنتها", "objective_ids": ["lo_timeline"], "scored_by": "deterministic", "weight": 0.15, "levels": levels(["لم يضع شيئاً", "وضع قليلاً", "وضع نصفها صحيحاً", "معظمها", "كلها في موضعها"])},
        {"id": "c_links", "name_ar": "ربط الأدلة بالفرضيات", "objective_ids": ["lo_diag"], "scored_by": "deterministic", "weight": 0.2, "levels": levels(["لا روابط", "قليلة", "نصفها صحيح", "معظمها", "كلها دقيقة"])},
        {"id": "c_uncertainty", "name_ar": "معايرة الثقة", "objective_ids": ["lo_calib"], "scored_by": "deterministic", "weight": 0.2, "levels": levels(["ثقة مفرطة", "حدود قليلة", "جزئية", "معقولة", "معايَرة كاملة"])},
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
    H("hg1", 1, "metacognitive", "أين ينتهي ما قاسه الجهاز وتبدأ طريقة عرض الرقم وتفسيره؟", {"always": True}, None, 0.02),
    H("hg2", 2, "focus_area", "ضع كل معلومة في جدول: مصدر أصلي أم نسخة أم تعليق؟", he("ev_summary_sheet"), None, 0.04),
    H("hg3", 3, "pointer", "راجع تحديداً الدليل الذي يوضح وحدة الرقم وظرف أخذه وسياق الوثيقة.", he("ev_sheet2"), None, 0.06),
    H("hm1", 1, "metacognitive", "هل الرقمان معروضان بالوحدة نفسها؟ وهل أُخذا عند الحرارة نفسها؟", he("ev_sheet2"), "i_units_a", 0.02),
    H("hm2", 2, "pointer", "ابحث عن مرجع يعطي جدول التحويل وصيغة التعويض الحراري وهامش الخطأ.", he("ev_sheet2"), "i_units_a", 0.05),
    H("hm3", 3, "partial_reveal", "افتح ورقة بيانات الجهاز، وحوّل 54.0 ملّي سيمنز لكل متر إلى وحدة الورقة الأولى، ثم وحّد الحرارة وقارن مع الهامش.", he("ev_device_sheet"), "i_units_a", 0.1),
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
he2 = he
Act("a_read_sheet1", "examine", "افتح ورقة القياس الأولى", al, [G("ev_sheet1")], "loc_lab", "READ_SHEET1")
Act("a_read_press", "examine", "اقرأ الخبر الصحفي", al, [G("ev_press_report")], "loc_press", "READ_PRESS")
Act("a_read_sheet2", "examine", "افتح ورقة القياس الثانية", he("ev_sheet1"), [G("ev_sheet2")], "loc_lab", "READ_SHEET2")
Act("a_read_summary", "examine", "اطلب الملخص الذي استند إليه الخبر", he("ev_press_report"), [G("ev_summary_sheet")], "loc_press", "READ_SUMMARY")
Act("a_read_conditions", "search_location", "افتح سجل ظروف أخذ العينات", he("ev_press_report"), [G("ev_conditions")], "loc_records", "READ_CONDITIONS")
Act("a_read_device", "search_location", "ابحث عن ورقة بيانات الجهاز", he("ev_sheet2"), [G("ev_device_sheet")], "loc_records", "READ_DEVICE")
Act("a_int_rana", "interview", "ابدأ مقابلة رنا", al, [{"op": "raise_trust", "ref_id": "rana", "amount": 1}], "rana", "INT_RANA")
Act("a_int_haitham", "interview", "ابدأ مقابلة د. هيثم", al, [{"op": "raise_trust", "ref_id": "haitham", "amount": 1}], "haitham", "INT_HAITHAM")
Act("a_int_yasser", "interview", "ابدأ مقابلة ياسر", he("ev_press_report"), [{"op": "raise_trust", "ref_id": "yasser", "amount": 1}], "yasser", "INT_YASSER")
Act("a_note_rana", "examine", "دوّن إفادة رنا", fu("f_display_mode_changed"), [G("ev_trainee_note")], "rana", "NOTE_RANA")
Act("a_note_yasser", "examine", "دوّن إفادة ياسر", fu("f_no_unit_table"), [G("ev_officer_stmt")], "yasser", "NOTE_YASSER")
Act("a_get_cal", "search_location", "اطلب سجل معايرة الجهاز", fu("f_calibrated"), [G("ev_cal_log")], "loc_records", "GET_CAL")
Act("a_get_calc", "examine", "اطلب ورقة حساب المشرف", fu("f_super_calc"), [G("ev_super_calc")], "haitham", "GET_CALC")
Act("p_press_rana", "present_evidence", "اعرض الخبر على رنا", {"presented": {"evidence_id": "ev_press_report", "to_character": "rana"}}, [{"op": "emit_event", "ref_id": "PRESENTED_PRESS"}], "rana", "P_PRESS_RANA", 0)
Act("p_sheet2_yasser", "present_evidence", "اعرض ورقة القياس الثانية على ياسر", {"presented": {"evidence_id": "ev_sheet2", "to_character": "yasser"}}, [{"op": "emit_event", "ref_id": "PRESENTED_SHEET2"}], "yasser", "P_SHEET2_YASSER", 0)
Act("a_hint", "request_hint", "اطلب تلميحاً", al, [], None, "REQUEST_HINT", 0)
Act("a_accuse", "final_accusation", "قدّم الاستنتاج النهائي", al, [{"op": "emit_event", "ref_id": "SUBMIT"}], None, "FINAL_ACCUSATION", 0)

topics = [
    {"id": "t_sampling", "label_ar": "أخذ العينتين", "example_questions_ar": ["كيف أخذت العينتين؟", "متى أخذت كل عينة؟"], "fact_ids": ["f_sample1_taken", "f_sample2_taken"], "claim_ids": ["cl_rana_same"]},
    {"id": "t_units", "label_ar": "وحدة عرض الجهاز", "example_questions_ar": ["بأي وحدة عرض الجهاز؟", "هل غيّرت إعدادات الجهاز؟"], "fact_ids": ["f_display_mode_changed"]},
    {"id": "t_device", "label_ar": "معايرة الجهاز وحدوده", "example_questions_ar": ["ما هامش خطأ الجهاز؟", "هل حُسبت الأرقام بعد توحيدها؟"], "fact_ids": ["f_device_margin", "f_calibrated", "f_super_calc"]},
    {"id": "t_press", "label_ar": "كتابة الخبر", "example_questions_ar": ["من أين أخذت الرقمين؟", "هل اطلعت على الوحدات؟"], "fact_ids": ["f_officer_read_summary", "f_no_unit_table"], "claim_ids": ["cl_press_big"]},
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
    (1, "الخبر والملخص يعرضان رقمين بلا وحدات؛ ورقة القياس الثانية تبيّن أن الرقم الثاني مكتوب بوحدة غير وحدة الأول.", ["ev_press_report", "ev_summary_sheet", "ev_sheet2"], "i_press_claim"),
    (2, "تحويل الرقم الثاني إلى وحدة الورقة الأولى يرفعه إلى 540، فيختفي الهبوط الظاهر ويحلّ محله ارتفاع.", ["ev_sheet1", "ev_sheet2", "ev_device_sheet"], "i_units_a"),
    (3, "العينتان أُخذتا عند حرارتين مختلفتين، والتوصيلية تتأثر بالحرارة؛ فلا بد من مرجع حراري واحد قبل المقارنة.", ["ev_sheet1", "ev_sheet2"], "i_temp_a"),
    (4, "بعد التوحيد يبقى فارق اسمي صغير، وهامش الجهاز يجعل فترتي الخطأ متداخلتين.", ["ev_device_sheet", "ev_sheet1", "ev_sheet2"], "i_margin_a"),
    (5, "إذن لا يثبت الملف تغيراً جوهرياً، ولا يصح كذلك الجزم بأن لا فرق إطلاقاً.", ["ev_super_calc"], "i_rule_change"),
]
ending = {
    "steps": [{"order": o, "text_ar": t, "uses_evidence_ids": u, "inference_id": i} for o, t, u, i in steps],
    "alternative_paths_ar": ["مسار مستقل: إفادة الباحثة تثبت تبديل نمط العرض، وسجل الظروف يثبت اختلاف الحرارة، وورقة المشرف تعرض الأرقام بعد التوحيد مع الهامش."],
    "what_evidence_could_not_show_ar": ["لا تحدد الأدلة سبب الفارق الاسمي الصغير المتبقي؛ فقد يعود إلى الوقت أو الموضع أو الخطأ العشوائي.", "ثابتا التعويض والهامش تمثيليان في هذه المحاكاة، فأرقامها للتعلم ولا تصلح مرجعاً علمياً دون مراجعة."],
    "science_notes_ar": ["مقارنة رقمين لا تصح قبل التأكد من وحدتيهما ومن ظروف أخذهما.", "تداخل فترتي الخطأ يعني أن الفرق لا يُثبت ولا يُنفى بهذه البيانات، لا أن القراءتين متطابقتان."],
}
core = {
    "schema_version": "0.1.0", "case_id": CID, "case_version": "0.1.0",
    "meta": {"title_ar": "مذكّرة المختبر الناقصة", "title_en": "The Incomplete Lab Note", "age_band": "16-18", "locale": "ar", "dialogue_register": "msa", "estimated_minutes": 30, "difficulty": 3,
             "content_flags": ["no_violence", "science_lab"], "authors": ["فريق أثر التحريري (مسودة بمساعدة الذكاء الاصطناعي، لم تُراجَع بشرياً بعد)"],
             "knowledge_object_refs": ["KO-RS-05-001", "KO-RS-05-005", "KO-RS-05-002", "KO-RS-06-003", "KO-RS-05-010", "KO-RS-06-009"]},
    "premise": {"hook_ar": "خبر يقول إن ماء نافورة المدرسة تغيّر تغيراً هائلاً في يوم واحد، لكن سجلاً في المختبر لا يؤيد ذلك. فأي الرقمين يُصدَّق؟",
                "player_role_ar": "أنت مراجع بيانات في نادي العلوم بالمدرسة، وعليك أن تقرر ماذا يثبت الملف فعلاً قبل أن يصدر المختبر بيانه.",
                "setting_ar": "مختبر مدرسة ثانوية في مدينة متخيَّلة، يوم الثلاثاء. القياسات تمثيلية لأغراض التعلم، وتوقيت المدرسة هو توقيت كل الأوراق.",
                "public_fact_ids": ["f_announce", "f_press_claim"],
                "assumed_general_knowledge_ar": ["البادئتان «ملّي» و«ميكرو» تدلان على أجزاء من الوحدة تختلف بمعامل ثابت", "توصيلية الماء الكهربائية تتغير بتغير حرارته"]},
    "entities": {"characters": chars, "locations": locations, "objects": objects, "organizations": orgs},
    "truth": {"solution": {"culprit_ids": ["yasser"], "summary_ar": "لم يثبت تغير جوهري. الرقمان لا يُقارنان مباشرة لأن لكل منهما وحدة وحرارة مختلفتين، وبعد التوحيد يبقى فارق صغير داخل هامش الجهاز ولا يُجزم بسببه. وجاءت المبالغة من خبر كُتب من ملخص بلا وحدات، دون قصد التضليل.",
                                  "key_fact_ids": ["f_unit_mismatch", "f_temp_differ", "f_within_margin"]},
              "facts": facts, "claims": claims},
    "timeline": timeline, "evidence": ev, "evidence_graph": {"inferences": inf},
    "character_knowledge": ck, "hypotheses": hyps, "misdirection_plan": mis, "learning_objectives": los,
    "mechanics": {"time_budget_units": 30, "actions": A},
    "state_machine": {"id": "c007", "initial": "briefing", "type": "compound", "states": {
        "briefing": {"description_ar": "الإحاطة", "type": "atomic", "on": {"START": {"target": "investigating"}}},
        "investigating": {"description_ar": "التحقيق", "type": "compound", "initial": "gathering",
                          "states": {"gathering": {"type": "atomic", "on": {"OPEN_DEDUCTION": {"target": "deducing"}}}, "deducing": {"type": "atomic", "on": {"BACK": {"target": "gathering"}}}},
                          "on": {"SUBMIT": {"target": "review"}}},
        "review": {"description_ar": "مراجعة", "type": "atomic", "on": {"CLOSE": {"target": "resolved"}}},
        "resolved": {"description_ar": "إغلاق", "type": "final"}}},
    "dialogue": {"max_turns_per_interview": 10, "llm_enabled": False, "topics": topics},
    "rubric": rub, "hint_ladder": hints,
    "fairness_test": {"requirements": {"min_disjoint_proof_paths": 2, "max_inference_depth": 3, "all_red_herrings_refutable": True, "culprit_uniquely_entailed": True, "no_hidden_fact_dependency": True, "max_required_actions": 30}, "runs": []},
    "ending_explanation": ending,
    "expert_review": [{"role": r, "reviewer": "—", "status": "pending", "content_hash": "unbound", "date": "2026-10-27", "notes_ar": "بانتظار مراجعة بشرية؛ لم يُجرَ أي اعتماد."} for r in
                      ["narrative_editor", "scientific_reviewer", "learning_designer", "age_appropriateness", "cultural_reviewer", "legal_rights", "safety"]],
}
ui = {
    "case_id": CID,
    "clock": {"epoch_hhmm": "07:00", "zone_label_ar": "توقيت المدرسة"},
    "cover": {"title_ar": "مذكّرة المختبر الناقصة", "tagline_ar": "رقمان في خبر… وأوراق لم تُقرأ كاملة", "kicker_ar": "الملف السابع · القياس", "glyph": "◈", "accent": "amber"},
    "cold_open_ar": ["الثلاثاء، الحادية عشرة صباحاً.", "خبر يقول إن ماء نافورة المدرسة تغيّر تغيراً هائلاً بين عينتين.", "في ملفك ورقة قياس واحدة وخبر، وسجل ثالث في المختبر لا يؤيد العنوان.", "قبل أن تصدّق الرقمين: ماذا كُتب بجانب كل رقم؟"],
    "labs": [],
    "source_classes": [
        {"id": "primary_record", "label_ar": "سجل أصلي", "help_ar": "يُنتجه الجهاز أو الباحثة لحظة القياس دون وسيط، كورقة قياس أو سجل معايرة."},
        {"id": "redisplay", "label_ar": "نسخة معروضة", "help_ar": "أرقام نُقلت أو أُعيد حسابها من سجلات أخرى."},
        {"id": "claim", "label_ar": "قول أو تصريح", "help_ar": "خبر أو إفادة شخص؛ تُقاس بالسجلات لا بنبرة صاحبها."},
        {"id": "template", "label_ar": "قالب أو نموذج", "help_ar": "نص جاهز لا يصف الحدث الفعلي بذاته."},
        {"id": "public_document", "label_ar": "وثيقة منشورة", "help_ar": "وثيقة معلنة ومعروف ناشرها، كورقة بيانات الجهاز."}],
    "limit_menu": [
        {"id": "l_cause", "label_ar": "الأدلة لا تحدد سبب الفارق الاسمي الصغير المتبقي بين العينتين"},
        {"id": "l_constants", "label_ar": "معامل التعويض وهامش الخطأ قيمتان تمثيليتان، فالاستنتاج مشروط بهما"},
        {"id": "l_two_samples", "label_ar": "عينتان في يوم واحد لا تكفيان لوصف اتجاه عام"},
        {"id": "l_invalid_headline", "label_ar": "قوة عنوان الخبر تدل على صحة استنتاجه"},
        {"id": "l_invalid_overlap", "label_ar": "تداخل فترتي الخطأ يثبت أن العينتين متطابقتان"}],
    "mind_change_menu": [
        {"id": "m_repeat", "label_ar": "ظهور قياسات متكررة بالوحدة والحرارة نفسيهما تُظهر فارقاً أكبر من الهامش"},
        {"id": "m_drift", "label_ar": "ثبوت انحراف في الجهاز بين الجلستين"},
        {"id": "m_republish", "label_ar": "تكرار نشر الخبر في مواقع أخرى"}],
    "skills": [{"skill_id": "KO-RS-05-001", "track": "B"}, {"skill_id": "KO-RS-05-005", "track": "B"}, {"skill_id": "KO-RS-05-002", "track": "D"}, {"skill_id": "KO-RS-06-003", "track": "C"}, {"skill_id": "KO-RS-05-010", "track": "D"}],
    "stage_hooks_ar": {"briefing": "رقمان وعنوان صاخب… فماذا تقول الأوراق نفسها؟", "investigating": "قبل أن تقارن: هل الوحدتان واحدة؟ وهل الظرفان واحد؟", "review": "قبل أن تُغلق الملف: كم تسمح البيانات بأن تجزم؟", "resolved": "أُغلق الملف. في الأرشيف ملف آخر ينتظر."},
    "character_glyphs": {"rana": "ر", "haitham": "هـ", "yasser": "ي"},
}
sc = {
    "case_id": CID,
    "accepted_conclusions": {"h_change": {"grade": 0, "note_ar": "يتجاوز ما تسمح به الأدلة: الفارق الظاهر ناتج عن وحدتين وحرارتين مختلفتين."},
                             "h_units": {"grade": 1, "note_ar": "استنتاج متسق مع الأدلة ويتطلب ذكر حدوده."},
                             "h_none": {"grade": 0, "note_ar": "ينفي كل فرق، والأدلة لا تستبعد فارقاً حقيقياً صغيراً."}},
    "confidence_band": {"h_change": [0, 15], "h_units": [60, 85], "h_none": [0, 10]},
    "source_key": {"ev_sheet1": "primary_record", "ev_sheet2": "primary_record", "ev_conditions": "primary_record", "ev_cal_log": "primary_record",
                   "ev_device_sheet": "public_document", "ev_summary_sheet": "redisplay", "ev_super_calc": "redisplay",
                   "ev_press_report": "claim", "ev_trainee_note": "claim", "ev_officer_stmt": "claim"},
    "link_key": {
        "h_units": {"ev_sheet1": "supports", "ev_sheet2": "supports", "ev_conditions": "supports", "ev_device_sheet": "supports", "ev_trainee_note": "supports", "ev_super_calc": "supports", "ev_cal_log": "neutral"},
        "h_change": {"ev_press_report": "supports", "ev_summary_sheet": "supports", "ev_sheet2": "weakens", "ev_conditions": "weakens", "ev_device_sheet": "weakens", "ev_super_calc": "weakens", "ev_cal_log": "neutral"},
        "h_none": {"ev_cal_log": "supports", "ev_super_calc": "weakens", "ev_device_sheet": "weakens", "ev_press_report": "neutral"},
    },
    "required_limits": ["l_cause", "l_constants"], "valid_mind_changers": ["m_repeat", "m_drift"], "invalid_limits": ["l_invalid_headline", "l_invalid_overlap"],
    "decisive_evidence": ["ev_sheet1", "ev_sheet2", "ev_device_sheet", "ev_conditions", "ev_super_calc"],
    "lab_requirement": None,
    "timeline_requirement": [{"evidence_id": "ev_sheet1", "utc_minute": 30, "tol": 5}, {"evidence_id": "ev_sheet2", "utc_minute": 480, "tol": 5}, {"evidence_id": "ev_super_calc", "utc_minute": 660, "tol": 10}],
    "refuted_hypotheses": ["h_change", "h_none"],
    "criteria_map": {"c_source": "source_typing", "c_conflict": "conflict_resolution", "c_links": "hypothesis_links", "c_uncertainty": "uncertainty", "c_revision": "revision", "c_elimination": "elimination", "c_justification": "justification_human"},
    "caps": {"no_citations_max": 45, "no_conflict_resolution_max": 70},
}
os.makedirs(OUT, exist_ok=True)
for suf, obj in [("", core), (".ui", ui), (".scoring", sc)]:
    with open(os.path.join(OUT, f"{CID}{suf}.json"), "w", encoding="utf8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
print("ok")
