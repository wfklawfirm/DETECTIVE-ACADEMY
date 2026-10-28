#!/usr/bin/env python3
# Case c024 «الدراجة الحمراء والسؤال الذي غيّر الوصف» — archetype ARC-15 «السؤال الذي زرع ذكرى», age band 16-18, difficulty 3.
# Teaches: a witness account can be CONTAMINATED by a leading question; the investigator must find the earliest, uncontaminated account (recorded
# before the suggestion), compare it with the later one, and separate a witness's CONFIDENCE (which rose) from the ACCURACY of the description (which fell).
# A small child is the witness: the case treats her gently (no pressure, a parent is present) and never blames her. Two independent chains reach the
# same facts: (1) a message sent by her mother before any suggestion + the interview record with its exact questions, and (2) the mother's and the
# vice-principal's own statements; (3) a gate-camera still + the janitor's closing-round sheet, and (4) the brother's text + the stewards' duty sheet.
# No-culprit convention: the older brother who borrowed the bike in good faith and forgot to tell (Karim) is recorded in culprit_ids; the janitor (Anwar)
# did nothing; the vice-principal's question was careless, not malicious.
# DEVIATIONS from ARC-15 (honest list): the archetype measures HOW THE PLAYER asks (ratio of open to leading questions, contamination events caused by the
# player). The engine has no free-form question-design mechanic, and the dialogue is a fixed topic list with authored lines, so no option exists to ask a
# leading question: every topic the player can pick is open, and contamination is modelled as something that already happened in the story, which the
# player must detect from the records. The «first-trust preservation» observable is therefore carried by the scoring of source typing and hypothesis links,
# not by a counter of player questions. The 13-15 variant (a pre-labelled question bank) is not built.
# Calendar (fictional): minute 0 = Thursday 15:00. Thu 16:05 = 65; 16:08 = 68; 16:21 = 81; 17:05 = 125; 17:30 = 150; 17:40 = 160; Fri 09:00 = 1080.
# Usage: gen_c024.py OUT_DIR
import sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
from _lib_c022_c025 import *

OUT = sys.argv[1]
CID = "c024_red_bicycle"
c = Case(CID)

# ---------------------------------------------------------------- characters
c.ch("yara", "يارا الخطيب", "witness", "طالبة في الصف الخامس، شاهدة صغيرة",
     "هادئة وخجولة، تجيب بجمل قصيرة وتنسى التفاصيل إذا طُلب منها تخمين. تحاول إرضاء الكبار وتقول «نعم» إذا شعرت أنهم يريدونها. تتحدث أفضل حين تروي بكلماتها.",
     ["ألا تخطئ أمام الكبار", "أن تفهم لماذا يسألونها"],
     [L("yr_greet", "greeting", "أمي معي، وأنا أتكلم بهدوء."),
      L("yr_saw", "reveal", "رأيت ولداً سترته خضراء يأخذ دراجة حمراء من عند البوابة الجانبية، وكان يضحك.", ["f_yara_saw"]),
      L("yr_mom", "reveal", "أخبرت أمي فوراً بما رأيت، وهي كتبت رسالة إلى مجموعة أولياء الأمور.", ["f_told_mother"]),
      L("yr_beard", "reveal", "بعد ذلك سألوني عن عمّ أنور، فقلت إنه ربما كان طويلاً وبلحية، لكنني لست متأكدة الآن.", None, ["cl_yara_beard"]),
      L("yr_unknown", "deflect_unknown", "لا أتذكر أكثر."),
      L("yr_off", "deflect_offtopic", "اسألني عمّا رأيته عند البوابة."),
      L("yr_bye", "farewell", "هل أستطيع أن أذهب مع أمي؟")])
c.ch("salma", "سلمى الخطيب", "witness", "والدة يارا",
     "حنون وحريصة على ابنتها، تتذكر ما قيل بدقة لأنها كتبته على هاتفها، وتتألم من الضغط على طفلة. تقول ما سمعته ولا تحكم على أحد.",
     ["حماية ابنتها", "ألا يُظلم أحد بسبب كلمات طفلة"],
     [L("sa_greet", "greeting", "ابنتي صادقة، لكنها صغيرة."),
      L("sa_says", "reveal", "قالت لي يارا «ولد» ولم تقل «رجل»، وكتبت ذلك في رسالتي. وفي المقابلة سألها الأستاذ إن كان طويلاً وبلحية فقالت «ربما».", ["f_mother_says"]),
      L("sa_unknown", "deflect_unknown", "لا أعرف أكثر."),
      L("sa_off", "deflect_offtopic", "اسأل عن ابنتي وما قالته."),
      L("sa_bye", "farewell", "أريدها أن تطمئن.")])
c.ch("fadi", "فادي العلي", "authority", "وكيل المدرسة المسؤول عن الانضباط",
     "جاد وسريع القرار، يظن أن الشاهدة تقول الحقيقة إذا كانت واثقة. يقدّر أنه لم يقصد الإيحاء، ويراجع حين يرى النص الحرفي لأسئلته.",
     ["حماية ممتلكات الطلاب", "ألا يتهم أحداً ظلماً"],
     [L("fd_greet", "greeting", "الشاهدة متأكدة تماماً، وهذا يكفيني."),
      L("fd_asked", "reveal", "سألت يارا عن عمّ أنور لأنه المسؤول عن ترتيب الدراجات؛ لم أقصد الإيحاء.", ["f_vp_asked"], ["cl_vp_sure"]),
      L("fd_cam", "reveal", "كاميرا البوابة الجانبية تلتقط صورة كل دقيقة، ويمكنني أن أخرج لك لقطات تلك الفترة.", ["f_camera_stills"]),
      L("fd_unknown", "deflect_unknown", "هذا ليس عندي."),
      L("fd_off", "deflect_offtopic", "اسألني عن المقابلة والكاميرا."),
      L("fd_bye", "farewell", "أريد قراراً عادلاً.")])
c.ch("hind", "هند الصباغ", "witness", "مرشدة نفسية في المدرسة، حضرت المقابلة",
     "هادئة ومنظمة، تدوّن حرفياً ما يُقال ولا تفسّره. تهتم براحة الطفلة قبل كل شيء.",
     ["أن تكون المقابلة آمنة للطفلة", "أن يبقى المحضر دقيقاً"],
     [L("hd_greet", "greeting", "دوّنت المقابلة كما جرت."),
      L("hd_notes", "reveal", "كتبت أسئلة الأستاذ فادي وأجوبة يارا بحروفها، ومعها ملاحظتي على كل جواب.", ["f_transcript_exists"]),
      L("hd_unknown", "deflect_unknown", "لا أعرف غير ما دوّنته."),
      L("hd_off", "deflect_offtopic", "اسأل عن المحضر."),
      L("hd_bye", "farewell", "المحضر أمامكم.")])
c.ch("anwar", "أنور الدهان", "suspect", "عامل في المدرسة منذ سنوات، طويل القامة وله لحية",
     "هادئ ومحرج من أن يُذكر اسمه، يجيب بإيجاز ويذكر ما يوقّعه. توتره ليس دليلاً على شيء.",
     ["ألا يفقد عمله", "أن يُنصَف"],
     [L("an_greet", "greeting", "أنا لم آخذ شيئاً. اسألوني."),
      L("an_round", "reveal", "كنت مناوباً عند باب القاعة الكبرى من الرابعة إلى الرابعة والنصف، ثم قمت بجولة الإغلاق نحو الخامسة والنصف وكتبتها في ورقتي.", ["f_steward_duty", "f_return_round"]),
      L("an_warn", "reveal", "نعم، تلقيت تنبيهاً شفهياً عام 2022 لأنني نقلت دراجات دون إذن مكتوب أثناء حفل.", ["f_old_warning"]),
      L("an_unknown", "deflect_unknown", "لا أعرف."),
      L("an_off", "deflect_offtopic", "اسألني عن عملي في المعرض."),
      L("an_bye", "farewell", "أرجو ألا يتضرر عملي.")])
