#!/usr/bin/env python3
# Generator for the flagship case c001 «الرصد الأخير». Writes core / ui / scoring JSON (UTF-8, ensure_ascii=False).
import json, sys, os

OUT = sys.argv[1]
CID = "c001_last_observation"

def T(m, p="exact", end=None):
    d = {"start_min": m, "precision": p}
    if end is not None:
        d["end_min"] = end
    return d

# ---------------------------------------------------------------- entities
chars = []
def ch(id, name, role, age, persona, motives, lines, forbidden=None, register="msa"):
    chars.append({
        "id": id, "name_ar": name, "role": role, "age_descriptor_ar": age, "persona_ar": persona, "motives_ar": motives,
        "speech_constraints": {"register": register, "max_sentences_per_turn": 3, "forbidden_topics_ar": forbidden or []},
        "authored_lines": lines,
    })
def L(id, purpose, text, facts=None, claims=None):
    d = {"line_id": id, "purpose": purpose, "text_ar": text}
    if facts: d["fact_ids"] = facts
    if claims: d["claim_ids"] = claims
    return d

ch("reem", "ريم الخزرجي", "victim", "متدربة في التاسعة عشرة، طالبة فيزياء فلكية",
   "متحمسة ودقيقة، تفضّل أن يتكلم الملف نيابةً عنها. قلقة من أن يُنظر إليها كمتّهمة لا كصاحبة اعتراض.",
   ["أن يُسجَّل الرصد الأول باسمها إن كان لها", "ألا تضيع فرصتها الأكاديمية بسبب خلاف مع رئيسها"],
   [
    L("reem_greet", "greeting", "تفضّل. أرجو أن تقرأ الملفات قبل أن تحكم؛ الأرقام في رأس الملف أصدق مني."),
    L("reem_arrival", "reveal", "التقطت كاميرا المسح الإطار الذي يظهر فيه الجسم في الحادية والعشرين وعشر دقائق بالتوقيت العالمي. هذا ما يقوله رأس الملف، لا ذاكرتي.", ["f_reem_frame_time"]),
    L("reem_clock", "reveal", "حاسوب الكاميرا مربوط بمستقبل GPS ويُضبط وقته باستمرار، ورأس الملف يسجّل ذلك.", ["f_clock_gps"]),
    L("reem_sent", "reveal", "أرسلت لد. هشام رسالة ومعها الإطار بعد نحو إحدى عشرة دقيقة، حين تأكدت أن الجسم ليس عيباً في الحسّاس.", ["f_chat_sent"]),
    L("reem_seen", "reveal", "ظهر لي إيصال القراءة بعد دقائق قليلة. ثم لم يأتِني ردّ.", ["f_chat_seen"]),
    L("reem_file", "reveal", "أستطيع أن أسلّمك الإطار الأصلي كما هو، برأس الملف دون أي تعديل. وهناك أيضاً نسخة في الأرشيف يمكن مقارنتها.", ["f_reem_file_shared"]),
    L("reem_warning", "reveal", "نعم، تلقيت تنبيهاً قبل أشهر لأنني استخدمت الكاميرا خارج الجدول. لا علاقة له بتلك الليلة، لكنني أفهم لماذا قد يُستخدم ضدي.", ["f_reem_warning"]),
    L("reem_unknown", "deflect_unknown", "لا أعرف هذا، ولا أريد أن أخمّن في ملفٍ يحتاج إلى أدلة."),
    L("reem_off", "deflect_offtopic", "أخشى أن هذا بعيد عمّا أعرفه. اسألني عن الإطار أو الرسالة أو الساعات."),
    L("reem_bye", "farewell", "شكراً لأنك تقرأ الملف قبل أن تسأل عن الأشخاص."),
   ], ["اتهام شخص بنية معيّنة دون دليل"])

ch("hisham", "د. هشام المنصور", "suspect", "في أواخر الخمسينات، رئيس قسم الرصد",
   "رصين ومهذّب، يحتمي بمكانته وبلغة الإجراءات. يجيب بدقة عمّا يُسأل عنه ولا يزيد.",
   ["أن يبقى اسم المرصد واسمه مقترنَين بالاكتشاف", "ألا يظهر أنه تأخر عن متدربة"],
   [
    L("h_greet", "greeting", "أهلاً بك. أثق أن اللجنة ستنصف الحقيقة، وهي أن رصدي موثّق بأدق ما لدينا من أجهزة."),
    L("h_frame", "reveal", "التقط المقراب الرئيسي أول إطار لي في الحادية والعشرين وأربع وثلاثين دقيقة بالتوقيت العالمي.", ["f_hisham_frame_time"]),
    L("h_bulletin", "reveal", "أرسلت البلاغ إلى النشرة الدولية بعد أن تأكدت من ثبات الجسم، وصرّحت فيه بأنني لا أعلم برصد أسبق.", ["f_bulletin_declared"]),
    L("h_lie_unaware", "lie", "لم تصلني أي رسالة قبل أن ألتقط إطاري. لو علمت بشيء لذكرته في البلاغ.", None, ["cl_h_unaware"]),
    L("h_lie_clock", "lie", "ساعة كاميرا المسح لم تكن موثوقة تلك الليلة؛ كانت هناك فروق في التوقيت في أكثر من جهاز.", None, ["cl_h_clock"]),
    L("h_lie_auto", "lie", "أي تعديل في الوسوم جاء من نظام الأرشفة الآلي، ولا علاقة لي به.", None, ["cl_h_auto"]),
    L("h_break_aware", "break_down", "فتحت رسالتها فعلاً قبل أن ألتقط إطاري. ظننت أن الإطار قد يكون ضجيجاً فأردت أن أتأكد بنفسي، ولم يكن ينبغي أن أترك ذلك خارج البلاغ.", ["f_hisham_aware"]),
    L("h_break_relabel", "break_down", "نعم، عدّلت الوسم من محطتي، وسمّيته «روتينياً» حتى لا يُربك البلاغ. كان خطأً.", ["f_relabel"]),
    L("h_refuse", "refuse_secret", "هذا سؤال لا أرى أن إجابته تفيد اللجنة الآن."),
    L("h_unknown", "deflect_unknown", "لا علم لي بهذا الأمر."),
    L("h_off", "deflect_offtopic", "فلنعد إلى ما يخصّ البلاغ والسجلات، فهذا اختصاص اللجنة."),
    L("h_bye", "farewell", "أرجو أن تكون اللجنة سريعة في قرارها."),
   ], ["اتهام ريم بالكذب دون سند"])

ch("yusuf", "يوسف السالم", "witness", "في منتصف الثلاثينات، مشغّل الليل",
   "دقيق ومتوتر قليلاً، يكره الدخول في خلافات الكبار ويفضّل أن يكتب ما رآه بدل أن يفسّره.",
   ["أن يحافظ على عمله وعلى علاقته بالفريق"],
   [
    L("y_greet", "greeting", "أهلاً. أنا هنا لأقول ما دوّنته وما رأيته، لا ما أظنّه."),
    L("y_logged", "reveal", "دوّنت في سجل التشغيل أن إطاراً جديداً وصل من كاميرا المسح في الحادية والعشرين وعشر دقائق بالتوقيت العالمي.", ["f_yusuf_logged"]),
    L("y_tz", "reveal", "ساعات الجدار عندنا محلية، لكن سجل التشغيل نكتبه بالتوقيت العالمي دائماً. والتوقيت المحلي ثلاث ساعات قبله.", ["f_local_tz"]),
    L("y_saw", "reveal", "رأيت د. هشام يفتح إطار المسح على محطته ويقول إن في الحقل شيئاً لم يكن موجوداً، وذلك قبل أن يوجّه المقراب، على ما أذكر. لا أجزم بالدقائق.", ["f_yusuf_saw"]),
    L("y_ws", "reveal", "المحطة تسجّل أي حساب يفتح أي ملف. يمكنك طلب سجلها.", ["f_ws_logs_exist"]),
    L("y_badge", "reveal", "والبوابة تسجّل البطاقات دخولاً وخروجاً.", ["f_badge_exists"]),
    L("y_alone", "reveal", "غادرت غرفة التحكم قرب الواحدة والخامسة ليلاً بالتوقيت المحلي، وبقي د. هشام فيها.", ["f_alone_in_room"]),
    L("y_unknown", "deflect_unknown", "لا أعرف، ولا أحب أن أخمّن."),
    L("y_off", "deflect_offtopic", "هذا خارج ما رأيته. اسألني عن السجل أو عن الغرفة."),
    L("y_bye", "farewell", "إن احتجت إلى السجلات فهي في الغرفة."),
   ])

ch("nadir", "نادر الجابري", "bystander", "في أوائل الأربعينات، مسؤول الإعلام",
   "حريص على صورة المرصد ويكتب بسرعة. لا يميل إلى التدقيق في الأرقام التي تبدو متفقة مع الرواية المعلنة.",
   ["أن يصدر البيان الصحفي في موعده"],
   [
    L("n_greet", "greeting", "أهلاً بك. أنا أنقل ما يصلني من الفريق، ولا أصنع الأخبار."),
    L("n_note", "reveal", "نسخت الوقت من شاشة الأرشيف كما هو إلى لوحتنا، ولم أتحقق من المنطقة الزمنية.", ["f_press_note_local"]),
    L("n_late", "reveal", "حسب اللوحة وصل إطار ريم بعد منتصف الليل، أي بعد رصد د. هشام. هذا ما فهمته وقتها.", None, ["cl_reem_late"]),
    L("n_unknown", "deflect_unknown", "لا أعلم، فهذا ليس من اختصاص مكتبي."),
    L("n_off", "deflect_offtopic", "اسألني عن البيان واللوحة فقط."),
    L("n_bye", "farewell", "أرجو أن لا يتأخر القرار؛ الصحافة تنتظر."),
   ])

ch("salma", "سلمى العطار", "witness", "في أواخر الثلاثينات، أمينة الأرشيف",
   "منظّمة وهادئة، تثق بالسجلات أكثر من الانطباعات وتكره أن يُنسب إليها ما لم تفحصه.",
   ["أن تبقى سجلات الأرشيف سليمة وموثوقة"],
   [
    L("s_greet", "greeting", "تفضّل. ما أعرفه مكتوب في تقارير الفحص."),
    L("s_lag", "reveal", "خادم الأرشيف يعرض الوقت المحلي، وآخر فحص مزامنة أظهر أنه متأخر أربع دقائق، ووثّقت ذلك في تقرير.", ["f_archive_lag"]),
    L("s_tz", "reveal", "الوقت المحلي للمرصد ثلاث ساعات قبل التوقيت العالمي، وأجهزة العرض عندنا معظمها محلية.", ["f_local_tz"]),
    L("s_audit", "reveal", "كل تعديل على وسوم الملفات يُسجَّل في سجل تدقيق، ويمكنني تصديره لك.", ["f_audit_available"]),
    L("s_unknown", "deflect_unknown", "هذا ليس مسجّلاً عندي."),
    L("s_off", "deflect_offtopic", "اسألني عن الأرشيف والساعات والتدقيق."),
    L("s_bye", "farewell", "إن احتجت إلى تصدير آخر فأخبرني."),
   ])

