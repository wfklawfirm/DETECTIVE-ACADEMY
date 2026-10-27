#!/usr/bin/env python3
# Case c005 «الصندوق ذو الرقمين» — data quality and entity types: the same number can name a container or an item.
# Teaches: a repeated value is not a duplicate entity; read what a column MEANS before matching rows; two documents that
# differ in field naming are not a forgery. No-culprit convention: the receiving clerk who merged the two fields into one column
# (an honest mistake) is recorded in culprit_ids. Usage: gen_c005.py OUT_DIR
# Calendar (fictional): minute 0 = day 0, 00:00 = 3 November (heirs' packing list). Receipt 5 Nov (day 2), data file 6 Nov, reviewer note 9 Nov.
import json, sys, os
OUT = sys.argv[1]
CID = "c005_double_number_box"

def dm(d, h=0, m=0): return d * 1440 + h * 60 + m
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

# ---------------------------------------------------------------- characters
ch("salim", "سليم البزري", "witness", "أمين المقتنيات، في الخمسينات",
   "متأنٍّ يحب النظام، يشرح تصميم الأرقام كمن صمّمه، ويتحفظ على أي نتيجة لم يحصل عليها بنفسه.",
   ["أن تبقى منظومة الترقيم سليمة", "ألا يُنسب إلى المتحف تزوير دون دليل"],
   [L("sl_greet", "greeting", "أهلاً. أعرف كيف صُمّم الترقيم عندنا، ولا أدّعي معرفة ما لم أفحصه."),
    L("sl_design", "reveal", "نعطي الصندوق رقماً يبدأ بحرف M، ونعطي كل قطعة رقماً يبدأ بحرف A. وقد يضم الصندوق الواحد أكثر من قطعة.", ["f_numbering_design"]),
    L("sl_donor", "reveal", "ملف الإهداء عندي، وفيه جرد كتبته المتبرعة نفسها قبل أن نرقّم شيئاً.", ["f_donor_file"]),
    L("sl_notest", "reveal", "لم يصلني أي فحص تقني للمعدن أو العمر. ما عندي سجلات، ولا شيء غيرها.", ["f_no_test"]),
    L("sl_unknown", "deflect_unknown", "لا أعرف ذلك، ولن أخمّن."),
    L("sl_off", "deflect_offtopic", "اسألني عن الترقيم وملف الإهداء."),
    L("sl_bye", "farewell", "اقرأ الوثائق بتأنٍّ، ففي الأرقام فخاخ.")])

ch("nuha", "نهى العطار", "suspect", "موظفة استلام في المتحف، في أواخر الثلاثينات",
   "سريعة ومنشغلة بالمواعيد، تعمل بحسب النماذج وتخشى أن يُنسب إليها خطأ في الجداول.",
   ["ألا تُلام على جدول جُمع على عجل", "أن تبقى إجراءات الاستلام مفهومة"],
   [L("nh_greet", "greeting", "أنا من تستلم الشحنات وتملأ نماذج الاستلام. اسألني عمّا فعلته."),
    L("nh_pack", "reveal", "كانت مع الشحنة قائمة تعبئة من الورثة، وقد أرفقتها بالملف.", ["f_packing_attached"]),
    L("nh_cond", "reveal", "فحصت الصينيتين بالعين عند الاستلام وملأت نموذج الحالة لكل قطعة على حدة.", ["f_condition_sheet"]),
    L("nh_compiled", "reveal", "جمعت صفّي الجدول من سجل الوارد وبطاقة المتحف في ملف واحد لجرد نهاية الأسبوع.", ["f_clerk_compiled"]),
    L("nh_claim", "reveal", "حسب فهمي كان عمود «الرقم» هو رقم القطعة.", None, ["cl_clerk_column"]),
    L("nh_check", "refuse_secret", "دعني أنظر إلى الملف أمامي قبل أن أحدد من أين نقلت القيمة."),
    L("nh_admit", "reveal", "نقلت القيمة 24 من الملصق المثبت على الصندوق، أي رقم الصندوق. لم أنتبه إلى أن العمود لا يقول ذلك.", ["f_column_from_box"]),
    L("nh_unknown", "deflect_unknown", "لا أذكر ذلك."),
    L("nh_off", "deflect_offtopic", "اسألني عن الاستلام والنماذج."),
    L("nh_bye", "farewell", "سأضيف تسمية واضحة للعمود في المرة القادمة.")])

ch("walid", "وليد الرفاعي", "witness", "مراجع جودة بيانات خارجي، في الأربعينات",
   "ودود لكنه يميل إلى الجزم بسرعة حين يرى نمطاً متكرراً، ويعتمد على ما يصله من لقطات الشاشة.",
   ["أن يُحترم تنبيهه كمراجع", "ألا يُتّهم بنشر اتهام بلا أساس"],
   [L("wl_greet", "greeting", "أنا مراجع بيانات من خارج المتحف. أراجع ما يُرسل إليّ."),
    L("wl_image", "reveal", "لم يصلني إلا صورة للجدول. لم أرَ سجل الوارد ولا بطاقة المتحف.", ["f_reviewer_saw_image"]),
    L("wl_claim", "reveal", "رأيت الرقم نفسه في صفين لصينيتين متشابهتين، فخمّنت أن إحداهما نسخة مزورة.", None, ["cl_reviewer_dup"]),
    L("wl_unknown", "deflect_unknown", "لا أملك غير ما رأيته في الصورة."),
    L("wl_off", "deflect_offtopic", "فلنعد إلى الجدول الذي رأيته."),
    L("wl_bye", "farewell", "سأعيد النظر إن وصلتني سجلات أخرى.")])

locations = [{"id": "loc_receiving", "name_ar": "قاعة الاستلام", "description_ar": "حيث تُفتح الشحنات وتُفحص قطعها."},
             {"id": "loc_office", "name_ar": "مكتب الجرد", "description_ar": "حيث تُجمع الجداول والملفات."},
             {"id": "loc_store", "name_ar": "مخزن المتحف", "description_ar": "حيث يُحفظ الصندوق وقطعه."}]
objects = [{"id": "obj_box", "name_ar": "الصندوق M-24", "description_ar": "صندوق الشحنة الذي ضم الصينيتين."},
           {"id": "obj_tray19", "name_ar": "القطعة A-19", "description_ar": "صينية نحاسية مستديرة."},
           {"id": "obj_tray20", "name_ar": "القطعة A-20", "description_ar": "صينية نحاسية مستديرة."},
           {"id": "obj_datafile", "name_ar": "ملف جمع بيانات الجرد", "description_ar": "جدول مُصدَّر من وثيقتين."}]
orgs = [{"id": "org_museum", "name_ar": "متحف الحِرَف", "description_ar": "متحف محلي تلقّى إهداء من ورثة متبرعة."},
        {"id": "org_heirs", "name_ar": "ورثة المتبرعة", "description_ar": "الجهة التي أرسلت الشحنة."}]

# ---------------------------------------------------------------- truth
facts = []
def F(id, st, kind, subj, spoiler, time=None, loc=None, ko=None):
    d = {"id": id, "statement_ar": st, "kind": kind, "subject_ids": subj, "spoiler_level": spoiler}
    if time: d["time"] = time
    if loc: d["location_id"] = loc
    if ko: d["science_ko_refs"] = ko
    facts.append(d)