c.ch("karim", "كريم حداد", "suspect", "طالب في الصف الأخير، أخو آدم",
     "ودود ومتعجل، ينسى الاستئذان أحياناً ويعتذر بسهولة. يقول ما فعله بلا لف.",
     ["ألا يتورط أحد بسببه", "أن يصلح ما فعل"],
     [L("kr_greet", "greeting", "أظن أنني السبب. دعني أشرح."),
      L("kr_says", "reveal", "أخذت دراجة أخي بمفتاح الاحتياط لأوصل لوحة الفريق إلى المطبعة، وكتبت له، وأعدتها قبل الخامسة ونسيت أن أتأكد أنه قرأ.", ["f_karim_says"]),
      L("kr_unknown", "deflect_unknown", "لا أعرف أكثر."),
      L("kr_off", "deflect_offtopic", "اسألني عن الدراجة."),
      L("kr_bye", "farewell", "سأعتذر لعمّ أنور.")])
c.ch("adam", "آدم حداد", "victim", "طالب في الصف التاسع، صاحب الدراجة",
     "صريح وغاضب في البداية، ثم يهدأ حين يرى الأدلة. يغلق هاتفه أثناء المعرض.",
     ["أن يعرف من أخذ دراجته", "ألا يتهم أحداً بلا دليل"],
     [L("ad_greet", "greeting", "دراجتي اختفت، ثم ظهرت. أريد أن أفهم."),
      L("ad_text", "reveal", "فتحت هاتفي بعد المعرض فوجدت رسالة من أخي كريم عن دراجتي، وصلتني قبل أن أقرأها بساعة ونصف.", ["f_adam_text"]),
      L("ad_unknown", "deflect_unknown", "لا أعرف أكثر."),
      L("ad_off", "deflect_offtopic", "اسألني عن دراجتي."),
      L("ad_bye", "farewell", "أريد أن ننتهي من هذا.")])

locations = [{"id": "loc_gate", "name_ar": "البوابة الجانبية وحامل الدراجات", "description_ar": "بوابة فيها كاميرا تلتقط صورة كل دقيقة، وبجانبها حامل الدراجات."},
             {"id": "loc_hall", "name_ar": "باب القاعة الكبرى", "description_ar": "موقع مناوبة مضيفي المعرض."},
             {"id": "loc_office", "name_ar": "مكتب وكيل المدرسة", "description_ar": "حيث تُجرى المقابلات وتُحفظ الملفات."}]
objects = [{"id": "obj_bike", "name_ar": "الدراجة الحمراء رقم 14", "description_ar": "دراجة آدم، تُقفل بسلسلة ومفتاح."}]
orgs = [{"id": "org_school", "name_ar": "مدرسة القنطرة", "description_ar": "مدرسة خيالية تقيم معرضاً مفتوحاً."}]

# ---------------------------------------------------------------- facts
c.F("f_bike_missing", "اختفت دراجة آدم الحمراء من حامل البوابة الجانبية عصر الخميس ثم ظهرت في مكانها قبل الخامسة والنصف.", "event", ["obj_bike", "adam"], 0, T(68), "loc_gate")
c.F("f_anwar_named", "نسب وكيل المدرسة أخذ الدراجة إلى العامل أنور بعد مقابلة شاهدة صغيرة.", "attribute", ["fadi", "anwar"], 0)
c.F("f_anwar_denies", "ينفي أنور أنه أخذ الدراجة.", "attribute", ["anwar"], 0)
c.F("f_yara_saw", "قالت يارا إنها رأت ولداً بسترة خضراء يأخذ دراجة حمراء من البوابة الجانبية ويضحك.", "attribute", ["yara"], 1, T(68), "loc_gate")
c.F("f_told_mother", "أخبرت يارا أمها بما رأت فوراً، فكتبت الأم رسالة إلى مجموعة أولياء الأمور 16:21.", "event", ["yara", "salma"], 1, T(81))
c.F("f_mother_says", "تقول الأم إن ابنتها قالت «ولد» ولم تقل «رجل»، وإنها أجابت «ربما» عن سؤال اللحية في المقابلة.", "attribute", ["salma", "yara"], 1, T(160), "loc_office")
c.F("f_vp_asked", "سأل الوكيل يارا في المقابلة هل كان الرجل طويلاً بلحية مثل أنور، ثم دوّن لاحقاً أنها متأكدة تماماً.", "event", ["fadi", "yara"], 1, T(160), "loc_office")
c.F("f_transcript_exists", "دوّنت المرشدة المقابلة حرفياً: أسئلة الوكيل وأجوبة يارا وملاحظة على كل جواب.", "state", ["hind"], 1, T(160), "loc_office")
c.F("f_camera_stills", "تلتقط كاميرا البوابة الجانبية صورة كل دقيقة وتحتفظ بها.", "state", ["fadi"], 1, None, "loc_gate")
c.F("f_return_round", "دوّن أنور في ورقة جولة الإغلاق حالة الدراجات على الحامل ومنها الدراجة الحمراء.", "event", ["anwar", "obj_bike"], 1, T(125), "loc_gate")
c.F("f_steward_duty", "ناوب أنور عند باب القاعة الكبرى وفق ورقة مناوبة وقّعتها منسقة المعرض.", "state", ["anwar"], 1, T(60, "exact", 90), "loc_hall")
c.F("f_old_warning", "تلقى أنور تنبيهاً شفهياً عام 2022 لنقله دراجات دون إذن مكتوب.", "event", ["anwar"], 1)
c.F("f_adam_text", "وجد آدم بعد المعرض رسالة من أخيه كريم عن دراجته وصلت قبل أن يقرأها بساعة ونصف.", "event", ["adam", "karim"], 1, T(65))
c.F("f_karim_says", "يقول كريم إنه أخذ الدراجة بمفتاح الاحتياط ليوصل لوحة إلى المطبعة وأعادها دون أن يتأكد أن أخاه قرأ رسالته.", "attribute", ["karim", "obj_bike"], 1, T(68), "loc_gate")
c.F("f_youth_took", "الذي أخذ الدراجة فتى بسترة خضراء من أسرة صاحبها، لا رجل بلحية ولا غريب، وقد أعادها إلى مكانها خلال ساعة تقريباً.", "event", ["obj_bike", "karim"], 3, T(68, "exact", 125), "loc_gate", ["KO-RS-05-004", "KO-RS-05-014"])
c.F("f_account_contaminated", "وصف يارا الأول كان «ولداً بسترة خضراء»، وتبدّل بعد سؤال موحٍ إلى «رجل بلحية»؛ فالتبدل صنعه السؤال، وارتفاع تأكدها لم يصاحبه ارتفاع في الدقة.", "relation", ["yara", "fadi"], 3, T(160), "loc_office", ["KO-RS-05-006", "KO-RS-05-008"])