locations = [
    {"id": "loc_committee", "name_ar": "مكتب اللجنة", "description_ar": "مكتبك المؤقت في المرصد: ملفات البلاغ والاعتراض."},
    {"id": "loc_control", "name_ar": "غرفة التحكم", "description_ar": "حيث يُدار المقراب الرئيسي T1 وتُدوَّن سجلات الليل."},
    {"id": "loc_dome", "name_ar": "قبّة المسح الصغيرة", "description_ar": "قبّة كاميرا المسح التي تعمل عليها المتدربة."},
    {"id": "loc_archive", "name_ar": "غرفة الأرشيف والخوادم", "description_ar": "خوادم تخزين الإطارات وسجلاتها."},
    {"id": "loc_press", "name_ar": "مكتب الإعلام", "description_ar": "لوحة الملاحظات السريعة وإعداد البيانات."},
]
objects = [
    {"id": "obj_cam", "name_ar": "كاميرا المسح (SURVEY-CAM-B)", "description_ar": "كاميرا مسح واسعة الحقل، ساعة حاسوبها مضبوطة بمستقبل GPS."},
    {"id": "obj_t1", "name_ar": "المقراب الرئيسي T1", "description_ar": "المقراب الذي يُدار من غرفة التحكم."},
    {"id": "obj_cr2", "name_ar": "محطة غرفة التحكم CR-2", "description_ar": "محطة العمل التي يدخلها العاملون ببطاقاتهم الشخصية."},
    {"id": "obj_frame", "name_ar": "الإطار field17_reem_0001", "description_ar": "الإطار الأول من حقل المسح 17 الذي يظهر فيه الجسم الجديد."},
    {"id": "obj_object", "name_ar": "الجسم الضوئي الجديد", "description_ar": "نقطة ضوئية غير موجودة في الإطار المرجعي للحقل 17."},
]
orgs = [
    {"id": "org_obs", "name_ar": "مرصد وادي النجوم", "description_ar": "مرصد افتراضي في هضبة صحراوية، توقيته المحلي UTC+3."},
    {"id": "org_union", "name_ar": "اتحاد الراصدين", "description_ar": "الجهة التي تشكّل لجنة الأسبقية وتراجع بلاغات الاكتشاف."},
]

# ---------------------------------------------------------------- facts
facts = []
def F(id, st, kind, subj, spoiler, time=None, loc=None, ko=None):
    d = {"id": id, "statement_ar": st, "kind": kind, "subject_ids": subj, "spoiler_level": spoiler}
    if time: d["time"] = time
    if loc: d["location_id"] = loc
    if ko: d["science_ko_refs"] = ko
    facts.append(d)

F("f_new_object", "ظهر جسم ضوئي جديد في حقل المسح 17 ليلة الحادثة.", "event", ["obj_object"], 0, T(10, "approx"), "loc_dome")
F("f_public_credit", "أعلن المرصد أن د. هشام المنصور هو مكتشف الجسم، وأرسل بلاغاً بذلك إلى النشرة الدولية.", "event", ["hisham", "org_obs"], 0)
F("f_reem_objects", "اعترضت المتدربة ريم الخزرجي على نسبة الاكتشاف وقالت إن كاميرا المسح التقطت الجسم قبل المقراب الرئيسي.", "event", ["reem"], 0)
F("f_local_tz", "التوقيت المحلي للمرصد هو UTC+3، ويُكتب سجل التشغيل الليلي بالتوقيت العالمي UTC.", "attribute", ["org_obs"], 0)
F("f_clock_gps", "حاسوب كاميرا المسح مضبوط على GPS، وانحراف ساعته أقل من ثانية.", "state", ["obj_cam"], 1, None, "loc_dome", ["KO-FC-04-024"])
F("f_archive_lag", "خادم الأرشيف يعرض توقيتاً محلياً وساعته متأخرة 4 دقائق عن المرجع.", "state", ["loc_archive"], 1, None, "loc_archive", ["KO-FC-04-024"])
F("f_press_note_local", "ورقة مكتب الإعلام نقلت وقت الأرشيف كما تعرضه شاشته (محلي وساعته متأخرة) دون ذكر المنطقة الزمنية، إلى جانب وقت هشام بالتوقيت العالمي.", "event", ["nadir"], 1, T(100, "approx"), "loc_press")
F("f_yusuf_logged", "دوّن يوسف في سجل التشغيل وصول إطار جديد من كاميرا المسح الساعة 21:10 UTC.", "event", ["yusuf"], 1, T(10), "loc_control")
F("f_reem_file_shared", "ريم مستعدة لتسليم الإطار الأصلي برأس الملف كما هو.", "state", ["reem", "obj_frame"], 1)
F("f_ws_logs_exist", "محطة غرفة التحكم تسجّل الحسابات التي تفتح الملفات.", "state", ["obj_cr2"], 1)
F("f_badge_exists", "بوابة غرفة التحكم تسجّل دخول البطاقات وخروجها.", "state", ["loc_control"], 1)
F("f_audit_available", "أرشيف الإطارات يحتفظ بسجل تدقيق لكل تعديل في وسوم الملفات.", "state", ["loc_archive"], 1)
F("f_reem_warning", "تلقّت ريم قبل أشهر تنبيهاً إدارياً لاستخدامها الكاميرا خارج الجدول المعتمد.", "event", ["reem"], 1)
F("f_bulletin_declared", "صرّح هشام في استمارة البلاغ بأنه لا يعلم بأي رصد أسبق لرصده.", "event", ["hisham"], 1, T(63), "loc_control")
F("f_reem_frame_time", "التقطت كاميرا المسح الإطار الأول الذي يظهر فيه الجسم الساعة 21:10 UTC.", "event", ["reem", "obj_cam", "obj_frame"], 2, T(10), "loc_dome", ["KO-FC-04-024"])
F("f_hisham_frame_time", "التقط المقراب T1 أول إطار لهشام الساعة 21:34 UTC.", "event", ["hisham", "obj_t1"], 2, T(34), "loc_control")
F("f_chat_sent", "أرسلت ريم إلى هشام رسالة مرفقة بالإطار الساعة 21:21 UTC (00:21 محلياً).", "event", ["reem", "hisham"], 2, T(21), "loc_dome")
F("f_chat_seen", "ظهر إيصال قراءة هشام للرسالة الساعة 21:27 UTC (00:27 محلياً).", "event", ["hisham"], 2, T(27), "loc_control")
F("f_ws_open", "فتح الحساب hmansour على المحطة CR-2 ملف إطار ريم الساعة 21:24 UTC، بعد دخوله ببطاقته.", "event", ["hisham", "obj_cr2", "obj_frame"], 2, T(24), "loc_control")
F("f_yusuf_saw", "شاهد يوسف هشاماً يفتح إطار المسح ويعلّق على جسم جديد قبل أن يوجّه المقراب، دون تحديد دقيق للوقت.", "event", ["yusuf", "hisham"], 2, T(25, "approx"), "loc_control")
F("f_alone_in_room", "غادر يوسف غرفة التحكم الساعة 22:05 UTC (01:05 محلياً) وبقي هشام وحده فيها حتى بعد التعديل.", "event", ["yusuf", "hisham"], 2, T(65), "loc_control")
F("f_reem_first", "إطار ريم سابق لإطار هشام بنحو 24 دقيقة.", "relation", ["reem", "hisham"], 3, T(10, "exact", 34), None, ["KO-RS-05-005", "KO-FC-04-024"])
F("f_hisham_aware", "علم هشام بإطار ريم قبل التقاط إطاره وقبل إرسال بلاغه، ثم لم يذكره في البلاغ.", "state", ["hisham"], 3, T(24, "exact", 63), "loc_control", ["KO-RS-06-017"])
F("f_relabel", "عُدّل وسم إطار ريم يدوياً من محطة CR-2 بحساب hmansour بعد البلاغ، من «جسم مرشّح» إلى «حقل روتيني».", "event", ["hisham", "obj_cr2", "obj_frame"], 3, T(72), "loc_control", ["KO-FC-04-026"])

claims = [
    {"id": "cl_h_unaware", "statement_ar": "لم أعلم بأي رصد سابق لرصدي قبل أن ألتقط إطاري وأرسل البلاغ.", "kind": "lie", "held_by": ["hisham"], "true_fact_id": "f_hisham_aware", "contradicted_by_evidence_ids": ["ev_chat_log", "ev_ws_log"]},
    {"id": "cl_h_clock", "statement_ar": "ساعة كاميرا المسح لم تكن موثوقة تلك الليلة.", "kind": "half_truth", "held_by": ["hisham"], "true_fact_id": "f_clock_gps", "contradicted_by_evidence_ids": ["ev_sync_report", "ev_reem_hdr"]},
    {"id": "cl_h_auto", "statement_ar": "تعديل الوسم جرى آلياً من نظام الأرشفة.", "kind": "lie", "held_by": ["hisham"], "true_fact_id": "f_relabel", "contradicted_by_evidence_ids": ["ev_audit_relabel", "ev_door_log"]},
    {"id": "cl_reem_late", "statement_ar": "إطار ريم وصل بعد إطار هشام.", "kind": "honest_mistake", "held_by": ["nadir"], "true_fact_id": "f_reem_first", "contradicted_by_evidence_ids": ["ev_reem_hdr", "ev_lab_norm"]},
]

# ---------------------------------------------------------------- timeline
timeline = []
def E(id, desc, m, loc, actors, facts_, mot=None, wit=None, end=None, prec="exact", cause=None):
    d = {"id": id, "description_ar": desc, "time": T(m, prec, end), "actor_ids": actors, "fact_ids": facts_}
    if loc: d["location_id"] = loc
    if mot: d["motivated_by_ar"] = mot
    if wit: d["witness_ids"] = wit
    if cause: d["caused_by_event_ids"] = cause
    timeline.append(d)