F("f_two_rows_same_number", "في جدول جرد المتحف صفّان لصينيتين نحاسيتين متشابهتين تحمل خانة «الرقم» فيهما القيمة نفسها.", "attribute", ["obj_datafile", "obj_tray19", "obj_tray20"], 0, T(dm(3, 9, 30), "approx"))
F("f_forgery_alleged", "قال مراجع خارجي إن تكرار الرقم يدل على أن إحدى القطعتين نسخة مزورة.", "attribute", ["walid", "org_museum"], 0, T(dm(6, 9), "approx"))
F("f_numbering_design", "يعطي المتحف الحاوية رقماً بحرف M والقطعة رقماً بحرف A، ويجوز أن تضم الحاوية الواحدة أكثر من قطعة.", "attribute", ["salim", "org_museum"], 1)
F("f_donor_file", "يضم ملف الإهداء جرداً كتبته المتبرعة قبل ترقيم المتحف.", "state", ["salim", "org_heirs"], 1)
F("f_no_test", "لم يُجرَ أي فحص تقني للمعدن أو العمر على القطعتين.", "absence", ["salim", "obj_tray19", "obj_tray20"], 0)
F("f_packing_attached", "أرفقت موظفة الاستلام بالشحنة قائمة تعبئة أرسلها الورثة.", "state", ["nuha", "org_heirs"], 1, T(dm(2, 10, 15)), "loc_receiving")
F("f_condition_sheet", "فحصت موظفة الاستلام القطعتين بالعين وملأت نموذج حالة لكل قطعة.", "event", ["nuha", "obj_tray19", "obj_tray20"], 1, T(dm(2, 10, 40)), "loc_receiving")
F("f_clerk_compiled", "جمعت موظفة الاستلام صفّي الجدول من سجل الوارد وبطاقة المتحف في ملف واحد.", "event", ["nuha", "obj_datafile"], 1, T(dm(3, 9, 30)), "loc_office")
F("f_column_from_box", "نقلت الموظفة قيمة عمود «الرقم» من ملصق الصندوق، أي رقم الحاوية، دون أن تسمّي العمود.", "event", ["nuha", "obj_datafile", "obj_box"], 2, T(dm(3, 9, 30)), "loc_office")
F("f_reviewer_saw_image", "لم يطّلع المراجع الخارجي إلا على صورة للجدول.", "state", ["walid", "obj_datafile"], 1, T(dm(5, 16)))
F("f_ledger_line", "سجل الوارد يسجّل أن الحاوية M-24 تضم القطعة A-19.", "attribute", ["obj_box", "obj_tray19"], 1, T(dm(2, 10, 15)), "loc_receiving")
F("f_card_line", "بطاقة المتحف تسجّل أن الحاوية M-24 تضم القطعة A-20.", "attribute", ["obj_box", "obj_tray20"], 1, T(dm(2, 14)), "loc_office")
F("f_independent_pair", "جرد المتبرعة، المؤرخ قبل ترقيم المتحف، يذكر زوجاً من الصواني في إحداهما إصلاح قديم في الحافة.", "relation", ["org_heirs", "obj_tray19", "obj_tray20"], 2, None, None, ["KO-FC-04-026", "KO-RS-05-004"])
F("f_column_is_box", "القيمة المتكررة في عمود «الرقم» تطابق رقم الحاوية في السجلين، لا رقمي القطعتين 19 و20.", "relation", ["obj_datafile", "obj_box"], 2, None, "loc_office", ["KO-RS-06-004"])
F("f_pair_in_one_box", "القطعتان A-19 وA-20 قطعتان مختلفتان وصلتا معاً في الحاوية M-24 نفسها، وليستا قطعة واحدة مكررة.", "relation", ["obj_box", "obj_tray19", "obj_tray20"], 3, T(dm(2, 10, 15), "exact", dm(2, 14)), "loc_receiving", ["KO-RS-06-004", "KO-RS-05-004"])

claims = [
    {"id": "cl_reviewer_dup", "statement_ar": "الرقم نفسه ظهر في قطعتين، فإحداهما نسخة مزورة.", "kind": "honest_mistake", "held_by": ["walid"], "true_fact_id": "f_column_is_box", "contradicted_by_evidence_ids": ["ev_policy", "ev_condition"]},
    {"id": "cl_clerk_column", "statement_ar": "عمود «الرقم» في الجدول هو رقم القطعة.", "kind": "honest_mistake", "held_by": ["nuha"], "true_fact_id": "f_column_is_box", "contradicted_by_evidence_ids": ["ev_ledger", "ev_card", "ev_policy"]},
]
timeline = [
    {"id": "te_pack", "description_ar": "الورثة يعدّون قائمة التعبئة ويغلقون الصندوق.", "time": T(dm(0, 11)), "fact_ids": ["f_independent_pair"], "actor_ids": []},
    {"id": "te_receive", "description_ar": "استلام الشحنة وتسجيل بند القطعة A-19 في سجل الوارد.", "time": T(dm(2, 10, 15)), "location_id": "loc_receiving", "actor_ids": ["nuha"], "fact_ids": ["f_ledger_line", "f_packing_attached"], "motivated_by_ar": "إجراء الاستلام المعتاد عند وصول الشحنات"},
    {"id": "te_condition", "description_ar": "فحص القطعتين بالعين وملء نموذج حالة لكل قطعة.", "time": T(dm(2, 10, 40)), "location_id": "loc_receiving", "actor_ids": ["nuha"], "fact_ids": ["f_condition_sheet", "f_pair_in_one_box"], "motivated_by_ar": "توثيق الحالة قبل التخزين"},
    {"id": "te_card", "description_ar": "كتابة بطاقة المتحف للقطعة A-20.", "time": T(dm(2, 14)), "location_id": "loc_office", "actor_ids": ["salim"], "fact_ids": ["f_card_line"], "motivated_by_ar": "إكمال بطاقة كل قطعة جديدة"},
    {"id": "te_compile", "description_ar": "جمع الصفين في ملف واحد ونقل القيمة 24 إلى عمود «الرقم».", "time": T(dm(3, 9, 30)), "location_id": "loc_office", "actor_ids": ["nuha"], "fact_ids": ["f_clerk_compiled", "f_column_from_box", "f_two_rows_same_number"], "motivated_by_ar": "تجهيز جرد نهاية الأسبوع"},
    {"id": "te_review", "description_ar": "وصول صورة الجدول إلى المراجع الخارجي.", "time": T(dm(5, 16)), "actor_ids": ["walid"], "fact_ids": ["f_reviewer_saw_image"], "motivated_by_ar": "مراجعة جودة بيانات الجرد"},
    {"id": "te_allege", "description_ar": "المراجع يدوّن أن الرقم المتكرر يرجّح نسخة مزورة.", "time": T(dm(6, 9), "approx"), "actor_ids": ["walid"], "fact_ids": ["f_forgery_alleged"], "motivated_by_ar": "الظن بأن التكرار يعني قطعة منسوخة"},
]