c.claims += [
    {"id": "cl_yara_beard", "statement_ar": "كان الرجل الذي أخذ الدراجة طويلاً وله لحية.", "kind": "honest_mistake", "held_by": ["yara"], "true_fact_id": "f_account_contaminated", "contradicted_by_evidence_ids": ["ev_first_message", "ev_interview_transcript"]},
    {"id": "cl_vp_sure", "statement_ar": "الشاهدة متأكدة تماماً أن الذي أخذ الدراجة هو أنور، وتأكدها دليل على صحة وصفها.", "kind": "honest_mistake", "held_by": ["fadi"], "true_fact_id": "f_account_contaminated", "contradicted_by_evidence_ids": ["ev_interview_transcript", "ev_mother_statement"]},
]
c.timeline += [
    {"id": "te_text", "description_ar": "كريم يكتب لأخيه أنه أخذ الدراجة.", "time": T(65), "actor_ids": ["karim"], "fact_ids": ["f_adam_text"], "motivated_by_ar": "أراد إخبار أخيه قبل أن يغادر"},
    {"id": "te_steward", "description_ar": "أنور مناوب عند باب القاعة الكبرى.", "time": T(60, "exact", 90), "location_id": "loc_hall", "actor_ids": ["anwar"], "fact_ids": ["f_steward_duty"], "motivated_by_ar": "مناوبة المعرض المكتوبة"},
    {"id": "te_take", "description_ar": "فتى بسترة خضراء يخرج بالدراجة من البوابة الجانبية.", "time": T(68), "location_id": "loc_gate", "actor_ids": ["karim", "yara"], "fact_ids": ["f_yara_saw", "f_youth_took"], "motivated_by_ar": "كريم يوصل لوحة الفريق، ويارا تنتظر قرب الحامل"},
    {"id": "te_message", "description_ar": "سلمى ترسل رسالة إلى مجموعة أولياء الأمور بما قالته يارا.", "time": T(81), "actor_ids": ["salma"], "fact_ids": ["f_told_mother"], "motivated_by_ar": "أرادت أن تساعد في العثور على صاحب الدراجة"},
    {"id": "te_return", "description_ar": "الدراجة تعود إلى الحامل وأنور يدوّنها في جولة الإغلاق.", "time": T(125), "location_id": "loc_gate", "actor_ids": ["anwar", "karim"], "fact_ids": ["f_return_round"], "motivated_by_ar": "كريم أعاد الدراجة وأنور يدوّن جولته الروتينية"},
    {"id": "te_interview", "description_ar": "مقابلة يارا بحضور أمها والمرشدة.", "time": T(160), "location_id": "loc_office", "actor_ids": ["fadi", "yara", "salma", "hind"], "fact_ids": ["f_vp_asked", "f_transcript_exists", "f_mother_says"], "motivated_by_ar": "أراد الوكيل معرفة ما رأته الشاهدة"},
]

# ---------------------------------------------------------------- evidence
c.V("ev_bike_report", "بلاغ آدم", "documentary",
    "مكتب وكيل المدرسة — بلاغ فقد — الخميس\n16:15 — آدم حداد: «دراجتي الحمراء رقم 14 كانت على حامل البوابة الجانبية 15:30 ولم أجدها عند 16:15.»\nإضافة 17:35: «وجدتها على الحامل 17:30. من أخذها؟»",
    None, ["f_bike_missing"], "moderate",
    "بلاغ صاحب الدراجة بوقتين كتبهما بنفسه؛ لا يقول من أخذها ولا كيف.",
    "اقرأ بلاغ آدم", loc="loc_office")
c.V("ev_vp_summary", "ملخص الوكيل ليوم الجمعة", "documentary",
    "مكتب وكيل المدرسة — ملخص — الجمعة 09:00\nالشاهدة يارا (11 سنة) متأكدة تماماً: رجل طويل (نحو 1.85 م) بلحية، سترة خضراء، يشبه الأستاذ العامل أنور الذي يرتب الدراجات.\nالتوصية: إنذار مكتوب للعامل ومنعه من حامل الدراجات.",
    None, ["f_anwar_named", "f_anwar_denies"], "moderate",
    "ملخص كتبه الوكيل بعد المقابلة بيوم؛ يعبّر عن تأكد الشاهدة ولا ينقل ألفاظها الأولى، ولم يقارَن برسالة أمها.",
    "اقرأ ملخص الوكيل ليوم الجمعة", red=True, loc="loc_office")
c.V("ev_first_message", "رسالة الأم إلى مجموعة أولياء الأمور", "digital",
    "هاتف سلمى الخطيب — مجموعة أولياء الأمور — الخميس 16:21\n«يارا تقول إنها رأت ولداً بسترة خضراء يأخذ دراجة حمراء من عند البوابة الجانبية ويضحك. هل ضاعت دراجة لأحدكم؟»\nالرسالة أُرسلت قبل أي مقابلة وقبل أن يتحدث معها أحد من الإدارة.",
    "f_told_mother", ["f_told_mother", "f_yara_saw"], "strong",
    "تنقل الأم ما قالته الطفلة لها بكلمات الأم، وتسجل أول وصف مكتوب بتاريخه؛ ولا تضمن أن الطفلة رأت كل التفاصيل.",
    "اطلب رسالة الأم إلى مجموعة أولياء الأمور", ko="KO-RS-05-008", loc="loc_office")
c.V("ev_interview_transcript", "محضر مقابلة يارا", "documentary",
    "مكتب وكيل المدرسة — محضر المرشدة هند — الخميس 17:40 — حاضرون: يارا وأمها والوكيل والمرشدة\nس1 (الوكيل): «احكي لي بكلماتك ماذا رأيتِ؟» — ج1: «ولد بسترة خضراء أخذ دراجة حمراء وركب وكان يضحك.»\nس2: «ماذا فعل بعد ذلك؟» — ج2: «خرج من البوابة بهدوء.»\nس3: «هل كان رجلاً طويلاً بلحية، مثل عمّ أنور الذي يرتب الدراجات؟» — ج3: «ربما... لا أعرف.»\nس4: «هل أنتِ متأكدة أنه هو؟» — ج4: «نعم، أظن.»\nملاحظة المرشدة: لم تذكر يارا لحية ولا طولاً قبل س3.",
    "f_transcript_exists", ["f_vp_asked", "f_transcript_exists"], "strong",
    "محضر كتبته مرشدة حاضرة بحروف الأسئلة والأجوبة؛ يبيّن ترتيب الكلام ولا يقيس ما كانت ترى الطفلة فعلاً.",
    "اطلب محضر مقابلة يارا", ko="KO-RS-05-006", loc="loc_office")
c.V("ev_mother_statement", "إفادة سلمى (ملخص)", "testimonial",
    "ملخص إفادة سلمى الخطيب:\n«ابنتي قالت لي «ولد» ولم تقل «رجل». حين سألها الأستاذ هل كان بلحية قالت «ربما». وفي الطريق إلى البيت سألتني: هل قلت شيئاً خطأ؟»",
    "f_mother_says", ["f_mother_says"], "moderate",
    "شهادة أم عن كلام ابنتها وعن المقابلة؛ تؤيدها رسالتها المكتوبة وتؤيدها المرشدة، ولا تغني عن المحضر.",
    "دوّن إفادة سلمى", loc="loc_office")
c.V("ev_vp_statement", "إفادة الوكيل (ملخص)", "testimonial",
    "ملخص إفادة فادي العلي:\n«سألت يارا عن أنور لأنه المسؤول عن ترتيب الدراجات، ولم أقصد الإيحاء. كتبت في ملخصي أنها متأكدة تماماً. لم أقارن جوابها برسالة أمها قبل الكتابة.»",
    "f_vp_asked", ["f_vp_asked"], "moderate",
    "اعتراف صاحب السؤال بما سأل، وهو يوافق المحضر المكتوب؛ ويقدّر نيته بنفسه ولا نملك ما يقيسها.",
    "دوّن إفادة الوكيل", loc="loc_office")
