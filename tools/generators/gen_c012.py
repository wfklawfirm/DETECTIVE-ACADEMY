#!/usr/bin/env python3
# Case c012 «العملة الأحدث من الوديعة» — adapted from heritage seed S-02 (pattern: the exhibit that is newer than its story; KO-NP-02H-002 anachronism + a broken
# chain of custody). Teaches: a date stamped on an object gives the EARLIEST moment it can have existed, not the moment it arrived; a seal that is intact
# now says nothing about earlier openings; opportunity is not guilt (the case ends with an institutional review, not a public shaming).
# Deviation from the seed: the grandmother is alive and handed the locker to her grandchildren (13-15 policy avoids death as a topic) — so "heirs" become "new holders".
# The person with the sole opportunity (the senior key holder) is recorded in culprit_ids; no confession: the case is closed by inference from records.
# Proof paths (each derives every key fact, rules out every false hypothesis):
#   A = coin photo + deposit contract + opening log + guard hire file + maintenance job sheet + custody form
#   B = mint bulletin + seal stock register + key register + vault door-card log
# Usage: gen_c012.py OUT_DIR
import json, sys, os
OUT = sys.argv[1]
CID = "c012_newer_coin"

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
ch("luay", "لؤي الحداد", "victim", "14 سنة، حفيد صاحبة الخزانة وأحد حامليها الجدد",
   "فضولي ومهذب، يريد أن يعرف ماذا حدث لسبائك جدته، ويميل إلى تصديق ما يردده الكبار عن الحارس الجديد.",
   ["أن يعرف أين ذهبت سبائك جدته", "ألا يُظلم أحد في الفرع بسبب ظن"],
   [L("ly_greet", "greeting", "أهلاً. جدتي تنازلت لنا عن الخزانة هذا الشهر، وعندما فتحناها وجدنا عملات بدل السبائك."),
    L("ly_silver", "reveal", "جدتي تقول إنها أودعت ست سبائك فضة صغيرة قبل اثنتي عشرة سنة، وهذا مكتوب في عقدها.", ["f_deposit_2014"]),
    L("ly_guard", "reveal", "الجميع في الفرع يقولون إن الحارس الليلي الجديد هو الفاعل، فهو الوحيد الغريب هنا.", None, ["cl_guard_stranger"]),
    L("ly_unknown", "deflect_unknown", "لا أعرف، كنت صغيراً عندما أودعت جدتي أغراضها."),
    L("ly_off", "deflect_offtopic", "رجاءً، لنعد إلى موضوع الخزانة."),
    L("ly_bye", "farewell", "شكراً لأنك تبحث عن الحقيقة قبل أن نحكم على أحد.")])
ch("bassam", "بسام العيسى", "witness", "موظف الخزائن الحالي في فرع المرسى",
   "حريص على الإجراءات ويقسم بما رآه بعينه، لكنه يعمّم ما رآه اليوم على ما جرى في الماضي.",
   ["أن يُثبت أن عمله سليم", "ألا يُنسب إلى الفرع إهمال في الحراسة"],
   [L("bs_greet", "greeting", "أقسم أنني فحصت الختم صباح اليوم أمام الحفيدين، وهو سليم."),
    L("bs_seal", "reveal", "الختم على الباب كما هو لم يُقطع ولم يُمسّ، فلا يمكن أن يكون أحد فتح الخزانة منذ الإيداع.", ["f_seal_checked"], ["cl_bassam_seal"]),
    L("bs_register", "reveal", "عندنا سجل لمخزون الأختام يدوّن رقم كل ختم وتاريخ تركيبه.", ["f_seal_register_exists"]),
    L("bs_unknown", "deflect_unknown", "هذا قبل مجيئي إلى الفرع."),
    L("bs_off", "deflect_offtopic", "اسألني عن الختم والإجراءات."),
    L("bs_bye", "farewell", "الإجراءات كلها مكتوبة، فاقرأها.")])
ch("nabil", "نبيل العمر", "suspect", "23 سنة، الحارس الليلي الجديد في الفرع",
   "متحمس وقليل الخبرة، يتكلم بسرعة حين يشعر أن الجميع يتهمه، ويكرر أنه لا يعرف الخزائن.",
   ["ألا يفقد عمله الجديد", "أن يُعرف أنه لم يقترب من غرفة الخزائن"],
   [L("nb_greet", "greeting", "أنا لم ألمس شيئاً. أحرس البوابة والممر فقط، واسألني عن عملي."),
    L("nb_start", "reveal", "باشرت العمل في الثاني من فبراير هذا العام، ومهمتي البوابة والممر الخارجي وجولة كل ساعتين.", ["f_guard_start"]),
    L("nb_key", "reveal", "سلّموني مفتاح باب الموظفين فقط، ولا أملك بطاقة لدخول غرفة الخزائن.", ["f_guard_key"]),
    L("nb_unknown", "deflect_unknown", "لا أعرف، لم أكن هنا حينها."),
    L("nb_off", "deflect_offtopic", "اسألني عن عملي في البوابة."),
    L("nb_bye", "farewell", "أرجو أن يعرفوا أنني لم أفعل شيئاً.")])
ch("sabri", "صبري المناصرة", "suspect", "موظف الخزائن الأقدم في الفرع، حامل المفتاح الاحتياطي",
   "وقور ومنظم الكلام، يستشهد بخبرته الطويلة، ويقلّل من شأن أي خروج عن الإجراء.",
   ["أن تبقى سمعته في الفرع سليمة", "أن تُغلق القضية دون مراجعة فتحة الصيانة"],
   [L("sb_greet", "greeting", "أعمل في هذه الخزائن منذ سنوات، وأعرف كل ما فيها من إجراءات."),
    L("sb_opened", "reveal", "نعم، فتحت الخزانة رقم 218 يوم أُجريت صيانة باب القفص أمامها.", ["f_sabri_opened"]),
    L("sb_short", "reveal", "فتحتها دقائق قليلة فقط لاختبار الباب بعد تغيير المفصلة، ثم أغلقتها وختمتها.", None, ["cl_sabri_short"]),
    L("sb_refuse", "refuse_secret", "قلت ما عندي عن تلك الفتحة، ولا أرى حاجة إلى المزيد."),
    L("sb_stayed", "reveal", "حسناً... بقيت في الغرفة أكثر مما قلت، حتى الثامنة وست وأربعين دقيقة، والمفتاح معي. لكنني لم أُخرج شيئاً من الخزانة.", ["f_sabri_stayed"]),
    L("sb_unknown", "deflect_unknown", "لا أذكر ذلك."),
    L("sb_off", "deflect_offtopic", "لنبقَ في موضوع الخزانة 218."),
    L("sb_bye", "farewell", "أرجو أن تُراجع السجلات بإنصاف.")])
ch("idris", "إدريس القاسم", "witness", "فني صيانة متعاقد مع الفرع",
   "عملي ودقيق، يكتب كل ما يخص أمر العمل ولا يخمّن في غير اختصاصه.",
   ["أن يبقى أمر العمل موثقاً بصورته الصحيحة"],
   [L("id_greet", "greeting", "أمر العمل عندي، وأقرأ منه ما كُلفت به فقط."),
    L("id_scope", "reveal", "كُلفت باستبدال مفصلة باب القفص أمام الخزانة 218، وانتهيت قبل الخامسة والنصف وسلّمت المكان للسيد صبري. لم أفتح الخزانة.", ["f_tech_scope"]),
    L("id_witness", "reveal", "أبلغت الفرع في أمر العمل بأن فتح الخزانة يلزمه شاهد ثانٍ، ولم يوقّع أحد.", ["f_witness_asked"]),
    L("id_unknown", "deflect_unknown", "ليس من اختصاصي."),
    L("id_off", "deflect_offtopic", "اسألني عن أمر العمل فقط."),
    L("id_bye", "farewell", "مع السلامة.")])
ch("sanaa", "سناء الفارس", "authority", "مديرة فرع المرسى وأمينة السجلات",
   "هادئة ورسمية، تعطي المحقق السجلات المتاحة وتشرح ما يعنيه كل سجل دون تأويل.",
   ["أن تُعرض السجلات كما هي", "أن تُراجع الإجراءات إن ثبت خلل"],
   [L("sn_greet", "greeting", "السجلات متاحة لك، وسأشرح لك ما يعنيه كل سجل ولا أفسّر ما لا يقوله."),
    L("sn_open", "reveal", "للخزائن سجل فتح يدوّن كل فتحة، وللأختام سجل مخزون يدوّن كل ختم ركّب.", ["f_open_log_exists", "f_seal_register_exists"]),
    L("sn_contract", "reveal", "عقد الخزانة 218 محفوظ، وفيه وصف المحتويات عند الإيداع في الثاني عشر من مارس 2014.", ["f_deposit_2014"]),
    L("sn_keys", "reveal", "للمفاتيح سجل عهدة، ولباب غرفة الخزائن سجل بطاقات إلكتروني.", ["f_key_register_exists", "f_door_log_exists"]),
    L("sn_custody", "reveal", "ولكل خزانة نموذج جرد وعهدة توقّع فيه الأطراف عند كل فتحة.", ["f_custody_form_exists"]),
    L("sn_unknown", "deflect_unknown", "ليس في السجلات."),
    L("sn_off", "deflect_offtopic", "اسألني عن سجلات الفرع."),
    L("sn_bye", "farewell", "سنراجع الإجراءات مهما كانت النتيجة.")])