E("te_sync", "أمينة الأرشيف تجري الفحص الدوري للمزامنة وتوثّق تأخر خادم الأرشيف.", -60, "loc_archive", ["salma"], ["f_archive_lag"], "إجراء روتيني أسبوعي")
E("te_frame_reem", "كاميرا المسح تلتقط الإطار الأول الذي يظهر فيه الجسم.", 10, "loc_dome", ["reem"], ["f_reem_frame_time", "f_new_object"], "مسح روتيني لحقل المسح 17", ["yusuf"])
E("te_log_yusuf", "يوسف يدوّن وصول إطار جديد في سجل التشغيل.", 10, "loc_control", ["yusuf"], ["f_yusuf_logged"], "واجب المشغّل تدوين كل إطار يصل")
E("te_chat_sent", "ريم ترسل الإطار إلى هشام وتخبره بوجود جسم جديد.", 21, "loc_dome", ["reem"], ["f_chat_sent"], "تريد التأكد من الجسم قبل أن تعلن شيئاً")
E("te_ws_open", "هشام يفتح ملف إطار ريم على المحطة CR-2.", 24, "loc_control", ["hisham"], ["f_ws_open", "f_yusuf_saw"], "يريد التحقق من الإطار بنفسه", ["yusuf"])
E("te_chat_seen", "إيصال القراءة يظهر لرسالة ريم.", 27, "loc_control", ["hisham"], ["f_chat_seen"], "فتح تطبيق المراسلة على المحطة")
E("te_frame_hisham", "المقراب T1 يلتقط إطار هشام الأول.", 34, "loc_control", ["hisham"], ["f_hisham_frame_time"], "التأكد بمقرابه قبل الإبلاغ")
E("te_bulletin", "هشام يرسل البلاغ إلى النشرة الدولية بصفته المكتشف.", 63, "loc_control", ["hisham"], ["f_bulletin_declared"], "الأسبقية تُنسب لأول مُبلِّغ")
E("te_yusuf_leaves", "يوسف يغادر غرفة التحكم.", 65, "loc_control", ["yusuf"], ["f_alone_in_room"], "انتهاء مناوبته المبكرة")
E("te_press", "نادر يكتب ملاحظة اللوحة منقولاً فيها وقت الأرشيف دون منطقته الزمنية.", 100, "loc_press", ["nadir"], ["f_press_note_local"], "تجهيز البيان الصحفي بسرعة")
E("te_relabel", "تعديل وسم إطار ريم يدوياً من CR-2.", 72, "loc_control", ["hisham"], ["f_relabel"], "تعديل الوسم يجعل الإطار يبدو روتينياً")

# ---------------------------------------------------------------- evidence
ev = []
def V(id, title, kind, content, acts, supports, rel, limits, contradicts=None, red=False, ko=None, loc=None):
    d = {"id": id, "title_ar": title, "kind": kind, "content_ar": content, "acquired_by_action_ids": acts, "supports_fact_ids": supports, "reliability": rel, "limits_ar": limits}
    if contradicts: d["contradicts_claim_ids"] = contradicts
    if red: d["is_red_herring"] = True
    if ko: d["forensic_ko_ref"] = ko
    if loc: d["location_id"] = loc
    ev.append(d)

V("ev_bulletin_form", "استمارة بلاغ الاكتشاف (نسخة المرصد)", "documentary",
  "استمارة بلاغ اكتشاف — النشرة الفلكية الدولية\nرقم البلاغ: WN-2291\nالجهة المبلِّغة: مرصد وادي النجوم\nالمبلِّغ: د. هشام المنصور\nالحقل: مسح 17\nأول رصد مسجَّل: 21:34:40 بالتوقيت العالمي (UTC) — المقراب T1\nوقت إرسال البلاغ: 22:03 UTC\nإقرار المبلِّغ: «أقرّ بأنني لا أعلم بأي رصد أسبق لهذا الجسم، وأن ما أوردته مبنيّ على معرفتي المباشرة.»",
  ["a_read_bulletin"], ["f_bulletin_declared", "f_hisham_frame_time"], "strong",
  "تثبت ما صرّح به المبلِّغ في الاستمارة، لا صحة هذا التصريح؛ الإقرار قولٌ يحتاج مقابلته بسجلات أخرى.", loc="loc_committee")

V("ev_reem_warning", "مذكرة إدارية: تنبيه لمتدربة", "documentary",
  "برنامج المتدربين — مذكرة داخلية\nإلى: ريم الخزرجي\nالموضوع: تنبيه كتابي\nاستخدمتِ كاميرا المسح خارج الجدول المعتمد في تموز الماضي. هذا تنبيه أول ولا إجراء إضافي.\nالتوقيع: إدارة البرنامج",
  ["a_read_hr"], ["f_reem_warning"], "weak",
  "تتعلق بمخالفة جدولة سابقة؛ لا علاقة لها بصحة الوقت المسجَّل في رأس ملف ليلة الحادثة، ولا تقول شيئاً عن صدق أحد.",
  red=True, loc="loc_committee")

V("ev_obs_log", "سجل التشغيل الليلي — غرفة التحكم", "documentary",
  "سجل التشغيل الليلي — غرفة التحكم\n(يُكتب بالتوقيت العالمي UTC؛ توقيت المرصد المحلي = UTC+3)\nالمشغّل: يوسف السالم\n20:55  بدء الجلسة. سماء صافية.\n21:10  وصل إطار جديد من كاميرا المسح (حقل 17). يظهر فيه جسم غير مدرج في الفهرس.\n21:34  د. هشام يوجّه المقراب T1 إلى الحقل 17.\n22:05  مغادرة المشغّل مبكراً بإذن.",
  ["a_search_control"], ["f_yusuf_logged", "f_local_tz"], "moderate",
  "سجل مكتوب يدوياً بأصبع المشغّل في اللحظة؛ دقّته في الدقيقة لا الثانية، وهو يعتمد على أمانة كاتبه.", loc="loc_control")

V("ev_press_board", "ورقة على لوحة مكتب الإعلام", "documentary",
  "[بخط اليد، حبر أزرق]\nملاحظة سريعة قبل البيان الصحفي:\n– رصد د. هشام (المقراب T1): 21:34\n– إطار الطالبة ريم (كاميرا المسح): وصل 00:06 (من الأرشيف)\n⇒ إطار ريم لاحق. لا داعي لذكره في البيان.\n— ن.",
  ["a_search_press"], ["f_press_note_local"], "weak",
  "ملاحظة بخط اليد تنقل رقمين من مصدرين مختلفين دون ذكر المنطقة الزمنية لأي منهما؛ لا تدل بنفسها على ترتيب الأحداث.",
  red=True, loc="loc_press")

V("ev_archive_log", "سجل استقبال خادم الأرشيف", "digital",
  "سجل استقبال خادم الأرشيف ARCH-1\n(عرض الوقت: محلي — كما تظهر على الشاشة)\n00:06:31  INGEST  survey17/field17_reem_0001.fits  48.2 MB  OK\n00:06:33  INDEX   object_flag = NEW_CANDIDATE\n00:06:40  NOTIFY  duty_operator\nتنبيه أسفل الشاشة: راجع تقرير المزامنة الأخير لهذا الخادم.",
  ["a_search_archive"], ["f_reem_frame_time"], "moderate",
  "يسجّل وقت وصول الملف إلى الخادم لا وقت التقاطه، ويعرض الوقت بساعة الخادم نفسه.", loc="loc_archive")

V("ev_sync_report", "تقرير فحص المزامنة الدوري", "documentary",
  "تقرير فحص المزامنة الدوري — خوادم المرصد\nالمسؤولة: س. العطار — وقت الفحص: 20:00 UTC (قبل ساعات من الحادثة)\nARCH-1 (الأرشيف، يعرض محلياً): متأخر عن المرجع بمقدار 4 دقائق 00 ثانية — لم يُصحَّح بعد\nCAM-SURVEY (حاسوب كاميرا المسح): مقفل على GPS — انحراف 0.2 ثانية\nCR-2 (محطة غرفة التحكم): NTP — انحراف 0.4 ثانية\nCHAT (خادم المراسلة، يعرض محلياً): NTP — انحراف 0.3 ثانية",
  ["a_get_sync"], ["f_archive_lag", "f_clock_gps"], "strong",
  "يصف حالة الأجهزة وقت الفحص قبل الحادثة بساعات؛ لا يثبت أن الانحراف بقي ثابتاً بعد ذلك، لكنه أفضل مرجع متاح.",
  contradicts=["cl_h_clock"], ko="KO-FC-04-024", loc="loc_archive")

V("ev_reem_hdr", "رأس ملف إطار ريم (نسخة مطابقة)", "digital",
  "رأس ملف field17_reem_0001.fits — نسخة مطابقة من الأرشيف\nTELESCOP = SURVEY-CAM-B\nDATE-OBS = 2026-03-14T21:10:12.4\nTIMESYS  = UTC (GPS-locked)\nEXPTIME  = 30.0\nOBJECT   = FIELD17_SURVEY\nANALYSIS = نقطة مصدرية جديدة عند (412, 877)، سطوعها 14.8، غير موجودة في الإطار المرجعي",
  ["a_get_reem_file"], ["f_reem_frame_time", "f_clock_gps"], "strong",
  "يثبت وقت التقاط الإطار على ساعة الكاميرا، ولا يقول من لاحظ الجسم أولاً بعينه ولا شيئاً عن نوايا أحد؛ ويفترض أن الملف لم يُغيَّر منذ التقاطه.",
  contradicts=["cl_h_clock", "cl_reem_late"], ko="KO-FC-04-024", loc="loc_dome")

V("ev_hisham_hdr", "رأس ملف إطار المقراب T1", "digital",
  "رأس ملف field17_t1_0001.fits\nTELESCOP = T1-MAIN\nDATE-OBS = 2026-03-14T21:34:40.1\nTIMESYS  = UTC (NTP)\nEXPTIME  = 60.0\nOBSERVER = h.mansour\nANALYSIS = نقطة مصدرية عند الإحداثيات نفسها تقريباً، سطوعها 14.7",
  ["a_inspect_t1"], ["f_hisham_frame_time"], "strong",
  "يثبت وقت إطار هشام وحده؛ لا يقول ماذا كان يعلم قبله.", ko="KO-FC-04-024", loc="loc_control")

V("ev_chat_log", "تصدير سجل المراسلة الداخلية", "digital",
  "تصدير سجل المراسلة الداخلية — قناة «رصد-ليلي»\n(يعرض الوقت المحلي UTC+3)\n[00:21] ريم الخزرجي: د. هشام، في الحقل 17 جسم جديد غير موجود في المرجع. أرفقت الإطار: field17_reem_0001.fits\n[00:27] ✓ تمت القراءة — هشام المنصور\n[00:28] ريم الخزرجي: هل تريد أن أعيد التقاط إطار ثانٍ؟\n(لا ردّ مسجَّل حتى 02:00)",
  ["a_get_chat"], ["f_chat_sent", "f_chat_seen"], "moderate",
  "إيصال القراءة يثبت فتح الرسالة لا فهم مضمونها ولا فتح المرفق؛ وهو سجل خادم لا شهادة شخص.",
  contradicts=["cl_h_unaware"], loc="loc_dome")

V("ev_ws_log", "سجل فتح الملفات — المحطة CR-2", "digital",
  "سجل دخول وفتح الملفات — محطة غرفة التحكم CR-2\n(الوقت المحلي UTC+3)\n00:19:44  LOGIN   hmansour (بطاقة شخصية)\n00:24:05  OPEN    /survey17/field17_reem_0001.fits   (قراءة)\n00:24:50  OPEN    /survey17/ref_field17.fits         (قراءة)\n00:31:20  SLEW    T1 → field17                        (hmansour)\n00:34:40  EXPOSE  T1 start                            (hmansour)",
  ["a_get_ws"], ["f_ws_open", "f_hisham_frame_time"], "strong",
  "يثبت أن الحساب فتح الملف لا أن صاحبه فحصه ولا ماذا استنتج؛ ويعتمد على أن الحساب لم يستخدمه غير صاحبه، وهو دخول ببطاقة شخصية.",
  contradicts=["cl_h_unaware"], loc="loc_control")

