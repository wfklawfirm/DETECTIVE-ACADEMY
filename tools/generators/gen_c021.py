#!/usr/bin/env python3
# Case c021 «هل بلغ صاحبك النافورة؟» — advanced (16-18) interview-and-digital-timeline case. Teaches: a «guilty-knowledge» slip (the denier
# says a detail he was never told) is a reason to look for INNOCENT routes and for independent evidence, never a confession; re-check
# whether a detail is still "unpublished" before using it; reconcile two reliable clocks (device vs network) with a skew; build the
# same conclusion on two source families that share nothing. No-culprit convention: the student who took the tablet in good faith and left
# it behind (Nour) is recorded in culprit_ids; the student wrongly suspected (Karim) did nothing wrong, and the claimant (Yazan) made an
# honest source-memory error. Library seed: S-11 (ARC-34, HS-003 «إياس والسؤال عن الشجرة»); origin card: attributed heritage report,
# rebuilt as an original ATHAR story. All names, places and records are fictional.
# Mechanics notes: no option exists to deceive the person being interviewed; the "unpublished-details record" is an evidence item
# (the complaint) whose limits the player must test; the engine has no free-form interview-design mechanic, so the neutrality of the
# interviewer's questions is evidenced by the interview note. The time lab (time_normalizer) carries the clock-skew reconciliation.
# Calendar (fictional): minute 0 = Tuesday 14:00 (university time). Mon 21:15 = -1005; Wed 10:00 = 1200.
# Usage: gen_c021.py OUT_DIR
import json, sys, os
OUT = sys.argv[1]
CID = "c021_fountain_tablet"

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
ch("yazan", "يزن العلي", "victim", "طالب في السنة الثانية، صاحب الجهاز اللوحي",
   "صادق ومتعجل، يثق بذاكرته أكثر مما ينبغي. يتألم من فقدان جهازه ويتمسك بأول تفسير خطر له، ثم يتراجع إذا رأى سجلاً.",
   ["أن يستعيد جهازه", "ألا يبدو أنه يتهم زميله بلا سبب"],
   [L("yz_greet", "greeting", "أريد جهازي فقط. أنا متأكد مما أتذكره."),
    L("yz_post", "reveal", "نشرت في مجموعة الصف مساء الثلاثاء أنني تركت الجهاز مع صديق عند النافورة، ولم أذكر لون الغلاف ولا الساعة.", ["f_post_public"]),
    L("yz_backup", "reveal", "حسابي السحابي يحتفظ بنسخة من سجل الشبكات التي يتصل بها جهازي، وأستطيع أن أطلب لك ما فيها.", ["f_backup_exists"]),
    L("yz_memory", "reveal", "كنت أنظر إلى هاتفي حين سلّمته، وظننت أن المستلم كريم لأنه هو من طلب الجهاز قبلها بيوم.", ["f_yazan_memory"]),
    L("yz_karim", "reveal", "سلّمته لكريم عند النافورة نحو الثالثة والعشر دقائق، ولا شاهد.", None, ["cl_yazan_karim"]),
    L("yz_unknown", "deflect_unknown", "لا أتذكر أكثر من هذا."),
    L("yz_off", "deflect_offtopic", "اسألني عن الجهاز وعن عصر الثلاثاء."),
    L("yz_bye", "farewell", "أرجو أن ننتهي بلا ظلم لأحد.")])
ch("karim", "كريم الصباغ", "suspect", "طالب هندسة في السنة الثانية",
   "هادئ ومتحفظ، يتوتر حين يُظن به سوء، فيجيب باختصار. توتره ليس دليلاً على شيء، وهو يقول ما يتذكره دون محاولة تجميله.",
   ["أن يُنصَف", "ألا يُنسب إليه ما لم يفعله"],
   [L("kr_greet", "greeting", "أنا لم آخذ شيئاً. اسألني ما شئت بهدوء."),
    L("kr_lab", "reveal", "كنت عصر الثلاثاء في الاختبار العملي في مختبر الهندسة حتى بعد الرابعة.", ["f_karim_says_lab"]),
    L("kr_chat", "reveal", "نعم، تحدثنا مساء الاثنين عن أن ألتقي يزن عند النافورة لأستعير الجهاز، ثم كتبت له ظهر الثلاثاء أنني لن أستطيع.", ["f_chat_agreed"]),
    L("kr_slip", "reveal", "قلت كلمة النافورة في المقابلة دون أن أنتبه لها. لا أذكر الآن لماذا قلتها.", ["f_karim_mentioned"]),
    L("kr_unknown", "deflect_unknown", "لا أعرف أكثر من هذا."),
    L("kr_off", "deflect_offtopic", "هذا لا يخص الجهاز. اسألني عن يوم الثلاثاء."),
    L("kr_bye", "farewell", "شكراً لأنك سألت قبل أن تحكم.")])
ch("nour", "نور السعيد", "suspect", "طالبة في السنة الثانية، صديقة يزن وكريم",
   "ودودة وسريعة النسيان في التفاصيل الصغيرة، تكتم إشعارات مجموعات الصف لتركز. تتفاجأ إذا ظهر اسمها في قضية، وتشرح ما حدث حين يتضح لها.",
   ["ألا تكون سبب مشكلة لصديقها", "أن تستعيد ما فاتها من الأحداث"],
   [L("nr_greet", "greeting", "أهلاً. لا أعرف لماذا طُلب مني الحضور، لكنني أجيب."),
    L("nr_returned", "reveal", "ظننت أنني أعدت كل شيء لأصحابه قبل أن أدخل المكتبة.", None, ["cl_nour_returned"]),
    L("nr_refuse", "refuse_secret", "لا أريد أن أخمّن في شيء لا أفهمه بعد."),
    L("nr_took", "reveal", "نعم... أخذت جهاز يزن من يديه عند النافورة قرابة الثالثة والعشر دقائق لأقرأ ملفاً، ثم نسيته على الطاولة 14 حين خرجت. وأنا أكتم إشعارات مجموعة الصف فلم أقرأ منشوره.", ["f_nour_took"]),
    L("nr_unknown", "deflect_unknown", "لا أذكر."),
    L("nr_off", "deflect_offtopic", "اسألني عن عصر الثلاثاء."),
    L("nr_bye", "farewell", "سأذهب إلى مكتب المفقودات الآن.")])
ch("sami", "سامي القاسم", "witness", "طالب في السنة الثانية، صديق ثالث",
   "اجتماعي ويحب نقل الأخبار، يبني على ما سمعه ولا يحدد من أين. يتراجع إذا طُلب منه أن يفرّق بين ما رآه وما سمعه.",
   ["ألا يُلام على نقل خبر", "أن تنتهي القضية سريعاً"],
   [L("sm_greet", "greeting", "سمعت القصة كلها، وأحب أن أساعد."),
    L("sm_msg", "reveal", "كتبت لكريم مساء الثلاثاء أسأله إن كان أخذ جهاز يزن عند النافورة، بعد أن قرأت المنشور.", ["f_friend_msg"]),
    L("sm_rumour", "reveal", "كل من في المجموعة يقول إن كريم هو من أخذه، فلا بد أن في الأمر شيئاً.", None, ["cl_sami_rumour"]),
    L("sm_unknown", "deflect_unknown", "لا أعرف شيئاً محدداً."),
    L("sm_off", "deflect_offtopic", "اسألني عمّا سمعته."),
    L("sm_bye", "farewell", "لن أنقل شيئاً قبل أن أتأكد.")])
ch("waleed", "وليد النجار", "expert", "مشرف شبكة الجامعة",
   "هادئ ودقيق، يتحدث بمرجع الخادم ويذكّر بأن لكل جهاز ساعته. لا يعرف من يحمل الجهاز ولا ما يفعله.",
   ["أن تُقرأ سجلات الشبكة بحدودها"],
   [L("wl_greet", "greeting", "أقرأ سجلات الشبكة، ولا أعرف من يحمل الأجهزة."),
    L("wl_wifi", "reveal", "تسجّل الشبكة اقتران كل جهاز بنقطة وصول وزمنه بساعة الخادم. أما الأجهزة غير المسجّلة فتظهر بمعرّف قصير، ولكل جهاز ساعته التي قد تختلف عن ساعتنا.", ["f_wifi_exists"]),
    L("wl_unknown", "deflect_unknown", "هذا خارج ما تسجّله الشبكة."),
    L("wl_off", "deflect_offtopic", "اسألني عن السجلات ونقاط الوصول."),
    L("wl_bye", "farewell", "اقرأ كل وقت مع ساعة مصدره.")])
ch("maha", "مها الحلبي", "witness", "موظفة خدمات في مكتبة الجامعة",
   "منظمة ومباشرة، تقرأ من سجلاتها وتميّز بين ما سُجّل وما افترضته. لا تخمّن من أخذ شيئاً.",
   ["أن تبقى سجلات المكتبة سليمة"],
   [L("mh_greet", "greeting", "السجلات أمامي. أقرأ منها."),
    L("mh_gate", "reveal", "بوابة المكتبة تسجّل دخول كل بطاقة وزمنه، وللطاولات في الطابق الثاني نظام حجز يسجّل اسم الحاجز ومدته.", ["f_gate_exists", "f_seat_exists"]),
    L("mh_lost", "reveal", "مكتب الخدمات يسجّل كل غرض يُسلَّم إلينا من المفقودات، بوقته ومكان العثور عليه.", ["f_lostfound_exists"]),
    L("mh_unknown", "deflect_unknown", "هذا ليس في سجلاتي."),
    L("mh_off", "deflect_offtopic", "اسألني عن المكتبة وسجلاتها."),
    L("mh_bye", "farewell", "السجل يبقى كما هو.")])
ch("haitham", "هيثم المراكشي", "witness", "مشرف مختبر الهندسة",
   "حازم في تنظيم الاختبارات، يقرأ ما وقّعه ويذكر ما لا يعرفه. لا يتحدث عن الطلاب إلا بما سجّله.",
   ["أن يبقى الاختبار منظماً", "ألا يُنسب إلى المختبر ما لم يسجّله"],
   [L("ht_greet", "greeting", "أنا أشرف على الاختبار العملي. أجيب بما سجّلته."),
    L("ht_door", "reveal", "باب المختبر يسجّل بطاقة كل داخل وخارج، ويُغلق أثناء الاختبار من الثالثة إلى الثالثة وخمسين دقيقة.", ["f_lab_door_exists"]),
    L("ht_sheet", "reveal", "أنادي الحاضرين وأوقّع ورقة الحضور بيدي أثناء الاختبار.", ["f_lab_sheet_exists"]),
    L("ht_unknown", "deflect_unknown", "لا أعرف."),
    L("ht_off", "deflect_offtopic", "اسألني عن الاختبار."),
    L("ht_bye", "farewell", "ورقتي موقّعة، فاقرأها.")])

