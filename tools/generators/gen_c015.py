#!/usr/bin/env python3
# Case c015 «المفتاح في جيب المعطف» — from seed S-05 (the planted item; HS-053/HS-052-inspired structure, original text).
# Teaches: ask WHO supplied each piece of evidence and what they stood to gain, separate "found in his coat" from "put there by him",
# and let neutral machine logs (door readers, key-board reader, round scans, cleaning sheet) fix the order of events.
# The accused guard is a careful craftsman, not a pitiable victim; one honest independent witness exists (the tour guide).
# Culprit convention: the assistant who planted the key is recorded in culprit_ids; the case ends with institutional follow-up, not shaming.
# Usage: gen_c015.py OUT_DIR
import json, sys, os
OUT = sys.argv[1]
CID = "c015_key_in_coat"

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
ch("mansour", "منصور الأيوبي", "suspect", "حارس قاعات في المتحف منذ ثلاثين سنة",
   "حِرفي دقيق يدوّن كل جولة ويثق بالسجلات أكثر من الكلام، قليل الشكوى، ويجيب عمّا يُسأل عنه بلا زيادة.",
   ["أن تُحسم المسألة بالسجلات", "أن يواصل عمله بعد انتهاء التحقيق"],
   [L("mn_greet", "greeting", "اسألني عمّا شئت. جولاتي كلها مدوّنة."),
    L("mn_coat", "reveal", "وصلت الثامنة وخمس دقائق، وعلقت معطفي في غرفة الموظفين وخرجت بعد دقيقتين، ولم أعد إليها حتى استُدعيت.", ["f_mansour_coat"]),
    L("mn_rounds", "reveal", "جولتي تمرّ بست نقاط تفقد كل نصف ساعة، ونقطتي الرابعة عند خزانة العرض 4، فمروري بها أمر عادي في كل دورة.", ["f_mansour_rounds"]),
    L("mn_unknown", "deflect_unknown", "لا أعرف كيف وصل المفتاح إلى معطفي."),
    L("mn_off", "deflect_offtopic", "لنبقَ عند المفتاح والجولة."),
    L("mn_bye", "farewell", "السجل أمامكم، فاقرؤوه.")])
ch("ramez", "رامز السعدي", "suspect", "مساعد عرض في المتحف",
   "طموح وواثق، يعرض المعلومات بصيغة تدين غيره، ويتراجع إذا عُرض عليه سجل لا يستطيع تفسيره.",
   ["أن يُنظر إليه كمن حمى المتحف", "أن ينال رئاسة فريق القاعات"],
   [L("rm_greet", "greeting", "أنا من وجد المفتاح وأبلغت فوراً. لا أظن أن الأمر يحتاج كل هذا البحث."),
    L("rm_found", "reveal", "دخلت غرفة الموظفين مرتين: الأولى نحو 10:12 لآخذ جهاز اللاسلكي، والثانية نحو 10:41 لأتفقد المعاطف، فوجدت المفتاح في الجيب الخارجي لمعطف منصور وأبلغت 10:45.", ["f_ramez_found"]),
    L("rm_claim", "reveal", "رأيت منصور قرب الخزانة، والمفتاح وُجد في معطفه؛ فمن غيره يكون؟", None, ["cl_ramez_inference"]),
    L("rm_refuse", "refuse_secret", "لا أذكر شيئاً آخر عن الصباح."),
    L("rm_took", "break_down", "نعم... سحبت وسم المفتاح من اللوحة 09:58 حين خرجت أمينة المتحف، ووضعته في معطف منصور وقت زيارتي الأولى، وأبلغت عنه بعد ذلك. خفت أن ينال هو الرئاسة، وأنا نادم.", ["f_ramez_took"]),
    L("rm_unknown", "deflect_unknown", "لا أذكر ذلك."),
    L("rm_off", "deflect_offtopic", "اسألني عن المفتاح وعن بلاغي."),
    L("rm_bye", "farewell", "أرجو أن ينتهي هذا قريباً.")])
ch("karam", "كرم الحلبي", "witness", "أمين شباك التذاكر",
   "ودود ومتعجل في الاستنتاج، يصف ما رآه بصدق ثم يضيف إليه تفسيراً من عنده، ولا يخفي أنه متقدم لرئاسة الفريق.",
   ["أن يُعامَل بإنصاف وهو أحد المتقدمين للرئاسة", "ألا يُظنّ أنه يتآمر على زميله"],
   [L("kr_greet", "greeting", "أهلاً. أنا أجلس خلف الشباك فلا أعرف الكثير عن غرفة المفاتيح."),
    L("kr_desk", "reveal", "استلمت الشباك 09:30 وبقيت فيه حتى الحادية عشرة، وكنت أبيع التذاكر طوال الوقت.", ["f_karam_desk"]),
    L("kr_saw", "reveal", "رأيت منصور من نافذة الشباك يمرّ قرب الخزانة 4 نحو 09:55.", ["f_karam_saw"]),
    L("kr_claim", "reveal", "ظننت أن وجوده هناك لا بد أنه غير عادي، فأخبرت رامز ونادر.", None, ["cl_karam_unusual"]),
    L("kr_unknown", "deflect_unknown", "لا أعرف أكثر من ذلك."),
    L("kr_off", "deflect_offtopic", "اسألني عن الشباك وما رأيته منه."),
    L("kr_bye", "farewell", "لم أقصد اتهام أحد.")])
ch("salwa", "سلوى الحسيني", "witness", "أمينة المتحف",
   "منظمة وحريصة على مفاتيح المتحف، تعترف بأنها تركت اللوحة مفتوحة دقائق، وتفرّق بين ما رأته وما لم تره.",
   ["أن تُفهم مسؤولية الإدارة عن لوحة المفاتيح", "ألا يُظلم أحد من الموظفين"],
   [L("sw_greet", "greeting", "تفضّل. أعترف أن اللوحة كانت مفتوحة دقائق، وهذا خطئي أنا."),
    L("sw_key", "reveal", "أعدت وسم مفتاح الخزانة 4 إلى اللوحة 09:50، وخرجت من مكتبي 09:56، وعدت 10:05 فوجدت الوسم غائباً.", ["f_key_returned", "f_curator_away"]),
    L("sw_asked", "reveal", "قبل خروجي بدقيقة جاءني رامز عند الباب يسأل عن المفتاح لفحص الخزانة 4، فقلت له إن ذلك يحتاج موافقة رئيس القاعات.", ["f_ramez_asked"]),
    L("sw_mansour", "reveal", "لم يأتِ منصور إلى مكتبي هذا الصباح إطلاقاً.", ["f_mansour_not_office"]),
    L("sw_unknown", "deflect_unknown", "لم أرَ ما جرى بعد خروجي."),
    L("sw_off", "deflect_offtopic", "اسألني عن المفتاح واللوحة."),
    L("sw_bye", "farewell", "سنراجع طريقة حفظ المفاتيح بعد هذا.")])
ch("yasmin", "ياسمين الخطيب", "witness", "مرشدة زوار",
   "هادئة ودقيقة، لا تعرف شيئاً عن المفتاح ولا عن الترقية، وتحكي ما رأته مع مجموعتها فقط.",
   ["أن تساعد بما رأته فقط"],
   [L("ys_greet", "greeting", "أنا لا أعرف شيئاً عن المفتاح، لكن يمكنني أن أقول أين رأيت أحداً."),
    L("ys_saw", "reveal", "كنت مع مجموعة مدرسية في القاعة 2، وفتح لنا منصور الباب نحو 10:10 ثم تابع جولته.", ["f_guide_saw"]),
    L("ys_unknown", "deflect_unknown", "لا أعرف غير ذلك."),
    L("ys_off", "deflect_offtopic", "هذا لا يخصّ ما رأيته مع مجموعتي."),
    L("ys_bye", "farewell", "أتمنى أن يتضح الأمر.")])

