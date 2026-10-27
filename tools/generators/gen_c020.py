#!/usr/bin/env python3
# Case c020 «جلسة استماع في متحف الأثر» — advanced (16-18) hearing case. Teaches: separate the strength of an ARGUMENT from the strength of
# its EVIDENCE; refuse appearance testimony; reconcile two reliable sources (daily-mean dashboard vs raw hourly logger); demand
# independence (two records from one process are one source), and keep the interested speaker's motive apart from proof.
# No-culprit convention: the facilities coordinator whose (unintended) handover gap left the dehumidifier switched off is recorded in
# culprit_ids; nobody damaged the manuscript on purpose. Library seed: S-10 (HER-seeds, ARC-30). Original ATHAR story whose frame
# echoes the cross-cultural «animal fable trial» structure; all names, documents and institutions are fictional.
# Mechanics note: the engine has no two-column "argument vs evidence" sheet and no cross-examination lab, so (a) the separation is
# trained through source typing + hypothesis links + the limit menu, and (b) the expert's written review is a player-visible
# request action (type request_lab_test) that grants one evidence item, as c009 did.
# Calendar (fictional): minute 0 = Thursday 00:00. Thu 14:10 report signed; 14:38 deposit; 20:05 unit switched off; Sat 16:10 restart.
# Usage: gen_c020.py OUT_DIR
import json, sys, os
OUT = sys.argv[1]
CID = "c020_museum_hearing"

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
ch("maher", "ماهر الشامي", "suspect", "نائب مدير المتحف، يتنافس على منصب المدير",
   "رسمي وواثق، يتكلم أولاً في كل جلسة ويعرض الأمور بصيغة الحسم. يعيد ما بلغه بثقة من يظن أن السلطة تغني عن الإسناد، ويصحّح نفسه إن واجهته بسجل.",
   ["أن يُنظر إلى المتحف على أنه يُدار بحزم", "ألا يُقال إنه استغل البلاغ لمصلحته"],
   [L("mh_greet", "greeting", "تفضّل. رفعتُ البلاغ إلى المجلس كما وصلني، وهذا واجبي."),
    L("mh_says", "reveal", "أقول ما أقوله للمجلس: المرمّمة تركت الطقم على طاولتها نهاية الأسبوع، ونمط التلف يشبه ما نراه حين تُساء المعالجة.", ["f_maher_says"]),
    L("mh_dash", "reveal", "راجعتُ لوحة المرافق بنفسي، وهي لم تُصدر أي إنذار رطوبة طوال الأيام الثلاثة.", ["f_dashboard_exists"]),
    L("mh_bench", "reveal", "ما فهمته أن الطقم لم يغادر طاولة المرمّمة قبل نهاية الأسبوع، ولهذا حكمتُ بأنها المسؤولة.", None, ["cl_maher_bench"]),
    L("mh_pattern", "reveal", "التلف بهذا الشكل لا يأتي من غرفة هادئة، فهو عندي دليل على تعامل خاطئ.", None, ["cl_maher_handling"]),
    L("mh_unknown", "deflect_unknown", "لا أملك ما أضيفه على هذا."),
    L("mh_off", "deflect_offtopic", "هذا خارج موضوع الجلسة. اسألني عن البلاغ وما بُني عليه."),
    L("mh_bye", "farewell", "المجلس سيقرر بما يراه، وأنا ملتزم بقراره.")])
ch("salma", "سلمى العمري", "suspect", "مرمّمة أولى مفصولة، في أواخر الثلاثينات",
   "دقيقة في توثيق عملها، وتتحدث بسرعة وتتلعثم حين تشعر أن الأنظار عليها. يجب ألا يُحكم عليها بطريقة كلامها بل بما تُظهره السجلات.",
   ["أن يُراجَع ملفها بسجلات لا بانطباعات", "أن تعود إلى عملها إن ثبتت سلامة معالجتها"],
   [L("sl_greet", "greeting", "أعلم أنني أبدو متوترة، لكنني أحتفظ بكل ما كتبته. اسأل عمّا شئت."),
    L("sl_report", "reveal", "وقّعت تقرير الإنجاز الخميس الساعة 14:10. كانت الأوراق مستقرة ولا بقع عليها.", ["f_report_signed"]),
    L("sl_imaging", "reveal", "بعد التقرير مرّ الطقم بمحطة التصوير الآلية، وهي تفحص الحواف وتحفظ سجلاً مؤرخاً من خادم المتحف.", ["f_imaging_clean"]),
    L("sl_unknown", "deflect_unknown", "لا أعرف، ولا أحب أن أخمّن في أمر يخص مخطوطة."),
    L("sl_off", "deflect_offtopic", "اسألني عن المعالجة والتوثيق."),
    L("sl_bye", "farewell", "شكراً لأنك تقرأ الأوراق قبل أن تحكم عليّ.")])
ch("rima", "ريما الخطيب", "witness", "مسجّلة المجموعات، مسؤولة المخزن",
   "منظمة وهادئة، تقرأ من نماذجها ولا تضيف إليها، وتحرص على أن يبقى كل ما سلّمته أو استلمته مكتوباً بتوقيعها.",
   ["ألا يُنسب إلى المخزن ما لم يُسجَّل فيه", "أن تبقى سلسلة العهدة للمخطوطة واضحة"],
   [L("rm_greet", "greeting", "نماذج الاستلام أمامي. أقرأ منها ولا أضيف إليها."),
    L("rm_intake", "reveal", "استلمت الطقم الخميس 14:38 وفحصته بصرياً وختمت الصندوق، وقد دوّنت ذلك في نموذج الاستلام.", ["f_intake"]),
    L("rm_door", "reveal", "كل دخول إلى المخزن وخروج منه يمر ببطاقة، ونظام الدخول يحتفظ بالسجل.", ["f_door_exists"]),
    L("rm_unknown", "deflect_unknown", "هذا ليس في نماذجي."),
    L("rm_off", "deflect_offtopic", "اسألني عن الاستلام والمخزن."),
    L("rm_bye", "farewell", "العهدة تبقى مكتوبة، فاقرأها.")])
ch("laith", "ليث الحلبي", "witness", "مساعد أمين المعرض، شاب في أوائل العشرينات",
   "ودود ويحب أن يكون له رأي. يخلط بين انطباعه عن الناس وبين ما شاهده فعلاً، ويتراجع عن الجزم إذا طُلب منه ذكر واقعة.",
   ["أن يبدو مفيداً للمجلس", "ألا يُلام على كلمة قالها"],
   [L("lt_greet", "greeting", "أحب أن أساعد المجلس بما أعرفه."),
    L("lt_imp", "reveal", "هذا انطباعي عن سلمى، لا أكثر. لم أرَها تفعل شيئاً بالمخطوطة.", ["f_laith_impression"]),
    L("lt_nerv", "reveal", "هي مرتبكة دائماً حين تتكلم عن عملها، ولذلك أظن أنها تخفي خطأً ما.", None, ["cl_laith_nervous"]),
    L("lt_unknown", "deflect_unknown", "لا أعرف شيئاً محدداً عن هذا."),
    L("lt_off", "deflect_offtopic", "اسألني عما رأيته في المعرض."),
    L("lt_bye", "farewell", "أتمنى ألا يُظلم أحد.")])
ch("adel", "عادل المنصور", "witness", "حارس المساء في المتحف، يعمل من الأحد إلى الخميس",
   "مخلص ويحب الدقة، لكنه يرتب ذكرياته بحسب جولاته لا بحسب الأيام، فيخطئ في تعيين اليوم حين تتشابه الليالي.",
   ["أن تُقبل شهادته", "ألا يخطئ في شيء يخص المتحف"],
   [L("ad_greet", "greeting", "أنا أمرّ على الممرات كل مساء. ما رأيته أرويه."),
    L("ad_saw", "reveal", "رأيت امرأة بمعطف أبيض ورجلاً يتجهان إلى ممر المخزن قبيل جولتي الأولى، ولم أتحقق من هويتها.", ["f_guard_saw"]),
    L("ad_friday", "reveal", "ظننتها المرمّمة، وتذكرت أن ذلك كان ليلة الجمعة قرابة الحادية عشرة.", None, ["cl_adel_friday"]),
    L("ad_unknown", "deflect_unknown", "لا أذكر أكثر من هذا."),
    L("ad_off", "deflect_offtopic", "اسألني عن جولاتي في المساء."),
    L("ad_bye", "farewell", "إن أخطأت في اليوم فصحّحوني بالسجل.")])
ch("murad", "مراد الحداد", "suspect", "منسّق المرافق، في الخمسينات",
   "عملي ومتعجل، يعتمد على لوحاته وعلى ما اعتاد عليه، ويحمل سهواً لم ينتبه له. يتألم حين يتبيّن له أثر قراره، ولا يخفي إن واجهته بورقة مكتوبة.",
   ["ألا يُلام على عطل في ثلاثة أيام", "أن تعمل أجهزة المتحف دون إنذار"],
   [L("mu_greet", "greeting", "أنا المسؤول عن الأجهزة. اسأل عمّا يخص الصيانة."),
    L("mu_visit", "reveal", "جاء فني الصيانة معي مساء الخميس لفحص مزيل الرطوبة، وهذا من عملنا السنوي.", ["f_service_visit"]),
    L("mu_wo", "reveal", "أمر الصيانة صدر في نيسان منذ بداية الشهر، قبل أن يتحدث أحد عن منصب المدير.", ["f_work_order"]),
    L("mu_dash", "reveal", "لوحتي لم تُظهر إنذاراً، فاعتبرت أن الرطوبة بخير.", None, ["cl_murad_dash"]),
    L("mu_return", "reveal", "فهمت أن الفنية ستعود قريباً وتكمل الفحص وتعيد التوصيل، فلم أدوّن لنفسي مهمة.", None, ["cl_murad_return"]),
    L("mu_refuse", "refuse_secret", "لا أذكر أن شيئاً بقي معطلاً بعد انتهاء الزيارة."),
    L("mu_left", "reveal", "نعم... ورقة الفنية صريحة. أُبلغتُ شفهياً أن الجهاز ما زال مفصولاً، ولم أكتب مهمة إعادة التوصيل، فبقي كذلك إلى ظهر السبت.", ["f_unit_left_off"]),
    L("mu_unknown", "deflect_unknown", "لا أعرف."),
    L("mu_off", "deflect_offtopic", "اسألني عن الصيانة والأجهزة."),
    L("mu_bye", "farewell", "سأكتب كل تسليم من الآن فصاعداً.")])
ch("nabil", "د. نبيل السعدي", "expert", "خبير حفظ مستقل يستعين به المجلس",
   "هادئ ودقيق في ما يمكن قوله وما لا يمكن، ولا يحكم على أشخاص. يقدّم قراءة للوثائق ويذكر حدودها.",
   ["أن يُفهم كل سجل بدقته الزمنية وحدوده"],
   [L("nb_greet", "greeting", "أقرأ وثائق، ولا أحكم على أشخاص. اسأل عن السجلات."),
    L("nb_logger", "reveal", "في المخزن مقياس رقمي يسجّل كل ساعة ويصدّر ملفاً خاماً. والمتوسط اليومي يمحو الذروات، فاقرأ القراءات لا معدلها.", ["f_logger_exists"]),
    L("nb_paper", "reveal", "وفي غرفة الممر المجاورة مسجّل ميكانيكي قديم يرسم خطاً على ورق، وهي تشترك مع المخزن في قناة التهوية نفسها.", ["f_paper_exists"]),
    L("nb_unknown", "deflect_unknown", "هذا فوق ما تسمح به الوثائق."),
    L("nb_off", "deflect_offtopic", "اسألني عن السجلات والحفظ."),
    L("nb_bye", "farewell", "اذكر حدود كل سجل حين تستند إليه.")])

