#!/usr/bin/env python3
# Case c008 «رسالة وصلت مبكراً» — time-zone / field-label reasoning. Teaches: normalise times to one reference before comparing,
# read what each timestamp field MEANS (created vs sent vs notified), and never equate a discrepancy with a lie.
# No-culprit convention: the person whose (innocent) action produced the confusing date (the editor who opened the draft early)
# is recorded in culprit_ids; nobody did anything wrong. Usage: gen_c008.py OUT_DIR
import json, sys, os
OUT = sys.argv[1]
CID = "c008_early_message"

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
ch("layla", "ليلى الراشد", "witness", "طالبة في الصف الحادي عشر، شاركت في المسابقة",
   "فضولية ودقيقة في وصف ما رأته على شاشتها، لكنها تفسّر الأرقام بحسب ما تتوقعه لا بحسب ما تعنيه.",
   ["أن تفهم لماذا تبدو أوقات الرسالة غير متفقة", "ألا يظن أحد أنها عرفت النتيجة بطريقة غير سليمة"],
   [L("ly_greet", "greeting", "أهلاً. أريد أن أفهم هذه الأوقات أكثر منكم."),
    L("ly_notified", "reveal", "ظهر إشعار الرسالة على هاتفي وعليه 18:10، وهاتفي مضبوط على التوقيت المحلي، أي UTC+3.", ["f_notified"]),
    L("ly_inbox", "reveal", "حين فتحت قائمة الرسائل وجدت تاريخ الرسالة 14:45، ولم أفهم كيف يسبق الإشعار بكل هذه الساعات.", ["f_layla_inbox"]),
    L("ly_late", "reveal", "ظننت أن الرسالة تأخرت ثلاث ساعات عن وقت إرسالها، فالإشعار 18:10 والإعلان نُشر عند الثالثة وبضع دقائق.", None, ["cl_layla_late"]),
    L("ly_unknown", "deflect_unknown", "لا أعرف، ولا أحب أن أخمّن في الأرقام."),
    L("ly_off", "deflect_offtopic", "هذا لا يخصّ الرسالة. اسألني عمّا رأيته على الشاشة."),
    L("ly_bye", "farewell", "شكراً لأنك تقرأ الأرقام قبل أن تحكم.")])
ch("rayan", "ريان القاسم", "witness", "طالب في الصف الثاني عشر، يشارك في معسكر علمي خارج البلاد",
   "متحمس ويحب الحسم، يرى في كل تعارض دليلاً على خلل، ويتراجع إذا واجهته بسجل واضح.",
   ["أن تكون المسابقة عادلة", "أن يُصحَّح الخلل إن كان هناك خلل"],
   [L("ry_greet", "greeting", "أنا أبلغت اللجنة لأن في الأمر شيئاً غير طبيعي."),
    L("ry_notified", "reveal", "وصلني الإشعار على حاسوبي وعليه 17:11، وتوقيت حاسوبي هنا UTC+2.", ["f_rayan_notified"]),
    L("ry_early", "reveal", "تاريخ رسالة ليلى 14:45، والنتيجة لم تُعتمد إلا 15:07؛ فلا بد أن أحداً أبلغها قبل أن تُكتب.", None, ["cl_rayan_early"]),
    L("ry_unknown", "deflect_unknown", "لا أعرف أكثر من الأرقام التي رأيتها."),
    L("ry_off", "deflect_offtopic", "اسألني عن الإشعار وعن الأوقات فقط."),
    L("ry_bye", "farewell", "أريد جواباً مقنعاً، لا أريد اتهام أحد بلا سبب.")])
ch("faris", "فارس الجابر", "expert", "المسؤول التقني عن بوابة المدرسة",
   "هادئ ومباشر، يعرف تعريفات حقول النظام جيداً ولا يعرف من قرأ الرسالة ولا متى فتحها أحد.",
   ["أن تُفهم حقول البوابة فهماً صحيحاً"],
   [L("fr_greet", "greeting", "تفضّل. أستطيع شرح الحقول، لكنني لا أعرف من قرأ الرسالة."),
    L("fr_sent", "reveal", "سجل الخادم يضع وقت الإرسال 15:10 بالتوقيت العالمي UTC.", ["f_sent"]),
    L("fr_autosave", "reveal", "المحرر يحفظ المسودات آلياً ويحتفظ بسجل لنسخها.", ["f_autosave_exists"]),
    L("fr_guide", "reveal", "للبوابة دليل منشور يعرّف كل حقل يظهر فيها.", ["f_guide_exists"]),
    L("fr_column", "reveal", "عمود «التاريخ» في قائمة الرسائل يعرض وقت إنشاء المسودة، لا وقت الإرسال.", ["f_list_date_created"]),
    L("fr_unknown", "deflect_unknown", "هذا خارج ما أعرفه عن النظام."),
    L("fr_off", "deflect_offtopic", "اسألني عن حقول البوابة فقط."),
    L("fr_bye", "farewell", "إن شككت في معنى حقل فاقرأ تعريفه أولاً.")])
ch("hind", "هند السعدي", "suspect", "محررة بيانات المسابقة",
   "مجتهدة وتخاف أن تُلام على أي تفصيل، فتقلّل من شأن خطوة أولى قامت بها مبكراً.",
   ["ألا تُلام على تاريخ ظهر في القائمة", "أن تُنشر النتيجة صحيحة"],
   [L("hn_greet", "greeting", "تفضّل. أنا أعدّ نصوص الإعلانات قبل نشرها."),
    L("hn_final", "reveal", "اعتمدت لجنة المسابقة النص النهائي ووصلني الاعتماد، وحفظت النسخة النهائية الساعة 15:07 UTC.", ["f_final_approved"]),
    L("hn_approval", "reveal", "وصلتني رسالة اعتماد من رئيسة اللجنة، وهي محفوظة عندي.", ["f_approval_exists"]),
    L("hn_refuse", "refuse_secret", "لا أذكر شيئاً آخر قبل الاعتماد."),
    L("hn_draft", "reveal", "نعم... فتحت المحرر 14:45 وكتبت العنوان فقط، وتركت النص فارغاً حتى تعتمد اللجنة النتيجة. لم أرسل شيئاً قبل ذلك.", ["f_draft_created"]),
    L("hn_unknown", "deflect_unknown", "لا أعرف."),
    L("hn_off", "deflect_offtopic", "اسألني عن إعداد الإعلان."),
    L("hn_bye", "farewell", "أرجو أن يتضح الأمر قبل أن يُظلم أحد.")])

locations = [{"id": "loc_portal", "name_ar": "خادم بوابة المدرسة", "description_ar": "سجلات الإرسال والنسخ الآلية."},
             {"id": "loc_office", "name_ar": "مكتب لجنة المسابقة", "description_ar": "حيث تُعدّ الإعلانات وتُعتمد."},
             {"id": "loc_home", "name_ar": "هاتف ليلى", "description_ar": "الجهاز الذي وصله الإشعار الأول."},
             {"id": "loc_camp", "name_ar": "حاسوب ريان في المعسكر", "description_ar": "جهاز يعمل بتوقيت بلد المعسكر."}]
objects = [{"id": "obj_msg", "name_ar": "رسالة النتيجة M-204", "description_ar": "رسالة بوابة المدرسة التي تعلن نتيجة مسابقة المقال العلمي."}]
orgs = [{"id": "org_school", "name_ar": "ثانوية الأفق", "description_ar": "مدرسة خيالية تنظم مسابقة المقال العلمي."}]