locations = [{"id": "loc_plaza", "name_ar": "ساحة الجامعة والنافورة", "description_ar": "ساحة مكشوفة فيها النافورة، وتغطيها نقطة وصول واحدة."},
             {"id": "loc_lab", "name_ar": "مختبر الهندسة", "description_ar": "قاعة الاختبار العملي، بابها يُغلق أثناء الاختبار."},
             {"id": "loc_library", "name_ar": "مكتبة الجامعة", "description_ar": "بوابة ببطاقات وطابق ثانٍ بطاولات تُحجز."},
             {"id": "loc_office", "name_ar": "مكتب الوسيط الطلابي", "description_ar": "حيث تُستقبل الشكاوى وتُجرى المقابلات الأولية."},
             {"id": "loc_network", "name_ar": "مركز الشبكة", "description_ar": "سجلات نقاط الوصول."}]
objects = [{"id": "obj_tablet", "name_ar": "جهاز يزن اللوحي", "description_ar": "جهاز بغلاف أزرق مخضر، غير مسجّل على شبكة الجامعة."}]
orgs = [{"id": "org_univ", "name_ar": "جامعة القنطرة", "description_ar": "جامعة خيالية في مدينة «القنطرة»."}]

# ---------------------------------------------------------------- facts
facts = []
def F(id, st, kind, subj, spoiler, time=None, loc=None, ko=None):
    d = {"id": id, "statement_ar": st, "kind": kind, "subject_ids": subj, "spoiler_level": spoiler}
    if time: d["time"] = time
    if loc: d["location_id"] = loc
    if ko: d["science_ko_refs"] = ko
    facts.append(d)
F("f_tablet_missing", "فُقد جهاز يزن اللوحي (غلافه أزرق مخضر) بعد عصر الثلاثاء.", "event", ["obj_tablet", "yazan"], 0)
F("f_yazan_claims", "يقول يزن إنه أعار الجهاز لكريم عند نافورة الجامعة قرابة الثالثة والعشر دقائق دون شاهد.", "attribute", ["yazan", "karim"], 0)
F("f_karim_denies", "ينكر كريم أنه استلم أي جهاز من يزن.", "attribute", ["karim"], 0)
F("f_complaint_details", "سجّل الوسيط من شكوى يزن ثلاث تفاصيل اعتبرها غير منشورة: النافورة، والغلاف الأزرق المخضر، ونحو الساعة 15:10.", "attribute", ["yazan"], 1, T(1150))
F("f_interview_neutral", "أسئلة المقابلة الأولية مع كريم كانت مفتوحة ولم تذكر النافورة ولا لون الغلاف ولا الساعة.", "relation", ["karim"], 1, T(1200), "loc_office", ["KO-RS-05-006", "KO-RS-05-011"])
F("f_karim_mentioned", "ذكر كريم النافورة من تلقاء نفسه في المقابلة الأولية صباح الأربعاء.", "event", ["karim"], 1, T(1200), "loc_office", ["KO-RS-05-009"])
F("f_post_public", "نشر يزن في مجموعة الصف الثلاثاء 17:48 أنه ترك الجهاز «مع صديق عند النافورة»، وظهر في قائمة المشاهدين اسم كريم 18:02.", "event", ["yazan", "karim"], 1, T(228), None, ["KO-RS-05-009"])
F("f_friend_msg", "كتب سامي لكريم الثلاثاء 18:30 يسأله إن كان قد أخذ جهاز يزن عند النافورة.", "event", ["sami", "karim"], 1, T(270))
F("f_chat_agreed", "اتفق يزن وكريم مساء الاثنين على احتمال استعارة الجهاز عند النافورة، وكتب كريم الثلاثاء 14:41 أنه لن يستطيع لأن لديه مختبراً.", "event", ["karim", "yazan"], 1, T(-1005))
F("f_karim_says_lab", "يقول كريم إنه كان في الاختبار العملي بمختبر الهندسة عصر الثلاثاء.", "attribute", ["karim"], 0)
F("f_yazan_memory", "يذكر يزن أنه سلّم الجهاز وهو ينظر إلى هاتفه، وأنه ظن أن المستلم كريم لأن كريم هو من طلب الجهاز.", "attribute", ["yazan"], 1)
F("f_backup_exists", "للجهاز اللوحي نسخة احتياطية سحابية في حساب يزن تحفظ سجل الشبكات التي اتصل بها.", "state", ["obj_tablet"], 1)
F("f_wifi_exists", "تسجّل شبكة الجامعة اقتران كل جهاز بنقطة وصول وزمنه بساعة الخادم، وللأجهزة غير المسجّلة معرّف قصير.", "state", ["org_univ"], 1, None, "loc_network")
F("f_gate_exists", "تسجّل بوابة المكتبة دخول كل بطاقة وزمنه.", "state", ["loc_library"], 1)
F("f_seat_exists", "يسجّل نظام حجز الطاولات في الطابق الثاني اسم الحاجز ومدة الحجز.", "state", ["loc_library"], 1)
F("f_lostfound_exists", "يسجّل مكتب الخدمات كل غرض يُسلَّم إليه من المفقودات بوقته ومكان العثور عليه.", "state", ["loc_library"], 1)
F("f_lab_door_exists", "يسجّل قارئ باب مختبر الهندسة كل دخول وخروج، ويُغلق الباب أثناء الاختبار العملي.", "state", ["loc_lab"], 1, None, "loc_lab")
F("f_lab_sheet_exists", "يوقّع مشرف المختبر ورقة حضور بيده بعد المناداة أثناء الاختبار.", "state", ["loc_lab"], 1, None, "loc_lab")
F("f_karim_elsewhere", "كان كريم في مختبر الهندسة من 14:58 إلى 16:41، فلم يكن عند النافورة قرابة 15:10.", "relation", ["karim", "loc_lab"], 3, T(58, "exact", 161), "loc_lab", ["KO-RS-05-004", "KO-RS-05-014"])
F("f_tablet_with_nour", "غادر الجهاز محيط النافورة مع نور ودخل معها المكتبة قرابة 15:40، فقد تسلّمته منذ التسليم عند النافورة.", "relation", ["obj_tablet", "nour"], 3, T(72, "exact", 104), "loc_library", ["KO-FC-04-024", "KO-RS-05-004"])
F("f_clock_skew", "ساعة الجهاز اللوحي متأخرة سبع دقائق عن ساعة الشبكة، فيتطابق 15:05 على الجهاز مع 15:12 على الخادم.", "relation", ["obj_tablet"], 2, T(72), None, ["KO-FC-04-024", "KO-RS-05-005"])
F("f_slip_innocent", "لذكر كريم كلمة النافورة طرق بريئة موثقة: المنشور العلني، ورسالة سامي، واتفاق الاثنين؛ وكلمة النافورة لم تعد غير منشورة قبل المقابلة.", "relation", ["karim"], 2, T(1200), None, ["KO-RS-05-009", "KO-RS-05-011"])
F("f_nour_took", "تسلّمت نور الجهاز من يزن عند النافورة قرابة 15:10 لتقرأ ملفاً، ونسيته على الطاولة 14 في المكتبة.", "event", ["nour", "obj_tablet"], 3, T(70, "approx"), "loc_plaza")

claims = [
    {"id": "cl_yazan_karim", "statement_ar": "سلّمت الجهاز لكريم عند النافورة.", "kind": "honest_mistake", "held_by": ["yazan"], "true_fact_id": "f_tablet_with_nour",
     "contradicted_by_evidence_ids": ["ev_wifi_log", "ev_lab_door", "ev_lab_sheet"]},
    {"id": "cl_sami_rumour", "statement_ar": "كريم هو من أخذ الجهاز، فكل من في المجموعة يقول ذلك.", "kind": "rumour", "held_by": ["sami"], "true_fact_id": "f_karim_elsewhere",
     "contradicted_by_evidence_ids": ["ev_lab_door", "ev_lab_sheet"]},
    {"id": "cl_nour_returned", "statement_ar": "أعدت كل ما استعرته قبل دخولي المكتبة.", "kind": "honest_mistake", "held_by": ["nour"], "true_fact_id": "f_nour_took",
     "contradicted_by_evidence_ids": ["ev_lostfound", "ev_seat_booking"]},
]
timeline = [
    {"id": "te_chat", "description_ar": "يزن وكريم يتبادلان رسائل عن احتمال الاستعارة عند النافورة.", "time": T(-1005), "location_id": None, "actor_ids": ["yazan", "karim"], "fact_ids": ["f_chat_agreed"], "motivated_by_ar": "أراد كريم استعارة الجهاز"} ,
    {"id": "te_cancel", "description_ar": "كريم يكتب ليزن أنه لن يستطيع اللقاء بسبب المختبر.", "time": T(41), "actor_ids": ["karim"], "fact_ids": ["f_chat_agreed"], "motivated_by_ar": "لديه اختبار عملي ولا يريد أن ينتظره يزن"},
    {"id": "te_lab", "description_ar": "كريم داخل مختبر الهندسة في الاختبار العملي.", "time": T(58, "exact", 161), "location_id": "loc_lab", "actor_ids": ["karim"], "fact_ids": ["f_karim_elsewhere"], "motivated_by_ar": "حضور الاختبار العملي"},
    {"id": "te_handover", "description_ar": "يزن يسلّم الجهاز لنور عند النافورة.", "time": T(70, "approx"), "location_id": "loc_plaza", "actor_ids": ["yazan", "nour"], "fact_ids": ["f_nour_took"], "motivated_by_ar": "طلبت نور قراءة ملف على الجهاز قبل محاضرتها"},
    {"id": "te_tablet_plaza", "description_ar": "الجهاز يقترن بنقطة وصول الساحة بساعة الخادم.", "time": T(72), "location_id": "loc_plaza", "actor_ids": [], "fact_ids": ["f_clock_skew"]},
    {"id": "te_gate_nour", "description_ar": "نور تدخل بوابة المكتبة.", "time": T(98), "location_id": "loc_library", "actor_ids": ["nour"], "fact_ids": ["f_tablet_with_nour"], "motivated_by_ar": "أرادت القراءة قبل محاضرتها"},
    {"id": "te_tablet_2f", "description_ar": "الجهاز يقترن بنقطة المكتبة في الطابق الثاني.", "time": T(104), "location_id": "loc_library", "actor_ids": [], "fact_ids": ["f_tablet_with_nour"]},
    {"id": "te_found", "description_ar": "عاملة النظافة تسلّم الجهاز إلى مكتب الخدمات.", "time": T(215), "location_id": "loc_library", "actor_ids": [], "fact_ids": ["f_lostfound_exists"]},
    {"id": "te_post", "description_ar": "يزن ينشر في مجموعة الصف عن جهازه.", "time": T(228), "actor_ids": ["yazan"], "fact_ids": ["f_post_public"], "motivated_by_ar": "أراد مساعدة زملائه في العثور على الجهاز"},
    {"id": "te_interview", "description_ar": "المقابلة الأولية مع كريم وهو يذكر النافورة.", "time": T(1200), "location_id": "loc_office", "actor_ids": ["karim"], "fact_ids": ["f_karim_mentioned"], "motivated_by_ar": "حضر المقابلة بطلب من مكتب الوسيط"},
]
for t in timeline:
    if t.get("location_id") is None: t.pop("location_id", None)

