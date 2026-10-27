#!/usr/bin/env python3
# Case c004 «شهادة الصورة الصامتة» — authenticity of an image vs. correctness of its context.
# Teaches: a derived file's date is not the capture date; a wall poster is an announcement, not a timestamp; a difference between
# a caption and a record is not a lie. No-culprit convention: the volunteer who wrote the wrong caption (honest mistake) is recorded
# in culprit_ids. Usage: gen_c004.py OUT_DIR
# Calendar (fictional): minute 0 = day 0, 00:00 = 26 October. Setup access 7 Nov (day 12), capture ~8 Nov (day 13),
# archive receipt 9 Nov 09:10 (day 14), public opening 15 Nov 11:00 (day 20).
import json, sys, os
OUT = sys.argv[1]
CID = "c004_silent_photo"

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
ch("mona", "منى القاسم", "witness", "أمينة أرشيف المركز، في الأربعينات",
   "منظّمة وحذرة، تقرأ من السجل ولا تضيف إليه، وتفرّق بين ما استلمته وما تفترضه.",
   ["أن يبقى سجل الأرشيف سليماً", "ألا يُنسب إلى الأرشيف ما لم يسجّله"],
   [L("mn_greet", "greeting", "سجل الاستلام أمامي. أقرأ منه ولا أضيف إليه."),
    L("mn_recv", "reveal", "سجّلنا استلام الملف الأصلي صباح التاسع من تشرين الثاني، قادماً من المصوّر، وهو محفوظ كما وصل.", ["f_archive_received"]),
    L("mn_nodate", "reveal", "ما يسجّله الأرشيف هو لحظة الاستلام. أما لحظة الالتقاط فليست في سجلي ولا أستطيع أن أخمّنها.", ["f_archive_no_capture_date"]),
    L("mn_notpub", "reveal", "الأرشيف لا ينشر شيئاً. نسخ النشر يعدّها فريق الإعلام من الملف المشترك.", ["f_archive_not_publisher"]),
    L("mn_unknown", "deflect_unknown", "هذا ليس في سجلاتي."),
    L("mn_off", "deflect_offtopic", "اسألني عمّا استلمه الأرشيف ومتى."),
    L("mn_bye", "farewell", "السجل يبقى كما هو، فاقرأه كما هو.")])

ch("karim", "كريم العلي", "witness", "مصوّر مستقل، في أواخر الثلاثينات",
   "هادئ ويعتدّ بدقته، يفصل بين ما رآه بعينه وما يسمعه لاحقاً، ولا يحب أن يُحمَّل ما لا يخصّه.",
   ["أن يُنسب إليه عمله كما هو", "ألا يُتّهم بنشر شيء لم ينشره"],
   [L("kr_greet", "greeting", "أهلاً. أخبرك بما أتذكره، وأفرّق بين ما رأيته وما سمعته لاحقاً."),
    L("kr_access", "reveal", "أُتيح لي دخول القاعة من السابع من تشرين الثاني بتصريح تصوير خاص بالتجهيز، أي قبل الافتتاح بثمانية أيام.", ["f_access_window"]),
    L("kr_sent", "reveal", "أرسلت صور الممر إلى أرشيف المركز برسالة صباح التاسع من الشهر، ومعها الملف الأصلي كما خرج من الكاميرا.", ["f_photog_sent"]),
    L("kr_memory", "reveal", "أذكر أنني صوّرتها والتركيب ما زال جارياً، لكنني لا أذكر اليوم بالضبط.", ["f_karim_memory"]),
    L("kr_notpub", "reveal", "لا أتابع ما يُنشر على حسابات المركز، ولا أعرف متى صُنعت كل نسخة منها.", ["f_karim_not_publisher"]),
    L("kr_unknown", "deflect_unknown", "لا أعرف، ولا أحب أن أخمّن."),
    L("kr_off", "deflect_offtopic", "هذا بعيد عمّا صوّرته. اسألني عن التصريح والإرسال."),
    L("kr_bye", "farewell", "شكراً لأنك تسأل عن المصدر قبل أن تحكم على الصورة.")])

ch("dima", "ديما الشامي", "witness", "منسقة المعرض، في أواخر الثلاثينات",
   "مشغولة بالتفاصيل العملية وحريصة على سمعة المركز، وتميل إلى تبنّي أول رواية رسمية وصلتها.",
   ["أن يبدو بيان الإدارة دقيقاً", "أن تُحفظ سجلات التجهيز كاملة"],
   [L("dm_greet", "greeting", "أنا منسقة المعرض. عندي جدول التجهيز وتفاصيل الملصق."),
    L("dm_log", "reveal", "نسجّل كل يوم حالة الممر في سجل التجهيز: ما عُلّق وما رُفع وما بقي في مكانه.", ["f_setup_log_kept"]),
    L("dm_poster", "reveal", "الملصق جزء من إعلان موسم المركز. عُلّق في إطار آخر الممر قبل أن يبدأ التركيب، ويبقى مكانه طوال فترة المعرض.", ["f_poster_hung"]),
    L("dm_claim", "reveal", "وصلنا أن الصورة من مساء الافتتاح، ولذلك قلنا في البيان إنها التقطت بعد الافتتاح.", None, ["cl_mgmt_after"]),
    L("dm_relied", "reveal", "اعتمدت في البيان على وصف المنشور الأول، ولم أرجع إلى سجل التجهيز قبل إصداره.", ["f_dima_relied"]),
    L("dm_unknown", "deflect_unknown", "هذا خارج ما أتابعه."),
    L("dm_off", "deflect_offtopic", "فلنبقَ مع التجهيز والملصق والبيان."),
    L("dm_bye", "farewell", "أرجو أن نصحّح ما يحتاج إلى تصحيح.")])

ch("rami", "رامي الخطيب", "suspect", "متطوع في فريق الإعلام، في العشرينات",
   "متحمس وسريع، ينشر بحماس ويكتب الوصف من الانطباع الأول، وقد يخلط بين وقت النشر ووقت التصوير.",
   ["أن ينجح منشور الافتتاح", "ألا يُلام على خطأ في وصف"],
   [L("rm_greet", "greeting", "أنا متطوع في فريق الإعلام. أنشر صور المركز وأكتب أوصافها."),
    L("rm_file", "reveal", "جهّزت نسخة النشر من الملف المشترك: قصصتها وصغّرتها بعد ظهر يوم الافتتاح.", ["f_derived_created"]),
    L("rm_claim", "reveal", "كتبت في الوصف أن الصورة التقطت بعد الافتتاح، فهذا ما فهمته.", None, ["cl_post_after"]),
    L("rm_check", "refuse_secret", "دعني أراجع سجل المنشور قبل أن أجيب عن ترتيب ما كتبته."),
    L("rm_admit", "reveal", "صحيح، أضفت الوصف بعد رفع الصورة. لم أسأل أحداً عن تاريخ الالتقاط؛ افترضت أنها من يوم الافتتاح لأنني نشرتها مساءه.", ["f_caption_added_later"]),
    L("rm_unknown", "deflect_unknown", "لا أعرف، لم أكن هناك أيام التجهيز."),
    L("rm_off", "deflect_offtopic", "اسألني عن الملف والمنشور."),
    L("rm_bye", "farewell", "سأصحّح الوصف إن ثبت الخطأ.")])

locations = [{"id": "loc_corridor", "name_ar": "ممر المعرض", "description_ar": "الممر الذي تظهر صورته، وفي آخره إطار الملصق."},
             {"id": "loc_archive", "name_ar": "أرشيف المركز", "description_ar": "سجل استلام المواد."},
             {"id": "loc_office", "name_ar": "مكتب التنسيق", "description_ar": "جدول التجهيز وسجل حالة الممر."},
             {"id": "loc_media", "name_ar": "مكتب الإعلام", "description_ar": "إعداد المنشورات ونسخ النشر."}]