c.V("ev_yara_statement", "إفادة يارا (ملخص)", "testimonial",
    "ملخص إفادة يارا الخطيب (بحضور أمها):\n«رأيت ولداً يضحك ويأخذ الدراجة. سألوني عن عمّ أنور، وهو طيب معنا، ولا أعرف إن كانت له لحية في ذلك اليوم.»",
    "f_yara_saw", ["f_yara_saw"], "weak",
    "إفادة طفلة صادقة بعد يومين من الحدث؛ لا نقيس بها صدقها بل نقارنها بما قيل قبل الأسئلة.",
    "دوّن إفادة يارا", loc="loc_office")
c.V("ev_gate_frame", "لقطة كاميرا البوابة الجانبية 16:08", "digital",
    "البوابة الجانبية — كاميرا (لقطة كل دقيقة) — الخميس 16:08\nتظهر دراجة حمراء يقودها شخص يعبر البوابة، بسترة خضراء داكنة.\nعمود البوابة 2.0 م، وقمة رأس الشخص عند نحو 83% من ارتفاعه.\nالوجه غير واضح. لقطة 16:07: الدراجة على الحامل. لقطة 16:09: لا دراجة في الإطار.",
    "f_camera_stills", ["f_youth_took"], "strong",
    "لقطة كل دقيقة لا ترى الوجه ولا كل اللحظة؛ تقدّر القامة بمقياس من العمود ولا تحدد الهوية.",
    "اطلب لقطات كاميرا البوابة الجانبية", ko="KO-FC-04-024", loc="loc_gate")
c.V("ev_return_sheet", "ورقة جولة الإغلاق", "documentary",
    "مدرسة القنطرة — ورقة جولة الإغلاق بخط العامل أنور — الخميس\n17:05: حامل البوابة الجانبية: الدراجة الحمراء رقم 14 في مكانها، سليمة، والسلسلة مفتوحة بمفتاح ولا كسر فيها.\nالتوقيع: أنور",
    "f_return_round", ["f_return_round", "f_youth_took"], "strong",
    "ورقة كتبها العامل المتهم نفسه في حينها ضمن عمل روتيني؛ تثبت وقت العودة وحالة السلسلة، ولا تقول من أعادها.",
    "اطلب ورقة جولة الإغلاق", loc="loc_gate")
c.V("ev_brother_text", "رسالة كريم إلى آدم", "digital",
    "هاتف آدم حداد — رسالة من كريم — الخميس 16:05\n«أخذت دراجتك الحمراء بمفتاح الاحتياط لأوصل لوحة الفريق إلى المطبعة. سأعيدها قبل الخامسة. أنا لابس سترة الفريق الخضراء. آسف نسيت أن أستأذنك!»\nحالة الرسالة: وصلت 16:05 وقُرئت 17:30 (هاتف آدم مغلق أثناء المعرض).",
    "f_adam_text", ["f_adam_text", "f_youth_took"], "strong",
    "رسالة بتاريخها على هاتف المستلم؛ تثبت ما كتبه كريم قبل الحادثة بثلاث دقائق، ولا تثبت وحدها أنه نفّذ ما كتب.",
    "اطلب رسالة كريم من هاتف آدم", loc="loc_office")
c.V("ev_steward_sheet", "ورقة مناوبة مضيفي المعرض", "documentary",
    "معرض مدرسة القنطرة — ورقة مناوبة باب القاعة الكبرى — الخميس\nأنور الدهان: حضور 16:00 — انصراف 16:30 (توقيع المنسقة ميساء السيد عند الحضور والانصراف)\nملاحظة المنسقة: «لم يغادر أحد المضيفين موقعه في هذه الفترة.»",
    "f_steward_duty", ["f_steward_duty", "f_youth_took"], "strong",
    "ورقة بتوقيع منسقة مستقلة عن الشاهدة والوكيل؛ تذكر موضع أنور المسجّل وقت الحادثة، ولا تثبت أن أحداً لم يعره بطاقته أو غاب لحظات.",
    "اطلب ورقة مناوبة مضيفي المعرض", loc="loc_hall")
c.V("ev_old_warning", "ملاحظة إدارية عام 2022", "documentary",
    "ملف العاملين — ملاحظة إدارية — 2022\nتنبيه شفهي للعامل أنور لنقله دراجات من مدخل المدرسة دون إذن مكتوب أثناء حفل سابق، وتُرك الأمر بعد توضيحه.",
    "f_old_warning", ["f_old_warning"], "weak",
    "واقعة مختلفة قبل سنتين لا تربط الرجل بهذه الدراجة؛ وهي سبب مفهوم لظن الوكيل لا دليل على فعل.",
    "اطلب ملاحظة عام 2022 من ملف العاملين", red=True, loc="loc_office")
c.V("ev_karim_statement", "إفادة كريم (ملخص)", "testimonial",
    "ملخص إفادة كريم حداد:\n«أخذت دراجة أخي بمفتاح الاحتياط لأوصل لوحة الفريق إلى المطبعة، وكتبت له رسالة، وأعدتها قبل الخامسة. لم أتأكد أنه قرأها. أنا آسف.»",
    "f_karim_says", ["f_karim_says"], "moderate",
    "إفادة اعتراف بفعل بحسن نية؛ يؤيدها نص الرسالة وورقة جولة الإغلاق ولا يعتمد عليها الاستنتاج.",
    "دوّن إفادة كريم", loc="loc_office")

# ---------------------------------------------------------------- inferences
c.I("i_a_youth", [E_("ev_gate_frame"), E_("ev_return_sheet")], "fact", "f_youth_took", "establishes", "strong",
    "اللقطة تُظهر شخصاً بسترة خضراء قامته نحو 1.65 م يخرج بالدراجة 16:08، وورقة العامل تثبت عودتها 17:05 والسلسلة مفتوحة بمفتاح؛ فالفاعل فتى لا رجل طويل، وقد أعادها.", ["KO-RS-05-004", "KO-RS-06-003"])
c.I("i_b_youth", [E_("ev_brother_text"), E_("ev_steward_sheet")], "fact", "f_youth_took", "establishes", "strong",
    "رسالة كريم قبل الحادثة بثلاث دقائق تذكر السترة الخضراء ومفتاح الاحتياط والعودة قبل الخامسة، وورقة المناوبة تضع أنور عند باب القاعة بتوقيع طرف ثالث؛ وهما مصدران لا يشتركان في كاتب.", ["KO-RS-05-004", "KO-RS-05-014"])
c.I("i_a_account", [E_("ev_first_message"), E_("ev_interview_transcript")], "fact", "f_account_contaminated", "establishes", "strong",
    "أول وصف مكتوب قبل أي سؤال هو «ولد بسترة خضراء»، وفي المحضر لم يظهر الطول ولا اللحية إلا بعد س3 الذي ذكر أنور والصفتين معاً؛ فالتبدل لاحق للسؤال، وجواب س4 يعبّر عن تأكد لا عن ذاكرة جديدة.", ["KO-RS-05-006", "KO-RS-05-008"])
c.I("i_b_account", [E_("ev_mother_statement"), E_("ev_vp_statement")], "fact", "f_account_contaminated", "establishes", "strong",
    "الأم تذكر أن ابنتها قالت «ولد» وأجابت «ربما» عن اللحية، والوكيل يقرّ بأنه سألها عن أنور وبأنه كتب «متأكدة تماماً» دون مقارنة؛ مصدران من طرفين مختلفين يتفقان على ترتيب ما جرى.", ["KO-RS-05-008", "KO-RS-05-011"])