# ---------------------------------------------------------------- evidence
ev = []
def V(id, title, kind, content, acts, supports, rel, limits, contradicts=None, red=False, ko=None, loc=None):
    d = {"id": id, "title_ar": title, "kind": kind, "content_ar": content, "acquired_by_action_ids": acts, "supports_fact_ids": supports, "reliability": rel, "limits_ar": limits}
    if contradicts: d["contradicts_claim_ids"] = contradicts
    if red: d["is_red_herring"] = True
    if ko: d["forensic_ko_ref"] = ko
    if loc: d["location_id"] = loc
    ev.append(d)
V("ev_complaint", "شكوى يزن وقائمة التفاصيل", "documentary",
  "مكتب الوسيط الطلابي — شكوى يزن العلي — الأربعاء 09:10\nالجهاز: لوحي بغلاف أزرق مخضر\nالنص: «أعرت الجهاز لكريم الصباغ عند نافورة الجامعة قرابة الثالثة والعشر دقائق عصر الثلاثاء. لا شاهد.»\nسجل الوسيط قبل المقابلة (تفاصيل افترض أنها غير منشورة): النافورة · لون الغلاف · الساعة 15:10",
  ["a_read_complaint"], ["f_complaint_details", "f_yazan_claims"], "moderate",
  "ادعاء صاحب الشكوى وقائمة كتبها الوسيط بافتراض أن التفاصيل لم تُنشر؛ لم تُراجع القائمة مقابل المنشورات العامة قبل وضعها.", red=True, loc="loc_office")
V("ev_interview_note", "محضر المقابلة الأولية مع كريم", "documentary",
  "محضر مقابلة — الأربعاء 10:00 — الحاضرون: الوسيط وكريم الصباغ\nأسئلة الوسيط بحروفها: «ماذا فعلت عصر الثلاثاء؟» ثم «هل تحدثت مع يزن في ذلك اليوم؟» ثم «هل تريد أن تضيف شيئاً؟»\nأجوبة كريم المختصرة: «كنت في الاختبار العملي. لم أستلم شيئاً من يزن، ولم أقف عند النافورة ذلك اليوم.»\nلم يُمارَس أي ضغط ولم يُعرض عليه أي تفصيل من الشكوى.",
  ["a_read_note"], ["f_interview_neutral", "f_karim_mentioned"], "strong",
  "يسجّل ما قيل وبماذا سُئل، ولا يبيّن لماذا قال كريم كلمة النافورة. كتبه الوسيط نفسه، فلا يُغني عن مقارنة أسئلته بالقائمة.", ko="KO-RS-05-011", loc="loc_office")
V("ev_group_post", "منشور يزن في مجموعة الصف", "digital",
  "مجموعة صف السنة الثانية — منشور يزن العلي — الثلاثاء 17:48\n«ضاع جهازي اللوحي. تركته مع صديق عند النافورة عصراً، ولا أجد الصديق ولا الجهاز. هل رآه أحد؟»\nشاهد المنشور 14 عضواً، منهم: ك. الصباغ 18:02 · س. القاسم 18:10",
  ["a_get_post"], ["f_post_public"], "strong",
  "يثبت أن الكلمة كانت معلنة في المجموعة منذ مساء الثلاثاء، أي قبل الشكوى بأكثر من خمس عشرة ساعة، وأن اسم كريم بين المشاهدين؛ ولا يثبت أنه قرأ المنشور فعلاً أو تذكره.", loc="loc_office")
V("ev_friend_msg", "رسالة سامي إلى كريم", "digital",
  "لقطة من هاتف كريم — رسالة خاصة من س. القاسم — الثلاثاء 18:30\n«قرأت منشور يزن. هل أنت من أخذ جهازه عند النافورة؟ كنتما تتكلمان عنه أمس.»\nرد كريم 18:41: «لا.»",
  ["a_get_friend"], ["f_friend_msg"], "moderate",
  "لقطة من جهاز كريم نفسه وبموافقته؛ تثبت أن اسم النافورة وصله من صديق ثالث، لا ما فعله عصر الثلاثاء.", loc="loc_office")
V("ev_chat_log", "محادثة يزن وكريم", "digital",
  "محادثة خاصة (نسخة من هاتف يزن بموافقته)\nالاثنين 21:15 — يزن: «تريد استعارة الجهاز غداً؟»\nالاثنين 21:20 — كريم: «نعم، نلتقي عند النافورة بعد المحاضرة؟»\nالاثنين 21:22 — يزن: «اتفقنا، نحو الثالثة.»\nالثلاثاء 14:41 — كريم: «لن أستطيع، سأكون في المختبر. أطلبه يوماً آخر.» (وصلت 14:41، قُرئت 18:50)",
  ["a_get_chat"], ["f_chat_agreed"], "strong",
  "سجل مراسلة لا يثبت أين كان أحد؛ يبيّن اتفاقاً مسبقاً على مكان وإلغاءً مكتوباً لم يقرأه يزن إلا مساءً.", loc="loc_office")
V("ev_wifi_log", "سجل اقتران الأجهزة بنقاط الوصول", "digital",
  "مركز الشبكة — سجل الاقتران — الثلاثاء (بتوقيت ساعة الخادم)\nD-77A0 هاتف (مسجّل: ي. العلي): نقطة الساحة 15:02–15:16 · نقطة المباني الإنسانية 15:21–17:05\nD-3F21 هاتف (مسجّل: ن. السعيد): نقطة الساحة 15:08–15:30 · نقطة المكتبة (الطابق الثاني) 15:40–17:32\nD-91C4 هاتف (مسجّل: ك. الصباغ): نقطة مختبر الهندسة 14:55–16:42\nD-5B08 جهاز لوحي (غير مسجّل، بلا اسم): نقطة الساحة 15:12–15:30 · نقطة المكتبة (الطابق الثاني) 15:44–17:20\nملاحظة: نقطة الساحة تغطي الساحة والنافورة ولا تغطي مدخل المكتبة.",
  ["a_get_wifi"], ["f_wifi_exists", "f_karim_elsewhere"], "strong",
  "يسجّل أين اقترنت الأجهزة بالشبكة لا من حملها، ولا يسمّي الجهاز اللوحي؛ والهاتف قد يكون بعيداً عن صاحبه. وقت الخادم مرجعه ساعة الخادم.", loc="loc_network")
V("ev_tablet_history", "سجل الشبكات في نسخة الجهاز الاحتياطية", "digital",
  "نسخة احتياطية سحابية — الجهاز اللوحي (حساب يزن)\nمعرّف الجهاز ينتهي بـ 5B08\nالشبكات المتصلة حديثاً (بساعة الجهاز):\nنقطة الساحة — 15:05 إلى 15:23\nنقطة المكتبة (الطابق الثاني) — 15:37 إلى 17:13\nحالة الساعة: الضبط التلقائي معطل؛ آخر مزامنة مع خادم الوقت قبل 9 أيام؛ الفرق عند آخر فحص: الجهاز متأخر 7 دقائق",
  ["a_get_history"], ["f_backup_exists", "f_clock_skew"], "moderate",
  "يصف الجهاز نفسه بساعته هو، وساعته غير مضبوطة تلقائياً؛ والفرق المكتوب (7 دقائق) قيس قبل أيام وقد لا يكون ثابتاً.", red=True, loc="loc_office")
V("ev_lab_norm", "تقرير توحيد الأزمنة", "lab_result",
  "تقرير مختبر الأزمنة: بعد إضافة سبع دقائق لساعة الجهاز اللوحي المتأخرة يتوافق سجله مع سجل الخادم عند 15:12، فمسارا الاتصال بالساحة ثم بالمكتبة هما نفسهما. أي أن الفارق بين 15:05 و15:12 فرق ساعة لا فرق واقعة، وأن الجهاز D-5B08 هو جهاز يزن.",
  ["a_compare_times"], ["f_clock_skew", "f_tablet_with_nour"], "strong",
  "نتيجة حسابية تعتمد على صحة الانحراف المكتوب في النسخة الاحتياطية؛ توحّد الأزمنة وتربط الجهاز بالمعرّف، ولا تقول من حمله.", ko="KO-FC-04-024", loc="loc_network")
V("ev_gate_log", "سجل بوابة المكتبة", "digital",
  "مكتبة الجامعة — سجل بوابة الدخول (البطاقات) — الثلاثاء\n15:38 دخول: ن. السعيد\n15:41 دخول: بطاقة زائر (غير مسمّاة)\n16:45 دخول: ك. الصباغ\n17:05 دخول: س. القاسم\nلا قيد دخول لـ ي. العلي في هذا اليوم.",
  ["a_get_gate"], ["f_gate_exists"], "strong",
  "يسجّل دخول البطاقات لا ما يحمله الداخل ولا الخروج، وتدخل البطاقة الزائرة دون اسم.", red=True, loc="loc_library")
V("ev_seat_booking", "نظام حجز طاولات القراءة", "digital",
  "نظام حجز الطاولات — الطابق الثاني — الثلاثاء\nالطاولة 14: محجوزة 15:40–17:30 باسم ن. السعيد\nلا حجز باسم ك. الصباغ أو ي. العلي في هذا اليوم.",
  ["a_get_seat"], ["f_seat_exists", "f_tablet_with_nour"], "strong",
  "يثبت من حجز الطاولة، لا من جلس عليها فعلاً ولا ما وُضع عليها.", loc="loc_library")