V("ev_audit_relabel", "سجل التدقيق في الأرشيف", "digital",
  "سجل التدقيق — خادم الأرشيف ARCH-1\n(عرض الوقت: محلي — الخادم متأخر 4 دقائق حسب آخر فحص)\n01:08:09  META_EDIT  field17_reem_0001.fits   OBJECT_FLAG: NEW_CANDIDATE → FIELD17_ROUTINE   by: hmansour   terminal: CR-2   method: manual\n01:08:41  INDEX_REBUILD  survey17   by: system\nملاحظة: لا توجد مهام مجدولة أو برامج آلية مضبوطة على تغيير الوسوم.",
  ["a_get_audit"], ["f_relabel"], "strong",
  "يسجّل من غيّر الوسم ومن أي محطة وكيف، لا سبب التغيير ولا نية صاحبه.",
  contradicts=["cl_h_auto"], ko="KO-FC-04-026", loc="loc_archive")

V("ev_door_log", "سجل بوابة غرفة التحكم", "documentary",
  "سجل قارئ البطاقات — بوابة غرفة التحكم\n(الوقت المحلي؛ القارئ مزامن)\n23:50  دخول — Y. Salem\n00:02  دخول — H. Mansour\n01:05  خروج — Y. Salem\n01:31  خروج — H. Mansour\nلا دخول آخر بين 00:02 و01:31.",
  ["a_get_door"], ["f_alone_in_room"], "strong",
  "يثبت من دخل وخرج ومتى، لا ما فعله داخل الغرفة؛ ولا يغطي من استعار بطاقة غيره.",
  contradicts=["cl_h_auto"], loc="loc_control")

V("ev_sheet", "ورقة رصد ورقية مكتوبة بالقلم", "physical",
  "ورقة رصد T1 مطبوعة، كُتب عليها بالقلم:\n«00:34 — حقل 17 — جسم جديد؟ (إطار ريم؟)»\nخطٌّ واحد مرسوم فوق عبارة «(إطار ريم؟)» تبقى كلماتها مقروءة.\nلا توقيع ولا تاريخ على الورقة.",
  ["a_search_desk"], ["f_hisham_aware"], "weak",
  "الورقة غير موقّعة ولا مؤرَّخة، ولا يمكن نسب خطّها إلى كاتب بالمقارنة العينية وحدها؛ فهي مؤشر يوجّه البحث لا دليل يكفي لإثبات علم أحد.",
  ko="KO-FC-04-017", loc="loc_control")

V("ev_yusuf_statement", "إفادة يوسف السالم (ملخص)", "testimonial",
  "ملخص إفادة يوسف السالم، دوّنه أمين اللجنة:\n«رأيت د. هشام يفتح إطار المسح على محطته ويعلّق على جسم جديد قبل أن يوجّه المقراب، على ما أذكر. لا أجزم بالدقائق، فقد كنت مشغولاً بالأجهزة.»",
  ["a_note_yusuf"], ["f_yusuf_saw"], "moderate",
  "ذاكرة شاهد عن ترتيب دقائق قبل أشهر؛ مفيدة للاتجاه لا للدقيقة.", loc="loc_control")

V("ev_nadir_statement", "إفادة نادر الجابري (ملخص)", "testimonial",
  "ملخص إفادة نادر الجابري، دوّنه أمين اللجنة:\n«نقلت الرقمين كما رأيتهما: 21:34 من د. هشام، و00:06 من شاشة الأرشيف. لم أنتبه أن أحدهما بالتوقيت العالمي والآخر محلي.»",
  ["a_note_nadir"], ["f_press_note_local"], "weak",
  "إفادة شخص يصف خطأه هو؛ لا تثبت وحدها عدم التلاعب، وإنما ينبغي أن يؤيدها فحص الأزمنة.", loc="loc_press")

V("ev_lab_norm", "تقرير توحيد الأزمنة", "lab_result",
  "تقرير مختبر الأزمنة: بعد تحويل كل وقت إلى التوقيت العالمي وتصحيح انحراف الساعة المسجَّل، تتوافق السجلات الثلاثة (سجل التشغيل، لوحة الإعلام، سجل الأرشيف) عند 21:10 UTC بفارق أقل من دقيقتين. أي أن الفارق الظاهر بين «21:10» و«00:10» ناتج عن اختلاف المنطقة الزمنية لا عن اختلاف الحدث.",
  ["a_compare_times"], ["f_reem_frame_time"], "strong",
  "نتيجة حسابية تعتمد على صحة المدخلات (الإزاحة والانحراف)؛ توحّد الأزمنة ولا تثبت وحدها من لاحظ أولاً أو ماذا علم أحد.",
  contradicts=["cl_reem_late"], ko="KO-FC-04-024", loc="loc_committee")

# ---------------------------------------------------------------- inferences
def P(t, i): return {"ref_type": t, "ref_id": i}
inf = []
def I(id, prem, concl_type, concl, rel, strength, rule, ks):
    inf.append({"id": id, "premises": prem, "conclusion": {"ref_type": concl_type, "ref_id": concl}, "relation": rel, "strength": strength, "rule_ar": rule, "skill_ko_refs": ks})

I("i_hdr_order", [P("evidence", "ev_reem_hdr"), P("evidence", "ev_hisham_hdr"), P("general_knowledge", "utc_common_reference")], "fact", "f_reem_first", "establishes", "conclusive",
  "رأسا الملفين مكتوبان بالتوقيت العالمي نفسه وبساعتين مضبوطتين؛ فمقارنة 21:10:12 بـ 21:34:40 مقارنة مباشرة بين لحظتين على مرجع واحد.", ["KO-RS-06-017", "KO-FC-04-024"])
I("i_lab_order", [P("evidence", "ev_lab_norm"), P("evidence", "ev_bulletin_form")], "fact", "f_reem_first", "establishes", "strong",
  "بعد توحيد المناطق الزمنية وتصحيح انحراف الساعة تصير كل السجلات تضع إطار ريم عند 21:10 UTC، وتصريح هشام نفسه يضع إطاره عند 21:34 UTC.", ["KO-RS-05-005", "KO-FC-04-024"])
I("i_aware_chat", [P("evidence", "ev_chat_log"), P("evidence", "ev_hisham_hdr"), P("general_knowledge", "local_utc_plus_3")], "fact", "f_hisham_aware", "establishes", "strong",
  "الوقت المحلي ناقص ثلاث ساعات يساوي UTC: إيصال القراءة 00:27 محلياً هو 21:27 UTC، أي قبل التقاط هشام لإطاره 21:34 UTC.", ["KO-FC-04-024", "KO-RS-06-001"])
I("i_aware_ws", [P("evidence", "ev_ws_log"), P("evidence", "ev_bulletin_form")], "fact", "f_hisham_aware", "establishes", "strong",
  "سجل المحطة مستقل عن المراسلة: فتح ملف إطار ريم 00:24 محلياً (21:24 UTC)، أي قبل إطار هشام وقبل بلاغه.", ["KO-FC-04-024", "KO-RS-05-004"])
I("i_unaware_false", [P("fact", "f_hisham_aware"), P("evidence", "ev_bulletin_form")], "claim", "cl_h_unaware", "contradicts_claim", "conclusive",
  "إقرار عدم العلم يتعارض مع واقعة علمه المسجَّلة بسجلين مستقلين؛ فهو قول يخالف السجلات لا مجرد نسيان.", ["KO-RS-05-014"])
I("i_clock_false", [P("evidence", "ev_sync_report"), P("evidence", "ev_reem_hdr")], "claim", "cl_h_clock", "contradicts_claim", "strong",
  "الذي كان متأخراً هو خادم الأرشيف (بـ4 دقائق) لا حاسوب الكاميرا، وهو مقفل على GPS؛ فالقول إن ساعة الكاميرا غير موثوقة نصف حقيقة.", ["KO-RS-06-003"])
I("i_relabel_fact", [P("evidence", "ev_audit_relabel"), P("evidence", "ev_door_log")], "fact", "f_relabel", "establishes", "strong",
  "سجل التدقيق يقول إن التعديل يدوي من المحطة CR-2 بحساب hmansour، وسجل البوابة يقول إن هشاماً كان وحده في الغرفة وقت التعديل.", ["KO-FC-04-026"])
I("i_auto_false", [P("evidence", "ev_audit_relabel"), P("evidence", "ev_door_log")], "claim", "cl_h_auto", "contradicts_claim", "strong",
  "حقل method يقول manual، ولا توجد مهام آلية مضبوطة على الوسوم؛ فالتعديل لم يكن آلياً.", ["KO-RS-05-014"])
I("i_late_false", [P("fact", "f_reem_first")], "claim", "cl_reem_late", "contradicts_claim", "conclusive",
  "إذا كان إطار ريم سابقاً بحسب السجلات الموحّدة فالقول إنه وصل لاحقاً خطأ ناتج عن قراءة أزمنة غير موحّدة.", ["KO-RS-06-004"])
I("i_support_hisham", [P("fact", "f_reem_first"), P("fact", "f_hisham_aware")], "hypothesis", "h_hisham", "supports", "strong",
  "سبق إطار ريم، وعلم هشام به قبل إطاره، وصرّح مع ذلك بعدم العلم؛ هذه الوقائع الثلاث تُنتج معاً أرجح تفسير، من غير أن تقول شيئاً عن دافعه.", ["KO-RS-05-002", "KO-RS-06-007"])
I("i_concealment", [P("fact", "f_relabel")], "hypothesis", "h_hisham", "supports", "suggestive",
  "تغيير وسم إطار ريم من «مرشّح» إلى «روتيني» بعد البلاغ بيد هشام يتسق مع إخفاء الإطار لا مع التصحيح التقني.", ["KO-RS-06-001"])
I("i_rule_reem_false", [P("fact", "f_reem_first")], "hypothesis", "h_reem_false", "rules_out", "conclusive",
  "فرضية أن ريم اختلقت سبقاً تسقط إذا كانت رؤوس الملفين المستقلة وسجلات الخوادم تؤيد أن إطارها هو الأسبق.", ["KO-RS-06-008"])
I("i_rule_nadir", [P("evidence", "ev_lab_norm")], "hypothesis", "h_nadir", "rules_out", "strong",
  "الرقم الذي بدا متناقضاً في لوحة الإعلام يتطابق بعد توحيد المناطق وتصحيح الانحراف مع السجلين الآخرين؛ فهو خطأ نقل لا تزوير.", ["KO-RS-06-008", "KO-FC-04-024"])
I("i_rule_nadir_b", [P("evidence", "ev_audit_relabel"), P("evidence", "ev_door_log")], "hypothesis", "h_nadir", "rules_out", "strong",
  "التعديل الوحيد المثبت على سجل جرى بحساب هشام من محطة في غرفة التحكم لا يظهر في سجل بوابتها أي دخول لنادر؛ فلا شيء يربط مسؤول الإعلام بتعديل سجل.", ["KO-RS-06-008", "KO-FC-04-026"])
I("i_rule_parallel", [P("fact", "f_hisham_aware")], "hypothesis", "h_parallel", "rules_out", "strong",
  "فرضية الاكتشاف المستقل المتزامن تقتضي أن لا يكون هشام قد اطّلع على إطار ريم قبل إطاره، وهذا ما تنفيه واقعة علمه.", ["KO-RS-06-008"])