c.I("i_support_borrow", [Fa("f_youth_took"), Fa("f_account_contaminated")], "hypothesis", "h_borrow", "supports", "strong",
    "الاستعارة تفسّر الدراجة العائدة والسلسلة المفتوحة بمفتاح وتفسّر لماذا تبدل وصف الطفلة؛ وكل شيء بسيط ولا يحتاج إلى سارق.", ["KO-RS-06-007"])
c.I("i_rule_anwar", [Fa("f_youth_took"), Fa("f_account_contaminated")], "hypothesis", "h_anwar", "rules_out", "strong",
    "من أخذ الدراجة فتى بسترة خضراء، والوصف الذي يوافق أنور جاء من سؤال لا من الذاكرة؛ وتأكد الطفلة لا يزيد وصفها دقة.", ["KO-RS-06-008", "KO-RS-05-008"])
c.I("i_rule_stranger", [Fa("f_youth_took"), Fa("f_account_contaminated")], "hypothesis", "h_stranger", "rules_out", "strong",
    "الذي أخذ الدراجة من أسرة صاحبها وبمفتاح الاحتياط وأعادها، فلا غريب هنا.", ["KO-RS-06-008"])
c.I("i_rule_lie", [Fa("f_youth_took"), Fa("f_account_contaminated")], "hypothesis", "h_yara_lie", "rules_out", "strong",
    "وصفها الأول «ولد بسترة خضراء» يطابق ما تثبته الكاميرا والرسالة، فهو لا يدل على اختلاق؛ والتبدل اللاحق نتيجة سؤال لا سوء نية.", ["KO-RS-05-014", "KO-RS-05-008"])
c.I("i_cl_yara", [Fa("f_account_contaminated")], "claim", "cl_yara_beard", "contradicts_claim", "strong",
    "اللحية والطول لم يردا في أول وصف ولا في س1 وس2، وإنما بعد س3؛ فهما جزء من الاقتراح.", ["KO-RS-05-006"])
c.I("i_cl_vp", [Fa("f_account_contaminated")], "claim", "cl_vp_sure", "contradicts_claim", "strong",
    "ثقة الشاهد ليست مقياساً لدقته، خصوصاً بعد سؤال موحٍ؛ وقد ارتفعت ثقتها وانخفضت دقة وصفها.", ["KO-RS-05-008"])

c.ck += [
    {"character_id": "yara", "knows": [K("f_yara_saw", "witnessed", "fairly_sure"), K("f_told_mother")], "hides": [], "believes": [{"claim_id": "cl_yara_beard", "stance": "sincere"}]},
    {"character_id": "salma", "knows": [K("f_mother_says")], "hides": [], "believes": []},
    {"character_id": "fadi", "knows": [K("f_vp_asked"), K("f_camera_stills", "professional")], "hides": [], "believes": [{"claim_id": "cl_vp_sure", "stance": "sincere"}]},
    {"character_id": "hind", "knows": [K("f_transcript_exists", "professional")], "hides": [], "believes": []},
    {"character_id": "anwar", "knows": [K("f_steward_duty"), K("f_return_round"), K("f_old_warning")], "hides": [], "believes": []},
    {"character_id": "karim", "knows": [K("f_karim_says")], "hides": [], "believes": []},
    {"character_id": "adam", "knows": [K("f_adam_text")], "hides": [], "believes": []},
]
hyps = [
    {"id": "h_anwar", "statement_ar": "أخذ العامل أنور الدراجة، كما وصفته الشاهدة بعد سؤالها عنه.", "is_true": False, "plausibility_at_start": "high", "suspect_id": "anwar"},
    {"id": "h_stranger", "statement_ar": "أخذ غريب الدراجة ثم أعادها بعد أن خاف.", "is_true": False, "plausibility_at_start": "medium"},
    {"id": "h_borrow", "statement_ar": "استعار كريم دراجة أخيه دون أن يستأذنه، ووصف يارا الأول صحيح، وقد تبدّل بعد سؤال موحٍ لا بسبب ذاكرة جديدة.", "is_true": True, "plausibility_at_start": "low", "suspect_id": "karim"},
    {"id": "h_yara_lie", "statement_ar": "اختلقت يارا قصة الولد بسترة خضراء، ولا أحد أخذ الدراجة.", "is_true": False, "plausibility_at_start": "medium", "suspect_id": "yara"},
]
mis = [
    {"id": "rh_sure", "points_to_hypothesis_id": "h_anwar", "planted_via_ar": "ملخص الوكيل يقول إن الشاهدة متأكدة تماماً من أنه أنور.", "evidence_ids": ["ev_vp_summary"],
     "refuted_by_inference_ids": ["i_cl_vp", "i_a_account", "i_rule_anwar"],
     "fairness_note_ar": "المحضر الحرفي ورسالة الأم متاحان للاعب، وفيهما أن اللحية لم ترد قبل السؤال عنها."},
    {"id": "rh_warning", "points_to_hypothesis_id": "h_anwar", "planted_via_ar": "تنبيه سابق لأنور بسبب نقل دراجات دون إذن.", "evidence_ids": ["ev_old_warning"],
     "refuted_by_inference_ids": ["i_b_youth", "i_rule_anwar"],
     "fairness_note_ar": "ورقة المناوبة توقعها منسقة مستقلة وتضع أنور عند باب القاعة، والواقعة القديمة ليست دليلاً على فعل جديد."},
    {"id": "rh_camera", "points_to_hypothesis_id": "h_stranger", "planted_via_ar": "الكاميرا لا تُظهر الوجه، فقد يكون الفاعل أي شخص.", "evidence_ids": ["ev_gate_frame"],
     "refuted_by_inference_ids": ["i_b_youth", "i_rule_stranger"],
     "fairness_note_ar": "رسالة كريم وسلسلة العودة بمفتاح الاحتياط تحددان أسرة صاحب الدراجة قبل أي اعتماد على الوجه."},
]
los = [
    {"id": "lo_source", "statement_ar": "يصنّف رسالة الأم والمحضر والسجلات مصادر أقرب إلى الحدث، والملخصات والإفادات أقوالاً لاحقة.", "skill_ko_ref": "KO-RS-05-001", "observable_behaviors_ar": ["يصنّف الإفادات أقوالاً", "يفرّق الأول عن اللاحق"], "evidence_sources": ["evidence_board"]},
    {"id": "lo_conflict", "statement_ar": "يرتّب الأحداث على خط زمني يضع الوصف الأول قبل السؤال الموحي والعودة قبل المقابلة.", "skill_ko_ref": "KO-RS-05-005", "observable_behaviors_ar": ["يضع الأدلة في أزمنتها"], "evidence_sources": ["timeline_task", "action_log"]},
    {"id": "lo_links", "statement_ar": "يفحص نص أسئلة المقابلة ويفرّق بين ثقة الشاهد ودقته، ويربط الدليل بالفرضية باتجاه صحيح.", "skill_ko_ref": "KO-RS-05-008", "observable_behaviors_ar": ["يقرأ نص الأسئلة", "يربط الدليل بالفرضية"], "evidence_sources": ["evidence_board", "final_justification"]},
    {"id": "lo_calib", "statement_ar": "يصوغ نسبة الترجيح بحدودها ويذكر ما لا يستطيع التسجيل إثباته عن ذاكرة الطفلة.", "skill_ko_ref": "KO-RS-06-021", "observable_behaviors_ar": ["يختار ثقة معقولة", "يذكر حدوداً"], "evidence_sources": ["final_justification"]},
    {"id": "lo_revise", "statement_ar": "يراجع رأيه الأول حين يظهر الوصف الأول للشاهدة.", "skill_ko_ref": "KO-RS-06-009", "observable_behaviors_ar": ["يغيّر فرضيته الرائدة بدليل"], "evidence_sources": ["hypothesis_ledger"]},
    {"id": "lo_elim", "statement_ar": "يبحث عن مسارين مستقلين ويستبعد ما تنقضه الأدلة.", "skill_ko_ref": "KO-RS-05-004", "observable_behaviors_ar": ["يضيف فرضيات", "يستبعد بدليل"], "evidence_sources": ["hypothesis_ledger"]},
    {"id": "lo_just", "statement_ar": "يكتب حجة تحافظ على كرامة الشاهدة وتذكر أن السؤال لا الطفلة هو سبب التبدل.", "skill_ko_ref": "KO-RS-05-006", "observable_behaviors_ar": ["يكتب حجة معللة"], "evidence_sources": ["final_justification"]},
]
topics = [
    {"id": "t_saw", "label_ar": "ما رأته يارا", "example_questions_ar": ["احكي لي بكلماتك ماذا رأيتِ؟", "ماذا فعل الولد؟"], "fact_ids": ["f_yara_saw"], "claim_ids": ["cl_yara_beard"]},
    {"id": "t_mom", "label_ar": "ما قالته لأمها", "example_questions_ar": ["لمن حكيتِ أولاً؟"], "fact_ids": ["f_told_mother"]},
    {"id": "t_mother_says", "label_ar": "ما قالته الطفلة وما سُئلت", "example_questions_ar": ["ماذا قالت ابنتك لك أولاً؟", "ماذا سُئلت في المقابلة؟"], "fact_ids": ["f_mother_says"]},
    {"id": "t_questions", "label_ar": "أسئلة المقابلة", "example_questions_ar": ["ماذا سألتَ الشاهدة؟", "كيف عرفت أنها متأكدة؟"], "fact_ids": ["f_vp_asked"], "claim_ids": ["cl_vp_sure"]},
    {"id": "t_camera", "label_ar": "كاميرا البوابة", "example_questions_ar": ["هل في البوابة كاميرا؟"], "fact_ids": ["f_camera_stills"]},
    {"id": "t_notes", "label_ar": "محضر المقابلة", "example_questions_ar": ["هل دوّنتِ ما قيل؟"], "fact_ids": ["f_transcript_exists"]},
    {"id": "t_round", "label_ar": "مناوبتي وجولتي", "example_questions_ar": ["أين كنت عصر الخميس؟", "ماذا دوّنت في جولة الإغلاق؟"], "fact_ids": ["f_steward_duty", "f_return_round"]},
    {"id": "t_warning", "label_ar": "التنبيه السابق", "example_questions_ar": ["هل نُبّهت من قبل؟"], "fact_ids": ["f_old_warning"]},
    {"id": "t_borrow", "label_ar": "الدراجة والمفتاح", "example_questions_ar": ["هل أخذت الدراجة؟", "كيف فتحت السلسلة؟"], "fact_ids": ["f_karim_says"]},
    {"id": "t_message", "label_ar": "الرسالة إلى آدم", "example_questions_ar": ["هل وصلتك رسالة من كريم؟"], "fact_ids": ["f_adam_text"]},
]
he = lambda e: {"has_evidence": e}
al = {"always": True}
c.H("hg1", 1, "metacognitive", "حين يتغيّر وصف الشاهد بين الرواية الأولى والثانية، اسأل: ما الذي حدث بينهما؟", al, None, 0.02)
c.H("hg2", 2, "focus_area", "قارن ما قيل قبل أول سؤال من المدرسة بما قيل بعده، وانظر في نص السؤال نفسه لا في جواب الطفلة وحده.", he("ev_vp_summary"), None, 0.04)
c.H("hg3", 3, "pointer", "ابحث عن سجلات لا تكتبها الطفلة ولا الوكيل: كاميرا، وأوراق مناوبة، ورسائل بتواريخها.", he("ev_vp_summary"), None, 0.08)
c.H("ha1", 1, "metacognitive", "هل يعني تأكد الشاهد أن وصفه أدق؟", he("ev_interview_transcript"), "i_a_account", 0.02)
c.H("ha2", 2, "pointer", "اقرأ س3 كلمة كلمة: ما الذي ذُكر فيه قبل أن تجيب الطفلة؟", he("ev_interview_transcript"), "i_a_account", 0.06)
c.H("hy1", 1, "metacognitive", "ما الدليل على هوية الفاعل الذي لا يتوقف على وجه ولا ذاكرة؟", he("ev_gate_frame"), "i_b_youth", 0.02)
c.H("hy2", 2, "pointer", "السلسلة فُتحت بمفتاح لا بكسر؛ من يملك مفتاحاً احتياطياً؟ وابحث عن رسالة بتاريخ قبل الحادثة.", he("ev_return_sheet"), "i_b_youth", 0.06)