V("ev_lostfound", "سجل المفقودات في مكتب الخدمات", "documentary",
  "مكتب خدمات المكتبة — سجل المفقودات — الثلاثاء 17:35\nاستلمنا من عاملة النظافة جهازاً لوحياً بغلاف أزرق مخضر، عُثر عليه فوق الطاولة رقم 14 في الطابق الثاني بعد انتهاء الحجز 17:30. الجهاز مقفل ولا اسم عليه، وُضع في خزانة المفقودات.\nصباح الأربعاء: لم يُطالَب به بعد.\nالتوقيع: م. الحلبي",
  ["a_get_lost"], ["f_lostfound_exists", "f_tablet_with_nour"], "strong",
  "يثبت أين وُجد الجهاز ومتى سُلِّم، لا من تركه هناك ولا متى وُضع على الطاولة.", loc="loc_library")
V("ev_lab_door", "سجل قارئ باب مختبر الهندسة", "digital",
  "مختبر الهندسة — قارئ البطاقات — الثلاثاء\n14:58 دخول: ك. الصباغ\n16:41 خروج: ك. الصباغ\nملاحظة النظام: الباب مغلق أثناء الاختبار العملي 15:00–15:50، ولا خروج مسجّل لأي بطاقة في هذه الفترة.",
  ["a_get_labdoor"], ["f_lab_door_exists", "f_karim_elsewhere"], "strong",
  "يسجّل مرور بطاقة لا شخصاً، وقد تُعار البطاقة؛ قوته أنه يتفق مع ورقة بخط المشرف لا تعتمد على الجهاز.", loc="loc_lab")
V("ev_lab_sheet", "ورقة حضور الاختبار العملي", "documentary",
  "مختبر الهندسة — ورقة حضور الاختبار العملي للدوائر — الثلاثاء\nالمناداة والتوقيع بخط المشرف: 15:30\nالحاضرون: ك. الصباغ ✓ · (12 اسماً آخر)\nملاحظة المشرف بخطه: «لم يغادر أحد القاعة أثناء الاختبار»\nالتوقيع: هـ. المراكشي",
  ["a_get_labsheet"], ["f_lab_sheet_exists", "f_karim_elsewhere"], "strong",
  "ورقة بخط المشرف تثبت الحضور وقت المناداة 15:30 وتؤيد غياب الخروج؛ لا تغطي ما قبل المناداة بالدقيقة.", loc="loc_lab")
V("ev_karim_statement", "إفادة كريم (ملخص)", "testimonial",
  "ملخص إفادة كريم الصباغ:\n«كنت في الاختبار العملي حتى بعد الرابعة. لم أستلم شيئاً. قلت كلمة النافورة ولا أذكر لماذا. تحدثنا أنا ويزن مساء الاثنين عن لقاء ثم ألغيته.»",
  ["a_note_karim"], ["f_karim_says_lab", "f_karim_mentioned"], "weak",
  "إفادة صاحب الشأن عن نفسه؛ تُقاس بسجلات لا تعتمد عليه، ولا يدل ارتباكه ولا هدوؤه على صدقه.", loc="loc_office")
V("ev_yazan_statement", "إفادة يزن (ملخص)", "testimonial",
  "ملخص إفادة يزن العلي:\n«سلّمت الجهاز عند النافورة نحو 15:10 وأنا أنظر إلى هاتفي. ظننت أن المستلم كريم لأنه طلب الجهاز قبلها بيوم. لا شاهد عندي.»",
  ["a_note_yazan"], ["f_yazan_memory"], "weak",
  "ذاكرة صادقة لكنها تخلط بين من طلب الجهاز ومن تسلّمه؛ يلزمها سجل لا يعتمد عليها.", loc="loc_office")
V("ev_nour_statement", "إفادة نور (ملخص)", "testimonial",
  "ملخص إفادة نور السعيد:\n«أخذت جهاز يزن من يديه عند النافورة نحو 15:10 لأقرأ ملفاً قبل محاضرتي. دخلت المكتبة وغادرت دون أن آخذه معي من الطاولة 14. أكتم إشعارات مجموعة الصف فلم أقرأ منشوره.»",
  ["a_note_nour"], ["f_nour_took"], "moderate",
  "إفادة اعتراف بفعل بحسن نية؛ يؤيدها حجز الطاولة وسجل المفقودات، ولا تغني عنهما.", loc="loc_office")

# ---------------------------------------------------------------- inferences
def P(t, i): return {"ref_type": t, "ref_id": i}
inf = []
def I(id, prem, ct, concl, rel, strength, rule, ks):
    inf.append({"id": id, "premises": prem, "conclusion": {"ref_type": ct, "ref_id": concl}, "relation": rel, "strength": strength, "rule_ar": rule, "skill_ko_refs": ks})
E = lambda x: P("evidence", x)
Fa = lambda x: P("fact", x)
# --- clock reconciliation (two reliable clocks)
I("i_clock", [E("ev_tablet_history"), E("ev_lab_norm")], "fact", "f_clock_skew", "establishes", "strong",
  "ساعة الجهاز متأخرة سبع دقائق بحسب نسخته الاحتياطية؛ وبعد التصحيح يتطابق مساراه مع سجل الخادم، فاختلاف 15:05 و15:12 اختلاف ساعتين لا اختلاف واقعتين.", ["KO-FC-04-024", "KO-RS-05-005"])
# --- key fact 1: Karim elsewhere (two independent chains)
I("i_a_elsewhere", [E("ev_wifi_log"), E("ev_lab_norm")], "fact", "f_karim_elsewhere", "establishes", "strong",
  "هاتف كريم مقترن بنقطة مختبر الهندسة من 14:55 إلى 16:42 بساعة الخادم، بينما الجهاز اللوحي المنسوب إليه التسليم يقترن بنقطة الساحة 15:12؛ فهاتفه لم يكن في الساحة.", ["KO-RS-05-004", "KO-FC-04-024"])
I("i_b_elsewhere", [E("ev_lab_door"), E("ev_lab_sheet")], "fact", "f_karim_elsewhere", "establishes", "strong",
  "قارئ الباب يضع بطاقته داخل المختبر المغلق من 14:58، وورقة المشرف بخطه تضعه حاضراً عند المناداة 15:30 وتقول إن أحداً لم يغادر؛ وهما مصدران لا يشتركان في جهاز ولا في كاتب.", ["KO-RS-05-004", "KO-RS-05-014"])
# --- key fact 2: the tablet went with Nour (two independent chains)
I("i_a_nour", [E("ev_wifi_log"), E("ev_lab_norm"), E("ev_gate_log")], "fact", "f_tablet_with_nour", "establishes", "strong",
  "الجهاز D-5B08 المربوط بجهاز يزن يقترن بنقطة الساحة مع هاتف نور، ثم ينتقل إلى نقطة المكتبة بعد دخول بطاقتها البوابة 15:38 بست دقائق، ولا يقترن بجهاز كريم؛ فالجهاز تحرّك معها.", ["KO-FC-04-024", "KO-RS-05-004"])
I("i_b_nour", [E("ev_lostfound"), E("ev_seat_booking")], "fact", "f_tablet_with_nour", "establishes", "strong",
  "الجهاز وُجد على الطاولة 14، والطاولة 14 محجوزة باسم نور 15:40–17:30؛ مصدران من نظامين مختلفين في المكتبة لا علاقة لأحدهما بشبكة الجامعة.", ["KO-RS-05-004"])
# --- the slip: innocent routes (two independent routes)
I("i_slip_a", [E("ev_group_post"), E("ev_complaint"), E("ev_interview_note")], "fact", "f_slip_innocent", "establishes", "strong",
  "المنشور العلني 17:48 سبق الشكوى، فالنافورة لم تعد من التفاصيل غير المنشورة؛ وكريم بين المشاهدين، ولم تذكر أسئلة الوسيط النافورة، فيبقى مصدر الكلمة إما المنشور وإما غيره من الطرق البريئة.", ["KO-RS-05-009", "KO-RS-05-011"])
I("i_slip_b", [E("ev_chat_log"), E("ev_friend_msg")], "fact", "f_slip_innocent", "establishes", "strong",
  "اتفاق الاثنين كان على النافورة مكاناً للقاء، ورسالة سامي ذكرتها لكريم قبل المقابلة؛ فالكلمة وصلت إليه بطريقين آخرين غير حضوره.", ["KO-RS-05-009"])
I("i_took", [E("ev_nour_statement"), E("ev_seat_booking")], "fact", "f_nour_took", "establishes", "strong",
  "إفادة نور تعترف بأنها تسلّمت الجهاز، وحجز الطاولة وسجل المفقودات يضعان الجهاز عند طاولتها؛ فالاعتراف هنا موافق لسجلات مستقلة وليس هو الأساس.", ["KO-RS-05-009", "KO-RS-05-014"])
# --- claims
I("i_cl_yazan", [Fa("f_tablet_with_nour"), Fa("f_karim_elsewhere")], "claim", "cl_yazan_karim", "contradicts_claim", "strong",
  "مسار الجهاز مع نور وغياب كريم عن الساحة يبيّنان أن المستلم غير كريم؛ ويفسّر خطأ يزن في الاسم أنه سلّم الجهاز وهو ينظر إلى هاتفه وأن كريم من طلبه قبلها.", ["KO-RS-05-014", "KO-RS-05-008"])
I("i_cl_sami", [Fa("f_karim_elsewhere")], "claim", "cl_sami_rumour", "contradicts_claim", "strong",
  "تكرار الناس لقول لا يزيده وزناً؛ وكريم كان في مختبر مغلق وقت التسليم المزعوم.", ["KO-RS-06-020", "KO-RS-05-004"])
I("i_cl_nour", [E("ev_lostfound"), E("ev_seat_booking")], "claim", "cl_nour_returned", "contradicts_claim", "strong",
  "الجهاز وُجد على طاولتها بعد انتهاء حجزها؛ فظنها أنها أعادته لا يوافق السجلات.", ["KO-RS-05-014"])
# --- hypotheses (every rule-out rests on the two key facts, so each proof path refutes every false hypothesis)
I("i_support_nour", [Fa("f_tablet_with_nour"), Fa("f_karim_elsewhere")], "hypothesis", "h_nour", "supports", "strong",
  "الجهاز تحرّك مع نور من الساحة إلى المكتبة وكريم كان في المختبر؛ فالتسليم عند النافورة كان لها، وفسّر السجلان معاً سبب خلط يزن.", ["KO-RS-06-007"])
I("i_rule_karim", [Fa("f_karim_elsewhere"), Fa("f_tablet_with_nour")], "hypothesis", "h_karim", "rules_out", "conclusive",
  "من كان في مختبر مغلق وقت التسليم لا يمكن أن يستلم الجهاز في الساحة، والجهاز نفسه تحرّك مع شخص آخر؛ فكلمته عن النافورة لا تغيّر ذلك.", ["KO-RS-06-008"])