locations = [{"id": "loc_vault", "name_ar": "غرفة الخزائن", "description_ar": "غرفة الخزائن وخزانة المفاتيح عند مدخلها."},
             {"id": "loc_office", "name_ar": "مكتب مديرة الفرع", "description_ar": "حيث تُحفظ السجلات والعقود."},
             {"id": "loc_gate", "name_ar": "بوابة الفرع والممر الخارجي", "description_ar": "منطقة عمل الحارس الليلي."}]
objects = [{"id": "obj_locker", "name_ar": "الخزانة رقم 218", "description_ar": "خزانة أمانات صغيرة عليها ختم يُستبدل عند كل فتح."},
           {"id": "obj_coins", "name_ar": "القطع التذكارية الست", "description_ar": "قطع فضية اللون وُجدت داخل الخزانة."}]
orgs = [{"id": "org_branch", "name_ar": "خزائن المرسى للأمانات", "description_ar": "مؤسسة خيالية لتأجير خزائن الأمانات في ميناء المرسى."},
        {"id": "org_mint", "name_ar": "دار سك المرسى", "description_ar": "دار خيالية تصدر قطعاً تذكارية."}]

# ---------------------------------------------------------------- facts
facts = []
def F(id, st, kind, subj, spoiler, time=None, loc=None, ko=None):
    d = {"id": id, "statement_ar": st, "kind": kind, "subject_ids": subj, "spoiler_level": spoiler}
    if time: d["time"] = time
    if loc: d["location_id"] = loc
    if ko: d["science_ko_refs"] = ko
    facts.append(d)
U0 = T(0, "unknown")
F("f_coins_found", "حين فتح الحفيدان الخزانة رقم 218 هذا الشهر وجدا ست قطع تذكارية بدل ست سبائك فضة صغيرة.", "event", ["obj_locker", "obj_coins", "luay"], 0)
F("f_clerk_swears", "يقسم موظف الخزائن بسام أن ختم الخزانة سليم لم يُمس.", "attribute", ["bassam", "obj_locker"], 0)
F("f_guard_suspected", "يشتبه كثيرون في الحارس الليلي الجديد.", "attribute", ["nabil"], 0)
F("f_deposit_2014", "أودعت صاحبة الخزانة ست سبائك فضة صغيرة في الثاني عشر من مارس 2014، وسُجّل ذلك في عقد الخزانة.", "event", ["obj_locker"], 1, U0)
F("f_coin_year", "تحمل القطع الست على حافتها سنة 2024 وعبارة «مئوية ميناء المرسى».", "state", ["obj_coins"], 1)
F("f_issue_date", "بدأ بيع مجموعة «مئوية ميناء المرسى» التذكارية في 20 مارس 2024 ولم تُسكّ قطعة منها قبل ذلك.", "event", ["obj_coins", "org_mint"], 1, U0)
F("f_coins_postdate", "القطع التذكارية لم تكن موجودة وقت الإيداع في 2014، فلا يصح أنها كانت في الخزانة منذئذ.", "relation", ["obj_coins", "obj_locker"], 2, U0, None, ["KO-NP-02H-002"])
F("f_seal_checked", "الختم الذي رآه بسام على الباب اليوم سليم غير مقطوع.", "state", ["bassam", "obj_locker"], 1)
F("f_seal_register_exists", "للفرع سجل مخزون أختام يدوّن رقم كل ختم وتاريخ تركيبه.", "state", ["org_branch"], 1)
F("f_seal_new", "الختم الحالي على الخزانة ركّب في 14 أغسطس 2024 وهو غير ختم الإيداع.", "relation", ["obj_locker"], 2, U0)
F("f_open_log_exists", "للفرع سجل يدوّن كل فتحة لكل خزانة.", "state", ["org_branch"], 1)
F("f_key_register_exists", "للفرع سجل عهدة للمفاتيح.", "state", ["org_branch"], 1)
F("f_door_log_exists", "لباب غرفة الخزائن سجل بطاقات إلكتروني.", "state", ["loc_vault"], 1)
F("f_custody_form_exists", "لكل خزانة نموذج جرد وعهدة يوقّعه الأطراف عند كل فتحة.", "state", ["org_branch"], 1)
F("f_maint_open", "فُتحت الخزانة 218 مرة واحدة منذ صدور القطع التذكارية: فتحة الصيانة في 14 أغسطس 2024.", "event", ["obj_locker", "sabri"], 2, T(35, "exact", 286), "loc_vault")
F("f_swap_at_maint", "استُبدلت محتويات الخزانة في فتحة الصيانة يوم 14 أغسطس 2024، لأنها الفتحة الوحيدة بعد صدور القطع.", "event", ["obj_locker", "obj_coins"], 3, T(35, "exact", 286), "loc_vault", ["KO-NP-02H-002"])
F("f_guard_start", "باشر الحارس نبيل العمل في 2 فبراير 2026، ومهامه البوابة والممر الخارجي وجولة كل ساعتين.", "event", ["nabil"], 1, U0, "loc_gate")
F("f_guard_key", "لا يملك الحارس نبيل إلا مفتاح باب الموظفين ولا بطاقة لدخول غرفة الخزائن.", "state", ["nabil"], 1)
F("f_guard_out", "الحارس نبيل التحق بعد فتحة الصيانة الوحيدة، ولا مفتاح له ولم تدخل بطاقته غرفة الخزائن، فلا فرصة له في التبديل.", "relation", ["nabil", "obj_locker"], 2, U0, None, ["KO-RS-05-007"])
F("f_guard_nervous", "بدا الحارس نبيل متوتراً أثناء أسئلة المحقق.", "attribute", ["nabil"], 1)
F("f_sabri_opened", "فتح صبري الخزانة 218 بنفسه يوم صيانة باب القفص.", "event", ["sabri", "obj_locker"], 1, T(35, "approx", 286), "loc_vault")
F("f_sabri_stayed", "بقي صبري في غرفة الخزائن حتى 20:46 والمفتاح الاحتياطي معه حتى 20:50.", "event", ["sabri"], 2, T(82, "exact", 290), "loc_vault")
F("f_tech_scope", "اقتصر عمل الفني إدريس على مفصلة باب القفص، وانصرف 17:22 دون أن يفتح الخزانة.", "event", ["idris", "loc_vault"], 1, T(38, "exact", 82), "loc_vault")
F("f_witness_asked", "طلب الفني في أمر العمل حضور شاهد ثانٍ عند فتح الخزانة ولم يوقّع أحد.", "event", ["idris"], 1, T(82), "loc_vault")
F("f_sabri_sole", "فتح حامل المفتاح الاحتياطي الخزانة في الصيانة بنفسه وبلا شاهد ثانٍ.", "relation", ["sabri", "obj_locker"], 2, T(35, "exact", 286), "loc_vault", ["KO-FC-04B-002"])
F("f_custody_gap", "لم يُجرَ جرد لمحتويات الخزانة ولم يُوقّع شاهد في فتحة الصيانة؛ انقطعت سلسلة العهدة عندها.", "relation", ["obj_locker"], 2, U0, None, ["KO-FC-04-026"])