# ---------------------------------------------------------------- evidence
ev = []
def V(id, title, kind, content, acts, supports, rel, limits, contradicts=None, red=False, ko=None, loc=None):
    d = {"id": id, "title_ar": title, "kind": kind, "content_ar": content, "acquired_by_action_ids": acts, "supports_fact_ids": supports, "reliability": rel, "limits_ar": limits}
    if contradicts: d["contradicts_claim_ids"] = contradicts
    if red: d["is_red_herring"] = True
    if ko: d["forensic_ko_ref"] = ko
    if loc: d["location_id"] = loc
    ev.append(d)
V("ev_ledger", "سجل الوارد (صفحة الاستلام)", "documentary",
  "سجل الوارد — متحف الحِرَف\nتاريخ الاستلام: 5 تشرين الثاني، 10:15\nالمورِّد: ورثة المتبرعة (شحنة واحدة)\nرقم الحاوية: M-24\nالبند المسجَّل: القطعة A-19 — صينية نحاسية مستديرة\nسلسلة العهدة: الورثة ← شركة النقل ← موظفة الاستلام ← مخزن المتحف",
  ["a_open_ledger"], ["f_ledger_line"], "strong",
  "يسجّل ما استلمه المتحف عن القطعة A-19 ولا يصف بقية محتويات الحاوية؛ وسلسلة العهدة فيه تخص هذه الشحنة وحدها.", ko="KO-FC-04-026", loc="loc_receiving")
V("ev_card", "بطاقة المتحف", "documentary",
  "بطاقة قطعة — متحف الحِرَف\nرقم الحاوية: M-24\nرقم القطعة: A-20\nالوصف: صينية نحاسية مستديرة\nتاريخ الكتابة: 5 تشرين الثاني، 14:00\nكتبها: أمين المقتنيات",
  ["a_open_card"], ["f_card_line"], "strong",
  "تسجّل القطعة A-20 وحاويتها، ولا تقول شيئاً عن القطعة A-19 ولا عن أنهما متكرّرتان أو متمايزتان.", loc="loc_office")
V("ev_datafile", "ملف جمع بيانات الجرد", "digital",
  "جدول مُصدَّر لجرد نهاية الأسبوع:\nالأعمدة: الرقم | الوصف | المصدر\nالصف 1: 24 | صينية نحاسية مستديرة | سجل الوارد\nالصف 2: 24 | صينية نحاسية مستديرة | بطاقة المتحف\nملاحظة: لا يوجد تعريف لنوع القيمة في عمود «الرقم».",
  ["a_open_datafile"], ["f_two_rows_same_number"], "weak",
  "مستند مشتق جُمع من وثيقتين، ولا يعرّف عمود «الرقم»، فلا يصلح وحده دليلاً على أن القيمتين لقطعتين متطابقتين.", ko="KO-RS-06-004", loc="loc_office")
V("ev_policy", "سياسة ترقيم المقتنيات", "documentary",
  "سياسة الترقيم — متحف الحِرَف:\n1. رقم الحاوية يبدأ بالحرف M ويُلصق على الصندوق عند الاستلام، ويتكرر لكل ما يضمه الصندوق.\n2. رقم القطعة يبدأ بالحرف A ويُمنح لكل قطعة على حدة، ولا يتكرر.\n3. قد يضم الصندوق الواحد أكثر من قطعة.\n4. يُسجَّل في سجل الوارد وفي بطاقة المتحف بند واحد لكل قطعة.",
  ["a_get_policy"], ["f_numbering_design"], "strong",
  "تصف القاعدة المعلنة لا ما جرى لقطعة بعينها، وتفترض أن العاملين اتبعوها.", loc="loc_office")
V("ev_reviewer_note", "ملاحظة المراجع الخارجي", "digital",
  "ملاحظة مراجع خارجي كُتبت من صورة للجدول:\n«الرقم 24 تكرر في صفين لصينيتين متشابهتين. إذا كان هذا الرقم هو رقم الصندوق فالرقمان متطابقان، وهذا يرجّح وجود نسخة مزورة بالرقم نفسه.»",
  ["a_open_note"], ["f_forgery_alleged"], "weak",
  "استنتاج مبني على صورة جدول لا على السجلات الأصلية، ويفترض أن التطابق في رقم يعني تطابقاً في القطعة.", red=True, loc="loc_office")
V("ev_packing", "قائمة تعبئة الورثة", "documentary",
  "قائمة تعبئة الورثة (مرفقة بالشحنة):\nالتاريخ: 3 تشرين الثاني\nعدد الصناديق: صندوق واحد\nالمحتويات: صينيتان نحاسيتان مستديرتان من زوج واحد، ملفوفة كل منهما على حدة\nملاحظة الورثة: في إحداهما إصلاح قديم في الحافة، وفي الأخرى شرخ شعري في القاعدة.",
  ["a_get_packing"], ["f_packing_attached"], "moderate",
  "وثيقة طرف خارجي تصف الشحنة قبل ترقيم المتحف ولا تذكر أرقامه، وتعتمد على دقة جرد الورثة.", ko="KO-RS-05-004", loc="loc_receiving")
V("ev_condition", "نموذج فحص الحالة عند الاستلام", "documentary",
  "نموذج فحص الحالة عند الاستلام — 5 تشرين الثاني، 10:40\nالحاوية: M-24\nالقطعة A-19: صينية نحاسية مستديرة؛ الحافة مصلَّحة بطول ثلاثة سنتيمترات تقريباً؛ لا شرخ في القاعدة.\nالقطعة A-20: صينية نحاسية مستديرة؛ الحافة سليمة؛ شرخ شعري في القاعدة.\nأعدّته: موظفة الاستلام",
  ["a_get_condition"], ["f_condition_sheet"], "strong",
  "يصف حالة ظاهرة بالعين، وليس فحصاً فنياً لعمر المعدن أو مصدره.", loc="loc_receiving")
V("ev_donor", "سند الإهداء وجرد المتبرعة", "documentary",
  "سند الإهداء وجرد المتبرعة (مؤرَّخ 2019، قبل ترقيم المتحف):\n«صينيتان نحاسيتان من زوج واحد؛ في إحداهما إصلاح قديم في الحافة.»\nالتوقيع: المتبرعة",
  ["a_get_donor"], ["f_donor_file"], "moderate",
  "وثيقة مستقلة عن المتحف تؤيد وجود زوج، لكنها وصف نصي لا يغني عن فحص فني.", ko="KO-RS-05-004", loc="loc_office")
V("ev_curator_stmt", "إفادة سليم البزري (ملخص)", "testimonial",
  "ملخص إفادة سليم البزري، أمين المقتنيات:\n«الترقيم عندنا نوعان: للحاوية وللقطعة. ولم يصلني أي فحص تقني للمعدن أو العمر.»",
  ["a_note_curator"], ["f_no_test"], "moderate",
  "إفادة من صمّم المنظومة؛ تبيّن القاعدة ولا تثبت ما جرى في هذه الشحنة.", loc="loc_office")
V("ev_clerk_stmt", "إفادة نهى العطار (ملخص)", "testimonial",
  "ملخص إفادة نهى العطار، موظفة الاستلام:\n«جمعت صفّي الجدول من الوثيقتين الأصليتين في ملف واحد، وفهمت أن عمود الرقم هو رقم القطعة.»",
  ["a_note_clerk"], ["f_clerk_compiled"], "weak",
  "إفادة صاحبة الجدول عن فهمها هي، وتُقاس بالسجلين والسياسة.", loc="loc_office")
