#!/usr/bin/env python3
# Case c003 «رسالة من الغد» — time-zone / display-time case with the time-normaliser lab.
# Teaches: convert every time to one reference before comparing, separate event time from display time, and know the limits of a
# shortened summary. No-culprit convention: the participant whose shortened summary dropped the zones is recorded as culprit_ids.
# Usage: gen_c003.py OUT_DIR
import json, sys, os
OUT = sys.argv[1]
CID = "c003_letter_from_tomorrow"
# Timeline epoch t=0 is Thursday 20:00 UTC. The message is created Thursday 23:58 at UTC-2 = Friday 01:58 UTC = minute 358.

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

ch("nora", "نورة العبدالله", "victim", "صحفية علمية على متن سفينة أبحاث، في أواخر الثلاثينات",
   "هادئة وعملية، تكتب أوقاتها بساعة السفينة وتتوقع أن يفهم القارئ ذلك، وتنزعج حين تُنسب إليها رسالة لم تقصدها.",
   ["أن تصل خلاصة قراءاتها إلى غرفة الأخبار", "ألا تُتّهم بأنها تلاعبت بالوقت"],
   [L("nr_greet", "greeting", "أهلاً. كتبتُ الرسالة مساءً على متن السفينة، ولم أتوقع أن تثير كل هذا."),
    L("nr_zone", "reveal", "ساعة السفينة مضبوطة على منطقة زمنية تتأخر ساعتين عن التوقيت العالمي، وأكتب أوقاتي بها دائماً.", ["f_ship_zone"]),
    L("nr_sent", "reveal", "أرسلتُ الرسالة قبل منتصف الليل بدقيقتين بحسب ساعة السفينة، ورأس الملف يسجّل ذلك.", ["f_nora_sent"]),
    L("nr_unknown", "deflect_unknown", "ليس لدي دليل يدعم ذلك."),
    L("nr_off", "deflect_offtopic", "اسألني عن رسالتي وساعة السفينة فقط."),
    L("nr_bye", "farewell", "أرجو أن تقرأ السجلات قبل الشائعات.")],
   ["اتهام أحد بالاختراق دون سند"])
ch("walid", "وليد البدر", "expert", "مسؤول نظم المراسلات في المركز",
   "دقيق ويفضّل أن يعرض السجل على أن يفسّره، ولا يتحدث عمّا لم يفحصه.",
   ["أن تبقى سجلات النظام سليمة وقابلة للتدقيق"],
   [L("wl_greet", "greeting", "أهلاً. أجيب عمّا في سجلات الخادم، لا عن النوايا."),
    L("wl_utc", "reveal", "الخادم يخزّن كل وقت بالتوقيت العالمي، ثم تعرضه الأجهزة بحسب منطقة صاحبها.", ["f_server_utc"]),
    L("wl_log", "reveal", "سجل الاستلام عندي، ويمكنني إخراج السطر الخاص بالرسالة.", ["f_server_log_exists"]),
    L("wl_net", "reveal", "أجرينا قياساً تجريبياً لزمن النقل من السفينة إلى الخادم، ونتيجته متاحة.", ["f_net_tested"]),
    L("wl_trace", "reveal", "إن أردت المصدر الكامل فسجل التسليم يغطي كل خطوة من الإنشاء إلى الوصول، وأستطيع تصديره.", ["f_trace_exists"]),
    L("wl_job", "reveal", "وتُسجَّل أيضاً المهام الليلية المجدولة، فاطلبها إن أردت.", ["f_job_exists"]),
    L("wl_unknown", "deflect_unknown", "ليس لدي دليل يدعم ذلك."),
    L("wl_off", "deflect_offtopic", "فلنعد إلى سجلات النظام."),
    L("wl_bye", "farewell", "السجلات متاحة متى احتجتها.")])
ch("rima", "ريما الشريف", "witness", "محررة في غرفة الأخبار، في أوائل الثلاثينات",
   "سريعة الانطباع وصادقة، تكتب ما رأته كما رأته وتتردد في التدقيق حين يتفق الرقمان مع انطباعها.",
   ["أن تعرف إن كانت الرسالة حقيقية قبل أن تنشر شيئاً"],
   [L("rm_greet", "greeting", "أهلاً. رأيتُ ما رأيته، وأريد أن أفهمه."),
    L("rm_tomorrow", "reveal", "فتحتُ الوارد فوجدتُ وقت الرسالة 23:58 وساعة جهازي تقول 04:59، فظننتها من الغد.", ["f_rima_saw"], ["cl_rima_tomorrow"]),
    L("rm_summary", "reveal", "وصلني بعد الاجتماع ملخص أعاد أحدهم إرساله، وفيه الوقتان كما رأيتهما.", ["f_summary_circulates"]),
    L("rm_unknown", "deflect_unknown", "ليس لدي دليل يدعم ذلك."),
    L("rm_off", "deflect_offtopic", "اسألني عمّا رأيته في الوارد."),
    L("rm_bye", "farewell", "شكراً لأنك تسأل قبل أن تحكم.")])
ch("karim", "كريم الحداد", "suspect", "أمين محضر اجتماع الصباح في غرفة الأخبار",
   "مستعجل ويحب الإيجاز، ويقلّل مما اختصره حين يشعر أنه قد يُلام.",
   ["ألا يُنسب إليه سبب الشائعة", "أن يبقى ملخصه وسيلة للتواصل السريع"],
   [L("kr_greet", "greeting", "تفضّل. كتبتُ المحضر، وأرسلتُ ملخصاً قصيراً بعده."),
    L("kr_minutes", "reveal", "المحضر الأصلي محفوظ في مجلد الاجتماع، ويمكنك الاطلاع عليه.", ["f_minutes_exist"]),
    L("kr_copy", "lie", "نقلتُ الوقتين كما ظهرا في المحضر، دون أي تغيير.", None, ["cl_karim_copy"]),
    L("kr_refuse", "refuse_secret", "لا أرى أن للملخص علاقة بما تسأل."),
    L("kr_break", "break_down", "نعم... اختصرتُ المحضر في سطر واحد، فحذفتُ المنطقتين الزمنيتين وكتبتُ «الخميس» للوقتين. لم أتخيل أن يُفهم منه أن الرسالة سبقت كتابتها.", ["f_summary_zone_dropped"]),
    L("kr_unknown", "deflect_unknown", "ليس لدي دليل يدعم ذلك."),
    L("kr_off", "deflect_offtopic", "اسألني عن المحضر والملخص."),
    L("kr_bye", "farewell", "كان ينبغي أن أترك المنطقتين في السطر.")],
   ["اتهام ريما أو نورة دون سند"])

locations = [{"id": "loc_ship", "name_ar": "سفينة الأبحاث «الندى»", "description_ar": "حيث كُتبت الرسالة، وساعتها مضبوطة على توقيتها."},
             {"id": "loc_server", "name_ar": "غرفة خوادم المراسلات", "description_ar": "سجلات الاستلام والتسليم."},
             {"id": "loc_newsroom", "name_ar": "غرفة الأخبار", "description_ar": "أجهزة المحررين ومجلد الاجتماع."}]
objects = [{"id": "obj_msg", "name_ar": "الرسالة msg-7141", "description_ar": "خلاصة قراءات الليلة المرسلة من السفينة."}]
orgs = [{"id": "org_center", "name_ar": "مركز الشرفة للإعلام العلمي", "description_ar": "مركز خيالي للإعلام العلمي."}]

facts = []
def F(id, st, kind, subj, spoiler, time=None, loc=None, ko=None):
    d = {"id": id, "statement_ar": st, "kind": kind, "subject_ids": subj, "spoiler_level": spoiler}
    if time: d["time"] = time
    if loc: d["location_id"] = loc
    if ko: d["science_ko_refs"] = ko
    facts.append(d)