# ---------------------------------------------------------------- knowledge
def K(fid, access, cert="certain", src=None):
    d = {"fact_id": fid, "access": access, "certainty": cert}
    if src: d["source_character_id"] = src
    return d
ck = [
    {"character_id": "reem", "knows": [K("f_reem_frame_time", "witnessed"), K("f_clock_gps", "professional"), K("f_chat_sent", "witnessed"), K("f_chat_seen", "witnessed"), K("f_reem_file_shared", "witnessed"), K("f_reem_warning", "witnessed")], "hides": [], "believes": []},
    {"character_id": "hisham", "knows": [K("f_hisham_frame_time", "witnessed"), K("f_bulletin_declared", "witnessed")],
     "hides": [
        {"fact_id": "f_hisham_aware", "reveal_when": {"any": [{"presented": {"evidence_id": "ev_chat_log", "to_character": "hisham"}}, {"presented": {"evidence_id": "ev_ws_log", "to_character": "hisham"}}]}, "cover_claim_id": "cl_h_unaware", "reveal_line_id": "h_break_aware"},
        {"fact_id": "f_relabel", "reveal_when": {"all": [{"presented": {"evidence_id": "ev_audit_relabel", "to_character": "hisham"}}, {"presented": {"evidence_id": "ev_door_log", "to_character": "hisham"}}]}, "cover_claim_id": "cl_h_auto", "reveal_line_id": "h_break_relabel"},
     ],
     "believes": [{"claim_id": "cl_h_unaware", "stance": "deliberate_lie"}, {"claim_id": "cl_h_clock", "stance": "deliberate_lie"}, {"claim_id": "cl_h_auto", "stance": "deliberate_lie"}]},
    {"character_id": "yusuf", "knows": [K("f_yusuf_logged", "witnessed"), K("f_local_tz", "common_knowledge"), K("f_yusuf_saw", "witnessed", "fairly_sure"), K("f_ws_logs_exist", "professional"), K("f_badge_exists", "professional"), K("f_alone_in_room", "witnessed")], "hides": [], "believes": []},
    {"character_id": "nadir", "knows": [K("f_press_note_local", "witnessed")], "hides": [], "believes": [{"claim_id": "cl_reem_late", "stance": "sincere"}]},
    {"character_id": "salma", "knows": [K("f_archive_lag", "professional"), K("f_local_tz", "common_knowledge"), K("f_audit_available", "professional")], "hides": [], "believes": []},
]

# ---------------------------------------------------------------- hypotheses / misdirection
hyps = [
    {"id": "h_hisham", "statement_ar": "هشام علم بإطار ريم السابق قبل إطاره، ونسب الاكتشاف إلى نفسه وأخفى إطارها.", "is_true": True, "plausibility_at_start": "low", "suspect_id": "hisham"},
    {"id": "h_reem_false", "statement_ar": "ريم تدّعي سبقاً لم يحدث؛ فإطارها وصل بعد إطار هشام.", "is_true": False, "plausibility_at_start": "high", "suspect_id": "reem"},
    {"id": "h_nadir", "statement_ar": "مسؤول الإعلام تلاعب بالسجلات (لوحة الإعلام أو وسم الإطار) ليخدم رواية المرصد.", "is_true": False, "plausibility_at_start": "low", "suspect_id": "nadir"},
    {"id": "h_parallel", "statement_ar": "لم يغشّ أحد: رصدان مستقلان متقاربان، والفروق في الأزمنة التباس مناطق زمنية فقط.", "is_true": False, "plausibility_at_start": "medium"},
]
mis = [
    {"id": "rh_press", "points_to_hypothesis_id": "h_reem_false", "planted_via_ar": "ورقة لوحة الإعلام تضع إطار ريم «00:06» بعد رصد هشام «21:34».", "evidence_ids": ["ev_press_board"], "refuted_by_inference_ids": ["i_lab_order", "i_rule_reem_false"], "fairness_note_ar": "كل ما يلزم لحل الالتباس موجود: المنطقة الزمنية في سجل التشغيل، وتقرير المزامنة، وسجل الأرشيف الذي يقول إن الوقت محلي."},
    {"id": "rh_warning", "points_to_hypothesis_id": "h_reem_false", "planted_via_ar": "مذكرة تنبيه سابق تُلمّح إلى أن ريم غير منضبطة.", "evidence_ids": ["ev_reem_warning"], "refuted_by_inference_ids": ["i_rule_reem_false"], "fairness_note_ar": "التنبيه عن مخالفة جدولة لا عن صدق؛ ورأس الملف سجل جهاز لا يتأثر بسمعة صاحبته."},
    {"id": "rh_nadir", "points_to_hypothesis_id": "h_nadir", "planted_via_ar": "الورقة المكتوبة بخط نادر تبدو كأنها تُقدّم رواية المرصد.", "evidence_ids": ["ev_press_board"], "refuted_by_inference_ids": ["i_rule_nadir", "i_rule_nadir_b"], "fairness_note_ar": "الرقم الذي بدا مزوّراً يتطابق بعد التوحيد مع سجلين آخرين، وسجلا التدقيق والبوابة يحددان من عدّل الوسم فعلاً."},
]

# ---------------------------------------------------------------- learning objectives / rubric
LO = [
    ("lo_source", "يصنّف الأدلة بحسب نوع مصدرها وطريقة معرفتها (سجل أصلي، نسخة معروضة، قول).", "KO-RS-05-001", ["يصنّف الورقة اليدوية كنسخة معروضة لا كسجل أصلي", "يفرّق بين الإقرار والسجل"], ["evidence_board"]),
    ("lo_time", "يوحّد أزمنة مكتوبة بمناطق زمنية وساعات مختلفة قبل مقارنتها.", "KO-RS-05-005", ["يحوّل المحلي إلى UTC", "يصحّح انحراف الساعة المعلن", "يضع الأحداث على الخط الزمني الموحّد"], ["action_log", "timeline_task"]),
    ("lo_hyp", "يوازن فرضيات متنافسة ويستبعد منها ما تنقضه الأدلة.", "KO-RS-05-002", ["يضيف أكثر من فرضية", "يستبعد فرضية بدليل مرفق"], ["hypothesis_ledger"]),
    ("lo_diag", "يقدّر القوة التشخيصية للدليل: هل يميّز بين الفرضيات أم يوافق عليها جميعاً؟", "KO-RS-06-001", ["يربط الدليل بالفرضية باتجاه صحيح", "يتجنب ربط الدليل الضعيف كحاسم"], ["evidence_board", "final_justification"]),
    ("lo_calib", "يعبّر عن ثقته بحدودها ويحدّد ما قد يغيّر رأيه.", "KO-RS-06-021", ["يختار ثقة معقولة", "يذكر حدود الأدلة", "يحدد دليلاً مغيّراً للرأي"], ["final_justification", "hypothesis_ledger"]),
    ("lo_revise", "يراجع فرضيته الأولى عند سقوط الدليل الذي بُنيت عليه.", "KO-RS-06-009", ["يعلن فرضية رائدة ثم يغيّرها بعد دليل جديد"], ["hypothesis_ledger", "action_log"]),
]
los = [{"id": a, "statement_ar": b, "skill_ko_ref": c, "observable_behaviors_ar": d, "evidence_sources": e} for a, b, c, d, e in LO]

def levels(desc):
    return [{"score": i, "descriptor_ar": d} for i, d in enumerate(desc)]

rub = {
    "reference_answer_ar": "أول إطار يُظهر الجسم هو إطار ريم عند 21:10 UTC، ويسبق إطار هشام عند 21:34 UTC بنحو 24 دقيقة. يظهر هذا من رأسي الملفين مباشرة، ومن توحيد السجلات الثلاثة التي بدت متناقضة (سجل التشغيل بالتوقيت العالمي، ولوحة الإعلام والأرشيف بالمحلي، والأرشيف متأخر 4 دقائق). وقد علم هشام بالإطار قبل إطاره: فتح ملفه 21:24 UTC وقرأ رسالتها 21:27 UTC، ثم صرّح في البلاغ بعدم علمه بأي رصد أسبق، وعدّل وسم الإطار يدوياً من محطته وهو وحده في الغرفة. أرجح تفسير أنه نسب الاكتشاف إلى نفسه وأخفى إطارها. والحدود: لا تثبت الأدلة دافعه ولا ما أدركه حين فتح الإطار، ولا تقرر هي أسبقية الاكتشاف رسمياً؛ ذلك قرار اللجنة الدولية.",
    "criteria": [
        {"id": "c_source", "name_ar": "تصنيف المصادر", "objective_ids": ["lo_source"], "scored_by": "deterministic", "weight": 0.15,
         "levels": levels(["لم يصنّف شيئاً", "صنّف قليلاً وأخطأ في الغالب", "صنّف نصف الأدلة بدقة", "صنّف معظمها بدقة", "صنّف كل الأدلة الأساسية بدقة وفرّق بين القول والسجل"])},
        {"id": "c_conflict", "name_ar": "حل تعارض الأزمنة", "objective_ids": ["lo_time"], "scored_by": "deterministic", "weight": 0.25,
         "levels": levels(["تجاهل التعارض", "لاحظه دون حل", "حاول الحل بمدخلات غير متسقة", "وحّد الأزمنة في المختبر", "وحّدها في المختبر ووضع الأحداث على الخط الزمني بالتوقيت الموحّد"])},
        {"id": "c_links", "name_ar": "ربط الأدلة بالفرضيات", "objective_ids": ["lo_diag"], "scored_by": "deterministic", "weight": 0.15,
         "levels": levels(["لا روابط", "روابط قليلة أو معظمها خاطئ", "نصف الروابط صحيح", "معظم الروابط صحيح مع مقارنة فرضيتين", "روابط دقيقة عبر عدة فرضيات"])},
        {"id": "c_uncertainty", "name_ar": "معايرة الثقة وحدود الاستنتاج", "objective_ids": ["lo_calib"], "scored_by": "deterministic", "weight": 0.15,
         "levels": levels(["ثقة مفرطة بلا حدود", "حدود قليلة أو غير ملائمة", "ثقة معقولة مع حدود جزئية", "ثقة معقولة وحدود صحيحة", "ثقة معايَرة وحدود كاملة ودليل مغيّر للرأي"])},
        {"id": "c_revision", "name_ar": "مراجعة الرأي", "objective_ids": ["lo_revise"], "scored_by": "deterministic", "weight": 0.1,
         "levels": levels(["بقي على فرضية تنقضها الأدلة", "لم يعلن فرضية", "ثبت على فرضية سليمة", "غيّر موقفه بعد دليل", "غيّر موقفه بعد دليل ووثّق المراجعة"])},
        {"id": "c_elimination", "name_ar": "استبعاد الفرضيات الخاطئة", "objective_ids": ["lo_hyp"], "scored_by": "deterministic", "weight": 0.1,
         "levels": levels(["لم يستبعد", "استبعد خطأً", "استبعد فرضية واحدة بدليل", "استبعد فرضيتين بدليل", "استبعد كل الفرضيات الخاطئة بأدلة مرفقة"])},
        {"id": "c_justification", "name_ar": "جودة الحجة المكتوبة", "objective_ids": ["lo_diag", "lo_hyp"], "scored_by": "human", "weight": 0.1,
         "levels": levels(["لا حجة", "ادعاء بلا سند", "ذكر أدلة دون ربط", "ربط الأدلة بالاستنتاج", "ربط الأدلة بالاستنتاج مع ذكر البدائل وما لا تثبته الأدلة"])},
    ],
}