claims = [
    {"id": "cl_guard_stranger", "statement_ar": "الحارس الجديد هو الوحيد الغريب في الفرع، فلا بد أنه الفاعل.", "kind": "rumour", "held_by": ["luay"], "true_fact_id": "f_guard_out", "contradicted_by_evidence_ids": ["ev_guard_hire", "ev_open_log", "ev_vault_door_log", "ev_key_register"]},
    {"id": "cl_bassam_seal", "statement_ar": "الختم سليم، فلا يمكن أن يكون أحد فتح الخزانة منذ الإيداع.", "kind": "honest_mistake", "held_by": ["bassam"], "true_fact_id": "f_seal_new", "contradicted_by_evidence_ids": ["ev_seal_register", "ev_seal_photo", "ev_deposit_receipt"]},
    {"id": "cl_sabri_short", "statement_ar": "فتحت الخزانة دقائق قليلة فقط لاختبار الباب.", "kind": "lie", "held_by": ["sabri"], "true_fact_id": "f_sabri_stayed", "contradicted_by_evidence_ids": ["ev_vault_door_log", "ev_key_register"]},
]
timeline = [
    {"id": "te_deposit", "description_ar": "الإيداع: ست سبائك فضة صغيرة، وتركيب الختم الأول.", "time": U0, "location_id": None, "actor_ids": [], "fact_ids": ["f_deposit_2014"]},
    {"id": "te_issue", "description_ar": "بدء بيع مجموعة «مئوية ميناء المرسى» التذكارية.", "time": U0, "actor_ids": [], "fact_ids": ["f_issue_date"]},
    {"id": "te_key_out", "description_ar": "صبري يخرج المفتاح الاحتياطي ويدخل غرفة الخزائن.", "time": T(35), "location_id": "loc_vault", "actor_ids": ["sabri"], "fact_ids": ["f_sabri_opened"], "motivated_by_ar": "كُلّف بمرافقة أمر الصيانة"},
    {"id": "te_tech", "description_ar": "الفني إدريس يستبدل مفصلة باب القفص.", "time": T(38, "exact", 82), "location_id": "loc_vault", "actor_ids": ["idris"], "fact_ids": ["f_tech_scope"], "motivated_by_ar": "أمر عمل الصيانة رقم 77"},
    {"id": "te_alone", "description_ar": "صبري وحده في غرفة الخزائن والخزانة مفتوحة، بلا جرد ولا شاهد ثانٍ.", "time": T(82, "exact", 280), "location_id": "loc_vault", "actor_ids": ["sabri"], "fact_ids": ["f_sabri_sole", "f_sabri_stayed", "f_custody_gap", "f_witness_asked"], "motivated_by_ar": "قال إنه يختبر باب الخزانة بعد تغيير المفصلة"},
    {"id": "te_seal", "description_ar": "تركيب الختم الجديد 9026 على الخزانة.", "time": T(280, "approx"), "location_id": "loc_vault", "actor_ids": ["sabri"], "fact_ids": ["f_seal_new"], "motivated_by_ar": "الإجراء يوجب تركيب ختم جديد عند كل فتح"},
    {"id": "te_key_back", "description_ar": "صبري يعيد المفتاح الاحتياطي ويوقّع.", "time": T(290), "location_id": "loc_office", "actor_ids": ["sabri"], "fact_ids": ["f_sabri_stayed"], "motivated_by_ar": "إغلاق دورة عهدة المفتاح"},
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
V("ev_coin_mint", "صورة القطع الست المكتشفة", "physical",
  "صورة مكبّرة لوجهي إحدى القطع الست:\nالوجه: «مئوية ميناء المرسى»\nالحافة: «2024»\nالوزن: نحو 8 غ لكل قطعة\nالمعدن: طلاء فضي اللون على قاعدة معدنية رخيصة\nالقطع الست متطابقة النقش",
  ["a_examine_coins"], ["f_coin_year"], "strong",
  "السنة المنقوشة تحدد أقدم زمن ممكن لوجود القطعة، لا زمن وضعها في الخزانة؛ ولا تدل على من وضعها.", loc="loc_vault")
V("ev_deposit_receipt", "عقد الخزانة رقم 218", "documentary",
  "عقد استئجار خزانة أمانات رقم 218 — فرع المرسى\nتاريخ العقد: 12/03/2014\nالمستأجرة: السيدة نوال الحداد\nوصف المحتويات المودعة (بخط الموظف وتوقيع المستأجرة): ست سبائك فضة صغيرة، وزن كل منها 50 غ\nالختم المركّب: 4471\nتوقيع الموظف المسؤول: ي. الرفاعي",
  ["a_read_contract"], ["f_deposit_2014"], "strong",
  "وصف كتبه الموظف عند الإيداع؛ لا يثبت وجود السبائك بذاتها ولا يغطي ما جرى بعد توقيع العقد.", loc="loc_office")
V("ev_open_log", "سجل فتح الخزانة 218", "documentary",
  "سجل فتح خزائن الأمانات — الخزانة 218 (نسخة الفرع)\n12/03/2014 — إيداع — بحضور المستأجرة\n04/05/2017 — زيارة — بحضور المستأجرة وموظف الخزائن\n19/06/2020 — زيارة — بحضور المستأجرة وموظف الخزائن\n08/11/2023 — زيارة — بحضور المستأجرة وموظف الخزائن\n14/08/2024 — فتح للصيانة — ص. المناصرة (حامل المفتاح الاحتياطي)\nلا فتحات مسجلة بعد ذلك حتى يوم الاكتشاف",
  ["a_get_open_log"], ["f_maint_open"], "strong",
  "يدوّن الفتحات المسجلة فقط؛ فتحة غير مسجلة لا تظهر فيه، ولا يبيّن ما دار داخل الخزانة.", loc="loc_office")
V("ev_mint_bulletin", "نشرة دار سك المرسى", "documentary",
  "نشرة دار سك المرسى (وثيقة منشورة)\nإصدار «مجموعة مئوية ميناء المرسى» — ست قطع تذكارية بطلاء فضي اللون\nبدء البيع في متجر الميناء: 20/03/2024\nلم تُسكّ أي قطعة من المجموعة قبل هذا التاريخ",
  ["a_read_bulletin"], ["f_issue_date"], "strong",
  "تؤرّخ لإصدار المجموعة لا لمن اشتراها ولا لمكان وضعها.", loc="loc_office")
V("ev_seal_register", "سجل مخزون الأختام", "documentary",
  "سجل مخزون الأختام وتركيبها — فرع المرسى (الخزانة 218)\n4471 — ركّب 12/03/2014 عند الإيداع\n4802 — ركّب 04/05/2017\n5530 — ركّب 19/06/2020\n6015 — ركّب 08/11/2023\n9026 — ركّب 14/08/2024 (فتح للصيانة) — مركّبه: ص. المناصرة\nلا ختم لاحق",
  ["a_get_seal_register"], ["f_seal_new", "f_maint_open"], "strong",
  "يدل على مواعيد استبدال الختم عند كل فتح؛ لا يدل على ما في الخزانة، ويصحّ فقط إن سُجّل كل ختم عند تركيبه.", contradicts=["cl_bassam_seal"], loc="loc_office")
V("ev_seal_photo", "صورة الختم الحالي", "physical",
  "صورة الختم على باب الخزانة 218: الرقم 9026، سليم غير مقطوع، وعليه تاريخ التركيب 14/08/2024.",
  ["a_photo_seal"], ["f_seal_checked", "f_seal_new"], "strong",
  "تثبت سلامة الختم الحالي منذ تركيبه؛ لا تثبت ما كان في الخزانة قبل تركيبه.", contradicts=["cl_bassam_seal"], loc="loc_vault")
V("ev_guard_hire", "ملف توظيف الحارس الليلي", "documentary",
  "ملف توظيف — الحارس الليلي نبيل العمر\nتاريخ المباشرة: 02/02/2026\nالمهام: بوابة الفرع والممر الخارجي وجولة كل ساعتين\nالمفاتيح المسلّمة: مفتاح باب الموظفين فقط\nلا صلاحية لدخول غرفة الخزائن",
  ["a_get_hire"], ["f_guard_start", "f_guard_key"], "strong",
  "يحدد ما أُسند إليه من مهام ومفاتيح؛ لا يثبت ما فعله فعلاً.", contradicts=["cl_guard_stranger"], loc="loc_office")
V("ev_vault_door_log", "سجل بطاقات باب غرفة الخزائن", "digital",
  "سجل بطاقات باب غرفة الخزائن (من نظام القفل الإلكتروني)\n14/08/2024 — 16:35 دخول: ص. المناصرة\n14/08/2024 — 16:38 دخول: إدريس (بطاقة زائر)\n14/08/2024 — 17:22 خروج: إدريس\n14/08/2024 — 20:46 خروج: ص. المناصرة\nمن 02/02/2026 إلى يوم الاكتشاف: لا دخول ببطاقة الحارس نبيل العمر",
  ["a_get_door_log"], ["f_sabri_stayed", "f_guard_key"], "strong",
  "يبيّن دخول البطاقات وخروجها لا ما فعله حاملها داخل الغرفة؛ وقد يدخل شخص خلف آخر دون مسح بطاقته.", contradicts=["cl_sabri_short"], ko="KO-FC-04-024", loc="loc_vault")
V("ev_key_register", "سجل عهدة المفاتيح", "documentary",
  "سجل عهدة المفاتيح — فرع المرسى\nالمفتاح الاحتياطي رقم 2 لخزائن القسم (ج): الحامل الدائم: ص. المناصرة\n14/08/2024 — خرج 16:35 — ص. المناصرة — عاد 20:50 — ص. المناصرة\nحاملو مفاتيح الغرفة: ص. المناصرة، ب. العيسى\nالحارس نبيل العمر غير مدرج",
  ["a_get_key_register"], ["f_sabri_stayed", "f_guard_key", "f_sabri_opened"], "strong",
  "سجل ورقي يملؤه حامل المفتاح نفسه؛ لا يثبت أن المفتاح لم يُنسخ.", contradicts=["cl_sabri_short"], loc="loc_office")
V("ev_job_sheet", "أمر عمل الصيانة رقم 77", "documentary",
  "أمر عمل صيانة رقم 77 — 14/08/2024\nالعمل: استبدال مفصلة باب القفص أمام الخزانة 218\nالفني: إدريس القاسم — بدأ 16:38 — أنهى 17:20\nنطاق العمل: باب القفص فقط، ولم يُطلب منه فتح الخزانة.\nسُلّم القفص مفتوحاً والخزانة مغلقة إلى: ص. المناصرة 17:22\nملاحظة الفني: فتح الخزانة يلزمه شاهد ثانٍ — [توقيع الشاهد: فارغ]",
  ["a_get_job_sheet"], ["f_tech_scope", "f_witness_asked"], "strong",
  "يثبت نطاق عمل الفني ومن تسلّم المكان؛ لا يثبت ما جرى بعد التسليم.", loc="loc_vault")
V("ev_custody_form", "نموذج جرد وعهدة الخزانة 218", "documentary",
  "نموذج جرد وعهدة محتويات الخزانة 218\n1) 12/03/2014 — جرد عند الإيداع: ست سبائك فضة — توقيع المستأجرة والموظف\n2–4) زيارات 2017 و2020 و2023 — مراجعة المحتويات بحضور موظف: «سليمة» — توقيع المستأجرة والموظف\n5) 14/08/2024 — فتح للصيانة — جرد المحتويات: [فارغ] — توقيع شاهد ثانٍ: [فارغ]\n6) يوم الاكتشاف — فتح بحضور الحفيدين: ست قطع تذكارية",
  ["a_get_custody"], ["f_custody_gap", "f_sabri_sole"], "strong",
  "يبيّن موضع انقطاع الجرد والتوقيع لا ما جرى في ذلك الموضع.", ko="KO-FC-04-026", loc="loc_office")
V("ev_bassam_statement", "إفادة بسام (ملخص)", "testimonial",
  "ملخص إفادة بسام العيسى:\n«فحصت الختم بنفسي أمام الحفيدين فوجدته سليماً. إن كان الختم سليماً فلا يمكن أن يكون أحد فتح الخزانة منذ الإيداع.»",
  ["a_note_bassam"], ["f_seal_checked"], "weak",
  "يصف ختماً سليماً اليوم ثم يعمّم على الماضي كله؛ والختم المركّب حديثاً يكون سليماً مهما جرى قبله.", red=True, loc="loc_vault")
V("ev_guard_demeanour", "ملاحظة عن سلوك الحارس في المقابلة", "observation",
  "ملاحظة المحقق: كان الحارس نبيل يتكلم بسرعة، ويكرر «لم ألمس شيئاً»، وتردّد قبل أن يجيب عن مفاتيحه.",
  ["a_note_nabil_manner"], ["f_guard_nervous"], "weak",
  "التوتر في المقابلة ملاحظة لا دليل؛ قد يشعر به كل من يعرف أن الجميع يشتبه به، ولا يفرّق بين البريء وغيره.", red=True, loc="loc_gate")
V("ev_sabri_statement", "إفادة صبري (ملخص)", "testimonial",
  "ملخص إفادة صبري المناصرة:\n«فتحت الخزانة دقائق قليلة لأختبر الباب بعد تغيير المفصلة، ثم أغلقتها وركّبت الختم. لم أُخرج منها شيئاً.»",
  ["a_note_sabri"], ["f_sabri_opened"], "weak",
  "إفادة صاحب مصلحة في بقاء سمعته؛ تُقاس بسجل البطاقات وسجل المفاتيح لا بنبرتها.", loc="loc_vault")

# ---------------------------------------------------------------- inferences
def P(t, i): return {"ref_type": t, "ref_id": i}
inf = []
def I(id, prem, ct, concl, rel, strength, rule, ks):
    inf.append({"id": id, "premises": prem, "conclusion": {"ref_type": ct, "ref_id": concl}, "relation": rel, "strength": strength, "rule_ar": rule, "skill_ko_refs": ks})
# f_coins_postdate (used against "always coins")
I("i_a_post", [P("evidence", "ev_coin_mint"), P("evidence", "ev_deposit_receipt")], "fact", "f_coins_postdate", "establishes", "strong",
  "العقد يؤرّخ الإيداع بسنة 2014، والقطع منقوشة بسنة 2024؛ فالقطع لم توجد وقت الإيداع.", ["KO-NP-02H-002", "KO-RS-06-017"])
I("i_b_post", [P("evidence", "ev_mint_bulletin"), P("evidence", "ev_seal_register")], "fact", "f_coins_postdate", "establishes", "strong",
  "النشرة تجعل بداية البيع 20/03/2024 وسجل الأختام يجعل الإيداع في 2014؛ فالقطع جاءت بعد الإيداع بعشر سنوات.", ["KO-NP-02H-002", "KO-RS-06-017"])
# f_swap_at_maint (key): route A = records of openings + coin year ; route B = seal register + mint bulletin
I("i_a_swap", [P("evidence", "ev_coin_mint"), P("evidence", "ev_deposit_receipt"), P("evidence", "ev_open_log")], "fact", "f_swap_at_maint", "establishes", "strong",
  "القطع منقوشة بسنة 2024 والإيداع في 2014، وسجل الفتح لا يذكر منذ بداية 2024 إلا فتحة الصيانة؛ فلا تبديل ممكناً قبلها ولا بعدها.", ["KO-RS-06-017", "KO-NP-02H-002"])
I("i_b_swap", [P("evidence", "ev_mint_bulletin"), P("evidence", "ev_seal_register")], "fact", "f_swap_at_maint", "establishes", "strong",
  "الأختام تُستبدل عند كل فتح، وبعد 20/03/2024 لا يظهر في سجلها إلا الختم 9026 المركّب في 14/08/2024؛ فتلك هي الفتحة الوحيدة بعد صدور القطع.", ["KO-RS-06-017", "KO-FC-04-026"])
# f_guard_out (key)
I("i_a_guard", [P("evidence", "ev_guard_hire"), P("evidence", "ev_open_log")], "fact", "f_guard_out", "establishes", "strong",
  "الحارس باشر العمل في 2026، ولا مفتاح غرفة بيده، وسجل الفتح لا يذكر فتحة بعد 14/08/2024؛ فلا فرصة لديه في التبديل.", ["KO-RS-05-007", "KO-RS-06-001"])
I("i_b_guard", [P("evidence", "ev_vault_door_log"), P("evidence", "ev_key_register")], "fact", "f_guard_out", "establishes", "strong",
  "سجل البطاقات لا يذكر دخولاً بطاقته إلى الغرفة، وسجل المفاتيح لا يدرجه بين الحاملين؛ فلا مفتاح ولا دخول.", ["KO-RS-05-007", "KO-RS-06-001"])
# f_sabri_sole (key)
I("i_a_sole", [P("evidence", "ev_job_sheet"), P("evidence", "ev_custody_form")], "fact", "f_sabri_sole", "establishes", "strong",
  "الفني لم يفتح الخزانة وسلّم المكان لصبري، ونموذج العهدة يخلو من توقيع شاهد وجرد في ذلك السطر؛ فالفتح كان بيد حامل المفتاح وحده.", ["KO-FC-04-026", "KO-RS-06-017"])
I("i_b_sole", [P("evidence", "ev_key_register"), P("evidence", "ev_vault_door_log")], "fact", "f_sabri_sole", "establishes", "strong",
  "المفتاح الاحتياطي خرج مع صبري 16:35 وعاد معه 20:50، وبعد خروج الفني 17:22 لم يبقَ في الغرفة غيره حتى 20:46؛ فالفتح كان بيده وحده بلا شاهد.", ["KO-FC-04-026", "KO-RS-06-017"])
I("i_gap", [P("evidence", "ev_custody_form")], "fact", "f_custody_gap", "establishes", "strong",
  "السطر الخاص بفتحة الصيانة بلا جرد وبلا توقيع شاهد، بينما كل سطر قبله موقّع؛ فهذه هي الحلقة المكسورة في سلسلة العهدة.", ["KO-FC-04-026"])
# claims
I("i_seal_claim", [P("evidence", "ev_seal_register"), P("evidence", "ev_seal_photo")], "claim", "cl_bassam_seal", "contradicts_claim", "strong",
  "الختم الحالي رقمه 9026 وتاريخ تركيبه 14/08/2024، وختم الإيداع كان 4471؛ فسلامة الختم الحالي لا تعني أن الخزانة لم تُفتح منذ الإيداع.", ["KO-RS-05-014", "KO-RS-06-001"])
I("i_sabri_claim", [P("evidence", "ev_vault_door_log"), P("evidence", "ev_key_register")], "claim", "cl_sabri_short", "contradicts_claim", "strong",
  "البطاقة تسجّل خروجه 20:46 والمفتاح عاد 20:50، أي بعد انصراف الفني بنحو ثلاث ساعات ونصف، لا بدقائق.", ["KO-RS-05-014", "KO-RS-06-017"])
I("i_guard_claim", [P("fact", "f_guard_out")], "claim", "cl_guard_stranger", "contradicts_claim", "strong",
  "كونه الأحدث التحاقاً لا يمنحه فرصة؛ الفرصة تُقاس بالمفتاح والدخول والزمن.", ["KO-RS-05-014"])
# hypotheses
I("i_support_maint", [P("fact", "f_swap_at_maint"), P("fact", "f_sabri_sole")], "hypothesis", "h_maint", "supports", "strong",
  "الفتحة الوحيدة بعد صدور القطع كانت فتحة الصيانة، وفيها انفرد حامل المفتاح الاحتياطي بالخزانة بلا شاهد ولا جرد؛ فهذا التفسير يجمع الأزمنة والسجلات كلها.", ["KO-RS-06-007"])
I("i_rule_guard", [P("fact", "f_guard_out")], "hypothesis", "h_guard", "rules_out", "strong",
  "من التحق بعد الفتحة الوحيدة ولا مفتاح ولا دخول له لا يمكن أن يكون مبدّل المحتويات.", ["KO-RS-06-008", "KO-RS-05-007"])
I("i_rule_always", [P("fact", "f_coins_postdate")], "hypothesis", "h_always", "rules_out", "conclusive",
  "قطعة صُكّت في 2024 لا يمكن أن تكون في الخزانة منذ 2014.", ["KO-RS-06-008"])

# ---------------------------------------------------------------- character knowledge
K = lambda f, a="witnessed", c="certain": {"fact_id": f, "access": a, "certainty": c}
ck = [
    {"character_id": "luay", "knows": [K("f_deposit_2014", "common_knowledge")], "hides": [], "believes": [{"claim_id": "cl_guard_stranger", "stance": "sincere"}]},
    {"character_id": "bassam", "knows": [K("f_seal_checked"), K("f_seal_register_exists", "professional")], "hides": [], "believes": [{"claim_id": "cl_bassam_seal", "stance": "sincere"}]},
    {"character_id": "nabil", "knows": [K("f_guard_start"), K("f_guard_key")], "hides": [], "believes": []},
    {"character_id": "sabri", "knows": [K("f_sabri_opened")],
     "hides": [{"fact_id": "f_sabri_stayed", "reveal_when": {"any": [{"presented": {"evidence_id": "ev_vault_door_log", "to_character": "sabri"}}, {"presented": {"evidence_id": "ev_key_register", "to_character": "sabri"}}]},
                "cover_claim_id": "cl_sabri_short", "reveal_line_id": "sb_stayed"}],
     "believes": [{"claim_id": "cl_sabri_short", "stance": "deliberate_lie"}]},
    {"character_id": "idris", "knows": [K("f_tech_scope"), K("f_witness_asked")], "hides": [], "believes": []},
    {"character_id": "sanaa", "knows": [K("f_open_log_exists", "professional"), K("f_seal_register_exists", "professional"), K("f_deposit_2014", "professional"), K("f_key_register_exists", "professional"), K("f_door_log_exists", "professional"), K("f_custody_form_exists", "professional")], "hides": [], "believes": []},
]
hyps = [
    {"id": "h_guard", "statement_ar": "بدّل الحارس الليلي الجديد محتويات الخزانة.", "is_true": False, "plausibility_at_start": "high", "suspect_id": "nabil"},
    {"id": "h_always", "statement_ar": "لم تكن في الخزانة سبائك أصلاً، وكانت القطع فيها منذ الإيداع.", "is_true": False, "plausibility_at_start": "medium"},
    {"id": "h_maint", "statement_ar": "جرى التبديل أثناء فتحة الصيانة يوم 14 أغسطس 2024، حين انفرد بالخزانة حامل المفتاح الاحتياطي بلا شاهد ولا جرد.", "is_true": True, "plausibility_at_start": "low", "suspect_id": "sabri"},
]
mis = [
    {"id": "rh_nerves", "points_to_hypothesis_id": "h_guard", "planted_via_ar": "الحارس الجديد غريب عن الفرع، ويتوتر ويتكلم بسرعة حين يُسأل عن مفاتيحه.",
     "evidence_ids": ["ev_guard_demeanour"], "refuted_by_inference_ids": ["i_rule_guard", "i_guard_claim"],
     "fairness_note_ar": "ملف التوظيف وسجل البطاقات وسجل المفاتيح تثبت كلها غياب المفتاح والدخول؛ والتوتر معلَّم في الواجهة «ملاحظة لا دليل» ويُفسَّر بأن الجميع يشتبه به."},
    {"id": "rh_seal", "points_to_hypothesis_id": "h_always", "planted_via_ar": "بسام يقسم أن الختم سليم، فيبدو أن الخزانة لم تُفتح قط وأن القطع كانت فيها دائماً.",
     "evidence_ids": ["ev_bassam_statement"], "refuted_by_inference_ids": ["i_seal_claim", "i_rule_always"],
     "fairness_note_ar": "الختم الحالي مركّب في 2024 حسب سجل الأختام وصورة الختم، وختم الإيداع رقمه 4471؛ وسنة 2024 على القطع تنقض أنها وُجدت وقت الإيداع."},
]
los = [
    {"id": "lo_time", "statement_ar": "يتحقق من اتساق السرد والخط الزمني، فيستخدم تاريخ الصنع حداً أدنى لزمن الوجود لا زمناً للوصول.", "skill_ko_ref": "KO-RS-06-017", "observable_behaviors_ar": ["يضع الأدلة في أزمنتها", "يحدد الفتحة الوحيدة بعد صدور القطع"], "evidence_sources": ["timeline_task", "action_log"]},
    {"id": "lo_diag", "statement_ar": "يقدّر القوة التشخيصية للدليل، فيعرف أن ختماً سليماً اليوم لا يخبر عن الماضي.", "skill_ko_ref": "KO-RS-06-001", "observable_behaviors_ar": ["يربط الدليل بالفرضية باتجاه صحيح", "يذكر حد السجل في الحجة"], "evidence_sources": ["evidence_board", "final_justification"]},
    {"id": "lo_lie_cues", "statement_ar": "يرفض إشارات السلوك دليلاً على الكذب، ويستبدلها بمطابقة الإفادة مع السجل.", "skill_ko_ref": "KO-RS-05-007", "observable_behaviors_ar": ["لا يعدّ توتر الحارس دليلاً", "يقابل قول صبري بسجل البطاقات"], "evidence_sources": ["action_log", "evidence_board", "final_justification"]},
    {"id": "lo_hyp", "statement_ar": "يوازن بين فرضيتين على الأقل ويستبعد ما تنقضه الأدلة.", "skill_ko_ref": "KO-RS-05-002", "observable_behaviors_ar": ["يضيف فرضيات", "يستبعد بدليل"], "evidence_sources": ["hypothesis_ledger"]},
    {"id": "lo_calib", "statement_ar": "يصوغ نسبة الترجيح بحدودها.", "skill_ko_ref": "KO-RS-06-021", "observable_behaviors_ar": ["يختار ثقة معقولة", "يذكر حدوداً"], "evidence_sources": ["final_justification"]},
    {"id": "lo_revise", "statement_ar": "يراجع رأيه الأول حين يظهر ما يخالفه.", "skill_ko_ref": "KO-RS-06-009", "observable_behaviors_ar": ["يغيّر فرضيته الرائدة بدليل"], "evidence_sources": ["hypothesis_ledger"]},
]
def levels(d): return [{"score": i, "descriptor_ar": t} for i, t in enumerate(d)]
rub = {
    "reference_answer_ar": "لم يبدّل الحارس شيئاً. القطع منقوشة بسنة 2024 وبيعها بدأ في 20 مارس 2024، فلا يمكن أن تكون في الخزانة منذ إيداع 2014. والفتحة الوحيدة المسجلة بعد ذلك هي فتحة الصيانة في 14 أغسطس 2024، وفيها انفرد حامل المفتاح الاحتياطي بالخزانة نحو ثلاث ساعات ونصف بلا شاهد ولا جرد، والختم الحالي رُكّب بعدها (رقمه 9026) فهو سليم دون أن يدل على شيء عما قبله. أما الحارس فباشر العمل في 2026، ولا مفتاح له ولم تدخل بطاقته الغرفة. حدود الاستنتاج: تثبت الأدلة الفرصة المنفردة وانقطاع العهدة، ولا تثبت من أخذ السبائك ولا أين هي، ولا تنفي وجود نسخة أخرى من المفتاح.",
    "criteria": [
        {"id": "c_source", "name_ar": "تصنيف المصادر", "objective_ids": ["lo_diag"], "scored_by": "deterministic", "weight": 0.15, "levels": levels(["لم يصنّف", "أخطأ في الأغلب", "نصف صحيح", "معظمه صحيح", "كله صحيح"])},
        {"id": "c_conflict", "name_ar": "ترتيب الأزمنة على الخط الزمني", "objective_ids": ["lo_time"], "scored_by": "deterministic", "weight": 0.2, "levels": levels(["لم يضع شيئاً", "وضع قليلاً", "وضع نصفها صحيحاً", "معظمها", "كلها في موضعها"])},
        {"id": "c_links", "name_ar": "ربط الأدلة بالفرضيات", "objective_ids": ["lo_diag", "lo_lie_cues"], "scored_by": "deterministic", "weight": 0.2, "levels": levels(["لا روابط", "قليلة", "نصفها صحيح", "معظمها", "كلها دقيقة"])},
        {"id": "c_uncertainty", "name_ar": "معايرة الثقة", "objective_ids": ["lo_calib"], "scored_by": "deterministic", "weight": 0.15, "levels": levels(["ثقة مفرطة", "حدود قليلة", "جزئية", "معقولة", "معايَرة كاملة"])},
        {"id": "c_revision", "name_ar": "مراجعة الرأي", "objective_ids": ["lo_revise"], "scored_by": "deterministic", "weight": 0.1, "levels": levels(["بقي على فرضية مرفوضة", "لم يعلن فرضية", "ثبت على فرضية سليمة", "غيّر بدليل", "غيّر بدليل ووثّق"])},
        {"id": "c_elimination", "name_ar": "استبعاد الفرضيات الخاطئة", "objective_ids": ["lo_hyp"], "scored_by": "deterministic", "weight": 0.1, "levels": levels(["لم يستبعد", "استبعد خطأً", "فرضية بدليل", "فرضيتين", "كل الخاطئة"])},
        {"id": "c_justification", "name_ar": "جودة الحجة المكتوبة", "objective_ids": ["lo_diag", "lo_hyp", "lo_time"], "scored_by": "human", "weight": 0.1, "levels": levels(["لا حجة", "ادعاء بلا سند", "أدلة دون ربط", "ربط الأدلة بالاستنتاج", "ربط مع البدائل والحدود"])},
    ],
}
def H(id, lv, kind, text, trig, target=None, w=0.0):
    d = {"id": id, "level": lv, "kind": kind, "text_ar": text, "trigger": trig, "assessment_weight": w}
    if target: d["targets_inference_id"] = target
    return d
he = lambda e: {"has_evidence": e}
al = {"always": True}
hints = [
    H("hg1", 1, "metacognitive", "التاريخ المنقوش على شيء يخبرك متى يمكن أن يكون قد وُجد، لا متى وصل إلى مكانه. ماذا يعني ذلك هنا؟", al, None, 0.02),
    H("hg2", 2, "focus_area", "رتّب على خط واحد: الإيداع، وصدور القطع، وكل فتحة للخزانة، والتحاق الحارس.", he("ev_coin_mint"), None, 0.04),
    H("hs1", 1, "metacognitive", "إن كان الختم الحالي سليماً، فمتى رُكّب هذا الختم؟", he("ev_bassam_statement"), "i_seal_claim", 0.02),
    H("hs2", 2, "pointer", "قارن رقم الختم في العقد برقم الختم الحالي في سجل مخزون الأختام.", he("ev_bassam_statement"), "i_seal_claim", 0.05),
    H("hk1", 1, "metacognitive", "من كان معه المفتاح، ومن كان في الغرفة، ومتى خرج كل منهما؟", he("ev_sabri_statement"), "i_b_sole", 0.02),
    H("hk2", 2, "focus_area", "قابل قول صبري «دقائق قليلة» بوقت خروجه في سجل البطاقات ووقت عودة المفتاح.", he("ev_sabri_statement"), "i_b_sole", 0.05),
    H("hn1", 1, "metacognitive", "التوتر يحتاج تفسيراً، لكنه ليس دليلاً. ما الذي يمنح شخصاً فرصة فعلية لفتح خزانة؟", he("ev_guard_demeanour"), "i_a_guard", 0.02),
    H("hn2", 2, "pointer", "ابحث عن تاريخ مباشرة الحارس العمل وعن المفاتيح التي سُلّمت له.", he("ev_guard_demeanour"), "i_a_guard", 0.05),
]
# ---------------------------------------------------------------- actions
A = []
def Act(id, typ, label, pre, effects, target=None, tel=None, cost=1):
    d = {"id": id, "type": typ, "label_ar": label, "precondition": pre, "effects": effects, "time_cost_units": cost}
    if target: d["target_id"] = target
    if tel: d["telemetry_code"] = tel
    A.append(d)
G = lambda e: {"op": "grant_evidence", "ref_id": e}
Uf = lambda f: {"op": "unlock_fact", "ref_id": f}
fu = lambda f: {"fact_unlocked": f}
Act("a_examine_coins", "examine", "افحص القطع الست المكتشفة", al, [G("ev_coin_mint")], "obj_coins", "EXAMINE_COINS")
Act("a_read_bulletin", "examine", "اقرأ نشرة دار سك المرسى", al, [G("ev_mint_bulletin")], "org_mint", "READ_BULLETIN")
Act("a_photo_seal", "examine", "صوّر الختم الحالي على باب الخزانة", al, [G("ev_seal_photo")], "loc_vault", "PHOTO_SEAL")
Act("a_read_contract", "examine", "اطلب عقد الخزانة 218", fu("f_deposit_2014"), [G("ev_deposit_receipt")], "loc_office", "READ_CONTRACT")
Act("a_get_open_log", "examine", "اطلب سجل فتح الخزانة 218", fu("f_open_log_exists"), [G("ev_open_log")], "loc_office", "GET_OPEN_LOG")
Act("a_get_seal_register", "examine", "اطلب سجل مخزون الأختام", fu("f_seal_register_exists"), [G("ev_seal_register")], "loc_office", "GET_SEAL_REGISTER")
Act("a_get_key_register", "examine", "اطلب سجل عهدة المفاتيح", fu("f_key_register_exists"), [G("ev_key_register")], "loc_office", "GET_KEY_REGISTER")
Act("a_get_door_log", "examine", "اطلب سجل بطاقات باب غرفة الخزائن", fu("f_door_log_exists"), [G("ev_vault_door_log")], "loc_vault", "GET_DOOR_LOG")
Act("a_get_custody", "examine", "اطلب نموذج جرد وعهدة الخزانة 218", fu("f_custody_form_exists"), [G("ev_custody_form")], "loc_office", "GET_CUSTODY")
Act("a_get_hire", "examine", "اطلب ملف توظيف الحارس الليلي", fu("f_guard_start"), [G("ev_guard_hire")], "loc_office", "GET_HIRE")
Act("a_get_job_sheet", "examine", "اطلب أمر عمل الصيانة من الفني", fu("f_tech_scope"), [G("ev_job_sheet")], "idris", "GET_JOB_SHEET")
for cid, lab in [("luay", "لؤي"), ("bassam", "بسام"), ("nabil", "نبيل"), ("sabri", "صبري"), ("idris", "إدريس"), ("sanaa", "السيدة سناء")]:
    Act(f"a_int_{cid}", "interview", f"ابدأ مقابلة {lab}", al, [{"op": "raise_trust", "ref_id": cid, "amount": 1}], cid, f"INT_{cid.upper()}")
Act("a_note_bassam", "examine", "دوّن إفادة بسام", fu("f_seal_checked"), [G("ev_bassam_statement")], "bassam", "NOTE_BASSAM")
Act("a_note_nabil_manner", "examine", "دوّن ملاحظة عن سلوك الحارس في المقابلة", fu("f_guard_start"), [G("ev_guard_demeanour")], "nabil", "NOTE_NABIL_MANNER")
Act("a_note_sabri", "examine", "دوّن إفادة صبري", fu("f_sabri_opened"), [G("ev_sabri_statement")], "sabri", "NOTE_SABRI")
Act("p_door_sabri", "present_evidence", "اعرض سجل البطاقات على صبري", {"presented": {"evidence_id": "ev_vault_door_log", "to_character": "sabri"}}, [{"op": "emit_event", "ref_id": "PRESENTED_DOOR"}], "sabri", "P_DOOR_SABRI", 0)
Act("p_keys_sabri", "present_evidence", "اعرض سجل المفاتيح على صبري", {"presented": {"evidence_id": "ev_key_register", "to_character": "sabri"}}, [{"op": "emit_event", "ref_id": "PRESENTED_KEYS"}], "sabri", "P_KEYS_SABRI", 0)
Act("p_register_bassam", "present_evidence", "اعرض سجل الأختام على بسام", {"presented": {"evidence_id": "ev_seal_register", "to_character": "bassam"}}, [{"op": "emit_event", "ref_id": "PRESENTED_REGISTER"}], "bassam", "P_REGISTER_BASSAM", 0)
Act("a_hint", "request_hint", "اطلب تلميحاً", al, [], None, "REQUEST_HINT", 0)
Act("a_accuse", "final_accusation", "قدّم الاستنتاج النهائي", al, [{"op": "emit_event", "ref_id": "SUBMIT"}], None, "FINAL_ACCUSATION", 0)

topics = [
    {"id": "t_locker", "label_ar": "الخزانة والسبائك", "example_questions_ar": ["ماذا أودعت جدتك؟", "من تشك فيه ولماذا؟"], "fact_ids": ["f_deposit_2014"], "claim_ids": ["cl_guard_stranger"]},
    {"id": "t_seal", "label_ar": "الختم", "example_questions_ar": ["هل الختم سليم؟", "هل يوجد سجل للأختام؟"], "fact_ids": ["f_seal_checked", "f_seal_register_exists"], "claim_ids": ["cl_bassam_seal"]},
    {"id": "t_guard", "label_ar": "عمل الحارس", "example_questions_ar": ["متى باشرت العمل؟", "أي مفاتيح لديك؟"], "fact_ids": ["f_guard_start", "f_guard_key"]},
    {"id": "t_open", "label_ar": "فتحة الصيانة", "example_questions_ar": ["هل فتحت الخزانة يوم الصيانة؟", "كم بقيت في الغرفة؟"], "fact_ids": ["f_sabri_opened", "f_sabri_stayed"], "claim_ids": ["cl_sabri_short"]},
    {"id": "t_tech", "label_ar": "عمل الصيانة", "example_questions_ar": ["ما نطاق أمر العمل؟", "هل طلبت شاهداً؟"], "fact_ids": ["f_tech_scope", "f_witness_asked"]},
    {"id": "t_records", "label_ar": "سجلات الفرع", "example_questions_ar": ["ما السجلات المتاحة؟", "هل يوجد سجل للمفاتيح؟", "ماذا يوقّع الأطراف عند كل فتحة؟"], "fact_ids": ["f_open_log_exists", "f_seal_register_exists", "f_key_register_exists", "f_door_log_exists", "f_custody_form_exists", "f_deposit_2014"]},
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
        Act(f"ask_{_c['id']}_{f}", "interview", f"[نموذج] {_c['id']} يذكر {f}", _pre[_c["id"]], [Uf(f)], _c["id"], f"ASK_{_c['id'].upper()}_{f.upper()}", 0)
    for f, h in _hid.items():
        if f not in _tf or f not in _voiced: continue
        Act(f"ask_{_c['id']}_{f}", "interview", f"[نموذج] {_c['id']} يكشف {f}", {"all": [_pre[_c["id"]], h["reveal_when"]]}, [Uf(f)], _c["id"], f"ASK_{_c['id'].upper()}_{f.upper()}", 0)

steps = [
    (1, "القطع منقوشة بسنة 2024 وبدأ بيعها في 20 مارس 2024، بينما أُودعت السبائك في 2014: فلم تكن القطع موجودة وقت الإيداع، ولم تكن في الخزانة قط قبل 2024.", ["ev_coin_mint", "ev_deposit_receipt", "ev_mint_bulletin"], "i_a_post"),
    (2, "بعد 2024 لا يذكر سجل الفتح إلا فتحة الصيانة يوم 14 أغسطس، ويتفق معه سجل الأختام المستقل الذي لا يحمل بعد صدور القطع إلا الختم 9026.", ["ev_open_log", "ev_seal_register", "ev_mint_bulletin"], "i_b_swap"),
    (3, "سلامة الختم الحالي لا تدل على شيء قبله: رُكّب في تلك الفتحة نفسها، وختم الإيداع كان رقماً آخر.", ["ev_seal_photo", "ev_seal_register", "ev_deposit_receipt"], "i_seal_claim"),
    (4, "في تلك الفتحة سلّم الفني المكان لصبري ولم يفتح الخزانة، ونموذج العهدة خالٍ من الجرد ومن توقيع الشاهد: هنا الحلقة المكسورة.", ["ev_job_sheet", "ev_custody_form"], "i_a_sole"),
    (5, "ومن مسار مستقل: المفتاح الاحتياطي معه من 16:35 إلى 20:50، وسجل البطاقات يُبقيه وحده في الغرفة بعد 17:22 إلى 20:46، وهذا يخالف قوله إنه بقي دقائق.", ["ev_key_register", "ev_vault_door_log"], "i_b_sole"),
    (6, "أما الحارس فالتحق في 2026 بلا مفتاح ولا بطاقة دخول، ولم تُفتح الخزانة بعد فتحة الصيانة؛ فلا فرصة لديه، وتوتره لا يغيّر ذلك.", ["ev_guard_hire", "ev_open_log"], "i_a_guard"),
    (7, "إذن حدث التبديل في فتحة الصيانة وحدها: الأدلة تثبت الفرصة المنفردة وانقطاع العهدة، وتترك للجهة المختصة أن تحدد ما جرى للسبائك.", ["ev_key_register", "ev_vault_door_log", "ev_custody_form"], "i_support_maint"),
]
ending = {
    "steps": [{"order": o, "text_ar": t, "uses_evidence_ids": u, "inference_id": i} for o, t, u, i in steps],
    "alternative_paths_ar": [
        "يمكن بلوغ النتيجة من العقد والقطع وسجل الفتح وأمر العمل ونموذج العهدة وملف الحارس، أي من المسار المكتوب وحده.",
        "ويمكن بلوغها من نشرة الدار وسجل الأختام وسجل المفاتيح وسجل البطاقات وحدها، دون العقد؛ والأقوى أن يتفق المساران.",
    ],
    "what_evidence_could_not_show_ar": [
        "لا تثبت الأدلة من أخذ السبائك ولا أين هي الآن؛ هي تثبت متى كان التبديل ممكناً ومن انفرد بالخزانة حينها.",
        "لا تنفي الأدلة وجود نسخة أخرى من المفتاح، وقد يدخل شخص خلف آخر دون مسح بطاقته.",
        "نموذج العهدة لا يخبرنا بما كان في الخزانة بعد زيارة 2023 إلا بالوصف الذي كُتب عندها.",
    ],
    "science_notes_ar": [
        "تاريخ الصنع المنقوش على شيء هو أقدم زمن ممكن لوجوده، لا زمن وصوله؛ ويكفي وجوده لنفي أنه كان في المكان قبل ذلك.",
        "الختم السليم اليوم لا يخبر عن فتحات سابقة؛ تحقق من تاريخ تركيبه ورقمه في سجل مستقل.",
        "الحلقة المكسورة في سلسلة العهدة هي الموضع الذي لا جرد فيه ولا شاهد ولا توقيع؛ عندها يضعف الاستدلال عمّا حدث للمحتويات ويقوى السؤال عن الإجراء.",
        "تُختم القضية بمساءلة مؤسسية لا بتشهير: يحيل الفرع الأمر إلى الجهة المختصة، ويعتمد قاعدة شاهدين وجرداً مكتوباً لكل فتحة، ويعتذر للحارس عن الاتهام السابق.",
        "ما نسميه نسبة الترجيح حكم مبني على سجلات يمكن تتبّعها، لا على ثقة بمجرد أن الشخص قديم أو جديد.",
    ],
}
core = {
    "schema_version": "0.1.0", "case_id": CID, "case_version": "0.1.0",
    "meta": {"title_ar": "العملة الأحدث من الوديعة", "title_en": "The Coin Newer Than the Deposit", "age_band": "13-15", "locale": "ar", "dialogue_register": "msa", "estimated_minutes": 30, "difficulty": 2,
             "content_flags": ["no_violence", "theft"], "authors": ["فريق أثر التحريري (مسودة بمساعدة الذكاء الاصطناعي، عن بذرة من قضايا التراث، لم تُراجَع بشرياً بعد)"],
             "knowledge_object_refs": ["KO-RS-06-017", "KO-RS-06-001", "KO-RS-05-007", "KO-RS-05-002", "KO-RS-06-009", "KO-RS-06-021", "KO-FC-04-024", "KO-FC-04-026", "KO-NP-02H-002"]},
    "premise": {"hook_ar": "ست سبائك فضة تحوّلت إلى ست قطع تذكارية، والجميع يشير إلى الحارس الجديد. لكن على حافة إحدى القطع تاريخاً يحكي قصة أخرى.",
                "player_role_ar": "أنت مراجع في لجنة مراجعة الأمانات بميناء المرسى، وطُلب منك أن تحسم متى جرى تبديل محتويات الخزانة وما الذي تثبته السجلات.",
                "setting_ar": "فرع المرسى لخزائن الأمانات، في ميناء المرسى. تتابع الأحداث على سنوات، ويوم الصيانة وحده مسجَّل بالساعة.",
                "public_fact_ids": ["f_coins_found", "f_clerk_swears", "f_guard_suspected"],
                "assumed_general_knowledge_ar": ["العملة لا توجد قبل سنة سكّها", "يُستبدل ختم الخزانة عند كل فتح"]},
    "entities": {"characters": chars, "locations": locations, "objects": objects, "organizations": orgs},
    "truth": {"solution": {"culprit_ids": ["sabri"], "summary_ar": "التبديل لم يحدث على يد الحارس. جاءت القطع بعد صدورها في 2024، ولم تُفتح الخزانة بعد ذلك إلا مرة واحدة هي فتحة الصيانة، وفيها انفرد بها حامل المفتاح الاحتياطي ساعات بلا شاهد ولا جرد، ثم رُكّب ختم جديد يبدو سليماً. تثبت الأدلة الفرصة وانقطاع العهدة، ولا تثبت وجهة السبائك.", "key_fact_ids": ["f_swap_at_maint", "f_sabri_sole", "f_guard_out"]},
              "facts": facts, "claims": claims},
    "timeline": timeline, "evidence": ev, "evidence_graph": {"inferences": inf},
    "character_knowledge": ck, "hypotheses": hyps, "misdirection_plan": mis, "learning_objectives": los,
    "mechanics": {"time_budget_units": 40, "actions": A},
    "state_machine": {"id": "c012", "initial": "briefing", "type": "compound", "states": {
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
    "clock": {"epoch_hhmm": "16:00", "zone_label_ar": "ساعة الفرع يوم الصيانة"},
    "cover": {"title_ar": "العملة الأحدث من الوديعة", "tagline_ar": "ست قطع في خزانة قديمة، وتاريخ على حافة إحداها لا يتفق مع الحكاية", "kicker_ar": "الملف الثاني عشر · الشيء الأحدث من روايته", "glyph": "◎", "accent": "amber"},
    "cold_open_ar": ["الخميس، فرع المرسى لخزائن الأمانات.", "فتح حفيدان خزانة جدتهما بعد اثنتي عشرة سنة، فوجدا ست قطع تذكارية بدل ست سبائك صغيرة من الفضة.",
                     "موظف الخزائن يقسم أن الختم سليم، والجميع يشير إلى الحارس الليلي الجديد.",
                     "على حافة إحدى القطع رقم صغير. ابدأ بسؤال واحد: متى يمكن أن توجد هذه القطعة أصلاً؟"],
    "labs": [],
    "source_classes": [
        {"id": "primary_record", "label_ar": "سجل أصلي", "help_ar": "يُنتجه نظام أو شخص لحظة الحدث دون وسيط، كسجل مفاتيح أو سجل بطاقات أو أمر عمل."},
        {"id": "redisplay", "label_ar": "نسخة معروضة", "help_ar": "معلومة نُقلت من سجل آخر أو أُعيد عرضها."},
        {"id": "claim", "label_ar": "قول أو تصريح", "help_ar": "إفادة شخص أو ملاحظة عن سلوكه؛ تُقاس بالسجلات لا بنبرة صاحبها ولا بسلوكه."},
        {"id": "template", "label_ar": "قالب أو نموذج", "help_ar": "نص جاهز لا يصف الحدث الفعلي بذاته."},
        {"id": "public_document", "label_ar": "وثيقة منشورة", "help_ar": "وثيقة معلنة ومعروف ناشرها، كنشرة دار السك."}],
    "limit_menu": [
        {"id": "l_who", "label_ar": "الأدلة تثبت فرصة منفردة وانقطاع عهدة، ولا تثبت من أخذ السبائك ولا أين هي"},
        {"id": "l_copy", "label_ar": "لا تنفي الأدلة وجود نسخة أخرى من المفتاح"},
        {"id": "l_after_2023", "label_ar": "لا نعرف ما كان في الخزانة بعد زيارة 2023 إلا بوصف مكتوب عندها"},
        {"id": "l_invalid_tension", "label_ar": "توتر الحارس الجديد يدل على أنه الفاعل"},
        {"id": "l_invalid_new", "label_ar": "كون الحارس الأحدث التحاقاً يجعله الأرجح"}],
    "mind_change_menu": [
        {"id": "m_unlogged", "label_ar": "ظهور فتحة غير مسجلة للخزانة بعد 20 مارس 2024"},
        {"id": "m_guard_key", "label_ar": "ثبوت أن الحارس حصل على نسخة من مفتاح الغرفة"},
        {"id": "m_early_coin", "label_ar": "ثبوت أن هذه القطع سُكّت قبل 2024"},
        {"id": "m_popular", "label_ar": "كثرة من يشيرون إلى الحارس الجديد"}],
    "skills": [{"skill_id": "KO-RS-06-017", "track": "B"}, {"skill_id": "KO-RS-06-001", "track": "B"}, {"skill_id": "KO-RS-05-007", "track": "D"}],
    "stage_hooks_ar": {"briefing": "قطع أحدث من الحكاية… فمتى دخلت إلى الخزانة؟", "investigating": "كل ختم وكل مفتاح وكل فتحة له تاريخ؛ اقرأ التواريخ قبل الأسماء.", "review": "قبل أن تغلق الملف: ما الذي لا تعرفه عن السبائك؟", "resolved": "أُغلق الملف. في الأرشيف وشاحان لم يُحسم أمرهما بعد."},
    "character_glyphs": {"luay": "ل", "bassam": "ب", "nabil": "ن", "sabri": "ص", "idris": "إ", "sanaa": "س"},
}
sc = {
    "case_id": CID,
    "accepted_conclusions": {"h_maint": {"grade": 1, "note_ar": "استنتاج متسق مع الأدلة ويتطلب ذكر حدوده: فرصة منفردة لا إثبات فعل."},
                             "h_guard": {"grade": 0, "note_ar": "يبني الاتهام على الحداثة والتوتر، ويتجاهل أن الحارس لا مفتاح له ولا فرصة."},
                             "h_always": {"grade": 0, "note_ar": "يتجاهل أن القطع منقوشة بسنة 2024 وأن الإيداع كان في 2014."}},
    "confidence_band": {"h_maint": [60, 88], "h_guard": [0, 15], "h_always": [0, 15]},
    "source_key": {"ev_coin_mint": "primary_record", "ev_deposit_receipt": "primary_record", "ev_open_log": "primary_record", "ev_mint_bulletin": "public_document",
                   "ev_seal_register": "primary_record", "ev_seal_photo": "primary_record", "ev_guard_hire": "primary_record", "ev_vault_door_log": "primary_record",
                   "ev_key_register": "primary_record", "ev_job_sheet": "primary_record", "ev_custody_form": "primary_record",
                   "ev_bassam_statement": "claim", "ev_guard_demeanour": "claim", "ev_sabri_statement": "claim"},
    "link_key": {
        "h_maint": {"ev_coin_mint": "supports", "ev_mint_bulletin": "supports", "ev_open_log": "supports", "ev_seal_register": "supports", "ev_key_register": "supports", "ev_vault_door_log": "supports", "ev_job_sheet": "supports", "ev_custody_form": "supports", "ev_seal_photo": "neutral", "ev_sabri_statement": "neutral"},
        "h_guard": {"ev_guard_hire": "weakens", "ev_vault_door_log": "weakens", "ev_key_register": "weakens", "ev_open_log": "weakens", "ev_guard_demeanour": "neutral"},
        "h_always": {"ev_coin_mint": "weakens", "ev_mint_bulletin": "weakens", "ev_deposit_receipt": "weakens", "ev_seal_register": "weakens", "ev_bassam_statement": "neutral"},
    },
    "required_limits": ["l_who", "l_copy"], "valid_mind_changers": ["m_unlogged", "m_guard_key", "m_early_coin"],
    "invalid_limits": ["l_invalid_tension", "l_invalid_new"],
    "decisive_evidence": ["ev_coin_mint", "ev_deposit_receipt", "ev_open_log", "ev_mint_bulletin", "ev_seal_register", "ev_key_register", "ev_vault_door_log", "ev_custody_form"],
    "lab_requirement": None,
    "timeline_requirement": [{"evidence_id": "ev_key_register", "utc_minute": 35, "tol": 3}, {"evidence_id": "ev_job_sheet", "utc_minute": 82, "tol": 3}, {"evidence_id": "ev_vault_door_log", "utc_minute": 286, "tol": 3}],
    "refuted_hypotheses": ["h_guard", "h_always"],
    "criteria_map": {"c_source": "source_typing", "c_conflict": "conflict_resolution", "c_links": "hypothesis_links", "c_uncertainty": "uncertainty", "c_revision": "revision", "c_elimination": "elimination", "c_justification": "justification_human"},
    "caps": {"no_citations_max": 45, "no_conflict_resolution_max": 65},
}
os.makedirs(OUT, exist_ok=True)
for suf, obj in [("", core), (".ui", ui), (".scoring", sc)]:
    with open(os.path.join(OUT, f"{CID}{suf}.json"), "w", encoding="utf8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
print("ok")