F("f_msg_looks_early", "تبدو رسالة نورة في الملخص المتداول وكأنها وصلت قبل أن تُكتب بساعات.", "event", ["obj_msg"], 0)
F("f_rumor_breach", "يتداول زملاء في المركز أن النظام اختُرق أو أن الوقت عُبث به.", "attribute", ["org_center"], 0)
F("f_nora_reporting", "نورة صحفية على متن سفينة أبحاث وترسل خلاصاتها إلى غرفة الأخبار.", "attribute", ["nora"], 0)
F("f_header_time", "يسجّل رأس الرسالة وقت الإنشاء الخميس 23:58 بمنطقة UTC-2.", "attribute", ["obj_msg", "nora"], 1, T(358), "loc_ship")
F("f_server_recv", "سجّل الخادم استلام الرسالة الجمعة 01:59 بالتوقيت العالمي.", "event", ["obj_msg"], 1, T(359), "loc_server")
F("f_device_time", "تعرض واجهة جهاز المحرر وصول الرسالة الجمعة 04:59 بمنطقة UTC+3.", "state", ["obj_msg"], 1, T(359), "loc_newsroom")
F("f_summary_text", "أعاد أحد المشاركين إرسال ملخص يضع الوصول والكتابة في يوم واحد دون ذكر منطقة.", "event", ["karim", "obj_msg"], 1, T(750), "loc_newsroom")
F("f_job_run", "شُغّلت مهمة فهرسة مجدولة على الخادم في الجمعة 03:12 بالتوقيت العالمي.", "event", ["loc_server"], 1, T(432), "loc_server")
F("f_ship_zone", "ساعة السفينة مضبوطة على منطقة تتأخر ساعتين عن التوقيت العالمي.", "state", ["nora", "loc_ship"], 1, None, "loc_ship")
F("f_nora_sent", "أرسلت نورة الرسالة قبل منتصف الليل بدقيقتين بساعة السفينة.", "event", ["nora", "obj_msg"], 1, T(358), "loc_ship")
F("f_server_utc", "يخزّن الخادم كل وقت بالتوقيت العالمي وتحوّله الأجهزة إلى منطقة صاحبها.", "state", ["loc_server"], 1, None, "loc_server")
F("f_server_log_exists", "يحتفظ الخادم بسجل استلام لكل رسالة.", "state", ["walid", "loc_server"], 1, None, "loc_server")
F("f_net_tested", "أُجري قياس تجريبي لزمن النقل من السفينة إلى الخادم.", "state", ["walid"], 1, None, "loc_server")
F("f_trace_exists", "يتوفر سجل تسليم كامل يغطي مراحل الرسالة.", "state", ["walid", "loc_server"], 1, None, "loc_server")
F("f_job_exists", "تُسجَّل المهام المجدولة على الخادم.", "state", ["walid", "loc_server"], 1, None, "loc_server")
F("f_rima_saw", "فتحت ريما الوارد فقارنت الوقتين 23:58 و04:59 دون اليوم ودون المنطقة.", "event", ["rima"], 1, T(365, "approx"), "loc_newsroom")
F("f_summary_circulates", "وصل زملاء في غرفة الأخبار ملخص معاد إرساله بعد الاجتماع.", "event", ["rima", "karim"], 1, T(750, "approx"), "loc_newsroom")
F("f_minutes_exist", "محضر الاجتماع الأصلي محفوظ في مجلد الاجتماع.", "state", ["karim", "loc_newsroom"], 1, None, "loc_newsroom")
F("f_one_instant", "الأزمنة الثلاثة المختلفة المكتوبة في الرأس والخادم والجهاز تقيس لحظة واحدة تقريباً، تفصل بينها دقيقة نقل.", "relation", ["obj_msg"], 3, T(358, "approx", 359), None, ["KO-FC-04-024"])
F("f_summary_zone_dropped", "الاختصار الذي أُعيد إرساله أسقط ما يدل على منطقتي الوقتين وجعل اليوم نفسه لهما، فنشأ ترتيب معكوس لا وجود له في الواقع.", "event", ["karim", "obj_msg"], 3, T(750), "loc_newsroom", ["KO-RS-05-014"])
claims = [
    {"id": "cl_rima_tomorrow", "statement_ar": "الرسالة مؤرَّخة بالغد؛ وقتها 23:58 وجهازي يشير إلى 04:59.", "kind": "honest_mistake", "held_by": ["rima"], "true_fact_id": "f_one_instant", "contradicted_by_evidence_ids": ["ev_delivery_trace", "ev_lab_norm"]},
    {"id": "cl_karim_copy", "statement_ar": "نقلت الوقتين كما ظهرا في المحضر دون تغيير.", "kind": "half_truth", "held_by": ["karim"], "true_fact_id": "f_summary_zone_dropped", "contradicted_by_evidence_ids": ["ev_minutes_orig", "ev_device_view"]},
]
timeline = [
    {"id": "te_write", "description_ar": "نورة تنشئ الرسالة على السفينة.", "time": T(358), "location_id": "loc_ship", "actor_ids": ["nora"], "fact_ids": ["f_header_time", "f_nora_sent"], "motivated_by_ar": "أنهت قراءات الليلة وأرادت إبلاغ غرفة الأخبار"},
    {"id": "te_server", "description_ar": "الخادم يقبل الرسالة ويسجّل الاستلام.", "time": T(359), "location_id": "loc_server", "actor_ids": [], "fact_ids": ["f_server_recv"]},
    {"id": "te_device", "description_ar": "الرسالة تظهر في صندوق المحرر بتوقيت غرفة الأخبار.", "time": T(359), "location_id": "loc_newsroom", "actor_ids": [], "fact_ids": ["f_device_time"]},
    {"id": "te_open", "description_ar": "ريما تفتح الوارد وتقرأ الوقتين.", "time": T(365, "approx"), "location_id": "loc_newsroom", "actor_ids": ["rima"], "fact_ids": ["f_rima_saw"], "motivated_by_ar": "بدأت وردية الصباح بمراجعة الوارد"},
    {"id": "te_job", "description_ar": "مهمة فهرسة مجدولة على الخادم.", "time": T(432), "location_id": "loc_server", "actor_ids": [], "fact_ids": ["f_job_run"]},
    {"id": "te_summary", "description_ar": "كريم يرسل ملخصاً مختصراً بعد الاجتماع.", "time": T(750), "location_id": "loc_newsroom", "actor_ids": ["karim"], "fact_ids": ["f_summary_text", "f_summary_zone_dropped", "f_summary_circulates"], "motivated_by_ar": "أراد إيصال الخلاصة بسرعة"},
]

ev = []
def V(id, title, kind, content, acts, supports, rel, limits, contradicts=None, red=False, ko=None, loc=None):
    d = {"id": id, "title_ar": title, "kind": kind, "content_ar": content, "acquired_by_action_ids": acts, "supports_fact_ids": supports, "reliability": rel, "limits_ar": limits}
    if contradicts: d["contradicts_claim_ids"] = contradicts
    if red: d["is_red_herring"] = True
    if ko: d["forensic_ko_ref"] = ko
    if loc: d["location_id"] = loc
    ev.append(d)
