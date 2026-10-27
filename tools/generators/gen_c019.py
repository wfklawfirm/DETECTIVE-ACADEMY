#!/usr/bin/env python3
# Case c019 «الكل يعترف ولا أحد فعلها» — seed S-12 (age band 16-18). Teaches: a confession is a CLAIM that needs independent support like any
# other claim (a sincere confession can still be factually wrong), and a record of what could not have happened (sequence, sensors) can outweigh
# four sincere voices. Non-graphic and teen-safe by design: nobody is hurt, the confessions are spontaneous and voluntary at a workshop meeting,
# NO interrogation, pressure or coercion is depicted, and the closing is institutional (a deferred repair ticket), not a punishment.
# Reconstructed from scratch (structure only): no body, no identities, no mockery. No-culprit convention: the facilities clerk whose (non-malicious)
# deferral of an old repair ticket allowed the defect to persist is recorded in culprit_ids; nobody dropped the sculpture.
# Mechanic note: the thermal-camera timeline is given as a log evidence item (no simulator needed). All persons, places and documents are fictional.
# Usage: gen_c019.py OUT_DIR
import json, sys, os
OUT = sys.argv[1]
CID = "c019_four_confessions"

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
ch("nour", "نور الفارس", "suspect", "طالبة في ورشة الفنون",
   "رقيقة ومسؤولة، تحمل همّ أي خطأ في الورشة، وتتحمّل اللوم بسرعة قبل أن تتحقق.",
   ["ألا يتضرر عمل ريتا", "أن تحمي رفاقها من اللوم"],
   [L("nr_greet", "greeting", "أنا قلت ما أظنه صحيحاً. اسألني ما تريد."),
    L("nr_conf", "reveal", "حين كنت أحمل صينية الألوان قرابة الرابعة وأربعين دقيقة لمس مرفقي جانب الرف. ظننت بعد ذلك أنني السبب فقلت ذلك في الاجتماع.", ["f_nour_acts"], ["cl_nour_bump"]),
    L("nr_unknown", "deflect_unknown", "لا أذكر أكثر من ذلك."),
    L("nr_off", "deflect_offtopic", "اسألني عمّا فعلته في الورشة."),
    L("nr_bye", "farewell", "أريد أن أعرف ما حدث فعلاً.")])
ch("basel", "باسل المهنا", "suspect", "طالب في ورشة الفنون",
   "سريع الحماسة وكريم، يقدّم نفسه حين يظن أن زميلاً يُتّهم، ويصدّق أنه المسؤول.",
   ["أن يحمي نور من اللوم", "ألا يتضرر المعرض"],
   [L("bs_greet", "greeting", "اعترفت لأنني لا أريد أن تُلام نور."),
    L("bs_conf", "reveal", "أغلقت باب الورشة بقوة وأنا خارج قبيل الخامسة والربع. ظننت أن الاهتزاز هو الذي أسقط المنحوتة.", ["f_basel_acts"], ["cl_basel_door"]),
    L("bs_unknown", "deflect_unknown", "لا أعرف."),
    L("bs_off", "deflect_offtopic", "اسألني عن الباب."),
    L("bs_bye", "farewell", "إن كنت مخطئاً فسأرتاح.")])
ch("hala", "هالة السيد", "suspect", "طالبة في ورشة الفنون",
   "عملية وهادئة، تتقدم حين ترى أن الحمل يقع على غيرها، وتبني تفسيرها على ما تعرف عن الأجهزة.",
   ["أن يُنصَف زملاؤها", "أن تفهم ما حدث لا أن تتحمل اللوم فقط"],
   [L("hl_greet", "greeting", "ظننت أن التفسير عندي، فقلته."),
    L("hl_conf", "reveal", "ضبطت المكيّف على أشد تبريد قرابة الخامسة وعشرين دقيقة. ظننت أن الاهتزاز الإضافي هو السبب.", ["f_hala_acts"], ["cl_hala_ac"]),
    L("hl_unknown", "deflect_unknown", "لا أعرف."),
    L("hl_off", "deflect_offtopic", "اسألني عن المكيّف."),
    L("hl_bye", "farewell", "المهم أن نعرف الحقيقة.")])
ch("jad", "جاد الخوري", "suspect", "طالب في ورشة الفنون، آخر من غادر الورشة",
   "جاد الضمير وقلق، يميل إلى أن يلوم نفسه لأنه كان آخر من لمس المنحوتة.",
   ["أن يتحمل مسؤولية ما فعله", "ألا يُظلم زملاؤه"],
   [L("jd_greet", "greeting", "كنت آخر من خرج، فأظن أن المسؤولية عليّ."),
    L("jd_conf", "reveal", "أدرت قاعدة المنحوتة بضعة سنتيمترات نحو الضوء قرابة الخامسة وخمس وعشرين دقيقة، ثم خرجت في الخامسة والنصف. ظننت أنني أخللت بتوازنها.", ["f_jad_acts"], ["cl_jad_turn"]),
    L("jd_unknown", "deflect_unknown", "لا أذكر."),
    L("jd_off", "deflect_offtopic", "اسألني عمّا فعلته قبل الخروج."),
    L("jd_bye", "farewell", "سأقبل ما تقوله الأدلة.")])
ch("rita", "ريتا العمر", "victim", "فنانة المنحوتة وطالبة في الورشة",
   "حزينة لكنها منصفة، لا تريد أن يُظلم أحد بسبب عملها، وتحتفظ بصور عملها.",
   ["أن تفهم سبب سقوط عملها", "ألا يُلام زملاؤها بغير حق"],
   [L("rt_greet", "greeting", "عملٌ استغرق أشهراً… لكني لا أريد أن يتحمل أحد ذنباً لم يفعله."),
    L("rt_found", "reveal", "وصلت إلى الورشة قرابة الخامسة وخمس وخمسين دقيقة فوجدت الحطام ولم يكن أحد هناك.", ["f_rita_found"]),
    L("rt_photo", "reveal", "عندي صور من معرض الفصل الماضي لعمل سابق لي، والرف نفسه يظهر في خلفيتها.", ["f_photo_exists"]),
    L("rt_unknown", "deflect_unknown", "لا أعرف."),
    L("rt_off", "deflect_offtopic", "اسألني عن المنحوتة وصورها."),
    L("rt_bye", "farewell", "شكراً لأنك تسأل قبل أن تحكم.")])
ch("maysa", "ميساء النجار", "suspect", "موظفة المرافق والصيانة في المدرسة",
   "مجتهدة ومثقلة بالطلبات، تؤجل ما تراه صغيراً، وتخشى أن تُلام فتقلل من شأن طلب قديم.",
   ["ألا تُلام على تأجيل صيانة", "أن تبقى سجلات الأجهزة سليمة"],
   [L("ms_greet", "greeting", "أتولى الأجهزة والصيانة هنا. أستطيع أن أعرض لك سجلاتها."),
    L("ms_systems", "reveal", "الورشة فيها كاميرا حرارية فوق الفرن، وقارئ بطاقات على الباب، ومسجّل اهتزاز على حائط الرف، ومتحكم في المكيّف، ولكل منها سجل.", ["f_thermal_exists", "f_door_log_exists", "f_vib_exists", "f_ac_log_exists"]),
    L("ms_claim", "lie", "لا طلبات صيانة مفتوحة تخص الرف.", None, ["cl_maysa_none"]),
    L("ms_refuse", "refuse_secret", "لا أذكر شيئاً آخر عن الصيانة."),
    L("ms_ticket", "reveal", "نعم... كان عندي طلب قديم عن صدع صغير في زاوية قاعدة الرف، صنّفته منخفض الأولوية وأجّلته إلى ما بعد المعرض. الطلب محفوظ عندي.", ["f_ticket_exists"]),
    L("ms_unknown", "deflect_unknown", "ليس عندي شيء عن هذا."),
    L("ms_off", "deflect_offtopic", "اسألني عن الأجهزة والصيانة."),
    L("ms_bye", "farewell", "سأراجع طريقة تأجيل الطلبات.")])