locations = [{"id": "loc_lab", "name_ar": "مختبر الترميم", "description_ar": "حيث عولجت المخطوطة ووُقّع تقرير الإنجاز."},
             {"id": "loc_store", "name_ar": "مخزن المخطوطات", "description_ar": "غرفة محكمة الإغلاق بمقياس رطوبة ومزيل رطوبة."},
             {"id": "loc_hall", "name_ar": "قاعة جلسات المجلس", "description_ar": "حيث تُعقد جلسات الاستماع العلنية."},
             {"id": "loc_corridor", "name_ar": "ممر المخزن", "description_ar": "الممر المؤدي إلى المخزن، فيه المسجّل الورقي."},
             {"id": "loc_facilities", "name_ar": "مكتب المرافق", "description_ar": "أوامر الصيانة وأوراق الخدمة."}]
objects = [{"id": "obj_ms", "name_ar": "مخطوطة «الأثر-17»", "description_ar": "طقم من أربع وعشرين ورقة رقية خيالية."},
           {"id": "obj_dehum", "name_ar": "مزيل رطوبة المخزن", "description_ar": "جهاز يحفظ رطوبة المخزن بين 45% و55%."}]
orgs = [{"id": "org_museum", "name_ar": "متحف الأثر", "description_ar": "متحف خيالي في مدينة «المرسى»."},
        {"id": "org_board", "name_ar": "مجلس الأمناء", "description_ar": "الجهة التي تعقد الجلسات وتقرر."}]

# ---------------------------------------------------------------- facts
facts = []
def F(id, st, kind, subj, spoiler, time=None, loc=None, ko=None):
    d = {"id": id, "statement_ar": st, "kind": kind, "subject_ids": subj, "spoiler_level": spoiler}
    if time: d["time"] = time
    if loc: d["location_id"] = loc
    if ko: d["science_ko_refs"] = ko
    facts.append(d)
F("f_damaged", "وُجدت على حواف أوراق من مخطوطة «الأثر-17» بقع عفن خفيفة وتموّج في الرق مساء السبت.", "event", ["obj_ms"], 0, T(3860), "loc_store")
F("f_dismissed", "فُصلت المرمّمة سلمى بعد بلاغ مجهول، ويعقد مجلس الأمناء ثلاث جلسات استماع علنية قبل أن يقرر.", "attribute", ["salma", "org_board"], 0)
F("f_anon_claim", "يقول البلاغ المجهول إن التلف نتج عن إهمال المرمّمة وتركها الطقم على طاولتها.", "attribute", ["salma"], 0)
F("f_vacancy", "أعلن المجلس قبل نحو اثني عشر يوماً من الحادثة شغور منصب المدير، ويتنافس عليه نائب المدير.", "attribute", ["maher", "org_board"], 0)
F("f_deputy_first", "نقل نائب المدير البلاغ إلى المجلس كما وصل، ويتكلم أولاً في الجلسات.", "attribute", ["maher"], 0)
F("f_report_signed", "وقّعت سلمى تقرير إنجاز الترميم الخميس 14:10 ووصفت الطقم بأنه مستقر بلا عفن.", "event", ["salma", "obj_ms"], 1, T(850), "loc_lab")
F("f_imaging_clean", "صوّرت محطة التصوير الآلية أوراق الطقم الخميس 14:20 ولم ترصد مناطق داكنة غير منتظمة على حوافها.", "event", ["obj_ms"], 1, T(860, "exact", 867), "loc_lab")
F("f_intake", "استلمت ريما الطقم في المخزن الخميس 14:38، وفحصته بصرياً فلم تجد بقعاً، وختمت صندوقه، وخرجت 14:44.", "event", ["rima", "obj_ms"], 1, T(878, "exact", 884), "loc_store")
F("f_ok_deposit", "كانت المخطوطة سليمة عند إيداعها في المخزن الخميس نحو 14:40، فلا تلف قبل هذه اللحظة.", "relation", ["obj_ms"], 3, T(878, "approx", 884), "loc_store", ["KO-RS-06-017", "KO-FC-04-026"])
F("f_door_exists", "يسجّل نظام بطاقات المخزن كل دخول وخروج.", "state", ["loc_store"], 1)
F("f_no_entry", "لم يدخل المخزن أحد بين الإيداع وفحص السبت سوى المنسّق والفنية معه مساء الخميس من 20:02 إلى 20:31.", "relation", ["loc_store", "rima"], 2, T(884, "exact", 3845), "loc_store", ["KO-RS-05-013"])
F("f_service_visit", "جاء فني الصيانة مع منسّق المرافق مساء الخميس لفحص مزيل الرطوبة، وفُصل الجهاز 20:05.", "event", ["murad", "obj_dehum"], 1, T(1202, "exact", 1231), "loc_store")
F("f_logger_exists", "يسجّل مقياس رقمي في المخزن الرطوبة كل ساعة ويصدّر منه ملف خام.", "state", ["loc_store"], 1)
F("f_dashboard_exists", "تعرض لوحة المرافق متوسطاً يومياً للرطوبة وتنذر عند متوسط يومي فوق 65%.", "state", ["org_museum"], 1)
F("f_paper_exists", "في ممر المخزن مسجّل ميكانيكي ورقي قديم يرسم الرطوبة أسبوعياً، وهواء الممر مشترك مع المخزن.", "state", ["loc_corridor"], 1, None, "loc_corridor")
F("f_peak", "بلغت الرطوبة في المخزن 82% فجر السبت 03:00، وبقيت فوق 65% نحو 16 ساعة موزعة على فجري الجمعة والسبت.", "event", ["loc_store"], 2, T(3120, "approx"), "loc_store", ["KO-RS-06-003"])
F("f_mean_below", "المتوسط اليومي المعروض في لوحة المرافق 62% للجمعة و64.5% للسبت، دون حد الإنذار.", "attribute", ["org_museum"], 1)
F("f_mean_hides", "المتوسط اليومي في اللوحة محسوب من القراءات الساعية نفسها، فلا يناقضها بل يطمس ذروتها الليلية.", "relation", ["org_museum", "loc_store"], 2, None, None, ["KO-RS-06-003", "KO-RS-06-004"])
F("f_excursion", "ارتفعت الرطوبة في المخزن إلى ما فوق حد الخطر 65% مدة طويلة من فجر الجمعة إلى السبت بعد فصل مزيل الرطوبة.", "relation", ["loc_store", "obj_dehum"], 3, T(1560, "approx", 3500), "loc_store", ["KO-RS-06-003", "KO-RS-05-004"])
F("f_unit_left_off", "بقي مزيل الرطوبة مفصولاً من الخميس 20:05 إلى السبت 16:10 لأن التسليم بين الفنية والمنسّق كان شفهياً ولم تُدوَّن مهمة إعادة التوصيل.", "event", ["murad", "obj_dehum"], 3, T(1205, "exact", 3850), "loc_store", ["KO-FC-04B-002"])
F("f_work_order", "صدر أمر الصيانة الوقائية للمزيل في 4 نيسان، قبل إعلان شغور المنصب، ومجدولاً لمساء الخميس 28 نيسان.", "state", ["obj_dehum", "murad"], 1)
F("f_planned", "فُصل المزيل لفحص سنوي مجدول بأمر صدر في 4 نيسان قبل إعلان شغور المنصب، لا لغرض آخر ولا بطلب من أحد.", "relation", ["obj_dehum"], 3, T(1205), "loc_store", ["KO-RS-05-004", "KO-RS-06-017"])
F("f_pattern", "نمط التلف (بقع متفرقة على الحواف الخارجية وتموّج عام بلا تمزق أو طيات) يوافق رطوبة عالية طويلة أكثر مما يوافق تلفاً بالتعامل.", "relation", ["obj_ms"], 2, None, None, ["KO-RS-06-001"])
F("f_maher_says", "يقول نائب المدير إن المرمّمة تركت الطقم على طاولتها وإن نمط التلف يدل على سوء المعالجة.", "attribute", ["maher"], 0)
F("f_laith_impression", "يرى ليث أن سلمى تبدو مرتبكة دائماً أثناء الكلام عن عملها.", "attribute", ["laith", "salma"], 0)
F("f_guard_saw", "رأى حارس المساء امرأة بمعطف أبيض ورجلاً يتجهان إلى ممر المخزن قبيل جولته الأولى، ولم يتحقق من هويتها.", "event", ["adel"], 1, T(1202, "approx"), "loc_corridor")