# ---------------------------------------------------------------- hints
def H(id, lv, kind, text, trig, target=None, w=0.0):
    d = {"id": id, "level": lv, "kind": kind, "text_ar": text, "trigger": trig, "assessment_weight": w}
    if target: d["targets_inference_id"] = target
    return d
he = lambda e: {"has_evidence": e}
hints = [
    H("hg1", 1, "metacognitive", "اسأل نفسك: هل كُتبت كل الأزمنة في هذه الأوراق بالمنطقة الزمنية نفسها؟ وما الذي يدلّك على ذلك؟", {"always": True}, None, 0.02),
    H("hg2", 2, "focus_area", "قارن بين السجلات التي تصف اللحظة نفسها، وانظر إلى ما يُكتب بجانب كل وقت: من كتبه، وبأي توقيت، وبأي ساعة.", he("ev_press_board"), None, 0.04),
    H("hg3", 3, "pointer", "ابحث عمّن يعرف حال ساعات الخوادم، ثم جرّب مختبر الأزمنة بعد أن تجمع ما يلزمه.", he("ev_archive_log"), None, 0.06),
    H("hl1", 1, "metacognitive", "هل بين أدلتك ما يخبرك بمقدار تأخر ساعة الأرشيف؟", he("ev_archive_log"), "i_lab_order", 0.02),
    H("hl2", 2, "focus_area", "الفرق بين سجل التشغيل واللوحة يكاد يكون ثلاث ساعات بالضبط. ماذا يعني ذلك؟", he("ev_sync_report"), "i_lab_order", 0.04),
    H("hl3", 3, "pointer", "حوّل كل وقت محلي إلى UTC بطرح 3 ساعات، ثم أضف دقائق التأخر إن كان الجهاز متأخراً.", he("ev_sync_report"), "i_lab_order", 0.08),
    H("hl4", 4, "partial_reveal", "بعد التحويل يتفق سجلان بسرعة؛ فإن لم يتفق الثالث فراجع تصحيح ساعة الأرشيف: هل هو متأخر أم متقدم؟", he("ev_sync_report"), "i_lab_order", 0.12),
    H("hc1", 1, "metacognitive", "ما الذي يثبته إيصال القراءة وما الذي لا يثبته؟", he("ev_chat_log"), "i_aware_chat", 0.02),
    H("hc2", 2, "pointer", "قارن وقت القراءة بعد تحويله إلى UTC بوقت أول إطار لهشام.", he("ev_hisham_hdr"), "i_aware_chat", 0.06),
    H("hc3", 3, "partial_reveal", "سجل المحطة يضيف مصدراً مستقلاً عن المراسلة؛ هل تتفق رواية السجلين على الترتيب؟", he("ev_ws_log"), "i_aware_chat", 0.1),
    H("ha1", 1, "metacognitive", "اقرأ حقل method جيداً. ماذا يقول عن طريقة التعديل؟", he("ev_audit_relabel"), "i_auto_false", 0.02),
    H("ha2", 2, "pointer", "قارن وقت التعديل بتوقيت خروج المشغّل من الغرفة في سجل البوابة.", he("ev_door_log"), "i_auto_false", 0.06),
]

# ---------------------------------------------------------------- actions
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
Act("a_read_bulletin", "examine", "اقرأ استمارة بلاغ الاكتشاف", al, [G("ev_bulletin_form")], "ev_bulletin_form", "READ_BULLETIN")
Act("a_read_hr", "examine", "افتح ملف المتدربة في إدارة البرنامج", al, [G("ev_reem_warning")], "ev_reem_warning", "READ_HR")
Act("a_search_control", "search_location", "ابحث في سجل غرفة التحكم", al, [G("ev_obs_log")], "loc_control", "SEARCH_CONTROL")
Act("a_search_desk", "search_location", "افحص مكتب المقراب T1", al, [G("ev_sheet")], "loc_control", "SEARCH_DESK")
Act("a_inspect_t1", "examine", "افحص إطار المقراب T1", al, [G("ev_hisham_hdr")], "obj_t1", "INSPECT_T1")
Act("a_search_press", "search_location", "ابحث في لوحة مكتب الإعلام", al, [G("ev_press_board")], "loc_press", "SEARCH_PRESS")
Act("a_search_archive", "search_location", "افتح سجل استقبال الأرشيف", al, [G("ev_archive_log")], "loc_archive", "SEARCH_ARCHIVE")
for cid, lab in [("reem", "ريم"), ("yusuf", "يوسف"), ("nadir", "نادر"), ("salma", "سلمى")]:
    Act(f"a_int_{cid}", "interview", f"ابدأ مقابلة {lab}", al, [{"op": "raise_trust", "ref_id": cid, "amount": 1}], cid, f"INT_{cid.upper()}")
Act("a_int_hisham", "interview", "ابدأ مقابلة د. هشام", he("ev_bulletin_form"), [{"op": "raise_trust", "ref_id": "hisham", "amount": 1}], "hisham", "INT_HISHAM")
Act("a_get_reem_file", "examine", "تسلّم الإطار الأصلي من ريم", fu("f_reem_file_shared"), [G("ev_reem_hdr")], "obj_frame", "GET_REEM_FILE")
Act("a_get_chat", "examine", "اطلب تصدير سجل المراسلة", fu("f_chat_sent"), [G("ev_chat_log")], "reem", "GET_CHAT")
Act("a_note_yusuf", "examine", "دوّن إفادة يوسف", fu("f_yusuf_saw"), [G("ev_yusuf_statement")], "yusuf", "NOTE_YUSUF")
Act("a_note_nadir", "examine", "دوّن إفادة نادر", fu("f_press_note_local"), [G("ev_nadir_statement")], "nadir", "NOTE_NADIR")
Act("a_get_sync", "examine", "اطلب تقرير المزامنة", fu("f_archive_lag"), [G("ev_sync_report")], "salma", "GET_SYNC")
Act("a_get_ws", "examine", "اطلب سجل المحطة CR-2", fu("f_ws_logs_exist"), [G("ev_ws_log")], "obj_cr2", "GET_WS")
Act("a_get_door", "examine", "اطلب سجل بوابة غرفة التحكم", fu("f_badge_exists"), [G("ev_door_log")], "loc_control", "GET_DOOR")
Act("a_get_audit", "examine", "اطلب سجل التدقيق من الأرشيف", fu("f_audit_available"), [G("ev_audit_relabel")], "salma", "GET_AUDIT")
Act("a_compare_times", "compare_evidence", "وحِّد الأزمنة (يُمنح عبر المختبر عند نجاحه)", {"all": [he("ev_obs_log"), he("ev_press_board"), he("ev_archive_log"), he("ev_sync_report")]}, [G("ev_lab_norm")], None, "COMPARE_TIMES")
for aid, e, to in [("p_chat_hisham", "ev_chat_log", "hisham"), ("p_ws_hisham", "ev_ws_log", "hisham"), ("p_audit_hisham", "ev_audit_relabel", "hisham"), ("p_door_hisham", "ev_door_log", "hisham"), ("p_hdr_nadir", "ev_reem_hdr", "nadir")]:
    Act(aid, "present_evidence", f"اعرض {e} على {to}", {"presented": {"evidence_id": e, "to_character": to}}, [{"op": "emit_event", "ref_id": f"PRESENTED_{e.upper()}_{to.upper()}"}], to, aid.upper(), 0)
Act("a_hint", "request_hint", "اطلب تلميحاً", al, [], None, "REQUEST_HINT", 0)
Act("a_accuse", "final_accusation", "قدّم الاستنتاج النهائي", al, [{"op": "emit_event", "ref_id": "SUBMIT"}], None, "FINAL_ACCUSATION", 0)

# ---------------------------------------------------------------- dialogue topics
topics = [
    {"id": "t_arrival", "label_ar": "الإطار الأول ووقته", "example_questions_ar": ["متى التُقط الإطار الأول؟", "ما الذي سجّلته أول مرة؟"], "fact_ids": ["f_reem_frame_time", "f_yusuf_logged"]},
    {"id": "t_clock", "label_ar": "الساعات والتوقيت", "example_questions_ar": ["هل ساعات الأجهزة موثوقة؟", "ما التوقيت المحلي؟"], "fact_ids": ["f_clock_gps", "f_archive_lag", "f_local_tz"], "claim_ids": ["cl_h_clock"]},
    {"id": "t_message", "label_ar": "الرسالة وإيصال القراءة", "example_questions_ar": ["هل وصلتك رسالة قبل إطارك؟", "متى أرسلت الرسالة؟"], "fact_ids": ["f_chat_sent", "f_chat_seen", "f_hisham_aware"], "claim_ids": ["cl_h_unaware"]},
    {"id": "t_filing", "label_ar": "بلاغ الاكتشاف", "example_questions_ar": ["متى أرسلت البلاغ؟", "ماذا صرّحت في الاستمارة؟"], "fact_ids": ["f_hisham_frame_time", "f_bulletin_declared"]},
    {"id": "t_relabel", "label_ar": "وسم الإطار في الأرشيف", "example_questions_ar": ["من غيّر وسم الإطار؟", "هل يُسجَّل أي تعديل؟"], "fact_ids": ["f_relabel", "f_audit_available"], "claim_ids": ["cl_h_auto"]},
    {"id": "t_press", "label_ar": "لوحة الإعلام", "example_questions_ar": ["من أين جاء رقم 00:10؟", "كيف كتبت الملاحظة؟"], "fact_ids": ["f_press_note_local"], "claim_ids": ["cl_reem_late"]},
    {"id": "t_presence", "label_ar": "من كان في غرفة التحكم", "example_questions_ar": ["من كان في الغرفة؟", "ماذا رأيت قبل التقاط الإطار؟"], "fact_ids": ["f_yusuf_saw", "f_alone_in_room"]},
    {"id": "t_records", "label_ar": "سجلات الدخول والمحطات", "example_questions_ar": ["هل توجد سجلات للمحطة؟", "هل تُسجَّل البطاقات؟"], "fact_ids": ["f_ws_logs_exist", "f_badge_exists"]},
    {"id": "t_file", "label_ar": "الملف الأصلي", "example_questions_ar": ["هل لديك الملف الأصلي؟", "هل عُدّل الإطار؟"], "fact_ids": ["f_reem_file_shared"]},
    {"id": "t_history", "label_ar": "التنبيه السابق", "example_questions_ar": ["ما قصة التنبيه الإداري؟"], "fact_ids": ["f_reem_warning"]},
]