I("i_rule_invented", [Fa("f_tablet_with_nour"), Fa("f_karim_elsewhere")], "hypothesis", "h_invented", "rules_out", "strong",
  "الجهاز غادر الساحة مع شخص آخر بينما كان هاتف يزن يتجه إلى مبنى آخر، فحدث تسليم فعلاً؛ وخطأ يزن في اسم المستلم لا يجعل القصة مختلقة.", ["KO-RS-06-008", "KO-RS-05-008"])
I("i_rule_clock", [Fa("f_karim_elsewhere"), Fa("f_tablet_with_nour")], "hypothesis", "h_clock", "rules_out", "strong",
  "مساران لا يشتركان في مصدر، أحدهما شبكي وجهازي والآخر سجلات المكتبة والمختبر، يصلان إلى النتيجة نفسها؛ فاختلاف الساعتين لا يبطل السجلات بل يُصحَّح بانحراف معلوم.", ["KO-RS-06-008", "KO-RS-05-004"])
I("i_rule_clock_2", [Fa("f_clock_skew"), E("ev_lostfound")], "hypothesis", "h_clock", "rules_out", "suggestive",
  "بعد تصحيح السبع دقائق يتفق مسار الجهاز مع سجل المفقودات الذي ينتهي عند الطاولة 14؛ فالتناقض الظاهر في الدقائق لا يغيّر الترتيب.", ["KO-RS-06-008"])

# ---------------------------------------------------------------- character knowledge
K = lambda f, a="witnessed", c="certain": {"fact_id": f, "access": a, "certainty": c}
ck = [
    {"character_id": "yazan", "knows": [K("f_post_public"), K("f_backup_exists"), K("f_yazan_memory", "witnessed", "fairly_sure")], "hides": [], "believes": [{"claim_id": "cl_yazan_karim", "stance": "sincere"}]},
    {"character_id": "karim", "knows": [K("f_karim_says_lab"), K("f_chat_agreed"), K("f_karim_mentioned", "witnessed", "unsure")], "hides": [], "believes": []},
    {"character_id": "nour", "knows": [], "hides": [{"fact_id": "f_nour_took", "reveal_when": {"presented": {"evidence_id": "ev_seat_booking", "to_character": "nour"}}, "cover_claim_id": None, "reveal_line_id": "nr_took"}],
     "believes": [{"claim_id": "cl_nour_returned", "stance": "sincere"}]},
    {"character_id": "sami", "knows": [K("f_friend_msg")], "hides": [], "believes": [{"claim_id": "cl_sami_rumour", "stance": "sincere"}]},
    {"character_id": "waleed", "knows": [K("f_wifi_exists", "professional")], "hides": [], "believes": []},
    {"character_id": "maha", "knows": [K("f_gate_exists", "professional"), K("f_seat_exists", "professional"), K("f_lostfound_exists", "professional")], "hides": [], "believes": []},
    {"character_id": "haitham", "knows": [K("f_lab_door_exists", "professional"), K("f_lab_sheet_exists")], "hides": [], "believes": []},
]
hyps = [
    {"id": "h_karim", "statement_ar": "استلم كريم الجهاز من يزن عند النافورة ثم أنكر ذلك.", "is_true": False, "plausibility_at_start": "high", "suspect_id": "karim"},
    {"id": "h_invented", "statement_ar": "لم يُعر يزن الجهاز لأحد عند النافورة، فقصته غير صحيحة.", "is_true": False, "plausibility_at_start": "medium", "suspect_id": "yazan"},
    {"id": "h_nour", "statement_ar": "سلّم يزن الجهاز لنور لا لكريم، فدخلت به المكتبة ونسيته على طاولة، دون قصد من أحد.", "is_true": True, "plausibility_at_start": "low", "suspect_id": "nour"},
    {"id": "h_clock", "statement_ar": "اختلاف ساعة الجهاز عن ساعة الشبكة بسبع دقائق يعني أن السجلات متضاربة فلا يُعتمد على أي منها.", "is_true": False, "plausibility_at_start": "medium"},
]
mis = [
    {"id": "rh_slip", "points_to_hypothesis_id": "h_karim", "planted_via_ar": "كريم ذكر النافورة من تلقاء نفسه، وكانت في قائمة التفاصيل التي افترض الوسيط أنها غير منشورة.", "evidence_ids": ["ev_complaint", "ev_interview_note"],
     "refuted_by_inference_ids": ["i_slip_a", "i_slip_b", "i_rule_karim"],
     "fairness_note_ar": "منشور المجموعة ورسالة سامي ومحادثة الاثنين كلها متاحة للاعب، وتوقيت المنشور يسبق الشكوى؛ والزلة وحدها لا تُدين ولا يُطلب من اللاعب الإيقاع بأحد."},
    {"id": "rh_gate", "points_to_hypothesis_id": "h_karim", "planted_via_ar": "كريم دخل المكتبة 16:45، أي قبل العثور على الجهاز في الطابق الثاني بنحو ساعة.", "evidence_ids": ["ev_gate_log"],
     "refuted_by_inference_ids": ["i_rule_karim", "i_a_nour", "i_b_nour"],
     "fairness_note_ar": "الجهاز كان على طاولة نور منذ 15:44 بحسب سجل الشبكة وحجز الطاولة، أي قبل دخول كريم بساعة؛ ودخوله لاحقاً لا يربطه بالجهاز."},
    {"id": "rh_clock", "points_to_hypothesis_id": "h_invented", "planted_via_ar": "ساعة الجهاز تضع اتصاله بالساحة 15:05، قبل ما يقوله يزن عن التسليم 15:10، فيبدو أن روايته غير دقيقة.", "evidence_ids": ["ev_tablet_history"],
     "refuted_by_inference_ids": ["i_clock", "i_rule_clock", "i_rule_invented"],
     "fairness_note_ar": "النسخة الاحتياطية نفسها تذكر أن الجهاز متأخر سبع دقائق وأن الضبط التلقائي معطل، فكل ما يلزم للتصحيح بين يدي اللاعب."},
    {"id": "rh_chat", "points_to_hypothesis_id": "h_karim", "planted_via_ar": "الاتفاق على اللقاء عند النافورة يجعل حضور كريم عندها محتملاً.", "evidence_ids": ["ev_chat_log"],
     "refuted_by_inference_ids": ["i_rule_karim", "i_slip_b"],
     "fairness_note_ar": "المحادثة نفسها تتضمن إلغاء كريم المكتوب قبل الموعد، والتصحيح الزمني ينقض الاحتمال."},
]
los = [
    {"id": "lo_claim", "statement_ar": "يعامل الاعتراف والادعاء والزلة ادعاءات تحتاج تأييداً مستقلاً.", "skill_ko_ref": "KO-RS-05-009", "observable_behaviors_ar": ["يصنّف الإفادات أقوالاً", "لا يعدّ الزلة إدانة"], "evidence_sources": ["evidence_board"]},
    {"id": "lo_interview", "statement_ar": "يفحص ما إذا كان التفصيل ما زال غير منشور ويتحقق من حياد أسئلة المقابلة.", "skill_ko_ref": "KO-RS-05-011", "observable_behaviors_ar": ["يقابل قائمة التفاصيل بالمنشورات", "يقرأ أسئلة المقابلة نفسها"], "evidence_sources": ["evidence_board", "final_justification"]},
    {"id": "lo_indep", "statement_ar": "يتحقق من استقلال الأدلة ويقدّم مسارين لا يشتركان في مصدر.", "skill_ko_ref": "KO-RS-05-004", "observable_behaviors_ar": ["يميز بين سجلات الشبكة والمكتبة والمختبر"], "evidence_sources": ["evidence_board", "final_justification"]},
    {"id": "lo_timeline", "statement_ar": "يوحّد الأزمنة بانحراف معلوم ويرتّب الأحداث على خط زمني واحد.", "skill_ko_ref": "KO-FC-04-024", "observable_behaviors_ar": ["يشغّل مختبر الأزمنة بانحراف صحيح", "يضع الأدلة في أزمنتها"], "evidence_sources": ["timeline_task", "action_log"]},
    {"id": "lo_hyp", "statement_ar": "يوازن بين فرضيتين على الأقل ويستبعد ما تنقضه الأدلة.", "skill_ko_ref": "KO-RS-05-002", "observable_behaviors_ar": ["يضيف فرضيات", "يستبعد بدليل"], "evidence_sources": ["hypothesis_ledger"]},
    {"id": "lo_diag", "statement_ar": "يقدّر ما يثبته كل سجل وما لا يثبته ويربطه بالفرضية باتجاه صحيح.", "skill_ko_ref": "KO-RS-06-001", "observable_behaviors_ar": ["يربط الدليل بالفرضية"], "evidence_sources": ["evidence_board", "final_justification"]},
    {"id": "lo_calib", "statement_ar": "يصوغ نسبة الترجيح بحدودها.", "skill_ko_ref": "KO-RS-06-021", "observable_behaviors_ar": ["يختار ثقة معقولة", "يذكر حدوداً"], "evidence_sources": ["final_justification"]},
    {"id": "lo_revise", "statement_ar": "يراجع رأيه الأول حين يظهر ما يخالفه.", "skill_ko_ref": "KO-RS-06-009", "observable_behaviors_ar": ["يغيّر فرضيته الرائدة بدليل"], "evidence_sources": ["hypothesis_ledger"]},
]
def levels(d): return [{"score": i, "descriptor_ar": t} for i, t in enumerate(d)]
rub = {
    "reference_answer_ar": "لا دليل على أن كريم استلم الجهاز. كلمة «النافورة» التي قالها نُشرت علناً قبل الشكوى، ووصلته أيضاً برسالة صديق وباتفاق سابق، فهي لا تدل على حضوره. كان كريم في اختبار مغلق بمختبر الهندسة وقت التسليم المزعوم بشهادة قارئ الباب وورقة المشرف وسجل الشبكة. أما الجهاز اللوحي فاقترن بنقطة الساحة مع هاتف نور ثم انتقل إلى نقطة المكتبة بعد دخول بطاقتها، ووُجد على طاولتها المحجوزة. واختلاف الدقائق بين ساعة الجهاز وساعة الخادم انحراف معلوم قدره سبع دقائق. حدود الاستنتاج: لا تبيّن السجلات ماذا قال يزن ونور بالضبط عند التسليم، ولا تثبت أن هاتف كريم كان في يده، وإفادة نور تؤيد السجلات ولا تقوم مقامها.",
    "criteria": [
        {"id": "c_source", "name_ar": "تصنيف المصادر", "objective_ids": ["lo_claim"], "scored_by": "deterministic", "weight": 0.15, "levels": levels(["لم يصنّف", "أخطأ في الأغلب", "نصف صحيح", "معظمه صحيح", "كله صحيح"])},
        {"id": "c_conflict", "name_ar": "توحيد الأزمنة وترتيبها", "objective_ids": ["lo_timeline"], "scored_by": "deterministic", "weight": 0.2, "levels": levels(["لم يوحّد شيئاً", "وحّد قليلاً", "وحّد نصفها", "معظمها", "كلها في موضعها"])},
        {"id": "c_links", "name_ar": "ربط الأدلة بالفرضيات", "objective_ids": ["lo_diag", "lo_indep"], "scored_by": "deterministic", "weight": 0.2, "levels": levels(["لا روابط", "قليلة", "نصفها صحيح", "معظمها", "كلها دقيقة"])},
        {"id": "c_uncertainty", "name_ar": "معايرة الثقة", "objective_ids": ["lo_calib"], "scored_by": "deterministic", "weight": 0.15, "levels": levels(["ثقة مفرطة", "حدود قليلة", "جزئية", "معقولة", "معايَرة كاملة"])},
        {"id": "c_revision", "name_ar": "مراجعة الرأي", "objective_ids": ["lo_revise"], "scored_by": "deterministic", "weight": 0.1, "levels": levels(["بقي على فرضية مرفوضة", "لم يعلن فرضية", "ثبت على فرضية سليمة", "غيّر بدليل", "غيّر بدليل ووثّق"])},
        {"id": "c_elimination", "name_ar": "استبعاد الفرضيات الخاطئة", "objective_ids": ["lo_hyp"], "scored_by": "deterministic", "weight": 0.1, "levels": levels(["لم يستبعد", "استبعد خطأً", "فرضية بدليل", "فرضيتين", "كل الخاطئة"])},
        {"id": "c_justification", "name_ar": "جودة الحجة المكتوبة", "objective_ids": ["lo_interview", "lo_hyp"], "scored_by": "human", "weight": 0.1, "levels": levels(["لا حجة", "ادعاء بلا سند", "أدلة دون ربط", "ربط الأدلة بالاستنتاج", "ربط مع الطرق البريئة والحدود"])},
    ],
}
def H(id, lv, kind, text, trig, target=None, w=0.0):
    d = {"id": id, "level": lv, "kind": kind, "text_ar": text, "trigger": trig, "assessment_weight": w}
    if target: d["targets_inference_id"] = target
    return d