V("ev_reviewer_stmt", "إفادة وليد الرفاعي (ملخص)", "testimonial",
  "ملخص إفادة وليد الرفاعي، المراجع الخارجي:\n«لم أرَ إلا صورة الجدول. رأيت الرقم نفسه في صفين فخمّنت وجود نسخة.»",
  ["a_note_reviewer"], ["f_reviewer_saw_image"], "weak",
  "تخمين مبني على صورة جدول؛ يصف ما رآه المراجع لا ما تقوله السجلات.", loc="loc_office")

def P(t, i): return {"ref_type": t, "ref_id": i}
inf = []
def I(id, prem, ct, concl, rel, strength, rule, ks):
    inf.append({"id": id, "premises": prem, "conclusion": {"ref_type": ct, "ref_id": concl}, "relation": rel, "strength": strength, "rule_ar": rule, "skill_ko_refs": ks})
KF = "f_pair_in_one_box"
I("i_path_a", [P("evidence", "ev_ledger"), P("evidence", "ev_card"), P("evidence", "ev_policy")], "fact", KF, "establishes", "strong",
  "السجلان يذكران الحاوية نفسها M-24 برقمي قطعة مختلفين، والسياسة تقول إن رقم الحاوية يتكرر ورقم القطعة لا يتكرر وإن الحاوية قد تضم أكثر من قطعة؛ فهما بندان لقطعتين لا بندان لقطعة.", ["KO-RS-06-004", "KO-RS-05-004"])
I("i_path_b", [P("evidence", "ev_packing"), P("evidence", "ev_condition")], "fact", KF, "establishes", "strong",
  "قائمة الورثة تذكر صينيتين في صندوق واحد بعلامتين مختلفتين، ونموذج الاستلام يسجّل لكل رقم قطعة العلامة التي تخصه داخل الحاوية؛ فالجسمان مختلفان.", ["KO-RS-05-004", "KO-RS-06-001"])
I("i_column", [P("evidence", "ev_datafile"), P("fact", KF)], "fact", "f_column_is_box", "establishes", "strong",
  "القيمة 24 تطابق رقم الحاوية في السجلين، أما رقما القطعتين فهما 19 و20؛ فالعمود الذي لا تعريف له يحمل رقم الحاوية.", ["KO-RS-06-004"])
I("i_provenance", [P("evidence", "ev_donor"), P("evidence", "ev_condition")], "fact", "f_independent_pair", "establishes", "suggestive",
  "وثيقة كُتبت قبل أي ترقيم تذكر زوجاً بإصلاح قديم في إحدى الحافتين، ونموذج الاستلام يسجّل الإصلاح نفسه في إحدى القطعتين؛ فالتوافق يأتي من مصدرين مستقلين عن الترقيم.", ["KO-RS-05-004"])
I("i_support_confusion", [P("fact", KF)], "hypothesis", "h_confusion", "supports", "strong",
  "إذا كانت القطعتان مختلفتين في حاوية واحدة فأي رقم مكرر بينهما هو رقم الحاوية، ويكون التعارض من تسمية الحقول لا من القطع.", ["KO-RS-05-002"])
I("i_rule_fake", [P("fact", KF)], "hypothesis", "h_fake", "rules_out", "strong",
  "الاتهام قام على تكرار رقم قطعة؛ فإذا كان المتكرر رقم الحاوية وكانت القطعتان مختلفتين سقط ما يدعو إلى افتراض نسخة.", ["KO-RS-06-001"])
I("i_rule_swap", [P("fact", KF)], "hypothesis", "h_swap", "rules_out", "strong",
  "السجلان لا يتعارضان إذا ضمّت الحاوية قطعتين، فلا حاجة إلى استبدال لتفسير اختلاف رقمي القطعتين.", ["KO-RS-06-008"])
I("i_rule_typo", [P("fact", KF)], "hypothesis", "h_typo", "rules_out", "strong",
  "حين يصف كل سجل قطعة موجودة فعلاً، لا يعود أي منهما خطأ كتابياً يحتاج إلى تصحيح.", ["KO-RS-06-008"])
I("i_claim_reviewer", [P("fact", "f_column_is_box")], "claim", "cl_reviewer_dup", "contradicts_claim", "strong",
  "التطابق الذي رآه المراجع هو تطابق رقم الحاوية، وهو متوقع أن يتكرر لقطع الحاوية الواحدة.", ["KO-RS-05-014"])
I("i_claim_clerk", [P("fact", "f_column_is_box")], "claim", "cl_clerk_column", "contradicts_claim", "strong",
  "ما في العمود هو رقم الحاوية لا رقم القطعة، فالفهم الأول للعمود لا يطابق السجلين.", ["KO-RS-05-014"])