locations = [{"id": "loc_office", "name_ar": "مكتب أمينة المتحف", "description_ar": "فيه لوحة المفاتيح وقارئ الوسوم وقارئ باب المكتب."},
             {"id": "loc_staff", "name_ar": "غرفة الموظفين", "description_ar": "فيها الشماعات وقارئ بطاقات على الباب."},
             {"id": "loc_gallery", "name_ar": "القاعات", "description_ar": "مسار الجولة بنقاطه الست، ومنها القاعة 2 وخزانة العرض 4."},
             {"id": "loc_desk", "name_ar": "شباك التذاكر", "description_ar": "قرب المدخل، بنافذة تطل على القاعة الأولى."},
             {"id": "loc_admin", "name_ar": "إدارة المتحف", "description_ar": "تستقبل البلاغات والتقارير."}]
objects = [{"id": "obj_key", "name_ar": "مفتاح خزانة العرض 4", "description_ar": "مفتاح موسوم يُحفظ في لوحة مفاتيح مكتب أمينة المتحف."},
           {"id": "obj_coat", "name_ar": "معطف منصور الرمادي", "description_ar": "معطف عليه بطاقة اسم، معلق في غرفة الموظفين."}]
orgs = [{"id": "org_museum", "name_ar": "متحف الأثر", "description_ar": "متحف خيالي في المرسى."}]

# ---------------------------------------------------------------- facts
facts = []
def F(id, st, kind, subj, spoiler, time=None, loc=None, ko=None):
    d = {"id": id, "statement_ar": st, "kind": kind, "subject_ids": subj, "spoiler_level": spoiler}
    if time: d["time"] = time
    if loc: d["location_id"] = loc
    if ko: d["science_ko_refs"] = ko
    facts.append(d)
F("f_key_missing", "فُقد وسم مفتاح خزانة العرض 4 من لوحة المفاتيح في مكتب أمينة المتحف صباح اليوم.", "event", ["obj_key", "loc_office"], 0)
F("f_key_found_coat", "وُجد المفتاح في الجيب الخارجي لمعطف الحارس منصور المعلق في غرفة الموظفين، وأُبلغ عنه الساعة 10:45.", "event", ["obj_key", "obj_coat", "mansour"], 0)
F("f_three_saw", "ثلاثة زملاء يقولون إنهم رأوا منصور قرب الخزانة 4، والإدارة تطلب حسم الأمر.", "attribute", ["mansour", "ramez", "karam"], 0)
F("f_mansour_coat", "علّق منصور معطفه في غرفة الموظفين نحو 08:05 وخرج بعد دقيقتين ولم يعد إليها حتى استُدعي.", "event", ["mansour", "obj_coat"], 1, T(5), "loc_staff")
F("f_mansour_rounds", "جولة منصور تمرّ بست نقاط كل نصف ساعة، ونقطتها الرابعة عند الخزانة 4.", "state", ["mansour"], 1, T(85, "exact", 165), "loc_gallery")
F("f_ramez_found", "دخل رامز غرفة الموظفين نحو 10:12 ثم نحو 10:41، وقال إنه وجد المفتاح في المرة الثانية وأبلغ 10:45.", "event", ["ramez", "obj_key"], 1, T(132, "approx", 165), "loc_staff")
F("f_karam_desk", "جلس كرم في شباك التذاكر من 09:30 حتى نحو 11:00.", "state", ["karam", "loc_desk"], 1, T(90, "exact", 180), "loc_desk")
F("f_karam_saw", "رأى كرم منصور يمرّ قرب الخزانة 4 نحو 09:55 من نافذة الشباك.", "event", ["karam", "mansour"], 1, T(115, "approx"), "loc_gallery")
F("f_key_returned", "أعادت أمينة المتحف وسم المفتاح إلى اللوحة 09:50.", "event", ["salwa", "obj_key"], 1, T(110), "loc_office")
F("f_curator_away", "غادرت أمينة المتحف مكتبها 09:56 وتركت اللوحة مفتوحة، وعادت 10:05 فوجدت الوسم غائباً.", "event", ["salwa", "obj_key"], 1, T(116, "exact", 125), "loc_office")
F("f_ramez_asked", "طلب رامز المفتاح من أمينة المتحف عند باب المكتب نحو 09:55 فأُحيل إلى رئيس القاعات.", "event", ["ramez", "salwa"], 2, T(115, "approx"), "loc_office")
F("f_mansour_not_office", "لم يأتِ منصور إلى مكتب أمينة المتحف صباح اليوم.", "state", ["mansour", "salwa"], 2, None, "loc_office")
F("f_guide_saw", "رأت المرشدة منصور يفتح باب القاعة 2 نحو 10:10 ويتابع جولته.", "event", ["yasmin", "mansour"], 2, T(130, "approx"), "loc_gallery")
F("f_ramez_took", "سحب رامز وسم المفتاح من اللوحة 09:58 ووضعه في جيب معطف منصور أثناء زيارته الأولى لغرفة الموظفين، ثم أبلغ عن «العثور» عليه.", "event", ["ramez", "obj_key", "obj_coat"], 3, T(118, "exact", 134), "loc_staff", ["KO-RS-05-005"])
F("f_coat_early", "كان معطف منصور معلقاً في غرفة الموظفين قبل أن يخرج المفتاح من اللوحة بنحو ساعة ونصف.", "relation", ["obj_coat", "obj_key"], 3, T(5, "exact", 118), None, ["KO-RS-05-005", "KO-RS-06-017"])
F("f_mansour_elsewhere", "كان منصور في جولته ولم يدخل مكتب أمينة المتحف ولا غرفة الموظفين بعد المعطف، لا وقت سحب الوسم ولا وقت زيارتي رامز.", "relation", ["mansour"], 3, T(110, "exact", 165), None, ["KO-RS-05-005", "KO-RS-06-001"])
F("f_ramez_only", "رامز وحده من الموظفين دخل مكتب الأمينة حين سُحب الوسم، ثم دخل غرفة الموظفين قبل أن يُعثر على المفتاح.", "relation", ["ramez"], 3, T(117, "exact", 164), None, ["KO-RS-05-005", "KO-RS-06-001"])
F("f_karam_elsewhere", "كان كرم في الشباك طوال الفترة، ولا أثر له عند المكتب أو في غرفة الموظفين بعد 09:24.", "relation", ["karam"], 3, T(90, "exact", 180), None, ["KO-RS-05-005"])
F("f_sightings_two_sources", "البلاغات الثلاثة عن رؤية منصور قرب الخزانة صادرة عن متقدمَين للرئاسة وعن سامع منهما، وكلها تصف مروراً عادياً في جولته.", "relation", ["mansour", "ramez", "karam"], 2, None, None, ["KO-RS-05-001", "KO-RS-06-002"])