# ---------------------------------------------------------------- facts
facts = []
def F(id, st, kind, subj, spoiler, time=None, loc=None, ko=None):
    d = {"id": id, "statement_ar": st, "kind": kind, "subject_ids": subj, "spoiler_level": spoiler}
    if time: d["time"] = time
    if loc: d["location_id"] = loc
    if ko: d["science_ko_refs"] = ko
    facts.append(d)
F("f_result_published", "نُشرت نتيجة مسابقة المقال العلمي عبر بوابة المدرسة عصر يوم الخميس.", "event", ["obj_msg"], 0)
F("f_rayan_alleges", "يقول ريان إن ليلى علمت بالنتيجة قبل أن تُكتب.", "attribute", ["rayan", "layla"], 0)
F("f_layla_confused", "ترى ليلى أن أوقات الرسالة لا تتفق ولا تعرف السبب.", "attribute", ["layla"], 0)
F("f_notified", "ظهر إشعار الرسالة على هاتف ليلى وعليه 18:10 بتوقيت هاتفها (UTC+3).", "event", ["layla", "obj_msg"], 1, T(70), "loc_home", ["KO-FC-04-024"])
F("f_layla_inbox", "يظهر في قائمة رسائل ليلى تاريخ للرسالة هو 14:45.", "state", ["layla", "obj_msg"], 1, None, "loc_home")
F("f_rayan_notified", "ظهر إشعار الرسالة على حاسوب ريان وعليه 17:11 بتوقيت حاسوبه (UTC+2).", "event", ["rayan", "obj_msg"], 1, T(71), "loc_camp", ["KO-FC-04-024"])
F("f_sent", "وُضعت الرسالة في قائمة الإرسال الساعة 15:10 UTC.", "event", ["obj_msg", "loc_portal"], 1, T(70), "loc_portal")
F("f_autosave_exists", "محرر البوابة يحفظ المسودات آلياً ويحتفظ بسجل لنسخها.", "state", ["loc_portal"], 1)
F("f_guide_exists", "للبوابة دليل حقول منشور يعرّف معنى كل تاريخ يظهر فيها.", "state", ["loc_portal"], 1)
F("f_list_date_created", "عمود «التاريخ» في قائمة الرسائل يعرض وقت إنشاء المسودة، لا وقت الإرسال.", "attribute", ["obj_msg", "loc_portal"], 2, None, "loc_portal", ["KO-FC-04-024"])
F("f_final_approved", "حُفظ النص النهائي الذي يتضمن النتيجة الساعة 15:07 UTC بعد اعتماد اللجنة.", "event", ["hind", "obj_msg"], 1, T(67), "loc_office")
F("f_approval_exists", "بعثت رئيسة اللجنة إلى المحررة رسالة اعتماد بالنتيجة.", "state", ["hind"], 1)
F("f_draft_created", "أنشأت المحررة مسودة الرسالة وحُفظت آلياً الساعة 14:45 UTC بعنوان فقط ودون نتيجة.", "event", ["hind", "obj_msg"], 2, T(45), "loc_office", ["KO-RS-06-017"])
F("f_same_instant", "إشعارا هاتف ليلى وحاسوب ريان، بعد تحويلهما إلى مرجع واحد، يصفان وصولاً واحداً تقريباً (15:10 و15:11 UTC).", "relation", ["layla", "rayan", "obj_msg"], 2, T(70, "approx", 71), None, ["KO-FC-04-024", "KO-RS-05-005"])
F("f_after_final", "وصلت الرسالة الطلاب بعد حفظ نصها النهائي (15:10 UTC مقابل 15:07 UTC)، فلم تصل قبل أن توجد النتيجة.", "relation", ["obj_msg", "hind"], 3, T(67, "exact", 70), None, ["KO-RS-05-005", "KO-RS-06-017"])
F("f_date_is_draft", "التاريخ 14:45 الذي تعرضه القائمة هو وقت إنشاء مسودة بلا نتيجة، لا وقت وصول الرسالة إلى أحد.", "relation", ["obj_msg", "hind"], 3, T(45), None, ["KO-FC-04-024", "KO-RS-05-001"])