ck = [
    {"character_id": "salim", "knows": [{"fact_id": "f_numbering_design", "access": "professional", "certainty": "certain"},
                                        {"fact_id": "f_donor_file", "access": "professional", "certainty": "certain"},
                                        {"fact_id": "f_no_test", "access": "professional", "certainty": "certain"}], "hides": [], "believes": []},
    {"character_id": "nuha", "knows": [{"fact_id": "f_packing_attached", "access": "witnessed", "certainty": "certain"},
                                       {"fact_id": "f_condition_sheet", "access": "witnessed", "certainty": "certain"},
                                       {"fact_id": "f_clerk_compiled", "access": "witnessed", "certainty": "certain"}],
     "hides": [{"fact_id": "f_column_from_box", "reveal_when": {"presented": {"evidence_id": "ev_datafile", "to_character": "nuha"}}, "cover_claim_id": None, "reveal_line_id": "nh_admit"}],
     "believes": [{"claim_id": "cl_clerk_column", "stance": "sincere"}]},
    {"character_id": "walid", "knows": [{"fact_id": "f_reviewer_saw_image", "access": "witnessed", "certainty": "certain"}], "hides": [],
     "believes": [{"claim_id": "cl_reviewer_dup", "stance": "sincere"}]},
]
hyps = [
    {"id": "h_fake", "statement_ar": "إحدى القطعتين نسخة مزورة من الأخرى، فهما تحملان الرقم نفسه.", "is_true": False, "plausibility_at_start": "high"},
    {"id": "h_confusion", "statement_ar": "الرقم المتكرر هو رقم الصندوق لا رقم القطعة، والقطعتان مختلفتان؛ والتعارض ناتج من اختلاط الحقول.", "is_true": True, "plausibility_at_start": "medium", "suspect_id": "nuha"},
    {"id": "h_swap", "statement_ar": "حدث استبدال لإحدى القطعتين داخل المتحف بعد الاستلام.", "is_true": False, "plausibility_at_start": "medium"},
    {"id": "h_typo", "statement_ar": "أحد السجلين يحمل رقم قطعة خاطئاً بسبب خطأ كتابي.", "is_true": False, "plausibility_at_start": "low"},
]
mis = [
    {"id": "rh_dup", "points_to_hypothesis_id": "h_fake", "planted_via_ar": "الجدول يُظهر القيمة 24 في صفين بوصف متطابق، فيبدو كأن لقطعتين الرقم نفسه.", "evidence_ids": ["ev_datafile"],
     "refuted_by_inference_ids": ["i_column", "i_rule_fake"],
     "fairness_note_ar": "السجلان الأصليان يذكران 24 رقماً للحاوية، ويذكران 19 و20 للقطعتين؛ والجدول المشتق لا يسمّي العمود."},
    {"id": "rh_conflict", "points_to_hypothesis_id": "h_swap", "planted_via_ar": "سجل الوارد يذكر القطعة A-19 وبطاقة المتحف تذكر القطعة A-20 للحاوية نفسها، فيبدو كأن إحداهما حلّت محل الأخرى.", "evidence_ids": ["ev_ledger", "ev_card"],
     "refuted_by_inference_ids": ["i_path_a", "i_rule_swap"],
     "fairness_note_ar": "سياسة الترقيم تجيز أن تضم الحاوية قطعتين وتسجّل لكل قطعة بنداً، ونموذج الحالة يصف القطعتين معاً عند الاستلام."},
    {"id": "rh_review", "points_to_hypothesis_id": "h_fake", "planted_via_ar": "مراجع خارجي يقول إن الرقمين متطابقان وإن هذا يرجّح نسخة مزورة.", "evidence_ids": ["ev_reviewer_note"],
     "refuted_by_inference_ids": ["i_claim_reviewer", "i_rule_fake"],
     "fairness_note_ar": "المراجع لم يطّلع إلا على صورة الجدول، ومقدمته الشرطية (إن كان الرقم رقم الصندوق) هي نفسها ما يفسّر التطابق دون تزوير."},
]
los = [
    {"id": "lo_source", "statement_ar": "يفرّق بين السجل الأصلي والجدول المشتق والتخمين، ويسأل ماذا يعني كل حقل.", "skill_ko_ref": "KO-RS-05-001", "observable_behaviors_ar": ["يصنّف الجدول المشتق نسخة معروضة", "يصنّف الملاحظة والإفادات أقوالاً"], "evidence_sources": ["evidence_board"]},
    {"id": "lo_hyp", "statement_ar": "يوازن بين فرضيات متنافسة ويستبعد ما تنقضه الأدلة.", "skill_ko_ref": "KO-RS-05-002", "observable_behaviors_ar": ["يضيف أكثر من فرضية", "يستبعد فرضية بدليل مرفق"], "evidence_sources": ["hypothesis_ledger"]},
    {"id": "lo_diag", "statement_ar": "يفرّق بين تطابق قيمة وتطابق كيان، ويقدّر ما يثبته كل دليل.", "skill_ko_ref": "KO-RS-06-001", "observable_behaviors_ar": ["يربط الدليل بالفرضية باتجاه صحيح", "لا يعامل تكرار القيمة تكراراً للكيان"], "evidence_sources": ["evidence_board", "final_justification"]},
    {"id": "lo_calib", "statement_ar": "يصوغ ثقته بحدودها ويحدد ما قد يغيّر رأيه.", "skill_ko_ref": "KO-RS-06-021", "observable_behaviors_ar": ["يختار ثقة معقولة", "يذكر حدوداً", "يحدد دليلاً مغيّراً للرأي"], "evidence_sources": ["final_justification"]},
    {"id": "lo_revise", "statement_ar": "يراجع رأيه الأول حين يظهر دليل أفضل.", "skill_ko_ref": "KO-RS-06-009", "observable_behaviors_ar": ["يغيّر فرضيته الرائدة بدليل"], "evidence_sources": ["hypothesis_ledger", "action_log"]},
]
def levels(d): return [{"score": i, "descriptor_ar": t} for i, t in enumerate(d)]
rub = {
    "reference_answer_ar": "الرقم الذي ظنه المراجع علامة على نسخة مزورة هو رقم الحاوية M-24، لا رقم قطعة. القطعتان A-19 وA-20 مختلفتان وصلتا في صندوق واحد. ويثبت ذلك مساران مستقلان: سجل الوارد وبطاقة المتحف مع سياسة الترقيم، ثم قائمة تعبئة الورثة مع نموذج فحص الاستلام الذي يسجّل علامة حالة مختلفة لكل قطعة. أما عمود «الرقم» في الجدول المشتق فنُقل إليه رقم الحاوية من غير تسمية. حدود الاستنتاج: لم يُجرَ فحص تقني للمعدن، ووثائق الورثة لا تُثبت العمر، ولا دليل على سوء نية في الجدول.",
    "criteria": [
        {"id": "c_source", "name_ar": "تمييز الادعاء من المستند الأصلي", "objective_ids": ["lo_source"], "scored_by": "deterministic", "weight": 0.2, "levels": levels(["لم يصنّف", "أخطأ في الأغلب", "نصف صحيح", "معظمه صحيح", "كله صحيح"])},
        {"id": "c_links", "name_ar": "ربط الأدلة بفرضيتين فأكثر", "objective_ids": ["lo_diag"], "scored_by": "deterministic", "weight": 0.2, "levels": levels(["لا روابط", "قليلة", "نصفها صحيح", "معظمها", "كلها دقيقة"])},
        {"id": "c_elimination", "name_ar": "تفسير التعارض واستبعاد الفرضيات الخاطئة", "objective_ids": ["lo_hyp"], "scored_by": "deterministic", "weight": 0.1, "levels": levels(["لم يستبعد", "استبعد خطأً", "فرضية بدليل", "فرضيتين", "كل الخاطئة"])},
        {"id": "c_uncertainty", "name_ar": "درجة عدم اليقين والمعلومات الناقصة", "objective_ids": ["lo_calib"], "scored_by": "deterministic", "weight": 0.15, "levels": levels(["ثقة مفرطة", "حدود قليلة", "جزئية", "معقولة", "معايَرة كاملة"])},
        {"id": "c_revision", "name_ar": "تعديل الرأي عند ظهور دليل أفضل", "objective_ids": ["lo_revise"], "scored_by": "deterministic", "weight": 0.1, "levels": levels(["بقي على فرضية مرفوضة", "لم يعلن فرضية", "ثبت على فرضية سليمة", "غيّر بدليل", "غيّر بدليل ووثّق"])},
        {"id": "c_justification", "name_ar": "جودة الحجة المكتوبة", "objective_ids": ["lo_diag", "lo_hyp"], "scored_by": "human", "weight": 0.25, "levels": levels(["لا حجة", "ادعاء بلا سند", "أدلة دون ربط", "ربط الأدلة بالاستنتاج", "ربط مع البدائل والحدود"])},
    ],
}
def H(id, lv, kind, text, trig, target=None, w=0.0):
    d = {"id": id, "level": lv, "kind": kind, "text_ar": text, "trigger": trig, "assessment_weight": w}
    if target: d["targets_inference_id"] = target
    return d