steps = [
    (1, "رتّب الكلام زمنياً: رسالة الأم 16:21 تسبق المقابلة 17:40، ووصف الطفلة فيها «ولد بسترة خضراء» بلا طول ولا لحية.", ["ev_first_message", "ev_interview_transcript"], "i_a_account"),
    (2, "اقرأ الأسئلة حرفياً: الطول واللحية واسم العامل دخلت معاً في س3، ثم جاء «نعم، أظن» في س4؛ فارتفاع التأكد لا يبرهن على دقة الوصف.", ["ev_interview_transcript"], "i_cl_vp"),
    (3, "طريق ثانٍ لما جرى: الأم تروي ترتيب الكلام، والوكيل يقرّ بسؤاله وبأنه كتب «متأكدة» دون مقارنة؛ طرفان مختلفان يتفقان.", ["ev_mother_statement", "ev_vp_statement"], "i_b_account"),
    (4, "من أخذ الدراجة؟ لقطة 16:08 تُظهر سترة خضراء وقامة أقصر من وصف الرجل، وورقة العامل تضع عودتها 17:05 والسلسلة مفتوحة بمفتاح.", ["ev_gate_frame", "ev_return_sheet"], "i_a_youth"),
    (5, "الطريق المستقل لهوية الفاعل: رسالة بتاريخها قبل الحادثة تذكر المفتاح والسترة والعودة، وورقة مناوبة بتوقيع منسقة تضع أنور في مكان آخر.", ["ev_brother_text", "ev_steward_sheet"], "i_b_youth"),
    (6, "فتسقط فكرة أن العامل هو الفاعل، وفكرة الغريب، وفكرة أن الطفلة اختلقت؛ ويبقى أن سؤالاً موحياً غيّر وصفاً كان صحيحاً.", ["ev_gate_frame", "ev_brother_text", "ev_first_message"], "i_rule_anwar"),
]
ending = {"steps": steps,
    "alt": ["يكفي طريق الكاميرا والجولة لهوية الفاعل، وطريق الرسالة والمحضر لتبدّل الوصف، من غير إفادات الأطراف.",
            "ويكفي طريق رسالة كريم وورقة المناوبة لهوية الفاعل، وإفادتا الأم والوكيل لتبدّل الوصف، من غير الكاميرا والمحضر؛ والأقوى أن يتفق الطريقان."],
    "limits": ["لا نستطيع أن نعرف ما تذكره يارا الآن؛ نعرف ما قالته قبل السؤال وما قالته بعده.",
               "الكاميرا تلتقط صورة كل دقيقة، فلا ترى الوجه ولا كل اللحظة، وقامتها المقدّرة تقريبية.",
               "ورقة المناوبة تضع أنور عند باب القاعة بتوقيع المنسقة، ولا تنفي من حيث المبدأ أن يكون قد غاب لحظات.",
               "لا نعرف لماذا اختار الوكيل أنور من بين الناس إلا أنه المسؤول عن ترتيب الدراجات."],
    "notes": ["السؤال الموحي يغيّر الذاكرة نفسها لا إجابة اللحظة فقط: ما تقوله الطفلة بعده قد يصبح ذكرى أوضح عندها من الأصل. لذلك تُحفظ الرواية الأولى قبل أي اقتراح، وتُطرح الأسئلة المفتوحة: «احكِ لي بكلماتك».",
              "ثقة الشاهد ليست دقته: ارتفعت ثقة يارا من «ربما» إلى «نعم، أظن»، وانخفضت دقة وصفها. يعرف المحققون هذا النمط في إفادات الكبار والصغار.",
              "الطفلة لم تكذب ولم تخطئ بسوء نية، والوكيل لم يقصد الإيحاء. وإصلاح الضرر ودّي: يُسحب الإنذار عن أنور، ويُعتذر له، وتُجرى مقابلات المدرسة بأسئلة مفتوحة وبحضور ولي الأمر.",
              "كريم لم يسرق: أخذ ما ظنه مباحاً داخل الأسرة وأخبر أخاه برسالة لم تُقرأ. وهذا يعلّمنا أن الرسالة التي لم تُقرأ ليست رسالة وصلت.",
              "لا يُعدّ ارتباك أنور ولا هدوؤه دليلاً؛ المعتمد هو السجلات.",
              "بطاقة الأصل: القضية أصلية من ATHAR، وبنيتها من نمط «السؤال الذي زرع ذكرى» في مكتبة تصميم القضايا؛ لا مقابلات حقيقية فيها."]}