locations = [{"id": "loc_workshop", "name_ar": "ورشة الفنون", "description_ar": "الفرن والرف الزجاجي وطاولات العمل."},
             {"id": "loc_door", "name_ar": "باب الورشة", "description_ar": "قارئ البطاقات وورقة التوقيع."},
             {"id": "loc_office", "name_ar": "مكتب المرافق", "description_ar": "سجلات الأجهزة وطلبات الصيانة."},
             {"id": "loc_hall", "name_ar": "قاعة اجتماع الورشة", "description_ar": "حيث قيلت الاعترافات في الاجتماع."}]
objects = [{"id": "obj_sculpture", "name_ar": "المنحوتة الزجاجية", "description_ar": "عمل ريتا المعدّ للمعرض."},
           {"id": "obj_shelf", "name_ar": "رف المنحوتة", "description_ar": "رف خشبي بقاعدة معدنية قرب الفرن."}]
orgs = [{"id": "org_workshop", "name_ar": "ورشة فنون المرسى", "description_ar": "ورشة مدرسية خيالية تعرض أعمال طلابها."}]

# ---------------------------------------------------------------- facts
facts = []
def F(id, st, kind, subj, spoiler, time=None, loc=None, ko=None):
    d = {"id": id, "statement_ar": st, "kind": kind, "subject_ids": subj, "spoiler_level": spoiler}
    if time: d["time"] = time
    if loc: d["location_id"] = loc
    if ko: d["science_ko_refs"] = ko
    facts.append(d)