# ---- declarative mirrors of dialogue unlocks (for static checkers; hidden from play via telemetry ASK_*) ----
_iv_pre = {a["target_id"]: a["precondition"] for a in A if a["type"] == "interview"}
_tf = set(f for t in topics for f in t["fact_ids"])
for _c in chars:
    _ks = next((k for k in ck if k["character_id"] == _c["id"]), None)
    if not _ks: continue
    _voiced = set(f for l in _c["authored_lines"] if l["purpose"] in ("reveal", "break_down") for f in l.get("fact_ids", []))
    _hid = {h["fact_id"]: h for h in _ks["hides"]}
    for k in _ks["knows"]:
        f = k["fact_id"]
        if f in _hid or f not in _tf or f not in _voiced: continue
        Act(f"ask_{_c['id']}_{f}", "interview", f"[نموذج] {_c['id']} يذكر {f}", _iv_pre[_c["id"]], [U(f)], _c["id"], f"ASK_{_c['id'].upper()}_{f.upper()}", 0)
    for f, h in _hid.items():
        if f not in _tf or f not in _voiced: continue
        Act(f"ask_{_c['id']}_{f}", "interview", f"[نموذج] {_c['id']} يكشف {f}", {"all": [_iv_pre[_c["id"]], h["reveal_when"]]}, [U(f)], _c["id"], f"ASK_{_c['id'].upper()}_{f.upper()}", 0)

# ---------------------------------------------------------------- ending
steps = [
    (1, "السجلات الثلاثة التي بدت متناقضة تصف لحظة واحدة: سجل التشغيل بالتوقيت العالمي، ولوحة الإعلام والأرشيف بالتوقيت المحلي (+3)، والأرشيف متأخر 4 دقائق. بعد التوحيد تتطابق كلها عند 21:10 UTC.", ["ev_obs_log", "ev_press_board", "ev_archive_log", "ev_sync_report", "ev_lab_norm"], "i_lab_order"),
    (2, "رأسا ملفي الإطارين، وهما سجلان آليان بساعتين مضبوطتين وبمرجع واحد، يضعان إطار ريم عند 21:10:12 وإطار هشام عند 21:34:40: ريم أسبق بنحو 24 دقيقة.", ["ev_reem_hdr", "ev_hisham_hdr"], "i_hdr_order"),
    (3, "ما بدا تزويراً في لوحة الإعلام كان نقلاً لرقمين بمنطقتين زمنيتين مختلفتين، وبعد التوحيد لا يوجد ما يشير إلى تلاعب.", ["ev_press_board", "ev_lab_norm", "ev_nadir_statement"], "i_rule_nadir"),
    (4, "علم هشام بإطار ريم قبل إطاره: فتح ملفها 21:24 UTC وقرأ رسالتها 21:27 UTC، بينما أول إطار له 21:34 UTC.", ["ev_chat_log", "ev_ws_log", "ev_hisham_hdr"], "i_aware_chat"),
    (5, "تصريحه في البلاغ بعدم العلم بأي رصد أسبق يخالف سجلين مستقلين، فلا يصلح تفسيراً أن الرصدين كانا مستقلين.", ["ev_bulletin_form", "ev_ws_log"], "i_unaware_false"),
    (6, "تعديل وسم إطارها إلى «روتيني» كان يدوياً من محطته وهو وحده في الغرفة، وليس آلياً كما قال.", ["ev_audit_relabel", "ev_door_log"], "i_relabel_fact"),
    (7, "الأرجح إذن أنه نسب الاكتشاف إلى نفسه وأخفى إطارها. هذا ترجيح مبني على وقائع مسجَّلة، لا حكم على دوافعه.", ["ev_reem_hdr", "ev_chat_log", "ev_audit_relabel"], "i_support_hisham"),
]
ending = {
    "steps": [{"order": o, "text_ar": t, "uses_evidence_ids": u, "inference_id": i} for o, t, u, i in steps],
    "alternative_paths_ar": [
        "يمكن بلوغ الاستنتاج مباشرة من رأسي الملفين دون المرور بتوحيد السجلات الثلاثة، لكن من يفعل ذلك يترك التعارض الظاهر في اللوحة والأرشيف بلا تفسير، وهذا يضعف الحجة أمام من يستشهد بتلك الورقة.",
        "يمكن إثبات علم هشام من سجل المراسلة وحده، أو من سجل المحطة وحده، والأقوى أن يتفقا معاً لأنهما مستقلان.",
    ],
    "what_evidence_could_not_show_ar": [
        "لا تثبت الأدلة دافع هشام ولا إن كان فهم مضمون الإطار حين فتحه.",
        "إيصال القراءة لا يثبت فتح المرفق، والورقة المكتوبة بالقلم لا يمكن نسبتها إلى كاتبها بلا فحص مختص.",
        "لا تحدد هذه الأدلة قرار الأسبقية الرسمي؛ ذلك للجنة الدولية.",
    ],
    "science_notes_ar": [
        "توحيد الأزمنة: لا تُقارن أزمنة قبل أن يُعرف مرجعها (المنطقة الزمنية) وانحراف ساعة الجهاز الذي سجّلها.",
        "رأس ملف الصورة سجل آلي، لكنه يثبت وقت ساعة الجهاز لا نية أحد، ويحتاج التأكد أن النسخة لم تتغير (سلسلة العهدة).",
        "سجلات الدخول والتدقيق تثبت الحسابات والمحطات، ولا تثبت الدوافع، وتحتاج دعماً مستقلاً.",
    ],
}

core = {
    "schema_version": "0.1.0", "case_id": CID, "case_version": "0.1.0",
    "meta": {"title_ar": "الرصد الأخير", "title_en": "The Last Observation", "age_band": "16-18", "locale": "ar", "dialogue_register": "msa", "estimated_minutes": 40, "difficulty": 3,
             "content_flags": ["no_violence", "fraud", "science_lab"], "authors": ["فريق أثر التحريري (مسودة بمساعدة الذكاء الاصطناعي، لم تُراجَع بشرياً بعد)"],
             "knowledge_object_refs": ["KO-RS-05-001", "KO-RS-05-005", "KO-RS-05-002", "KO-RS-06-001", "KO-RS-06-009", "KO-RS-06-021", "KO-FC-04-024", "KO-FC-04-026"]},
    "premise": {
        "hook_ar": "ليلة واحدة، نقطة ضوء واحدة، واسمان يطالبان بها. أحدهما يملك المنصب، والآخر يملك الملف الأصلي.",
        "player_role_ar": "أنت محقّق في لجنة أسبقية الاكتشافات التابعة لاتحاد الراصدين. مهمتك أن تحدد من سجّل الجسم أولاً، وهل أُخفي شيء.",
        "setting_ar": "مرصد وادي النجوم، على هضبة صحراوية بعيدة عن أضواء المدن. توقيت المرصد المحلي UTC+3، وسجل التشغيل الليلي يُكتب بالتوقيت العالمي.",
        "public_fact_ids": ["f_new_object", "f_public_credit", "f_reem_objects", "f_local_tz"],
        "assumed_general_knowledge_ar": ["التوقيت العالمي UTC مرجع زمني واحد، والتوقيت المحلي يزيد عنه أو ينقص بعدد ثابت من الساعات", "إذا كان الجهاز متأخراً فالوقت الحقيقي أكبر مما يعرضه"],
    },
    "entities": {"characters": chars, "locations": locations, "objects": objects, "organizations": orgs},
    "truth": {"solution": {"culprit_ids": ["hisham"],
                           "summary_ar": "علم هشام بإطار ريم الأسبق (21:10 UTC) قبل التقاط إطاره (21:34 UTC)، فنسب الاكتشاف إلى نفسه في البلاغ مصرّحاً بعدم علمه بأي رصد أسبق، ثم عدّل وسم إطارها يدوياً ليبدو روتينياً. ولا تثبت الأدلة دافعه.",
                           "key_fact_ids": ["f_reem_first", "f_hisham_aware"]},
              "facts": facts, "claims": claims},
    "timeline": timeline, "evidence": ev, "evidence_graph": {"inferences": inf},
    "character_knowledge": ck, "hypotheses": hyps, "misdirection_plan": mis, "learning_objectives": los,
    "mechanics": {"time_budget_units": 60, "actions": A},
    "state_machine": {"id": "c001", "initial": "briefing", "type": "compound", "states": {
        "briefing": {"description_ar": "الإحاطة الأولى", "type": "atomic", "on": {"START": {"target": "investigating"}}},
        "investigating": {"description_ar": "التحقيق", "type": "compound", "initial": "gathering",
                          "states": {"gathering": {"type": "atomic", "on": {"OPEN_DEDUCTION": {"target": "deducing"}}}, "deducing": {"type": "atomic", "on": {"BACK": {"target": "gathering"}}}},
                          "on": {"SUBMIT": {"target": "review"}}},
        "review": {"description_ar": "مراجعة الاستنتاج", "type": "atomic", "on": {"CLOSE": {"target": "resolved"}}},
        "resolved": {"description_ar": "إغلاق الملف", "type": "final"},
    }},
    "dialogue": {"max_turns_per_interview": 14, "llm_enabled": False, "topics": topics},
    "rubric": rub, "hint_ladder": hints,
    "fairness_test": {"requirements": {"min_disjoint_proof_paths": 2, "max_inference_depth": 3, "all_red_herrings_refutable": True, "culprit_uniquely_entailed": True, "no_hidden_fact_dependency": True, "max_required_actions": 40}, "runs": []},
    "ending_explanation": ending,
    "expert_review": [{"role": r, "reviewer": "—", "status": "pending", "content_hash": "unbound", "date": "2026-10-27", "notes_ar": "بانتظار مراجعة بشرية؛ لم يُجرَ أي اعتماد."} for r in
                      ["narrative_editor", "scientific_reviewer", "learning_designer", "age_appropriateness", "cultural_reviewer", "legal_rights", "safety"]],
}