meta = {"title_ar": "الدراجة الحمراء والسؤال الذي غيّر الوصف", "title_en": "The Red Bicycle and the Question That Changed the Description", "age_band": "16-18", "locale": "ar", "dialogue_register": "msa", "estimated_minutes": 30, "difficulty": 3,
        "content_flags": ["theft", "missing_person"], "authors": ["فريق أثر التحريري (مسودة بمساعدة الذكاء الاصطناعي، لم تُراجَع بشرياً بعد)"],
        "knowledge_object_refs": ["KO-RS-05-006", "KO-RS-05-008", "KO-RS-05-011", "KO-RS-05-001", "KO-RS-05-004", "KO-RS-05-005", "KO-RS-05-014", "KO-RS-05-007", "KO-RS-06-001", "KO-RS-06-003", "KO-RS-06-021", "KO-RS-06-009", "KO-RS-06-007", "KO-RS-06-008", "KO-FC-04-024", "KO-CD-05-004"]}
premise = {"hook_ar": "طفلة قالت لأمها «ولد بسترة خضراء». بعد سؤال واحد من الكبار صارت تقول «رجل طويل بلحية». أيهما كانت ذاكرتها، وأيهما صنعه السؤال؟",
           "player_role_ar": "أنت وسيط مدرسي تراجع ملف دراجة اختفت ثم ظهرت، وطُلب منك رأي معلّل قبل أن يُنذر أحد العاملين.",
           "setting_ar": "مدرسة القنطرة، يوم معرض مفتوح من الخميس 15:00 إلى صباح الجمعة. أوقات البوابة والمناوبة بساعة المدرسة.",
           "public_fact_ids": ["f_bike_missing", "f_anwar_named", "f_anwar_denies"],
           "assumed_general_knowledge_ar": ["الأسئلة الموحية تغيّر الإجابات", "ثقة الشاهد ليست دقته", "الأطفال يحتاجون إلى مقابلة هادئة بحضور ولي أمر"]}
solution = {"culprit_ids": ["karim"], "summary_ar": "لم تُسرق الدراجة. استعارها كريم بمفتاح الاحتياط وأعادها، وكتب لأخيه رسالة لم تُقرأ في وقتها. ووصف يارا الأول لولد بسترة خضراء كان صحيحاً، وتبدّل إلى رجل بلحية بعد سؤال من الوكيل ذكر عمّ أنور، وقد زاد تأكدها دون أن تزيد دقتها.",
            "key_fact_ids": ["f_youth_took", "f_account_contaminated"]}