objects = [{"id": "obj_photo", "name_ar": "الملف الأصلي للصورة", "description_ar": "ملف الصورة كما خرج من الكاميرا."},
           {"id": "obj_derived", "name_ar": "ملف النشر", "description_ar": "نسخة مقصوصة ومصغّرة أُعدّت للمنشور."},
           {"id": "obj_poster", "name_ar": "ملصق الموسم", "description_ar": "ملصق مؤطَّر في آخر الممر."},
           {"id": "obj_post", "name_ar": "المنشور الأول", "description_ar": "المنشور الذي حمل الصورة ووصفها."}]
orgs = [{"id": "org_center", "name_ar": "المركز الثقافي", "description_ar": "مركز ثقافي يستضيف معرض «ممر الضوء»."}]

# ---------------------------------------------------------------- truth
facts = []
def F(id, st, kind, subj, spoiler, time=None, loc=None, ko=None):
    d = {"id": id, "statement_ar": st, "kind": kind, "subject_ids": subj, "spoiler_level": spoiler}
    if time: d["time"] = time
    if loc: d["location_id"] = loc
    if ko: d["science_ko_refs"] = ko
    facts.append(d)
F("f_photo_circulates", "تداولت الشبكات مساء يوم الافتتاح صورة لممر معرض «ممر الضوء».", "event", ["loc_corridor", "obj_derived"], 0, T(dm(20, 18, 30), "approx"))
F("f_post_claim", "كتب المنشور الأول أن الصورة لقطة من الممر بعد الافتتاح.", "attribute", ["obj_post"], 0)
F("f_mgmt_claim", "قالت إدارة المعرض في بيانها إن الصورة التقطت بعد الافتتاح.", "attribute", ["org_center"], 0)
F("f_poster_visible", "يظهر في آخر الممر ملصق فيه موعد افتتاح المعرض بصيغة المستقبل.", "attribute", ["obj_poster", "loc_corridor"], 0)
F("f_access_window", "أُتيح للمصوّر دخول القاعة قبل الافتتاح بثمانية أيام، بتصريح تجهيز يبدأ في 7 تشرين الثاني.", "state", ["karim", "loc_corridor"], 1, T(dm(12, 9), "exact", dm(19, 18)))
F("f_photog_sent", "أرسل المصوّر صور الممر والملف الأصلي إلى أرشيف المركز صباح 9 تشرين الثاني.", "event", ["karim", "obj_photo"], 1, T(dm(14, 8, 55)), "loc_office", ["KO-FC-04-026"])
F("f_karim_memory", "يتذكّر المصوّر أنه التقط الصورة والتركيب جارٍ، ولا يذكر اليوم تحديداً.", "attribute", ["karim"], 1, T(dm(13), "unknown"))
F("f_karim_not_publisher", "لا يتابع المصوّر ما يُنشر على حسابات المركز ولا يعرف متى صُنعت نسخ النشر.", "attribute", ["karim"], 0)
F("f_archive_received", "سجّل الأرشيف استلام الملف الأصلي صباح 9 تشرين الثاني.", "event", ["mona", "obj_photo"], 1, T(dm(14, 9, 10)), "loc_archive", ["KO-FC-04-026"])
F("f_archive_no_capture_date", "سجل الأرشيف يحفظ وقت الاستلام ولا يحدد وقت الالتقاط.", "attribute", ["mona", "obj_photo"], 1, None, "loc_archive")
F("f_archive_not_publisher", "الأرشيف لا ينشر؛ نسخ النشر يعدّها فريق الإعلام.", "attribute", ["mona"], 0)
F("f_setup_log_kept", "تحتفظ منسقة المعرض بسجل يومي لحالة الممر أثناء التجهيز.", "state", ["dima", "loc_office"], 1, None, "loc_office")
F("f_poster_hung", "عُلّق ملصق إعلان الموسم في إطار آخر الممر قبل بدء التجهيز، ويبقى مكانه طوال فترة المعرض.", "state", ["dima", "obj_poster"], 1, T(dm(0, 11), "exact"), "loc_corridor")
F("f_dima_relied", "اعتمدت منسقة المعرض في بيان الإدارة على وصف المنشور الأول دون الرجوع إلى سجل التجهيز.", "event", ["dima"], 1, T(dm(21, 10), "approx"))
F("f_derived_created", "أعدّ متطوع الإعلام ملف النشر قصّاً وتصغيراً من الملف المشترك بعد ظهر يوم الافتتاح.", "event", ["rami", "obj_derived"], 1, T(dm(20, 15, 40)), "loc_media", ["KO-FC-04-024"])
F("f_caption_added_later", "أضاف المتطوع عبارة «بعد الافتتاح» إلى المنشور بعد رفع الصورة، افتراضاً منه ودون مرجع لتاريخ الالتقاط.", "event", ["rami", "obj_post"], 2, T(dm(20, 19, 5)), "loc_media")
F("f_derived_later", "تاريخ إنشاء ملف النشر يعود إلى نسخة مشتقة أُنشئت بعد تسجيل الأصل في الأرشيف بستة أيام.", "relation", ["obj_derived", "obj_photo"], 2, None, None, ["KO-FC-04-024", "KO-RS-06-004"])
F("f_poster_standing", "الملصق معلّق قبل بدء التجهيز ويبقى بعد الافتتاح، فلا يحدّد وقت أي لقطة تظهر فيها جدرانه.", "relation", ["obj_poster"], 2, None, "loc_corridor", ["KO-RS-06-004"])
F("f_capture_in_setup", "التُقطت الصورة بين 7 و9 تشرين الثاني في مرحلة تركيب المعرض، أي قبل افتتاحه بستة أيام على الأقل.", "event", ["karim", "obj_photo", "loc_corridor"], 3, T(dm(12, 9), "approx", dm(14, 9, 10)), "loc_corridor", ["KO-FC-04-024", "KO-RS-05-005"])