# ---------------------------------------------------------------- ui sidecar
ui = {
    "case_id": CID,
    "clock": {"epoch_hhmm": "21:00", "zone_label_ar": "التوقيت العالمي UTC"},
    "cover": {"title_ar": "الرصد الأخير", "tagline_ar": "ثلاث ساعات لا تتفق… وأحدها يكذب", "kicker_ar": "القضية الرئيسية · مرصد وادي النجوم", "glyph": "✦", "accent": "amber"},
    "cold_open_ar": [
        "الساعة 23:55 بتوقيت المرصد.",
        "فوق هضبة لا تصلها أضواء المدن، ظهرت نقطة لم تكن في الخريطة.",
        "بعد ساعات، أُعلن اسم من رآها أولاً. وبعد ساعات أخرى وصلك اعتراض مكتوب بسرعة: «ليست له».",
        "أمامك ثلاثة سجلات وثلاث ساعات، ولا اثنتان منها تتفقان.",
    ],
    "labs": [{
        "id": "lab_time", "type": "time_normalizer", "title_ar": "مختبر توحيد الأزمنة",
        "intro_ar": "لكل سجل زمنٌ مكتوب بمنطقة وساعة مختلفتين. أدخل لكل سجل: الإزاحة عن UTC بالساعات (التوقيت المحلي = UTC + الإزاحة)، وانحراف الساعة بالدقائق (أدخل رقماً موجباً إن كان الجهاز متأخراً، فيُضاف إلى الوقت). حين تتطابق الأزمنة ضمن دقيقتين يصدر التقرير.",
        "tolerance_min": 2, "epoch_utc_minute_of_day": 1260, "day_labels_ar": ["ليلة الحادثة", "اليوم التالي (بعد منتصف الليل المحلي)"],
        "grants_evidence_on_converge": "ev_lab_norm",
        "items": [
            {"evidence_id": "ev_obs_log", "label_ar": "سجل التشغيل — وصول الإطار", "day": 0, "hhmm": "21:10", "basis_ar": "العنوان يقول إن السجل بالتوقيت العالمي"},
            {"evidence_id": "ev_press_board", "label_ar": "لوحة الإعلام — وصول إطار ريم", "day": 1, "hhmm": "00:06", "basis_ar": "منقول من شاشة الأرشيف: ساعة الخادم نفسها"},
            {"evidence_id": "ev_archive_log", "label_ar": "سجل الأرشيف — INGEST", "day": 1, "hhmm": "00:06", "basis_ar": "ساعة الخادم تعرض الوقت المحلي"},
        ],
    }],
    "source_classes": [
        {"id": "primary_record", "label_ar": "سجل أصلي", "help_ar": "يُنتجه جهاز أو نظام لحظة الحدث دون وسيط، كرأس ملف أو سجل دخول."},
        {"id": "redisplay", "label_ar": "نسخة معروضة", "help_ar": "معلومة نُقلت أو أُعيد عرضها من سجل آخر، كملاحظة بخط اليد أو لقطة شاشة."},
        {"id": "claim", "label_ar": "قول أو تصريح", "help_ar": "إفادة شخص أو إقراره؛ تُقاس بالسجلات لا بمكانة قائلها."},
        {"id": "template", "label_ar": "قالب أو نموذج", "help_ar": "نص جاهز أو نموذج لا يصف الحدث الفعلي بذاته."},
        {"id": "public_document", "label_ar": "وثيقة منشورة", "help_ar": "وثيقة معلنة للعموم ومعروف ناشرها."},
    ],
    "limit_menu": [
        {"id": "l_intent", "label_ar": "الأدلة لا تثبت دافع هشام ولا نيّته"},
        {"id": "l_read_receipt", "label_ar": "إيصال القراءة يثبت فتح الرسالة لا فهم مضمونها"},
        {"id": "l_handwriting", "label_ar": "الورقة المكتوبة بالقلم لا تُنسب إلى كاتبها بلا فحص مختص"},
        {"id": "l_memory", "label_ar": "ذاكرة الشهود عن الدقائق غير دقيقة"},
        {"id": "l_invalid_demeanor", "label_ar": "ارتباك هشام في المقابلة يدل على الكذب"},
        {"id": "l_invalid_reputation", "label_ar": "التنبيه السابق لريم يضعف كلامها"},
        {"id": "l_invalid_all", "label_ar": "كل ما يخالف روايتي مزيّف"},
    ],
    "mind_change_menu": [
        {"id": "m_other_user", "label_ar": "ثبوت أن حساب hmansour استخدمه شخص غير هشام"},
        {"id": "m_gps_fault", "label_ar": "ثبوت عطل في مستقبل GPS لكاميرا المسح تلك الليلة"},
        {"id": "m_third_frame", "label_ref": "", "label_ar": "ظهور إطار ثالث موثّق من جهة مستقلة أسبق من الاثنين"},
        {"id": "m_rank", "label_ar": "كون هشام أرفع منصباً من ريم"},
        {"id": "m_popularity", "label_ar": "كثرة المتعاطفين مع أحد الطرفين على وسائل التواصل"},
    ],
    "transfer": {
        "id": "tr_flood", "title_ar": "اختبار نقل المهارة: صورة السوق",
        "scenario_ar": "منشور ينتشر مع صورة سوق غارق بالمياه، ويقول صاحبه إنها «الآن». أمامك ثلاث وثائق متعارضة الظاهر.",
        "documents": [
            {"title_ar": "المنشور", "body_ar": "«الآن! السوق القديم تحت الماء بعد العاصفة.» — نُشر الساعة 02:15 حسب الهاتف."},
            {"title_ar": "بيانات الصورة", "body_ar": "تاريخ الالتقاط: 02:11 (توقيت الجهاز). المنطقة الزمنية للجهاز: UTC+4. حجم الملف أصغر من المعتاد بكثير."},
            {"title_ar": "خبر وكالة محلية", "body_ar": "هطلت الأمطار الغزيرة على المدينة، ويُتوقع استمرارها. نُشر الخبر 22:40 بتوقيت غرينتش."},
        ],
        "prompt_ar": "اختر الخطوات التي تصلح للتحقق من هذا المنشور (يمكنك اختيار أكثر من خطوة).",
        "options": [
            {"id": "o1", "text_ar": "تحويل كل وقت إلى مرجع واحد قبل المقارنة بين المنشور والخبر"},
            {"id": "o2", "text_ar": "البحث عن أقدم نسخة منشورة للصورة"},
            {"id": "o3", "text_ar": "طلب الملف الأصلي بدل لقطة الشاشة لفحص بياناته"},
            {"id": "o4", "text_ar": "مقارنة الحدث بمصدر مستقل كسجلات الأرصاد"},
            {"id": "o5", "text_ar": "الاكتفاء بعدد المشاركات دليلاً على الصحة"},
            {"id": "o6", "text_ar": "الحكم من حدّة نبرة الناشر"},
            {"id": "o7", "text_ar": "اعتماد التعليق الأكثر ثقةً في لهجته"},
            {"id": "o8", "text_ar": "تجاهل الوقت الذي يصعب تفسيره"},
        ],
        "free_text_prompt_ar": "اكتب في ثلاثة أسطر كيف تقرّر درجة ثقتك في أن الصورة من الليلة نفسها.",
    },
    "skills": [{"skill_id": "KO-RS-05-001", "track": "B"}, {"skill_id": "KO-RS-05-005", "track": "B"}, {"skill_id": "KO-RS-05-002", "track": "D"}, {"skill_id": "KO-RS-06-001", "track": "C"}, {"skill_id": "KO-RS-06-009", "track": "D"}, {"skill_id": "KO-RS-06-021", "track": "D"}, {"skill_id": "KO-FC-04-024", "track": "E"}],
    "stage_hooks_ar": {
        "briefing": "ثلاث ساعات لا تتفق في ملفٍ واحد… أيّها يكذب؟",
        "investigating": "كل دليل تفتحه قد يقلب ما ظننته؛ احذر الأرقام التي تبدو متفقة.",
        "review": "الحجة وحدها لا تكفي… هل أنت مستعد لتحمّل حدودها؟",
        "resolved": "أُغلق الملف، لكن في الأرشيف ملفاً آخر لم يُفتح بعد.",
    },
    "character_glyphs": {"reem": "ر", "hisham": "ه", "yusuf": "ي", "nadir": "ن", "salma": "س"},
}
for m in ui["mind_change_menu"]:
    m.pop("label_ref", None)

# ---------------------------------------------------------------- scoring sidecar
sc = {
    "case_id": CID,
    "accepted_conclusions": {
        "h_hisham": {"grade": 1, "note_ar": "استنتاج متسق مع الأدلة ويتطلب ذكر حدوده."},
        "h_parallel": {"grade": 0, "note_ar": "يتجاهل واقعة علم هشام المسجَّلة بسجلين مستقلين."},
        "h_reem_false": {"grade": 0, "note_ar": "قائم على قراءة أزمنة غير موحّدة."},
        "h_nadir": {"grade": 0, "note_ar": "الفرق الظاهر ناتج عن اختلاف المنطقة الزمنية لا عن تزوير."},
    },
    "confidence_band": {"h_hisham": [65, 92], "h_parallel": [0, 20], "h_reem_false": [0, 15], "h_nadir": [0, 15]},
    "source_key": {"ev_obs_log": "primary_record", "ev_press_board": "redisplay", "ev_archive_log": "primary_record", "ev_sync_report": "primary_record", "ev_reem_hdr": "primary_record",
                   "ev_hisham_hdr": "primary_record", "ev_chat_log": "primary_record", "ev_ws_log": "primary_record", "ev_audit_relabel": "primary_record", "ev_door_log": "primary_record",
                   "ev_bulletin_form": "claim", "ev_yusuf_statement": "claim", "ev_nadir_statement": "claim"},
    "link_key": {
        "h_hisham": {"ev_reem_hdr": "supports", "ev_hisham_hdr": "supports", "ev_chat_log": "supports", "ev_ws_log": "supports", "ev_audit_relabel": "supports", "ev_door_log": "supports", "ev_lab_norm": "supports", "ev_sheet": "supports", "ev_press_board": "neutral", "ev_reem_warning": "neutral"},
        "h_reem_false": {"ev_reem_hdr": "weakens", "ev_hisham_hdr": "weakens", "ev_chat_log": "weakens", "ev_lab_norm": "weakens", "ev_press_board": "supports", "ev_reem_warning": "neutral"},
        "h_nadir": {"ev_lab_norm": "weakens", "ev_nadir_statement": "weakens", "ev_press_board": "supports"},
        "h_parallel": {"ev_chat_log": "weakens", "ev_ws_log": "weakens", "ev_audit_relabel": "weakens", "ev_bulletin_form": "neutral"},
    },
    "required_limits": ["l_intent", "l_read_receipt"],
    "valid_mind_changers": ["m_other_user", "m_gps_fault", "m_third_frame"],
    "invalid_limits": ["l_invalid_demeanor", "l_invalid_reputation", "l_invalid_all"],
    "decisive_evidence": ["ev_reem_hdr", "ev_hisham_hdr", "ev_chat_log", "ev_ws_log", "ev_lab_norm"],
    "lab_requirement": {"lab_id": "lab_time", "must_converge": True},
    "timeline_requirement": [
        {"evidence_id": "ev_obs_log", "utc_minute": 10, "tol": 2}, {"evidence_id": "ev_press_board", "utc_minute": 10, "tol": 2},
        {"evidence_id": "ev_archive_log", "utc_minute": 10, "tol": 2}, {"evidence_id": "ev_reem_hdr", "utc_minute": 10, "tol": 2},
        {"evidence_id": "ev_hisham_hdr", "utc_minute": 34, "tol": 2},
    ],
    "refuted_hypotheses": ["h_reem_false", "h_nadir", "h_parallel"],
    "criteria_map": {"c_source": "source_typing", "c_conflict": "conflict_resolution", "c_links": "hypothesis_links", "c_uncertainty": "uncertainty", "c_revision": "revision", "c_elimination": "elimination", "c_justification": "justification_human"},
    "transfer_key": {"valid": ["o1", "o2", "o3", "o4"], "invalid": ["o5", "o6", "o7", "o8"]},
    "caps": {"no_citations_max": 45, "no_conflict_resolution_max": 60},
}

os.makedirs(OUT, exist_ok=True)
for suffix, obj in [("", core), (".ui", ui), (".scoring", sc)]:
    with open(os.path.join(OUT, f"{CID}{suffix}.json"), "w", encoding="utf8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
print("ok", len(json.dumps(core, ensure_ascii=False)))