ref = "لا دليل على أن أنور أخذ الدراجة. أول وصف مكتوب للطفلة جاء في رسالة أمها قبل أي سؤال من المدرسة: ولد بسترة خضراء. أما الطول واللحية فظهرا بعد سؤال في المحضر ذكر أنور بنفسه، وارتفع تأكدها دون أن ترتفع دقتها. لقطة الكاميرا تُظهر سترة خضراء وقامة أقصر، وورقة الجولة تثبت عودة الدراجة والسلسلة مفتوحة بمفتاح، ورسالة كريم بتاريخها ترويها، وورقة المناوبة تضع أنور عند باب القاعة. حدود الاستنتاج: لا نعرف ما تذكره الطفلة اليوم، والكاميرا لا ترى الوجه، وورقة المناوبة لا تنفي غياباً قصيراً."
ui = {
    "clock": {"epoch_hhmm": "15:00", "zone_label_ar": "ساعة المدرسة (الخميس 15:00 = البداية)"},
    "cover": {"title_ar": "الدراجة الحمراء والسؤال الذي غيّر الوصف", "tagline_ar": "ثقة الشاهدة ارتفعت… فهل ارتفعت دقتها؟", "kicker_ar": "الملف الرابع والعشرون · السؤال قبل الجواب", "glyph": "?", "accent": "rose"},
    "cold_open_ar": ["الجمعة صباحاً، مكتب وكيل المدرسة.", "اختفت دراجة حمراء من البوابة الجانبية ثم ظهرت في مكانها. طفلة في الحادية عشرة رأت من أخذها، والوكيل يقول إنها متأكدة تماماً: العامل أنور.",
                     "عندك رسالة أمها ومحضر المقابلة وسجلات المدرسة. ماذا قالت الطفلة قبل أن يسألها أحد؟ وماذا قالت بعد؟"],
    "limit_menu": [
        {"id": "l_memory_unknown", "label_ar": "لا نعرف ما تذكره الطفلة اليوم، بل ما قالته قبل السؤال وبعده"},
        {"id": "l_camera_limits", "label_ar": "الكاميرا تلتقط صورة كل دقيقة ولا ترى الوجه، وقامتها المقدّرة تقريبية"},
        {"id": "l_steward_gap", "label_ar": "ورقة المناوبة لا تنفي من حيث المبدأ غياباً قصيراً"},
        {"id": "l_invalid_sure", "label_ar": "تأكد الطفلة بعد السؤال يرفع صدق وصفها"},
        {"id": "l_invalid_child", "label_ar": "كلام الأطفال لا يُعتدّ به أصلاً"},
        {"id": "l_invalid_warning", "label_ar": "التنبيه السابق لأنور يدل على أنه أخذ الدراجة"}],
    "mind_change_menu": [
        {"id": "m_text_late", "label_ar": "ظهور أن رسالة كريم أُرسلت بعد عودة الدراجة لا قبلها"},
        {"id": "m_frame_other", "label_ar": "ظهور لقطة أخرى للكاميرا تُظهر رجلاً بلحية قرب الدراجة"},
        {"id": "m_steward_left", "label_ar": "ظهور أن أنور غادر باب القاعة بين 16:00 و16:30"},
        {"id": "m_confident", "label_ar": "ازدياد ثقة الشاهدة في اليوم التالي"}],
    "transfer": {
        "id": "tr_bookseller", "title_ar": "اختبار نقل المهارة: بائع الكتب والصورة",
        "scenario_ar": "بائع كتب في سوق القنطرة رأى زبوناً يأخذ كتاباً دون دفع. قال أولاً: «شاب بقبعة زرقاء». ثم عرض عليه موظف صورة رجل بلحية وسأله: «هذا هو، أليس كذلك؟» فقال: «نعم، أنا متأكد».",
        "documents": [
            {"title_ar": "ملاحظة الموظف الأولى", "body_ar": "في الدقيقة الأولى، قبل أي سؤال: «شاب بقبعة زرقاء، أخذ كتاباً وخرج.»"},
            {"title_ar": "سجل كاميرا المحل", "body_ar": "لقطة تظهر شاباً بقبعة زرقاء ومعه كتاب عند الباب، وقامته أقصر من الرجل الذي في الصورة المعروضة."}],
        "prompt_ar": "اختر الخطوات التي تصلح لتقدير ما يعنيه تأكد البائع من الصورة (يمكنك اختيار أكثر من خطوة).",
        "options": [
            {"id": "o1", "text_ar": "إيجاد الوصف الأول المسجّل قبل عرض أي صورة أو اسم"},
            {"id": "o2", "text_ar": "قراءة نص السؤال الذي عُرضت به الصورة لمعرفة هل كان موحياً"},
            {"id": "o3", "text_ar": "البحث عن سجل مستقل كالكاميرا لا يعتمد على ذاكرة البائع"},
            {"id": "o4", "text_ar": "التمييز بين ثقة البائع في جوابه ودقة وصفه"},
            {"id": "o5", "text_ar": "اعتبار تأكده دليلاً على أنه تعرّف على الرجل الصحيح"},
            {"id": "o6", "text_ar": "تكرار عرض الصورة عليه حتى يثبت جوابه"},
            {"id": "o7", "text_ar": "الحكم على الشاهد بحسب هدوئه أو ارتباكه"}],
        "free_text_prompt_ar": "اكتب في ثلاثة أسطر كيف تقرّر نسبة الترجيح بأن الرجل في الصورة هو من أخذ الكتاب.",
    },
    "skills": [{"skill_id": "KO-RS-05-006", "track": "B"}, {"skill_id": "KO-RS-05-008", "track": "B"}, {"skill_id": "KO-RS-05-004", "track": "B"}, {"skill_id": "KO-RS-05-011", "track": "B"}, {"skill_id": "KO-RS-05-014", "track": "B"}],
    "stage_hooks_ar": {"briefing": "كلمتان في سؤال واحد قد تغيّران ما تقوله شاهدة صغيرة… فابحث عن أول ما قالت.", "investigating": "الرواية الأولى قبل أي اقتراح هي أثمن ما عندك.", "review": "قبل أن تغلق الملف: ما الذي لا يعرفه أحد عن ذاكرة الطفلة؟", "resolved": "أُغلق الملف. أُعيد الاعتبار لعمّ أنور، وبقي سؤال عن طريقة أفضل لسؤال الصغار."},
    "character_glyphs": {"yara": "ي", "salma": "س", "fadi": "ف", "hind": "هـ", "anwar": "أ", "karim": "ك", "adam": "آ"},
}
sc = {
    "case_id": CID,
    "accepted_conclusions": {
        "h_borrow": {"grade": 1, "note_ar": "استنتاج متسق مع الأدلة ويتطلب ذكر حدوده."},
        "h_anwar": {"grade": 0, "note_ar": "يبني الاتهام على وصف تبدّل بعد سؤال موحٍ، ويتجاهل الرواية الأولى والكاميرا ورسالة كريم وورقة المناوبة."},
        "h_stranger": {"grade": 0, "note_ar": "الدراجة فُتحت بمفتاح الاحتياط وأعادها أخو صاحبها؛ لا غريب."},
        "h_yara_lie": {"grade": 0, "note_ar": "وصفها الأول يطابق الكاميرا والرسالة، والتبدل نتيجة سؤال لا اختلاق."}},
    "confidence_band": {"h_borrow": [65, 90], "h_anwar": [0, 10], "h_stranger": [0, 15], "h_yara_lie": [0, 10]},
    "source_key": {"ev_bike_report": "claim", "ev_vp_summary": "claim", "ev_first_message": "primary_record", "ev_interview_transcript": "primary_record", "ev_mother_statement": "claim", "ev_vp_statement": "claim",
                   "ev_yara_statement": "claim", "ev_gate_frame": "primary_record", "ev_return_sheet": "primary_record", "ev_brother_text": "primary_record", "ev_steward_sheet": "primary_record",
                   "ev_old_warning": "primary_record", "ev_karim_statement": "claim"},
    "link_key": {
        "h_borrow": {"ev_first_message": "supports", "ev_interview_transcript": "supports", "ev_gate_frame": "supports", "ev_return_sheet": "supports", "ev_brother_text": "supports",
                     "ev_steward_sheet": "supports", "ev_mother_statement": "supports", "ev_vp_statement": "supports", "ev_karim_statement": "supports", "ev_vp_summary": "weakens"},
        "h_anwar": {"ev_vp_summary": "supports", "ev_old_warning": "supports", "ev_steward_sheet": "weakens", "ev_gate_frame": "weakens", "ev_brother_text": "weakens", "ev_first_message": "weakens", "ev_return_sheet": "neutral"},
        "h_stranger": {"ev_gate_frame": "neutral", "ev_brother_text": "weakens", "ev_return_sheet": "weakens"},
        "h_yara_lie": {"ev_first_message": "weakens", "ev_gate_frame": "weakens", "ev_bike_report": "neutral"},
    },
    "required_limits": ["l_memory_unknown", "l_camera_limits"], "valid_mind_changers": ["m_text_late", "m_frame_other", "m_steward_left"],
    "invalid_limits": ["l_invalid_sure", "l_invalid_child", "l_invalid_warning"],
    "decisive_evidence": ["ev_first_message", "ev_interview_transcript", "ev_gate_frame", "ev_return_sheet", "ev_brother_text", "ev_steward_sheet", "ev_mother_statement", "ev_vp_statement"],
    "lab_requirement": None,
    "timeline_requirement": [{"evidence_id": "ev_brother_text", "utc_minute": 65, "tol": 4}, {"evidence_id": "ev_gate_frame", "utc_minute": 68, "tol": 4}, {"evidence_id": "ev_first_message", "utc_minute": 81, "tol": 4},
                             {"evidence_id": "ev_return_sheet", "utc_minute": 125, "tol": 6}, {"evidence_id": "ev_interview_transcript", "utc_minute": 160, "tol": 6}, {"evidence_id": "ev_vp_summary", "utc_minute": 1080, "tol": 20}],
    "refuted_hypotheses": ["h_anwar", "h_stranger", "h_yara_lie"],
    "criteria_map": {"c_source": "source_typing", "c_conflict": "conflict_resolution", "c_links": "hypothesis_links", "c_uncertainty": "uncertainty", "c_revision": "revision", "c_elimination": "elimination", "c_justification": "justification_human"},
    "transfer_key": {"valid": ["o1", "o2", "o3", "o4"], "invalid": ["o5", "o6", "o7"]},
    "caps": {"no_citations_max": 45, "no_conflict_resolution_max": 65},
}
c.build(OUT, meta=meta, premise=premise, solution=solution, locations=locations, objects=objects, orgs=orgs, hyps=hyps, mis=mis, los=los, reference_answer=ref, ending=ending, ui=ui, sc=sc, topics=topics)