he = lambda e: {"has_evidence": e}
hints = [
    H("hg1", 1, "metacognitive", "أين ينتهي ما شاهده الشخص وتبدأ طريقته في تفسيره؟", {"always": True}, None, 0.02),
    H("hg2", 2, "focus_area", "ضع كل معلومة في جدول: مصدر أصلي أم نسخة أم تعليق؟ وماذا يسمّي كل مصدر الرقم الذي يذكره؟", he("ev_datafile"), None, 0.04),
    H("hg3", 3, "pointer", "راجع تحديداً الدليل الذي يوضح معنى الرقم في كل وثيقة: هل هو للحاوية أم للقطعة؟", he("ev_datafile"), None, 0.06),
    H("ha1", 1, "metacognitive", "ما الفرق بين رقم يدل على الصندوق ورقم يدل على ما بداخله؟", he("ev_ledger"), "i_path_a", 0.02),
    H("ha2", 2, "pointer", "اسأل من صمّم الترقيم عن القاعدة المكتوبة، ثم قارن بها البندين المسجَّلين في الوارد وفي البطاقة.", he("ev_card"), "i_path_a", 0.06),
    H("ha3", 3, "partial_reveal", "في السجلين حقلان بدل حقل واحد: انظر أيهما يتكرر وأيهما يختلف.", he("ev_card"), "i_path_a", 0.1),
    H("hb1", 1, "metacognitive", "هل توجد وثيقة تصف الشحنة قبل أن يعطيها المتحف أي رقم؟", he("ev_datafile"), "i_path_b", 0.02),
    H("hb2", 2, "pointer", "اسأل موظفة الاستلام عمّا أُرفق بالشحنة وعمّا دوّنته عن كل قطعة عند فتح الصندوق.", he("ev_datafile"), "i_path_b", 0.06),
    H("hb3", 3, "partial_reveal", "قارن حالة كل قطعة كما سجلها نموذج الاستلام بما وصفه الورثة.", he("ev_packing"), "i_path_b", 0.1),
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
Act("a_open_ledger", "examine", "افتح صفحة الاستلام في سجل الوارد", al, [G("ev_ledger")], "loc_receiving", "OPEN_LEDGER")
Act("a_open_note", "examine", "اقرأ ملاحظة المراجع الخارجي", al, [G("ev_reviewer_note")], "walid", "OPEN_NOTE")
Act("a_open_card", "examine", "اطلب بطاقة المتحف للصندوق M-24", al, [G("ev_card")], "loc_office", "OPEN_CARD")
Act("a_open_datafile", "examine", "افتح ملف جمع بيانات الجرد", al, [G("ev_datafile")], "obj_datafile", "OPEN_DATAFILE")
for cid, lab in [("salim", "سليم"), ("nuha", "نهى")]:
    Act(f"a_int_{cid}", "interview", f"ابدأ مقابلة {lab}", al, [{"op": "raise_trust", "ref_id": cid, "amount": 1}], cid, f"INT_{cid.upper()}")
Act("a_int_walid", "interview", "ابدأ مقابلة وليد", he("ev_reviewer_note"), [{"op": "raise_trust", "ref_id": "walid", "amount": 1}], "walid", "INT_WALID")
Act("a_get_policy", "examine", "اطلب سياسة ترقيم المقتنيات", fu("f_numbering_design"), [G("ev_policy")], "salim", "GET_POLICY")
Act("a_get_donor", "examine", "اطلب ملف الإهداء وجرد المتبرعة", fu("f_donor_file"), [G("ev_donor")], "salim", "GET_DONOR")
Act("a_get_packing", "examine", "اطلب قائمة تعبئة الورثة", fu("f_packing_attached"), [G("ev_packing")], "loc_receiving", "GET_PACKING")
Act("a_get_condition", "examine", "اطلب نموذج فحص الحالة عند الاستلام", fu("f_condition_sheet"), [G("ev_condition")], "loc_receiving", "GET_CONDITION")
Act("a_note_curator", "examine", "دوّن إفادة سليم", fu("f_no_test"), [G("ev_curator_stmt")], "salim", "NOTE_CURATOR")
Act("a_note_clerk", "examine", "دوّن إفادة نهى", fu("f_clerk_compiled"), [G("ev_clerk_stmt")], "nuha", "NOTE_CLERK")
Act("a_note_reviewer", "examine", "دوّن إفادة وليد", fu("f_reviewer_saw_image"), [G("ev_reviewer_stmt")], "walid", "NOTE_REVIEWER")
Act("p_datafile_nuha", "present_evidence", "اعرض ملف جمع البيانات على نهى", {"presented": {"evidence_id": "ev_datafile", "to_character": "nuha"}}, [{"op": "emit_event", "ref_id": "PRESENTED_DATAFILE"}], "nuha", "P_DATAFILE_NUHA", 0)
Act("a_hint", "request_hint", "اطلب تلميحاً", al, [], None, "REQUEST_HINT", 0)
Act("a_accuse", "final_accusation", "قدّم الاستنتاج النهائي", al, [{"op": "emit_event", "ref_id": "SUBMIT"}], None, "FINAL_ACCUSATION", 0)

topics = [
    {"id": "t_numbering", "label_ar": "نظام ترقيم الصناديق والقطع", "example_questions_ar": ["كيف يُرقَّم الصندوق والقطعة؟", "هل يتكرر رقم القطعة؟"], "fact_ids": ["f_numbering_design"]},
    {"id": "t_donor", "label_ar": "ملف الإهداء وجرد المتبرعة", "example_questions_ar": ["هل يوجد جرد من المتبرعة؟", "ماذا في ملف الإهداء؟"], "fact_ids": ["f_donor_file"]},
    {"id": "t_test", "label_ar": "الفحص التقني للقطعتين", "example_questions_ar": ["هل أُجري فحص تقني؟", "هل فُحص المعدن؟"], "fact_ids": ["f_no_test"]},
    {"id": "t_packing", "label_ar": "قائمة التعبئة المرفقة بالشحنة", "example_questions_ar": ["ماذا أُرفق بالشحنة؟", "هل وصلت قائمة تعبئة؟"], "fact_ids": ["f_packing_attached"]},
    {"id": "t_condition", "label_ar": "فحص الحالة عند الاستلام", "example_questions_ar": ["كيف فحصت القطعتين؟", "ماذا دوّنت عن كل قطعة؟"], "fact_ids": ["f_condition_sheet"]},
    {"id": "t_datafile", "label_ar": "إعداد ملف جمع البيانات", "example_questions_ar": ["من أعدّ الجدول؟", "ماذا يعني عمود الرقم؟", "من أين نقلت القيمة؟"], "fact_ids": ["f_clerk_compiled", "f_column_from_box"], "claim_ids": ["cl_clerk_column"]},
    {"id": "t_review", "label_ar": "ما اطّلع عليه المراجع", "example_questions_ar": ["ماذا رأيت من السجلات؟", "على ماذا بنيت تنبيهك؟"], "fact_ids": ["f_reviewer_saw_image"], "claim_ids": ["cl_reviewer_dup"]},
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
    (1, "سجل الوارد وبطاقة المتحف يذكران حاوية واحدة برقمي قطعة مختلفين، وسياسة الترقيم تجعل رقم الحاوية هو ما يتكرر ورقم القطعة هو ما لا يتكرر.", ["ev_ledger", "ev_card", "ev_policy"], "i_path_a"),
    (2, "مسار ثانٍ لا يستعمل أرقام المتحف: قائمة الورثة تذكر صينيتين في صندوق واحد بعلامتين، ونموذج الاستلام يربط كل رقم بعلامته.", ["ev_packing", "ev_condition"], "i_path_b"),
    (3, "القيمة 24 في الجدول المشتق تطابق رقم الحاوية في السجلين، لا رقمي القطعتين، فالعمود الذي لم يُعرَّف حمل رقم الحاوية.", ["ev_datafile", "ev_ledger", "ev_card"], "i_column"),
    (4, "جرد المتبرعة المؤرخ قبل الترقيم يذكر زوجاً بإصلاح قديم في إحدى الحافتين، فيتفق مع نموذج الاستلام من مصدر مستقل.", ["ev_donor", "ev_condition"], "i_provenance"),
    (5, "إذن لا نسخة مزورة ولا استبدال ولا خطأ كتابي: هي قطعتان في صندوق واحد، والتشابه في رقم الحاوية لا في رقم القطعة.", ["ev_condition", "ev_policy"], "i_support_confusion"),
]
ending = {
    "steps": [{"order": o, "text_ar": t, "uses_evidence_ids": u, "inference_id": i} for o, t, u, i in steps],
    "alternative_paths_ar": ["يكفي المسار الأول وحده (السجلان والسياسة) أو المسار الثاني وحده (قائمة الورثة ونموذج الاستلام)؛ والأقوى أن يتقاطعا."],
    "what_evidence_could_not_show_ar": ["لم يُجرَ أي فحص تقني للمعدن أو العمر؛ فعدم وجود قرينة على التزييف ليس برهاناً فنياً على الأصالة.", "لا يثبت إلا إفادة الموظفة كيف انتقلت القيمة إلى الجدول، ولا سجل آخر يبيّن ذلك.", "وثائق الورثة وصف نصي لا يثبت عمر القطعتين."],
    "science_notes_ar": ["تطابق قيمة لا يعني تطابق كيان: القيمة نفسها قد تسمّي حاوية في وثيقة وعنصراً في أخرى.", "قبل مطابقة السجلات اسأل ما الذي يعرّفه كل حقل، ومن يملك قاموس البيانات.", "سلسلة العهدة تتتبع حركة كل قطعة، لا رقم الصندوق وحده."],
}
core = {
    "schema_version": "0.1.0", "case_id": CID, "case_version": "0.1.0",
    "meta": {"title_ar": "الصندوق ذو الرقمين", "title_en": "The Box With Two Numbers", "age_band": "16-18", "locale": "ar", "dialogue_register": "msa", "estimated_minutes": 25, "difficulty": 2,
             "content_flags": ["no_violence"], "authors": ["فريق أثر التحريري (مسودة بمساعدة الذكاء الاصطناعي، لم تُراجَع بشرياً بعد)"],
             "knowledge_object_refs": ["KO-RS-05-001", "KO-RS-05-002", "KO-RS-05-004", "KO-RS-05-014", "KO-RS-06-001", "KO-RS-06-004", "KO-RS-06-008", "KO-RS-06-009", "KO-RS-06-021", "KO-FC-04-026"]},
    "premise": {"hook_ar": "رقم واحد في صفين، واتهام بنسخة مزورة. هل الرقم هو ما تظنه؟",
                "player_role_ar": "أنت مدقق بيانات في متحف الحِرَف، وأول مهامك أن تحسم هل في الجرد قطعة مزورة أم أن في الجدول خللاً.",
                "setting_ar": "متحف الحِرَف في المدينة، بعد إهداء من ورثة متبرعة. كل التواريخ بتوقيت المتحف.",
                "public_fact_ids": ["f_two_rows_same_number", "f_forgery_alleged"],
                "assumed_general_knowledge_ar": ["الأرقام قد تسمّي أشياء من أنواع مختلفة", "الجدول المُصدَّر قد يحذف عناوين الحقول الأصلية"]},
    "entities": {"characters": chars, "locations": locations, "objects": objects, "organizations": orgs},
    "truth": {"solution": {"culprit_ids": ["nuha"], "summary_ar": "لا نسخة مزورة في الجرد. القطعتان صينيتان مختلفتان وصلتا في صندوق واحد، والرقم المكرر هو رقم الصندوق لا رقم قطعة. جمعت موظفة الاستلام الصفّين في عمود واحد غير مسمّى، فظهر التشابه كأنه تكرار قطعة.", "key_fact_ids": [KF]},
              "facts": facts, "claims": claims},
    "timeline": timeline, "evidence": ev, "evidence_graph": {"inferences": inf},
    "character_knowledge": ck, "hypotheses": hyps, "misdirection_plan": mis, "learning_objectives": los,
    "mechanics": {"time_budget_units": 30, "actions": A},
    "state_machine": {"id": "c005", "initial": "briefing", "type": "compound", "states": {
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
    "clock": {"epoch_hhmm": "00:00", "zone_label_ar": "توقيت المتحف"},
    "cover": {"title_ar": "الصندوق ذو الرقمين", "tagline_ar": "الرقم نفسه… لكن هل هو الشيء نفسه؟", "kicker_ar": "قضية · متحف الحِرَف", "glyph": "▣", "accent": "green"},
    "cold_open_ar": [
        "جرد نهاية الأسبوع في متحف الحِرَف.",
        "في جدول الجرد صينيتان نحاسيتان متشابهتان، وفي خانة «الرقم» عندهما القيمة نفسها.",
        "مراجع خارجي لفت الأنظار إلى التكرار، وانتشر في المتحف همس باتهام: «إحداهما مزورة».",
        "أمامك سجلات وأرقام. قبل أن تحكم، اسأل: ماذا يعني هذا الرقم في كل وثيقة؟",
    ],
    "labs": [],
    "source_classes": [
        {"id": "primary_record", "label_ar": "سجل أصلي", "help_ar": "يُنتجه نظام أو شخص لحظة الحدث دون وسيط، كسجل الوارد ونموذج الاستلام."},
        {"id": "redisplay", "label_ar": "نسخة معروضة", "help_ar": "معلومة جُمعت أو نُقلت من وثائق أخرى، كجدول مُصدَّر."},
        {"id": "claim", "label_ar": "قول أو تصريح", "help_ar": "إفادة أو تخمين؛ يُقاس بالسجلات لا بلقب صاحبه."},
        {"id": "template", "label_ar": "قالب أو نموذج", "help_ar": "نص جاهز لا يصف الحدث الفعلي بذاته."},
        {"id": "public_document", "label_ar": "وثيقة منشورة", "help_ar": "وثيقة معلنة ومعروف ناشرها، كسياسة معتمدة."}],
    "limit_menu": [
        {"id": "l_no_test", "label_ar": "لم يُجرَ فحص تقني للمعدن أو العمر، فالأصالة هنا مبنية على السجلات وحدها"},
        {"id": "l_how_filled", "label_ar": "إفادة الموظفة وحدها تشرح كيف دخل رقم الصندوق إلى الجدول"},
        {"id": "l_donor", "label_ar": "جرد المتبرعة وصف نصي لا يغني عن فحص فني"},
        {"id": "l_invalid_dup", "label_ar": "تطابق القيمتين في الجدول يكفي لإثبات وجود نسخة"},
        {"id": "l_invalid_title", "label_ar": "تنبيه مراجع خارجي يعني أن الاتهام صحيح"},
        {"id": "l_invalid_swap", "label_ar": "اختلاف رقمي القطعتين في السجلين يثبت حدوث استبدال"}],
    "mind_change_menu": [
        {"id": "m_ledger_edit", "label_ar": "ثبوت أن سجل الوارد عُدّل بعد الاستلام"},
        {"id": "m_other_box", "label_ar": "ثبوت أن الصينيتين وصلتا في صندوقين مختلفين"},
        {"id": "m_policy_changed", "label_ar": "ثبوت أن سياسة الترقيم المعتمدة تمنع أن تضم الحاوية أكثر من قطعة"},
        {"id": "m_title", "label_ar": "كون المراجع الخارجي أكثر خبرة من موظفة الاستلام"},
        {"id": "m_many", "label_ar": "كثرة من يردّدون الاتهام في المتحف"}],
    "transfer": {
        "id": "tr_library", "title_ar": "اختبار نقل المهارة: كتب المكتبة",
        "scenario_ar": "مكتبة جامعية تفحص جدولاً فيه رقم 7 مكرر لثلاثة كتب، ويقول موظف إن في الجدول نسخاً مكررة مسروقة. أمامك ثلاث وثائق.",
        "documents": [
            {"title_ar": "الجدول", "body_ar": "الأعمدة: الرقم | العنوان. الصفوف: 7 | مدخل إلى الفلك، 7 | مدخل إلى الفلك، 7 | مدخل إلى الفلك."},
            {"title_ar": "دليل الرفوف", "body_ar": "الرف رقم 7 في القاعة الثانية يضم الكتب الفلكية؛ يحمل كل كتاب رقم الرف ثم رقماً تسلسلياً خاصاً به."},
            {"title_ar": "بطاقات الكتب", "body_ar": "الكتاب الأول: رف 7 / تسلسل 31. الكتاب الثاني: رف 7 / تسلسل 32. الكتاب الثالث: رف 7 / تسلسل 33."},
        ],
        "prompt_ar": "اختر الخطوات التي تصلح لتحديد هل في الجدول نسخ مكررة (يمكنك اختيار أكثر من خطوة).",
        "options": [
            {"id": "o1", "text_ar": "سؤال ماذا يعني الرقم في عمود «الرقم»: هل هو رقم الرف أم رقم الكتاب؟"},
            {"id": "o2", "text_ar": "مطابقة الصفوف على الحقلين معاً: رقم الرف والرقم التسلسلي"},
            {"id": "o3", "text_ar": "قراءة دليل الرفوف لمعرفة هل يجوز أن يضم الرف أكثر من كتاب"},
            {"id": "o4", "text_ar": "البحث عن وثيقة مستقلة تصف كل كتاب على حدة"},
            {"id": "o5", "text_ar": "الحكم بأن الصفوف المتطابقة تعني كتباً مكررة"},
            {"id": "o6", "text_ar": "حذف صفين من الجدول لأن لهما القيمة نفسها"},
            {"id": "o7", "text_ar": "تصديق الموظف الأعلى منصباً"},
            {"id": "o8", "text_ar": "اعتبار تكرار القيمة دليلاً على سرقة"}],
        "free_text_prompt_ar": "اكتب في ثلاثة أسطر كيف تتأكد من أن قيمتين متشابهتين تسميان الشيء نفسه قبل أن تتهم أحداً.",
    },
    "skills": [{"skill_id": "KO-RS-05-001", "track": "B"}, {"skill_id": "KO-RS-05-002", "track": "D"}, {"skill_id": "KO-RS-06-001", "track": "C"}, {"skill_id": "KO-RS-06-009", "track": "D"}, {"skill_id": "KO-RS-06-021", "track": "D"}, {"skill_id": "KO-FC-04-026", "track": "E"}],
    "stage_hooks_ar": {"briefing": "رقم واحد في صفين… هل هما صفّان لشيء واحد؟", "investigating": "لا تقارن القيم قبل أن تعرف ماذا يسمّي كل حقل.", "review": "قبل أن تُغلق الملف: ما الذي لم يُفحص بعد؟", "resolved": "أُغلق ملف الجدول. المتحف يملك سجلات أخرى بأسماء حقول تشبه هذه."},
    "character_glyphs": {"salim": "س", "nuha": "ن", "walid": "و"},
}
sc = {
    "case_id": CID,
    "accepted_conclusions": {
        "h_confusion": {"grade": 1, "note_ar": "استنتاج متسق مع الأدلة ويتطلب ذكر حدوده."},
        "h_fake": {"grade": 0, "note_ar": "يخلط بين تطابق القيمة وتطابق القطعة."},
        "h_swap": {"grade": 0, "note_ar": "السجلان لا يتعارضان إذا ضمّت الحاوية قطعتين."},
        "h_typo": {"grade": 0, "note_ar": "كل سجل يصف قطعة موجودة، فلا خطأ كتابياً يلزم افتراضه."}},
    "confidence_band": {"h_confusion": [65, 90], "h_fake": [0, 15], "h_swap": [0, 15], "h_typo": [0, 20]},
    "source_key": {"ev_ledger": "primary_record", "ev_card": "primary_record", "ev_datafile": "redisplay", "ev_policy": "public_document", "ev_reviewer_note": "claim",
                   "ev_packing": "primary_record", "ev_condition": "primary_record", "ev_donor": "primary_record",
                   "ev_curator_stmt": "claim", "ev_clerk_stmt": "claim", "ev_reviewer_stmt": "claim"},
    "link_key": {
        "h_confusion": {"ev_ledger": "supports", "ev_card": "supports", "ev_policy": "supports", "ev_packing": "supports", "ev_condition": "supports", "ev_datafile": "neutral", "ev_donor": "supports"},
        "h_fake": {"ev_datafile": "neutral", "ev_reviewer_note": "neutral", "ev_policy": "weakens", "ev_condition": "weakens", "ev_packing": "weakens", "ev_donor": "weakens"},
        "h_swap": {"ev_ledger": "neutral", "ev_card": "neutral", "ev_policy": "weakens", "ev_condition": "weakens", "ev_packing": "weakens"},
        "h_typo": {"ev_ledger": "weakens", "ev_card": "weakens", "ev_condition": "weakens", "ev_packing": "weakens"}},
    "required_limits": ["l_no_test", "l_how_filled"], "valid_mind_changers": ["m_ledger_edit", "m_other_box", "m_policy_changed"],
    "invalid_limits": ["l_invalid_dup", "l_invalid_title", "l_invalid_swap"],
    "decisive_evidence": ["ev_ledger", "ev_card", "ev_policy", "ev_packing", "ev_condition"],
    "lab_requirement": None,
    "refuted_hypotheses": ["h_fake", "h_swap", "h_typo"],
    "criteria_map": {"c_source": "source_typing", "c_links": "hypothesis_links", "c_elimination": "elimination", "c_uncertainty": "uncertainty", "c_revision": "revision", "c_justification": "justification_human"},
    "transfer_key": {"valid": ["o1", "o2", "o3", "o4"], "invalid": ["o5", "o6", "o7", "o8"]},
    "caps": {"no_citations_max": 45, "no_conflict_resolution_max": 70},
}
os.makedirs(OUT, exist_ok=True)
for suf, obj in [("", core), (".ui", ui), (".scoring", sc)]:
    with open(os.path.join(OUT, f"{CID}{suf}.json"), "w", encoding="utf8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
print("ok")