V("ev_header", "رأس الرسالة msg-7141", "digital",
  "رأس الرسالة (مبسّط)\nالمعرّف: msg-7141\nمن: نورة العبدالله — سفينة الأبحاث «الندى»\nإلى: غرفة الأخبار\nأُنشئت: الخميس 23:58 (UTC-2)\nالموضوع: خلاصة قراءات الليلة",
  ["a_read_header"], ["f_header_time"], "strong", "يثبت وقت الإنشاء بتوقيت جهاز المرسلة ومنطقته؛ لا يثبت متى وصلت الرسالة ولا كيف عُرض وقتها لدى غيرها.", loc="loc_ship")
V("ev_device_view", "واجهة بريد جهاز المحرر", "digital",
  "واجهة بريد جهاز المحرر في غرفة الأخبار:\nmsg-7141 — وصلت: الجمعة 04:59 (UTC+3)",
  ["a_read_device"], ["f_device_time", "f_msg_looks_early"], "moderate", "تعرض الوقت بمنطقة جهاز المستلم؛ ليست وقت الحدث نفسه بل صورة له.", loc="loc_newsroom")
V("ev_server_log", "سجل استلام خادم المراسلات", "digital",
  "سجل خادم المراسلات — الأوقات مخزّنة بالتوقيت العالمي UTC\nmsg-7141 | الاستلام: الجمعة 01:59 UTC | الحالة: مقبولة | تعديل لاحق: لا يوجد",
  ["a_get_server"], ["f_server_recv"], "strong", "يثبت وقت قبول الخادم للرسالة بمرجع واحد؛ لا يثبت وقت كتابتها ولا ما عُرض على الأجهزة.", loc="loc_server")
V("ev_summary", "ملخص أُعيد إرساله بعد الاجتماع", "digital",
  "رسالة أعاد أحد المشاركين إرسالها بعد اجتماع الصباح:\n«وصلت رسالة نورة الخميس 04:59، وكتبتها الخميس 23:58.»",
  ["a_get_summary"], ["f_summary_text", "f_summary_circulates"], "weak", "نسخة مختصرة أُعيد إرسالها؛ لا تذكر منطقة أي وقت، فلا تثبت ترتيب الحدثين وحدها.", red=True, loc="loc_newsroom")
V("ev_network_info", "قياس زمن النقل التجريبي", "digital",
  "قياس شبكة تجريبي بين سفينة الأبحاث وخادم المراسلات:\nزمن النقل المعتاد نحو دقيقة واحدة (متوسط عشر رسائل اختبار: 58 ثانية).",
  ["a_get_net"], ["f_net_tested"], "moderate", "بيانات اختبار لرسائل أخرى؛ تقدّر الزمن الاعتيادي ولا تقيس هذه الرسالة بعينها.", loc="loc_server")
V("ev_rima_comment", "تعليق ريما", "testimonial",
  "ريما الشريف، محررة:\n«فتحت الوارد فرأيت أن وقت الرسالة 23:58 وساعة جهازي تقول 04:59. يعني وصلت من الغد!»",
  ["a_note_rima"], ["f_rima_saw"], "weak", "انطباع شخص قارن رقمين دون يومهما ودون منطقتيهما؛ لا يثبت ترتيب الحدثين.", red=True, loc="loc_newsroom")
V("ev_delivery_trace", "سجل التسليم الكامل", "digital",
  "سجل التسليم الكامل للرسالة msg-7141 — كل الأوقات بالتوقيت العالمي UTC\n01:58:12 إنشاء عند المرسلة\n01:59:10 قبول عند الخادم\n01:59:11 تسليم إلى صندوق المحرر\nيعرض جهاز المحرر الوقت بمنطقته UTC+3.\nعدد الحلقات: 3 — دون فجوات.",
  ["a_get_trace"], ["f_trace_exists", "f_one_instant"], "strong", "يربط خطوات الرسالة بمرجع زمني واحد؛ لا يثبت أن محتوى الرسالة صحيح ولا ما قيل عنها لاحقاً.", contradicts=["cl_rima_tomorrow"], loc="loc_server")
V("ev_minutes_orig", "محضر الاجتماع الأصلي", "documentary",
  "محضر اجتماع الصباح (قبل أن يختصره أحد):\n«وصلت الرسالة الجمعة 04:59 بتوقيت غرفة الأخبار (UTC+3)، وكانت أُنشئت الخميس 23:58 بتوقيت السفينة (UTC-2).»",
  ["a_get_minutes"], ["f_minutes_exist", "f_summary_text"], "strong", "يحفظ اليوم والمنطقة لكل وقت؛ كتبه أمين الاجتماع نقلاً من الشاشتين ولا يعرض سجل الخادم.", contradicts=["cl_karim_copy"], loc="loc_newsroom")
V("ev_karim_statement", "إفادة أمين المحضر (ملخص)", "testimonial",
  "ملخص إفادة كريم الحداد، دوّنه أمين اللجنة:\n«اختصرت المحضر في سطر لأرسله بسرعة. حذفت المنطقتين، وكتبت (الخميس) للوقتين لأنه التاريخ الذي بدأ به المحضر.»",
  ["a_note_karim"], ["f_summary_zone_dropped"], "moderate", "إقرار شخص عن عمله هو؛ يؤيده المحضر، ولا يثبت وحده أن الاختصار هو سبب الشائعة.", loc="loc_newsroom")
V("ev_job_log", "سجل المهام المجدولة", "digital",
  "سجل المهام المجدولة على الخادم:\nالجمعة 03:12 UTC — إعادة بناء فهرس البحث في البريد (أسبوعية، قراءة فقط)",
  ["a_get_job"], ["f_job_run"], "moderate", "يثبت تشغيل مهمة فهرسة بعد الاستلام؛ لا يقول إنها لمست هذه الرسالة أو أوقاتها.", red=True, loc="loc_server")
V("ev_lab_norm", "تقرير توحيد الأزمنة", "lab_result",
  "تقرير مختبر الأزمنة: بعد تحويل كل وقت إلى التوقيت العالمي تتقارب القراءات الثلاث (رأس الرسالة، سجل الخادم، واجهة الجهاز) عند 01:58 و01:59 UTC فجر الجمعة بفارق دقيقة واحدة. أي أن الفارق الظاهر بين «23:58» و«04:59» ناتج عن اختلاف المنطقة الزمنية لا عن اختلاف الحدث.",
  ["a_compare_times"], ["f_one_instant"], "strong", "نتيجة حسابية تعتمد على صحة الإزاحات المدخلة؛ توحّد الأزمنة ولا تثبت وحدها أن الخادم غير معدَّل.", contradicts=["cl_rima_tomorrow"], ko="KO-FC-04-024", loc="loc_server")

def P(t, i): return {"ref_type": t, "ref_id": i}
inf = []
def I(id, prem, ct, concl, rel, strength, rule, ks):
    inf.append({"id": id, "premises": prem, "conclusion": {"ref_type": ct, "ref_id": concl}, "relation": rel, "strength": strength, "rule_ar": rule, "skill_ko_refs": ks})
UTC = P("general_knowledge", "utc_common_reference")
I("i_one_instant_a", [P("evidence", "ev_header"), P("evidence", "ev_server_log"), P("evidence", "ev_device_view"), UTC], "fact", "f_one_instant", "establishes", "conclusive",
  "بتحويل 23:58 (UTC-2) و04:59 (UTC+3) إلى التوقيت العالمي تصبحان 01:58 و01:59، وهما تلتقيان مع سجل الخادم 01:59؛ فالأرقام الثلاثة تصف لحظة واحدة.", ["KO-FC-04-024"])
I("i_one_instant_lab", [P("evidence", "ev_lab_norm")], "fact", "f_one_instant", "establishes", "strong",
  "ناتج المختبر يوحّد الأزمنة الثلاثة في نافذة دقيقة واحدة بعد تحويل الإزاحات.", ["KO-FC-04-024"])