claims = [
    {"id": "cl_post_after", "statement_ar": "الصورة التقطت بعد الافتتاح.", "kind": "honest_mistake", "held_by": ["rami"], "true_fact_id": "f_capture_in_setup", "contradicted_by_evidence_ids": ["ev_archive_receipt", "ev_photog_msg", "ev_setup_log"]},
    {"id": "cl_mgmt_after", "statement_ar": "إدارة المعرض: الصورة التقطت بعد الافتتاح.", "kind": "honest_mistake", "held_by": ["dima"], "true_fact_id": "f_capture_in_setup", "contradicted_by_evidence_ids": ["ev_archive_receipt", "ev_setup_log"]},
]
timeline = [
    {"id": "te_poster", "description_ar": "تعليق ملصق الموسم في إطار آخر الممر.", "time": T(dm(0, 11)), "location_id": "loc_corridor", "actor_ids": ["dima"], "fact_ids": ["f_poster_hung"], "motivated_by_ar": "إعلان موسم المركز قبل بدء التركيب"},
    {"id": "te_access", "description_ar": "بدء تصريح التجهيز وتغطية المنصات وفرش الورق الواقي.", "time": T(dm(12, 9)), "location_id": "loc_corridor", "actor_ids": ["karim", "dima"], "fact_ids": ["f_access_window"], "motivated_by_ar": "بدء أعمال التركيب قبل الافتتاح"},
    {"id": "te_capture", "description_ar": "المصوّر يلتقط صورة الممر أثناء التركيب.", "time": T(dm(13, 15, 20), "approx", dm(13, 15, 50)), "location_id": "loc_corridor", "actor_ids": ["karim"], "fact_ids": ["f_capture_in_setup", "f_karim_memory"], "motivated_by_ar": "توثيق مراحل التجهيز"},
    {"id": "te_send", "description_ar": "المصوّر يرسل الملف الأصلي والأرشيف يسجّل استلامه.", "time": T(dm(14, 8, 55), "exact", dm(14, 9, 10)), "location_id": "loc_archive", "actor_ids": ["karim", "mona"], "fact_ids": ["f_photog_sent", "f_archive_received"], "motivated_by_ar": "حفظ مواد التوثيق في الأرشيف"},
    {"id": "te_open", "description_ar": "افتتاح المعرض للجمهور.", "time": T(dm(20, 11)), "location_id": "loc_corridor", "actor_ids": ["dima"], "fact_ids": [], "motivated_by_ar": "الموعد المعلن للافتتاح"},
    {"id": "te_derived", "description_ar": "إعداد نسخة النشر قصّاً وتصغيراً.", "time": T(dm(20, 15, 40)), "location_id": "loc_media", "actor_ids": ["rami"], "fact_ids": ["f_derived_created"], "motivated_by_ar": "تجهيز منشور مساء الافتتاح"},
    {"id": "te_post", "description_ar": "نشر الصورة ثم إضافة الوصف بعد رفعها.", "time": T(dm(20, 18, 30), "exact", dm(20, 19, 5)), "location_id": "loc_media", "actor_ids": ["rami"], "fact_ids": ["f_photo_circulates", "f_caption_added_later"], "motivated_by_ar": "الظن بأن الصورة من يوم الافتتاح"},
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
V("ev_photo", "الصورة المتداولة (نسخة النشر)", "digital",
  "صورة أفقية لممر معرض «ممر الضوء». على الجدار الأيمن إطارات معلّقة، ومكان بطاقة التعريف بجانب كل إطار فارغ. في وسط الممر سلّم ألمنيوم مسنود إلى الجدار، والأرضية مغطاة بورق واقٍ. إلى اليسار منصتان مغطاتان بقماش أبيض. في آخر الممر ملصق مؤطَّر نصه: «معرض ممر الضوء — يفتتح في 15 تشرين الثاني». لا يظهر في المشهد زوار ولا حبال إرشاد، ولا تاريخ مكتوب سوى الملصق.",
  ["a_view_photo"], ["f_photo_circulates", "f_poster_visible"], "moderate",
  "تعرض حالة الممر لحظة التصوير ولا تحمل تاريخاً؛ والملصق إعلان لا يؤرّخ اللقطة.", loc="loc_corridor")
V("ev_post", "المنشور الأول على حساب المركز", "digital",
  "منشور على حساب المركز الثقافي، نُشر 15 تشرين الثاني الساعة 18:30. الصورة المرفقة هي نسخة النشر. نص الوصف: «لقطة من ممر المعرض بعد افتتاحه اليوم.» عدد التعليقات: 212.",
  ["a_open_post"], ["f_post_claim"], "weak",
  "ادعاء كتبه ناشر المنشور؛ لا يذكر مصدراً لتاريخ الالتقاط، وكثرة التعليقات لا تدل على صحته.", loc="loc_media")
V("ev_file_meta", "خصائص ملف النشر", "digital",
  "خصائص الملف المرفق بالمنشور:\nالنوع: صورة مقصوصة ومصغّرة (نسخة للنشر)\nأُنشئ بواسطة: برنامج تحرير صور\nتاريخ الإنشاء: 15 تشرين الثاني، 15:40\nحقل «تاريخ الالتقاط»: فارغ",
  ["a_open_meta"], ["f_derived_created"], "moderate",
  "تاريخ إنشاء نسخة مشتقة وليس تاريخ الالتقاط الأصلي؛ وحقول الملف قد تتغير أو تُمحى عند التصدير والتصغير، فلا تُعتمد برهاناً قاطعاً.", red=True, ko="KO-FC-04-024", loc="loc_media")
V("ev_post_history", "سجل تعديلات المنشور", "digital",
  "سجل النظام للمنشور على حساب المركز:\n15 تشرين الثاني 18:30 — نُشر المنشور بصورة مرفقة دون أي نص وصفي.\n15 تشرين الثاني 19:05 — عُدّل المنشور بإضافة النص «لقطة من ممر المعرض بعد افتتاحه اليوم».\nالحساب المحرِّر: فريق الإعلام (متطوع).\nحقل «مصدر التاريخ» في نموذج الوصف: فارغ.",
  ["a_open_history"], ["f_caption_added_later"], "strong",
  "يثبت متى كُتب الوصف ومن أي حساب، ولا يثبت سبب كتابته ولا صحته.", ko="KO-RS-06-004", loc="loc_media")
V("ev_access", "جدول تصاريح التجهيز", "documentary",
  "جدول دخول قاعة المعرض في فترة التجهيز:\nالفترة: من 7 تشرين الثاني إلى 14 تشرين الثاني، يومياً من 09:00 إلى 18:00\nالمصرَّح لهم: فريق التركيب، منسقة المعرض، المصوّر كريم العلي (تصريح تصوير التجهيز)\nافتتاح الجمهور: 15 تشرين الثاني، 11:00\nينتهي تصريح التصوير بنهاية فترة التجهيز.",
  ["a_get_access"], ["f_access_window"], "strong",
  "يثبت متى أُتيح الدخول، ولا يثبت أن الصورة التقطت في يوم بعينه ولا أن صاحب التصريح هو من التقطها.", loc="loc_office")
V("ev_photog_msg", "رسالة المصوّر إلى الأرشيف", "digital",
  "رسالة بريد:\nمن: كريم العلي — إلى: أرشيف المركز\nالوقت: 9 تشرين الثاني، 08:55\nالنص: «صباح الخير. أرفقت صور ممر المعرض التي التقطتها خلال أعمال التركيب، وهي بالملف الأصلي كما خرج من الكاميرا. التركيب لم ينتهِ بعد، فاحتفظوا بها ضمن مواد التوثيق.»\nالمرفقات: ممر_المعرض_01 (ملف أصلي)",
  ["a_get_msg"], ["f_photog_sent"], "moderate",
  "يثبت وقت إرسال الملف ووصفه بحسب المصوّر، ولا يحدد يوم الالتقاط الدقيق؛ ويحتاج إلى سجل الأرشيف لتأكيد وصول المرفق.", ko="KO-FC-04-026", loc="loc_office")
V("ev_archive_receipt", "سجل استلام الأرشيف", "documentary",
  "سجل استلام المواد — أرشيف المركز\nرقم الإدخال: 0412\nالتاريخ والوقت: 9 تشرين الثاني، 09:10\nالمرسل: كريم العلي (مصوّر)\nالوصف: صورة ممر المعرض — ملف أصلي كامل الإطار\nسلسلة العهدة: المصوّر ← بريد الأرشيف ← خادم الأرشيف، دون انتقال آخر\nملاحظة الأمينة: المشهد هو نفسه الظاهر في نسخة النشر، وفي الأصل امتداد أوسع للممر.",
  ["a_get_receipt"], ["f_archive_received"], "strong",
  "يثبت وقت وجود الأصل عند الأرشيف لا وقت التقاطه، ويعتمد على دقة تسجيل الأرشيف نفسه.", ko="KO-FC-04-026", loc="loc_archive")
V("ev_setup_log", "سجل حالة الممر اليومي", "documentary",
  "سجل التجهيز اليومي — إعداد منسقة المعرض:\n7 تشرين الثاني: بدء التركيب؛ تغطية المنصات بالقماش؛ فرش الورق الواقي؛ السلّم داخل الممر.\n8 تشرين الثاني: تعليق الإطارات على الجدار الأيمن؛ البطاقات التعريفية غير مركّبة؛ السلّم داخل الممر.\n9 تشرين الثاني: متابعة التعليق؛ السلّم داخل الممر.\n10 تشرين الثاني: إخراج السلّم من الممر؛ تركيب الإضاءة.\n11–12 تشرين الثاني: ضبط الإضاءة؛ المنصات ما زالت مغطاة.\n13 تشرين الثاني: رفع أغطية المنصات وإزالة الورق الواقي؛ تركيب البطاقات التعريفية.\n14 تشرين الثاني: تنظيف نهائي وتركيب الحبال الإرشادية.\n15 تشرين الثاني: افتتاح الجمهور 11:00.",
  ["a_get_setup_log"], ["f_setup_log_kept"], "strong",
  "سجل داخلي كتبته المنسقة يحدد حالة الممر يوماً بيوم لا ساعة الالتقاط، ولا يغني عن فحص مستقل لسلامة الصورة نفسها.", loc="loc_office")
V("ev_poster_record", "سجل طباعة الملصق وتعليقه", "documentary",
  "سجل أعمال الطباعة والتعليق — المركز الثقافي:\nالبند: ملصق إعلان الموسم، وفيه عبارة «يفتتح في 15 تشرين الثاني»\nطُبع: 20 تشرين الأول\nعُلّق في إطار آخر الممر: 26 تشرين الأول\nملاحظة: يبقى الملصق في إطاره حتى انتهاء المعرض ولا يُستبدل عند الافتتاح.",
  ["a_get_poster"], ["f_poster_hung"], "strong",
  "يفسّر وجود الملصق وصيغته المستقبلية، ولا يحدد تاريخ أي صورة التُقطت أمامه.", loc="loc_office")
V("ev_rami_stmt", "إفادة رامي الخطيب (ملخص)", "testimonial",
  "ملخص إفادة رامي الخطيب، متطوع الإعلام:\n«جهّزت نسخة النشر من الملف المشترك بعد ظهر يوم الافتتاح، وكتبت في الوصف أن الصورة التقطت بعد الافتتاح.»",
  ["a_note_rami"], ["f_derived_created"], "weak",
  "إفادة ناشر المنشور تذكر ما كتبه لا ما تحقق منه، وتُقاس بالسجلات.", loc="loc_media")
V("ev_dima_stmt", "إفادة ديما الشامي (ملخص)", "testimonial",
  "ملخص إفادة ديما الشامي، منسقة المعرض:\n«بياننا الأول اعتمد وصف المنشور. وعندنا سجل لحالة الممر يوماً بيوم لم أرجع إليه قبل إصدار البيان.»",
  ["a_note_dima"], ["f_dima_relied"], "moderate",
  "تشرح كيف نشأ بيان الإدارة، وتُظهر أنه ترديد لوصف المنشور لا نتيجة فحص.", loc="loc_office")
V("ev_karim_stmt", "إفادة كريم العلي (ملخص)", "testimonial",
  "ملخص إفادة كريم العلي، المصوّر:\n«صوّرت الممر والتركيب جارٍ وأرسلتها إلى الأرشيف. لا أذكر اليوم بالضبط، ولا أتابع نشر النسخ.»",
  ["a_note_karim"], ["f_karim_memory"], "weak",
  "ذاكرة صاحب اللقطة عن اليوم غير دقيقة، وتتقوّى فقط حين تؤيدها سجلات مستقلة.", loc="loc_corridor")

def P(t, i): return {"ref_type": t, "ref_id": i}
inf = []
def I(id, prem, ct, concl, rel, strength, rule, ks):
    inf.append({"id": id, "premises": prem, "conclusion": {"ref_type": ct, "ref_id": concl}, "relation": rel, "strength": strength, "rule_ar": rule, "skill_ko_refs": ks})
KF = "f_capture_in_setup"
I("i_derived", [P("evidence", "ev_file_meta"), P("evidence", "ev_archive_receipt")], "fact", "f_derived_later", "establishes", "strong",
  "تاريخ إنشاء ملف النشر (15 تشرين الثاني) متأخر عن تسجيل الأصل لدى الأرشيف (9 تشرين الثاني)؛ فهو يؤرّخ النسخة المشتقة لا اللقطة.", ["KO-FC-04-024", "KO-RS-06-004"])
I("i_path_a", [P("evidence", "ev_access"), P("evidence", "ev_photog_msg"), P("evidence", "ev_archive_receipt")], "fact", KF, "establishes", "strong",
  "الدخول لم يُتَح قبل 7 تشرين الثاني، والملف الأصلي وصل إلى الأرشيف صباح 9 تشرين الثاني بسلسلة عهدة قصيرة؛ فاللقطة وقعت بين التاريخين، قبل الافتتاح بستة أيام على الأقل.", ["KO-FC-04-026", "KO-RS-05-004"])
I("i_path_b", [P("evidence", "ev_photo"), P("evidence", "ev_setup_log")], "fact", KF, "establishes", "strong",
  "اجتماع السلّم والأغطية والورق الواقي والإطارات المعلّقة دون بطاقات لا يتحقق في سجل الحالة إلا يومي 8 و9 تشرين الثاني؛ فمشهد الصورة يطابق مرحلة التركيب لا مرحلة الجمهور.", ["KO-RS-06-004", "KO-RS-05-005"])
I("i_poster", [P("evidence", "ev_poster_record")], "fact", "f_poster_standing", "establishes", "strong",
  "ما كان معلّقاً قبل التركيب وبقي بعد الافتتاح موجود في أي لقطة من الفترتين؛ فوجوده لا يرجّح إحداهما.", ["KO-RS-06-001"])
I("i_support_misdated", [P("fact", KF)], "hypothesis", "h_misdated", "supports", "strong",
  "إذا وقعت اللقطة في مرحلة التركيب فالصورة أصلية في سياقها، ويكون وصف «بعد الافتتاح» هو الخطأ.", ["KO-RS-05-002"])
I("i_rule_after", [P("fact", KF)], "hypothesis", "h_after_ok", "rules_out", "strong",
  "لا تجتمع لقطة قبل الافتتاح بستة أيام مع كونها بعد الافتتاح.", ["KO-RS-06-008"])
I("i_rule_fake", [P("fact", KF)], "hypothesis", "h_fake", "rules_out", "strong",
  "حين يتفق مسار الملف مع سجلات مستقلة، أو يتفق المشهد بتفاصيله مع سجل مستقل لحالة المكان، لا يبقى للتركيب الكامل سند؛ ويبقى احتمالاً نظرياً لم يُفحص تقنياً.", ["KO-RS-06-001", "KO-RS-05-004"])
I("i_rule_unknown", [P("fact", KF)], "hypothesis", "h_unknowable", "rules_out", "strong",
  "حين تحصر السجلات اللقطة في نافذة محددة قبل الافتتاح، يكون القول بأن لا شيء يمكن إثباته أضعف مما تدل عليه الأدلة.", ["KO-RS-05-010"])
I("i_poster_ctx", [P("fact", "f_poster_standing")], "hypothesis", "h_fake", "refutes", "suggestive",
  "إذا لم يكن في الملصق تعارض فعلي مع بقية السجلات، فلا تبقى قرينة التركيب التي بدت منه.", ["KO-RS-06-001"])
I("i_claim_post", [P("fact", KF)], "claim", "cl_post_after", "contradicts_claim", "strong",
  "قول «بعد الافتتاح» يخالف لقطة وقعت قبل الافتتاح بستة أيام على الأقل.", ["KO-RS-05-014"])
I("i_claim_mgmt", [P("fact", KF)], "claim", "cl_mgmt_after", "contradicts_claim", "strong",
  "بيان الإدارة ردّد الوصف نفسه؛ فيسقط معه حين تسقط المقارنة بالسجلات.", ["KO-RS-05-014"])

ck = [
    {"character_id": "mona", "knows": [{"fact_id": "f_archive_received", "access": "professional", "certainty": "certain"},
                                       {"fact_id": "f_archive_no_capture_date", "access": "professional", "certainty": "certain"},
                                       {"fact_id": "f_archive_not_publisher", "access": "professional", "certainty": "certain"}], "hides": [], "believes": []},
    {"character_id": "karim", "knows": [{"fact_id": "f_access_window", "access": "witnessed", "certainty": "certain"},
                                        {"fact_id": "f_photog_sent", "access": "witnessed", "certainty": "certain"},
                                        {"fact_id": "f_karim_memory", "access": "witnessed", "certainty": "unsure"},
                                        {"fact_id": "f_karim_not_publisher", "access": "witnessed", "certainty": "certain"}], "hides": [], "believes": []},
    {"character_id": "dima", "knows": [{"fact_id": "f_setup_log_kept", "access": "professional", "certainty": "certain"},
                                       {"fact_id": "f_poster_hung", "access": "professional", "certainty": "certain"},
                                       {"fact_id": "f_dima_relied", "access": "witnessed", "certainty": "certain"}], "hides": [],
     "believes": [{"claim_id": "cl_mgmt_after", "stance": "sincere"}]},
    {"character_id": "rami", "knows": [{"fact_id": "f_derived_created", "access": "witnessed", "certainty": "certain"}],
     "hides": [{"fact_id": "f_caption_added_later", "reveal_when": {"presented": {"evidence_id": "ev_post_history", "to_character": "rami"}}, "cover_claim_id": None, "reveal_line_id": "rm_admit"}],
     "believes": [{"claim_id": "cl_post_after", "stance": "sincere"}]},
]
hyps = [
    {"id": "h_fake", "statement_ar": "الصورة مفبركة أو مركّبة بالكامل.", "is_true": False, "plausibility_at_start": "high"},
    {"id": "h_misdated", "statement_ar": "الصورة حقيقية، لكن الوصف الذي نسب لقطتها إلى ما بعد الافتتاح خاطئ.", "is_true": True, "plausibility_at_start": "medium", "suspect_id": "rami"},
    {"id": "h_unknowable", "statement_ar": "لا يمكن إثبات أي شيء عن تاريخ التقاط الصورة.", "is_true": False, "plausibility_at_start": "low"},
    {"id": "h_after_ok", "statement_ar": "الصورة حقيقية والتقطت بعد الافتتاح كما ورد في المنشور وبيان الإدارة.", "is_true": False, "plausibility_at_start": "medium"},
]
mis = [
    {"id": "rh_meta", "points_to_hypothesis_id": "h_after_ok", "planted_via_ar": "خصائص ملف النشر تعطي تاريخ إنشاء يوم الافتتاح بعد الظهر، فتبدو وكأنها تؤيد وصف «بعد الافتتاح».", "evidence_ids": ["ev_file_meta"],
     "refuted_by_inference_ids": ["i_derived", "i_rule_after"],
     "fairness_note_ar": "سجل الاستلام يضع الأصل لدى الأرشيف قبل تاريخ إنشاء ملف النشر بستة أيام، وخصائص الملف نفسها تقول إنه نسخة مقصوصة ومصغّرة."},
    {"id": "rh_poster", "points_to_hypothesis_id": "h_fake", "planted_via_ar": "الملصق في الصورة يعلن الافتتاح بصيغة المستقبل بينما يقول الوصف إن الصورة بعد الافتتاح، فيبدو التعارض كأنه تلاعب.", "evidence_ids": ["ev_photo"],
     "refuted_by_inference_ids": ["i_poster", "i_poster_ctx", "i_rule_fake"],
     "fairness_note_ar": "سجل الطباعة والتعليق يبيّن أن الملصق عُلّق قبل التركيب ويبقى بعد الافتتاح، فصيغته المستقبلية تعارض الوصف لا الصورة."},
]
los = [
    {"id": "lo_source", "statement_ar": "يفرّق بين السجل الأصلي والنسخة المشتقة والادعاء، ويسأل أي ملف يصفه كل تاريخ.", "skill_ko_ref": "KO-RS-05-001", "observable_behaviors_ar": ["يصنّف خصائص الملف المنشور نسخة معروضة", "يصنّف المنشور والإفادات أقوالاً"], "evidence_sources": ["evidence_board"]},
    {"id": "lo_hyp", "statement_ar": "يوازن بين فرضيات متنافسة ويستبعد ما تنقضه الأدلة.", "skill_ko_ref": "KO-RS-05-002", "observable_behaviors_ar": ["يضيف أكثر من فرضية", "يستبعد فرضية بدليل مرفق"], "evidence_sources": ["hypothesis_ledger"]},
    {"id": "lo_diag", "statement_ar": "يقدّر ما يثبته كل دليل وما لا يثبته، ويفرّق بين أصالة الصورة وصحة وصفها.", "skill_ko_ref": "KO-RS-06-001", "observable_behaviors_ar": ["يربط الدليل بالفرضية باتجاه صحيح", "لا يعامل الاختلاف في الرواية تزويراً"], "evidence_sources": ["evidence_board", "final_justification"]},
    {"id": "lo_calib", "statement_ar": "يصوغ ثقته بحدودها ويحدد ما قد يغيّر رأيه.", "skill_ko_ref": "KO-RS-06-021", "observable_behaviors_ar": ["يختار ثقة معقولة", "يذكر حدوداً", "يحدد دليلاً مغيّراً للرأي"], "evidence_sources": ["final_justification"]},
    {"id": "lo_revise", "statement_ar": "يراجع رأيه الأول حين يظهر دليل أفضل.", "skill_ko_ref": "KO-RS-06-009", "observable_behaviors_ar": ["يغيّر فرضيته الرائدة بدليل"], "evidence_sources": ["hypothesis_ledger", "action_log"]},
]
def levels(d): return [{"score": i, "descriptor_ar": t} for i, t in enumerate(d)]
rub = {
    "reference_answer_ar": "الصورة أصلية والخطأ في وصف زمنها. التقطها المصوّر في مرحلة التركيب بين 7 و9 تشرين الثاني، وبهذا يثبت مساران مستقلان: تصريح الدخول ورسالة المصوّر وسجل الأرشيف يضعون الملف الأصلي عند الأرشيف صباح 9 تشرين الثاني، وتفاصيل المشهد لا تجتمع في سجل المنسقة إلا في يومي 8 و9. أما تاريخ ملف النشر فيعود إلى قصّ وتصغير جرى يوم الافتتاح، والملصق معلّق من قبل ويبقى من بعد. كتب متطوع الإعلام «بعد الافتتاح» افتراضاً ثم ردّدته الإدارة. حدود الاستنتاج: لا نعرف ساعة اللقطة، ولم يُجرَ فحص تقني مستقل لنفي التركيب، ولا دليل على سوء نية.",
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
    H("hg1", 1, "metacognitive", "أين ينتهي ما تُظهره الصورة وتبدأ العبارة التي كُتبت عنها؟", {"always": True}, None, 0.02),
    H("hg2", 2, "focus_area", "ضع كل معلومة في جدول: مصدر أصلي أم نسخة أم تعليق؟ ثم اسأل عن أي ملف تتحدث خصائص الملف.", he("ev_file_meta"), None, 0.04),
    H("hg3", 3, "pointer", "راجع تحديداً الدليل الذي يوضح سياق الرقم أو الزمن أو الوثيقة: متى وصل الأصل إلى جهة محايدة؟", he("ev_file_meta"), None, 0.06),
    H("hd1", 1, "metacognitive", "هل التاريخ الذي تقرؤه يخصّ اللقطة نفسها أم ملفاً صُنع منها؟", he("ev_file_meta"), "i_derived", 0.02),
    H("hd2", 2, "pointer", "اطلب من الأرشيف سجل استلام الملف الأصلي، وقارن تاريخه بتاريخ إنشاء ملف النشر.", he("ev_file_meta"), "i_derived", 0.06),
    H("ha1", 1, "metacognitive", "من يستطيع أن يخبرك متى خرج الملف الأصلي من الكاميرا إلى جهة أخرى؟", he("ev_post"), "i_path_a", 0.02),
    H("ha2", 2, "pointer", "اسأل المصوّر والأرشيف عن أول لحظة سُجّل فيها الملف الأصلي، وعن بداية السماح بالدخول.", he("ev_post"), "i_path_a", 0.06),
    H("ha3", 3, "partial_reveal", "ضع التصريح والرسالة وسجل الاستلام على سطر واحد: بين أي تاريخين تقع اللقطة؟", he("ev_archive_receipt"), "i_path_a", 0.1),
    H("hb1", 1, "metacognitive", "ما العناصر في الصورة التي تتبدّل من يوم إلى يوم في مكان يجري تجهيزه؟", he("ev_photo"), "i_path_b", 0.02),
    H("hb2", 2, "pointer", "اسأل المنسقة عمّا يوثّق حالة الممر يوماً بيوم.", he("ev_photo"), "i_path_b", 0.06),
    H("hb3", 3, "partial_reveal", "طابق ثلاثة عناصر مرئية في الصورة مع أسطر السجل، وانظر في أي يوم تجتمع معاً.", he("ev_setup_log"), "i_path_b", 0.1),
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
Act("a_view_photo", "examine", "افحص الصورة المتداولة", al, [G("ev_photo")], "obj_derived", "VIEW_PHOTO")
Act("a_open_post", "examine", "افتح المنشور الأول", al, [G("ev_post")], "obj_post", "OPEN_POST")
Act("a_open_meta", "examine", "افتح خصائص الملف المرفق بالمنشور", he("ev_post"), [G("ev_file_meta")], "obj_derived", "OPEN_META")
Act("a_open_history", "examine", "اطلب سجل تعديلات المنشور", he("ev_post"), [G("ev_post_history")], "obj_post", "OPEN_HISTORY")
for cid, lab in [("mona", "منى"), ("karim", "كريم"), ("dima", "ديما")]:
    Act(f"a_int_{cid}", "interview", f"ابدأ مقابلة {lab}", al, [{"op": "raise_trust", "ref_id": cid, "amount": 1}], cid, f"INT_{cid.upper()}")
Act("a_int_rami", "interview", "ابدأ مقابلة رامي", he("ev_post"), [{"op": "raise_trust", "ref_id": "rami", "amount": 1}], "rami", "INT_RAMI")
Act("a_get_receipt", "examine", "اطلب سجل استلام الأرشيف", fu("f_archive_received"), [G("ev_archive_receipt")], "loc_archive", "GET_RECEIPT")
Act("a_get_msg", "examine", "اطلب رسالة المصوّر المرسلة إلى الأرشيف", fu("f_photog_sent"), [G("ev_photog_msg")], "karim", "GET_MSG")
Act("a_get_access", "examine", "اطلب جدول تصاريح التجهيز", fu("f_access_window"), [G("ev_access")], "loc_office", "GET_ACCESS")
Act("a_get_setup_log", "examine", "اطلب سجل حالة الممر اليومي", fu("f_setup_log_kept"), [G("ev_setup_log")], "loc_office", "GET_SETUP_LOG")
Act("a_get_poster", "examine", "اطلب سجل طباعة الملصق وتعليقه", fu("f_poster_hung"), [G("ev_poster_record")], "obj_poster", "GET_POSTER")
Act("a_note_karim", "examine", "دوّن إفادة كريم", fu("f_karim_memory"), [G("ev_karim_stmt")], "karim", "NOTE_KARIM")
Act("a_note_dima", "examine", "دوّن إفادة ديما", fu("f_dima_relied"), [G("ev_dima_stmt")], "dima", "NOTE_DIMA")
Act("a_note_rami", "examine", "دوّن إفادة رامي", fu("f_derived_created"), [G("ev_rami_stmt")], "rami", "NOTE_RAMI")
Act("p_history_rami", "present_evidence", "اعرض سجل تعديلات المنشور على رامي", {"presented": {"evidence_id": "ev_post_history", "to_character": "rami"}}, [{"op": "emit_event", "ref_id": "PRESENTED_HISTORY"}], "rami", "P_HISTORY_RAMI", 0)
Act("a_hint", "request_hint", "اطلب تلميحاً", al, [], None, "REQUEST_HINT", 0)
Act("a_accuse", "final_accusation", "قدّم الاستنتاج النهائي", al, [{"op": "emit_event", "ref_id": "SUBMIT"}], None, "FINAL_ACCUSATION", 0)

topics = [
    {"id": "t_capture", "label_ar": "متى التُقطت الصورة", "example_questions_ar": ["متى التقطت الصورة؟", "هل تذكر يوم التصوير؟"], "fact_ids": ["f_karim_memory"]},
    {"id": "t_access", "label_ar": "تصريح الدخول إلى القاعة", "example_questions_ar": ["متى سُمح لك بدخول القاعة؟", "ما تصريح التصوير؟"], "fact_ids": ["f_access_window"]},
    {"id": "t_sending", "label_ar": "إرسال الملف إلى الأرشيف", "example_questions_ar": ["متى أرسلت الملف؟", "متى استلم الأرشيف الملف الأصلي؟", "هل يحدد السجل تاريخ الالتقاط؟"], "fact_ids": ["f_photog_sent", "f_archive_received", "f_archive_no_capture_date"]},
    {"id": "t_publishing", "label_ar": "نسخ النشر", "example_questions_ar": ["من يعدّ نسخ النشر؟", "متى صُنعت نسخة المنشور؟"], "fact_ids": ["f_karim_not_publisher", "f_archive_not_publisher", "f_derived_created"]},
    {"id": "t_setup", "label_ar": "سجل التجهيز اليومي", "example_questions_ar": ["هل يوجد سجل لحالة الممر؟", "كيف وثّقتم أيام التجهيز؟"], "fact_ids": ["f_setup_log_kept"]},
    {"id": "t_poster", "label_ar": "الملصق في آخر الممر", "example_questions_ar": ["متى عُلّق الملصق؟", "لماذا يقول الملصق يفتتح؟"], "fact_ids": ["f_poster_hung"]},
    {"id": "t_statement", "label_ar": "بيان إدارة المعرض", "example_questions_ar": ["على ماذا اعتمد البيان؟", "من أين عرفتم أنها بعد الافتتاح؟"], "fact_ids": ["f_dima_relied"], "claim_ids": ["cl_mgmt_after"]},
    {"id": "t_caption", "label_ar": "وصف المنشور", "example_questions_ar": ["من كتب الوصف؟", "متى أضفت عبارة بعد الافتتاح؟"], "fact_ids": ["f_caption_added_later"], "claim_ids": ["cl_post_after"]},
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
    (1, "خصائص ملف النشر تؤرّخ نسخة صُنعت يوم الافتتاح، بينما سجل الأرشيف يضع الأصل عنده قبل ذلك بستة أيام؛ فاختلاف الملفين هو مصدر الالتباس.", ["ev_file_meta", "ev_archive_receipt"], "i_derived"),
    (2, "التصريح يبدأ في 7 تشرين الثاني، ورسالة المصوّر وسجل الاستلام يضعان الأصل في الأرشيف صباح 9 تشرين الثاني: وقعت اللقطة بين التاريخين.", ["ev_access", "ev_photog_msg", "ev_archive_receipt"], "i_path_a"),
    (3, "مسار ثانٍ لا يستعمل تلك السجلات: عناصر المشهد معاً لا تتحقق في سجل حالة الممر إلا يومي 8 و9 تشرين الثاني.", ["ev_photo", "ev_setup_log"], "i_path_b"),
    (4, "الملصق طُبع وعُلّق قبل بدء التركيب ولا يُرفع عند الافتتاح، فصيغته المستقبلية لا تؤرّخ اللقطة ولا تدل على تركيب.", ["ev_poster_record"], "i_poster"),
    (5, "إذن الصورة حقيقية، والعبارة التي نسبتها إلى ما بعد الافتتاح هي الخطأ؛ كُتبت على سبيل الافتراض ثم رُدّدت في البيان.", ["ev_post_history", "ev_archive_receipt"], "i_support_misdated"),
]
ending = {
    "steps": [{"order": o, "text_ar": t, "uses_evidence_ids": u, "inference_id": i} for o, t, u, i in steps],
    "alternative_paths_ar": ["يكفي المسار الأول وحده (التصريح والرسالة وسجل الاستلام) أو المسار الثاني وحده (مطابقة مشهد الصورة لسجل حالة الممر)؛ والأفضل أن تتقاطع الحجتان."],
    "what_evidence_could_not_show_ar": ["لا يحدد أي دليل ساعة اللقطة بالدقيقة؛ المثبت نافذة أيام قبل الافتتاح.", "لم يُجرَ فحص تقني مستقل لبيانات الصورة نفسها، فنفي التركيب مبني على تعدد السجلات المستقلة لا على فحص مخبري.", "لا تثبت الأدلة سبب افتراض الناشر ولا دافعه؛ المعروف فقط أنه كتب الوصف دون مرجع."],
    "science_notes_ar": ["تاريخ إنشاء الملف وتاريخ الالتقاط معلومتان مختلفتان: الأولى تخص النسخة التي بين يديك، والثانية تخص اللحظة الأولى.", "اختلاف الرواية عن السجل لا يعني أن أحداً كذب؛ قد يكون ظناً لم يُراجَع.", "سلسلة العهدة القصيرة الموثقة تقوّي الاستنتاج حول الأصل، ولا تغني عن ذكر حدوده."],
}
core = {
    "schema_version": "0.1.0", "case_id": CID, "case_version": "0.1.0",
    "meta": {"title_ar": "شهادة الصورة الصامتة", "title_en": "The Silent Photograph", "age_band": "16-18", "locale": "ar", "dialogue_register": "msa", "estimated_minutes": 25, "difficulty": 2,
             "content_flags": ["no_violence"], "authors": ["فريق أثر التحريري (مسودة بمساعدة الذكاء الاصطناعي، لم تُراجَع بشرياً بعد)"],
             "knowledge_object_refs": ["KO-RS-05-001", "KO-RS-05-002", "KO-RS-05-004", "KO-RS-05-005", "KO-RS-05-010", "KO-RS-05-014", "KO-RS-06-001", "KO-RS-06-004", "KO-RS-06-008", "KO-RS-06-009", "KO-RS-06-021", "KO-FC-04-024", "KO-FC-04-026"]},
    "premise": {"hook_ar": "صورة واحدة وتاريخان لا يتفقان. فمن يكذب: الصورة أم من وصفها؟",
                "player_role_ar": "أنت مدقق معلومات في المركز الثقافي، وأول مهامك أن تحكم على صحة صورة الممر ووصفها قبل أن يتسع الجدل.",
                "setting_ar": "المركز الثقافي في المدينة، مساء يوم افتتاح معرض «ممر الضوء». كل الأوقات والتواريخ بتوقيت المركز.",
                "public_fact_ids": ["f_photo_circulates", "f_post_claim", "f_mgmt_claim", "f_poster_visible"],
                "assumed_general_knowledge_ar": ["تُنشأ نسخ النشر من ملف أصلي ويُغيَّر فيها الحجم والقص", "الملصق المعلّق في مكان ثابت لا يتغير بين يوم وآخر"]},
    "entities": {"characters": chars, "locations": locations, "objects": objects, "organizations": orgs},
    "truth": {"solution": {"culprit_ids": ["rami"], "summary_ar": "الصورة غير مفبركة، لكن وصفها الأول أخطأ في زمنها: لقطة من مرحلة تركيب المعرض قبل افتتاحه بأيام، ونسخة منها نُشرت مساء الافتتاح. كتب متطوع الإعلام عبارة «بعد الافتتاح» افتراضاً ثم ردّدتها الإدارة. وتاريخ ملف النشر يخص النسخة، والملصق معلّق قبل التركيب وبعد الافتتاح.", "key_fact_ids": [KF]},
              "facts": facts, "claims": claims},
    "timeline": timeline, "evidence": ev, "evidence_graph": {"inferences": inf},
    "character_knowledge": ck, "hypotheses": hyps, "misdirection_plan": mis, "learning_objectives": los,
    "mechanics": {"time_budget_units": 30, "actions": A},
    "state_machine": {"id": "c004", "initial": "briefing", "type": "compound", "states": {
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
    "clock": {"epoch_hhmm": "00:00", "zone_label_ar": "توقيت المركز"},
    "cover": {"title_ar": "شهادة الصورة الصامتة", "tagline_ar": "الصورة لا تتكلم… ومن وصفها تكلّم كثيراً", "kicker_ar": "قضية · معرض ممر الضوء", "glyph": "◍", "accent": "rose"},
    "cold_open_ar": [
        "مساء يوم افتتاح معرض «ممر الضوء».",
        "انتشرت صورة لممر المعرض، وكتب ناشرها أنها لقطة بعد الافتتاح، وكرّرت الإدارة العبارة نفسها.",
        "لكن ما يظهر على الجدار وفي أرض الممر يبدو غريباً على صالة افتتحت للتو، وبدأ بعض الناس يهمسون بأن الصورة مركّبة.",
        "أمامك صورة واحدة ومنشور واحد. ابدأ بما تراه فعلاً، ثم اسأل عن كل تاريخ: لأي ملف هو؟",
    ],
    "labs": [],
    "source_classes": [
        {"id": "primary_record", "label_ar": "سجل أصلي", "help_ar": "يُنتجه نظام أو شخص لحظة الحدث دون وسيط، كسجل استلام أو رسالة مؤرخة."},
        {"id": "redisplay", "label_ar": "نسخة معروضة", "help_ar": "معلومة نُقلت أو اشتُقّت من ملف آخر، كخصائص نسخة مصغّرة."},
        {"id": "claim", "label_ar": "قول أو تصريح", "help_ar": "إفادة شخص أو وصف منشور؛ يُقاس بالسجلات لا بتكراره."},
        {"id": "template", "label_ar": "قالب أو نموذج", "help_ar": "نص جاهز لا يصف الحدث الفعلي بذاته."},
        {"id": "public_document", "label_ar": "وثيقة منشورة", "help_ar": "وثيقة معلنة ومعروف ناشرها."}],
    "limit_menu": [
        {"id": "l_window", "label_ar": "الأدلة تحدد نافذة أيام قبل الافتتاح لا ساعة الالتقاط بالدقيقة"},
        {"id": "l_no_pixel", "label_ar": "لم يُجرَ فحص تقني مستقل لبيانات الصورة نفسها، فنفي التركيب مبني على السجلات"},
        {"id": "l_intent", "label_ar": "الأدلة لا تثبت دافع الناشر ولا سبب افتراضه"},
        {"id": "l_meta", "label_ar": "تاريخ ملف النشر لا يحدد لحظة الالتقاط"},
        {"id": "l_invalid_poster", "label_ar": "صيغة الملصق المستقبلية وحدها تكفي لتحديد تاريخ اللقطة"},
        {"id": "l_invalid_conflict", "label_ar": "تعارض بيان الإدارة مع السجلات يدل على أنها كاذبة"},
        {"id": "l_invalid_nodate", "label_ar": "غياب تاريخ مكتوب داخل المشهد يعني أن الصورة مفبركة"}],
    "mind_change_menu": [
        {"id": "m_receipt_late", "label_ar": "ثبوت أن سجل الاستلام كُتب بأثر رجعي بعد الافتتاح"},
        {"id": "m_log_rewritten", "label_ar": "ثبوت أن سجل حالة الممر كُتب بعد الافتتاح ثم عُدّل"},
        {"id": "m_other_file", "label_ar": "ثبوت أن الملف المحفوظ في الأرشيف صورة أخرى غير الصورة المنشورة"},
        {"id": "m_popular", "label_ar": "كثرة التعليقات المصدّقة للمنشور"},
        {"id": "m_confident", "label_ar": "ثقة الناشر العالية بأنه محق"}],
    "transfer": {
        "id": "tr_bakery", "title_ar": "اختبار نقل المهارة: صورة الطابور",
        "scenario_ar": "منشور ينتشر مع صورة طابور طويل أمام مخبز، وكاتبه يقول إنها «من هذا الصباح». أمامك ثلاث وثائق تبدو مختلفة.",
        "documents": [
            {"title_ar": "المنشور", "body_ar": "«الطابور أمام المخبز الآن بعد الإعلان عن رفع السعر!» — نُشر الساعة 08:05."},
            {"title_ar": "خصائص الملف المرفق", "body_ar": "نوع الملف: صورة مصغّرة. تاريخ الإنشاء: اليوم 07:50. حقل تاريخ الالتقاط: فارغ. أُنشئ بواسطة تطبيق مراسلة."},
            {"title_ar": "رسالة صاحب المخبز", "body_ar": "«صوّرنا هذا الطابور أول أيام العرض الخاص، أي قبل ثمانية أيام، وأرسلنا الصورة الأصلية إلى المصور في اليوم نفسه.»"},
        ],
        "prompt_ar": "اختر الخطوات التي تصلح للتحقق من وقت التقاط هذه الصورة (يمكنك اختيار أكثر من خطوة).",
        "options": [
            {"id": "o1", "text_ar": "طلب الملف الأصلي وسؤال متى أُرسل أو سُجّل لأول مرة عند جهة أخرى"},
            {"id": "o2", "text_ar": "التفريق بين تاريخ إنشاء النسخة المصغّرة وتاريخ الالتقاط"},
            {"id": "o3", "text_ar": "مقارنة ما يظهر في الصورة بسجل مستقل لأيام العرض الخاص"},
            {"id": "o4", "text_ar": "البحث عن أقدم نسخة منشورة للصورة ومن نشرها أولاً"},
            {"id": "o5", "text_ar": "اعتبار تاريخ إنشاء الملف هو تاريخ الالتقاط ما دام مكتوباً"},
            {"id": "o6", "text_ar": "الاكتفاء بعدد المشاركات دليلاً على الصحة"},
            {"id": "o7", "text_ar": "اعتبار اختلاف المنشور عن رسالة صاحب المخبز دليل تزوير"},
            {"id": "o8", "text_ar": "تصديق الرواية الأكثر ثقةً في لهجتها"}],
        "free_text_prompt_ar": "اكتب في ثلاثة أسطر ما الذي تعتبره ثابتاً وما الذي ما زال مفتوحاً بشأن وقت التقاط الصورة.",
    },
    "skills": [{"skill_id": "KO-RS-05-001", "track": "B"}, {"skill_id": "KO-RS-05-002", "track": "D"}, {"skill_id": "KO-RS-06-001", "track": "C"}, {"skill_id": "KO-RS-06-009", "track": "D"}, {"skill_id": "KO-RS-06-021", "track": "D"}, {"skill_id": "KO-FC-04-024", "track": "E"}],
    "stage_hooks_ar": {"briefing": "صورة بلا تاريخ، ومنشور بتاريخ، وبيان يكرّره… أيها يحمل الدليل؟", "investigating": "كل تاريخ تجده ينتمي إلى ملف ما؛ اعرف ملفه قبل أن تقارن.", "review": "قبل أن تُغلق الملف: ما الذي ثبت، وما الذي لم يُثبَت؟", "resolved": "أُغلق ملف الصورة، وفي الأرشيف رقمٌ مكرر ينتظر من يفسّره."},
    "character_glyphs": {"mona": "م", "karim": "ك", "dima": "د", "rami": "ر"},
}
sc = {
    "case_id": CID,
    "accepted_conclusions": {
        "h_misdated": {"grade": 1, "note_ar": "استنتاج متسق مع الأدلة ويتطلب ذكر حدوده."},
        "h_fake": {"grade": 0, "note_ar": "يخلط بين اختلاف الوصف عن السجل وتركيب الصورة."},
        "h_unknowable": {"grade": 0, "note_ar": "السجلات المستقلة تحصر اللقطة في نافذة أيام قبل الافتتاح."},
        "h_after_ok": {"grade": 0, "note_ar": "يعتمد على تاريخ ملف النشر وهو تاريخ نسخة مشتقة."}},
    "confidence_band": {"h_misdated": [65, 90], "h_fake": [0, 15], "h_unknowable": [0, 25], "h_after_ok": [0, 15]},
    "source_key": {"ev_photo": "primary_record", "ev_post": "claim", "ev_file_meta": "redisplay", "ev_post_history": "primary_record", "ev_access": "primary_record",
                   "ev_photog_msg": "primary_record", "ev_archive_receipt": "primary_record", "ev_setup_log": "primary_record", "ev_poster_record": "primary_record",
                   "ev_rami_stmt": "claim", "ev_dima_stmt": "claim", "ev_karim_stmt": "claim"},
    "link_key": {
        "h_misdated": {"ev_photo": "supports", "ev_access": "supports", "ev_photog_msg": "supports", "ev_archive_receipt": "supports", "ev_setup_log": "supports", "ev_post_history": "supports", "ev_file_meta": "neutral", "ev_poster_record": "neutral"},
        "h_after_ok": {"ev_file_meta": "neutral", "ev_post": "neutral", "ev_archive_receipt": "weakens", "ev_photog_msg": "weakens", "ev_access": "weakens", "ev_setup_log": "weakens", "ev_photo": "weakens", "ev_post_history": "weakens"},
        "h_fake": {"ev_archive_receipt": "weakens", "ev_setup_log": "weakens", "ev_poster_record": "weakens", "ev_photog_msg": "weakens", "ev_file_meta": "neutral"},
        "h_unknowable": {"ev_archive_receipt": "weakens", "ev_setup_log": "weakens", "ev_access": "weakens", "ev_file_meta": "neutral"}},
    "required_limits": ["l_window", "l_no_pixel"], "valid_mind_changers": ["m_receipt_late", "m_log_rewritten", "m_other_file"],
    "invalid_limits": ["l_invalid_poster", "l_invalid_conflict", "l_invalid_nodate"],
    "decisive_evidence": ["ev_archive_receipt", "ev_photog_msg", "ev_access", "ev_setup_log", "ev_photo"],
    "lab_requirement": None,
    "refuted_hypotheses": ["h_fake", "h_after_ok", "h_unknowable"],
    "criteria_map": {"c_source": "source_typing", "c_links": "hypothesis_links", "c_elimination": "elimination", "c_uncertainty": "uncertainty", "c_revision": "revision", "c_justification": "justification_human"},
    "transfer_key": {"valid": ["o1", "o2", "o3", "o4"], "invalid": ["o5", "o6", "o7", "o8"]},
    "caps": {"no_citations_max": 45, "no_conflict_resolution_max": 70},
}
os.makedirs(OUT, exist_ok=True)
for suf, obj in [("", core), (".ui", ui), (".scoring", sc)]:
    with open(os.path.join(OUT, f"{CID}{suf}.json"), "w", encoding="utf8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
print("ok")