claims = [
    {"id": "cl_maher_bench", "statement_ar": "تركت المرمّمة الطقم على طاولتها نهاية الأسبوع فتلف بسبب إهمالها.", "kind": "half_truth", "held_by": ["maher"], "true_fact_id": "f_ok_deposit",
     "contradicted_by_evidence_ids": ["ev_intake_receipt", "ev_imaging_log", "ev_door_log"]},
    {"id": "cl_maher_handling", "statement_ar": "نمط التلف يدل على سوء معالجة وليس على الرطوبة.", "kind": "honest_mistake", "held_by": ["maher"], "true_fact_id": "f_pattern",
     "contradicted_by_evidence_ids": ["ev_expert_review", "ev_logger_raw"]},
    {"id": "cl_laith_nervous", "statement_ar": "المرمّمة مرتبكة دائماً، فلا بد أنها تخفي خطأً.", "kind": "rumour", "held_by": ["laith"], "true_fact_id": "f_ok_deposit",
     "contradicted_by_evidence_ids": ["ev_intake_receipt"]},
    {"id": "cl_adel_friday", "statement_ar": "رأيت المرمّمة تدخل ممر المخزن ليلة الجمعة قرابة الحادية عشرة.", "kind": "honest_mistake", "held_by": ["adel"], "true_fact_id": "f_service_visit",
     "contradicted_by_evidence_ids": ["ev_door_log", "ev_service_sheet"]},
    {"id": "cl_murad_dash", "statement_ar": "لوحة المرافق لم تُظهر إنذاراً فالرطوبة كانت بخير.", "kind": "honest_mistake", "held_by": ["murad"], "true_fact_id": "f_mean_hides",
     "contradicted_by_evidence_ids": ["ev_logger_raw", "ev_paper_trace"]},
    {"id": "cl_murad_return", "statement_ar": "ظننت أن الفنية ستعود وتعيد توصيل الجهاز، فلم أدوّن مهمة.", "kind": "honest_mistake", "held_by": ["murad"], "true_fact_id": "f_unit_left_off",
     "contradicted_by_evidence_ids": ["ev_service_sheet"]},
]
timeline = [
    {"id": "te_report", "description_ar": "سلمى توقّع تقرير إنجاز الترميم.", "time": T(850), "location_id": "loc_lab", "actor_ids": ["salma"], "fact_ids": ["f_report_signed"], "motivated_by_ar": "انتهت من المعالجة وأرادت تسليم الطقم"},
    {"id": "te_imaging", "description_ar": "محطة التصوير تفحص الأوراق وتحفظ الصور.", "time": T(860, "exact", 867), "location_id": "loc_lab", "actor_ids": [], "fact_ids": ["f_imaging_clean"]},
    {"id": "te_deposit", "description_ar": "ريما تستلم الطقم وتختم صندوقه في المخزن.", "time": T(878, "exact", 884), "location_id": "loc_store", "actor_ids": ["rima"], "fact_ids": ["f_intake"], "motivated_by_ar": "إجراء الاستلام المعتاد بعد الترميم"},
    {"id": "te_service", "description_ar": "الفنية والمنسّق في المخزن، ويُفصل المزيل 20:05.", "time": T(1202, "exact", 1231), "location_id": "loc_store", "actor_ids": ["murad"], "fact_ids": ["f_service_visit"], "motivated_by_ar": "تنفيذ الصيانة السنوية المجدولة"},
    {"id": "te_guard", "description_ar": "الحارس يرى زائرين يتجهان إلى ممر المخزن.", "time": T(1202, "approx"), "location_id": "loc_corridor", "actor_ids": ["adel"], "fact_ids": ["f_guard_saw"], "motivated_by_ar": "جولته المسائية المعتادة"},
    {"id": "te_peak", "description_ar": "الرطوبة تبلغ ذروتها في المخزن فجر السبت.", "time": T(3120, "approx"), "location_id": "loc_store", "actor_ids": [], "fact_ids": ["f_peak"]},
    {"id": "te_restart", "description_ar": "المنسّق يعيد توصيل المزيل بعد استدعاء ريما، وريما تفتح الصندوق وتدوّن الضرر.", "time": T(3845, "exact", 3860), "location_id": "loc_store", "actor_ids": ["murad", "rima"], "fact_ids": ["f_damaged", "f_unit_left_off"], "motivated_by_ar": "فحص ما بعد الصيانة المعتاد"},
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
V("ev_restoration_report", "تقرير إنجاز الترميم الموقّع", "documentary",
  "متحف الأثر — قسم الترميم\nتقرير إنجاز ترميم المخطوطة «الأثر-17» (طقم من 24 ورقة)\nالتاريخ: الخميس 28 نيسان — 14:10\nالحالة عند الانتهاء: الرق مستقر، لا بقع نشطة ولا عفن ظاهر ولا تموّج. رطوبة غرفة الترميم 47%.\nالتوصية: يُحفظ بين 45% و55% رطوبة.\nالتوقيع: سلمى العمري، مرمّمة أولى",
  ["a_read_report"], ["f_report_signed"], "moderate",
  "كتبته المرمّمة نفسها، فهي صاحبة مصلحة في وصفه. وهو يصف الطقم في غرفة الترميم لحظة التوقيع، لا حاله في المخزن بعد ذلك؛ وقيمته كبيرة حين يوافقه سجل كتبه شخص آخر.", loc="loc_lab")
V("ev_anon_report", "البلاغ المجهول", "documentary",
  "بلاغ عبر نموذج المتحف الإلكتروني (دون اسم)\nالوقت: الأحد 05:12\nالنص: «المرمّمة أهملت الطقم وتركته على طاولتها نهاية الأسبوع فأتلفته. يجب فصلها فوراً.»",
  ["a_read_anon"], ["f_anon_claim"], "weak",
  "مصدره مجهول ولا يذكر شاهداً أو سجلاً؛ والتشابه بين عبارته وعبارة بعض المتكلمين لا يثبت من كتبه. هو ادعاء يحتاج تأييداً لا دليلاً.", red=True, loc="loc_hall")
V("ev_damage_record", "سجل الحالة بعد الصيانة", "documentary",
  "سجل حالة — السبت 16:20 — أعدّته: ريما الخطيب\nالطقم «الأثر-17» في صندوقه، والختم 2 سليم كما وُضع الخميس.\nعند الفتح: بقع عفن خفيفة على حواف 9 أوراق خارجية، وتموّج عام في الرق، ولا تمزق ولا طيات.\nالإجراء: عُزل الطقم وطُلب الفحص. أُعيد تشغيل مزيل الرطوبة 16:10.",
  ["a_read_damage"], ["f_damaged"], "strong",
  "يصف الضرر وقت اكتشافه، لا وقت حدوثه ولا سببه.", loc="loc_store")
V("ev_intake_receipt", "نموذج استلام المخزن", "documentary",
  "نموذج استلام المخزن رقم 311\nالمادة: طقم «الأثر-17» (24 ورقة) في صندوق محايد\nالتسليم من: قسم الترميم\nالاستلام: ريما الخطيب، مسجّلة المجموعات — الخميس 14:38\nالفحص البصري عند الاستلام: لا بقع ولا تموّج على الأوراق الخارجية. الصندوق مختوم بالختم 2.\nشاشة المخزن: رطوبة 48%.\nالتوقيع: ريما الخطيب",
  ["a_get_intake"], ["f_intake"], "strong",
  "فحص بصري سريع للأوراق الخارجية لا للداخلية كلها، وهو يثبت الحال لحظة الإيداع فقط. كاتبته شخص غير المرمّمة.", loc="loc_store")
V("ev_imaging_log", "سجل محطة التصوير الآلية", "digital",
  "سجل محطة التصوير — الخميس\nالمهمة IMG-0428: «الأثر-17» الأوراق 1–24\nبدء التصوير: 14:20:11 — الانتهاء: 14:27:50\nفحص آلي لحواف الأوراق: لا مناطق داكنة غير منتظمة (عتبة التنبيه 3%)\nالخاتم الزمني: من خادم المتحف\nالمنفِّذ: حساب المحطة (تلقائي)",
  ["a_get_imaging"], ["f_imaging_clean"], "strong",
  "الفحص الآلي يلتقط المناطق الداكنة الكبيرة فقط ولا يكشف عفناً مبكراً أو تموجاً خفيفاً. ويسبق الإيداع بنحو إحدى عشرة دقيقة.", loc="loc_lab")
V("ev_door_log", "سجل بطاقات المخزن", "digital",
  "سجل نظام الدخول — مخزن المخطوطات\nالخميس 14:38 دخول: ريما الخطيب — 14:44 خروج\nالخميس 20:02 دخول: بطاقة م. الحداد (معه مرافق واحد دون بطاقة) — 20:31 خروج\nالجمعة: لا قيود\nالسبت 16:05 دخول: ريما الخطيب — 16:40 خروج\nالسبت 16:08 دخول: م. الحداد — 16:20 خروج\nملاحظة النظام: بطاقة سلمى العمري غير مخوّلة للمخزن، وبطاقة ماهر الشامي لم تُستعمل في المخزن في هذه الفترة.",
  ["a_get_door"], ["f_no_entry", "f_service_visit"], "strong",
  "يسجّل مرور البطاقات لا ما جرى داخل الغرفة، ويسمح بمرافق واحد دون بطاقة فلا يسمّيه.", contradicts=["cl_adel_friday"], loc="loc_store")
V("ev_logger_raw", "تصدير مقياس الرطوبة الخام", "digital",
  "تصدير مقياس رطوبة المخزن (قراءة كل ساعة؛ المعروض عينة كل 3 ساعات من الملف الكامل)\nحدود الحفظ المعتمدة في الإعدادات: الهدف 45–55%، الخطر فوق 65%\nالخميس 19:00 — 47% | 22:00 — 55%\nالجمعة 00:00 — 60% | 03:00 — 78% | 06:00 — 80% | 09:00 — 62% | 12:00 — 50% | 15:00 — 48% | 18:00 — 52% | 21:00 — 62%\nالسبت 00:00 — 70% | 03:00 — 82% | 06:00 — 79% | 09:00 — 60% | 12:00 — 49% | 15:00 — 47%\nملخص التصدير: أعلى قراءة 82% (السبت 03:00) · عدد الساعات فوق 65%: 16",
  ["a_get_logger"], ["f_peak"], "strong",
  "يقيس هواء نقطة واحدة في المخزن لا الورق نفسه، ولا يبيّن سبب الارتفاع. والعينة المعروضة كل ثلاث ساعات، أما الملخص فمن الملف الكامل.", contradicts=["cl_murad_dash"], ko="KO-RS-06-003", loc="loc_store")
V("ev_dashboard", "لوحة مراقبة المرافق", "digital",
  "لوحة مراقبة المرافق — مخزن المخطوطات\nالمتوسط اليومي للرطوبة: الخميس 49% · الجمعة 62% · السبت (حتى 16:00) 64.5%\nحد الإنذار: متوسط يومي فوق 65%\nحالة الإنذار: لا إنذار\nمفتاح اللوحة: المتوسط اليومي = مجموع قراءات مقياس المخزن الساعية ÷ عددها",
  ["a_get_dashboard"], ["f_mean_below"], "strong",
  "تعرض متوسطاً لا القراءات نفسها؛ والمتوسط لا يبيّن أعلى قراءة ولا مدة بقاء الرطوبة مرتفعة. حدّ إنذارها وُضع لراحة التشغيل لا لحفظ المخطوطات.", red=True, loc="loc_facilities")
V("ev_paper_trace", "ورقة المسجّل الميكانيكي", "physical",
  "المسجّل الورقي الميكانيكي — ممر المخزن (أسبوع الأحد–السبت). قراءة الخط بالمسطرة (±3%):\nخط شبه ثابت بين 46% و50% حتى مساء الخميس.\nقمة نحو 79% فجر الجمعة. قمة نحو 81% فجر السبت. هبوط حاد بعد ظهر السبت.\nملاحظة بخط اليد على الورقة: «الممر يشترك مع المخزن في قناة التهوية».",
  ["a_get_paper"], ["f_peak"], "moderate",
  "يقيس هواء الممر المجاور لا المخزن، بقراءة بصرية تقريبية؛ يدل على اتجاه الارتفاع وتوقيته لا على رقم دقيق. ميزته أنه جهاز ميكانيكي لا يعتمد على المقياس الرقمي.", contradicts=["cl_murad_dash"], loc="loc_corridor")
V("ev_service_sheet", "ورقة خدمة الصيانة", "documentary",
  "إدارة المرافق — ورقة خدمة WO-3302\nالموقع: مخزن المخطوطات — مزيل الرطوبة\nالعمل: فحص الضاغط (صيانة سنوية مجدولة، بموجب أمر صدر في 4 نيسان)\nالفنية: نهى الحسن\n20:02 دخول بصحبة المنسّق\n20:05 عزل الجهاز كهربائياً لبدء الفحص\n20:28 انتهت المدة المخصصة دون إتمام الفحص؛ الجهاز سليم لكنه ما زال معزولاً ويلزم إعادة توصيله\nلا توجد في هذه الورقة مهمة محددة لإعادة التوصيل\n20:31 خروج؛ أُبلغ المنسّق شفهياً\nالتوقيع: ن. الحسن",
  ["a_get_service"], ["f_service_visit", "f_planned"], "strong",
  "تثبت ما كتبته الفنية وما أبلغته، لا ما فهمه المنسّق، ولا متى أُعيد التشغيل.", contradicts=["cl_adel_friday", "cl_murad_return"], loc="loc_facilities")
V("ev_work_order", "أمر الصيانة الوقائية", "documentary",
  "أمر صيانة وقائية WO-3302\nتاريخ الإصدار: 4 نيسان\nالموضوع: فحص سنوي لضاغط مزيل الرطوبة — مخزن المخطوطات\nموعد التنفيذ: الخميس 28 نيسان، 20:00\nالجهة: إدارة المرافق (جدول الصيانة السنوي)\nالاعتماد: م. الحداد",
  ["a_get_workorder"], ["f_work_order", "f_planned"], "strong",
  "يثبت أن الصيانة كانت مجدولة سلفاً، لا ما جرى عند تنفيذها ولا أنها نُفذت كما خُطط.", loc="loc_facilities")
V("ev_expert_review", "رأي خبير الحفظ المكتوب", "lab_result",
  "رأي خبير الحفظ المستقل د. نبيل السعدي (مكتوب)\nاطّلع على: سجل الحالة بعد الصيانة، وصور محطة التصوير، والتصدير الخام لمقياس الرطوبة.\nالملاحظة: البقع متفرقة على الحواف الخارجية لأوراق الطقم، والتموّج عام لا موضعي، ولم يُسجَّل تمزق ولا طيات ولا بصمات.\nالتقدير: نمط يوافق تعرضاً طويلاً لرطوبة عالية أكثر مما يوافق تلفاً بالتعامل.\nالحدود: رأي على وثائق لا على فحص المخطوطة، ولا يحدد اللحظة التي بدأ فيها الضرر.",
  ["a_request_expert"], ["f_pattern"], "moderate",
  "قراءة خبير لصور ووثائق، تعتمد على صحة تلك الوثائق، وهي رأي لا قياس. لم يفحص المخطوطة نفسها.", contradicts=["cl_maher_handling"], ko="KO-FC-04-031", loc="loc_hall")
V("ev_maher_statement", "إفادة ماهر الشامي (ملخص)", "testimonial",
  "ملخص إفادة ماهر الشامي، نائب المدير (الجلسة الأولى):\n«رفعت البلاغ للمجلس كما وصلني. المرمّمة تركت الطقم على طاولتها نهاية الأسبوع، ونمط التلف يدل على سوء المعالجة. ولوحة المرافق لم تُظهر مشكلة رطوبة.»",
  ["a_note_maher"], ["f_maher_says"], "weak",
  "إفادة من صاحب مصلحة معلنة في المنصب، تعيد ما في البلاغ وتستند إلى لوحة لم يتحقق من معنى أرقامها. قوة العرض لا تُعوّض غياب السجل.", red=True, loc="loc_hall")
V("ev_laith_statement", "إفادة ليث الحلبي (ملخص)", "testimonial",
  "ملخص إفادة ليث الحلبي، مساعد أمين المعرض (الجلسة الثانية):\n«سلمى مرتبكة دائماً حين تتكلم عن عملها، وأظن أنها تخفي خطأً ما. لم أرَها تلمس المخطوطة.»",
  ["a_note_laith"], ["f_laith_impression"], "weak",
  "انطباع شخصي عن طبع إنسان لا واقعة قابلة للفحص، ولا يخبر بما جرى للمخطوطة.", red=True, loc="loc_hall")
V("ev_adel_statement", "إفادة عادل المنصور (ملخص)", "testimonial",
  "ملخص إفادة عادل المنصور، حارس المساء (الجلسة الثالثة):\nالإفادة الأولى: «رأيت ليلة الجمعة قرابة الحادية عشرة امرأة بمعطف أبيض تدخل ممر المخزن، وظننتها المرمّمة.»\nالإفادة الثانية: «كان ذلك قبل جولتي التي أبدأها عند التاسعة. وأنا لا أعمل يوم الجمعة مساءً.»",
  ["a_note_adel"], ["f_guard_saw"], "weak",
  "تناقض داخلي في التوقيت واختلاط في هوية من رآه؛ وتُقاس بسجل البطاقات وبورقة الخدمة لا بثقة صاحبها.", red=True, loc="loc_corridor")
V("ev_murad_statement", "إفادة مراد الحداد (ملخص)", "testimonial",
  "ملخص إفادة مراد الحداد، منسّق المرافق:\n«فصلت الفنية الجهاز مساء الخميس للفحص، وأبلغتني أن العمل لم يكتمل. ظننت أنها ستعود وتعيد التوصيل ولم أكتب مهمة. لم أعد إلى المخزن حتى استدعتني ريما السبت، فأعدت التشغيل 16:10.»",
  ["a_note_murad"], ["f_unit_left_off"], "moderate",
  "إفادة اعتراف بسهو دون قصد، وتتفق مع ورقة الفنية؛ والاعتراف وحده لا يكفي ما لم يؤيده سجل مكتوب.", loc="loc_facilities")

# ---------------------------------------------------------------- inferences
def P(t, i): return {"ref_type": t, "ref_id": i}
inf = []
def I(id, prem, ct, concl, rel, strength, rule, ks):
    inf.append({"id": id, "premises": prem, "conclusion": {"ref_type": ct, "ref_id": concl}, "relation": rel, "strength": strength, "rule_ar": rule, "skill_ko_refs": ks})
E = lambda x: P("evidence", x)
Fa = lambda x: P("fact", x)
# --- key fact 1: sound at deposit (two independent chains)
I("i_ok_a", [E("ev_restoration_report"), E("ev_intake_receipt")], "fact", "f_ok_deposit", "establishes", "strong",
  "تقرير المرمّمة الموقّع 14:10 ونموذج الاستلام الذي كتبته ريما 14:38 صادران من شخصين مختلفين، ويصفان الحال نفسها: أوراق مستقرة بلا بقع؛ فهي سليمة عند الإيداع.", ["KO-RS-05-004", "KO-RS-06-017"])
I("i_ok_b", [E("ev_imaging_log"), E("ev_door_log")], "fact", "f_ok_deposit", "establishes", "strong",
  "محطة التصوير الآلية 14:20–14:27 لا ترصد مناطق داكنة، وسجل البطاقات يضع الإيداع 14:38، أي بعد إحدى عشرة دقيقة؛ فلا فرصة لتلف بين التصوير والإيداع. المصدران آلان ولا يعتمدان على أحد.", ["KO-RS-05-004", "KO-FC-04-026"])
# --- key fact 2: long humidity excursion (two independent chains)
I("i_exc_a", [E("ev_logger_raw"), E("ev_dashboard")], "fact", "f_excursion", "establishes", "strong",
  "اللوحة تعرض متوسط القراءات الساعية نفسها كما يقول مفتاحها؛ فالمتوسط 62% لا يناقض القراءة 80% بل يطمسها. والمقياس الخام يبيّن ست عشرة ساعة فوق حد الخطر.", ["KO-RS-06-003", "KO-RS-06-004"])
I("i_exc_b", [E("ev_service_sheet"), E("ev_paper_trace")], "fact", "f_excursion", "establishes", "strong",
  "ورقة الخدمة تقول إن الجهاز عُزل 20:05 ولم يُعد توصيله، والمسجّل الميكانيكي المستقل في الممر يرسم قمتين فجر الجمعة والسبت؛ فهبوط المزيل أعقبته رطوبة عالية رصدها جهازان بآليتين مختلفتين.", ["KO-RS-05-004", "KO-RS-06-003"])
I("i_plan_a", [E("ev_work_order")], "fact", "f_planned", "establishes", "strong",
  "أمر الصيانة WO-3302 مؤرخ 4 نيسان وموعد تنفيذه الخميس 28 نيسان، وإعلان الشغور جاء بعده بنحو ثلاثة أسابيع؛ فالفصل جزء من جدول سنوي سابق للمنافسة.", ["KO-RS-06-017"])
I("i_plan_b", [E("ev_service_sheet")], "fact", "f_planned", "establishes", "strong",
  "ورقة الفنية تنص على أن العمل صيانة سنوية بموجب أمر 4 نيسان، وتوقيعها وتوقيتها من كتابتها لا من كتابة أحد غيرها؛ فالمصدر مستقل عن أمر الجدولة.", ["KO-RS-05-004"])
I("i_mean", [E("ev_logger_raw"), E("ev_dashboard")], "fact", "f_mean_hides", "establishes", "strong",
  "حين تُعاد القراءات الثلاث المعروضة لليوم الجمعة إلى متوسطها يخرج رقم اللوحة؛ فالمصدران صحيحان ويختلفان في دقة العرض لا في الحقيقة.", ["KO-RS-06-004"])
# --- supporting facts and claims
I("i_noentry", [E("ev_door_log")], "fact", "f_no_entry", "establishes", "strong",
  "سجل البطاقات لا يضع في المخزن بين الإيداع والسبت إلا المنسّق ومرافقه ليلة الخميس؛ وبطاقة المرمّمة غير مخوّلة أصلاً.", ["KO-RS-05-013"])
I("i_pattern", [E("ev_expert_review"), E("ev_logger_raw")], "fact", "f_pattern", "establishes", "suggestive",
  "الخبير يقرأ نمط التلف من الصور والتصدير الخام، والتصدير يؤيد وجود الظرف الذي يفسره؛ والرأي يبقى مقيَّداً بحدوده.", ["KO-FC-04-031", "KO-RS-06-001"])
I("i_left_off", [E("ev_service_sheet"), E("ev_murad_statement")], "fact", "f_unit_left_off", "establishes", "strong",
  "الورقة المكتوبة تقول إن الجهاز ما زال معزولاً وإن التسليم شفهي، وإفادة المنسّق تؤيدها دون أن تكون هي الأساس؛ فبقاء الجهاز مفصولاً سببه فجوة التسليم.", ["KO-RS-05-009", "KO-FC-04B-002"])
I("i_cl_bench", [Fa("f_ok_deposit"), Fa("f_no_entry")], "claim", "cl_maher_bench", "contradicts_claim", "strong",
  "الطقم غادر طاولة المرمّمة إلى المخزن مختوماً الخميس، ولم يدخله بعدها من يمسّه؛ فقول النائب إنه بقي على الطاولة نهاية الأسبوع لا يوافق السجلات.", ["KO-RS-05-014"])
I("i_cl_handling", [Fa("f_pattern"), Fa("f_excursion")], "claim", "cl_maher_handling", "contradicts_claim", "strong",
  "الخبير يقرأ النمط على أنه رطوبة، والمقياس يثبت أن الرطوبة ارتفعت فعلاً؛ فادعاء سوء المعالجة لا يفسر ما يفسره ارتفاع الرطوبة.", ["KO-RS-06-001"])
I("i_cl_nervous", [Fa("f_ok_deposit"), Fa("f_excursion")], "claim", "cl_laith_nervous", "contradicts_claim", "strong",
  "طريقة كلام الشخص لا تقول شيئاً عن سبب تلف الورق، والسجلات تثبت سلامة الطقم عند الإيداع وارتفاع رطوبة المخزن بعده؛ فلا حاجة إلى تفسير يخص طبع المرمّمة.", ["KO-RS-05-007"])
I("i_cl_adel", [E("ev_door_log"), E("ev_service_sheet")], "claim", "cl_adel_friday", "contradicts_claim", "strong",
  "السجل لا يضع أحداً في المخزن يوم الجمعة، والزيارة الوحيدة كانت الخميس 20:02 للفنية والمنسّق؛ فالمرأة بمعطف أبيض فنية الصيانة، والحارس أخطأ في اليوم وفي الهوية بحسن نية.", ["KO-RS-05-008", "KO-RS-06-017"])
I("i_cl_dash", [Fa("f_mean_hides"), Fa("f_excursion")], "claim", "cl_murad_dash", "contradicts_claim", "strong",
  "غياب الإنذار يعني أن المتوسط لم يتجاوز الحد، لا أن كل ساعة كانت سليمة؛ والقراءات الساعية تتجاوز الحد.", ["KO-RS-06-003"])
I("i_cl_return", [E("ev_service_sheet")], "claim", "cl_murad_return", "contradicts_claim", "strong",
  "الورقة لا تذكر عودة مقررة ولا مهمة لإعادة التوصيل؛ فافتراض المنسّق لم يكن مدوّناً في أي مكان.", ["KO-RS-05-014"])
# --- hypotheses
I("i_support_unit", [Fa("f_ok_deposit"), Fa("f_excursion"), Fa("f_planned")], "hypothesis", "h_unit", "supports", "strong",
  "سلامة الطقم عند الإيداع ثم ارتفاع رطوبة المخزن بعد عزل المزيل؛ سلسلة تفسر ظهور البقع والتموّج بلا افتراض مخالف، أما من تسبب في بقاء المزيل معزولاً فتجيب عنه ورقة الخدمة.", ["KO-RS-06-007"])
I("i_rule_restorer", [Fa("f_ok_deposit"), Fa("f_excursion")], "hypothesis", "h_restorer", "rules_out", "conclusive",
  "إن كانت الأوراق سليمة عند الإيداع المختوم، ثم ارتفعت رطوبة المخزن بعده ارتفاعاً طويلاً موثقاً، فالتفسير الكافي للتلف لاحق للإيداع ولا يحتاج إلى معالجة خاطئة قبله.", ["KO-RS-06-008"])
I("i_rule_restorer_2", [Fa("f_pattern"), Fa("f_excursion")], "hypothesis", "h_restorer", "rules_out", "strong",
  "النمط الذي يوافق الرطوبة الطويلة ثبتت له علة قياسية في المخزن؛ فلا حاجة إلى معالجة خاطئة لتفسيره.", ["KO-RS-06-008"])
I("i_rule_sabotage", [Fa("f_planned"), Fa("f_excursion")], "hypothesis", "h_sabotage", "rules_out", "strong",
  "عزل الجهاز كان جزءاً من جدول صيانة سابق لإعلان الشغور، والرطوبة العالية تفسّرها بقاء الجهاز معزولاً؛ فالمصلحة المعلنة لصاحب المنصب لا تكفي لإثبات فعل، ولا يوجد أثر لفعل.", ["KO-RS-05-007", "KO-RS-06-008"])
I("i_rule_sabotage_2", [Fa("f_no_entry")], "hypothesis", "h_sabotage", "rules_out", "suggestive",
  "سجل البطاقات لا يضع نائب المدير في المخزن بين الإيداع والسبت؛ وغياب أثر دخول يضعف أي قصة فعل مباشر دون أن يغني عن بقية السجلات.", ["KO-RS-05-013"])
I("i_rule_nodata", [Fa("f_ok_deposit"), Fa("f_excursion")], "hypothesis", "h_nodata", "rules_out", "strong",
  "مساران مستقلان يتفقان على أن الطقم سليم عند الإيداع، ومساران مستقلان يتفقان على أن الرطوبة ارتفعت بعده؛ فالسجلات تتسق في صورة واحدة ولا تبرر القول إن السبب مجهول.", ["KO-RS-06-008", "KO-RS-05-004"])
I("i_rule_nodata_2", [Fa("f_mean_hides"), E("ev_paper_trace")], "hypothesis", "h_nodata", "rules_out", "strong",
  "التعارض بين اللوحة والمقياس يزول بمعرفة أن اللوحة تتوسط القراءات، ويؤيد الورق الميكانيكي المستقل القمم نفسها؛ فالسجلات تتسق ولا يلزم اعتبارها كلها باطلة.", ["KO-RS-06-008", "KO-RS-06-003"])

# ---------------------------------------------------------------- character knowledge
K = lambda f, a="witnessed", c="certain": {"fact_id": f, "access": a, "certainty": c}
ck = [
    {"character_id": "maher", "knows": [K("f_dashboard_exists", "common_knowledge"), K("f_maher_says", "inferred", "fairly_sure")], "hides": [], "believes": [{"claim_id": "cl_maher_bench", "stance": "sincere"}, {"claim_id": "cl_maher_handling", "stance": "sincere"}]},
    {"character_id": "salma", "knows": [K("f_report_signed"), K("f_imaging_clean", "witnessed", "fairly_sure")], "hides": [], "believes": []},
    {"character_id": "rima", "knows": [K("f_intake"), K("f_door_exists", "professional")], "hides": [], "believes": []},
    {"character_id": "laith", "knows": [K("f_laith_impression", "inferred", "fairly_sure")], "hides": [], "believes": [{"claim_id": "cl_laith_nervous", "stance": "sincere"}]},
    {"character_id": "adel", "knows": [K("f_guard_saw", "witnessed", "unsure")], "hides": [], "believes": [{"claim_id": "cl_adel_friday", "stance": "sincere"}]},
    {"character_id": "murad", "knows": [K("f_service_visit"), K("f_work_order")],
     "hides": [{"fact_id": "f_unit_left_off", "reveal_when": {"presented": {"evidence_id": "ev_service_sheet", "to_character": "murad"}}, "cover_claim_id": None, "reveal_line_id": "mu_left"}],
     "believes": [{"claim_id": "cl_murad_dash", "stance": "sincere"}, {"claim_id": "cl_murad_return", "stance": "sincere"}]},
    {"character_id": "nabil", "knows": [K("f_logger_exists", "professional"), K("f_paper_exists", "professional")], "hides": [], "believes": []},
]
hyps = [
    {"id": "h_restorer", "statement_ar": "تلفت المخطوطة بسبب سوء معالجة المرمّمة أو إهمالها قبل إيداعها.", "is_true": False, "plausibility_at_start": "high", "suspect_id": "salma"},
    {"id": "h_sabotage", "statement_ar": "أتلف نائب المدير المخطوطة عمداً ليُزاح غيره عن المنافسة على المنصب.", "is_true": False, "plausibility_at_start": "medium", "suspect_id": "maher"},
    {"id": "h_unit", "statement_ar": "تلفت المخطوطة بسبب ارتفاع رطوبة المخزن بعد أن بقي مزيل الرطوبة مفصولاً إثر صيانة مجدولة، دون قصد من أحد.", "is_true": True, "plausibility_at_start": "low", "suspect_id": "murad"},
    {"id": "h_nodata", "statement_ar": "سجلات الرطوبة متضاربة فلا يمكن معرفة سبب التلف أصلاً.", "is_true": False, "plausibility_at_start": "medium"},
]
mis = [
    {"id": "rh_dashboard", "points_to_hypothesis_id": "h_restorer", "planted_via_ar": "لوحة المرافق تقول إن الرطوبة لم تتجاوز حد الإنذار، فيبدو أن الرطوبة ليست السبب.", "evidence_ids": ["ev_dashboard"],
     "refuted_by_inference_ids": ["i_exc_a", "i_mean", "i_cl_dash", "i_rule_restorer_2"],
     "fairness_note_ar": "مفتاح اللوحة في الدليل نفسه يقول إن الرقم متوسط القراءات الساعية، والتصدير الخام بين يدي اللاعب يبيّن القراءات؛ فالتعارض ظاهري ويُحل بالقراءة لا بتخمين."},
    {"id": "rh_nervous", "points_to_hypothesis_id": "h_restorer", "planted_via_ar": "ليث يصف سلمى بأنها مرتبكة دائماً ويستنتج أنها تخفي خطأً.", "evidence_ids": ["ev_laith_statement"],
     "refuted_by_inference_ids": ["i_rule_restorer", "i_cl_nervous"],
     "fairness_note_ar": "الإفادة تصف انطباعاً لا واقعة، وتقيس السجلات المكتوبة سلامة الطقم عند الإيداع؛ ولا يحتاج اللاعب إلى قراءة طبع أحد."},
    {"id": "rh_guard", "points_to_hypothesis_id": "h_restorer", "planted_via_ar": "الحارس يقول إنه رأى المرمّمة تدخل ممر المخزن ليلة الجمعة.", "evidence_ids": ["ev_adel_statement"],
     "refuted_by_inference_ids": ["i_cl_adel", "i_rule_restorer"],
     "fairness_note_ar": "الإفادة تناقض نفسها في اليوم والوقت، وسجل البطاقات وورقة الخدمة متاحان ويضعان زائرين آخرين في يوم آخر."},
    {"id": "rh_motive", "points_to_hypothesis_id": "h_sabotage", "planted_via_ar": "نائب المدير يتنافس على المنصب ويتكلم أولاً ويرفع البلاغ، فيبدو أن له مصلحة في الإتلاف.", "evidence_ids": ["ev_maher_statement", "ev_anon_report"],
     "refuted_by_inference_ids": ["i_rule_sabotage", "i_rule_sabotage_2", "i_plan_a", "i_plan_b"],
     "fairness_note_ar": "أمر الصيانة مؤرخ قبل الشغور، وسجل البطاقات لا يضع النائب في المخزن؛ والمصلحة وحدها لا تثبت فعلاً ولا تنفيه، والنتيجة تُبنى على السجلات."},
]
los = [
    {"id": "lo_claim", "statement_ar": "يفرّق بين قوة الحجة وقوة الدليل، ويصنّف المصادر قبل أن يقيس القول بالسجل.", "skill_ko_ref": "KO-RS-06-018", "observable_behaviors_ar": ["يصنّف الإفادات أقوالاً", "لا يقبل حجة قوية العرض بلا سند"], "evidence_sources": ["evidence_board"]},
    {"id": "lo_indep", "statement_ar": "يتحقق من استقلال الأدلة ولا يعدّ سجلين من عملية واحدة مصدرين.", "skill_ko_ref": "KO-RS-05-004", "observable_behaviors_ar": ["يقدّم مسارين لا يشتركان في مصدر"], "evidence_sources": ["evidence_board", "final_justification"]},
    {"id": "lo_timeline", "statement_ar": "يرتّب الأحداث على خط زمني ليكشف التعارض.", "skill_ko_ref": "KO-RS-06-017", "observable_behaviors_ar": ["يضع الأدلة في أزمنتها"], "evidence_sources": ["timeline_task", "action_log"]},
    {"id": "lo_hyp", "statement_ar": "يوازن بين فرضيات متعددة ويستبعد ما تنقضه الأدلة، ويصوغ الحجة المضادة لأقوى فرضية خاطئة.", "skill_ko_ref": "KO-RS-06-019", "observable_behaviors_ar": ["يضيف فرضيات", "يستبعد بدليل"], "evidence_sources": ["hypothesis_ledger"]},
    {"id": "lo_diag", "statement_ar": "يقدّر ما يثبته كل سجل وما لا يثبته، ويرفض شهادة المظهر.", "skill_ko_ref": "KO-RS-05-007", "observable_behaviors_ar": ["يربط الدليل بالفرضية باتجاه صحيح", "لا يستند إلى الارتباك دليلاً"], "evidence_sources": ["evidence_board", "final_justification"]},
    {"id": "lo_calib", "statement_ar": "يصوغ نسبة الترجيح بحدودها.", "skill_ko_ref": "KO-RS-06-021", "observable_behaviors_ar": ["يختار ثقة معقولة", "يذكر حدوداً"], "evidence_sources": ["final_justification"]},
    {"id": "lo_revise", "statement_ar": "يراجع رأيه الأول حين يظهر ما يخالفه.", "skill_ko_ref": "KO-RS-06-009", "observable_behaviors_ar": ["يغيّر فرضيته الرائدة بدليل"], "evidence_sources": ["hypothesis_ledger"]},
]
def levels(d): return [{"score": i, "descriptor_ar": t} for i, t in enumerate(d)]
rub = {
    "reference_answer_ar": "لم تتلف المخطوطة بسبب المرمّمة. كانت سليمة عند الإيداع المختوم الخميس 14:38 بشهادة وثيقتين من كاتبين مختلفين وسجلين آليين، ولم يدخل المخزن بعدها إلا المنسّق وفنية الصيانة ليلة الخميس. ثم عُزل مزيل الرطوبة 20:05 لصيانة مجدولة قبل شغور المنصب، ولم يُعد توصيله لأن التسليم كان شفهياً، فارتفعت الرطوبة إلى 82% وبقيت فوق حد الخطر نحو ست عشرة ساعة. ولوحة المرافق لا تناقض ذلك، فمتوسطها اليومي يطمس الذروة. حدود الاستنتاج: لا نعرف من كتب البلاغ المجهول، ولا لحظة بدء الضرر بالدقيقة، ولم يُفحص الورق نفسه.",
    "criteria": [
        {"id": "c_source", "name_ar": "تصنيف المصادر", "objective_ids": ["lo_claim"], "scored_by": "deterministic", "weight": 0.15, "levels": levels(["لم يصنّف", "أخطأ في الأغلب", "نصف صحيح", "معظمه صحيح", "كله صحيح"])},
        {"id": "c_conflict", "name_ar": "ترتيب الأحداث وكشف التعارض", "objective_ids": ["lo_timeline"], "scored_by": "deterministic", "weight": 0.15, "levels": levels(["لم يضع شيئاً", "وضع قليلاً", "وضع نصفها صحيحاً", "معظمها", "كلها في موضعها"])},
        {"id": "c_links", "name_ar": "ربط الأدلة بالفرضيات", "objective_ids": ["lo_diag", "lo_indep"], "scored_by": "deterministic", "weight": 0.2, "levels": levels(["لا روابط", "قليلة", "نصفها صحيح", "معظمها", "كلها دقيقة"])},
        {"id": "c_uncertainty", "name_ar": "معايرة الثقة", "objective_ids": ["lo_calib"], "scored_by": "deterministic", "weight": 0.15, "levels": levels(["ثقة مفرطة", "حدود قليلة", "جزئية", "معقولة", "معايَرة كاملة"])},
        {"id": "c_revision", "name_ar": "مراجعة الرأي", "objective_ids": ["lo_revise"], "scored_by": "deterministic", "weight": 0.1, "levels": levels(["بقي على فرضية مرفوضة", "لم يعلن فرضية", "ثبت على فرضية سليمة", "غيّر بدليل", "غيّر بدليل ووثّق"])},
        {"id": "c_elimination", "name_ar": "استبعاد الفرضيات الخاطئة", "objective_ids": ["lo_hyp"], "scored_by": "deterministic", "weight": 0.1, "levels": levels(["لم يستبعد", "استبعد خطأً", "فرضية بدليل", "فرضيتين", "كل الخاطئة"])},
        {"id": "c_justification", "name_ar": "جودة الحجة المكتوبة", "objective_ids": ["lo_claim", "lo_hyp"], "scored_by": "human", "weight": 0.15, "levels": levels(["لا حجة", "ادعاء بلا سند", "أدلة دون ربط", "ربط الأدلة بالاستنتاج", "ربط مع الحجة المضادة والحدود"])},
    ],
}
def H(id, lv, kind, text, trig, target=None, w=0.0):
    d = {"id": id, "level": lv, "kind": kind, "text_ar": text, "trigger": trig, "assessment_weight": w}
    if target: d["targets_inference_id"] = target
    return d
he = lambda e: {"has_evidence": e}
hints = [
    H("hg1", 1, "metacognitive", "حين يتكلم أحدهم بثقة، افصل سؤالين: كم الحجة مقنعة، وما السجل الذي يسندها؟", {"always": True}, None, 0.02),
    H("hg2", 2, "focus_area", "اكتب لكل متكلم جملة واحدة: ما الذي رآه بنفسه، وما الذي نقله عن غيره أو استنتجه؟", he("ev_maher_statement"), None, 0.04),
    H("hg3", 3, "pointer", "ضع إفادة من يصف الطباع في خانة منفصلة، وانظر ماذا يبقى من الأدلة حين تُحذف.", he("ev_laith_statement"), None, 0.08),
    H("hd1", 1, "metacognitive", "حين يخالف رقمٌ رقماً، اسأل: هل يقيسان الشيء نفسه بالدقة الزمنية نفسها؟", he("ev_dashboard"), "i_exc_a", 0.02),
    H("hd2", 2, "pointer", "اقرأ مفتاح اللوحة، ثم قارن رقمها بمجموع القراءات الساعية في التصدير الخام.", he("ev_dashboard"), "i_exc_a", 0.06),
    H("hd3", 3, "partial_reveal", "احسب متوسط قراءات الجمعة الثماني في التصدير، وانظر هل يساوي رقم اللوحة وما هي أعلى قراءة فيها.", he("ev_logger_raw"), "i_exc_a", 0.1),
    H("hi1", 1, "metacognitive", "إذا اتفق سجلان صادران من الجهة نفسها، فهل هما مصدر واحد أم مصدران؟", he("ev_intake_receipt"), "i_ok_a", 0.02),
    H("hi2", 2, "pointer", "ابحث عن سجل لحالة الطقم ليس من كتابة المرمّمة ولا من كتابة المسجّلة.", he("ev_intake_receipt"), "i_ok_a", 0.06),
    H("hl1", 1, "metacognitive", "من يملك الدليل على ما حدث للجهاز بعد انتهاء الزيارة؟", he("ev_service_sheet"), "i_left_off", 0.02),
    H("hl2", 2, "pointer", "اعرض ورقة الخدمة على المنسّق بعد أن تقرأ ما جاء فيها عن التسليم.", he("ev_service_sheet"), "i_left_off", 0.06),
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
Act("a_read_report", "examine", "اقرأ تقرير إنجاز الترميم", al, [G("ev_restoration_report")], "loc_lab", "READ_REPORT")
Act("a_read_anon", "examine", "اقرأ البلاغ المجهول", al, [G("ev_anon_report")], "loc_hall", "READ_ANON")
Act("a_read_damage", "examine", "اطلب سجل الحالة بعد الصيانة", al, [G("ev_damage_record")], "loc_store", "READ_DAMAGE")
for cid, lab in [("maher", "ماهر الشامي"), ("salma", "سلمى"), ("rima", "ريما"), ("laith", "ليث"), ("adel", "عادل"), ("murad", "مراد"), ("nabil", "د. نبيل")]:
    Act(f"a_int_{cid}", "interview", f"ابدأ مقابلة {lab}", al, [{"op": "raise_trust", "ref_id": cid, "amount": 1}], cid, f"INT_{cid.upper()}")
Act("a_get_intake", "examine", "اطلب نموذج استلام المخزن", fu("f_intake"), [G("ev_intake_receipt")], "loc_store", "GET_INTAKE")
Act("a_get_imaging", "examine", "اطلب سجل محطة التصوير", fu("f_imaging_clean"), [G("ev_imaging_log")], "loc_lab", "GET_IMAGING")
Act("a_get_door", "examine", "اطلب سجل بطاقات المخزن", fu("f_door_exists"), [G("ev_door_log")], "loc_store", "GET_DOOR")
Act("a_get_logger", "examine", "اطلب التصدير الخام لمقياس الرطوبة", fu("f_logger_exists"), [G("ev_logger_raw")], "loc_store", "GET_LOGGER")
Act("a_get_dashboard", "examine", "افتح لوحة مراقبة المرافق", fu("f_dashboard_exists"), [G("ev_dashboard")], "loc_facilities", "GET_DASHBOARD")
Act("a_get_paper", "examine", "افحص ورقة المسجّل الميكانيكي", fu("f_paper_exists"), [G("ev_paper_trace")], "loc_corridor", "GET_PAPER")
Act("a_get_service", "examine", "اطلب ورقة خدمة الصيانة", fu("f_service_visit"), [G("ev_service_sheet")], "loc_facilities", "GET_SERVICE")
Act("a_get_workorder", "examine", "اطلب أمر الصيانة الوقائية", fu("f_work_order"), [G("ev_work_order")], "loc_facilities", "GET_WORKORDER")
Act("a_request_expert", "request_lab_test", "اطلب من خبير الحفظ المستقل رأياً مكتوباً في نمط التلف", he("ev_damage_record"), [G("ev_expert_review")], "loc_hall", "REQUEST_EXPERT")
Act("a_note_maher", "examine", "دوّن إفادة ماهر الشامي", fu("f_maher_says"), [G("ev_maher_statement")], "maher", "NOTE_MAHER")
Act("a_note_laith", "examine", "دوّن إفادة ليث", fu("f_laith_impression"), [G("ev_laith_statement")], "laith", "NOTE_LAITH")
Act("a_note_adel", "examine", "دوّن إفادة عادل", fu("f_guard_saw"), [G("ev_adel_statement")], "adel", "NOTE_ADEL")
Act("a_note_murad", "examine", "دوّن إفادة مراد", fu("f_unit_left_off"), [G("ev_murad_statement")], "murad", "NOTE_MURAD")
Act("p_service_murad", "present_evidence", "اعرض ورقة خدمة الصيانة على مراد", {"presented": {"evidence_id": "ev_service_sheet", "to_character": "murad"}}, [{"op": "emit_event", "ref_id": "PRESENTED_SERVICE"}], "murad", "P_SERVICE_MURAD", 0)
Act("a_hint", "request_hint", "اطلب تلميحاً", al, [], None, "REQUEST_HINT", 0)
Act("a_accuse", "final_accusation", "قدّم الرأي المعلّل النهائي", al, [{"op": "emit_event", "ref_id": "SUBMIT"}], None, "FINAL_ACCUSATION", 0)

topics = [
    {"id": "t_report", "label_ar": "تقرير الترميم والتصوير", "example_questions_ar": ["متى وقّعتِ تقرير الإنجاز؟", "هل صُوّر الطقم قبل التسليم؟"], "fact_ids": ["f_report_signed", "f_imaging_clean"]},
    {"id": "t_intake", "label_ar": "الاستلام في المخزن", "example_questions_ar": ["متى استلمتِ الطقم؟", "كيف تُسجَّل الدخول إلى المخزن؟"], "fact_ids": ["f_intake", "f_door_exists"]},
    {"id": "t_deputy", "label_ar": "ما قيل في الجلسة الأولى", "example_questions_ar": ["على أي أساس رفعت البلاغ؟", "هل تحققت من لوحة المرافق؟"], "fact_ids": ["f_maher_says", "f_dashboard_exists"]},
    {"id": "t_bench", "label_ar": "أين كان الطقم نهاية الأسبوع", "example_questions_ar": ["أين بقي الطقم نهاية الأسبوع؟", "ما مصدر قولك إنه بقي على الطاولة؟"], "fact_ids": [], "claim_ids": ["cl_maher_bench"]},
    {"id": "t_pattern", "label_ar": "نمط التلف", "example_questions_ar": ["لماذا ترى أن النمط يدل على سوء المعالجة؟"], "fact_ids": [], "claim_ids": ["cl_maher_handling"]},
    {"id": "t_impression", "label_ar": "انطباع عن المرمّمة", "example_questions_ar": ["ماذا رأيت من سلمى؟", "هل شاهدت شيئاً محدداً؟"], "fact_ids": ["f_laith_impression"], "claim_ids": ["cl_laith_nervous"]},
    {"id": "t_night", "label_ar": "جولة المساء", "example_questions_ar": ["ماذا رأيت في الممر؟", "في أي يوم كان ذلك؟"], "fact_ids": ["f_guard_saw"], "claim_ids": ["cl_adel_friday"]},
    {"id": "t_service", "label_ar": "زيارة الصيانة", "example_questions_ar": ["من جاء إلى المخزن مساء الخميس؟", "متى صدر أمر الصيانة؟"], "fact_ids": ["f_service_visit", "f_work_order"]},
    {"id": "t_handover", "label_ar": "ما بعد الزيارة", "example_questions_ar": ["ماذا حدث للجهاز بعد انتهاء الزيارة؟", "من أعاد تشغيله؟"], "fact_ids": ["f_unit_left_off"], "claim_ids": ["cl_murad_return"]},
    {"id": "t_monitoring", "label_ar": "لوحة المراقبة", "example_questions_ar": ["هل أنذرت اللوحة؟", "ماذا تعني أرقامها؟"], "fact_ids": [], "claim_ids": ["cl_murad_dash"]},
    {"id": "t_records", "label_ar": "سجلات الرطوبة", "example_questions_ar": ["أي أجهزة تقيس الرطوبة؟", "ماذا يسجّل المقياس؟"], "fact_ids": ["f_logger_exists", "f_paper_exists"]},
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
    (1, "لوحة المرافق تعرض متوسط القراءات الساعية نفسها: المتوسط 62% لا يناقض قراءة 80%، بل يطمسها، والمقياس الخام يبيّن نحو ست عشرة ساعة فوق حد الخطر.", ["ev_logger_raw", "ev_dashboard"], "i_exc_a"),
    (2, "المسار المستقل للرطوبة: ورقة الخدمة تقول إن المزيل عُزل 20:05 ولم يُعد توصيله، والمسجّل الميكانيكي في الممر يرسم القمتين نفسيهما بآلية لا تعتمد على الرقمي.", ["ev_service_sheet", "ev_paper_trace"], "i_exc_b"),
    (3, "سلامة الطقم عند الإيداع: تقرير المرمّمة ونموذج استلام ريما من كاتبين مختلفين يصفان الحال نفسها.", ["ev_restoration_report", "ev_intake_receipt"], "i_ok_a"),
    (4, "المسار المستقل للسلامة: محطة التصوير الآلية وسجل بطاقات المخزن يغلقان الفجوة بين التصوير والإيداع من دون أي إفادة بشرية.", ["ev_imaging_log", "ev_door_log"], "i_ok_b"),
    (5, "فرضية المعالجة الخاطئة تسقط: الأوراق سليمة عند إيداعها المختوم، ثم ارتفعت رطوبة المخزن بعده، ولا بطاقة للمرمّمة في المخزن.", ["ev_intake_receipt", "ev_door_log", "ev_logger_raw"], "i_rule_restorer"),
    (6, "فرضية الإتلاف المتعمد تسقط: أمر الصيانة وورقة الفنية يثبتان أن العزل كان لجدول سابق لإعلان الشغور، والنائب لم يدخل المخزن، فالمصلحة المعلنة لا تحلّ محل أثر على الفعل.", ["ev_work_order", "ev_service_sheet", "ev_door_log"], "i_rule_sabotage"),
    (7, "من أين جاء الفراغ؟ الفنية كتبت أن الجهاز ما زال معزولاً وأن التسليم شفهي، واعترف المنسّق بأنه لم يدوّن مهمة؛ فسهو التسليم هو الحلقة المفقودة، لا تقصير فرد بعينه.", ["ev_service_sheet", "ev_murad_statement"], "i_left_off"),
]
ending = {
    "steps": [{"order": o, "text_ar": t, "uses_evidence_ids": u, "inference_id": i} for o, t, u, i in steps],
    "alternative_paths_ar": [
        "يمكن إثبات سلامة الطقم عند الإيداع من تقرير المرمّمة ونموذج الاستلام وحدهما، ويمكن إثباتها من سجل محطة التصوير وسجل البطاقات وحدهما؛ والأقوى أن يتفق المساران.",
        "ويمكن إثبات ارتفاع الرطوبة من المقياس الخام ومفتاح اللوحة، أو من ورقة الخدمة والمسجّل الميكانيكي؛ ولا يعتمد المساران على دليل مشترك.",
    ],
    "what_evidence_could_not_show_ar": [
        "لا تبيّن الأدلة من كتب البلاغ المجهول ولا لماذا شابهت عبارته عبارة بعض المتكلمين.",
        "لا تحدد الأدلة اللحظة التي بدأ فيها العفن بالدقيقة، ولم يُفحص الورق مخبرياً؛ الرأي الفني على صور ووثائق.",
        "لا تنفي الأدلة أن تكون لمصلحة النائب علاقة بتسريع الفصل، لكنها لا تُثبت فعلاً منه، ولا يصح بناء حكم على المصلحة وحدها.",
    ],
    "science_notes_ar": [
        "قوة الحجة وقوة الدليل شيئان: عرض واثق أو متكلم يبدأ الجلسة لا يزيدان وزن الدليل، والعبرة بالسجل الذي يسند كل جملة.",
        "الارتباك في الكلام ليس دليلاً على إخفاء خطأ؛ فشهادة المظهر تُرفض ويُسأل عن الوقائع المكتوبة.",
        "الاستقلال لا يُعدّ بعدد الأوراق بل بعدد الآليات: سجلان من العملية نفسها مصدر واحد، وجهازان بآليتين مختلفتين مصدران.",
        "المتوسط يخفي الذروة: اسأل عن دقة كل رقم الزمنية قبل أن تحكم أن سجلين متعارضين، وستجد أن كليهما صحيح.",
        "سلسلة العهدة لا تقف عند الإيداع: ما لم يُدوَّن في التسليم الشفهي يضيع، وإصلاح الضرر هنا مؤسسي: تدوين المهام وإنذار ساعي لا يومي، وإعادة النظر في قرار الفصل.",
        "كلفة الاستعجال: فُصلت مرمّمة وعُلّقت جلسات قبل أن يُراجع أحد المقياس الخام. بطاقة الأصل: القضية أصلية من ATHAR، وبنيتها مستلهمة من إطار «المحاكمة أمام القاضي» في حكايات شعبية عابرة للثقافات متعددة النسخ.",
    ],
}
core = {
    "schema_version": "0.1.0", "case_id": CID, "case_version": "0.1.0",
    "meta": {"title_ar": "جلسة استماع في متحف الأثر", "title_en": "A Hearing at the Athar Museum", "age_band": "16-18", "locale": "ar", "dialogue_register": "msa", "estimated_minutes": 40, "difficulty": 4,
             "content_flags": ["no_violence", "science_lab"], "authors": ["فريق أثر التحريري (مسودة بمساعدة الذكاء الاصطناعي، لم تُراجَع بشرياً بعد)"],
             "knowledge_object_refs": ["KO-RS-06-018", "KO-RS-06-019", "KO-RS-05-007", "KO-RS-05-004", "KO-RS-06-003", "KO-RS-06-001", "KO-RS-06-017", "KO-RS-05-002", "KO-RS-06-021", "KO-RS-06-009", "KO-FC-04-031"]},
    "premise": {"hook_ar": "مرمّمة فُصلت بناءً على بلاغ مجهول، وثلاثة متحدثين أمام مجلس الأمناء يقدّمون روايات تبدو متفقة. لكن الأرقام في المخزن لها رأي آخر.",
                "player_role_ar": "أنت مراجع مستقل يعيّنه مجلس أمناء متحف الأثر ليقدّم رأياً معلّلاً في سبب تلف المخطوطة قبل أن يحسم المجلس شيئاً.",
                "setting_ar": "متحف الأثر في مدينة «المرسى». تُعقد ثلاث جلسات استماع علنية عن مخطوطة «الأثر-17»، والوقائع بين الخميس والسبت بتوقيت المتحف.",
                "public_fact_ids": ["f_damaged", "f_dismissed", "f_anon_claim", "f_vacancy", "f_deputy_first"],
                "assumed_general_knowledge_ar": ["الرق والورق يتأثران بارتفاع الرطوبة الطويل", "المتوسط اليومي لا يبيّن أعلى قراءة", "قوة العرض لا تساوي قوة الدليل"]},
    "entities": {"characters": chars, "locations": locations, "objects": objects, "organizations": orgs},
    "truth": {"solution": {"culprit_ids": ["murad"], "summary_ar": "لم يُتلف أحد المخطوطة عمداً. فُصل مزيل الرطوبة لصيانة مجدولة سلفاً، وبقي مفصولاً بسبب تسليم شفهي لم تُدوَّن فيه مهمة إعادة التوصيل، فارتفعت رطوبة المخزن ليلتين. والطقم كان سليماً عند الإيداع، ولوحة المرافق تتوسط القراءات فلا تنذر.", "key_fact_ids": ["f_ok_deposit", "f_excursion", "f_planned"]},
              "facts": facts, "claims": claims},
    "timeline": timeline, "evidence": ev, "evidence_graph": {"inferences": inf},
    "character_knowledge": ck, "hypotheses": hyps, "misdirection_plan": mis, "learning_objectives": los,
    "mechanics": {"time_budget_units": 50, "actions": A},
    "state_machine": {"id": "c020", "initial": "briefing", "type": "compound", "states": {
        "briefing": {"description_ar": "الإحاطة", "type": "atomic", "on": {"START": {"target": "investigating"}}},
        "investigating": {"description_ar": "التحقيق", "type": "compound", "initial": "gathering",
                          "states": {"gathering": {"type": "atomic", "on": {"OPEN_DEDUCTION": {"target": "deducing"}}}, "deducing": {"type": "atomic", "on": {"BACK": {"target": "gathering"}}}},
                          "on": {"SUBMIT": {"target": "review"}}},
        "review": {"description_ar": "مراجعة", "type": "atomic", "on": {"CLOSE": {"target": "resolved"}}},
        "resolved": {"description_ar": "إغلاق", "type": "final"}}},
    "dialogue": {"max_turns_per_interview": 10, "llm_enabled": False, "topics": topics},
    "rubric": rub, "hint_ladder": hints,
    "fairness_test": {"requirements": {"min_disjoint_proof_paths": 2, "max_inference_depth": 3, "all_red_herrings_refutable": True, "culprit_uniquely_entailed": True, "no_hidden_fact_dependency": True, "max_required_actions": 50}, "runs": []},
    "ending_explanation": ending,
    "expert_review": [{"role": r, "reviewer": "—", "status": "pending", "content_hash": "unbound", "date": "2026-10-27", "notes_ar": "بانتظار مراجعة بشرية؛ لم يُجرَ أي اعتماد."} for r in
                      ["narrative_editor", "scientific_reviewer", "learning_designer", "age_appropriateness", "cultural_reviewer", "legal_rights", "safety"]],
}
ui = {
    "case_id": CID,
    "clock": {"epoch_hhmm": "00:00", "zone_label_ar": "توقيت المتحف"},
    "cover": {"title_ar": "جلسة استماع في متحف الأثر", "tagline_ar": "ثلاثة متحدثين يتفقون، وسجل واحد لم يقرأه أحد", "kicker_ar": "الملف العشرون · الحجة والدليل", "glyph": "⚖", "accent": "amber"},
    "cold_open_ar": ["الأحد، قبل الجلسة الأولى.", "فُصلت مرمّمة من متحف الأثر بعد بلاغ بلا اسم عن تلف مخطوطة. نائب المدير يتكلم أولاً، وشاهد يقول إنها «مرتبكة دائماً»، وحارس يرى امرأة في الممر.",
                     "يطلب منك مجلس الأمناء رأياً معلّلاً، لا عرضاً مقنعاً. أمامك أوراق وسجلات ومقياس يقرأ الهواء كل ساعة.",
                     "ابدأ بسؤال واحد: ما الذي يسند كل جملة قيلت في القاعة؟"],
    "labs": [],
    "source_classes": [
        {"id": "primary_record", "label_ar": "سجل أصلي", "help_ar": "يُنتجه نظام أو شخص لحظة الحدث دون وسيط، كنموذج استلام أو سجل بطاقات أو ورقة خدمة."},
        {"id": "redisplay", "label_ar": "نسخة معروضة", "help_ar": "معلومة أُعيد عرضها أو لُخّصت من سجل آخر، كمتوسط في لوحة؛ تتأثر بطريقة التلخيص."},
        {"id": "claim", "label_ar": "قول أو تصريح", "help_ar": "إفادة أو رأي أو بلاغ؛ يُقاس بالسجلات لا بنبرة صاحبه ولا بموقعه."},
        {"id": "template", "label_ar": "قالب أو نموذج", "help_ar": "نص جاهز لا يصف الحدث الفعلي بذاته."},
        {"id": "public_document", "label_ar": "وثيقة منشورة", "help_ar": "وثيقة معلنة ومعروف ناشرها."}],
    "limit_menu": [
        {"id": "l_anon", "label_ar": "الأدلة لا تبيّن من كتب البلاغ المجهول"},
        {"id": "l_onset", "label_ar": "لا تحدد الأدلة لحظة بدء العفن بالدقيقة، والرأي الفني على صور ووثائق لا على فحص الورق"},
        {"id": "l_motive", "label_ar": "لا تنفي الأدلة أن تكون لنائب المدير مصلحة، لكنها لا تثبت منه فعلاً"},
        {"id": "l_invalid_nerves", "label_ar": "ارتباك المرمّمة أثناء كلامها يدل على أنها تخفي خطأً"},
        {"id": "l_invalid_first", "label_ar": "كون النائب أول المتكلمين يدل على أنه محق"},
        {"id": "l_invalid_motive", "label_ar": "مصلحة النائب في المنصب تكفي لإثبات أنه أتلف المخطوطة"}],
    "mind_change_menu": [
        {"id": "m_seal", "label_ar": "ظهور دليل على أن ختم الصندوق فُتح بين الخميس والسبت"},
        {"id": "m_card", "label_ar": "ظهور دخول لبطاقة المرمّمة أو النائب إلى المخزن في الفترة نفسها"},
        {"id": "m_logger_fault", "label_ar": "ثبوت عطل في مقياس الرطوبة الرقمي وفي المسجّل الميكانيكي معاً"},
        {"id": "m_louder", "label_ar": "ازدياد عدد المتحدثين الذين يؤيدون رواية النائب"}],
    "transfer": {
        "id": "tr_cold_room", "title_ar": "اختبار نقل المهارة: غرفة البذور الباردة",
        "scenario_ar": "قال مدير مخزن بذور إن غرفة التبريد «سليمة طوال الأسبوع» لأن لوحة المراقبة لم تُنذر، لكن عينة تلفت. أمامك وثيقتان من واقعة خيالية لا علاقة لها بالقضية.",
        "documents": [
            {"title_ar": "لوحة المراقبة", "body_ar": "المتوسط اليومي لحرارة الغرفة: الثلاثاء 4.1° · الأربعاء 4.6° · الخميس 4.9°. حد الإنذار: متوسط يومي فوق 6°."},
            {"title_ar": "سجل الحرارة الخام", "body_ar": "الأربعاء: 01:00 — 3.5° · 04:00 — 9.2° · 07:00 — 8.8° · 10:00 — 3.9°. حد الخطر للبذور: فوق 8° لأكثر من ساعتين."}],
        "prompt_ar": "اختر الخطوات التي تصلح للحكم على سلامة الغرفة (يمكنك اختيار أكثر من خطوة).",
        "options": [
            {"id": "o1", "text_ar": "معرفة كيف حُسب رقم اللوحة قبل مقارنته بالسجل الخام"},
            {"id": "o2", "text_ar": "قراءة القراءات الخام لا متوسطها ومقابلتها بحد الخطر المعتمد"},
            {"id": "o3", "text_ar": "البحث عن جهاز قياس مستقل آخر بآلية مختلفة"},
            {"id": "o4", "text_ar": "التفريق بين غياب الإنذار وسلامة كل ساعة"},
            {"id": "o5", "text_ar": "تصديق المدير لأن لوحته لم تُنذر"},
            {"id": "o6", "text_ar": "الحكم من ثقة المتحدث في عرضه"},
            {"id": "o7", "text_ar": "اعتبار اللوحة والسجل باطلين لأن رقميهما مختلفان"}],
        "free_text_prompt_ar": "اكتب في ثلاثة أسطر كيف تقرّر نسبة الترجيح بأن الغرفة كانت سليمة طوال الأسبوع.",
    },
    "skills": [{"skill_id": "KO-RS-06-018", "track": "B"}, {"skill_id": "KO-RS-06-019", "track": "D"}, {"skill_id": "KO-RS-05-007", "track": "B"}, {"skill_id": "KO-RS-05-004", "track": "B"}, {"skill_id": "KO-FC-04-031", "track": "E"}],
    "stage_hooks_ar": {"briefing": "كل متحدث واثق… فمن منهم يحمل ورقة؟", "investigating": "سجلان يتعارضان ظاهرياً، وكلاهما صحيح.", "review": "قبل أن تقدّم رأيك للمجلس: ما الذي لا تعرفه؟", "resolved": "أُغلقت الجلسات. في الأرشيف خلاف حول جهاز لوحي ونافورة."},
    "character_glyphs": {"maher": "م", "salma": "س", "rima": "ر", "laith": "ل", "adel": "ع", "murad": "د", "nabil": "ن"},
}
sc = {
    "case_id": CID,
    "accepted_conclusions": {
        "h_unit": {"grade": 1, "note_ar": "استنتاج متسق مع الأدلة ويتطلب ذكر حدوده."},
        "h_restorer": {"grade": 0, "note_ar": "يبني على الانطباع ولوحة المتوسطات، ويتجاهل سلامة الطقم عند الإيداع المختوم."},
        "h_sabotage": {"grade": 0, "note_ar": "يحوّل المصلحة المعلنة إلى فعل، ولا أثر للفعل في السجلات."},
        "h_nodata": {"grade": 0, "note_ar": "التعارض ظاهري ويزول بفهم دقة كل سجل؛ لا يعني بطلان السجلات."}},
    "confidence_band": {"h_unit": [65, 90], "h_restorer": [0, 15], "h_sabotage": [0, 15], "h_nodata": [0, 20]},
    "source_key": {"ev_restoration_report": "primary_record", "ev_anon_report": "claim", "ev_damage_record": "primary_record", "ev_intake_receipt": "primary_record",
                   "ev_imaging_log": "primary_record", "ev_door_log": "primary_record", "ev_logger_raw": "primary_record", "ev_dashboard": "redisplay",
                   "ev_paper_trace": "primary_record", "ev_service_sheet": "primary_record", "ev_work_order": "primary_record", "ev_expert_review": "claim",
                   "ev_maher_statement": "claim", "ev_laith_statement": "claim", "ev_adel_statement": "claim", "ev_murad_statement": "claim"},
    "link_key": {
        "h_unit": {"ev_restoration_report": "supports", "ev_intake_receipt": "supports", "ev_imaging_log": "supports", "ev_door_log": "supports", "ev_logger_raw": "supports", "ev_paper_trace": "supports",
                   "ev_service_sheet": "supports", "ev_work_order": "supports", "ev_expert_review": "supports", "ev_murad_statement": "supports", "ev_dashboard": "neutral", "ev_damage_record": "neutral"},
        "h_restorer": {"ev_anon_report": "supports", "ev_laith_statement": "supports", "ev_adel_statement": "supports", "ev_maher_statement": "supports", "ev_dashboard": "supports",
                       "ev_intake_receipt": "weakens", "ev_imaging_log": "weakens", "ev_door_log": "weakens", "ev_logger_raw": "weakens", "ev_expert_review": "weakens", "ev_restoration_report": "weakens"},
        "h_sabotage": {"ev_maher_statement": "neutral", "ev_anon_report": "neutral", "ev_work_order": "weakens", "ev_door_log": "weakens", "ev_service_sheet": "weakens"},
        "h_nodata": {"ev_dashboard": "supports", "ev_logger_raw": "weakens", "ev_paper_trace": "weakens", "ev_service_sheet": "weakens"},
    },
    "required_limits": ["l_anon", "l_onset"], "valid_mind_changers": ["m_seal", "m_card", "m_logger_fault"], "invalid_limits": ["l_invalid_nerves", "l_invalid_first", "l_invalid_motive"],
    "decisive_evidence": ["ev_intake_receipt", "ev_restoration_report", "ev_logger_raw", "ev_service_sheet", "ev_paper_trace", "ev_door_log"],
    "lab_requirement": None,
    "timeline_requirement": [{"evidence_id": "ev_restoration_report", "utc_minute": 850, "tol": 6}, {"evidence_id": "ev_intake_receipt", "utc_minute": 878, "tol": 8},
                             {"evidence_id": "ev_service_sheet", "utc_minute": 1205, "tol": 10}, {"evidence_id": "ev_damage_record", "utc_minute": 3860, "tol": 12}],
    "refuted_hypotheses": ["h_restorer", "h_sabotage", "h_nodata"],
    "criteria_map": {"c_source": "source_typing", "c_conflict": "conflict_resolution", "c_links": "hypothesis_links", "c_uncertainty": "uncertainty", "c_revision": "revision", "c_elimination": "elimination", "c_justification": "justification_human"},
    "transfer_key": {"valid": ["o1", "o2", "o3", "o4"], "invalid": ["o5", "o6", "o7"]},
    "caps": {"no_citations_max": 45, "no_conflict_resolution_max": 65},
}
os.makedirs(OUT, exist_ok=True)
for suf, obj in [("", core), (".ui", ui), (".scoring", sc)]:
    with open(os.path.join(OUT, f"{CID}{suf}.json"), "w", encoding="utf8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
print("ok")