I("i_one_instant_b", [P("evidence", "ev_delivery_trace"), P("evidence", "ev_network_info")], "fact", "f_one_instant", "establishes", "strong",
  "السلسلة الكاملة مكتوبة بمرجع واحد: إنشاء 01:58:12 وقبول 01:59:10؛ وفارق الدقيقة يطابق زمن النقل الاعتيادي في القياس التجريبي.", ["KO-FC-04-024", "KO-RS-05-004"])
I("i_zone_dropped_a", [P("evidence", "ev_summary"), P("evidence", "ev_device_view"), P("evidence", "ev_header")], "fact", "f_summary_zone_dropped", "establishes", "strong",
  "الملخص يكتب 04:59 و23:58 تحت اليوم نفسه، بينما تضعهما الواجهة والرأس في يومين وبمنطقتين؛ فالترتيب المعكوس صنعه الاختصار لا الرسالة.", ["KO-RS-05-014"])
I("i_zone_dropped_b", [P("evidence", "ev_minutes_orig"), P("evidence", "ev_karim_statement")], "fact", "f_summary_zone_dropped", "establishes", "strong",
  "المحضر الأصلي يحفظ المنطقة واليوم لكل وقت، وصاحب الملخص يقرّ بأنه حذفهما وكتب يوماً واحداً؛ فمصدر الالتباس هو الاختصار.", ["KO-RS-05-014"])
I("i_rima_claim", [P("evidence", "ev_header"), P("evidence", "ev_device_view")], "claim", "cl_rima_tomorrow", "contradicts_claim", "strong",
  "الوقتان اللذان قارنتهما ريما من يومين مختلفين وبمنطقتين مختلفتين؛ لا يصحّ مقارنة 23:58 بـ04:59 قبل تحويلهما.", ["KO-RS-05-001"])
I("i_karim_claim", [P("evidence", "ev_minutes_orig"), P("evidence", "ev_summary")], "claim", "cl_karim_copy", "contradicts_claim", "strong",
  "المحضر يحوي اليوم والمنطقة والملخص لا يحويهما؛ فالقول إن الوقتين نُقلا دون تغيير غير دقيق.", ["KO-RS-05-001"])
I("i_rule_breach_a", [P("evidence", "ev_header"), P("evidence", "ev_server_log"), P("evidence", "ev_device_view")], "hypothesis", "h_breach", "rules_out", "strong",
  "بعد توحيد الأزمنة يأتي الإنشاء قبل الاستلام بدقيقة، وسجل الخادم يقول إنه لم يُعدَّل؛ فلا يبقى شيء يحتاج إلى اختراق لتفسيره.", ["KO-RS-06-008"])
I("i_rule_breach_b", [P("evidence", "ev_delivery_trace"), P("evidence", "ev_network_info")], "hypothesis", "h_breach", "rules_out", "strong",
  "السلسلة كاملة بلا فجوات وبمرجع واحد، وفارق خطواتها يطابق زمن النقل المعتاد؛ فلا موضع لتلاعب في الوقت.", ["KO-RS-06-008"])
I("i_job_explained", [P("evidence", "ev_job_log"), P("evidence", "ev_server_log")], "hypothesis", "h_breach", "rules_out", "strong",
  "مهمة الفهرسة قراءة فقط وجرت بعد الاستلام بأكثر من ساعة، وسجل الخادم لا يذكر تعديلاً لاحقاً؛ فلا علاقة لها بوقت الرسالة.", ["KO-RS-06-008"])
I("i_rule_insufficient_a", [P("evidence", "ev_header"), P("evidence", "ev_server_log"), P("evidence", "ev_device_view")], "hypothesis", "h_insufficient", "rules_out", "strong",
  "ثلاثة سجلات أصلية لكل منها منطقته تكفي بعد التحويل لتفسير التسلسل دون انتظار سجل آخر.", ["KO-RS-06-001"])
I("i_rule_insufficient_b", [P("evidence", "ev_delivery_trace")], "hypothesis", "h_insufficient", "rules_out", "strong",
  "سجل التسليم الكامل نفسه يغطي مراحل الرسالة كلها بمرجع واحد، فلا ينقص أصل سجل.", ["KO-RS-06-001"])
I("i_support_zones", [P("fact", "f_one_instant"), P("fact", "f_summary_zone_dropped")], "hypothesis", "h_zones", "supports", "strong",
  "حدث واحد قُرئ بثلاث مناطق زمنية، ثم اختصر ملخص ما يدل على مناطقها؛ وهذا يفسّر كل ما بدا مستحيلاً دون افتراض سفر في الزمن أو اختراق.", ["KO-RS-05-002"])

def K(fid, access, cert="certain", src=None):
    d = {"fact_id": fid, "access": access, "certainty": cert}
    if src: d["source_character_id"] = src
    return d