claims = [
    {"id": "cl_ramez_inference", "statement_ar": "رأيته قرب الخزانة والمفتاح وُجد في معطفه، فهو من أخذه.", "kind": "half_truth", "held_by": ["ramez"], "true_fact_id": "f_ramez_only", "contradicted_by_evidence_ids": ["ev_round_scans", "ev_staff_door_log", "ev_cleaning_sheet"]},
    {"id": "cl_karam_unusual", "statement_ar": "وجود منصور قرب الخزانة وقت اختفاء المفتاح أمر غير عادي.", "kind": "honest_mistake", "held_by": ["karam"], "true_fact_id": "f_mansour_elsewhere", "contradicted_by_evidence_ids": ["ev_round_scans"]},
]
timeline = [
    {"id": "te_coat", "description_ar": "منصور يعلّق معطفه في غرفة الموظفين ويخرج.", "time": T(5, "exact", 7), "location_id": "loc_staff", "actor_ids": ["mansour"], "fact_ids": ["f_mansour_coat"], "motivated_by_ar": "بدأ وردية الحراسة"},
    {"id": "te_clean", "description_ar": "عاملة التنظيف تنظف الغرفة وتدوّن أن المعطف معلق على الشماعة الثالثة.", "time": T(15, "exact", 30), "location_id": "loc_staff", "actor_ids": [], "fact_ids": ["f_coat_early"]},
    {"id": "te_rounds", "description_ar": "منصور يمشي جولته على النقاط الست كل نصف ساعة.", "time": T(85, "exact", 165), "location_id": "loc_gallery", "actor_ids": ["mansour"], "fact_ids": ["f_mansour_rounds", "f_mansour_elsewhere"], "motivated_by_ar": "واجب الجولة الدورية"},
    {"id": "te_desk", "description_ar": "كرم في الشباك يبيع التذاكر.", "time": T(90, "exact", 180), "location_id": "loc_desk", "actor_ids": ["karam"], "fact_ids": ["f_karam_desk"], "motivated_by_ar": "وردية الشباك"},
    {"id": "te_return", "description_ar": "أمينة المتحف تعيد وسم المفتاح إلى اللوحة.", "time": T(110), "location_id": "loc_office", "actor_ids": ["salwa"], "fact_ids": ["f_key_returned"], "motivated_by_ar": "انتهت من استعمال المفتاح"},
    {"id": "te_ask", "description_ar": "رامز يسأل الأمينة عن المفتاح عند باب المكتب، وتخرج الأمينة بعد دقيقة.", "time": T(115, "approx", 116), "location_id": "loc_office", "actor_ids": ["ramez", "salwa"], "fact_ids": ["f_ramez_asked", "f_curator_away"], "motivated_by_ar": "قال إنه يريد فحص الخزانة 4"},
    {"id": "te_pull", "description_ar": "رامز يدخل المكتب ويسحب الوسم.", "time": T(117, "exact", 120), "location_id": "loc_office", "actor_ids": ["ramez"], "fact_ids": ["f_ramez_took", "f_ramez_only"], "motivated_by_ar": "أراد أن يوقع زميله في الشبهة قبل قرار الرئاسة"},
    {"id": "te_missing", "description_ar": "الأمينة تعود وتجد الوسم غائباً.", "time": T(125), "location_id": "loc_office", "actor_ids": ["salwa"], "fact_ids": ["f_key_missing", "f_curator_away"], "motivated_by_ar": "عادت إلى مكتبها بعد استقبال المجموعة"},
    {"id": "te_plant", "description_ar": "رامز يدخل غرفة الموظفين دقيقتين.", "time": T(132, "exact", 134), "location_id": "loc_staff", "actor_ids": ["ramez"], "fact_ids": ["f_ramez_took", "f_ramez_found"], "motivated_by_ar": "قال إنه ذهب لأخذ جهاز اللاسلكي"},
    {"id": "te_found", "description_ar": "رامز يدخل ثانية ويخرج، ثم يبلّغ الإدارة بالعثور على المفتاح.", "time": T(161, "exact", 165), "location_id": "loc_staff", "actor_ids": ["ramez"], "fact_ids": ["f_ramez_found", "f_key_found_coat"], "motivated_by_ar": "قال إنه أراد تفقد المعاطف"},
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
V("ev_incident_report", "تقرير الحادث (الساعة 10:45)", "documentary",
  "متحف الأثر — تقرير حادث\n10:05: فُقد وسم مفتاح خزانة العرض 4 من لوحة المفاتيح في مكتب أمينة المتحف.\n10:45: أبلغ مساعد العرض رامز السعدي أنه وجد المفتاح في الجيب الخارجي لمعطف رمادي معلق في غرفة الموظفين، عليه بطاقة اسم «م. الأيوبي».\nحالة الخزانة 4: مغلقة وسليمة، ولم يُفقد شيء من محتوياتها.",
  ["a_get_report"], ["f_key_missing", "f_key_found_coat"], "strong",
  "يثبت أين وُجد المفتاح ومن أبلغ ومتى، ولا يثبت من وضعه في الجيب.", red=True, loc="loc_admin")
V("ev_sightings", "ملخص البلاغات الثلاثة", "documentary",
  "ملخص ما ورد إلى الإدارة عن رؤية منصور قرب الخزانة 4:\n1) رامز السعدي: «رأيت منصور واقفاً قرب الخزانة 4 نحو 09:55». المصدر: رآه بنفسه.\n2) كرم الحلبي: «رأيته يمرّ قرب الخزانة 4 نحو 09:55 من نافذة الشباك». المصدر: رآه بنفسه.\n3) نادر المصري (حارس القاعة 2): «سمعت أنه كان عند الخزانة وقت اختفاء المفتاح». المصدر: سمعه من كرم.",
  ["a_get_sightings"], ["f_three_saw"], "moderate",
  "ملخص لأقوال ثلاثة أشخاص؛ يثبت أن مروراً بجانب الخزانة أُبلغ عنه، لا أن منصور فعل شيئاً.", red=True, loc="loc_admin")
V("ev_promo_notice", "إعلان شغور رئاسة فريق القاعات", "documentary",
  "إعلان داخلي رقم 7 — متحف الأثر\nشغور رئاسة فريق القاعات الأرضية.\nالمتقدمون: رامز السعدي، كرم الحلبي، منصور الأيوبي.\nآخر موعد: نهاية الشهر. القرار: لجنة الإدارة.",
  ["a_get_promo"], ["f_sightings_two_sources"], "strong",
  "يبيّن أن المتقدمين ثلاثة؛ لا يبيّن أن أحداً منهم تصرف بدافع الترقية.", loc="loc_admin")
V("ev_staff_door_log", "سجل قارئ باب غرفة الموظفين", "digital",
  "سجل قارئ بطاقات باب غرفة الموظفين — اليوم\n08:05 دخول: منصور الأيوبي | 08:07 خروج: منصور الأيوبي\n08:15 دخول: عاملة التنظيف | 08:30 خروج: عاملة التنظيف\n09:20 دخول: كرم الحلبي | 09:24 خروج: كرم الحلبي\n10:12 دخول: رامز السعدي | 10:14 خروج: رامز السعدي\n10:41 دخول: رامز السعدي | 10:44 خروج: رامز السعدي\n(لا قيود أخرى حتى 11:30)",
  ["a_get_staff_log"], ["f_mansour_coat", "f_ramez_found", "f_coat_early"], "strong",
  "يسجل بطاقات الداخلين فقط؛ لا يرى من يدخل خلف حامل بطاقة أو والباب مفتوح، ولا يبيّن ما فعله أحد داخل الغرفة.",
  contradicts=["cl_ramez_inference"], loc="loc_staff")
V("ev_office_door_log", "سجل قارئ باب مكتب أمينة المتحف", "digital",
  "سجل قارئ بطاقات باب مكتب أمينة المتحف — اليوم\n09:45 دخول: سلوى الحسيني | 09:56 خروج: سلوى الحسيني\n09:57 دخول: رامز السعدي | 10:00 خروج: رامز السعدي\n10:05 دخول: سلوى الحسيني\n(لا قيود أخرى بين 08:00 و11:00)",
  ["a_get_office_log"], ["f_ramez_asked", "f_mansour_not_office"], "strong",
  "يسجل البطاقات فقط ولا يبيّن ما فعله الداخل في المكتب؛ ويمكن لمن يدخل خلف غيره ألا يظهر فيه.", loc="loc_office")
V("ev_cabinet_log", "سجل قارئ لوحة المفاتيح", "digital",
  "سجل قارئ لوحة المفاتيح في مكتب أمينة المتحف (لا يسجل هوية من يستعملها):\n09:50 وسم مفتاح الخزانة 4: إعادة\n09:58 وسم مفتاح الخزانة 4: سحب\n10:05 إنذار: وسم مفتاح الخزانة 4 غائب",
  ["a_get_cabinet"], ["f_key_returned", "f_curator_away"], "strong",
  "يثبت وقت الإعادة والسحب لا هوية الساحب، ولا ما جرى للمفتاح بعد سحبه.", loc="loc_office")
V("ev_round_scans", "سجل نقاط جولة منصور", "digital",
  "سجل وسوم نقاط التفقد — منصور الأيوبي\nنقاط الجولة الست تتكرر كل نصف ساعة؛ النقطة 4 عند الخزانة 4، والنقطتان 1 و2 قرب القاعة 2.\n09:40 ن1 | 09:45 ن2 | 09:50 ن3 | 09:55 ن4 | 10:00 ن5 | 10:05 ن6\n10:10 ن1 | 10:15 ن2 | 10:20 ن3 | 10:25 ن4 | 10:30 ن5 | 10:35 ن6 | 10:40 ن1",
  ["a_get_rounds"], ["f_mansour_rounds", "f_mansour_elsewhere"], "strong",
  "يثبت مرور وسم منصور بالنقاط في هذه الأوقات، لا أنه حمل الوسم بنفسه في كل لحظة؛ والفراغ بين نقطتين خمس دقائق.",
  contradicts=["cl_karam_unusual", "cl_ramez_inference"], loc="loc_gallery")
V("ev_cleaning_sheet", "ورقة تنظيف غرفة الموظفين", "documentary",
  "ورقة تنظيف غرفة الموظفين — اليوم\nالبدء: 08:15 | الانتهاء: 08:30\nملاحظات العاملة: «معطف رمادي عليه بطاقة اسم م. الأيوبي معلق على الشماعة الثالثة. جيوبه مغلقة بالأزرار».",
  ["a_get_cleaning"], ["f_coat_early"], "moderate",
  "ورقة مكتوبة بخط اليد من عاملة التنظيف؛ تثبت وجود المعطف 08:30 ولا تفحص ما في داخل جيوبه.", contradicts=["cl_ramez_inference"], loc="loc_staff")
V("ev_ticket_desk_log", "سجل عمليات شباك التذاكر", "digital",
  "سجل عمليات شباك التذاكر — وردية كرم الحلبي (09:30 إلى 11:00)\nعمليات البيع: 09:36، 09:41، 09:47، 09:52، 09:58، 10:03، 10:09، 10:12، 10:19، 10:26، 10:33، 10:38، 10:41، 10:46، 10:52",
  ["a_get_desk"], ["f_karam_desk"], "strong",
  "يثبت أن شباك التذاكر كان يعمل بحسابه في هذه الأوقات؛ لا يستبعد أن يغيب صاحبه دقيقة بين عمليتين.", loc="loc_desk")
V("ev_curator_statement", "إفادة سلوى الحسيني (ملخص)", "testimonial",
  "ملخص إفادة سلوى الحسيني، أمينة المتحف:\n«أعدت وسم المفتاح 09:50. خرجت 09:56 لاستقبال مجموعة وتركت اللوحة مفتوحة دقائق. قبل خروجي بدقيقة جاءني رامز يسأل عن المفتاح لفحص الخزانة 4، فأحلته إلى رئيس القاعات. عدت 10:05 فوجدت الوسم غائباً. لم يأتِ منصور مكتبي هذا الصباح.»",
  ["a_note_curator"], ["f_key_returned", "f_curator_away", "f_ramez_asked", "f_mansour_not_office"], "moderate",
  "ذاكرة شاهدة عن أوقات قريبة؛ تحتاج إلى سجل يؤيد الترتيب، وهي تعترف بتقصيرها في ترك اللوحة مفتوحة.", loc="loc_office")
V("ev_guide_statement", "إفادة ياسمين الخطيب (ملخص)", "testimonial",
  "ملخص إفادة ياسمين الخطيب، مرشدة الزوار:\n«كنت مع مجموعة مدرسية في القاعة 2 من 10:05 إلى 10:30. فتح لنا منصور الباب نحو 10:10 ثم تابع جولته. لا أعرف شيئاً عن المفتاح.»",
  ["a_note_guide"], ["f_guide_saw"], "moderate",
  "شاهدة لا مصلحة لها في الترقية، لكن ذاكرتها عن الوقت تقريبية؛ وتصف ما رأته مع مجموعتها فقط.", loc="loc_gallery")
V("ev_ramez_statement", "إفادة رامز السعدي (ملخص)", "testimonial",
  "ملخص إفادة رامز السعدي:\n«كنت قرب مكتب أمينة المتحف نحو العاشرة إلا خمس أنتظر رئيس القاعات. دخلت غرفة الموظفين نحو 10:12 لآخذ جهاز اللاسلكي، ثم نحو 10:41 لأتفقد المعاطف بعد أن أخبرني كرم أن منصور كان قرب الخزانة، فوجدت المفتاح في معطفه وأبلغت.»",
  ["a_note_ramez"], ["f_ramez_found"], "weak",
  "إفادة متقدم للرئاسة وصاحب البلاغ؛ تُقاس بسجلات الأبواب والوسوم.", loc="loc_admin")
V("ev_karam_statement", "إفادة كرم الحلبي (ملخص)", "testimonial",
  "ملخص إفادة كرم الحلبي:\n«رأيت منصور من نافذة الشباك يمرّ قرب الخزانة 4 نحو 09:55 فظننت أن هذا غير عادي وأخبرت رامز ونادر. أنا في الشباك منذ 09:30.»",
  ["a_note_karam"], ["f_karam_saw", "f_karam_desk"], "weak",
  "إفادة متقدم للرئاسة؛ تصف ما رآه وتضيف تفسيراً من عنده.", loc="loc_desk")
V("ev_mansour_statement", "إفادة منصور الأيوبي (ملخص)", "testimonial",
  "ملخص إفادة منصور الأيوبي:\n«علقت معطفي 08:05 وخرجت. جولتي تمرّ بالخزانة 4 في كل دورة. لا أعرف كيف وصل المفتاح إلى جيبي.»",
  ["a_note_mansour"], ["f_mansour_coat", "f_mansour_rounds"], "moderate",
  "إفادة صاحب الاتهام؛ تؤيدها سجلات الأبواب والوسوم ولا تغني عنها.", loc="loc_gallery")

# ---------------------------------------------------------------- inferences
def P(t, i): return {"ref_type": t, "ref_id": i}
inf = []
def I(id, prem, ct, concl, rel, strength, rule, ks):
    inf.append({"id": id, "premises": prem, "conclusion": {"ref_type": ct, "ref_id": concl}, "relation": rel, "strength": strength, "rule_ar": rule, "skill_ko_refs": ks})
# path A: machine logs of doors, key board and round tags
I("i_a_coat", [P("evidence", "ev_staff_door_log"), P("evidence", "ev_cabinet_log")], "fact", "f_coat_early", "establishes", "strong",
  "قارئ الغرفة يضع دخول منصور 08:05، وقارئ اللوحة يضع سحب الوسم 09:58؛ فالمعطف سبق خروج المفتاح بنحو ساعة ونصف.", ["KO-RS-05-005", "KO-RS-06-017"])
I("i_a_mansour", [P("evidence", "ev_round_scans"), P("evidence", "ev_office_door_log"), P("evidence", "ev_staff_door_log")], "fact", "f_mansour_elsewhere", "establishes", "strong",
  "وسوم الجولة كل خمس دقائق تغطي وقت سحب الوسم وزيارتي رامز، وقارئا البابين لا يسجلان لمنصور دخولاً بعد 08:07؛ فمنصور كان في جولته.", ["KO-RS-05-005", "KO-RS-06-001"])
I("i_a_ramez", [P("evidence", "ev_cabinet_log"), P("evidence", "ev_office_door_log"), P("evidence", "ev_staff_door_log")], "fact", "f_ramez_only", "establishes", "strong",
  "الوسم سُحب 09:58 وبطاقة رامز وحدها سجّلت دخول المكتب بين 09:57 و10:00، ثم سجّلت بطاقته وحدها دخول غرفة الموظفين 10:12 و10:41؛ فهو الوحيد الذي ربطته السجلات بالموضعين في الفترة.", ["KO-RS-05-005", "KO-RS-06-001"])
I("i_a_karam", [P("evidence", "ev_staff_door_log"), P("evidence", "ev_office_door_log")], "fact", "f_karam_elsewhere", "establishes", "strong",
  "آخر دخول لكرم في أي من البابين 09:24 غرفة الموظفين، ولا قيد له في المكتب؛ فلا أثر لبطاقته في الفترة التي سُحب فيها الوسم ووُضع.", ["KO-RS-05-005"])
I("i_a_sources", [P("evidence", "ev_sightings"), P("evidence", "ev_promo_notice")], "fact", "f_sightings_two_sources", "establishes", "strong",
  "البلاغان المباشران من متقدمَين للرئاسة، والثالث سمعه صاحبه من أحدهما؛ فلا استقلال بين البلاغات الثلاثة، وكلها تصف مروراً.", ["KO-RS-05-001", "KO-RS-06-002"])
# path B: cleaner, curator, guide, desk and the report-maker's own account
I("i_b_coat", [P("evidence", "ev_cleaning_sheet"), P("evidence", "ev_curator_statement")], "fact", "f_coat_early", "establishes", "strong",
  "عاملة التنظيف سجلت المعطف معلقاً 08:30، والأمينة تقول إن الوسم بقي في اللوحة حتى خروجها 09:56؛ فالمعطف سبق خروج المفتاح.", ["KO-RS-05-005", "KO-RS-06-017"])
I("i_b_mansour", [P("evidence", "ev_guide_statement"), P("evidence", "ev_curator_statement")], "fact", "f_mansour_elsewhere", "establishes", "strong",
  "مرشدة لا مصلحة لها رأت منصور يفتح باب القاعة 2 نحو 10:10، أي وقت دخول رامز الغرفة، والأمينة تقول إنه لم يأتِ مكتبها؛ فمنصور في جولته لا في المكتب ولا في الغرفة.", ["KO-RS-05-005", "KO-RS-06-001"])
I("i_b_ramez", [P("evidence", "ev_curator_statement"), P("evidence", "ev_ramez_statement")], "fact", "f_ramez_only", "establishes", "strong",
  "الأمينة تقول إن رامز كان عند بابها قبل خروجها بدقيقة وطلب المفتاح، ورامز يقر بأنه دخل غرفة الموظفين مرتين قبل أن يُعثر على المفتاح؛ فهو مرتبط بالموضعين من أقواله هو.", ["KO-RS-05-014", "KO-RS-06-001"])
I("i_b_karam", [P("evidence", "ev_ticket_desk_log")], "fact", "f_karam_elsewhere", "establishes", "strong",
  "عمليات البيع متصلة من 09:36 إلى 10:52 وتشمل 09:58 و10:12 و10:41؛ فكرم كان خلف الشباك في الأوقات الثلاثة.", ["KO-RS-05-005"])
# hypothesis ledger
I("i_support_ramez", [P("fact", "f_ramez_only"), P("fact", "f_coat_early")], "hypothesis", "h_ramez", "supports", "strong",
  "المعطف سبق خروج المفتاح، والمفتاح خرج من اللوحة ثم ظهر في غرفة الموظفين، ورامز وحده ارتبط بالمكانين في الفترة؛ فأرجح تفسير أنه حمله ووضعه ثم أبلغ.", ["KO-RS-06-001"])
I("i_rule_mansour", [P("fact", "f_coat_early"), P("fact", "f_mansour_elsewhere")], "hypothesis", "h_mansour", "rules_out", "conclusive",
  "من علّق معطفه قبل خروج المفتاح بساعة ونصف وبقي في جولته ولم يدخل المكتب ولا الغرفة بعد ذلك لا يمكن أن يكون من نقل المفتاح إلى معطفه.", ["KO-RS-06-008"])
I("i_rule_karam", [P("fact", "f_karam_elsewhere")], "hypothesis", "h_karam", "rules_out", "strong",
  "من لازم الشباك في الأوقات التي سُحب فيها الوسم ووُضع المفتاح، ولا أثر لبطاقته في البابين، لا يصح أن يكون هو من فعل ذلك.", ["KO-RS-06-008"])
I("i_rule_chance", [P("fact", "f_coat_early"), P("fact", "f_ramez_only")], "hypothesis", "h_chance", "rules_out", "strong",
  "المفتاح خرج من لوحة في مكتب إلى جيب مغلق في غرفة أخرى بعد أن عُلّق المعطف؛ فلا بد أن حمله شخص، ولا يُنسى مفتاح موسوم صدفة في معطف زميل بعد سحبه من اللوحة بقليل.", ["KO-RS-06-008"])
I("i_claim_ramez", [P("fact", "f_coat_early"), P("fact", "f_mansour_elsewhere")], "claim", "cl_ramez_inference", "contradicts_claim", "strong",
  "وجود المفتاح في المعطف لا يدل على أن صاحبه وضعه؛ فالمعطف كان معلقاً قبل خروج المفتاح، وصاحبه كان في جولته.", ["KO-RS-05-001", "KO-RS-06-004"])
I("i_claim_karam", [P("fact", "f_mansour_elsewhere")], "claim", "cl_karam_unusual", "contradicts_claim", "strong",
  "نقطة الجولة الرابعة عند الخزانة 4 في كل دورة؛ فمرور منصور بها 09:55 جزء من عمله لا شذوذ.", ["KO-RS-05-001"])
I("i_rule_mansour_src", [P("fact", "f_sightings_two_sources")], "hypothesis", "h_mansour", "rules_out", "suggestive",
  "البلاغات الثلاثة لا تعدّ ثلاثة أدلة مستقلة؛ هي مرور عادي رآه متقدمان للرئاسة وسامع منهما، فلا تحمل وزناً كبيراً ضد منصور.", ["KO-RS-05-004"])

# ---------------------------------------------------------------- character knowledge
K = lambda f, a="witnessed", c="certain": {"fact_id": f, "access": a, "certainty": c}
ck = [
    {"character_id": "mansour", "knows": [K("f_mansour_coat"), K("f_mansour_rounds")], "hides": [], "believes": []},
    {"character_id": "ramez", "knows": [K("f_ramez_found")],
     "hides": [{"fact_id": "f_ramez_took", "reveal_when": {"presented": {"evidence_id": "ev_office_door_log", "to_character": "ramez"}}, "cover_claim_id": "cl_ramez_inference", "reveal_line_id": "rm_took"}],
     "believes": [{"claim_id": "cl_ramez_inference", "stance": "deliberate_lie"}]},
    {"character_id": "karam", "knows": [K("f_karam_desk"), K("f_karam_saw")], "hides": [], "believes": [{"claim_id": "cl_karam_unusual", "stance": "sincere"}]},
    {"character_id": "salwa", "knows": [K("f_key_returned"), K("f_curator_away"), K("f_ramez_asked"), K("f_mansour_not_office")], "hides": [], "believes": []},
    {"character_id": "yasmin", "knows": [K("f_guide_saw", "witnessed", "fairly_sure")], "hides": [], "believes": []},
]
hyps = [
    {"id": "h_ramez", "statement_ar": "سحب رامز وسم المفتاح من اللوحة ووضعه في معطف منصور، ثم أبلغ عن «العثور» عليه.", "is_true": True, "plausibility_at_start": "low", "suspect_id": "ramez"},
    {"id": "h_mansour", "statement_ar": "أخذ منصور المفتاح وأخفاه في جيب معطفه.", "is_true": False, "plausibility_at_start": "high", "suspect_id": "mansour"},
    {"id": "h_karam", "statement_ar": "أخذ كرم المفتاح وألقاه في المعطف ليُتّهم منصور.", "is_true": False, "plausibility_at_start": "medium", "suspect_id": "karam"},
    {"id": "h_chance", "statement_ar": "لم يتعمد أحد شيئاً؛ نسي أحدهم المفتاح في جيب المعطف مصادفة.", "is_true": False, "plausibility_at_start": "low"},
]
mis = [
    {"id": "rh_found", "points_to_hypothesis_id": "h_mansour", "planted_via_ar": "المفتاح وُجد في جيب معطف منصور، فيبدو أنه هو من خبّأه.", "evidence_ids": ["ev_incident_report"],
     "refuted_by_inference_ids": ["i_rule_mansour", "i_a_coat", "i_b_coat", "i_claim_ramez"],
     "fairness_note_ar": "التقرير يذكر مكان العثور لا من وضعه؛ وسجل الغرفة وورقة التنظيف يضعان المعطف معلقاً قبل خروج المفتاح من اللوحة، وسجلات الجولة تضع صاحبه بعيداً."},
    {"id": "rh_sightings", "points_to_hypothesis_id": "h_mansour", "planted_via_ar": "ثلاثة زملاء يقولون إنهم رأوه قرب الخزانة، فيبدو أن الأمر متفق عليه.", "evidence_ids": ["ev_sightings"],
     "refuted_by_inference_ids": ["i_rule_mansour_src", "i_a_sources", "i_claim_karam", "i_rule_mansour"],
     "fairness_note_ar": "حقل «المصدر» في الملخص يبيّن أن اثنين رأيا مروراً والثالث سمع من أحدهما، وسجل الجولة يبيّن أن نقطة الخزانة جزء من مسار منصور في كل دورة."},
]
los = [
    {"id": "lo_claim", "statement_ar": "يسأل من أين جاء كل دليل ومن المستفيد منه، ويفرّق بين مكان العثور على شيء ومن وضعه.", "skill_ko_ref": "KO-RS-05-001", "observable_behaviors_ar": ["يصنّف الإفادات أقوالاً", "يحدد مصدر كل بلاغ"], "evidence_sources": ["evidence_board"]},
    {"id": "lo_timeline", "statement_ar": "يرتّب سجلات الأبواب واللوحة والجولة على خط زمني ليعرف ما سبق ما.", "skill_ko_ref": "KO-RS-05-005", "observable_behaviors_ar": ["يضع المعطف والسحب والبلاغ في أزمنتها"], "evidence_sources": ["timeline_task", "action_log"]},
    {"id": "lo_hyp", "statement_ar": "يوازن بين عدة فرضيات ويستبعد ما تنقضه الأدلة.", "skill_ko_ref": "KO-RS-05-002", "observable_behaviors_ar": ["يضيف فرضيات", "يستبعد بدليل"], "evidence_sources": ["hypothesis_ledger"]},
    {"id": "lo_diag", "statement_ar": "يقدّر ما يثبته كل سجل وما لا يثبته، ويربط الدليل بالفرضية باتجاه صحيح.", "skill_ko_ref": "KO-RS-06-002", "observable_behaviors_ar": ["يعرف حدود قارئ البطاقات", "يربط الدليل بالفرضية"], "evidence_sources": ["evidence_board", "final_justification"]},
    {"id": "lo_calib", "statement_ar": "يصوغ نسبة الترجيح بحدودها.", "skill_ko_ref": "KO-RS-06-021", "observable_behaviors_ar": ["يختار ثقة معقولة", "يذكر حدوداً"], "evidence_sources": ["final_justification"]},
    {"id": "lo_revise", "statement_ar": "يراجع رأيه الأول حين يظهر ما يخالفه.", "skill_ko_ref": "KO-RS-06-009", "observable_behaviors_ar": ["يغيّر فرضيته الرائدة بدليل"], "evidence_sources": ["hypothesis_ledger"]},
]
def levels(d): return [{"score": i, "descriptor_ar": t} for i, t in enumerate(d)]
rub = {
    "reference_answer_ar": "منصور لم يأخذ المفتاح. معطفه كان معلقاً في غرفة الموظفين منذ 08:05 وأكدته ورقة التنظيف عند الثامنة والنصف، أي قبل خروج الوسم من اللوحة 09:58 بنحو ساعة ونصف، وهو كان طوال ذلك في جولته ووسومه تمرّ كل خمس دقائق، ولم يسجّل قارئ البابين دخوله بعد 08:07. أما رامز فهو الذي ارتبطت بطاقته بمكتب الأمينة حين سُحب الوسم وبغرفة الموظفين قبل «العثور»، وأقواله هو والأمينة تتفق مع ذلك. والبلاغات الثلاثة صادرة عن متقدمَين للرئاسة وسامع منهما وتصف مروراً عادياً. حدود الاستنتاج: قد يتجاوز القارئ شخصاً دخل في أثر غيره، ولا تثبت السجلات نية رامز ولا لحظة وضع المفتاح، وقد يوجد تفسير لم تغطه السجلات.",
    "criteria": [
        {"id": "c_source", "name_ar": "تصنيف المصادر", "objective_ids": ["lo_claim"], "scored_by": "deterministic", "weight": 0.15, "levels": levels(["لم يصنّف", "أخطأ في الأغلب", "نصف صحيح", "معظمه صحيح", "كله صحيح"])},
        {"id": "c_conflict", "name_ar": "ترتيب الأحداث على الخط الزمني", "objective_ids": ["lo_timeline"], "scored_by": "deterministic", "weight": 0.2, "levels": levels(["لم يضع شيئاً", "وضع قليلاً", "وضع نصفها صحيحاً", "معظمها", "كلها في موضعها"])},
        {"id": "c_links", "name_ar": "ربط الأدلة بالفرضيات", "objective_ids": ["lo_diag"], "scored_by": "deterministic", "weight": 0.2, "levels": levels(["لا روابط", "قليلة", "نصفها صحيح", "معظمها", "كلها دقيقة"])},
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
    H("hg1", 1, "metacognitive", "قبل أن تقرر من أخذ المفتاح، اسأل: من أين جاء كل دليل، وماذا يكسب صاحبه؟", {"always": True}, None, 0.02),
    H("hg2", 2, "focus_area", "ضع كل بلاغ في جدول: من قاله؟ هل رأى بنفسه أم سمع؟ وهل هو متقدم للرئاسة؟", he("ev_sightings"), None, 0.04),
    H("hg3", 3, "pointer", "ابحث عن سجلات لا مصلحة لأحد فيها: قارئات الأبواب واللوحة ووسوم الجولة.", he("ev_sightings"), None, 0.08),
    H("hc1", 1, "metacognitive", "متى عُلّق المعطف؟ ومتى خرج الوسم من اللوحة؟ أيهما سبق الآخر؟", he("ev_incident_report"), "i_a_coat", 0.02),
    H("hc2", 2, "pointer", "قارن وقت دخول منصور غرفة الموظفين بوقت سحب الوسم في سجل اللوحة.", he("ev_incident_report"), "i_a_coat", 0.06),
    H("hc3", 3, "partial_reveal", "اطلب سجل باب غرفة الموظفين وسجل لوحة المفاتيح وضعهما معاً على الخط الزمني، ثم انظر من دخل بعد 09:58.", he("ev_incident_report"), "i_a_coat", 0.1),
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
Act("a_get_report", "examine", "اقرأ تقرير الحادث", al, [G("ev_incident_report")], "loc_admin", "GET_REPORT")
Act("a_get_sightings", "examine", "اطلب ملخص البلاغات الثلاثة", al, [G("ev_sightings")], "loc_admin", "GET_SIGHTINGS")
Act("a_get_promo", "examine", "اقرأ إعلان شغور رئاسة الفريق", al, [G("ev_promo_notice")], "loc_admin", "GET_PROMO")
Act("a_get_staff_log", "examine", "اطلب سجل باب غرفة الموظفين بإذن الإدارة", al, [G("ev_staff_door_log")], "loc_staff", "GET_STAFF_LOG")
Act("a_get_office_log", "examine", "اطلب سجل باب مكتب الأمينة بإذن الإدارة", al, [G("ev_office_door_log")], "loc_office", "GET_OFFICE_LOG")
Act("a_get_cabinet", "examine", "اطلب سجل قارئ لوحة المفاتيح بإذن الإدارة", al, [G("ev_cabinet_log")], "loc_office", "GET_CABINET")
Act("a_get_rounds", "examine", "اطلب سجل وسوم جولة التفقد", al, [G("ev_round_scans")], "loc_gallery", "GET_ROUNDS")
Act("a_get_cleaning", "examine", "اطلب ورقة تنظيف غرفة الموظفين", al, [G("ev_cleaning_sheet")], "loc_staff", "GET_CLEANING")
Act("a_get_desk", "examine", "اطلب سجل عمليات شباك التذاكر", al, [G("ev_ticket_desk_log")], "loc_desk", "GET_DESK")
for cid, lab in [("mansour", "منصور"), ("ramez", "رامز"), ("karam", "كرم"), ("salwa", "سلوى"), ("yasmin", "ياسمين")]:
    Act(f"a_int_{cid}", "interview", f"ابدأ مقابلة {lab}", al, [{"op": "raise_trust", "ref_id": cid, "amount": 1}], cid, f"INT_{cid.upper()}")
Act("a_note_curator", "examine", "دوّن إفادة سلوى", fu("f_key_returned"), [G("ev_curator_statement")], "salwa", "NOTE_CURATOR")
Act("a_note_guide", "examine", "دوّن إفادة ياسمين", fu("f_guide_saw"), [G("ev_guide_statement")], "yasmin", "NOTE_GUIDE")
Act("a_note_ramez", "examine", "دوّن إفادة رامز", fu("f_ramez_found"), [G("ev_ramez_statement")], "ramez", "NOTE_RAMEZ")
Act("a_note_karam", "examine", "دوّن إفادة كرم", fu("f_karam_saw"), [G("ev_karam_statement")], "karam", "NOTE_KARAM")
Act("a_note_mansour", "examine", "دوّن إفادة منصور", fu("f_mansour_coat"), [G("ev_mansour_statement")], "mansour", "NOTE_MANSOUR")
Act("p_office_ramez", "present_evidence", "اعرض سجل باب مكتب الأمينة على رامز", {"presented": {"evidence_id": "ev_office_door_log", "to_character": "ramez"}}, [{"op": "emit_event", "ref_id": "PRESENTED_OFFICE_LOG"}], "ramez", "P_OFFICE_RAMEZ", 0)
Act("a_hint", "request_hint", "اطلب تلميحاً", al, [], None, "REQUEST_HINT", 0)
Act("a_accuse", "final_accusation", "قدّم الاستنتاج النهائي", al, [{"op": "emit_event", "ref_id": "SUBMIT"}], None, "FINAL_ACCUSATION", 0)

topics = [
    {"id": "t_coat", "label_ar": "المعطف والغرفة", "example_questions_ar": ["متى علّقت المعطف؟", "هل عدت إلى غرفة الموظفين؟"], "fact_ids": ["f_mansour_coat", "f_ramez_found"], "claim_ids": ["cl_ramez_inference"]},
    {"id": "t_rounds", "label_ar": "الجولة والخزانة 4", "example_questions_ar": ["أين كنت صباحاً؟", "ماذا رأيت قرب الخزانة؟"], "fact_ids": ["f_mansour_rounds", "f_karam_saw", "f_guide_saw"], "claim_ids": ["cl_karam_unusual"]},
    {"id": "t_key", "label_ar": "المفتاح واللوحة", "example_questions_ar": ["متى أعيد المفتاح؟", "من سأل عنه؟", "هل جاء منصور إلى المكتب؟"], "fact_ids": ["f_key_returned", "f_curator_away", "f_ramez_asked", "f_mansour_not_office"]},
    {"id": "t_desk", "label_ar": "الشباك", "example_questions_ar": ["أين كنت من 09:30؟"], "fact_ids": ["f_karam_desk"]},
    {"id": "t_after", "label_ar": "ما جرى للمفتاح", "example_questions_ar": ["كيف وصل المفتاح إلى المعطف؟"], "fact_ids": ["f_ramez_took"]},
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
    (1, "المفتاح وُجد في معطف منصور، لكن مكان العثور لا يقول من وضعه؛ فسجل الغرفة يضع معطفه 08:05 وورقة التنظيف تؤيد ذلك 08:30، وسجل اللوحة يضع سحب الوسم 09:58.", ["ev_staff_door_log", "ev_cabinet_log", "ev_cleaning_sheet"], "i_a_coat"),
    (2, "منصور في جولته: وسومه كل خمس دقائق، وقارئا البابين لا يسجلان له دخولاً بعد 08:07، والمرشدة رأته في القاعة 2 نحو 10:10 والأمينة تقول إنه لم يأتِ مكتبها.", ["ev_round_scans", "ev_office_door_log", "ev_staff_door_log", "ev_guide_statement", "ev_curator_statement"], "i_a_mansour"),
    (3, "البلاغات الثلاثة ليست ثلاثة أدلة: اثنان رأيا مروراً والثالث سمع من أحدهما، وصاحبا البلاغين متقدمان للرئاسة نفسها.", ["ev_sightings", "ev_promo_notice"], "i_a_sources"),
    (4, "كرم في الشباك طوال الفترة: عملياته متصلة، ولا أثر لبطاقته في البابين بعد 09:24.", ["ev_ticket_desk_log", "ev_staff_door_log", "ev_office_door_log"], "i_b_karam"),
    (5, "رامز وحده ارتبطت بطاقته بمكتب الأمينة حين سُحب الوسم وبغرفة الموظفين قبل بلاغه؛ وأقواله هو وأقوال الأمينة تتفق مع قارئي البابين.", ["ev_cabinet_log", "ev_office_door_log", "ev_staff_door_log", "ev_curator_statement", "ev_ramez_statement"], "i_a_ramez"),
    (6, "إذن لم ينسَ أحد المفتاح في المعطف: حمله شخص بعد سحبه، والأرجح أنه رامز، ثم أبلغ عن العثور عليه.", ["ev_staff_door_log", "ev_cabinet_log"], "i_support_ramez"),
]
ending = {
    "steps": [{"order": o, "text_ar": t, "uses_evidence_ids": u, "inference_id": i} for o, t, u, i in steps],
    "alternative_paths_ar": [
        "يمكن الوصول إلى النتيجة من سجلات الأبواب واللوحة والوسوم وحدها دون أن تسأل أحداً، لكن من يفعل ذلك قد يتجاهل أن الأمينة نفسها قصّرت بترك اللوحة مفتوحة.",
        "ويمكن الوصول إليها من ورقة التنظيف وإفادات الأمينة والمرشدة وكرم ورامز وسجل الشباك دون قراءة قارئات الأبواب؛ والأقوى أن يتفق المساران.",
    ],
    "what_evidence_could_not_show_ar": [
        "لا تثبت السجلات لحظة وضع المفتاح في الجيب ولا نية رامز؛ تثبت الارتباط بالمكانين في الفترة فقط.",
        "قارئ البطاقات لا يرى من يدخل خلف حامل بطاقة أو والباب مفتوح، فلا يستبعد وجود شخص لم تسجله البطاقات.",
        "لا تبيّن السجلات هل استعمل رامز المفتاح قبل أن يضعه أم لا.",
    ],
    "science_notes_ar": [
        "مكان العثور على شيء لا يدل على من وضعه؛ اسأل: ما الذي سبق ما؟ ومن كان يستطيع الوصول؟",
        "الدليل الذي يأتي من شخص له مصلحة في النتيجة يُقاس بسجل لا مصلحة لأحد فيه؛ وثلاثة أقوال من مصدرين ليست ثلاثة أدلة مستقلة.",
        "تتبّع المفتاح بسجلات الأبواب واللوحة شبيه بسلسلة العهدة، ويبقى ما نسميه نسبة الترجيح حكماً قابلاً للمراجعة.",
    ],
}
core = {
    "schema_version": "0.1.0", "case_id": CID, "case_version": "0.1.0",
    "meta": {"title_ar": "المفتاح في جيب المعطف", "title_en": "The Key in the Coat Pocket", "age_band": "13-15", "locale": "ar", "dialogue_register": "msa", "estimated_minutes": 30, "difficulty": 2,
             "content_flags": ["no_violence", "theft"], "authors": ["فريق أثر التحريري (مسودة بمساعدة الذكاء الاصطناعي، لم تُراجَع بشرياً بعد)"],
             "knowledge_object_refs": ["KO-RS-05-001", "KO-RS-05-004", "KO-RS-05-005", "KO-RS-05-002", "KO-RS-06-002", "KO-RS-06-001", "KO-RS-06-009", "KO-RS-06-021"]},
    "premise": {"hook_ar": "مفتاح خزانة عرض وُجد في جيب حارس عمره في المتحف ثلاثون سنة، وثلاثة زملاء يقولون إنهم رأوه. لكن من أين جاءت هذه الأدلة؟",
                "player_role_ar": "أنت متدرب في إدارة متحف الأثر، وطُلب منك أن تراجع الاتهام الموجّه إلى حارس القاعات.",
                "setting_ar": "متحف الأثر في المرسى، صباح يوم عادي. بإذن مكتوب من الإدارة تطّلع على سجلات الأبواب واللوحة والجولة، ولا تفتح غيرها.",
                "public_fact_ids": ["f_key_missing", "f_key_found_coat", "f_three_saw"],
                "assumed_general_knowledge_ar": ["قارئ البطاقات يسجل البطاقة لا الشخص", "من يعثر على شيء لا يلزم أن يكون هو من وضعه"]},
    "entities": {"characters": chars, "locations": locations, "objects": objects, "organizations": orgs},
    "truth": {"solution": {"culprit_ids": ["ramez"], "summary_ar": "لم يخبئ منصور المفتاح. حمله مساعد العرض رامز من اللوحة بعد خروج الأمينة ووضعه في معطف علّقه صاحبه قبل ذلك بساعات، ثم قدّم نفسه بوصفه من عثر عليه. أما البلاغات الثلاثة فمرجعها شخصان يتنافسان على الرئاسة ذاتها، ولا تصف غير مرور اعتيادي.", "key_fact_ids": ["f_coat_early", "f_mansour_elsewhere", "f_ramez_only", "f_karam_elsewhere"]},
              "facts": facts, "claims": claims},
    "timeline": timeline, "evidence": ev, "evidence_graph": {"inferences": inf},
    "character_knowledge": ck, "hypotheses": hyps, "misdirection_plan": mis, "learning_objectives": los,
    "mechanics": {"time_budget_units": 40, "actions": A},
    "state_machine": {"id": "c015", "initial": "briefing", "type": "compound", "states": {
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
    "clock": {"epoch_hhmm": "08:00", "zone_label_ar": "توقيت المتحف"},
    "cover": {"title_ar": "المفتاح في جيب المعطف", "tagline_ar": "ثلاثة بلاغات ومعطف واحد… فمن أين جاءت الأدلة؟", "kicker_ar": "الملف الخامس عشر · مصدر الدليل", "glyph": "⚿", "accent": "rose"},
    "cold_open_ar": ["العاشرة والنصف صباحاً في متحف الأثر.", "اختفى وسم مفتاح خزانة العرض 4، ثم أُبلغ أنه وُجد في جيب معطف الحارس منصور.",
                     "ثلاثة زملاء يقولون إنهم رأوه قرب الخزانة، والإدارة تميل إلى إقفال الملف بسرعة.",
                     "قبل أن تحكم، ارسم لكل دليل سؤالين: من جاء به؟ وماذا يكسب؟"],
    "labs": [],
    "source_classes": [
        {"id": "primary_record", "label_ar": "سجل أصلي", "help_ar": "يُنتجه نظام أو شخص لحظة الحدث دون وسيط، كقارئ باب أو قارئ لوحة أو ورقة تنظيف."},
        {"id": "redisplay", "label_ar": "نسخة معروضة", "help_ar": "معلومة نُقلت من سجل آخر أو لُخّصت منه."},
        {"id": "claim", "label_ar": "قول أو تصريح", "help_ar": "إفادة شخص؛ تُقاس بالسجلات وبمصلحة صاحبها لا بنبرته."},
        {"id": "template", "label_ar": "قالب أو نموذج", "help_ar": "نص جاهز لا يصف الحدث الفعلي بذاته."},
        {"id": "public_document", "label_ar": "وثيقة منشورة", "help_ar": "وثيقة معلنة ومعروف ناشرها، كإعلان داخلي أو تقرير."}],
    "limit_menu": [
        {"id": "l_tailgate", "label_ar": "قارئ البطاقات لا يرى من يدخل خلف حامل بطاقة، فلا يستبعد وجود شخص لم تسجله البطاقات"},
        {"id": "l_intent", "label_ar": "السجلات لا تثبت نية رامز ولا لحظة وضع المفتاح"},
        {"id": "l_cabinet_id", "label_ar": "قارئ اللوحة لا يسجل هوية من سحب الوسم"},
        {"id": "l_invalid_found", "label_ar": "العثور على المفتاح في معطف منصور يثبت أنه وضعه"},
        {"id": "l_invalid_motive", "label_ar": "رغبة رامز في الترقية تثبت وحدها أنه الفاعل"}],
    "mind_change_menu": [
        {"id": "m_badge_shared", "label_ar": "ثبوت أن بطاقة رامز استُعملت بيد شخص آخر"},
        {"id": "m_log_edit", "label_ar": "ثبوت أن سجل اللوحة أو سجل الباب عُدّل بعد الحادث"},
        {"id": "m_coat_moved", "label_ar": "ظهور دليل على أن المعطف نُقل من مكانه أو جيوبه فُتحت قبل 09:58"},
        {"id": "m_popular", "label_ar": "كثرة من يظنون أن منصور هو الفاعل"}],
    "skills": [{"skill_id": "KO-RS-05-001", "track": "B"}, {"skill_id": "KO-RS-05-005", "track": "B"}, {"skill_id": "KO-RS-05-004", "track": "B"}, {"skill_id": "KO-RS-06-002", "track": "D"}],
    "stage_hooks_ar": {"briefing": "مفتاح في جيب… وهذا لا يكفي لمعرفة من وضعه.", "investigating": "لا تعدّ البلاغات؛ اسأل من قالها.", "review": "قبل أن تغلق الملف: ما الذي لا تعرفه؟", "resolved": "أُغلق ملف المفتاح، وبقيت لوحة المفاتيح تحتاج إلى قفل أفضل."},
    "character_glyphs": {"mansour": "م", "ramez": "ر", "karam": "ك", "salwa": "س", "yasmin": "ي"},
}
sc = {
    "case_id": CID,
    "accepted_conclusions": {"h_ramez": {"grade": 1, "note_ar": "استنتاج متسق مع الأدلة ويتطلب ذكر حدوده."},
                             "h_mansour": {"grade": 0, "note_ar": "يخلط بين مكان العثور على المفتاح ومن وضعه، ويعدّ ثلاثة بلاغات من مصدرين ثلاثة أدلة."},
                             "h_karam": {"grade": 0, "note_ar": "سجل الشباك وقارئا البابين يضعانه بعيداً عن المكتب والغرفة."},
                             "h_chance": {"grade": 0, "note_ar": "المفتاح خرج من اللوحة بعد تعليق المعطف، فلا بد أن حمله شخص."}},
    "confidence_band": {"h_ramez": [60, 88], "h_mansour": [0, 15], "h_karam": [0, 15], "h_chance": [0, 15]},
    "source_key": {"ev_incident_report": "public_document", "ev_sightings": "redisplay", "ev_promo_notice": "public_document", "ev_staff_door_log": "primary_record", "ev_office_door_log": "primary_record",
                   "ev_cabinet_log": "primary_record", "ev_round_scans": "primary_record", "ev_cleaning_sheet": "primary_record", "ev_ticket_desk_log": "primary_record",
                   "ev_curator_statement": "claim", "ev_guide_statement": "claim", "ev_ramez_statement": "claim", "ev_karam_statement": "claim", "ev_mansour_statement": "claim"},
    "link_key": {
        "h_ramez": {"ev_cabinet_log": "supports", "ev_office_door_log": "supports", "ev_staff_door_log": "supports", "ev_curator_statement": "supports", "ev_ramez_statement": "supports", "ev_incident_report": "neutral"},
        "h_mansour": {"ev_incident_report": "supports", "ev_sightings": "supports", "ev_round_scans": "weakens", "ev_cleaning_sheet": "weakens", "ev_staff_door_log": "weakens", "ev_guide_statement": "weakens", "ev_promo_notice": "weakens"},
        "h_karam": {"ev_ticket_desk_log": "weakens", "ev_staff_door_log": "weakens", "ev_office_door_log": "weakens"},
        "h_chance": {"ev_cabinet_log": "weakens", "ev_cleaning_sheet": "weakens"},
    },
    "required_limits": ["l_tailgate", "l_intent"], "valid_mind_changers": ["m_badge_shared", "m_log_edit", "m_coat_moved"], "invalid_limits": ["l_invalid_found", "l_invalid_motive"],
    "decisive_evidence": ["ev_staff_door_log", "ev_office_door_log", "ev_cabinet_log", "ev_round_scans", "ev_cleaning_sheet"],
    "lab_requirement": None,
    "timeline_requirement": [{"evidence_id": "ev_cleaning_sheet", "utc_minute": 30, "tol": 15}, {"evidence_id": "ev_cabinet_log", "utc_minute": 118, "tol": 10}, {"evidence_id": "ev_incident_report", "utc_minute": 165, "tol": 10}],
    "refuted_hypotheses": ["h_mansour", "h_karam", "h_chance"],
    "criteria_map": {"c_source": "source_typing", "c_conflict": "conflict_resolution", "c_links": "hypothesis_links", "c_uncertainty": "uncertainty", "c_revision": "revision", "c_elimination": "elimination", "c_justification": "justification_human"},
    "caps": {"no_citations_max": 45, "no_conflict_resolution_max": 70},
}
os.makedirs(OUT, exist_ok=True)
for suf, obj in [("", core), (".ui", ui), (".scoring", sc)]:
    with open(os.path.join(OUT, f"{CID}{suf}.json"), "w", encoding="utf8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
print("ok")