he = lambda e: {"has_evidence": e}
hints = [
    H("hg1", 1, "metacognitive", "حين يقول أحدهم كلمة لم تتوقعها، اسأل أولاً: من أين يمكن أن تكون وصلته بغير حضوره؟", {"always": True}, None, 0.02),
    H("hg2", 2, "focus_area", "قارن قائمة «التفاصيل غير المنشورة» بتوقيت كل منشور ورسالة قبل المقابلة: هل ما زالت كلها غير منشورة؟", he("ev_interview_note"), None, 0.04),
    H("hg3", 3, "pointer", "ابحث عن سجلات لا يكتبها يزن ولا كريم: شبكة، وبوابات، وأوراق مشرفين.", he("ev_complaint"), None, 0.08),
    H("hc1", 1, "metacognitive", "هل ساعتان تذكران وقتين مختلفين تعنيان وقعتين مختلفتين أم ساعتين مختلفتين؟", he("ev_tablet_history"), "i_clock", 0.02),
    H("hc2", 2, "pointer", "اقرأ في نسخة الجهاز الاحتياطية سطر حالة الساعة، ثم أدخل الانحراف في المختبر.", he("ev_tablet_history"), "i_clock", 0.06),
    H("hc3", 3, "partial_reveal", "استعمل مختبر الأزمنة: فرق التوقيت 0 للجهازين، وانحراف الجهاز اللوحي +7 دقائق لأن ساعته متأخرة.", he("ev_wifi_log"), "i_clock", 0.1),
    H("hn1", 1, "metacognitive", "من يملك سجلاً يضع الجهاز في مكان غير الساحة بعد الثالثة؟", he("ev_lostfound"), "i_b_nour", 0.02),
    H("hn2", 2, "pointer", "اسأل: لمن حُجزت الطاولة التي وُجد عليها الجهاز؟", he("ev_lostfound"), "i_b_nour", 0.06),
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
Act("a_read_complaint", "examine", "اقرأ شكوى يزن وقائمة التفاصيل", al, [G("ev_complaint")], "loc_office", "READ_COMPLAINT")
Act("a_read_note", "examine", "اقرأ محضر المقابلة الأولية مع كريم", al, [G("ev_interview_note")], "loc_office", "READ_NOTE")
for cid, lab in [("yazan", "يزن"), ("karim", "كريم"), ("nour", "نور"), ("sami", "سامي"), ("waleed", "وليد"), ("maha", "مها"), ("haitham", "هيثم")]:
    Act(f"a_int_{cid}", "interview", f"ابدأ مقابلة {lab}", al, [{"op": "raise_trust", "ref_id": cid, "amount": 1}], cid, f"INT_{cid.upper()}")
Act("a_get_post", "examine", "اطلب منشور يزن في مجموعة الصف", fu("f_post_public"), [G("ev_group_post")], "loc_office", "GET_POST")
Act("a_get_friend", "examine", "اطلب لقطة رسالة سامي من هاتف كريم", fu("f_friend_msg"), [G("ev_friend_msg")], "loc_office", "GET_FRIEND")
Act("a_get_chat", "examine", "اطلب نسخة محادثة يزن وكريم", fu("f_chat_agreed"), [G("ev_chat_log")], "loc_office", "GET_CHAT")
Act("a_get_wifi", "examine", "اطلب سجل اقتران الأجهزة من مركز الشبكة", fu("f_wifi_exists"), [G("ev_wifi_log")], "loc_network", "GET_WIFI")
Act("a_get_history", "examine", "اطلب سجل الشبكات من النسخة الاحتياطية للجهاز", fu("f_backup_exists"), [G("ev_tablet_history")], "loc_office", "GET_HISTORY")
Act("a_get_gate", "examine", "اطلب سجل بوابة المكتبة", fu("f_gate_exists"), [G("ev_gate_log")], "loc_library", "GET_GATE")
Act("a_get_seat", "examine", "اطلب سجل حجز طاولات القراءة", fu("f_seat_exists"), [G("ev_seat_booking")], "loc_library", "GET_SEAT")
Act("a_get_lost", "examine", "اطلب سجل المفقودات في مكتب الخدمات", fu("f_lostfound_exists"), [G("ev_lostfound")], "loc_library", "GET_LOST")
Act("a_get_labdoor", "examine", "اطلب سجل قارئ باب مختبر الهندسة", fu("f_lab_door_exists"), [G("ev_lab_door")], "loc_lab", "GET_LABDOOR")
Act("a_get_labsheet", "examine", "اطلب ورقة حضور الاختبار العملي", fu("f_lab_sheet_exists"), [G("ev_lab_sheet")], "loc_lab", "GET_LABSHEET")
Act("a_note_karim", "examine", "دوّن إفادة كريم", fu("f_karim_says_lab"), [G("ev_karim_statement")], "karim", "NOTE_KARIM")
Act("a_note_yazan", "examine", "دوّن إفادة يزن", fu("f_yazan_memory"), [G("ev_yazan_statement")], "yazan", "NOTE_YAZAN")
Act("a_note_nour", "examine", "دوّن إفادة نور", fu("f_nour_took"), [G("ev_nour_statement")], "nour", "NOTE_NOUR")
Act("a_compare_times", "compare_evidence", "وحِّد الأزمنة (يُمنح عبر المختبر عند نجاحه)", {"all": [he("ev_tablet_history"), he("ev_wifi_log")]}, [G("ev_lab_norm")], None, "COMPARE_TIMES")
Act("p_seat_nour", "present_evidence", "اعرض سجل حجز الطاولة على نور", {"presented": {"evidence_id": "ev_seat_booking", "to_character": "nour"}}, [{"op": "emit_event", "ref_id": "PRESENTED_SEAT"}], "nour", "P_SEAT_NOUR", 0)
Act("a_hint", "request_hint", "اطلب تلميحاً", al, [], None, "REQUEST_HINT", 0)
Act("a_accuse", "final_accusation", "قدّم الرأي المعلّل النهائي", al, [{"op": "emit_event", "ref_id": "SUBMIT"}], None, "FINAL_ACCUSATION", 0)

topics = [
    {"id": "t_post", "label_ar": "ما نُشر في المجموعة", "example_questions_ar": ["ماذا نشرت في المجموعة؟", "هل ذكرت لون الغلاف أو الساعة؟"], "fact_ids": ["f_post_public"]},
    {"id": "t_backup", "label_ar": "النسخة الاحتياطية للجهاز", "example_questions_ar": ["هل للجهاز نسخة احتياطية؟", "ماذا تحفظ؟"], "fact_ids": ["f_backup_exists"]},
    {"id": "t_memory", "label_ar": "كيف سلّمت الجهاز", "example_questions_ar": ["كيف سلّمت الجهاز؟", "كيف عرفت من استلمه؟"], "fact_ids": ["f_yazan_memory"], "claim_ids": ["cl_yazan_karim"]},
    {"id": "t_whereabouts", "label_ar": "أين كنت عصر الثلاثاء", "example_questions_ar": ["أين كنت عصر الثلاثاء؟", "ماذا فعلت بعد الظهر؟"], "fact_ids": ["f_karim_says_lab"]},
    {"id": "t_arrangement", "label_ar": "الاتفاق على اللقاء", "example_questions_ar": ["هل تحدثت مع يزن عن الجهاز؟", "ماذا كتبتما؟"], "fact_ids": ["f_chat_agreed"]},
    {"id": "t_fountain", "label_ar": "كلمة النافورة في المقابلة", "example_questions_ar": ["لماذا ذكرت النافورة؟"], "fact_ids": ["f_karim_mentioned"]},
    {"id": "t_taken", "label_ar": "ما حدث عند النافورة", "example_questions_ar": ["هل تسلّمت شيئاً عند النافورة؟", "ماذا فعلت بعد ذلك؟"], "fact_ids": ["f_nour_took"], "claim_ids": ["cl_nour_returned"]},
    {"id": "t_message", "label_ar": "الرسالة إلى كريم", "example_questions_ar": ["ماذا كتبت لكريم؟", "ماذا سمعت؟"], "fact_ids": ["f_friend_msg"]},
    {"id": "t_rumour", "label_ar": "ما يقوله الناس", "example_questions_ar": ["ماذا يقول الناس عن كريم؟"], "fact_ids": [], "claim_ids": ["cl_sami_rumour"]},
    {"id": "t_network", "label_ar": "سجلات الشبكة", "example_questions_ar": ["ماذا تسجّل الشبكة؟", "هل تسجّل الأجهزة غير المسجّلة؟"], "fact_ids": ["f_wifi_exists"]},
    {"id": "t_library_records", "label_ar": "سجلات المكتبة", "example_questions_ar": ["ماذا يسجّل البوابة والحجز؟"], "fact_ids": ["f_gate_exists", "f_seat_exists"]},
    {"id": "t_lostfound", "label_ar": "المفقودات", "example_questions_ar": ["كيف تسجّلون المفقودات؟"], "fact_ids": ["f_lostfound_exists"]},
    {"id": "t_lab_records", "label_ar": "سجلات المختبر", "example_questions_ar": ["كيف تثبتون حضور الطلاب؟", "ماذا يسجّل الباب؟"], "fact_ids": ["f_lab_door_exists", "f_lab_sheet_exists"]},
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
    (1, "اختلاف 15:05 و15:12 هو اختلاف ساعتين: الجهاز متأخر سبع دقائق بنص نسخته الاحتياطية، وبعد التصحيح يتطابق مساراه مع سجل الخادم.", ["ev_tablet_history", "ev_wifi_log", "ev_lab_norm"], "i_clock"),
    (2, "مسار الشبكة: الجهاز اللوحي يقترن بنقطة الساحة مع هاتف نور، ثم ينتقل إلى نقطة المكتبة بعد دخول بطاقتها البوابة، ولا أثر لهاتف كريم هناك.", ["ev_wifi_log", "ev_lab_norm", "ev_gate_log"], "i_a_nour"),
    (3, "المسار المستقل: الجهاز وُجد على الطاولة 14 بعد انتهاء الحجز، والحجز باسم نور؛ سجلان من نظامين في المكتبة لا علاقة لهما بالشبكة.", ["ev_lostfound", "ev_seat_booking"], "i_b_nour"),
    (4, "كريم في المختبر: هاتفه مقترن بنقطة المختبر طوال الفترة، وبطاقته داخل الباب المغلق، وورقة المشرف بخطه توقّع حضوره 15:30.", ["ev_wifi_log", "ev_lab_door", "ev_lab_sheet"], "i_b_elsewhere"),
    (5, "الزلة: كلمة «النافورة» نُشرت علناً قبل الشكوى، وأسئلة الوسيط لم تذكرها؛ فلا تدل على حضور كريم.", ["ev_group_post", "ev_complaint", "ev_interview_note"], "i_slip_a"),
    (6, "طريقان آخران إلى الكلمة نفسها: اتفاق الاثنين على النافورة مكاناً للقاء، ورسالة صديق ثالث قبل المقابلة.", ["ev_chat_log", "ev_friend_msg"], "i_slip_b"),
    (7, "كريم خارج الاحتمال: من كان في مختبر مغلق لا يستلم الجهاز في الساحة، والجهاز تحرّك مع آخر.", ["ev_lab_door", "ev_lab_sheet", "ev_lostfound", "ev_seat_booking"], "i_rule_karim"),
    (8, "إفادة نور لا تُعدّ دليل الإثبات، بل تؤيد سجلات سبقتها: الجهاز على طاولتها وهي لم تقصد أن تتركه.", ["ev_nour_statement", "ev_seat_booking"], "i_took"),
]
ending = {
    "steps": [{"order": o, "text_ar": t, "uses_evidence_ids": u, "inference_id": i} for o, t, u, i in steps],
    "alternative_paths_ar": [
        "يمكن إثبات أن الجهاز مع نور وأن كريم في المختبر من سجل الشبكة بعد توحيد الأزمنة وسجل البوابة وحدها، دون سجلات المكتبة والمختبر.",
        "ويمكن إثباتهما من سجل المفقودات وحجز الطاولة وقارئ باب المختبر وورقة المشرف وحدها، دون سجل الشبكة؛ والأقوى أن يتفق المساران.",
    ],
    "what_evidence_could_not_show_ar": [
        "لا تبيّن السجلات ما قيل بالضبط بين يزن ونور عند النافورة، ولا لماذا سُلِّم الجهاز لها دون أن يلاحظ يزن من هي.",
        "لا يثبت قارئ الباب ولا سجل الشبكة أن الهاتف أو البطاقة كانا بيد صاحبهما؛ قوتهما أنهما يتفقان مع ورقة بخط المشرف.",
        "لا نعرف لماذا ذكر كريم كلمة النافورة تحديداً في المقابلة؛ يكفي أن لها ثلاثة طرق بريئة موثقة.",
    ],
    "science_notes_ar": [
        "الزلة وحدها لا تُدين: كلمة لم تتوقعها من أحد تفتح باب البحث عن طرقها البريئة ولا تغلق القضية. وقبل أن تعتمد قائمة «تفاصيل غير منشورة» أعد فحصها مقابل كل ما نُشر.",
        "لا خيار في هذه القضية لخداع من تقابله أو الإيقاع به؛ المقابلة الجيدة هادئة وأسئلتها مفتوحة، ويُفحص نص السؤال نفسه كي لا يكون هو مصدر التسرب.",
        "ساعتان صادقتان قد تذكران وقتين مختلفين لأن لكل جهاز انحرافه؛ اقرأ مرجع كل ساعة ثم قارن، فالتضارب الظاهر يزول بالتصحيح ولا يبطل السجل.",
        "الاستقلال بالآلية لا بالعدد: سجل الشبكة وسجل المكتبة وورقة المشرف أنظمة لا يشترك أحدها في مصدر مع غيره، ولذلك يقوى الاستنتاج حين تتفق.",
        "يزن لم يكذب ولا كريم؛ الذاكرة خلطت بين من طلب الجهاز ومن تسلّمه. وإصلاح الضرر هنا ودّي: الجهاز في مكتب المفقودات، ويُسأل الجميع عن أسلم طريقة لتسليم الأشياء بين الأصدقاء.",
        "بطاقة الأصل: القضية أصلية من ATHAR، وبنيتها مستلهمة من خبر تراثي منسوب في سؤال الصديق عن «الشجرة» (نسبته مختلف فيها).",
    ],
}
core = {
    "schema_version": "0.1.0", "case_id": CID, "case_version": "0.1.0",
    "meta": {"title_ar": "هل بلغ صاحبك النافورة؟", "title_en": "Did Your Friend Reach the Fountain?", "age_band": "16-18", "locale": "ar", "dialogue_register": "msa", "estimated_minutes": 40, "difficulty": 4,
             "content_flags": ["no_violence", "missing_person"], "authors": ["فريق أثر التحريري (مسودة بمساعدة الذكاء الاصطناعي، لم تُراجَع بشرياً بعد)"],
             "knowledge_object_refs": ["KO-RS-05-009", "KO-RS-05-011", "KO-RS-05-004", "KO-FC-04-024", "KO-RS-05-005", "KO-RS-05-002", "KO-RS-06-001", "KO-RS-06-021", "KO-RS-06-009", "KO-RS-05-006"]},
    "premise": {"hook_ar": "طالب يقول إنه أعار زميله جهازه عند النافورة، والزميل ينكر. وفي المقابلة الهادئة يقول الزميل كلمة لم يُسأل عنها.",
                "player_role_ar": "أنت وسيط طلابي في جامعة القنطرة، وطُلب منك رأي معلّل في شكوى فقدان جهاز لوحي، دون اتهام أحد قبل أن تثبت السجلات شيئاً.",
                "setting_ar": "جامعة القنطرة، من مساء الاثنين إلى صباح الأربعاء. أوقات الشبكة والمكتبة والمختبر بساعة الجامعة، أما الأجهزة فلكل منها ساعته.",
                "public_fact_ids": ["f_tablet_missing", "f_yazan_claims", "f_karim_denies"],
                "assumed_general_knowledge_ar": ["ساعة الجهاز قد تختلف عن ساعة الخادم", "التوتر في المقابلة لا يدل على كذب", "ما نُشر علناً لا يعود تفصيلاً سرياً"]},
    "entities": {"characters": chars, "locations": locations, "objects": objects, "organizations": orgs},
    "truth": {"solution": {"culprit_ids": ["nour"], "summary_ar": "لم يستلم كريم الجهاز. سلّم يزن جهازه لنور عند النافورة، فدخلت به المكتبة ونسيته على طاولتها دون قصد، وخلط يزن بينها وبين كريم الذي كان قد طلب الجهاز. وكلمة النافورة جاءت كريم من المنشور العلني والرسالة والاتفاق السابق.", "key_fact_ids": ["f_karim_elsewhere", "f_tablet_with_nour"]},
              "facts": facts, "claims": claims},
    "timeline": timeline, "evidence": ev, "evidence_graph": {"inferences": inf},
    "character_knowledge": ck, "hypotheses": hyps, "misdirection_plan": mis, "learning_objectives": los,
    "mechanics": {"time_budget_units": 50, "actions": A},
    "state_machine": {"id": "c021", "initial": "briefing", "type": "compound", "states": {
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
    "clock": {"epoch_hhmm": "14:00", "zone_label_ar": "ساعة الجامعة (الخادم)"},
    "cover": {"title_ar": "هل بلغ صاحبك النافورة؟", "tagline_ar": "كلمة واحدة قالها المنكِر… فهل تكفي؟", "kicker_ar": "الملف الحادي والعشرون · المقابلة والسجل", "glyph": "◎", "accent": "cyan"},
    "cold_open_ar": ["الأربعاء، بعد المقابلة الأولى.", "قال يزن إنه أعار جهازه اللوحي لكريم عند نافورة الجامعة، دون شاهد. أنكر كريم، وفي إجابته وردت كلمة «النافورة» دون أن يسأله أحد عنها.",
                     "قائمة الوسيط تقول إن النافورة من التفاصيل غير المنشورة. ومن حولك من يهمس بأن الأمر محسوم.",
                     "قبل أي حكم: من أين يمكن أن تكون الكلمة وصلته؟ وما السجل الذي لا يملكه يزن ولا كريم؟"],
    "labs": [{
        "id": "lab_skew", "type": "time_normalizer", "title_ar": "مختبر توحيد الأزمنة",
        "intro_ar": "لكل جهاز ساعته. أدخل لكل سجل فرق التوقيت عن ساعة الجامعة بالساعات، وانحراف الساعة بالدقائق إن عُرف (موجب إن كانت الساعة متأخرة). حين تتطابق الأزمنة ضمن دقيقتين يصدر التقرير.",
        "tolerance_min": 2, "epoch_utc_minute_of_day": 840, "day_labels_ar": ["الثلاثاء"],
        "grants_evidence_on_converge": "ev_lab_norm",
        "items": [
            {"evidence_id": "ev_tablet_history", "label_ar": "الجهاز اللوحي — اتصاله بنقطة الساحة", "day": 0, "hhmm": "15:05", "basis_ar": "الوقت بساعة الجهاز نفسه"},
            {"evidence_id": "ev_wifi_log", "label_ar": "سجل الخادم — اقتران الجهاز D-5B08 بنقطة الساحة", "day": 0, "hhmm": "15:12", "basis_ar": "الوقت بساعة الخادم"},
        ],
    }],
    "source_classes": [
        {"id": "primary_record", "label_ar": "سجل أصلي", "help_ar": "يُنتجه نظام أو شخص لحظة الحدث دون وسيط، كسجل بوابة أو شبكة أو ورقة مشرف."},
        {"id": "redisplay", "label_ar": "نسخة معروضة", "help_ar": "معلومة أُعيد عرضها أو نُقلت عن جهاز آخر، كلقطة شاشة أو نسخة احتياطية تتأثر بساعة جهازها."},
        {"id": "claim", "label_ar": "قول أو تصريح", "help_ar": "إفادة أو شكوى أو رسالة؛ تُقاس بالسجلات لا بنبرة صاحبها."},
        {"id": "template", "label_ar": "قالب أو نموذج", "help_ar": "نص جاهز لا يصف الحدث الفعلي بذاته."},
        {"id": "public_document", "label_ar": "وثيقة منشورة", "help_ar": "وثيقة معلنة ومعروف ناشرها."}],
    "limit_menu": [
        {"id": "l_unknown_handover", "label_ar": "السجلات لا تبيّن ما قيل بين يزن ونور عند التسليم"},
        {"id": "l_phone_card", "label_ar": "الهاتف والبطاقة قد لا يكونان بيد صاحبهما، وقوة السجلات في اتفاقها مع ورقة المشرف"},
        {"id": "l_why_word", "label_ar": "لا نعرف لماذا ذكر كريم كلمة النافورة تحديداً، ويكفي أن لها طرقاً بريئة موثقة"},
        {"id": "l_invalid_slip", "label_ar": "ذكر كريم للنافورة من تلقاء نفسه يدل على أنه كان هناك"},
        {"id": "l_invalid_nervous", "label_ar": "توتر كريم في المقابلة يدل على أنه يخفي شيئاً"},
        {"id": "l_invalid_crowd", "label_ar": "اتفاق أكثر الطلاب على أن كريم هو الفاعل يرجّح ذلك"}],
    "mind_change_menu": [
        {"id": "m_karim_phone", "label_ar": "ظهور دليل على أن كريم غادر المختبر قبل 15:50 أو أن بطاقته كانت بيد غيره"},
        {"id": "m_tablet_other", "label_ar": "ظهور سجل يربط الجهاز اللوحي بشخص غير نور في المكتبة"},
        {"id": "m_skew_wrong", "label_ar": "ثبوت أن انحراف ساعة الجهاز ليس سبع دقائق"},
        {"id": "m_popular", "label_ar": "كثرة من يرددون رواية يزن"}],
    "transfer": {
        "id": "tr_room_code", "title_ar": "اختبار نقل المهارة: رمز القاعة",
        "scenario_ar": "ذكر طالب رمز قاعة «B12» أثناء مقابلة هادئة، وقال الوسيط إن الرمز لم يُنشر. أمامك وثيقتان من واقعة خيالية لا علاقة لها بالقضية.",
        "documents": [
            {"title_ar": "جدول القاعات المعلن", "body_ar": "الجدول العام على لوحة الأخبار منذ الأحد: القاعة B12 — امتحان الكيمياء — الثلاثاء 10:00."},
            {"title_ar": "محضر المقابلة", "body_ar": "سؤال الوسيط: «ماذا فعلت صباح الثلاثاء؟» جواب الطالب: «كنت أبحث عن القاعة B12 فلم أجدها.»"}],
        "prompt_ar": "اختر الخطوات التي تصلح لتقدير ما يعنيه ذكر الطالب للرمز (يمكنك اختيار أكثر من خطوة).",
        "options": [
            {"id": "o1", "text_ar": "التحقق مما إذا كان الرمز منشوراً علناً قبل المقابلة"},
            {"id": "o2", "text_ar": "قراءة نص أسئلة الوسيط للتأكد أنها لم تتضمن الرمز"},
            {"id": "o3", "text_ar": "البحث عن سجل مستقل يضع الطالب في المكان المعني أو خارجه"},
            {"id": "o4", "text_ar": "إدراج طرق بريئة يمكن أن يعرف بها الرمز"},
            {"id": "o5", "text_ar": "اعتبار ذكر الرمز اعترافاً"},
            {"id": "o6", "text_ar": "الإلحاح على الطالب بأسئلة موحية حتى يغيّر جوابه"},
            {"id": "o7", "text_ar": "الحكم بحسب توتر الطالب أثناء الكلام"}],
        "free_text_prompt_ar": "اكتب في ثلاثة أسطر كيف تقرّر نسبة الترجيح بأن الطالب كان في القاعة المعنية.",
    },
    "skills": [{"skill_id": "KO-RS-05-009", "track": "B"}, {"skill_id": "KO-RS-05-011", "track": "B"}, {"skill_id": "KO-RS-05-004", "track": "B"}, {"skill_id": "KO-FC-04-024", "track": "E"}, {"skill_id": "KO-RS-05-002", "track": "D"}],
    "stage_hooks_ar": {"briefing": "كلمة واحدة تكفي في نظر الجميع… فهل تكفي في نظر السجل؟", "investigating": "الزلة تفتح بابين: باب الشبهة، وباب الطرق البريئة.", "review": "قبل أن تغلق الملف: ما الذي لا يستطيع السجل أن يقوله؟", "resolved": "أُغلق الملف. الجهاز عاد إلى صاحبه، وبقي سؤال عن قنطرة أخرى."},
    "character_glyphs": {"yazan": "ي", "karim": "ك", "nour": "ن", "sami": "س", "waleed": "و", "maha": "م", "haitham": "هـ"},
}
sc = {
    "case_id": CID,
    "accepted_conclusions": {
        "h_nour": {"grade": 1, "note_ar": "استنتاج متسق مع الأدلة ويتطلب ذكر حدوده."},
        "h_karim": {"grade": 0, "note_ar": "يجعل الزلة إدانة، ويتجاهل أن الكلمة لها طرق بريئة وأن كريم كان في مختبر مغلق."},
        "h_invented": {"grade": 0, "note_ar": "خطأ في اسم المستلم لا يعني أن التسليم لم يحدث؛ سجلات الجهاز تؤكد حدوثه."},
        "h_clock": {"grade": 0, "note_ar": "الفرق انحراف ساعة معلوم يُصحَّح؛ لا يبطل السجلات."}},
    "confidence_band": {"h_nour": [65, 90], "h_karim": [0, 15], "h_invented": [0, 15], "h_clock": [0, 20]},
    "source_key": {"ev_complaint": "claim", "ev_interview_note": "primary_record", "ev_group_post": "primary_record", "ev_friend_msg": "redisplay", "ev_chat_log": "redisplay",
                   "ev_wifi_log": "primary_record", "ev_tablet_history": "redisplay", "ev_gate_log": "primary_record", "ev_seat_booking": "primary_record", "ev_lostfound": "primary_record",
                   "ev_lab_door": "primary_record", "ev_lab_sheet": "primary_record", "ev_karim_statement": "claim", "ev_yazan_statement": "claim", "ev_nour_statement": "claim"},
    "link_key": {
        "h_nour": {"ev_wifi_log": "supports", "ev_lab_norm": "supports", "ev_gate_log": "supports", "ev_seat_booking": "supports", "ev_lostfound": "supports", "ev_lab_door": "supports", "ev_lab_sheet": "supports",
                   "ev_nour_statement": "supports", "ev_chat_log": "neutral", "ev_group_post": "neutral"},
        "h_karim": {"ev_complaint": "supports", "ev_interview_note": "supports", "ev_chat_log": "supports", "ev_lab_door": "weakens", "ev_lab_sheet": "weakens", "ev_wifi_log": "weakens", "ev_lostfound": "weakens",
                    "ev_seat_booking": "weakens", "ev_group_post": "weakens", "ev_friend_msg": "weakens", "ev_gate_log": "supports"},
        "h_invented": {"ev_tablet_history": "supports", "ev_lab_norm": "weakens", "ev_wifi_log": "weakens", "ev_lostfound": "weakens"},
        "h_clock": {"ev_tablet_history": "supports", "ev_lab_norm": "weakens", "ev_lostfound": "weakens"},
    },
    "required_limits": ["l_unknown_handover", "l_phone_card"], "valid_mind_changers": ["m_karim_phone", "m_tablet_other", "m_skew_wrong"],
    "invalid_limits": ["l_invalid_slip", "l_invalid_nervous", "l_invalid_crowd"],
    "decisive_evidence": ["ev_wifi_log", "ev_lab_norm", "ev_gate_log", "ev_lostfound", "ev_seat_booking", "ev_lab_door", "ev_lab_sheet"],
    "lab_requirement": {"lab_id": "lab_skew", "must_converge": True},
    "timeline_requirement": [{"evidence_id": "ev_tablet_history", "utc_minute": 72, "tol": 3}, {"evidence_id": "ev_wifi_log", "utc_minute": 72, "tol": 3},
                             {"evidence_id": "ev_gate_log", "utc_minute": 98, "tol": 4}, {"evidence_id": "ev_lostfound", "utc_minute": 215, "tol": 6}, {"evidence_id": "ev_group_post", "utc_minute": 228, "tol": 6}],
    "refuted_hypotheses": ["h_karim", "h_invented", "h_clock"],
    "criteria_map": {"c_source": "source_typing", "c_conflict": "conflict_resolution", "c_links": "hypothesis_links", "c_uncertainty": "uncertainty", "c_revision": "revision", "c_elimination": "elimination", "c_justification": "justification_human"},
    "transfer_key": {"valid": ["o1", "o2", "o3", "o4"], "invalid": ["o5", "o6", "o7"]},
    "caps": {"no_citations_max": 45, "no_conflict_resolution_max": 65},
}
os.makedirs(OUT, exist_ok=True)
for suf, obj in [("", core), (".ui", ui), (".scoring", sc)]:
    with open(os.path.join(OUT, f"{CID}{suf}.json"), "w", encoding="utf8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
print("ok")