ck = [
    {"character_id": "nora", "knows": [K("f_ship_zone", "witnessed"), K("f_nora_sent", "witnessed")], "hides": [], "believes": []},
    {"character_id": "walid", "knows": [K("f_server_utc", "professional"), K("f_server_log_exists", "professional"), K("f_net_tested", "professional"), K("f_trace_exists", "professional"), K("f_job_exists", "professional")], "hides": [], "believes": []},
    {"character_id": "rima", "knows": [K("f_rima_saw", "witnessed"), K("f_summary_circulates", "witnessed")], "hides": [], "believes": [{"claim_id": "cl_rima_tomorrow", "stance": "sincere"}]},
    {"character_id": "karim", "knows": [K("f_minutes_exist", "witnessed")],
     "hides": [{"fact_id": "f_summary_zone_dropped", "reveal_when": {"presented": {"evidence_id": "ev_minutes_orig", "to_character": "karim"}}, "cover_claim_id": "cl_karim_copy", "reveal_line_id": "kr_break"}],
     "believes": [{"claim_id": "cl_karim_copy", "stance": "deliberate_lie"}]},
]
hyps = [
    {"id": "h_breach", "statement_ar": "حدث اختراق أو عبث بالوقت: عُدّلت أوقات الرسالة أو دُسّت في النظام فوصلت قبل أن تُكتب.", "is_true": False, "plausibility_at_start": "high"},
    {"id": "h_zones", "statement_ar": "اختلاف في المناطق الزمنية وطريقة العرض: حدث واحد كُتب بوقت السفينة وعُرض بوقت المحرر، وأسقط ملخص مختصر ما يدل على المنطقة.", "is_true": True, "plausibility_at_start": "low", "suspect_id": "karim"},
    {"id": "h_insufficient", "statement_ar": "لا تكفي الأدلة للفصل بين الاختراق وتنسيق الزمن قبل الحصول على أصل سجل التسليم.", "is_true": False, "plausibility_at_start": "medium"},
]
mis = [
    {"id": "rh_summary", "points_to_hypothesis_id": "h_breach", "planted_via_ar": "الملخص المتداول يضع الوصول الخميس 04:59 والكتابة الخميس 23:58، أي وصولاً قبل الكتابة بتسع عشرة ساعة.", "evidence_ids": ["ev_summary"], "refuted_by_inference_ids": ["i_zone_dropped_a", "i_zone_dropped_b", "i_rule_breach_a"],
     "fairness_note_ar": "الرأس وواجهة الجهاز وسجل الخادم متاحة من البداية أو بسؤال وليد، وفيها المنطقة واليوم؛ والمحضر الأصلي محفوظ في مجلد الاجتماع."},
    {"id": "rh_witness", "points_to_hypothesis_id": "h_breach", "planted_via_ar": "ريما تقول إن وقت الرسالة 23:58 أكبر من ساعة جهازها 04:59، فتبدو الرسالة من الغد.", "evidence_ids": ["ev_rima_comment"], "refuted_by_inference_ids": ["i_rima_claim", "i_rule_breach_a"],
     "fairness_note_ar": "الوقتان المقارَنان يحملان منطقتين مختلفتين مكتوبتين في الرأس والواجهة، فالتحويل ممكن لكل لاعب."},
    {"id": "rh_job", "points_to_hypothesis_id": "h_breach", "planted_via_ar": "سجل المهام يُظهر نشاطاً على الخادم بعد وصول الرسالة بساعة تقريباً.", "evidence_ids": ["ev_job_log"], "refuted_by_inference_ids": ["i_job_explained"],
     "fairness_note_ar": "سطر المهمة نفسه يقول إنها قراءة فقط، وسجل الخادم يقول إن الرسالة لم تُعدَّل."},
]
los = [
    {"id": "lo_claim", "statement_ar": "يصنّف المصادر الزمنية (رأس أصلي، عرض جهاز، ملخص مختصر، شهادة) قبل الاعتماد عليها.", "skill_ko_ref": "KO-RS-05-001", "observable_behaviors_ar": ["يصنّف الرأس والخادم والملخص", "يقابل القول بسجل"], "evidence_sources": ["evidence_board"]},
    {"id": "lo_timeline", "statement_ar": "يحوّل كل وقت إلى مرجع واحد ويرتّب الأحداث عليه.", "skill_ko_ref": "KO-RS-05-005", "observable_behaviors_ar": ["يشغّل مختبر الأزمنة بإزاحات صحيحة", "يضع الأدلة في أزمنتها الموحّدة"], "evidence_sources": ["timeline_task", "action_log"]},
    {"id": "lo_hyp", "statement_ar": "يوازن بين فرضيتين على الأقل ويستبعد ما تنقضه الأدلة.", "skill_ko_ref": "KO-RS-05-002", "observable_behaviors_ar": ["يضيف فرضيات", "يستبعد بدليل"], "evidence_sources": ["hypothesis_ledger"]},
    {"id": "lo_diag", "statement_ar": "يفصل بين وقت الحدث ووقت عرضه، ويحدد حدود موثوقية الملخص المختصر.", "skill_ko_ref": "KO-RS-06-001", "observable_behaviors_ar": ["يربط الدليل بالفرضية باتجاه صحيح"], "evidence_sources": ["evidence_board", "final_justification"]},
    {"id": "lo_calib", "statement_ar": "يصوغ ثقته بحدودها.", "skill_ko_ref": "KO-RS-06-021", "observable_behaviors_ar": ["يختار ثقة معقولة", "يذكر حدوداً"], "evidence_sources": ["final_justification"]},
    {"id": "lo_revise", "statement_ar": "يراجع رأيه الأول حين يظهر دليل جديد.", "skill_ko_ref": "KO-RS-06-009", "observable_behaviors_ar": ["يغيّر فرضيته الرائدة بدليل"], "evidence_sources": ["hypothesis_ledger"]},
]
def levels(d): return [{"score": i, "descriptor_ar": t} for i, t in enumerate(d)]
rub = {
    "reference_answer_ar": "لا سفر في الزمن ولا اختراق. أُنشئت الرسالة مساء الخميس عند 23:58 على ساعة السفينة (UTC-2)، أي 01:58 بالتوقيت العالمي فجر الجمعة، وقبلها الخادم بعد دقيقة تقريباً (01:59 UTC)، وعرضها جهاز المحرر في 04:59 بتوقيته (UTC+3). ثلاثة أرقام لحظة واحدة. ثم أعاد أحد المشاركين إرسال ملخص حذف المناطق وكتب «الخميس» للوقتين، فبدت الرسالة وصلت قبل كتابتها. حدود الاستنتاج: السجلات تثبت التوقيت لا صحة محتوى الرسالة، ولا تثبت لماذا اختُصر الملخص هكذا.",
    "criteria": [
        {"id": "c_source", "name_ar": "استدعاء مصادر مناسبة وتصنيفها", "objective_ids": ["lo_claim"], "scored_by": "deterministic", "weight": 0.25, "levels": levels(["لم يصنّف", "أخطأ في الأغلب", "نصف صحيح", "معظمه صحيح", "كله صحيح"])},
        {"id": "c_conflict", "name_ar": "تفسير التعارض بتوحيد الأزمنة", "objective_ids": ["lo_timeline"], "scored_by": "deterministic", "weight": 0.25, "levels": levels(["لم يوحّد شيئاً", "حاول دون نجاح", "وحّد نصفها", "وحّد معظمها", "وحّد كلها ووضعها في مواضعها"])},
        {"id": "c_links", "name_ar": "ربط الأدلة بالفرضيات", "objective_ids": ["lo_diag"], "scored_by": "deterministic", "weight": 0.12, "levels": levels(["لا روابط", "قليلة", "نصفها صحيح", "معظمها", "كلها دقيقة"])},
        {"id": "c_elimination", "name_ar": "استبعاد الفرضيات الخاطئة", "objective_ids": ["lo_hyp"], "scored_by": "deterministic", "weight": 0.08, "levels": levels(["لم يستبعد", "استبعد خطأً", "فرضية بدليل", "فرضيتين", "كل الخاطئة"])},
        {"id": "c_uncertainty", "name_ar": "التعامل مع عدم اليقين", "objective_ids": ["lo_calib"], "scored_by": "deterministic", "weight": 0.15, "levels": levels(["ثقة مفرطة", "حدود قليلة", "جزئية", "معقولة", "معايَرة كاملة"])},
        {"id": "c_revision", "name_ar": "تصحيح الرأي عند الدليل الجديد", "objective_ids": ["lo_revise"], "scored_by": "deterministic", "weight": 0.15, "levels": levels(["بقي على فرضية مرفوضة", "لم يعلن فرضية", "ثبت على فرضية سليمة", "غيّر بدليل", "غيّر بدليل ووثّق"])},
        {"id": "c_justification", "name_ar": "جودة الحجة المكتوبة (مراجعة بشرية)", "objective_ids": ["lo_diag", "lo_hyp"], "scored_by": "human", "weight": 0.0, "levels": levels(["لا حجة", "ادعاء بلا سند", "أدلة دون ربط", "ربط الأدلة بالاستنتاج", "ربط مع البدائل والحدود"])},
    ],
}
def H(id, lv, kind, text, trig, target=None, w=0.0):
    d = {"id": id, "level": lv, "kind": kind, "text_ar": text, "trigger": trig, "assessment_weight": w}
    if target: d["targets_inference_id"] = target
    return d