F("f_sculpture_fell", "سقطت منحوتة ريتا الزجاجية من الرف وتشظّت قبل المعرض بأيام، ولم يُصب أحد.", "event", ["obj_sculpture", "obj_shelf", "rita"], 0)
F("f_four_confessed", "اعترف أربعة طلاب واحداً بعد الآخر في اجتماع الورشة، وكل منهم يظن أن فعلاً صغيراً منه هو السبب.", "event", ["nour", "basel", "hala", "jad"], 0)
F("f_voluntary", "قيلت الاعترافات طوعاً في اجتماع عام للورشة، من غير استجواب ولا ضغط على أحد.", "state", ["nour", "basel", "hala", "jad", "loc_hall"], 0)
F("f_nour_acts", "لمس مرفق نور جانب الرف نحو 16:40 وهي تحمل صينية.", "event", ["nour", "obj_shelf"], 1, T(40, "approx"), "loc_workshop")
F("f_basel_acts", "أغلق باسل باب الورشة بقوة وهو يخرج نحو 17:12.", "event", ["basel", "loc_door"], 1, T(72, "approx"), "loc_door")
F("f_hala_acts", "ضبطت هالة المكيّف على أشد تبريد نحو 17:20.", "event", ["hala"], 1, T(80, "approx"), "loc_workshop")
F("f_jad_acts", "أدار جاد قاعدة المنحوتة بضعة سنتيمترات نحو 17:25 وخرج 17:30.", "event", ["jad", "obj_sculpture"], 1, T(85, "approx", 90), "loc_workshop")
F("f_rita_found", "وصلت ريتا نحو 17:55 فوجدت الحطام ولم يكن في الورشة أحد.", "event", ["rita", "loc_workshop"], 1, T(115, "approx"), "loc_workshop")
F("f_photo_exists", "لدى ريتا صور من معرض الفصل الماضي يظهر الرف في خلفيتها.", "state", ["rita", "obj_shelf"], 1)
F("f_thermal_exists", "في الورشة كاميرا حرارية فوق الفرن تغطي الرف المجاور ولها سجل لقطات.", "state", ["maysa", "loc_workshop"], 1)
F("f_door_log_exists", "على باب الورشة قارئ بطاقات له سجل دخول وخروج.", "state", ["maysa", "loc_door"], 1)
F("f_vib_exists", "على حائط الرف جهاز يسجّل الاهتزاز طوال اليوم.", "state", ["maysa", "obj_shelf"], 1)
F("f_ac_log_exists", "للمكيّف متحكم يسجّل تغيّر الضبط وتشغيل الضاغط.", "state", ["maysa", "loc_workshop"], 1)
F("f_ticket_exists", "في مكتب المرافق طلب صيانة قديم يخص الرف.", "state", ["maysa", "loc_office"], 1)
F("f_ticket_postponed", "سُجّل قبل خمسة أشهر طلب إصلاح لصدع في زاوية قاعدة الرف، وصُنّف منخفض الأولوية وأُجّل إلى ما بعد المعرض.", "event", ["maysa", "obj_shelf", "loc_office"], 2, None, "loc_office", ["KO-RS-05-014"])
F("f_break_old_new", "سطح الكسر في زاوية القاعدة مظلم ومغبر في جزئه الأول وفاتح حديث في بقيته.", "state", ["obj_shelf"], 1, None, "loc_workshop")
F("f_vib_quiet", "سجّل جهاز الاهتزاز هدوءاً تاماً من 17:30 حتى لحظة السقوط ثم نبضة واحدة كبيرة.", "state", ["obj_shelf"], 1, T(90, "exact", 101), "loc_workshop")
F("f_no_act_caused", "لم يكن أي فعل من الأفعال الأربعة المعترف بها هو سبب السقوط: بقيت المنحوتة سليمة بعد كل منها، وسقطت في وقت خلت فيه الورشة من الناس.", "relation", ["obj_sculpture", "nour", "basel", "hala", "jad"], 3, T(90, "exact", 102), "loc_workshop", ["KO-RS-05-009", "KO-RS-06-015"])
F("f_shelf_defect", "كان في زاوية قاعدة الرف صدع سابق للحادث بأشهر، فالرف لم يكن سليماً حين وُضعت عليه المنحوتة.", "relation", ["obj_shelf"], 3, None, "loc_workshop", ["KO-RS-06-009", "KO-RS-06-001"])
claims = [
    {"id": "cl_nour_bump", "statement_ar": "سقطت المنحوتة بسبب أن مرفقي لمس الرف.", "kind": "honest_mistake", "held_by": ["nour"], "true_fact_id": "f_no_act_caused", "contradicted_by_evidence_ids": ["ev_thermal_log", "ev_vib_log"]},
    {"id": "cl_basel_door", "statement_ar": "سقطت المنحوتة بسبب اهتزاز الباب الذي أغلقته.", "kind": "honest_mistake", "held_by": ["basel"], "true_fact_id": "f_no_act_caused", "contradicted_by_evidence_ids": ["ev_vib_log", "ev_door_log"]},
    {"id": "cl_hala_ac", "statement_ar": "سقطت المنحوتة بسبب اهتزاز المكيّف الذي ضبطته.", "kind": "honest_mistake", "held_by": ["hala"], "true_fact_id": "f_no_act_caused", "contradicted_by_evidence_ids": ["ev_ac_log", "ev_vib_log"]},
    {"id": "cl_jad_turn", "statement_ar": "سقطت المنحوتة لأنني أدرت قاعدتها قبل خروجي.", "kind": "honest_mistake", "held_by": ["jad"], "true_fact_id": "f_no_act_caused", "contradicted_by_evidence_ids": ["ev_thermal_log", "ev_door_log"]},
    {"id": "cl_maysa_none", "statement_ar": "لا طلبات صيانة مفتوحة تخص الرف.", "kind": "half_truth", "held_by": ["maysa"], "true_fact_id": "f_ticket_postponed", "contradicted_by_evidence_ids": ["ev_maintenance_ticket", "ev_break_surface"]},
]
timeline = [
    {"id": "te_nour", "description_ar": "مرفق نور يلمس جانب الرف وهي تحمل صينية الألوان.", "time": T(40, "approx"), "location_id": "loc_workshop", "actor_ids": ["nour"], "fact_ids": ["f_nour_acts"], "motivated_by_ar": "كانت تنقل الألوان إلى الطاولة"},
    {"id": "te_basel", "description_ar": "باسل يغلق باب الورشة بقوة وهو يخرج.", "time": T(72, "approx"), "location_id": "loc_door", "actor_ids": ["basel"], "fact_ids": ["f_basel_acts"], "motivated_by_ar": "كان متعجلاً للحاق بمحاضرته"},
    {"id": "te_hala", "description_ar": "هالة تضبط المكيّف على أشد تبريد.", "time": T(80, "approx"), "location_id": "loc_workshop", "actor_ids": ["hala"], "fact_ids": ["f_hala_acts"], "motivated_by_ar": "اشتدت حرارة الورشة قرب الفرن"},
    {"id": "te_jad", "description_ar": "جاد يدير قاعدة المنحوتة بضعة سنتيمترات ثم يخرج 17:30.", "time": T(85, "approx", 90), "location_id": "loc_workshop", "actor_ids": ["jad"], "fact_ids": ["f_jad_acts"], "motivated_by_ar": "أراد أن تواجه المنحوتة الضوء قبل أن يغادر"},
    {"id": "te_fall", "description_ar": "الرف يهبط والمنحوتة تسقط وتتشظى والورشة خالية.", "time": T(101, "approx", 102), "location_id": "loc_workshop", "actor_ids": [], "fact_ids": ["f_no_act_caused", "f_vib_quiet"]},
    {"id": "te_found", "description_ar": "ريتا تدخل الورشة وتجد الحطام.", "time": T(115, "approx"), "location_id": "loc_workshop", "actor_ids": ["rita"], "fact_ids": ["f_rita_found"], "motivated_by_ar": "جاءت لتتفقد عملها قبل المعرض"},
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
V("ev_incident_report", "تقرير الحادثة الأول", "documentary",
  "تقرير مشرفة الورشة — مساء الخميس\n«سقطت منحوتة ريتا الزجاجية قبل المعرض. في اجتماع المساء قال أربعة طلاب واحداً بعد الآخر إنهم أسقطوها: نور بلمسة، وباسل بإغلاق الباب، وهالة بضبط المكيّف، وجاد بتحريك القاعدة. لم يُسأل أحد بعد عن الأدلة.»",
  ["a_read_report"], ["f_four_confessed"], "moderate",
  "ملخص كتبته المشرفة من أقوال الطلاب؛ يسجّل ما قيل لا ما حدث، ولا يبيّن توقيت السقوط.", red=True, loc="loc_hall")
V("ev_nour_statement", "إفادة نور الفارس (ملخص)", "testimonial",
  "ملخص إفادة نور الفارس:\n«لمس مرفقي الرف وأنا أحمل الصينية قرابة الرابعة وأربعين دقيقة، وظننت أنني السبب. لا أعرف متى سقطت المنحوتة.»",
  ["a_note_nour"], ["f_nour_acts"], "weak",
  "إفادة صادقة في نية صاحبتها؛ تصف فعلاً حقيقياً وتضيف استنتاجاً عن سببه لا يقاس إلا بالسجلات.", loc="loc_hall")
V("ev_basel_statement", "إفادة باسل المهنا (ملخص)", "testimonial",
  "ملخص إفادة باسل المهنا:\n«أغلقت الباب بقوة وأنا خارج. اعترفت لأحمي نور من اللوم، فأنا لا أعرف إن كان الباب هو السبب.»",
  ["a_note_basel"], ["f_basel_acts"], "weak",
  "إفادة تجمع وصف فعل مع دافع الحماية؛ لا تثبت أن للفعل أثراً في الرف.", loc="loc_hall")
V("ev_hala_statement", "إفادة هالة السيد (ملخص)", "testimonial",
  "ملخص إفادة هالة السيد:\n«ضبطت المكيّف على أشد تبريد قرابة الخامسة وعشرين دقيقة، وظننت أن اهتزازه أسقط المنحوتة.»",
  ["a_note_hala"], ["f_hala_acts"], "weak",
  "إفادة صادقة في الفعل، والربط بالسقوط ظنّ لا قياس.", loc="loc_hall")
V("ev_jad_statement", "إفادة جاد الخوري (ملخص)", "testimonial",
  "ملخص إفادة جاد الخوري:\n«أدرت القاعدة قليلاً قبل الخامسة والنصف وخرجت. كنت آخر من غادر، فظننت أن اللوم عليّ.»",
  ["a_note_jad"], ["f_jad_acts"], "weak",
  "كونه آخر من لمس المنحوتة لا يجعله سبب سقوطها؛ ما يقرره الترتيب الزمني ومدة ما بين اللمس والسقوط.", red=True, loc="loc_hall")
V("ev_rita_statement", "إفادة ريتا العمر (ملخص)", "testimonial",
  "ملخص إفادة ريتا العمر:\n«وصلت قرابة الخامسة وخمس وخمسين دقيقة فوجدت الحطام والورشة خالية. لا أعرف متى سقط.»",
  ["a_note_rita"], ["f_rita_found"], "moderate",
  "شهادة على ما وجدته عند وصولها فقط، لا على لحظة السقوط.", loc="loc_workshop")
V("ev_thermal_log", "سجل الكاميرا الحرارية فوق الفرن", "digital",
  "سجل لقطات الكاميرا الحرارية — ورشة الفنون (تغطي الفرن والرف المجاور)\n16:35 المنحوتة ظاهرة على الرف؛ شخص واحد قرب الفرن.\n16:45 المنحوتة ظاهرة؛ شخص واحد قرب الطاولة.\n17:10 المنحوتة ظاهرة؛ شخصان.\n17:25 المنحوتة ظاهرة؛ شخصان.\n17:30 المنحوتة ظاهرة؛ شخص واحد يتجه إلى الباب.\n17:35 المنحوتة ظاهرة؛ لا أحد في اللقطة.\n17:40 المنحوتة ظاهرة؛ لا أحد في اللقطة.\n17:42 (لقطة تغيّر مفاجئ) الرف مائل والمنحوتة غائبة وشظايا باردة على الأرض؛ لا أحد في اللقطة.\n17:55 دخول شخص إلى اللقطة.",
  ["a_get_thermal"], ["f_no_act_caused"], "strong",
  "لقطة كل خمس دقائق تقريباً، فلا تحدد لحظة السقوط بالثانية؛ والكاميرا لا ترى الباب، وتظهر الأشخاص بحرارتهم لا بأسمائهم.", ko="KO-RS-06-001", loc="loc_workshop")
V("ev_door_log", "سجل بطاقات باب الورشة", "digital",
  "سجل قارئ البطاقات — ورشة الفنون\n15:48 دخول: نور\n16:52 خروج: نور\n17:03 دخول: باسل\n17:10 دخول: هالة\n17:12 خروج: باسل\n17:14 دخول: جاد\n17:28 خروج: هالة\n17:30 خروج: جاد\n(لا حركة بين 17:31 و17:54)\n17:55 دخول: ريتا",
  ["a_get_door"], ["f_no_act_caused"], "strong",
  "يسجّل مرور البطاقات فقط؛ قد يدخل شخص خلف آخر دون تمرير بطاقته، ويؤيد ذلك أو ينفيه سجل آخر مستقل.", loc="loc_door")
V("ev_signout_sheet", "ورقة الحضور المعلقة عند الباب", "documentary",
  "ورقة التوقيع اليدوية عند باب الورشة (يوقّع الطلاب أوقات الدخول والخروج)\nنور: 15:50 – 16:50\nباسل: 17:00 – 17:12\nهالة: 17:10 – 17:30\nجاد: 17:15 – 17:30\n(لا توقيعات أخرى حتى 17:55، ثم: ريتا 17:55)",
  ["a_read_signout"], ["f_no_act_caused"], "moderate",
  "ورقة كتبها الطلاب بأنفسهم بأوقات تقريبية؛ لا تغني عن سجل مستقل، لكنها لا تتأثر بسجل البطاقات.", loc="loc_door")
V("ev_vib_log", "سجل جهاز الاهتزاز على حائط الرف", "digital",
  "جهاز تسجيل الاهتزاز — حائط الرف (وحدة قياس اعتبارية من 0 إلى 10)\n16:40: 0.4\n17:12: 0.8\n17:20: 1.9 (بدء ضاغط المكيّف)\n17:25: 0.2\nمن 17:30 حتى 17:41: 0.1 ثابتة (هدوء)\n17:41: 6.5 (نبضة واحدة)\nملاحظة: بدء الضاغط يتكرر 6 إلى 8 مرات يومياً بقيمة نحو 1.9.",
  ["a_get_vib"], ["f_vib_quiet", "f_no_act_caused"], "strong",
  "جهاز واحد على حائط واحد؛ يقيس الاهتزاز لا من تسبب فيه، ولا يقيس لمسة بطيئة هادئة.", ko="KO-RS-06-015", loc="loc_workshop")
V("ev_ac_log", "سجل متحكم المكيّف", "digital",
  "سجل المكيّف — اليوم\n12:05 بدء الضاغط\n14:30 بدء الضاغط\n17:20 تغيير الضبط إلى 18 درجة ومروحة عالية (المستخدم: هالة)\n19:00 بدء الضاغط\nسجل الأسابيع السابقة: تغيّر الضبط ثلاث إلى أربع مرات يومياً.",
  ["a_get_ac"], ["f_ac_log_exists"], "strong",
  "يثبت تغيير الضبط وتكراره المعتاد؛ لا يقيس أثره في الرف مباشرة.", loc="loc_workshop")
V("ev_crack_photo", "صورة من معرض الفصل الماضي", "digital",
  "صورة لعمل سابق لريتا في معرض الفصل الماضي، ويظهر الرف نفسه في الخلفية.\nفي الزاوية اليسرى لقاعدة الرف خط شعري داكن.\nبيانات الصورة: مؤرخة قبل خمسة أشهر.",
  ["a_get_photo"], ["f_shelf_defect"], "moderate",
  "تثبت أن علامة قديمة كانت على القاعدة قبل الحادثة؛ لا تقيس عمقها ولا مقدار ما كان الرف يتحمله، وتاريخ الصورة من بياناتها.", ko="KO-RS-06-009", loc="loc_workshop")
V("ev_maintenance_ticket", "طلب صيانة الرف المؤجل", "documentary",
  "طلب صيانة رقم 3 — مكتب المرافق\nالتاريخ: قبل خمسة أشهر\nالموضع: رف الزجاج في ورشة الفنون\nالوصف: صدع شعري في الزاوية اليسرى لقاعدة الرف\nالأولوية: منخفضة\nالحالة: مؤجل إلى ما بعد المعرض\nالمسجِّلة: م. النجار",
  ["a_get_ticket"], ["f_ticket_postponed"], "strong",
  "سجل إداري يثبت وجود الصدع قبل الحادثة وتأجيل إصلاحه؛ لا يثبت وحده أنه سبب الانهيار.", contradicts=["cl_maysa_none"], loc="loc_office")
V("ev_break_surface", "فحص موضع الكسر في الرف", "physical",
  "فحص عيني لحطام الرف بعد الحادثة\nسطح الكسر في الزاوية اليسرى لقاعدة الرف: الثلث الأول منه مظلم ومغبر وأملس، وبقيته فاتح وخشن حديث.\nلا علامة ضربة أو انبعاج على جانب الرف.",
  ["a_inspect_break"], ["f_break_old_new"], "moderate",
  "فحص عيني دون مختبر؛ يدل على أن جزءاً من الكسر قديم ولا يحدد عمره بالأيام ولا حمل الانهيار.", contradicts=["cl_maysa_none"], loc="loc_workshop")

# ---------------------------------------------------------------- inferences
def P(t, i): return {"ref_type": t, "ref_id": i}
inf = []
def I(id, prem, ct, concl, rel, strength, rule, ks):
    inf.append({"id": id, "premises": prem, "conclusion": {"ref_type": ct, "ref_id": concl}, "relation": rel, "strength": strength, "rule_ar": rule, "skill_ko_refs": ks})
# path A: sensors that see the room
I("i_a_acts", [P("evidence", "ev_thermal_log"), P("evidence", "ev_door_log")], "fact", "f_no_act_caused", "establishes", "strong",
  "اللقطات تُظهر المنحوتة في مكانها بعد كل فعل معترف به حتى 17:40، وسجل الباب يثبت خلو الورشة منذ 17:30؛ فلم يكن أحد حاضراً لحظة السقوط.", ["KO-RS-05-009", "KO-RS-06-015"])
I("i_a_defect", [P("evidence", "ev_crack_photo")], "fact", "f_shelf_defect", "establishes", "strong",
  "صورة مؤرخة قبل خمسة أشهر تُظهر خطاً شعرياً في زاوية القاعدة؛ فالعيب سبق الحادثة بزمن طويل.", ["KO-RS-06-009"])
# path B: instruments and paper that do not depend on path A
I("i_b_acts", [P("evidence", "ev_vib_log"), P("evidence", "ev_signout_sheet")], "fact", "f_no_act_caused", "establishes", "strong",
  "أكبر اهتزازات الأفعال المعترف بها (0.8) أصغر من بدء الضاغط المعتاد (1.9) الذي لا يُسقط شيئاً، ومن 17:30 إلى السقوط لا اهتزاز، وورقة التوقيع لا تذكر أحداً بعد 17:30؛ فسقطت المنحوتة بلا تدخل.", ["KO-RS-05-009", "KO-RS-06-015"])
I("i_b_defect", [P("evidence", "ev_maintenance_ticket"), P("evidence", "ev_break_surface")], "fact", "f_shelf_defect", "establishes", "strong",
  "الطلب القديم يصف الصدع في الزاوية نفسها، وسطح الكسر مظلم مغبر في أوله فاتح في آخره؛ فبدأ الكسر من صدع قديم وانتهى بانهيار حديث.", ["KO-RS-06-009", "KO-RS-06-001"])
# claims and hypotheses
I("i_claim_nour", [P("evidence", "ev_thermal_log"), P("evidence", "ev_vib_log")], "claim", "cl_nour_bump", "contradicts_claim", "strong",
  "لمسة 16:40 سجّلت اهتزازاً صغيراً (0.4)، وبقيت المنحوتة ظاهرة في لقطات 16:45 وما بعدها بساعة تقريباً؛ فلم تُسقطها.", ["KO-RS-05-009", "KO-RS-05-014"])
I("i_claim_basel", [P("evidence", "ev_vib_log"), P("evidence", "ev_door_log")], "claim", "cl_basel_door", "contradicts_claim", "strong",
  "إغلاق الباب 17:12 سجّل 0.8 وهو دون اهتزاز المكيّف المعتاد، وبقيت المنحوتة بعده نحو ثلاثين دقيقة.", ["KO-RS-05-009", "KO-RS-05-014"])
I("i_claim_hala", [P("evidence", "ev_ac_log"), P("evidence", "ev_vib_log")], "claim", "cl_hala_ac", "contradicts_claim", "strong",
  "اهتزاز المكيّف 1.9 يتكرر كل يوم بلا سقوط، وبقيت المنحوتة بعده أكثر من عشرين دقيقة.", ["KO-RS-05-009", "KO-RS-05-014"])
I("i_claim_jad", [P("evidence", "ev_thermal_log"), P("evidence", "ev_door_log")], "claim", "cl_jad_turn", "contradicts_claim", "strong",
  "المنحوتة ظاهرة في لقطات 17:30 و17:35 و17:40 بعد تحريك القاعدة، وجاد خرج 17:30؛ فمرّ أكثر من عشر دقائق بين لمسته وسقوطها دون أن يكون أحد هناك.", ["KO-RS-05-009", "KO-RS-06-015"])
I("i_claim_maysa", [P("evidence", "ev_maintenance_ticket")], "claim", "cl_maysa_none", "contradicts_claim", "strong",
  "الطلب المؤجل موجود ومسجّل باسمها، فلا صحة لقولها إن لا طلب مفتوحاً.", ["KO-RS-05-014"])
I("i_support_defect", [P("fact", "f_no_act_caused"), P("fact", "f_shelf_defect")], "hypothesis", "h_defect", "supports", "strong",
  "إذا لم يسقطها أحد وكان في الرف عيب قديم، فانهيار الرف بعيبه هو التفسير الذي يجمع السجلات كلها.", ["KO-RS-06-009"])
I("i_rule_last", [P("fact", "f_no_act_caused")], "hypothesis", "h_last", "rules_out", "conclusive",
  "حتى لو كان جاد آخر من لمس المنحوتة، فقد بقيت سليمة بعد لمسته ثم سقطت والورشة خالية؛ فالتتابع لا يجعله السبب.", ["KO-RS-06-008"])
I("i_rule_sum", [P("fact", "f_no_act_caused")], "hypothesis", "h_sum", "rules_out", "strong",
  "لو كان التراكم هو السبب لسقطت المنحوتة وقت أكبر الأحمال، لا بعد أحد عشر دقيقة من الهدوء التام.", ["KO-RS-06-015"])
I("i_rule_sum_b", [P("evidence", "ev_vib_log"), P("evidence", "ev_ac_log")], "hypothesis", "h_sum", "rules_out", "strong",
  "أحمال الأفعال الأربعة أصغر من أحمال يومية متكررة، ولم تتراكم لأن المنحوتة بقيت بعد كل فعل بدرجة سلامتها نفسها.", ["KO-RS-06-015"])

# ---------------------------------------------------------------- character knowledge
K = lambda f, a="witnessed", c="certain": {"fact_id": f, "access": a, "certainty": c}
ck = [
    {"character_id": "nour", "knows": [K("f_nour_acts")], "hides": [], "believes": [{"claim_id": "cl_nour_bump", "stance": "sincere"}]},
    {"character_id": "basel", "knows": [K("f_basel_acts")], "hides": [], "believes": [{"claim_id": "cl_basel_door", "stance": "sincere"}]},
    {"character_id": "hala", "knows": [K("f_hala_acts")], "hides": [], "believes": [{"claim_id": "cl_hala_ac", "stance": "sincere"}]},
    {"character_id": "jad", "knows": [K("f_jad_acts")], "hides": [], "believes": [{"claim_id": "cl_jad_turn", "stance": "sincere"}]},
    {"character_id": "rita", "knows": [K("f_rita_found"), K("f_photo_exists")], "hides": [], "believes": []},
    {"character_id": "maysa", "knows": [K("f_thermal_exists", "professional"), K("f_door_log_exists", "professional"), K("f_vib_exists", "professional"), K("f_ac_log_exists", "professional")],
     "hides": [{"fact_id": "f_ticket_exists", "reveal_when": {"presented": {"evidence_id": "ev_incident_report", "to_character": "maysa"}}, "cover_claim_id": "cl_maysa_none", "reveal_line_id": "ms_ticket"}],
     "believes": [{"claim_id": "cl_maysa_none", "stance": "deliberate_lie"}]},
]
hyps = [
    {"id": "h_last", "statement_ar": "أسقطها جاد، فهو آخر من لمس المنحوتة واعترافه الأقرب إلى لحظة السقوط.", "is_true": False, "plausibility_at_start": "high", "suspect_id": "jad"},
    {"id": "h_defect", "statement_ar": "لم يسقطها أحد؛ انهار الرف لعيب قديم في قاعدته، وكل اعتراف كان خاطئاً بحسن نية.", "is_true": True, "plausibility_at_start": "low", "suspect_id": "maysa"},
    {"id": "h_sum", "statement_ar": "تراكمت الأفعال الأربعة (اللمسة والباب والمكيّف والتحريك) حتى أسقطت المنحوتة.", "is_true": False, "plausibility_at_start": "medium"},
]
mis = [
    {"id": "rh_report", "points_to_hypothesis_id": "h_sum", "planted_via_ar": "أربعة اعترافات متتالية في تقرير واحد، فيبدو أن الأفعال كلها حقيقية وتجتمع.", "evidence_ids": ["ev_incident_report"],
     "refuted_by_inference_ids": ["i_rule_sum", "i_rule_sum_b", "i_a_acts"],
     "fairness_note_ar": "الأفعال حقيقية لكنها لا تفسر السقوط: بقيت المنحوتة سليمة بعد كل فعل، وأحمالها أصغر من أحمال يومية، وسجلات الحساسات متاحة للاعب."},
    {"id": "rh_jad", "points_to_hypothesis_id": "h_last", "planted_via_ar": "اعتراف جاد الأخير يطابق الأقرب زمناً إلى السقوط، وهو آخر من غادر.", "evidence_ids": ["ev_jad_statement"],
     "refuted_by_inference_ids": ["i_rule_last", "i_claim_jad", "i_b_acts"],
     "fairness_note_ar": "الترتيب الزمني وحده لا يثبت سبباً: لقطات 17:30 و17:35 و17:40 تُظهر المنحوتة سليمة بعد لمسته، وخلت الورشة بعد خروجه."},
]
los = [
    {"id": "lo_confession", "statement_ar": "يعامل الاعتراف ادعاءً يحتاج تأييداً مستقلاً ولا يعدّه إثباتاً بذاته.", "skill_ko_ref": "KO-RS-05-009", "observable_behaviors_ar": ["يطلب سجلاً مستقلاً لكل اعتراف", "لا يقيس الصدق بنبرة المعترف"], "evidence_sources": ["evidence_board", "final_justification"]},
    {"id": "lo_causal", "statement_ar": "يفرّق بين التتابع في الزمن والسببية، ويطلب آلية ومقداراً.", "skill_ko_ref": "KO-RS-06-015", "observable_behaviors_ar": ["لا يحمّل آخر من لمس المنحوتة المسؤولية بسبب الترتيب", "يقارن الأحمال بالمعتاد"], "evidence_sources": ["evidence_board", "hypothesis_ledger"]},
    {"id": "lo_revise", "statement_ar": "يراجع الاعتقاد عند سقوط دليل، ولو كان في الأصل رواية متفقاً عليها.", "skill_ko_ref": "KO-RS-06-009", "observable_behaviors_ar": ["يغيّر فرضيته الرائدة بدليل"], "evidence_sources": ["hypothesis_ledger"]},
    {"id": "lo_hyp", "statement_ar": "يوازن بين فرضيات متنافسة ويستبعد ما تنقضه الأدلة.", "skill_ko_ref": "KO-RS-05-002", "observable_behaviors_ar": ["يضيف فرضيات", "يستبعد بدليل"], "evidence_sources": ["hypothesis_ledger"]},
    {"id": "lo_timeline", "statement_ar": "يرتّب الأحداث على خط زمني ليكشف أن الأفعال سبقت السقوط بفواصل.", "skill_ko_ref": "KO-RS-05-005", "observable_behaviors_ar": ["يضع الأدلة في أزمنتها"], "evidence_sources": ["timeline_task", "action_log"]},
    {"id": "lo_calib", "statement_ar": "يصوغ نسبة الترجيح بحدودها.", "skill_ko_ref": "KO-RS-06-021", "observable_behaviors_ar": ["يختار ثقة معقولة", "يذكر حدوداً"], "evidence_sources": ["final_justification"]},
]
def levels(d): return [{"score": i, "descriptor_ar": t} for i, t in enumerate(d)]
rub = {
    "reference_answer_ar": "لم يُسقط أحد المنحوتة، وكل الاعترافات الأربعة صادقة في نيتها خاطئة في ربطها بالسقوط. الأفعال حدثت فعلاً (لمسة، وباب، ومكيّف، وتحريك قاعدة)، لكن لقطات الكاميرا الحرارية تُظهر المنحوتة في مكانها بعد كل منها حتى 17:40، وسجل البطاقات وورقة التوقيع يثبتان خلو الورشة بعد 17:30، وجهاز الاهتزاز يسجّل أصغر مما يسجّله المكيّف كل يوم ثم هدوءاً تاماً إلى لحظة السقوط. وفي الرف عيب قديم موثق: خط شعري في صورة قبل خمسة أشهر، وطلب صيانة مؤجل، وسطح كسر قديم في جزء منه. فالأرجح أن الرف انهار بعيبه. حدود الاستنتاج: اللقطات متباعدة نحو خمس دقائق، ولا نعرف حمل الرف بدقة، ولا يمكن نفي أثر ضئيل جداً لأي لمسة، ويبقى سبب تأجيل الإصلاح مسألة إدارية لا أكثر.",
    "criteria": [
        {"id": "c_source", "name_ar": "تصنيف المصادر", "objective_ids": ["lo_confession"], "scored_by": "deterministic", "weight": 0.15, "levels": levels(["لم يصنّف", "أخطأ في الأغلب", "نصف صحيح", "معظمه صحيح", "كله صحيح"])},
        {"id": "c_conflict", "name_ar": "ترتيب الأفعال والسقوط على الخط الزمني", "objective_ids": ["lo_timeline"], "scored_by": "deterministic", "weight": 0.2, "levels": levels(["لم يضع شيئاً", "وضع قليلاً", "وضع نصفها صحيحاً", "معظمها", "كلها في موضعها"])},
        {"id": "c_links", "name_ar": "ربط الأدلة بالفرضيات", "objective_ids": ["lo_causal", "lo_confession"], "scored_by": "deterministic", "weight": 0.2, "levels": levels(["لا روابط", "قليلة", "نصفها صحيح", "معظمها", "كلها دقيقة"])},
        {"id": "c_uncertainty", "name_ar": "معايرة الثقة", "objective_ids": ["lo_calib"], "scored_by": "deterministic", "weight": 0.15, "levels": levels(["ثقة مفرطة", "حدود قليلة", "جزئية", "معقولة", "معايَرة كاملة"])},
        {"id": "c_revision", "name_ar": "مراجعة الرأي", "objective_ids": ["lo_revise"], "scored_by": "deterministic", "weight": 0.1, "levels": levels(["بقي على فرضية مرفوضة", "لم يعلن فرضية", "ثبت على فرضية سليمة", "غيّر بدليل", "غيّر بدليل ووثّق"])},
        {"id": "c_elimination", "name_ar": "استبعاد الفرضيات الخاطئة", "objective_ids": ["lo_hyp"], "scored_by": "deterministic", "weight": 0.1, "levels": levels(["لم يستبعد", "استبعد خطأً", "فرضية بدليل", "فرضيتين", "كل الخاطئة"])},
        {"id": "c_justification", "name_ar": "جودة الحجة المكتوبة", "objective_ids": ["lo_confession", "lo_causal"], "scored_by": "human", "weight": 0.1, "levels": levels(["لا حجة", "ادعاء بلا سند", "أدلة دون ربط", "ربط الأدلة بالاستنتاج", "ربط مع البدائل والحدود"])},
    ],
}
def H(id, lv, kind, text, trig, target=None, w=0.0):
    d = {"id": id, "level": lv, "kind": kind, "text_ar": text, "trigger": trig, "assessment_weight": w}
    if target: d["targets_inference_id"] = target
    return d
he = lambda e: {"has_evidence": e}
hints = [
    H("hg1", 1, "metacognitive", "حين يقول أكثر من شخص إنه الفاعل، ما الذي يقيس صدق كل قول غير نبرة صاحبه؟", {"always": True}, None, 0.02),
    H("hg2", 2, "focus_area", "لكل اعتراف اسأل: ما الذي بقي في مكانه بعد الفعل، وكم دقيقة مرّت قبل السقوط؟", he("ev_incident_report"), None, 0.04),
    H("ha1", 1, "metacognitive", "ما الذي كانت حرارة الكاميرا تراه بعد كل فعل؟", he("ev_incident_report"), "i_a_acts", 0.02),
    H("ha2", 2, "pointer", "اسأل ميساء عن أجهزة الورشة، ثم رتّب لقطات الكاميرا وسجل الباب على خط واحد.", he("ev_incident_report"), "i_a_acts", 0.06),
    H("hb1", 1, "metacognitive", "هل اهتزاز الباب أكبر مما يحدث كل يوم أم أصغر؟", he("ev_incident_report"), "i_b_acts", 0.02),
    H("hb2", 2, "pointer", "قارن أرقام جهاز الاهتزاز بأرقام المكيّف المعتادة، وانظر إلى ما بعد الخامسة والنصف.", he("ev_incident_report"), "i_b_acts", 0.06),
    H("hd1", 1, "metacognitive", "ماذا لو كان الرف نفسه هو ما تغيّر قبل أشهر؟ أين يمكن أن يبقى أثر لذلك؟", he("ev_incident_report"), "i_b_defect", 0.02),
    H("hd2", 2, "pointer", "افحص موضع الكسر بنفسك، واسأل ريتا عن صور الرف قبل الحادثة.", he("ev_incident_report"), "i_b_defect", 0.06),
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
Act("a_read_report", "examine", "اقرأ تقرير المشرفة الأول", al, [G("ev_incident_report")], "loc_hall", "READ_REPORT")
Act("a_read_signout", "examine", "اقرأ ورقة الحضور عند باب الورشة", al, [G("ev_signout_sheet")], "loc_door", "READ_SIGNOUT")
Act("a_inspect_break", "search_location", "افحص موضع الكسر في قاعدة الرف", al, [G("ev_break_surface")], "loc_workshop", "INSPECT_BREAK")
for cid, lab in [("nour", "نور"), ("basel", "باسل"), ("hala", "هالة"), ("jad", "جاد"), ("rita", "ريتا"), ("maysa", "ميساء")]:
    Act(f"a_int_{cid}", "interview", f"ابدأ مقابلة {lab}", al, [{"op": "raise_trust", "ref_id": cid, "amount": 1}], cid, f"INT_{cid.upper()}")
Act("a_get_thermal", "examine", "اطلب سجل الكاميرا الحرارية", fu("f_thermal_exists"), [G("ev_thermal_log")], "loc_office", "GET_THERMAL")
Act("a_get_door", "examine", "اطلب سجل بطاقات الباب", fu("f_door_log_exists"), [G("ev_door_log")], "loc_office", "GET_DOOR")
Act("a_get_vib", "examine", "اطلب سجل جهاز الاهتزاز", fu("f_vib_exists"), [G("ev_vib_log")], "loc_office", "GET_VIB")
Act("a_get_ac", "examine", "اطلب سجل متحكم المكيّف", fu("f_ac_log_exists"), [G("ev_ac_log")], "loc_office", "GET_AC")
Act("a_get_photo", "examine", "اطلب صورة المعرض السابق من ريتا", fu("f_photo_exists"), [G("ev_crack_photo")], "loc_workshop", "GET_PHOTO")
Act("a_get_ticket", "examine", "اطلب طلب الصيانة القديم", fu("f_ticket_exists"), [G("ev_maintenance_ticket")], "loc_office", "GET_TICKET")
Act("a_note_nour", "examine", "دوّن إفادة نور", fu("f_nour_acts"), [G("ev_nour_statement")], "nour", "NOTE_NOUR")
Act("a_note_basel", "examine", "دوّن إفادة باسل", fu("f_basel_acts"), [G("ev_basel_statement")], "basel", "NOTE_BASEL")
Act("a_note_hala", "examine", "دوّن إفادة هالة", fu("f_hala_acts"), [G("ev_hala_statement")], "hala", "NOTE_HALA")
Act("a_note_jad", "examine", "دوّن إفادة جاد", fu("f_jad_acts"), [G("ev_jad_statement")], "jad", "NOTE_JAD")
Act("a_note_rita", "examine", "دوّن إفادة ريتا", fu("f_rita_found"), [G("ev_rita_statement")], "rita", "NOTE_RITA")
Act("p_report_maysa", "present_evidence", "اعرض تقرير الحادثة على ميساء", {"presented": {"evidence_id": "ev_incident_report", "to_character": "maysa"}}, [{"op": "emit_event", "ref_id": "PRESENTED_REPORT_MAYSA"}], "maysa", "P_REPORT_MAYSA", 0)
Act("a_hint", "request_hint", "اطلب تلميحاً", al, [], None, "REQUEST_HINT", 0)
Act("a_accuse", "final_accusation", "قدّم الاستنتاج النهائي", al, [{"op": "emit_event", "ref_id": "SUBMIT"}], None, "FINAL_ACCUSATION", 0)

topics = [
    {"id": "t_nour", "label_ar": "ما فعلته نور", "example_questions_ar": ["ماذا فعلتِ قرب الرف؟", "لماذا اعترفتِ؟"], "fact_ids": ["f_nour_acts"], "claim_ids": ["cl_nour_bump"]},
    {"id": "t_basel", "label_ar": "ما فعله باسل", "example_questions_ar": ["ماذا فعلت عند الباب؟", "لماذا اعترفت؟"], "fact_ids": ["f_basel_acts"], "claim_ids": ["cl_basel_door"]},
    {"id": "t_hala", "label_ar": "ما فعلته هالة", "example_questions_ar": ["ماذا فعلتِ بالمكيّف؟", "لماذا اعترفتِ؟"], "fact_ids": ["f_hala_acts"], "claim_ids": ["cl_hala_ac"]},
    {"id": "t_jad", "label_ar": "ما فعله جاد", "example_questions_ar": ["ماذا فعلت قبل الخروج؟", "لماذا اعترفت؟"], "fact_ids": ["f_jad_acts"], "claim_ids": ["cl_jad_turn"]},
    {"id": "t_found", "label_ar": "اكتشاف الحطام وصور الرف", "example_questions_ar": ["متى وجدتِ الحطام؟", "هل لديكِ صور للرف؟"], "fact_ids": ["f_rita_found", "f_photo_exists"]},
    {"id": "t_devices", "label_ar": "أجهزة الورشة", "example_questions_ar": ["ما الأجهزة التي تسجّل في الورشة؟", "هل يوجد سجل لكل منها؟"], "fact_ids": ["f_thermal_exists", "f_door_log_exists", "f_vib_exists", "f_ac_log_exists"]},
    {"id": "t_repair", "label_ar": "صيانة الرف", "example_questions_ar": ["هل هناك طلبات صيانة للرف؟", "ماذا كان في الطلب القديم؟"], "fact_ids": ["f_ticket_exists"], "claim_ids": ["cl_maysa_none"]},
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
    (1, "لا يكفي أن يتفق أربعة أقوال: كل اعتراف ادعاء يُقاس بسجل مستقل. وقد جُمعت سجلات ترى الورشة من جهات مختلفة.", ["ev_incident_report", "ev_thermal_log"], "i_a_acts"),
    (2, "الكاميرا الحرارية تُظهر المنحوتة في مكانها بعد كل فعل حتى 17:40، وسجل الباب يثبت خلو الورشة منذ 17:30؛ فسقطت بلا حضور أحد.", ["ev_thermal_log", "ev_door_log"], "i_a_acts"),
    (3, "مسار مستقل: جهاز الاهتزاز يسجّل لكل فعل معترف به أقل من بدء المكيّف اليومي، ثم هدوءاً تاماً قبل السقوط، وورقة الحضور تؤيد خلو الورشة.", ["ev_vib_log", "ev_signout_sheet"], "i_b_acts"),
    (4, "ظن آخر المعترفين أنه السبب لأنه آخر من لمسها، لكن الترتيب الزمني لا يصنع سبباً: مرّت أكثر من عشر دقائق دون أحد.", ["ev_thermal_log", "ev_door_log"], "i_rule_last"),
    (5, "العيب القديم: صورة قبل خمسة أشهر تُظهر خطاً في زاوية القاعدة.", ["ev_crack_photo"], "i_a_defect"),
    (6, "ومسار مستقل للعيب: طلب صيانة مؤجل يصف الصدع نفسه، وسطح كسر قديم في جزئه الأول.", ["ev_maintenance_ticket", "ev_break_surface"], "i_b_defect"),
    (7, "إذن الأرجح أن الرف انهار لعيبه القديم؛ والمسؤولية مؤسسية: نظام تأجيل الطلبات بلا مراجعة، لا طالب بعينه.", ["ev_maintenance_ticket", "ev_break_surface"], "i_support_defect"),
]
ending = {
    "steps": [{"order": o, "text_ar": t, "uses_evidence_ids": u, "inference_id": i} for o, t, u, i in steps],
    "alternative_paths_ar": [
        "يمكن الوصول إلى النتيجة من الكاميرا الحرارية وسجل الباب وصورة الرف وحدها دون جهاز الاهتزاز، لكن من يفعل ذلك يترك أرقام الاهتزاز بلا تفسير أمام من يعترف بالباب أو المكيّف.",
        "ويمكن الوصول إليها من جهاز الاهتزاز وورقة الحضور وطلب الصيانة وفحص الكسر وحدها، والأقوى أن يتفق المساران.",
    ],
    "what_evidence_could_not_show_ar": [
        "لقطات الكاميرا متباعدة نحو خمس دقائق، فلا تحدد لحظة السقوط بدقة ثوانٍ.",
        "لا نعرف الحمل الذي كان يحتمله الرف بدقة، ولا يمكن نفي أثر ضئيل جداً لأي لمسة.",
        "لا تثبت الأدلة لماذا صُنّف الطلب منخفض الأولوية، ولا أن تأجيله وحده هو سبب الانهيار.",
    ],
    "science_notes_ar": [
        "الاعتراف ادعاء يحتاج تأييداً مستقلاً كغيره: قد يكون صادق النية وخاطئ الوقائع لأسباب منها حسن النية والظن بالمسؤولية والرغبة في حماية الآخر. وهذه ظاهرة موثقة في البحث وراء حالات حقيقية خطيرة، فلا نهوّن منها هنا لأن قضيتنا خيالية صغيرة.",
        "التتابع الزمني ليس سببية: يلزم أن نسأل عن الآلية وعن المقدار قياساً بالمعتاد.",
        "صدق نبرة المعترف أو ارتباكه لا يدل على صحة اعترافه ولا على بطلانه؛ المقياس هو السجلات المستقلة وسلسلة العهدة لها، ثم نسبة الترجيح بحدودها.",
        "بطاقة الأصل (حكاية شعبية عابرة للثقافات): استُلهمت بنية «سلسلة الاعترافات» فقط، وأُعيد بناء القضية كلها دون جسد ولا هويات ولا سخرية.",
    ],
}
core = {
    "schema_version": "0.1.0", "case_id": CID, "case_version": "0.1.0",
    "meta": {"title_ar": "الكل يعترف ولا أحد فعلها", "title_en": "Everyone Confessed and Nobody Did It", "age_band": "16-18", "locale": "ar", "dialogue_register": "msa", "estimated_minutes": 35, "difficulty": 3,
             "content_flags": ["no_violence", "science_lab"], "authors": ["فريق أثر التحريري (مسودة بمساعدة الذكاء الاصطناعي، لم تُراجَع بشرياً بعد)"],
             "knowledge_object_refs": ["KO-RS-05-009", "KO-RS-06-015", "KO-RS-06-009", "KO-RS-06-001", "KO-RS-05-005", "KO-RS-05-002", "KO-RS-06-021", "KO-RS-05-014"]},
    "premise": {"hook_ar": "سقطت منحوتة زجاجية قبل المعرض، وقال أربعة طلاب واحداً بعد الآخر إنهم السبب. كلٌّ منهم يظن أنه يحمي سواه.",
                "player_role_ar": "أنت مراجع في ورشة فنون المرسى، وطُلب منك أن تقول ما تثبته السجلات قبل أن يُغلق الملف على الاعترافات.",
                "setting_ar": "ورشة الفنون في المرسى، عصر يوم الخميس. أوقات الأجهزة وبطاقات الباب بتوقيت الورشة.",
                "public_fact_ids": ["f_sculpture_fell", "f_four_confessed", "f_voluntary"],
                "assumed_general_knowledge_ar": ["الاعتراف قول يحتاج إلى ما يؤيده", "الجسم الساكن لا يسقط بلا سبب في لحظة محددة"]},
    "entities": {"characters": chars, "locations": locations, "objects": objects, "organizations": orgs},
    "truth": {"solution": {"culprit_ids": ["maysa"], "summary_ar": "لم يُسقط أحد المنحوتة. الأفعال الأربعة المعترف بها وقعت، لكن المنحوتة بقيت قائمة بعدها، وسقطت حين كانت الورشة خالية. انهارت القاعدة عند صدع قديم أُجِّل إصلاحه إدارياً، وكانت الاعترافات صادقة النية خاطئة في تحديد السبب.", "key_fact_ids": ["f_no_act_caused", "f_shelf_defect"]},
              "facts": facts, "claims": claims},
    "timeline": timeline, "evidence": ev, "evidence_graph": {"inferences": inf},
    "character_knowledge": ck, "hypotheses": hyps, "misdirection_plan": mis, "learning_objectives": los,
    "mechanics": {"time_budget_units": 45, "actions": A},
    "state_machine": {"id": "c019", "initial": "briefing", "type": "compound", "states": {
        "briefing": {"description_ar": "الإحاطة", "type": "atomic", "on": {"START": {"target": "investigating"}}},
        "investigating": {"description_ar": "التحقيق", "type": "compound", "initial": "gathering",
                          "states": {"gathering": {"type": "atomic", "on": {"OPEN_DEDUCTION": {"target": "deducing"}}}, "deducing": {"type": "atomic", "on": {"BACK": {"target": "gathering"}}}},
                          "on": {"SUBMIT": {"target": "review"}}},
        "review": {"description_ar": "مراجعة", "type": "atomic", "on": {"CLOSE": {"target": "resolved"}}},
        "resolved": {"description_ar": "إغلاق", "type": "final"}}},
    "dialogue": {"max_turns_per_interview": 10, "llm_enabled": False, "topics": topics},
    "rubric": rub, "hint_ladder": hints,
    "fairness_test": {"requirements": {"min_disjoint_proof_paths": 2, "max_inference_depth": 3, "all_red_herrings_refutable": True, "culprit_uniquely_entailed": True, "no_hidden_fact_dependency": True, "max_required_actions": 45}, "runs": []},
    "ending_explanation": ending,
    "expert_review": [{"role": r, "reviewer": "—", "status": "pending", "content_hash": "unbound", "date": "2026-10-27", "notes_ar": "بانتظار مراجعة بشرية؛ لم يُجرَ أي اعتماد."} for r in
                      ["narrative_editor", "scientific_reviewer", "learning_designer", "age_appropriateness", "cultural_reviewer", "legal_rights", "safety"]],
}
ui = {
    "case_id": CID,
    "clock": {"epoch_hhmm": "16:00", "zone_label_ar": "توقيت الورشة"},
    "cover": {"title_ar": "الكل يعترف ولا أحد فعلها", "tagline_ar": "أربعة اعترافات، ومنحوتة واحدة سقطت", "kicker_ar": "الملف التاسع عشر · الاعتراف ادعاء", "glyph": "◇", "accent": "amber"},
    "cold_open_ar": ["الخميس، قبل المعرض بأيام.", "منحوتة زجاجية استغرق إعدادها أشهراً سقطت عن الرف وتشظّت. لم يُصب أحد.", "في اجتماع المساء رفع أربعة طلاب أيديهم واحداً بعد الآخر: كل منهم يظن أن فعلاً صغيراً منه هو السبب.", "المشرفة مستعدة لإغلاق الملف. ابدأ بسؤال: ما الذي يجعل اعترافاً مقبولاً؟ وهل هذا يكفي؟"],
    "labs": [],
    "source_classes": [
        {"id": "primary_record", "label_ar": "سجل أصلي", "help_ar": "يُنتجه جهاز أو شخص لحظة الحدث دون وسيط، كسجل كاميرا أو بطاقات أو طلب صيانة."},
        {"id": "redisplay", "label_ar": "نسخة معروضة", "help_ar": "معلومة نُقلت من سجل آخر أو أُعيد عرضها، كملخص تقرير."},
        {"id": "claim", "label_ar": "قول أو تصريح", "help_ar": "إفادة أو اعتراف؛ يُقاس بالسجلات المستقلة لا بنبرة صاحبه."},
        {"id": "template", "label_ar": "قالب أو نموذج", "help_ar": "نص جاهز لا يصف الحدث الفعلي بذاته."},
        {"id": "public_document", "label_ar": "وثيقة منشورة", "help_ar": "وثيقة معلنة ومعروف ناشرها."}],
    "limit_menu": [
        {"id": "l_frame_gap", "label_ar": "لقطات الكاميرا متباعدة نحو خمس دقائق فلا تحدد لحظة السقوط بدقة ثوانٍ"},
        {"id": "l_load", "label_ar": "لا نعرف الحمل الذي كان يحتمله الرف، فنثبت وجود العيب لا مقدار أثره"},
        {"id": "l_tiny_touch", "label_ar": "لا يمكن نفي أثر ضئيل جداً لأي لمسة، ولا دليل على أنها أسقطت المنحوتة"},
        {"id": "l_invalid_sincere", "label_ar": "صدق نبرة المعترفين يثبت أن اعترافاتهم صحيحة"},
        {"id": "l_invalid_count", "label_ar": "كثرة المعترفين تقوّي كل اعتراف على حدة"}],
    "mind_change_menu": [
        {"id": "m_late_entry", "label_ar": "ظهور من دخل الورشة بعد 17:30 دون تمرير بطاقة"},
        {"id": "m_thermal_tilt", "label_ar": "لقطة حرارية قبل 17:40 تُظهر الرف مائلاً أو المنحوتة غائبة"},
        {"id": "m_photo_date", "label_ar": "ثبوت أن بيانات صورة الصدع مؤرخة خطأً"},
        {"id": "m_popular", "label_ar": "إجماع الطلاب على رواية واحدة"}],
    "skills": [{"skill_id": "KO-RS-05-009", "track": "B"}, {"skill_id": "KO-RS-06-015", "track": "D"}, {"skill_id": "KO-RS-06-009", "track": "D"}],
    "stage_hooks_ar": {"briefing": "أربعة يعترفون ولا أحد متأكد… فهل يكفي الاعتراف؟", "investigating": "كل اعتراف ادعاء. ما الذي يقوله الجهاز الذي لا يجامل أحداً؟", "review": "قبل أن تغلق الملف: ما الذي لا تعرفه؟", "resolved": "أُغلق الملف. ملف جديد ينتظر في الأرشيف."},
    "character_glyphs": {"nour": "ن", "basel": "ب", "hala": "هـ", "jad": "ج", "rita": "ر", "maysa": "م"},
}
sc = {
    "case_id": CID,
    "accepted_conclusions": {"h_defect": {"grade": 1, "note_ar": "استنتاج متسق مع الأدلة ويتطلب ذكر حدوده."},
                             "h_last": {"grade": 0, "note_ar": "يبني السبب على الترتيب الزمني وحده ويتجاهل بقاء المنحوتة بعد لمسته وخلو الورشة."},
                             "h_sum": {"grade": 0, "note_ar": "الأفعال أصغر من أحمال يومية متكررة، ولم تتراكم لأن المنحوتة بقيت سليمة بعد كل منها."}},
    "confidence_band": {"h_defect": [65, 90], "h_last": [0, 15], "h_sum": [0, 15]},
    "source_key": {"ev_incident_report": "redisplay", "ev_nour_statement": "claim", "ev_basel_statement": "claim", "ev_hala_statement": "claim", "ev_jad_statement": "claim", "ev_rita_statement": "claim",
                   "ev_thermal_log": "primary_record", "ev_door_log": "primary_record", "ev_signout_sheet": "primary_record", "ev_vib_log": "primary_record", "ev_ac_log": "primary_record",
                   "ev_crack_photo": "primary_record", "ev_maintenance_ticket": "primary_record", "ev_break_surface": "primary_record"},
    "link_key": {
        "h_defect": {"ev_thermal_log": "supports", "ev_door_log": "supports", "ev_vib_log": "supports", "ev_signout_sheet": "supports", "ev_crack_photo": "supports", "ev_maintenance_ticket": "supports", "ev_break_surface": "supports", "ev_incident_report": "neutral"},
        "h_last": {"ev_jad_statement": "supports", "ev_thermal_log": "weakens", "ev_door_log": "weakens", "ev_vib_log": "weakens"},
        "h_sum": {"ev_incident_report": "supports", "ev_vib_log": "weakens", "ev_ac_log": "weakens", "ev_thermal_log": "weakens", "ev_break_surface": "weakens"},
    },
    "required_limits": ["l_frame_gap", "l_load"], "valid_mind_changers": ["m_late_entry", "m_thermal_tilt", "m_photo_date"],
    "invalid_limits": ["l_invalid_sincere", "l_invalid_count"],
    "decisive_evidence": ["ev_thermal_log", "ev_door_log", "ev_vib_log", "ev_signout_sheet", "ev_crack_photo", "ev_maintenance_ticket", "ev_break_surface"],
    "lab_requirement": None,
    "timeline_requirement": [{"evidence_id": "ev_door_log", "utc_minute": 90, "tol": 3}, {"evidence_id": "ev_vib_log", "utc_minute": 101, "tol": 3}, {"evidence_id": "ev_rita_statement", "utc_minute": 115, "tol": 5}],
    "refuted_hypotheses": ["h_last", "h_sum"],
    "criteria_map": {"c_source": "source_typing", "c_conflict": "conflict_resolution", "c_links": "hypothesis_links", "c_uncertainty": "uncertainty", "c_revision": "revision", "c_elimination": "elimination", "c_justification": "justification_human"},
    "caps": {"no_citations_max": 45, "no_conflict_resolution_max": 70},
}
os.makedirs(OUT, exist_ok=True)
for suf, obj in [("", core), (".ui", ui), (".scoring", sc)]:
    with open(os.path.join(OUT, f"{CID}{suf}.json"), "w", encoding="utf8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
print("ok")