claims = [
    {"id": "cl_rayan_early", "statement_ar": "وصلت الرسالة ليلى قبل أن تُكتب النتيجة، فلا بد أن أحداً أبلغها مسبقاً.", "kind": "half_truth", "held_by": ["rayan"], "true_fact_id": "f_after_final", "contradicted_by_evidence_ids": ["ev_draft_history", "ev_published_notice"]},
    {"id": "cl_layla_late", "statement_ar": "الرسالة تأخرت ثلاث ساعات عن إرسالها.", "kind": "honest_mistake", "held_by": ["layla"], "true_fact_id": "f_same_instant", "contradicted_by_evidence_ids": ["ev_lab_norm", "ev_system_ref"]},
]
timeline = [
    {"id": "te_draft", "description_ar": "هند تفتح محرر الرسالة وتكتب العنوان فقط، فيُحفظ آلياً.", "time": T(45), "location_id": "loc_office", "actor_ids": ["hind"], "fact_ids": ["f_draft_created"], "motivated_by_ar": "أرادت تجهيز الإعلان قبل اعتماد اللجنة"},
    {"id": "te_final", "description_ar": "حفظ النص النهائي بعد اعتماد اللجنة.", "time": T(67), "location_id": "loc_office", "actor_ids": ["hind"], "fact_ids": ["f_final_approved"], "motivated_by_ar": "وصلها اعتماد رئيسة اللجنة"},
    {"id": "te_send", "description_ar": "الرسالة تدخل قائمة الإرسال في الخادم.", "time": T(70), "location_id": "loc_portal", "actor_ids": [], "fact_ids": ["f_sent"]},
    {"id": "te_layla", "description_ar": "الإشعار يظهر على هاتف ليلى.", "time": T(70, "approx"), "location_id": "loc_home", "actor_ids": ["layla"], "fact_ids": ["f_notified"], "motivated_by_ar": "تلقّت إشعاراً تلقائياً من التطبيق"},
    {"id": "te_rayan", "description_ar": "الإشعار يظهر على حاسوب ريان في المعسكر.", "time": T(71, "approx"), "location_id": "loc_camp", "actor_ids": ["rayan"], "fact_ids": ["f_rayan_notified"], "motivated_by_ar": "تلقّى إشعاراً تلقائياً من التطبيق"},
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
V("ev_server_log", "سجل إرسال بوابة المدرسة", "digital",
  "سجل خادم البوابة (كل الأوقات بالتوقيت العالمي UTC)\nالرسالة M-204 «نتيجة مسابقة المقال العلمي»\nالحالة: مُرسلة\nوقت الإرسال sent_at: 15:10 UTC\nالمستلمون: 4 طلاب\nالمحاولات: 1",
  ["a_read_server"], ["f_sent"], "strong",
  "يثبت وقت وضع الرسالة في قائمة الإرسال؛ لا يثبت وقت ظهور الإشعار عند كل مستلم ولا ما كُتب في نصها.", loc="loc_portal")
V("ev_published_notice", "إعلان النتيجة كما نُشر", "documentary",
  "ثانوية الأفق — مسابقة المقال العلمي\nإعلان النتيجة (النسخة النهائية)\nالمركز الأول: مقال «ماء الفجر»\nالمركز الثاني: مقال «صدى الطين»\nحُفظت النسخة النهائية: 15:07 UTC\nاعتمدتها: لجنة المسابقة",
  ["a_read_notice"], ["f_final_approved"], "strong",
  "وثيقة منشورة تبيّن وقت حفظ النسخة النهائية؛ لا تذكر وقت إرسالها ولا ما حفظه المحرر قبلها.", loc="loc_office")
V("ev_phone_screen", "لقطة شاشة هاتف ليلى", "digital",
  "لقطة شاشة هاتف ليلى:\nإشعار: «بوابة المدرسة — نتيجة مسابقة المقال العلمي»\nوقت ظهور الإشعار: 18:10\nإعدادات الهاتف: المنطقة الزمنية UTC+3 (ضبط تلقائي)",
  ["a_get_phone"], ["f_notified"], "moderate",
  "لقطة لجهاز واحد تعرض وقت ظهور الإشعار بتوقيت الجهاز؛ لا تعرض وقت الإرسال ولا تثبت وحدها صحة ضبط ساعته.", red=True, loc="loc_home")
V("ev_laptop_screen", "لقطة شاشة حاسوب ريان", "digital",
  "لقطة شاشة حاسوب ريان:\nإشعار سطح المكتب: «بوابة المدرسة — نتيجة مسابقة المقال العلمي»\nوقت الظهور: 17:11\nالمنطقة الزمنية للحاسوب: UTC+2",
  ["a_get_laptop"], ["f_rayan_notified"], "moderate",
  "لقطة لجهاز واحد بتوقيت بلد المعسكر؛ تصف جهازه هو لا جهاز ليلى.", loc="loc_camp")
V("ev_inbox_screen", "لقطة قائمة رسائل ليلى", "digital",
  "لقطة من قائمة الرسائل في بوابة المدرسة (الحساب: ليلى)\nالرسالة: نتيجة مسابقة المقال العلمي\nالتاريخ: 14:45 (توقيت البوابة UTC)\nالحالة: غير مقروءة",
  ["a_get_inbox"], ["f_layla_inbox"], "moderate",
  "تعرض عمودًا اسمه «التاريخ» ولا تبيّن أي حقل في النظام يغذّيه.", red=True, loc="loc_home")
V("ev_draft_history", "سجل النسخ الآلية لمحرر البوابة", "digital",
  "سجل نسخ محرر البوابة (UTC) — الرسالة M-204\nالنسخة 1 — 14:45:03 — حفظ آلي — العنوان: «نتيجة مسابقة المقال العلمي» — النص: «[تُكتب النتيجة لاحقاً]»\nالنسخة 2 — 15:07:40 — حفظ يدوي — النص الكامل متضمناً النتيجة",
  ["a_get_draft"], ["f_draft_created", "f_final_approved"], "strong",
  "يبيّن ما كان في كل نسخة ووقت حفظها؛ لا يبيّن متى أُرسلت الرسالة ولا من فتحها.", contradicts=["cl_rayan_early"], loc="loc_portal")
V("ev_system_ref", "دليل حقول بوابة المدرسة", "documentary",
  "دليل المستخدم — حقول التواريخ في البوابة\ncreated_at: وقت أول حفظ آلي لمسودة الرسالة (UTC).\nsent_at: وقت وضع الرسالة في قائمة الإرسال (UTC).\nnotified_at: وقت ظهور الإشعار على جهاز المستلم، بتوقيت جهازه المحلي.\nعمود «التاريخ» في قائمة الرسائل يعرض الحقل created_at.",
  ["a_get_guide"], ["f_list_date_created"], "strong",
  "مرجع تعريفي منشور؛ يشرح معنى الحقول ولا يخبر بقيمها في رسالة بعينها.", contradicts=["cl_layla_late"], loc="loc_portal")
V("ev_approval_email", "رسالة اعتماد النتيجة", "digital",
  "رسالة داخلية من رئيسة لجنة المسابقة إلى المحررة\nالوقت: 15:07 UTC\nالموضوع: اعتماد النتيجة\n«اعتمدتُ النتيجة بصيغتها الأخيرة. أرسلي الإعلان للطلاب الآن.»",
  ["a_get_approval"], ["f_final_approved"], "strong",
  "تثبت وقت الاعتماد؛ لا تثبت وقت الإرسال ولا وقت وصول الرسالة.", loc="loc_office")
V("ev_lab_norm", "تقرير توحيد الأزمنة", "lab_result",
  "تقرير مختبر الأزمنة: بعد تحويل 18:10 (UTC+3) و17:11 (UTC+2) إلى التوقيت العالمي يتوافق إشعار هاتف ليلى وحاسوب ريان عند نحو 15:10 و15:11 UTC بفارق دقيقة. أي أن الفارق الظاهر بينهما ناتج عن اختلاف المنطقة الزمنية لا عن اختلاف اللحظة.",
  ["a_compare_times"], ["f_same_instant"], "strong",
  "نتيجة حسابية تعتمد على صحة الإزاحتين المدخلتين؛ توحّد الأزمنة ولا تقول متى كُتب النص ولا من علم به قبل غيره.", contradicts=["cl_layla_late"], ko="KO-FC-04-024", loc="loc_portal")
V("ev_faris_statement", "إفادة فارس الجابر (ملخص)", "testimonial",
  "ملخص إفادة فارس الجابر، المسؤول التقني:\n«عمود التاريخ في قائمة الرسائل يأخذ قيمته من وقت إنشاء المسودة، لا من وقت الإرسال. لا أعرف من فتح الرسالة ولا متى.»",
  ["a_note_faris"], ["f_list_date_created"], "moderate",
  "إفادة خبير بالنظام عن تعريف الحقول؛ تُقاس بالدليل المنشور وبالسجل، ولا تخبر بما حدث لرسالة بعينها.", loc="loc_portal")
V("ev_layla_statement", "إفادة ليلى (ملخص)", "testimonial",
  "ملخص إفادة ليلى الراشد:\n«ظهر الإشعار على هاتفي 18:10 فظننت أن الرسالة تأخرت ثلاث ساعات. وفي القائمة تاريخ الرسالة 14:45، ولا أفهم السبب.»",
  ["a_note_layla"], ["f_notified", "f_layla_inbox"], "weak",
  "تصف ما رأته على شاشتها وتضيف تفسيراً من عندها؛ يُقاس التفسير بتعريف الحقول.", loc="loc_home")
V("ev_rayan_statement", "إفادة ريان (ملخص)", "testimonial",
  "ملخص إفادة ريان القاسم:\n«وصلني الإشعار 17:11 بتوقيت حاسوبي. لكن تاريخ رسالة ليلى 14:45، أي قبل 15:07، فأرى أن أحداً أبلغها مسبقاً.»",
  ["a_note_rayan"], ["f_rayan_notified"], "weak",
  "استنتاج صاحبه من مقارنة أرقام بعضها بتوقيت مختلف وبعضها لا يُعرف حقله؛ يحتاج إلى معنى الحقل قبل أن يصير دليلاً.", loc="loc_camp")
V("ev_hind_statement", "إفادة هند (ملخص)", "testimonial",
  "ملخص إفادة هند السعدي، محررة البيان:\n«فتحت المحرر 14:45 وكتبت العنوان فقط. حفظت النص النهائي 15:07 بعد الاعتماد وأرسلت الإعلان بعده.»",
  ["a_note_hind"], ["f_draft_created", "f_final_approved"], "weak",
  "إفادة صاحبة الشأن؛ تؤيدها سجلات النسخ ولا تغني عنها.", loc="loc_office")

# ---------------------------------------------------------------- inferences
def P(t, i): return {"ref_type": t, "ref_id": i}
inf = []
def I(id, prem, ct, concl, rel, strength, rule, ks):
    inf.append({"id": id, "premises": prem, "conclusion": {"ref_type": ct, "ref_id": concl}, "relation": rel, "strength": strength, "rule_ar": rule, "skill_ko_refs": ks})
I("i_a_after", [P("evidence", "ev_server_log"), P("evidence", "ev_published_notice")], "fact", "f_after_final", "establishes", "strong",
  "الخادم يضع الإرسال 15:10 UTC والنسخة النهائية حُفظت 15:07 UTC، والتوقيتان على مرجع واحد؛ فالإرسال جاء بعد اكتمال النص.", ["KO-RS-05-005"])
I("i_b_after", [P("evidence", "ev_lab_norm"), P("evidence", "ev_approval_email")], "fact", "f_after_final", "establishes", "strong",
  "إشعارا الجهازين، بعد توحيد منطقتيهما، يقعان عند 15:10 و15:11 UTC، والاعتماد 15:07 UTC؛ فالوصول جاء بعد الاعتماد بمسار مستقل عن سجل الخادم.", ["KO-RS-05-005", "KO-FC-04-024"])
I("i_a_date", [P("evidence", "ev_inbox_screen"), P("evidence", "ev_system_ref")], "fact", "f_date_is_draft", "establishes", "strong",
  "الدليل المنشور يقول إن عمود «التاريخ» يعرض created_at؛ فالقيمة 14:45 في القائمة وقت إنشاء المسودة لا وقت الوصول.", ["KO-FC-04-024"])
I("i_b_date", [P("evidence", "ev_draft_history"), P("evidence", "ev_faris_statement")], "fact", "f_date_is_draft", "establishes", "strong",
  "سجل النسخ يضع إنشاء المسودة 14:45 وهي بلا نتيجة، وخبير النظام يقول إن عمود التاريخ يأخذ قيمة الإنشاء؛ فالتاريخ الظاهر يعود إلى مسودة فارغة.", ["KO-FC-04-024", "KO-RS-05-001"])
I("i_same", [P("evidence", "ev_lab_norm"), P("evidence", "ev_server_log")], "fact", "f_same_instant", "establishes", "strong",
  "الإشعاران بعد التحويل متقاربان، ويتفقان مع وقت الإرسال في الخادم؛ فالفرق الظاهر في الأرقام من اختلاف المنطقة لا من اختلاف اللحظة.", ["KO-FC-04-024"])
I("i_rayan_claim", [P("fact", "f_after_final"), P("fact", "f_date_is_draft")], "claim", "cl_rayan_early", "contradicts_claim", "strong",
  "التاريخ الذي استند إليه ريان هو تاريخ مسودة فارغة، أما الرسالة بنصها فلم تصل إلا بعد حفظ النتيجة؛ فاستنتاجه قفز من تسمية حقل إلى واقعة لم تحدث.", ["KO-RS-05-001", "KO-RS-05-007"])
I("i_layla_claim", [P("evidence", "ev_lab_norm"), P("evidence", "ev_system_ref")], "claim", "cl_layla_late", "contradicts_claim", "strong",
  "حقل notified_at يُعرض بتوقيت الجهاز المحلي، وبعد طرح الإزاحة (+3) يصير الإشعار 15:10 UTC؛ فلا يوجد تأخير بثلاث ساعات.", ["KO-FC-04-024", "KO-RS-05-007"])
I("i_support_display", [P("fact", "f_after_final"), P("fact", "f_date_is_draft")], "hypothesis", "h_display", "supports", "strong",
  "اختلاف معنى الحقول وتوقيتات العرض يفسّر كل الأرقام: مسودة مبكرة فارغة، واعتماد 15:07، وإرسال 15:10، وإشعارات بتوقيتات محلية.", ["KO-RS-05-002"])
I("i_rule_leak", [P("fact", "f_after_final"), P("fact", "f_date_is_draft")], "hypothesis", "h_leak", "rules_out", "conclusive",
  "لا يمكن أن يُبلَّغ أحد بنتيجة بعد وصولها فقط؛ والتاريخ المبكر كان لمسودة فارغة، فلا يدل على إبلاغ سابق عبر هذه الرسالة.", ["KO-RS-06-008"])
I("i_rule_untrust", [P("fact", "f_after_final"), P("fact", "f_date_is_draft")], "hypothesis", "h_untrust", "rules_out", "strong",
  "حين يُعرف مرجع كل رقم ومعنى كل حقل تتسق سجلات من أنظمة مستقلة في ترتيب واحد؛ فالتضارب كان في قراءتنا الأولى لا في زمن البيانات.", ["KO-RS-06-008"])
I("i_rule_untrust_lab", [P("fact", "f_same_instant")], "hypothesis", "h_untrust", "rules_out", "strong",
  "جهازان بمنطقتين مختلفتين يتطابقان بعد التوحيد؛ فلا يصح القول إن زمن البيانات لا يوثق به.", ["KO-RS-06-008"])

# ---------------------------------------------------------------- character knowledge
K = lambda f, a="witnessed", c="certain": {"fact_id": f, "access": a, "certainty": c}
ck = [
    {"character_id": "layla", "knows": [K("f_notified"), K("f_layla_inbox")], "hides": [], "believes": [{"claim_id": "cl_layla_late", "stance": "sincere"}]},
    {"character_id": "rayan", "knows": [K("f_rayan_notified")], "hides": [], "believes": [{"claim_id": "cl_rayan_early", "stance": "sincere"}]},
    {"character_id": "faris", "knows": [K("f_sent", "professional"), K("f_autosave_exists", "professional"), K("f_guide_exists", "professional"), K("f_list_date_created", "professional")], "hides": [], "believes": []},
    {"character_id": "hind", "knows": [K("f_final_approved"), K("f_approval_exists"), K("f_draft_created")],
     "hides": [{"fact_id": "f_draft_created", "reveal_when": {"presented": {"evidence_id": "ev_inbox_screen", "to_character": "hind"}}, "cover_claim_id": None, "reveal_line_id": "hn_draft"}], "believes": []},
]
hyps = [
    {"id": "h_leak", "statement_ar": "أُبلغت ليلى بالنتيجة قبل أن تُكتب، فالرسالة وصلتها مبكراً بطريقة غير مشروعة.", "is_true": False, "plausibility_at_start": "high"},
    {"id": "h_display", "statement_ar": "اختلاف الأوقات ناتج عن اختلاف معنى الحقول وتوقيتات العرض؛ الرسالة وصلت بعد كتابة نتيجتها.", "is_true": True, "plausibility_at_start": "low", "suspect_id": "hind"},
    {"id": "h_untrust", "statement_ar": "أزمنة البوابة متضاربة ولا يمكن الوثوق بها إطلاقاً.", "is_true": False, "plausibility_at_start": "medium"},
]
mis = [
    {"id": "rh_inbox", "points_to_hypothesis_id": "h_leak", "planted_via_ar": "قائمة رسائل ليلى تضع الرسالة عند 14:45، قبل حفظ النص النهائي 15:07.", "evidence_ids": ["ev_inbox_screen"],
     "refuted_by_inference_ids": ["i_rule_leak", "i_a_date", "i_b_date"],
     "fairness_note_ar": "دليل المستخدم المنشور وسجل النسخ وإفادة الخبير تبيّن كلها أن عمود التاريخ هو وقت الإنشاء، وأن النسخة الأولى كانت بلا نتيجة."},
    {"id": "rh_phone", "points_to_hypothesis_id": "h_untrust", "planted_via_ar": "الهاتف يقول 18:10 والخادم يقول 15:10، فتبدو الأزمنة متضاربة.", "evidence_ids": ["ev_phone_screen"],
     "refuted_by_inference_ids": ["i_rule_untrust", "i_rule_untrust_lab", "i_layla_claim", "i_same"],
     "fairness_note_ar": "اللقطة نفسها تذكر المنطقة الزمنية UTC+3، وحقل notified_at معرَّف في الدليل بأنه بتوقيت الجهاز؛ كل ما يلزم للتحويل متاح للاعب."},
]
los = [
    {"id": "lo_claim", "statement_ar": "يفرّق بين قول فُسِّر خطأً وقول كاذب، ويقيس القول بتعريف الحقل وبالسجل.", "skill_ko_ref": "KO-RS-05-001", "observable_behaviors_ar": ["يصنّف الإفادات أقوالاً", "لا يساوي بين الاختلاف والكذب"], "evidence_sources": ["evidence_board"]},
    {"id": "lo_timeline", "statement_ar": "يوحّد الأزمنة ويرتّب الأحداث على خط زمني واحد.", "skill_ko_ref": "KO-RS-05-005", "observable_behaviors_ar": ["يشغّل مختبر الأزمنة بإزاحات صحيحة", "يضع الأدلة في أزمنتها بالتوقيت العالمي"], "evidence_sources": ["timeline_task", "action_log"]},
    {"id": "lo_hyp", "statement_ar": "يوازن بين فرضيتين على الأقل ويستبعد ما تنقضه الأدلة.", "skill_ko_ref": "KO-RS-05-002", "observable_behaviors_ar": ["يضيف فرضيات", "يستبعد بدليل"], "evidence_sources": ["hypothesis_ledger"]},
    {"id": "lo_diag", "statement_ar": "يقدّر ما يثبته كل حقل زمني وما لا يثبته، ويربط الدليل بالفرضية باتجاه صحيح.", "skill_ko_ref": "KO-RS-06-001", "observable_behaviors_ar": ["يميز created وsent وnotified", "يربط الدليل بالفرضية"], "evidence_sources": ["evidence_board", "final_justification"]},
    {"id": "lo_calib", "statement_ar": "يصوغ نسبة الترجيح بحدودها.", "skill_ko_ref": "KO-RS-06-021", "observable_behaviors_ar": ["يختار ثقة معقولة", "يذكر حدوداً"], "evidence_sources": ["final_justification"]},
    {"id": "lo_revise", "statement_ar": "يراجع رأيه الأول حين يظهر ما يخالفه.", "skill_ko_ref": "KO-RS-06-009", "observable_behaviors_ar": ["يغيّر فرضيته الرائدة بدليل"], "evidence_sources": ["hypothesis_ledger"]},
]
def levels(d): return [{"score": i, "descriptor_ar": t} for i, t in enumerate(d)]
rub = {
    "reference_answer_ar": "لا دليل على أن ليلى عرفت النتيجة قبل كتابتها. التاريخ 14:45 في قائمتها هو وقت إنشاء مسودة فيها عنوان بلا نتيجة، وليس وقت وصول الرسالة. النسخة النهائية حُفظت 15:07 UTC، والإرسال 15:10 UTC، وإشعارا هاتف ليلى (18:10 بتوقيت UTC+3) وحاسوب ريان (17:11 بتوقيت UTC+2) يقعان بعد التحويل عند 15:10 و15:11 UTC. فالأرقام لم تتضارب، بل كانت بمناطق زمنية وحقول مختلفة المعنى. حدود الاستنتاج: لا تنفي الأدلة وجود قناة أخرى خارج البوابة، ولقطات الشاشة تصف أجهزة بعينها، ولا نعرف لماذا فُتحت المسودة قبل الاعتماد.",
    "criteria": [
        {"id": "c_source", "name_ar": "تصنيف المصادر", "objective_ids": ["lo_claim"], "scored_by": "deterministic", "weight": 0.15, "levels": levels(["لم يصنّف", "أخطأ في الأغلب", "نصف صحيح", "معظمه صحيح", "كله صحيح"])},
        {"id": "c_conflict", "name_ar": "توحيد الأزمنة وترتيبها", "objective_ids": ["lo_timeline"], "scored_by": "deterministic", "weight": 0.25, "levels": levels(["لم يوحّد شيئاً", "وحّد قليلاً", "وحّد نصفها", "معظمها", "كلها في موضعها"])},
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
    H("hg1", 1, "metacognitive", "أين ينتهي ما شاهده الشخص وتبدأ طريقته في تفسيره؟", {"always": True}, None, 0.02),
    H("hg2", 2, "focus_area", "ضع كل معلومة في جدول: هل هي سجل أصلي، أم نسخة معروضة، أم تعليق؟", he("ev_phone_screen"), None, 0.04),
    H("hg3", 3, "pointer", "راجع تحديداً الدليل الذي يوضح معنى كل تاريخ في البوابة قبل أن تقارن بين الأرقام.", he("ev_phone_screen"), None, 0.08),
    H("ht1", 1, "metacognitive", "هل الوقت الذي تراه مكتوب بالمرجع نفسه الذي في الخادم؟", he("ev_laptop_screen"), "i_b_after", 0.02),
    H("ht2", 2, "pointer", "حوّل كل وقت محلي إلى UTC بطرح الإزاحة المذكورة في اللقطة، ثم قارنه بوقت الاعتماد.", he("ev_laptop_screen"), "i_b_after", 0.06),
    H("ht3", 3, "partial_reveal", "استعمل مختبر الأزمنة بإزاحة +3 للهاتف و+2 للحاسوب، وسترى أين يلتقيان.", he("ev_laptop_screen"), "i_b_after", 0.1),
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
Act("a_read_server", "examine", "اطلب سجل إرسال البوابة", al, [G("ev_server_log")], "loc_portal", "READ_SERVER")
Act("a_read_notice", "examine", "اقرأ إعلان النتيجة المنشور", al, [G("ev_published_notice")], "loc_office", "READ_NOTICE")
for cid, lab in [("layla", "ليلى"), ("rayan", "ريان"), ("faris", "فارس")]:
    Act(f"a_int_{cid}", "interview", f"ابدأ مقابلة {lab}", al, [{"op": "raise_trust", "ref_id": cid, "amount": 1}], cid, f"INT_{cid.upper()}")
Act("a_int_hind", "interview", "ابدأ مقابلة هند", al, [{"op": "raise_trust", "ref_id": "hind", "amount": 1}], "hind", "INT_HIND")
Act("a_get_phone", "examine", "اطلب لقطة شاشة هاتف ليلى", fu("f_notified"), [G("ev_phone_screen")], "loc_home", "GET_PHONE")
Act("a_get_inbox", "examine", "اطلب لقطة قائمة رسائل ليلى", fu("f_layla_inbox"), [G("ev_inbox_screen")], "loc_home", "GET_INBOX")
Act("a_get_laptop", "examine", "اطلب لقطة شاشة حاسوب ريان", fu("f_rayan_notified"), [G("ev_laptop_screen")], "loc_camp", "GET_LAPTOP")
Act("a_get_draft", "examine", "اطلب سجل النسخ الآلية للمحرر", fu("f_autosave_exists"), [G("ev_draft_history")], "loc_portal", "GET_DRAFT")
Act("a_get_guide", "examine", "اقرأ دليل حقول البوابة", fu("f_guide_exists"), [G("ev_system_ref")], "loc_portal", "GET_GUIDE")
Act("a_get_approval", "examine", "اطلب رسالة اعتماد النتيجة", fu("f_approval_exists"), [G("ev_approval_email")], "loc_office", "GET_APPROVAL")
Act("a_note_layla", "examine", "دوّن إفادة ليلى", fu("f_notified"), [G("ev_layla_statement")], "layla", "NOTE_LAYLA")
Act("a_note_rayan", "examine", "دوّن إفادة ريان", fu("f_rayan_notified"), [G("ev_rayan_statement")], "rayan", "NOTE_RAYAN")
Act("a_note_faris", "examine", "دوّن إفادة فارس", fu("f_list_date_created"), [G("ev_faris_statement")], "faris", "NOTE_FARIS")
Act("a_note_hind", "examine", "دوّن إفادة هند", fu("f_draft_created"), [G("ev_hind_statement")], "hind", "NOTE_HIND")
Act("a_compare_times", "compare_evidence", "وحِّد الأزمنة (يُمنح عبر المختبر عند نجاحه)", {"all": [he("ev_phone_screen"), he("ev_laptop_screen")]}, [G("ev_lab_norm")], None, "COMPARE_TIMES")
Act("p_inbox_hind", "present_evidence", "اعرض قائمة رسائل ليلى على هند", {"presented": {"evidence_id": "ev_inbox_screen", "to_character": "hind"}}, [{"op": "emit_event", "ref_id": "PRESENTED_INBOX"}], "hind", "P_INBOX_HIND", 0)
Act("a_hint", "request_hint", "اطلب تلميحاً", al, [], None, "REQUEST_HINT", 0)
Act("a_accuse", "final_accusation", "قدّم الاستنتاج النهائي", al, [{"op": "emit_event", "ref_id": "SUBMIT"}], None, "FINAL_ACCUSATION", 0)

topics = [
    {"id": "t_notice", "label_ar": "إشعار الرسالة", "example_questions_ar": ["متى ظهر الإشعار عندك؟", "بأي توقيت يعمل جهازك؟"], "fact_ids": ["f_notified", "f_rayan_notified"], "claim_ids": ["cl_layla_late"]},
    {"id": "t_inbox", "label_ar": "التاريخ في قائمة الرسائل", "example_questions_ar": ["ماذا رأيت في قائمة الرسائل؟", "لماذا يظن البعض أن الرسالة وصلت مبكراً؟"], "fact_ids": ["f_layla_inbox", "f_list_date_created"], "claim_ids": ["cl_rayan_early"]},
    {"id": "t_system", "label_ar": "حقول البوابة وسجلاتها", "example_questions_ar": ["متى أُرسلت الرسالة؟", "هل يحتفظ النظام بنسخ المسودات؟", "هل يوجد دليل لمعاني الحقول؟"], "fact_ids": ["f_sent", "f_autosave_exists", "f_guide_exists"]},
    {"id": "t_approval", "label_ar": "اعتماد النص النهائي", "example_questions_ar": ["متى اعتُمدت النتيجة؟", "هل بقي أثر للاعتماد؟"], "fact_ids": ["f_final_approved", "f_approval_exists"]},
    {"id": "t_draft", "label_ar": "المسودة الأولى", "example_questions_ar": ["ماذا فعلتِ في المحرر قبل الاعتماد؟"], "fact_ids": ["f_draft_created"]},
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
    (1, "أرقام الإشعارات مكتوبة بتوقيتين محليين مختلفين (+3 و+2): بعد التحويل إلى UTC يتقاربان عند 15:10 و15:11، فلا تأخير بثلاث ساعات.", ["ev_phone_screen", "ev_laptop_screen", "ev_lab_norm", "ev_system_ref"], "i_layla_claim"),
    (2, "الخادم يضع الإرسال 15:10 UTC والنسخة النهائية حُفظت 15:07 UTC؛ فالرسالة بنصها أُرسلت بعد اكتماله.", ["ev_server_log", "ev_published_notice"], "i_a_after"),
    (3, "المسار المستقل: الإشعاران الموحَّدان واعتماد رئيسة اللجنة 15:07 يعطيان الترتيب نفسه دون الاعتماد على سجل الخادم.", ["ev_lab_norm", "ev_approval_email"], "i_b_after"),
    (4, "التاريخ 14:45 في قائمة ليلى يغذّيه الحقل created_at، ووقت إنشاء المسودة الأولى، وهي بلا نتيجة.", ["ev_inbox_screen", "ev_system_ref", "ev_draft_history", "ev_faris_statement"], "i_a_date"),
    (5, "ريان انتقل من تسمية حقل إلى واقعة لم تحدث: لا يدل التاريخ المبكر على إبلاغ مسبق.", ["ev_draft_history", "ev_server_log"], "i_rule_leak"),
    (6, "الأزمنة لم تكن عديمة القيمة؛ حين وُحّدت تطابقت سجلات مستقلة، وبقي الخطأ في قراءتنا لها.", ["ev_lab_norm"], "i_rule_untrust_lab"),
]
ending = {
    "steps": [{"order": o, "text_ar": t, "uses_evidence_ids": u, "inference_id": i} for o, t, u, i in steps],
    "alternative_paths_ar": [
        "يمكن الوصول إلى النتيجة من سجل الخادم ووثيقة الإعلان دون مختبر الأزمنة، لكن من يفعل ذلك يترك أرقام الإشعارات بلا تفسير ويضعف حجته أمام من يستشهد بها.",
        "ويمكن الوصول إليها من الإشعارين الموحَّدين واعتماد اللجنة وحدهما، دون الرجوع إلى سجل الخادم؛ والأقوى أن يتفق المساران.",
    ],
    "what_evidence_could_not_show_ar": [
        "لا تنفي الأدلة وجود قناة أخرى (مكالمة أو رسالة خارج البوابة) نقلت النتيجة قبل 15:07؛ هي تنفي هذه الرسالة فقط.",
        "لقطات الشاشة تصف جهازين بعينهما ولا تثبت صحة ضبط ساعتيهما.",
        "لا تبيّن الأدلة لماذا فتحت المحررة المسودة قبل الاعتماد.",
    ],
    "science_notes_ar": [
        "توحيد الأزمنة: لا تُقارن أزمنة قبل أن يُعرف مرجع كل منها (UTC أم توقيت محلي) وما يعنيه الحقل الذي كُتبت فيه.",
        "created وsent وnotified قياسات لثلاث لحظات مختلفة؛ سمّها بأسمائها قبل أن تقارنها.",
        "يبقى ما نسميه نسبة الترجيح حكماً مبنياً على سجلات يمكن تتبّعها (سلسلة العهدة)، لا ثقة بمجرد أن الرقم مكتوب.",
    ],
}
core = {
    "schema_version": "0.1.0", "case_id": CID, "case_version": "0.1.0",
    "meta": {"title_ar": "رسالة وصلت مبكراً", "title_en": "The Message That Arrived Early", "age_band": "16-18", "locale": "ar", "dialogue_register": "msa", "estimated_minutes": 25, "difficulty": 2,
             "content_flags": ["no_violence", "science_lab"], "authors": ["فريق أثر التحريري (مسودة بمساعدة الذكاء الاصطناعي، لم تُراجَع بشرياً بعد)"],
             "knowledge_object_refs": ["KO-RS-05-001", "KO-RS-05-005", "KO-RS-05-002", "KO-RS-06-001", "KO-RS-06-009", "KO-RS-06-021", "KO-FC-04-024"]},
    "premise": {"hook_ar": "أربعة طلاب تلقّوا الإعلان نفسه، لكن كل واحد يذكر وقتاً مختلفاً. ويزعم واحد منهم أن الرسالة سبقت كتابة النتيجة.",
                "player_role_ar": "أنت مراجع في لجنة مسابقة المقال العلمي، وطُلب منك أن تحسم هل وصلت رسالة النتيجة قبل أن تُكتب.",
                "setting_ar": "ثانوية الأفق، عصر يوم الخميس. سجلات الخادم بالتوقيت العالمي UTC، أما الأجهزة فتعرض توقيتها المحلي.",
                "public_fact_ids": ["f_result_published", "f_rayan_alleges", "f_layla_confused"],
                "assumed_general_knowledge_ar": ["التوقيت المحلي = UTC + الإزاحة", "تسمية الحقل في الشاشة قد لا تطابق الحقل الذي يغذّيها"]},
    "entities": {"characters": chars, "locations": locations, "objects": objects, "organizations": orgs},
    "truth": {"solution": {"culprit_ids": ["hind"], "summary_ar": "لم تصل الرسالة قبل كتابة النتيجة. فتحت المحررة مسودة بعنوان فقط مبكراً فتولّد تاريخ 14:45 الذي عرضته القائمة، أما النص النهائي فحُفظ 15:07 وأُرسل 15:10، وإشعارات الأجهزة كانت بتوقيتات محلية مختلفة. لا إبلاغ مسبق ولا تلاعب.", "key_fact_ids": ["f_after_final", "f_date_is_draft"]},
              "facts": facts, "claims": claims},
    "timeline": timeline, "evidence": ev, "evidence_graph": {"inferences": inf},
    "character_knowledge": ck, "hypotheses": hyps, "misdirection_plan": mis, "learning_objectives": los,
    "mechanics": {"time_budget_units": 40, "actions": A},
    "state_machine": {"id": "c008", "initial": "briefing", "type": "compound", "states": {
        "briefing": {"description_ar": "الإحاطة", "type": "atomic", "on": {"START": {"target": "investigating"}}},
        "investigating": {"description_ar": "التحقيق", "type": "compound", "initial": "gathering",
                          "states": {"gathering": {"type": "atomic", "on": {"OPEN_DEDUCTION": {"target": "deducing"}}}, "deducing": {"type": "atomic", "on": {"BACK": {"target": "gathering"}}}},
                          "on": {"SUBMIT": {"target": "review"}}},
        "review": {"description_ar": "مراجعة", "type": "atomic", "on": {"CLOSE": {"target": "resolved"}}},
        "resolved": {"description_ar": "إغلاق", "type": "final"}}},
    "dialogue": {"max_turns_per_interview": 10, "llm_enabled": False, "topics": topics},
    "rubric": rub, "hint_ladder": hints,
    "fairness_test": {"requirements": {"min_disjoint_proof_paths": 2, "max_inference_depth": 3, "all_red_herrings_refutable": True, "culprit_uniquely_entailed": True, "no_hidden_fact_dependency": True, "max_required_actions": 40}, "runs": []},
    "ending_explanation": ending,
    "expert_review": [{"role": r, "reviewer": "—", "status": "pending", "content_hash": "unbound", "date": "2026-10-27", "notes_ar": "بانتظار مراجعة بشرية؛ لم يُجرَ أي اعتماد."} for r in
                      ["narrative_editor", "scientific_reviewer", "learning_designer", "age_appropriateness", "cultural_reviewer", "legal_rights", "safety"]],
}
ui = {
    "case_id": CID,
    "clock": {"epoch_hhmm": "14:00", "zone_label_ar": "التوقيت العالمي UTC"},
    "cover": {"title_ar": "رسالة وصلت مبكراً", "tagline_ar": "أربعة طلاب، ثلاثة أوقات، ورسالة يقال إنها سبقت كاتبتها", "kicker_ar": "الملف الثامن · منطق زمني", "glyph": "◷", "accent": "green"},
    "cold_open_ar": ["الخميس، بعد الثالثة بقليل.", "أُعلنت نتيجة مسابقة المقال العلمي عبر بوابة المدرسة، وتلقّى الطلاب إشعاراً واحداً.",
                     "بعد دقائق وصلك اعتراض: «رسالة ليلى تاريخها قبل أن تُكتب النتيجة».",
                     "أمامك سجلات بتوقيتات مختلفة وأسماء حقول لا تعرف بعد ماذا تقيس. ابدأ بأن تسأل: ماذا يعني كل رقم؟"],
    "labs": [{
        "id": "lab_zone", "type": "time_normalizer", "title_ar": "مختبر توحيد الأزمنة",
        "intro_ar": "لكل جهاز وقت مكتوب بمنطقة زمنية مختلفة. أدخل لكل جهاز الإزاحة عن UTC بالساعات (التوقيت المحلي = UTC + الإزاحة)، وانحراف الساعة بالدقائق إن عُرف. حين تتطابق الأزمنة ضمن دقيقتين يصدر التقرير.",
        "tolerance_min": 2, "epoch_utc_minute_of_day": 840, "day_labels_ar": ["يوم الإعلان"],
        "grants_evidence_on_converge": "ev_lab_norm",
        "items": [
            {"evidence_id": "ev_phone_screen", "label_ar": "هاتف ليلى — ظهور الإشعار", "day": 0, "hhmm": "18:10", "basis_ar": "اللقطة تذكر المنطقة الزمنية للهاتف"},
            {"evidence_id": "ev_laptop_screen", "label_ar": "حاسوب ريان — ظهور الإشعار", "day": 0, "hhmm": "17:11", "basis_ar": "اللقطة تذكر المنطقة الزمنية للحاسوب"},
        ],
    }],
    "source_classes": [
        {"id": "primary_record", "label_ar": "سجل أصلي", "help_ar": "يُنتجه نظام أو شخص لحظة الحدث دون وسيط، كسجل خادم أو سجل نسخ."},
        {"id": "redisplay", "label_ar": "نسخة معروضة", "help_ar": "معلومة أُعيد عرضها على شاشة جهاز أو في لقطة، فتتأثر بتوقيت الجهاز وتسمية العرض."},
        {"id": "claim", "label_ar": "قول أو تصريح", "help_ar": "إفادة شخص؛ تُقاس بالسجلات وبتعريف الحقول لا بنبرة صاحبها."},
        {"id": "template", "label_ar": "قالب أو نموذج", "help_ar": "نص جاهز لا يصف الحدث الفعلي بذاته."},
        {"id": "public_document", "label_ar": "وثيقة منشورة", "help_ar": "وثيقة معلنة ومعروف ناشرها، كإعلان أو دليل مستخدم."}],
    "limit_menu": [
        {"id": "l_other_channel", "label_ar": "الأدلة تنفي وصول هذه الرسالة مبكراً، ولا تنفي وجود قناة أخرى نقلت النتيجة قبل اعتمادها"},
        {"id": "l_device_clock", "label_ar": "لقطات الشاشة تصف جهازين بعينهما ولا تثبت صحة ضبط ساعتيهما"},
        {"id": "l_why_draft", "label_ar": "لا تبيّن الأدلة لماذا فُتحت المسودة قبل الاعتماد"},
        {"id": "l_invalid_diff", "label_ar": "اختلاف الأرقام بين السجلات يثبت أن أحدها مزوَّر"},
        {"id": "l_invalid_insist", "label_ar": "إلحاح ريان في اتهامه يدل على أنه محق"}],
    "mind_change_menu": [
        {"id": "m_other_msg", "label_ar": "ظهور رسالة أخرى فيها النتيجة أُرسلت قبل 15:07 UTC"},
        {"id": "m_server_edit", "label_ar": "ثبوت أن سجل الخادم عُدّل بعد الإرسال"},
        {"id": "m_guide_wrong", "label_ar": "ثبوت أن دليل الحقول لا يطابق ما يفعله النظام فعلاً"},
        {"id": "m_popular", "label_ar": "كثرة الطلاب الذين يصدقون رواية ريان"}],
    "transfer": {
        "id": "tr_ferry", "title_ar": "اختبار نقل المهارة: تذكرة العبّارة",
        "scenario_ar": "قال مسافر إن عبّارته وصلت الميناء قبل موعد إقلاعها. أمامك وثيقتان من واقعة خيالية لا علاقة لها بالقضية.",
        "documents": [
            {"title_ar": "تذكرة المسافر", "body_ar": "وقت الإقلاع المطبوع: 23:50 (التوقيت المحلي للميناء الشمالي، UTC-5). الصعود حتى 23:20."},
            {"title_ar": "سجل مراقبة الميناء", "body_ar": "وصول العبّارة إلى الرصيف: 04:35 UTC. ملاحظة: السجل يُعرض بالتوقيت العالمي دون ذكر اليوم."}],
        "prompt_ar": "اختر الخطوات التي تصلح لتحديد هل وصلت العبّارة قبل موعد إقلاعها (يمكنك اختيار أكثر من خطوة).",
        "options": [
            {"id": "o1", "text_ar": "تحويل الوقتين إلى مرجع واحد قبل المقارنة"},
            {"id": "o2", "text_ar": "التأكد من اليوم الذي يخصه كل وقت"},
            {"id": "o3", "text_ar": "معرفة ما يقيسه كل حقل: وقت إقلاع مطبوع أم وقت وصول مسجَّل"},
            {"id": "o4", "text_ar": "طلب سجل ثالث مستقل لتأكيد وقت الوصول"},
            {"id": "o5", "text_ar": "مقارنة الرقمين 23:50 و04:35 كما هما"},
            {"id": "o6", "text_ar": "الحكم بحسب ثقة المسافر في روايته"},
            {"id": "o7", "text_ar": "اعتبار السجلات كلها باطلة لأن أرقامها لا تتفق"}],
        "free_text_prompt_ar": "اكتب في ثلاثة أسطر كيف تقرّر نسبة الترجيح بأن العبّارة وصلت قبل موعد إقلاعها.",
    },
    "skills": [{"skill_id": "KO-RS-05-001", "track": "B"}, {"skill_id": "KO-RS-05-005", "track": "B"}, {"skill_id": "KO-RS-05-002", "track": "D"}, {"skill_id": "KO-FC-04-024", "track": "E"}],
    "stage_hooks_ar": {"briefing": "رسالة بتاريخ لا يتفق مع كاتبتها… فمن أخطأ؟", "investigating": "كل رقم يحمل توقيته وتسميته؛ اقرأهما معاً.", "review": "قبل أن تغلق الملف: ما الذي لا تعرفه؟", "resolved": "أُغلق الملف. في الأرشيف مخطوطة لم تُفتح بعد."},
    "character_glyphs": {"layla": "ل", "rayan": "ر", "faris": "ف", "hind": "هـ"},
}
sc = {
    "case_id": CID,
    "accepted_conclusions": {"h_display": {"grade": 1, "note_ar": "استنتاج متسق مع الأدلة ويتطلب ذكر حدوده."},
                             "h_leak": {"grade": 0, "note_ar": "يقرأ تسمية الحقل على أنها وقت الوصول، ويتجاهل أن المسودة الأولى كانت بلا نتيجة."},
                             "h_untrust": {"grade": 0, "note_ar": "الاختلاف ظاهري ويزول بتوحيد المرجع الزمني؛ لا يعني بطلان السجلات."}},
    "confidence_band": {"h_display": [65, 92], "h_leak": [0, 15], "h_untrust": [0, 15]},
    "source_key": {"ev_server_log": "primary_record", "ev_published_notice": "public_document", "ev_phone_screen": "redisplay", "ev_laptop_screen": "redisplay", "ev_inbox_screen": "redisplay",
                   "ev_draft_history": "primary_record", "ev_system_ref": "public_document", "ev_approval_email": "primary_record",
                   "ev_faris_statement": "claim", "ev_layla_statement": "claim", "ev_rayan_statement": "claim", "ev_hind_statement": "claim"},
    "link_key": {
        "h_display": {"ev_server_log": "supports", "ev_published_notice": "supports", "ev_draft_history": "supports", "ev_system_ref": "supports", "ev_approval_email": "supports", "ev_lab_norm": "supports", "ev_faris_statement": "supports", "ev_inbox_screen": "supports", "ev_phone_screen": "neutral"},
        "h_leak": {"ev_inbox_screen": "supports", "ev_draft_history": "weakens", "ev_published_notice": "weakens", "ev_server_log": "weakens", "ev_approval_email": "weakens", "ev_lab_norm": "weakens", "ev_rayan_statement": "neutral"},
        "h_untrust": {"ev_phone_screen": "supports", "ev_lab_norm": "weakens", "ev_server_log": "weakens", "ev_system_ref": "weakens"},
    },
    "required_limits": ["l_other_channel", "l_device_clock"], "valid_mind_changers": ["m_other_msg", "m_server_edit", "m_guide_wrong"],
    "invalid_limits": ["l_invalid_diff", "l_invalid_insist"],
    "decisive_evidence": ["ev_server_log", "ev_published_notice", "ev_system_ref", "ev_draft_history", "ev_lab_norm"],
    "lab_requirement": {"lab_id": "lab_zone", "must_converge": True},
    "timeline_requirement": [{"evidence_id": "ev_draft_history", "utc_minute": 45, "tol": 3}, {"evidence_id": "ev_published_notice", "utc_minute": 67, "tol": 3},
                             {"evidence_id": "ev_server_log", "utc_minute": 70, "tol": 3}, {"evidence_id": "ev_phone_screen", "utc_minute": 70, "tol": 3}],
    "refuted_hypotheses": ["h_leak", "h_untrust"],
    "criteria_map": {"c_source": "source_typing", "c_conflict": "conflict_resolution", "c_links": "hypothesis_links", "c_uncertainty": "uncertainty", "c_revision": "revision", "c_elimination": "elimination", "c_justification": "justification_human"},
    "transfer_key": {"valid": ["o1", "o2", "o3", "o4"], "invalid": ["o5", "o6", "o7"]},
    "caps": {"no_citations_max": 45, "no_conflict_resolution_max": 65},
}
os.makedirs(OUT, exist_ok=True)
for suf, obj in [("", core), (".ui", ui), (".scoring", sc)]:
    with open(os.path.join(OUT, f"{CID}{suf}.json"), "w", encoding="utf8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
print("ok")