he = lambda e: {"has_evidence": e}
hints = [
    H("hg1", 1, "metacognitive", "قبل أن تقارن وقتين، اسأل: هل كُتبا بمرجع زمني واحد؟", {"always": True}, None, 0.02),
    H("hg2", 2, "focus_area", "اقرأ بجانب كل وقت ما يدل على منطقته واليوم الذي ينتمي إليه.", he("ev_server_log"), None, 0.04),
    H("hz1", 1, "metacognitive", "أي السجلات الثلاثة يكتب بمرجع واحد لا يتغير بتغير الجهاز؟", he("ev_server_log"), "i_one_instant_a", 0.02),
    H("hz2", 2, "focus_area", "ابدأ من سجل الخادم، ثم حوّل وقت الرأس ووقت الواجهة إليه.", he("ev_server_log"), "i_one_instant_a", 0.04),
    H("hz3", 3, "pointer", "الوقت المحلي = UTC + الإزاحة؛ فاطرح الإزاحة من الوقت المحلي، وإن كانت سالبة فسيزيد الوقت.", he("ev_server_log"), "i_one_instant_a", 0.08),
    H("hz4", 4, "partial_reveal", "بعد التحويل الصحيح ستتقارب القراءات الثلاث إلى دقيقة أو دقيقتين؛ فإن لم تتقارب فراجع إشارة الإزاحة.", he("ev_server_log"), "i_one_instant_a", 0.12),
    H("hs1", 1, "metacognitive", "ما الذي يظهر في الرأس والواجهة ولا يظهر في الملخص المعاد إرساله؟", he("ev_summary"), "i_zone_dropped_a", 0.02),
    H("hs2", 2, "pointer", "قارن تاريخ كل وقت في الملخص بتاريخه في الرأس وفي الواجهة.", he("ev_summary"), "i_zone_dropped_a", 0.06),
    H("hs3", 3, "partial_reveal", "اعرض المحضر الأصلي على من أرسل الملخص وسترى ما يقوله عمّا حذفه.", he("ev_summary"), "i_zone_dropped_a", 0.1),
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
Act("a_read_header", "examine", "افتح رأس الرسالة msg-7141", al, [G("ev_header")], "obj_msg", "READ_HEADER")
Act("a_read_device", "examine", "افتح واجهة بريد جهاز المحرر", al, [G("ev_device_view")], "loc_newsroom", "READ_DEVICE")
Act("a_get_server", "examine", "اطلب سطر الرسالة من سجل الخادم", fu("f_server_log_exists"), [G("ev_server_log")], "loc_server", "GET_SERVER")
Act("a_get_net", "examine", "اطلب نتيجة قياس زمن النقل", fu("f_net_tested"), [G("ev_network_info")], "loc_server", "GET_NET")
Act("a_get_trace", "examine", "اطلب سجل التسليم الكامل", fu("f_trace_exists"), [G("ev_delivery_trace")], "loc_server", "GET_TRACE")
Act("a_get_job", "examine", "اطلب سجل المهام المجدولة", fu("f_job_exists"), [G("ev_job_log")], "loc_server", "GET_JOB")
Act("a_get_summary", "examine", "اطلب الملخص الذي أُعيد إرساله", fu("f_summary_circulates"), [G("ev_summary")], "loc_newsroom", "GET_SUMMARY")
Act("a_note_rima", "examine", "دوّن تعليق ريما", fu("f_rima_saw"), [G("ev_rima_comment")], "rima", "NOTE_RIMA")
Act("a_get_minutes", "examine", "افتح محضر الاجتماع الأصلي", fu("f_minutes_exist"), [G("ev_minutes_orig")], "loc_newsroom", "GET_MINUTES")
Act("a_note_karim", "examine", "دوّن إفادة كريم", fu("f_summary_zone_dropped"), [G("ev_karim_statement")], "karim", "NOTE_KARIM")
for cid, lab in [("nora", "نورة"), ("walid", "وليد"), ("rima", "ريما"), ("karim", "كريم")]:
    Act(f"a_int_{cid}", "interview", f"ابدأ مقابلة {lab}", al, [{"op": "raise_trust", "ref_id": cid, "amount": 1}], cid, f"INT_{cid.upper()}")
Act("a_compare_times", "compare_evidence", "وحِّد الأزمنة (يُمنح عبر المختبر عند نجاحه)", {"all": [he("ev_header"), he("ev_server_log"), he("ev_device_view")]}, [G("ev_lab_norm")], None, "COMPARE_TIMES")
Act("p_minutes_karim", "present_evidence", "اعرض المحضر الأصلي على كريم", {"presented": {"evidence_id": "ev_minutes_orig", "to_character": "karim"}}, [{"op": "emit_event", "ref_id": "PRESENTED_MINUTES_KARIM"}], "karim", "P_MINUTES_KARIM", 0)
Act("a_hint", "request_hint", "اطلب تلميحاً", al, [], None, "REQUEST_HINT", 0)
Act("a_accuse", "final_accusation", "قدّم الاستنتاج النهائي", al, [{"op": "emit_event", "ref_id": "SUBMIT"}], None, "FINAL_ACCUSATION", 0)

topics = [
    {"id": "t_ship", "label_ar": "ساعة السفينة والإرسال", "example_questions_ar": ["متى أرسلت الرسالة؟", "ما توقيت ساعة السفينة؟"], "fact_ids": ["f_ship_zone", "f_nora_sent"]},
    {"id": "t_server", "label_ar": "سجلات الخادم", "example_questions_ar": ["بأي توقيت يخزّن الخادم الأوقات؟", "هل لديك سجل الاستلام؟", "هل أُجري قياس لزمن النقل؟", "هل يوجد سجل تسليم كامل؟", "هل جرى شيء على الخادم بعد الاستلام؟"], "fact_ids": ["f_server_utc", "f_server_log_exists", "f_net_tested", "f_trace_exists", "f_job_exists"]},
    {"id": "t_seen", "label_ar": "ما رأته ريما", "example_questions_ar": ["ماذا رأيت في الوارد؟", "هل وصلك ملخص بعد الاجتماع؟"], "fact_ids": ["f_rima_saw", "f_summary_circulates"], "claim_ids": ["cl_rima_tomorrow"]},
    {"id": "t_minutes", "label_ar": "المحضر والملخص", "example_questions_ar": ["أين المحضر الأصلي؟", "هل غيّرت شيئاً في الوقتين؟"], "fact_ids": ["f_minutes_exist", "f_summary_zone_dropped"], "claim_ids": ["cl_karim_copy"]},
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
    (1, "الرأس مكتوب بمنطقة السفينة (UTC-2)، وسجل الخادم بالتوقيت العالمي، وواجهة الجهاز بمنطقة المحرر (UTC+3)؛ فالأرقام الثلاثة لا تُقارن قبل تحويلها إلى مرجع واحد.", ["ev_header", "ev_server_log", "ev_device_view"], "i_one_instant_a"),
    (2, "بعد التحويل تقع الأرقام الثلاثة بين 01:58 و01:59 UTC فجر الجمعة، وفارق الدقيقة يطابق زمن النقل المعتاد وسلسلة التسليم الكاملة.", ["ev_lab_norm", "ev_delivery_trace", "ev_network_info"], "i_one_instant_b"),
    (3, "الملخص المعاد إرساله كتب 04:59 و23:58 تحت «الخميس» معاً، بينما يضعهما الرأس والواجهة في يومين مختلفين؛ فالترتيب المعكوس جاء من الاختصار.", ["ev_summary", "ev_device_view", "ev_header"], "i_zone_dropped_a"),
    (4, "المحضر الأصلي يحفظ المنطقة واليوم، وصاحب الملخص يقرّ بأنه حذفهما.", ["ev_minutes_orig", "ev_karim_statement"], "i_zone_dropped_b"),
    (5, "مهمة الفهرسة الليلية قراءة فقط وبعد الاستلام، وسجل الخادم يقول إن الرسالة لم تُعدَّل؛ فلا قرينة على اختراق.", ["ev_job_log", "ev_server_log"], "i_job_explained"),
    (6, "انطباع «من الغد» قارن رقمين من يومين ومنطقتين؛ فلا يصحّ حتى يُحوَّلا.", ["ev_rima_comment", "ev_header", "ev_device_view"], "i_rima_claim"),
    (7, "نسبة الترجيح عالية لتعارض في تنسيقات الزمن والمناطق، لا لحدث مستحيل؛ وهي مبنية على سجلات تُعيد بناء التسلسل من المصدر.", ["ev_delivery_trace", "ev_minutes_orig", "ev_lab_norm"], "i_support_zones"),
]
ending = {
    "steps": [{"order": o, "text_ar": t, "uses_evidence_ids": u, "inference_id": i} for o, t, u, i in steps],
    "alternative_paths_ar": ["يمكن الوصول إلى النتيجة بتحويل الأوقات الثلاثة بنفسك، أو من سجل التسليم الكامل وقياس زمن النقل ومحضر الاجتماع الأصلي دون حساب."],
    "what_evidence_could_not_show_ar": ["السجلات تثبت التوقيت لا صحة محتوى الرسالة.", "لا تثبت الأدلة لماذا اختُصر الملخص بهذه الصورة، ولا أن الاختصار هو وحده سبب انتشار الشائعة."],
    "science_notes_ar": ["التوقيت النسبي (محلي بلا منطقة) قد يولد معجزة وهمية؛ حوّل كل وقت إلى مرجع واحد قبل المقارنة.", "سجل التسليم الكامل هو سلسلة العهدة الرقمية للرسالة: يربط كل خطوة بمرجع زمني واحد، ويُعاد بناء التسلسل منه لا من الملخص."],
}
core = {
    "schema_version": "0.1.0", "case_id": CID, "case_version": "0.1.0",
    "meta": {"title_ar": "رسالة من الغد", "title_en": "A Letter From Tomorrow", "age_band": "16-18", "locale": "ar", "dialogue_register": "msa", "estimated_minutes": 30, "difficulty": 3,
             "content_flags": ["no_violence", "science_lab"], "authors": ["فريق أثر التحريري (مسودة بمساعدة الذكاء الاصطناعي، لم تُراجَع بشرياً بعد)"],
             "knowledge_object_refs": ["KO-RS-05-001", "KO-RS-05-005", "KO-RS-05-002", "KO-RS-05-004", "KO-RS-06-001", "KO-RS-06-008", "KO-RS-06-009", "KO-RS-06-021", "KO-FC-04-024", "KO-RS-05-014"]},
    "premise": {"hook_ar": "رسالة بدا أنها وصلت قبل أن تُكتب بساعات، وزملاء يهمسون: اختراق، أو شيء أغرب.",
                "player_role_ar": "أنت مراجع ملفات في مركز الشرفة للإعلام العلمي، وطُلب منك تفسير ما حدث قبل أن تنتشر الشائعة أكثر.",
                "setting_ar": "غرفة الأخبار في مركز علمي خيالي صباح الجمعة. المرسلة على سفينة أبحاث في عرض البحر، وللسفينة ساعتها الخاصة.",
                "public_fact_ids": ["f_msg_looks_early", "f_rumor_breach", "f_nora_reporting"],
                "assumed_general_knowledge_ar": ["لكل منطقة زمنية إزاحة عن التوقيت العالمي UTC", "الوقت المعروض على الجهاز قد يختلف عن الوقت المخزّن في الخادم"]},
    "entities": {"characters": chars, "locations": locations, "objects": objects, "organizations": orgs},
    "truth": {"solution": {"culprit_ids": ["karim"], "summary_ar": "لم تصل رسالة قبل كتابتها ولم يخترق أحد النظام. الرسالة كُتبت بتوقيت السفينة وخُزّنت بالتوقيت العالمي وعُرضت بتوقيت المحرر، فبدت الأرقام متناقضة. وملخص مختصر أُعيد إرساله حذف ما يدل على المناطق.",
                          "key_fact_ids": ["f_one_instant", "f_summary_zone_dropped"]},
              "facts": facts, "claims": claims},
    "timeline": timeline, "evidence": ev, "evidence_graph": {"inferences": inf},
    "character_knowledge": ck, "hypotheses": hyps, "misdirection_plan": mis, "learning_objectives": los,
    "mechanics": {"time_budget_units": 30, "actions": A},
    "state_machine": {"id": "c003", "initial": "briefing", "type": "compound", "states": {
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
    "clock": {"epoch_hhmm": "20:00", "zone_label_ar": "التوقيت العالمي UTC (مساء الخميس)"},
    "cover": {"title_ar": "رسالة من الغد", "tagline_ar": "وصلت قبل أن تُكتب… أم هكذا يبدو؟", "kicker_ar": "الملف الثالث · مركز الشرفة للإعلام العلمي", "glyph": "◷", "accent": "cyan"},
    "cold_open_ar": ["صباح الجمعة في غرفة الأخبار.", "رسالة من سفينة أبحاث في عرض البحر، ومن يقرأ الملخص المتداول يرى أنها وصلت قبل أن تُكتب بتسع عشرة ساعة.", "تهمس الغرفة: اختراق، أو خلل في الخادم، أو شيء أغرب.", "ابدأ بالسؤال: ما الذي يقوله كل سجل، وبأي ساعة يقوله؟"],
    "labs": [{
        "id": "lab_time", "type": "time_normalizer", "title_ar": "مختبر توحيد الأزمنة",
        "intro_ar": "لكل سجل وقتٌ مكتوب بمنطقة زمنية مختلفة. أدخل لكل سجل إزاحته عن التوقيت العالمي UTC بالساعات (التوقيت المحلي = UTC + الإزاحة، وقد تكون الإزاحة سالبة)، وأبقِ انحراف الساعة صفراً ما لم يذكر السجل انحرافاً. حين تتقارب الأزمنة بعد التحويل يمنحك المختبر تقريراً.",
        "tolerance_min": 2, "epoch_utc_minute_of_day": 1200, "day_labels_ar": ["الخميس (يوم الإرسال)", "الجمعة"],
        "grants_evidence_on_converge": "ev_lab_norm",
        "items": [
            {"evidence_id": "ev_header", "label_ar": "رأس الرسالة — وقت الإنشاء", "day": 0, "hhmm": "23:58", "basis_ar": "الرأس يكتب منطقة المرسلة بجانب الوقت"},
            {"evidence_id": "ev_server_log", "label_ar": "سجل الخادم — وقت الاستلام", "day": 1, "hhmm": "01:59", "basis_ar": "السجل يذكر أنه بالتوقيت العالمي"},
            {"evidence_id": "ev_device_view", "label_ar": "واجهة جهاز المحرر — وقت الوصول", "day": 1, "hhmm": "04:59", "basis_ar": "الواجهة تكتب منطقة الجهاز بجانب الوقت"},
        ],
    }],
    "source_classes": [
        {"id": "primary_record", "label_ar": "سجل أصلي", "help_ar": "يُنتجه جهاز أو نظام لحظة الحدث دون وسيط، كرأس رسالة أو سجل خادم."},
        {"id": "redisplay", "label_ar": "نسخة معروضة", "help_ar": "معلومة أُعيد عرضها أو اختصارها، كواجهة جهاز أو ملخص أُعيد إرساله."},
        {"id": "claim", "label_ar": "قول أو تصريح", "help_ar": "إفادة شخص أو انطباعه؛ تُقاس بالسجلات لا بنبرة صاحبها."},
        {"id": "template", "label_ar": "قالب أو نموذج", "help_ar": "نص جاهز لا يصف الحدث الفعلي بذاته."},
        {"id": "public_document", "label_ar": "وثيقة منشورة", "help_ar": "وثيقة معلنة ومعروف ناشرها."}],
    "limit_menu": [
        {"id": "l_intent", "label_ar": "الأدلة لا تثبت لماذا اختُصر الملخص بهذه الصورة ولا أن صاحبه قصد شيئاً"},
        {"id": "l_content", "label_ar": "السجلات تثبت التوقيت لا صحة محتوى الرسالة"},
        {"id": "l_network", "label_ar": "قياس زمن النقل التجريبي تقديري ولا يقيس هذه الرسالة بعينها"},
        {"id": "l_invalid_display", "label_ar": "اختلاف الوقت المعروض بين جهازين يثبت وقوع اختراق"},
        {"id": "l_invalid_witness", "label_ar": "ريما أخطأت في الأرقام فهي تكذب"},
        {"id": "l_invalid_all", "label_ar": "لا حاجة لذكر حدود ما دامت السجلات متفقة بعد التحويل"}],
    "mind_change_menu": [
        {"id": "m_server_edit", "label_ar": "ثبوت تعديل على سجل الخادم بعد الاستلام"},
        {"id": "m_trace_gap", "label_ar": "ظهور فجوة أو تعارض في سجل التسليم الكامل"},
        {"id": "m_header_zone", "label_ar": "ثبوت أن المنطقة المكتوبة في الرأس ليست منطقة جهاز المرسلة"},
        {"id": "m_popular", "label_ar": "كثرة من يرددون شائعة الاختراق"}],
    "transfer": {
        "id": "tr_webinar", "title_ar": "اختبار نقل المهارة: موعد الندوة",
        "scenario_ar": "في منظمة خيالية، ثلاث وثائق تذكر موعد ندوة عبر الإنترنت، ولا تتفق ساعاتها.",
        "documents": [
            {"title_ar": "بطاقة الدعوة (لقطة شاشة مقصوصة)", "body_ar": "تبدأ الندوة الساعة 20:00."},
            {"title_ar": "تقويم الفريق", "body_ar": "الندوة: 17:00 UTC."},
            {"title_ar": "رسالة تذكير", "body_ar": "تبدأ الندوة بعد ساعتين من وصول هذا التذكير. وصل: 18:10 بتوقيت المنظّم (UTC+2)."},
        ],
        "prompt_ar": "اختر الخطوات التي تصلح للتحقق من موعد الندوة (يمكنك اختيار أكثر من خطوة).",
        "options": [
            {"id": "o1", "text_ar": "تحديد منطقة كل وقت وتحويلها كلها إلى مرجع واحد قبل المقارنة"},
            {"id": "o2", "text_ar": "الفصل بين وقت الحدث ووقت عرضه على جهاز كل شخص"},
            {"id": "o3", "text_ar": "طلب أصل الدعوة بدل لقطة الشاشة المقصوصة"},
            {"id": "o4", "text_ar": "مقارنة الموعد بمصدر مستقل كصفحة المنظّم"},
            {"id": "o5", "text_ar": "اعتماد أكبر رقم بين الأوقات لأنه الأحدث"},
            {"id": "o6", "text_ar": "الحكم بأن المنظّم زوّر الدعوة لمجرد اختلاف الساعات"},
            {"id": "o7", "text_ar": "الاكتفاء بالوثيقة التي تبدو أوضح خطاً"},
            {"id": "o8", "text_ar": "تجاهل التذكير لأن صياغته معقدة"}],
        "free_text_prompt_ar": "اكتب في ثلاثة أسطر كيف تقرّر موعد الندوة وما الذي يجعلك أقل ثقة بنتيجتك."},
    "skills": [{"skill_id": "KO-RS-05-001", "track": "B"}, {"skill_id": "KO-RS-05-005", "track": "B"}, {"skill_id": "KO-RS-05-002", "track": "D"}, {"skill_id": "KO-RS-06-001", "track": "C"}, {"skill_id": "KO-FC-04-024", "track": "E"}],
    "stage_hooks_ar": {"briefing": "رسالة من الغد… أم ساعة لا تشبه ساعة؟", "investigating": "ثلاثة أرقام، وكل رقم يعيش في منطقة غير الأخرى.", "review": "قبل أن تغلق الملف: ما الذي لا تثبته الساعات؟", "resolved": "أُغلق الملف. الملف التالي أبعد عن الساعات وأقرب إلى الخرائط."},
    "character_glyphs": {"nora": "ن", "walid": "و", "rima": "ر", "karim": "ك"},
}
sc = {
    "case_id": CID,
    "accepted_conclusions": {
        "h_zones": {"grade": 1, "note_ar": "استنتاج متسق مع الأدلة ويتطلب ذكر حدوده."},
        "h_breach": {"grade": 0, "note_ar": "يخلط بين اختلاف العرض والتلاعب؛ بعد توحيد الأزمنة لا يبقى ما يستدعي الاختراق."},
        "h_insufficient": {"grade": 0, "note_ar": "تحفّظ مفرط: السجلات المتاحة تكفي لإعادة بناء التسلسل؛ والتحفظ المقبول يخص النيّة ومحتوى الرسالة."}},
    "confidence_band": {"h_zones": [70, 92], "h_breach": [0, 10], "h_insufficient": [0, 20]},
    "source_key": {"ev_header": "primary_record", "ev_server_log": "primary_record", "ev_device_view": "redisplay", "ev_summary": "redisplay", "ev_network_info": "primary_record",
                   "ev_rima_comment": "claim", "ev_delivery_trace": "primary_record", "ev_minutes_orig": "primary_record", "ev_karim_statement": "claim", "ev_job_log": "primary_record"},
    "link_key": {
        "h_zones": {"ev_header": "supports", "ev_server_log": "supports", "ev_device_view": "supports", "ev_delivery_trace": "supports", "ev_network_info": "supports", "ev_minutes_orig": "supports",
                    "ev_karim_statement": "supports", "ev_lab_norm": "supports", "ev_summary": "neutral", "ev_rima_comment": "neutral", "ev_job_log": "neutral"},
        "h_breach": {"ev_header": "weakens", "ev_server_log": "weakens", "ev_device_view": "weakens", "ev_delivery_trace": "weakens", "ev_network_info": "weakens", "ev_minutes_orig": "weakens", "ev_lab_norm": "weakens",
                     "ev_summary": "supports", "ev_rima_comment": "supports", "ev_job_log": "supports"},
        "h_insufficient": {"ev_header": "weakens", "ev_server_log": "weakens", "ev_delivery_trace": "weakens", "ev_lab_norm": "weakens", "ev_summary": "neutral", "ev_rima_comment": "neutral"},
    },
    "required_limits": ["l_intent", "l_content"],
    "valid_mind_changers": ["m_server_edit", "m_trace_gap", "m_header_zone"],
    "invalid_limits": ["l_invalid_display", "l_invalid_witness", "l_invalid_all"],
    "decisive_evidence": ["ev_header", "ev_server_log", "ev_device_view", "ev_lab_norm", "ev_minutes_orig"],
    "lab_requirement": {"lab_id": "lab_time", "must_converge": True},
    "timeline_requirement": [{"evidence_id": "ev_header", "utc_minute": 358, "tol": 2}, {"evidence_id": "ev_server_log", "utc_minute": 359, "tol": 2}, {"evidence_id": "ev_device_view", "utc_minute": 359, "tol": 2}],
    "refuted_hypotheses": ["h_breach", "h_insufficient"],
    "criteria_map": {"c_source": "source_typing", "c_conflict": "conflict_resolution", "c_links": "hypothesis_links", "c_elimination": "elimination", "c_uncertainty": "uncertainty", "c_revision": "revision", "c_justification": "justification_human"},
    "transfer_key": {"valid": ["o1", "o2", "o3", "o4"], "invalid": ["o5", "o6", "o7", "o8"]},
    "caps": {"no_citations_max": 45, "no_conflict_resolution_max": 60},
}
os.makedirs(OUT, exist_ok=True)
for suf, obj in [("", core), (".ui", ui), (".scoring", sc)]:
    with open(os.path.join(OUT, f"{CID}{suf}.json"), "w", encoding="utf8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
print("ok")
