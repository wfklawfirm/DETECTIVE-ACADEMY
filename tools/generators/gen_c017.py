#!/usr/bin/env python3
# Case c017 «رسالة النوارس» — seed S-08 (age band 13-15). Teaches: a correct decipherment tells you WHAT a text says, not WHY it was written
# (and a secret is not a wrong); letter-frequency induction needs an adequate sample; and normalising the text before counting must be declared.
# No-culprit convention: the student whose (innocent) act produced the confusing situation (she wrote the sheet and left it inside a loaned book)
# is recorded in culprit_ids; nobody did anything wrong. The cipher is a fixed monoalphabetic substitution generated here (so the letter counts
# in the evidence are exact). Mechanic note: the engine has no letter-counting simulator, so counting and comparing against the reference table are
# player-visible request actions (request_lab_test) that grant the table / worksheet evidence, as c009 did for its comparison.
# All people, places, institutions and documents are fictional. Usage: gen_c017.py OUT_DIR
import json, sys, os, random, collections
OUT = sys.argv[1]
CID = "c017_seagull_cipher"

# ---------------------------------------------------------------- the cipher (computed, not typed)
ALPHA = "ابتثجحخدذرزسشصضطظعغفقكلمنهوي"
PLAIN = ["الاستاذه لبني تتقاعد يوم الخميس", "نجتمع في قاعه المكتبه قبل الخامسه", "عدنان يحضر الكعكه وريما تحضر الدعوات", "لا تخبروا احدا فهي مفاجاه لها"]
_rnd = random.Random(2026)
while True:
    _p = list(ALPHA); _rnd.shuffle(_p)
    if all(a != b for a, b in zip(ALPHA, _p)): break
ENC = dict(zip(ALPHA, _p)); DEC = {v: k for k, v in ENC.items()}
CIPHER = [" ".join("".join(ENC[c] for c in w) for w in l.split()) for l in PLAIN]
_cnt = collections.Counter(c for l in CIPHER for c in l if c != " ")
N_LETTERS = sum(_cnt.values())
TOP = _cnt.most_common(8)
REF_ORDER = "ا ل ي م و ن ه ت ر ب ع ك د ف س ق ح ج".split()  # fictional reference ranking (see ev_ref_freq)
_plain_cnt = collections.Counter(c for l in PLAIN for c in l if c != " ")
CONFIRMED = [c for c, n in _cnt.most_common() if n >= 3]
UNSURE = [c for c, n in _cnt.most_common() if n < 3]
def ar_n(n): return str(n).translate(str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩"))

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
ch("maher", "ماهر الصيرفي", "witness", "مشرف الامتحانات في ثانوية القنطرة",
   "حازم ويقظ، يخشى الغش أكثر مما يخشى الخطأ في الظن، ويقرأ الغموض بما يتوقعه.",
   ["أن يمنع الغش قبل وقوعه", "ألا يُتّهم بالتساهل"],
   [L("mh_greet", "greeting", "أهلاً بك. أمامنا ورقة غريبة ورسالتان لا تفسير لهما."),
    L("mh_claim", "reveal", "أظن أن الورقة ورسالتي النوارس خطة لتبادل الإجابات في اختبار قريب. لم أراجع الجدول الرسمي قبل أن أقول هذا.", ["f_maher_basis"], ["cl_maher_cheat"]),
    L("mh_unknown", "deflect_unknown", "لا أعرف أكثر من ذلك."),
    L("mh_off", "deflect_offtopic", "ركّز على الورقة والرسائل لو سمحت."),
    L("mh_bye", "farewell", "أريد أن أعرف الحقيقة قبل أن أحكم على أحد.")])
ch("rima", "ريما الحداد", "suspect", "طالبة في الصف التاسع",
   "ذكية ومتحمسة، تخاف أن يُساء فهمها وتصمت إذا اقترب أحد من سرّ تحبّ أن يبقى جميلاً.",
   ["أن يبقى ما تحضّره مفاجأة", "ألا يُظنّ بها سوء"],
   [L("rm_greet", "greeting", "أنا لم أفعل شيئاً سيئاً. اسألني ما تريد."),
    L("rm_refuse", "refuse_secret", "هذا الموضوع... أفضّل ألا أتحدث عنه الآن."),
    L("rm_codes", "reveal", "عبارة «النوارس أورقت» تعني أن بطاقات الدعوة التي عليها رسم النورس طُبعت، و«القارب الأحمر» هو العلبة الحمراء التي سنضع فيها الكعكة. وإيصال الطباعة محفوظ عندي.", ["f_codewords", "f_print_exists"]),
    L("rm_wrote", "reveal", "نعم... أنا كتبتها بحروف مبدلة لأتدرب على لعبة الشفرة، ثم نسيتها بين صفحات الكتاب وأعدته دون أن أنتبه.", ["f_rima_wrote"]),
    L("rm_unknown", "deflect_unknown", "لا أذكر."),
    L("rm_off", "deflect_offtopic", "اسألني عن الورقة والرسائل."),
    L("rm_bye", "farewell", "أرجو أن ينتهي هذا الالتباس قريباً.")])
ch("adnan", "عدنان البيطار", "suspect", "طالب في الصف التاسع، صديق ريما",
   "مرح ومتحفظ، يلقي النكتة حين يريد أن يحمي سراً، ويتراجع إن رأى أن الصمت يضر غيره.",
   ["حماية المفاجأة", "ألا تُتّهم ريما بشيء لم تفعله"],
   [L("ad_greet", "greeting", "أهلاً! إن كنت تبحث عن مؤامرة فأنت في المكان الخطأ."),
    L("ad_joke", "lie", "هذه مجرد رسائل مزاح بيننا، ولا شيء وراءها.", None, ["cl_adnan_joke"]),
    L("ad_refuse", "refuse_secret", "لا أريد أن أفسد شيئاً."),
    L("ad_bakery", "reveal", "حسناً... طلبتُ كعكة من مخبز «السنابل»، وإيصال الطلب عندي. السر ليس لسوء، بل ليبقى حفلاً مفاجئاً.", ["f_bakery_exists", "f_codewords"]),
    L("ad_unknown", "deflect_unknown", "لا أعرف."),
    L("ad_off", "deflect_offtopic", "اسألني عن الرسائل."),
    L("ad_bye", "farewell", "اعتذر لمن ظنّ بنا ظناً سيئاً.")])
ch("sawsan", "سوسن الخطيب", "expert", "أمينة مكتبة جامعة القنطرة",
   "دقيقة وهادئة، تحب أن تعرض ما في السجلات والجداول وحده، ولا تعرف شيئاً عن غرض الورقة.",
   ["أن يعود الكتاب إلى الجامعة سليماً", "أن يُعرف الفرق بين فك الشفرة وفهم الغرض منها"],
   [L("sw_greet", "greeting", "أهلاً. وجدت الورقة بين صفحات كتاب أُعيد إلينا اليوم."),
    L("sw_loan", "reveal", "للكتاب سجل إعارة يبيّن من استعاره ومتى أُعيد.", ["f_loan_record_exists"]),
    L("sw_ref", "reveal", "في دار السِّجِل جدول مرجعي لتكرار الحروف في العربية، ويمكنك الرجوع إليه.", ["f_ref_exists"]),
    L("sw_unknown", "deflect_unknown", "هذا خارج ما أعرفه."),
    L("sw_off", "deflect_offtopic", "اسألني عن الكتاب وسجلاته."),
    L("sw_bye", "farewell", "العدّ يحتاج عينة كافية قبل أن يُصدَّق.")])
ch("hanan", "حنان الزين", "witness", "موظفة المكتب المدرسي",
   "منظمة ومحبة للتفاصيل، تحتفظ بكل نموذج حجز وتجيب عما في الأوراق فقط.",
   ["أن تبقى سجلات الحجز مرتبة"],
   [L("hn_greet", "greeting", "تفضّل. السجلات في ملف واحد."),
    L("hn_booking", "reveal", "حجزت ريما وعدنان قاعة المكتبة الصغيرة يوم الخميس عند الخامسة، ونموذج الحجز محفوظ عندي.", ["f_hall_booking_exists"]),
    L("hn_unknown", "deflect_unknown", "ليس عندي شيء عن هذا."),
    L("hn_off", "deflect_offtopic", "اسألني عن حجز القاعات."),
    L("hn_bye", "farewell", "مع السلامة.")])

locations = [{"id": "loc_library", "name_ar": "مكتبة جامعة القنطرة", "description_ar": "الكتب المعارة وسجلات الإعارة."},
             {"id": "loc_board", "name_ar": "سلسلة نقاش الصف", "description_ar": "منتدى الصف على بوابة المدرسة."},
             {"id": "loc_office", "name_ar": "المكتب المدرسي", "description_ar": "نماذج الحجز وجداول الامتحانات."},
             {"id": "loc_sijil", "name_ar": "دار السِّجِل", "description_ar": "أداة عدّ الحروف والجداول المرجعية."}]
objects = [{"id": "obj_sheet", "name_ar": "الورقة ذات الحروف المبدلة", "description_ar": "ورقة بخط اليد وُجدت بين صفحات كتاب معار."},
           {"id": "obj_msgs", "name_ar": "رسالتا النوارس", "description_ar": "رسالتان نُشرتا في سلسلة نقاش الصف."}]
orgs = [{"id": "org_school", "name_ar": "ثانوية القنطرة", "description_ar": "مدرسة خيالية استعارت الكتاب من مكتبة الجامعة."}]

# ---------------------------------------------------------------- facts
facts = []
def F(id, st, kind, subj, spoiler, time=None, loc=None, ko=None):
    d = {"id": id, "statement_ar": st, "kind": kind, "subject_ids": subj, "spoiler_level": spoiler}
    if time: d["time"] = time
    if loc: d["location_id"] = loc
    if ko: d["science_ko_refs"] = ko
    facts.append(d)
F("f_sheet_found", "عثرت أمينة المكتبة على ورقة بحروف مبدلة بين صفحات كتاب أُعيد إلى مكتبة الجامعة صباح الاثنين.", "event", ["obj_sheet", "sawsan"], 0)
F("f_msgs_posted", "ظهرت في سلسلة نقاش الصف رسالتان غامضتان بين ريما وعدنان: «النوارس أورقت» و«القارب الأحمر جاهز».", "event", ["obj_msgs", "rima", "adnan"], 0)
F("f_maher_suspects", "يظن مشرف الامتحانات أن الورقة والرسالتين خطة غش.", "attribute", ["maher"], 0)
F("f_maher_basis", "بنى مشرف الامتحانات ظنه على غموض الورقة والرسالتين، ولم يراجع جدول الامتحانات الرسمي.", "attribute", ["maher"], 1)
F("f_loan_record_exists", "للكتاب سجل إعارة في مكتبة الجامعة.", "state", ["sawsan", "loc_library"], 1)
F("f_loan_returned", "استعارت ريما الكتاب أول أمس وأعادته صباح الاثنين الساعة 08:30، والورقة بين صفحاته.", "event", ["rima", "obj_sheet"], 1, T(90), "loc_library")
F("f_ref_exists", "لدار السِّجِل جدول مرجعي منشور يرتّب الحروف العربية بحسب تكرارها.", "state", ["loc_sijil"], 1)
F("f_hall_booking_exists", "في المكتب المدرسي نموذج حجز قاعة باسم ريما وعدنان.", "state", ["hanan", "loc_office"], 1)
F("f_bakery_exists", "لدى عدنان إيصال طلب من مخبز.", "state", ["adnan"], 1)
F("f_print_exists", "لدى ريما إيصال طباعة بطاقات.", "state", ["rima"], 1)
F("f_codewords", "عبارتا الرسالتين اصطلاح بين الصديقين: «النوارس» هي بطاقات الدعوة المطبوعة، و«القارب الأحمر» هو علبة الكعكة.", "relation", ["rima", "adnan", "obj_msgs"], 2)
F("f_rima_wrote", "كتبت ريما الورقة تدرّباً على لعبة شفرة، ونسيتها بين صفحات الكتاب فلم تتعمد إخفاءها ولا تسليمها لأحد.", "event", ["rima", "obj_sheet"], 2, T(90), "loc_library", ["KO-RS-06-004"])
F("f_hall_booked", "حُجزت قاعة المكتبة الصغيرة يوم الخميس عند الخامسة باسم الطالبين لمناسبة تكريمية.", "state", ["rima", "adnan", "loc_office"], 1)
F("f_bakery_ordered", "طُلبت كعكة وعلبة حمراء تُسلَّم يوم الخميس عند الثالثة والنصف بعبارة تهنئة بالتقاعد.", "state", ["adnan"], 1)
F("f_exam_window", "الامتحانات انتهت قبل أسبوعين، ولا اختبار مقرر لصف الطالبين قبل خمسة أسابيع.", "state", ["loc_office"], 1)
F("f_key_fits", "ترتيب تكرار الحروف في الورقة يوافق في أعلاه ترتيب العربية، فالإبدال بسيط ثابت ويمكن فكه، مع الإقرار بأن العينة قصيرة.", "relation", ["obj_sheet", "loc_sijil"], 2, None, "loc_sijil", ["KO-RS-06-012"])
F("f_party_plan", "موضوع الورقة والرسالتين ترتيب مناسبة سرية لتكريم معلمة تتقاعد، لا اختبار ولا إجابات.", "relation", ["obj_sheet", "obj_msgs", "rima", "adnan"], 3, None, None, ["KO-RS-06-004", "KO-RS-06-006"])
F("f_not_exam", "لا صلة للورقة ولا للرسالتين بأي امتحان، فلا شيء فيهما من أسئلة أو إجابات أو موعد اختبار.", "relation", ["obj_sheet", "obj_msgs", "maher"], 3, None, None, ["KO-RS-06-002", "KO-RS-05-001"])
claims = [
    {"id": "cl_maher_cheat", "statement_ar": "الورقة والرسالتان خطة لتبادل إجابات اختبار قريب.", "kind": "honest_mistake", "held_by": ["maher"], "true_fact_id": "f_not_exam", "contradicted_by_evidence_ids": ["ev_decoded", "ev_exam_schedule", "ev_hall_booking"]},
    {"id": "cl_adnan_joke", "statement_ar": "هذه رسائل مزاح بيننا، ولا شيء وراءها.", "kind": "half_truth", "held_by": ["adnan"], "true_fact_id": "f_codewords", "contradicted_by_evidence_ids": ["ev_bakery_order", "ev_hall_booking"]},
]
timeline = [
    {"id": "te_msg1", "description_ar": "عدنان ينشر عبارة «النوارس أورقت» بدل أن يرسلها في محادثتهما الخاصة.", "time": T(10), "location_id": "loc_board", "actor_ids": ["adnan"], "fact_ids": ["f_msgs_posted"], "motivated_by_ar": "أراد أن يخبر ريما أن البطاقات صارت جاهزة"},
    {"id": "te_msg2", "description_ar": "ريما ترد بعبارة «القارب الأحمر جاهز» في السلسلة نفسها.", "time": T(25), "location_id": "loc_board", "actor_ids": ["rima"], "fact_ids": ["f_msgs_posted", "f_codewords"], "motivated_by_ar": "أرادت أن تؤكد أن العلبة جاهزة"},
    {"id": "te_return", "description_ar": "ريما تعيد الكتاب إلى مكتبة الجامعة والورقة بين صفحاته.", "time": T(90), "location_id": "loc_library", "actor_ids": ["rima"], "fact_ids": ["f_loan_returned", "f_rima_wrote"], "motivated_by_ar": "حان موعد إعادة الكتاب المعار"},
    {"id": "te_found", "description_ar": "أمينة المكتبة تجد الورقة بين الصفحات.", "time": T(135), "location_id": "loc_library", "actor_ids": ["sawsan"], "fact_ids": ["f_sheet_found"], "motivated_by_ar": "فحص روتيني للكتب المعادة"},
    {"id": "te_maher", "description_ar": "مشرف الامتحانات يطّلع على الورقة والرسالتين ويرفع الأمر.", "time": T(165), "location_id": "loc_office", "actor_ids": ["maher"], "fact_ids": ["f_maher_suspects", "f_maher_basis"], "motivated_by_ar": "قلق من الغش في المدرسة"},
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

_top_lines = "\n".join(f"{c}: {ar_n(n)} مرة" for c, n in TOP)
_top_ref = " ".join(REF_ORDER[:8])
_top_cipher_order = " ".join(c for c, _ in TOP[:6])
_worksheet_map = "\n".join(f"{c} ← {DEC[c]}" + ("  (مؤكد)" if c in CONFIRMED else "  (مرجّح من سياق الكلمة)") for c, _ in _cnt.most_common())
V("ev_cipher_sheet", "الورقة ذات الحروف المبدلة", "physical",
  "ورقة بخط اليد وُجدت بين صفحات كتاب معار، بلا عنوان ولا توقيع. أربعة أسطر:\n" + "\n".join(CIPHER) + "\n(بين الكلمات مسافات، ولا تظهر همزات ولا نقاط شكل.)",
  ["a_get_sheet"], ["f_sheet_found"], "strong",
  "تثبت وجود نص مكتوب بحروف مبدلة؛ لا تقول وحدها ما معناه ولا من كتبه ولا لماذا.", loc="loc_library")
V("ev_chat_msgs", "رسالتا سلسلة النقاش", "digital",
  "سلسلة نقاش الصف — صباح الاثنين\n07:10 عدنان: «النوارس أورقت.»\n07:25 ريما: «والقارب الأحمر جاهز.»\n(لم يردّ أحد، وحُذفت الرسالتان من السلسلة ظهراً.)",
  ["a_get_chat"], ["f_msgs_posted"], "moderate",
  "نصّان كُتبا بعبارات رمزية؛ يثبتان أن الصديقين تبادلا هذا الكلام، ولا يثبتان معناه ولا غرضه.", red=True, loc="loc_board")
V("ev_book_loan", "سجل إعارة الكتاب", "documentary",
  "سجل مكتبة جامعة القنطرة — الإعارة للمدارس\nالكتاب: «مبادئ في علم الحروف»\nالمستعير: ريما الحداد (ثانوية القنطرة)\nأُعير: الأحد 14:20\nأُعيد: الاثنين 08:30\nحالة الكتاب عند الإعادة: سليم، وُجدت ورقة بين الصفحات 41 و42",
  ["a_get_loan"], ["f_loan_returned"], "strong",
  "يثبت من استعار الكتاب ومتى أعاده؛ لا يثبت من كتب الورقة ولا أنها وُضعت بقصد.", loc="loc_library")
V("ev_ref_freq", "الجدول المرجعي لتكرار الحروف", "documentary",
  "دار السِّجِل — جدول تكرار الحروف في نصوص عربية منوعة (عينة 50 ألف حرف، بعد توحيد الهمزات والتاء المربوطة والألف المقصورة)\nالترتيب من الأكثر إلى الأقل:\n" + " ".join(REF_ORDER) + "\nملاحظة: الأحرف الخمسة الأولى تتقدم في معظم النصوص الطويلة، أما النصوص القصيرة فقد يتبدل الترتيب بعد المراتب الأولى.",
  ["a_get_ref"], ["f_ref_exists"], "strong",
  "جدول مرجعي لنصوص طويلة منوعة؛ لا يطابق بالضرورة ترتيب نص قصير بعينه.", loc="loc_sijil")
V("ev_freq_table", "جدول عدّ حروف الورقة", "lab_result",
  f"أداة العدّ في دار السِّجِل — الورقة ذات الحروف المبدلة\nأُعلن التوحيد قبل العدّ: الهمزات صارت ألفاً، والتاء المربوطة هاءً، والألف المقصورة ياءً، وأُهملت المسافات.\nعدد الأحرف المعدودة: {ar_n(N_LETTERS)} حرفاً\nأعلى ثمانية أحرف:\n{_top_lines}\nأقل الأحرف تكراراً مرّة أو مرتين: {ar_n(len(UNSURE))} حرفاً.",
  ["a_count_letters"], ["f_key_fits"], "moderate",
  "العينة قصيرة (نحو مئة حرف)؛ الفروق الصغيرة بين المراتب لا تدل على شيء، ولا يوثق إلا بالمراتب الأولى. والتوحيد قبل العد يغيّر الأعداد قليلاً.", red=True, ko="KO-RS-06-012", loc="loc_sijil")
V("ev_decoded", "ورقة الفك بعد المقارنة بالجدول", "lab_result",
  "ورقة الفك — مقارنة تكرار الورقة بالجدول المرجعي\nأبدلنا أولاً أكثر الأحرف تكراراً، ثم ثبّتنا الباقي بأنماط الكلمات (أداة التعريف في أول الكلمة وتكرار حرف في آخرها).\nجدول الإبدال:\n" + _worksheet_map +
  "\nالنص بعد الفك (بعد التوحيد):\n" + "\n".join(PLAIN),
  ["a_decode_compare"], ["f_key_fits"], "strong",
  "نتيجة قراءة لنص قصير؛ الأحرف المرجّحة من السياق قد تحتمل غيرها، ونص الفك يخبر بما كُتب لا بمن كتبه أو ما يريده منه الآخرون.", contradicts=["cl_maher_cheat"], ko="KO-RS-06-012", loc="loc_sijil")
V("ev_hall_booking", "نموذج حجز قاعة المكتبة الصغيرة", "documentary",
  "نموذج حجز قاعة — ثانوية القنطرة\nالحاجزان: ريما الحداد، عدنان البيطار\nالقاعة: المكتبة الصغيرة\nالموعد: الخميس 17:00\nالغرض: «لقاء تقدير لمعلمتنا السابقة الأستاذة لبنى»\nعدد الحضور المتوقع: 25\nموافقة: المكتب المدرسي",
  ["a_get_booking"], ["f_hall_booked"], "strong",
  "يثبت حجزاً ومناسبة مكتوبة؛ لا يثبت أن الورقة تخص هذا اللقاء، ولا يكفي وحده لنفي كل احتمال آخر.", contradicts=["cl_maher_cheat", "cl_adnan_joke"], loc="loc_office")
V("ev_bakery_order", "إيصال طلب كعكة", "documentary",
  "مخبز «السنابل» — إيصال طلب\nكعكة كبيرة بالشوكولا في علبة حمراء\nالاستلام: الخميس 15:30\nالعبارة المطلوبة على الكعكة: «شكراً يا أستاذتنا، وهنيئاً بالتقاعد»\nالطالب: عدنان البيطار",
  ["a_get_bakery"], ["f_bakery_ordered"], "strong",
  "إيصال تجاري يبيّن الطلب والعبارة؛ لا يبيّن ما كُتب في الورقة، ولا يثبت أن الطلب يخص الرسالتين إلا بمقارنة الاصطلاح.", contradicts=["cl_adnan_joke"], loc="loc_office")
V("ev_print_receipt", "إيصال طباعة بطاقات الدعوة", "documentary",
  "مطبعة الحي — إيصال\n30 بطاقة دعوة بشعار «نورس» أزرق\nتاريخ التسليم: الأحد\nصاحبة الطلب: ريما الحداد",
  ["a_get_print"], ["f_print_exists"], "moderate",
  "يثبت طباعة بطاقات بشعار نورس؛ لا يثبت وحده أن عبارة الرسالة تعني هذه البطاقات.", loc="loc_office")
V("ev_exam_schedule", "جدول الامتحانات المعلن", "documentary",
  "ثانوية القنطرة — لوحة الإعلانات\nانتهت امتحانات الفصل يوم الثلاثاء قبل الماضي.\nالاختبار القصير القادم لصف التاسع: بعد خمسة أسابيع من اليوم.\nلا اختبارات إضافية مقررة قبل ذلك.",
  ["a_get_exams"], ["f_exam_window"], "strong",
  "جدول رسمي معلن؛ لا يمنع في ذاته محاولة غش في اختبار غير معلن، لكن لا أثر لاختبار قريب.", loc="loc_office")
V("ev_maher_statement", "إفادة ماهر الصيرفي (ملخص)", "testimonial",
  "ملخص إفادة ماهر الصيرفي:\n«رأيت ورقة بحروف غريبة ورسالتين غامضتين، فظننتها خطة غش. لم أراجع جدول الامتحانات الرسمي.»",
  ["a_note_maher"], ["f_maher_basis"], "weak",
  "ظن صاحبه من غموض النص؛ لا يقاس بالظن بل بالجدول والسجلات.", loc="loc_office")
V("ev_rima_statement", "إفادة ريما الحداد (ملخص)", "testimonial",
  "ملخص إفادة ريما الحداد:\n«كتبت الورقة تدرباً على لعبة شفرة، ونسيتها في الكتاب. وعبارتا الرسالتين اصطلاح بيني وبين عدنان.»",
  ["a_note_rima"], ["f_rima_wrote"], "weak",
  "إفادة صاحبة الشأن؛ تؤيدها سجلات الإعارة والحجز ولا تغني عنها.", loc="loc_library")
V("ev_adnan_statement", "إفادة عدنان البيطار (ملخص)", "testimonial",
  "ملخص إفادة عدنان البيطار:\n«قلت إنها مزحة لأني لم أرد أن أفسد المفاجأة. طلبت الكعكة بنفسي.»",
  ["a_note_adnan"], ["f_bakery_exists"], "weak",
  "إفادة صاحب مصلحة في بقاء السر؛ يعدّل قوله الأول بعد أن رأى الإيصالات.", loc="loc_office")
V("ev_sawsan_statement", "إفادة سوسن الخطيب (ملخص)", "testimonial",
  "ملخص إفادة سوسن الخطيب:\n«وجدت الورقة بين الصفحتين 41 و42 حين فحصت الكتاب المعاد. لا أعرف شيئاً عن غرضها.»",
  ["a_note_sawsan"], ["f_loan_record_exists"], "moderate",
  "شهادة على موضع الورقة فقط، ولا تقول شيئاً عن كاتبها أو غرضها.", loc="loc_library")

# ---------------------------------------------------------------- inferences
def P(t, i): return {"ref_type": t, "ref_id": i}
inf = []
def I(id, prem, ct, concl, rel, strength, rule, ks):
    inf.append({"id": id, "premises": prem, "conclusion": {"ref_type": ct, "ref_id": concl}, "relation": rel, "strength": strength, "rule_ar": rule, "skill_ko_refs": ks})
# path A: reading the cipher
I("i_a_key", [P("evidence", "ev_cipher_sheet"), P("evidence", "ev_freq_table"), P("evidence", "ev_ref_freq")], "fact", "f_key_fits", "establishes", "strong",
  "أكثر أحرف الورقة تكراراً تقابل أكثر حروف العربية تكراراً في الجدول المرجعي، فالإبدال ثابت ويمكن فكه، مع التنبيه إلى قصر العينة.", ["KO-RS-06-012"])
I("i_a_plan", [P("fact", "f_key_fits"), P("evidence", "ev_decoded")], "fact", "f_party_plan", "establishes", "strong",
  "النص الذي خرج من الفك متصل ومفهوم، وموضوعه تهيئة مناسبة سرية لمعلمة؛ فهذا ما تقوله الورقة.", ["KO-RS-06-004"])
I("i_a_noexam", [P("fact", "f_key_fits"), P("evidence", "ev_decoded")], "fact", "f_not_exam", "establishes", "strong",
  "لا ورد في النص المفكوك سؤال ولا مادة ولا موعد اختبار، فليس خطة لتبادل إجابات.", ["KO-RS-06-004", "KO-RS-06-002"])
# path B: records, no decipherment
I("i_b_plan", [P("evidence", "ev_hall_booking"), P("evidence", "ev_bakery_order")], "fact", "f_party_plan", "establishes", "strong",
  "حجز القاعة بغرض تقدير معلمة وطلب كعكة بعبارة تهنئة بالتقاعد في اليوم نفسه يفسران الرسالتين دون الحاجة إلى فك الورقة.", ["KO-RS-06-006"])
I("i_b_noexam", [P("evidence", "ev_exam_schedule"), P("evidence", "ev_hall_booking")], "fact", "f_not_exam", "establishes", "strong",
  "الامتحانات انتهت ولا اختبار قبل خمسة أسابيع، والحجز مكتوب لمناسبة تقدير؛ فلا موضع لخطة غش في هذه الأيام.", ["KO-RS-06-002", "KO-RS-05-001"])
I("i_wrote", [P("evidence", "ev_book_loan"), P("evidence", "ev_rima_statement")], "fact", "f_rima_wrote", "establishes", "strong",
  "سجل الإعارة يضع الكتاب بيد ريما وقت وجود الورقة، وإفادتها تقول إنها كتبتها تدرباً وسهت عنها؛ وهذا لا يدل على قصد الإخفاء.", ["KO-RS-06-004"])
I("i_codes", [P("evidence", "ev_print_receipt"), P("evidence", "ev_chat_msgs")], "fact", "f_codewords", "supports", "suggestive",
  "طباعة بطاقات بشعار نورس تقابل «النوارس أورقت»، لكنها لا تثبت المعنى وحدها.", ["KO-RS-06-006"])
I("i_claim_maher", [P("fact", "f_not_exam")], "claim", "cl_maher_cheat", "contradicts_claim", "strong",
  "ظن الغش جاء من غموض الشكل لا من محتوى؛ وحين وُجد المحتوى والجدول لم يبق للظن سند.", ["KO-RS-05-001", "KO-RS-05-014"])
I("i_claim_adnan", [P("evidence", "ev_bakery_order"), P("evidence", "ev_hall_booking")], "claim", "cl_adnan_joke", "contradicts_claim", "strong",
  "الإيصال والحجز يبيّنان تحضيراً حقيقياً؛ فكلام عدنان «مزاح» أخفى سراً لا مزحة، وإخفاء المفاجأة ليس إخفاء لذنب.", ["KO-RS-05-014"])
I("i_support_party", [P("fact", "f_party_plan")], "hypothesis", "h_party", "supports", "strong",
  "التكريم السري يفسر الورقة والرسالتين والحجز والإيصال معاً، ويفسر لماذا بقي المضمون مستوراً.", ["KO-RS-06-006"])
I("i_rule_cheat", [P("fact", "f_not_exam")], "hypothesis", "h_cheat", "rules_out", "conclusive",
  "لو كانت خطة غش لوُجد فيها ما يخص اختباراً قريباً؛ وليس في النص ولا في الجدول ما يدل على ذلك.", ["KO-RS-06-008"])
I("i_rule_cheat_b", [P("fact", "f_party_plan")], "hypothesis", "h_cheat", "rules_out", "strong",
  "إذا كان للورقة موضوع آخر موثق بحجز وإيصال فلا يبقى لتفسير الغش حاجة.", ["KO-RS-06-008"])
I("i_rule_nonsense", [P("fact", "f_key_fits")], "hypothesis", "h_nonsense", "rules_out", "strong",
  "تطابق مراتب التكرار مع الجدول وخروج نص مفهوم عند الفك يدلان على أن الورقة ليست حروفاً عشوائية.", ["KO-RS-06-012"])
I("i_rule_nonsense_b", [P("fact", "f_party_plan")], "hypothesis", "h_nonsense", "rules_out", "strong",
  "الحجز والإيصال يربطان الرسالتين بحدث حقيقي، فليست بلا معنى.", ["KO-RS-06-008"])

# ---------------------------------------------------------------- character knowledge
K = lambda f, a="witnessed", c="certain": {"fact_id": f, "access": a, "certainty": c}
ck = [
    {"character_id": "maher", "knows": [K("f_maher_basis")], "hides": [], "believes": [{"claim_id": "cl_maher_cheat", "stance": "sincere"}]},
    {"character_id": "rima", "knows": [K("f_loan_returned")],
     "hides": [{"fact_id": "f_codewords", "reveal_when": {"presented": {"evidence_id": "ev_chat_msgs", "to_character": "rima"}}, "cover_claim_id": None, "reveal_line_id": "rm_codes"},
               {"fact_id": "f_print_exists", "reveal_when": {"presented": {"evidence_id": "ev_chat_msgs", "to_character": "rima"}}, "cover_claim_id": None, "reveal_line_id": "rm_codes"},
               {"fact_id": "f_rima_wrote", "reveal_when": {"presented": {"evidence_id": "ev_book_loan", "to_character": "rima"}}, "cover_claim_id": None, "reveal_line_id": "rm_wrote"}], "believes": []},
    {"character_id": "adnan", "knows": [],
     "hides": [{"fact_id": "f_bakery_exists", "reveal_when": {"presented": {"evidence_id": "ev_chat_msgs", "to_character": "adnan"}}, "cover_claim_id": "cl_adnan_joke", "reveal_line_id": "ad_bakery"},
               {"fact_id": "f_codewords", "reveal_when": {"presented": {"evidence_id": "ev_chat_msgs", "to_character": "adnan"}}, "cover_claim_id": "cl_adnan_joke", "reveal_line_id": "ad_bakery"}],
     "believes": [{"claim_id": "cl_adnan_joke", "stance": "deliberate_lie"}]},
    {"character_id": "sawsan", "knows": [K("f_loan_record_exists", "professional"), K("f_ref_exists", "professional")], "hides": [], "believes": []},
    {"character_id": "hanan", "knows": [K("f_hall_booking_exists", "professional")], "hides": [], "believes": []},
]
hyps = [
    {"id": "h_cheat", "statement_ar": "الورقة والرسالتان خطة لتبادل إجابات في اختبار قريب.", "is_true": False, "plausibility_at_start": "high"},
    {"id": "h_nonsense", "statement_ar": "الورقة حروف عشوائية بلا معنى يمكن فكه، والرسالتان مزحة فارغة.", "is_true": False, "plausibility_at_start": "medium"},
    {"id": "h_party", "statement_ar": "الورقة والرسالتان تحضير لمناسبة تكريمية سرية، وبقيت الورقة في الكتاب سهواً.", "is_true": True, "plausibility_at_start": "low", "suspect_id": "rima"},
]
mis = [
    {"id": "rh_chat", "points_to_hypothesis_id": "h_cheat", "planted_via_ar": "رسالتان غامضتان تتبادلهما طالبان صباح يوم دراسي مع ورقة مشفرة.", "evidence_ids": ["ev_chat_msgs"],
     "refuted_by_inference_ids": ["i_rule_cheat", "i_rule_cheat_b", "i_claim_maher"],
     "fairness_note_ar": "الغموض ليس دليل غش؛ جدول الامتحانات المعلن وحجز القاعة وإيصال المخبز متاحة للاعب بلا مفاتيح خفية، ونص الفك متاح بالعدّ والمقارنة."},
    {"id": "rh_freq", "points_to_hypothesis_id": "h_nonsense", "planted_via_ar": "جدول العدّ لعينة قصيرة تبدو فيه فروق صغيرة بين المراتب، فقد يظن اللاعب أن لا نمط.", "evidence_ids": ["ev_freq_table"],
     "refuted_by_inference_ids": ["i_rule_nonsense", "i_rule_nonsense_b", "i_a_key"],
     "fairness_note_ar": "الجدول نفسه يعلن قصر العينة ويبيّن أن المراتب الأولى فقط يوثق بها، وهي تطابق الجدول المرجعي؛ والحجز والإيصال يؤكدان وجود معنى من خارج الورقة."},
]
los = [
    {"id": "lo_induct", "statement_ar": "يقدّر ما تسمح به عينة قصيرة من الحروف، ويوثّق المراتب الأولى دون غيرها.", "skill_ko_ref": "KO-RS-06-012", "observable_behaviors_ar": ["يشغّل العدّ ويقارنه بالمرجع", "يذكر قصر العينة حداً"], "evidence_sources": ["action_log", "final_justification"]},
    {"id": "lo_source", "statement_ar": "يفرّق بين السجل الأصلي والنص المفكوك والقول، ويقيس القول بالسجل.", "skill_ko_ref": "KO-RS-06-002", "observable_behaviors_ar": ["يصنّف المصادر", "لا يبني على الظن"], "evidence_sources": ["evidence_board"]},
    {"id": "lo_hyp", "statement_ar": "يولّد فرضيات متعددة ويستبعد ما تنقضه الأدلة.", "skill_ko_ref": "KO-RS-06-006", "observable_behaviors_ar": ["يضيف فرضيات", "يستبعد بدليل"], "evidence_sources": ["hypothesis_ledger"]},
    {"id": "lo_obs", "statement_ar": "يفصل بين ما تقوله الورقة وما يُستنتج عن غرضها.", "skill_ko_ref": "KO-RS-06-004", "observable_behaviors_ar": ["يربط الدليل بالفرضية باتجاه صحيح", "يميز الفك من الغرض"], "evidence_sources": ["evidence_board", "final_justification"]},
    {"id": "lo_calib", "statement_ar": "يصوغ نسبة الترجيح بحدودها.", "skill_ko_ref": "KO-RS-06-021", "observable_behaviors_ar": ["يختار ثقة معقولة", "يذكر حدوداً"], "evidence_sources": ["final_justification"]},
    {"id": "lo_revise", "statement_ar": "يراجع رأيه الأول حين يظهر ما يخالفه.", "skill_ko_ref": "KO-RS-06-009", "observable_behaviors_ar": ["يغيّر فرضيته الرائدة بدليل"], "evidence_sources": ["hypothesis_ledger"]},
]
def levels(d): return [{"score": i, "descriptor_ar": t} for i, t in enumerate(d)]
rub = {
    "reference_answer_ar": "فكّ الإبدال صحيح، لكن الواقع بريء: الورقة تدبير مناسبة سرية لتكريم معلمة متقاعدة، لا خطة غش. جدول العدّ لعينة قصيرة يوافق في مراتبه الأولى ترتيب العربية، والنص المفكوك متصل ولا يذكر اختباراً. ويتفق معه مسار مستقل من السجلات: حجز القاعة لمناسبة تقدير، وإيصال كعكة بعبارة تهنئة بالتقاعد، وجدول امتحانات لا يضم اختباراً قريباً. كتبت ريما الورقة تدرباً ونسيتها في كتاب معار. حدود الاستنتاج: العينة قصيرة وبعض الأحرف مرجّحة بالسياق، ولا يثبت الفك نية كاتبته، ولا نعرف إن كانت هناك أوراق أخرى.",
    "criteria": [
        {"id": "c_source", "name_ar": "تصنيف المصادر", "objective_ids": ["lo_source"], "scored_by": "deterministic", "weight": 0.15, "levels": levels(["لم يصنّف", "أخطأ في الأغلب", "نصف صحيح", "معظمه صحيح", "كله صحيح"])},
        {"id": "c_conflict", "name_ar": "ترتيب الأدلة على الخط الزمني", "objective_ids": ["lo_obs"], "scored_by": "deterministic", "weight": 0.2, "levels": levels(["لم يضع شيئاً", "وضع قليلاً", "وضع نصفها صحيحاً", "معظمها", "كلها في موضعها"])},
        {"id": "c_links", "name_ar": "ربط الأدلة بالفرضيات", "objective_ids": ["lo_induct", "lo_obs"], "scored_by": "deterministic", "weight": 0.2, "levels": levels(["لا روابط", "قليلة", "نصفها صحيح", "معظمها", "كلها دقيقة"])},
        {"id": "c_uncertainty", "name_ar": "معايرة الثقة", "objective_ids": ["lo_calib"], "scored_by": "deterministic", "weight": 0.15, "levels": levels(["ثقة مفرطة", "حدود قليلة", "جزئية", "معقولة", "معايَرة كاملة"])},
        {"id": "c_revision", "name_ar": "مراجعة الرأي", "objective_ids": ["lo_revise"], "scored_by": "deterministic", "weight": 0.1, "levels": levels(["بقي على فرضية مرفوضة", "لم يعلن فرضية", "ثبت على فرضية سليمة", "غيّر بدليل", "غيّر بدليل ووثّق"])},
        {"id": "c_elimination", "name_ar": "استبعاد الفرضيات الخاطئة", "objective_ids": ["lo_hyp"], "scored_by": "deterministic", "weight": 0.1, "levels": levels(["لم يستبعد", "استبعد خطأً", "فرضية بدليل", "فرضيتين", "كل الخاطئة"])},
        {"id": "c_justification", "name_ar": "جودة الحجة المكتوبة", "objective_ids": ["lo_induct", "lo_hyp"], "scored_by": "human", "weight": 0.1, "levels": levels(["لا حجة", "ادعاء بلا سند", "أدلة دون ربط", "ربط الأدلة بالاستنتاج", "ربط مع البدائل والحدود"])},
    ],
}
def H(id, lv, kind, text, trig, target=None, w=0.0):
    d = {"id": id, "level": lv, "kind": kind, "text_ar": text, "trigger": trig, "assessment_weight": w}
    if target: d["targets_inference_id"] = target
    return d
he = lambda e: {"has_evidence": e}
hints = [
    H("hg1", 1, "metacognitive", "ما الفرق بين أن تعرف ما كُتب وأن تعرف لماذا كُتب؟", {"always": True}, None, 0.02),
    H("hg2", 2, "focus_area", "حين تفحص الأدلة اسأل: هل وجودها في الملف يتعلق بما تقوله الورقة، أم بما يفعله أصحابها في اليوم نفسه؟", he("ev_chat_msgs"), None, 0.04),
    H("hk1", 1, "metacognitive", "كم حرفاً في عينتك؟ وهل يكفي لتثق بترتيب الأحرف كلها؟", he("ev_cipher_sheet"), "i_a_key", 0.02),
    H("hk2", 2, "pointer", "قارن أعلى الأحرف تكراراً في الورقة بما يقابلها في جدول دار السِّجِل، ثم ثبّت الباقي بأنماط الكلمات.", he("ev_cipher_sheet"), "i_a_key", 0.06),
    H("hk3", 3, "partial_reveal", "استعمل أداة العدّ في دار السِّجِل ثم قارنها بالجدول المرجعي وسترى أي الأحرف مؤكد وأيها مرجّح.", he("ev_cipher_sheet"), "i_a_key", 0.1),
    H("hb1", 1, "metacognitive", "لو لم تفك الورقة أبداً، ما الذي في السجلات الرسمية يصلح لتفسير الرسالتين؟", he("ev_chat_msgs"), "i_b_plan", 0.02),
    H("hb2", 2, "pointer", "اسأل المكتب المدرسي عن حجوزات الطالبين، واسأل عدنان عمّا طلبه.", he("ev_chat_msgs"), "i_b_plan", 0.06),
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
Act("a_get_sheet", "examine", "افحص الورقة التي وُجدت في الكتاب", al, [G("ev_cipher_sheet")], "loc_library", "GET_SHEET")
Act("a_get_chat", "examine", "افتح سلسلة نقاش الصف", al, [G("ev_chat_msgs")], "loc_board", "GET_CHAT")
Act("a_get_exams", "examine", "اقرأ جدول الامتحانات المعلن", al, [G("ev_exam_schedule")], "loc_office", "GET_EXAMS")
for cid, lab in [("maher", "ماهر"), ("rima", "ريما"), ("adnan", "عدنان"), ("sawsan", "سوسن"), ("hanan", "حنان")]:
    Act(f"a_int_{cid}", "interview", f"ابدأ مقابلة {lab}", al, [{"op": "raise_trust", "ref_id": cid, "amount": 1}], cid, f"INT_{cid.upper()}")
Act("a_get_loan", "examine", "اطلب سجل إعارة الكتاب", fu("f_loan_record_exists"), [G("ev_book_loan")], "loc_library", "GET_LOAN")
Act("a_get_ref", "examine", "اقرأ الجدول المرجعي لتكرار الحروف", fu("f_ref_exists"), [G("ev_ref_freq")], "loc_sijil", "GET_REF")
Act("a_count_letters", "request_lab_test", "اعدد حروف الورقة في دار السِّجِل", he("ev_cipher_sheet"), [G("ev_freq_table")], "loc_sijil", "COUNT_LETTERS")
Act("a_decode_compare", "request_lab_test", "قارن العدّ بالجدول المرجعي وجرّب الفك", {"all": [he("ev_freq_table"), he("ev_ref_freq")]}, [G("ev_decoded")], "loc_sijil", "DECODE_COMPARE")
Act("a_get_booking", "examine", "اطلب نموذج حجز القاعة", fu("f_hall_booking_exists"), [G("ev_hall_booking")], "loc_office", "GET_BOOKING")
Act("a_get_bakery", "examine", "اطلب إيصال المخبز من عدنان", fu("f_bakery_exists"), [G("ev_bakery_order")], "loc_office", "GET_BAKERY")
Act("a_get_print", "examine", "اطلب إيصال الطباعة من ريما", fu("f_print_exists"), [G("ev_print_receipt")], "loc_office", "GET_PRINT")
Act("a_note_maher", "examine", "دوّن إفادة ماهر", fu("f_maher_basis"), [G("ev_maher_statement")], "maher", "NOTE_MAHER")
Act("a_note_rima", "examine", "دوّن إفادة ريما", fu("f_rima_wrote"), [G("ev_rima_statement")], "rima", "NOTE_RIMA")
Act("a_note_adnan", "examine", "دوّن إفادة عدنان", fu("f_bakery_exists"), [G("ev_adnan_statement")], "adnan", "NOTE_ADNAN")
Act("a_note_sawsan", "examine", "دوّن إفادة سوسن", fu("f_loan_record_exists"), [G("ev_sawsan_statement")], "sawsan", "NOTE_SAWSAN")
Act("p_chat_rima", "present_evidence", "اعرض رسالتي النقاش على ريما", {"presented": {"evidence_id": "ev_chat_msgs", "to_character": "rima"}}, [{"op": "emit_event", "ref_id": "PRESENTED_CHAT_RIMA"}], "rima", "P_CHAT_RIMA", 0)
Act("p_chat_adnan", "present_evidence", "اعرض رسالتي النقاش على عدنان", {"presented": {"evidence_id": "ev_chat_msgs", "to_character": "adnan"}}, [{"op": "emit_event", "ref_id": "PRESENTED_CHAT_ADNAN"}], "adnan", "P_CHAT_ADNAN", 0)
Act("p_loan_rima", "present_evidence", "اعرض سجل الإعارة على ريما", {"presented": {"evidence_id": "ev_book_loan", "to_character": "rima"}}, [{"op": "emit_event", "ref_id": "PRESENTED_LOAN_RIMA"}], "rima", "P_LOAN_RIMA", 0)
Act("a_hint", "request_hint", "اطلب تلميحاً", al, [], None, "REQUEST_HINT", 0)
Act("a_accuse", "final_accusation", "قدّم الاستنتاج النهائي", al, [{"op": "emit_event", "ref_id": "SUBMIT"}], None, "FINAL_ACCUSATION", 0)

topics = [
    {"id": "t_suspicion", "label_ar": "سبب الظن بالغش", "example_questions_ar": ["لماذا ظننت أنها خطة غش؟", "هل راجعت جدول الامتحانات؟"], "fact_ids": ["f_maher_basis"], "claim_ids": ["cl_maher_cheat"]},
    {"id": "t_book", "label_ar": "الكتاب والورقة", "example_questions_ar": ["أين وجدت الورقة؟", "هل للكتاب سجل إعارة؟", "هل هناك جدول لتكرار الحروف؟", "هل كتبتِ هذه الورقة؟"], "fact_ids": ["f_loan_record_exists", "f_ref_exists", "f_rima_wrote"]},
    {"id": "t_messages", "label_ar": "رسالتا النوارس", "example_questions_ar": ["ماذا تعني «النوارس أورقت»؟", "وما «القارب الأحمر»؟", "هل كانت مزحة؟"], "fact_ids": ["f_codewords", "f_print_exists"], "claim_ids": ["cl_adnan_joke"]},
    {"id": "t_prep", "label_ar": "الحجز والطلبات", "example_questions_ar": ["هل حجزتما قاعة؟", "هل طلبتَ شيئاً من مخبز؟"], "fact_ids": ["f_hall_booking_exists", "f_bakery_exists"]},
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
    (1, "عدّ حروف الورقة (نحو مئة حرف) يعطي مراتب أولى توافق ترتيب الحروف في الجدول المرجعي؛ فالإبدال ثابت وقابل للفك مع الاعتراف بقصر العينة.", ["ev_cipher_sheet", "ev_freq_table", "ev_ref_freq"], "i_a_key"),
    (2, "النص الذي ظهر عند الفك متصل، ويدور حول ترتيب مناسبة لمعلمة، ولا يحوي ما يخص امتحاناً.", ["ev_decoded"], "i_a_plan"),
    (3, "مسار مستقل لا يحتاج إلى فك: حجز القاعة لمناسبة تقدير وإيصال المخبز بعبارة التهنئة يفسران الرسالتين.", ["ev_hall_booking", "ev_bakery_order"], "i_b_plan"),
    (4, "جدول الامتحانات يخلو من اختبار قريب، فظن الغش لم يستند إلى محتوى بل إلى غموض الشكل.", ["ev_exam_schedule", "ev_hall_booking"], "i_b_noexam"),
    (5, "سجل الإعارة وإفادة ريما يبيّنان أنها كتبت الورقة تدرباً ونسيتها في الكتاب، ولم تقصد إخفاءها.", ["ev_book_loan", "ev_rima_statement"], "i_wrote"),
    (6, "فك الشفرة أجاب عن سؤال «ماذا كُتب؟» فقط، أما «لماذا؟» فأجابت عنه السجلات من خارج الورقة.", ["ev_decoded", "ev_hall_booking"], "i_rule_cheat"),
]
ending = {
    "steps": [{"order": o, "text_ar": t, "uses_evidence_ids": u, "inference_id": i} for o, t, u, i in steps],
    "alternative_paths_ar": [
        "يمكن الوصول إلى النتيجة دون فك الورقة، من حجز القاعة وإيصال المخبز وجدول الامتحانات، لكن من يكتفي بذلك يترك الورقة نفسها بلا تفسير.",
        "ويمكن الوصول إليها من عدّ الحروف ومقارنتها بالمرجع والفك وحده، لكن الأقوى أن يتفق المساران.",
    ],
    "what_evidence_could_not_show_ar": [
        "العينة قصيرة (نحو مئة حرف)، وبعض أحرف الفك مرجّح من سياق الكلمة لا من عدد التكرار.",
        "لا تثبت الأدلة أنه لا توجد أوراق أخرى مكتوبة بالشفرة نفسها.",
        "فك الشفرة لا يثبت نية الكاتبة؛ ما أثبتها هو الحجز والإيصال وإفادتها.",
    ],
    "science_notes_ar": [
        "تكرار الحروف يعمل جيداً مع نصوص طويلة؛ في النصوص القصيرة يوثق بالمراتب الأولى فقط وتُثبَّت البقية بأنماط الكلمات.",
        "قبل العدّ تُوحَّد الهمزات والتاء المربوطة والألف المقصورة، ويجب إعلان ذلك لأنه يغيّر الأعداد.",
        "السر ليس دليلاً على الذنب؛ يُقاس التفسير بسجلات مستقلة يمكن تتبّع أصلها (سلسلة العهدة)، ثم تُعلن نسبة الترجيح بحدودها.",
        "بطاقة الأصل (خبر تراثي منسوب): تتصل الفكرة بما رُوي قديماً عن عدّ الحروف لقراءة المكتوب المغلق، وقد أُعيدت صياغتها كلها في موقف مدرسي خيالي، وليست هذه الحكاية «الأولى» في التاريخ.",
    ],
}
core = {
    "schema_version": "0.1.0", "case_id": CID, "case_version": "0.1.0",
    "meta": {"title_ar": "رسالة النوارس", "title_en": "The Seagull Message", "age_band": "13-15", "locale": "ar", "dialogue_register": "msa", "estimated_minutes": 25, "difficulty": 2,
             "content_flags": ["no_violence"], "authors": ["فريق أثر التحريري (مسودة بمساعدة الذكاء الاصطناعي، لم تُراجَع بشرياً بعد)"],
             "knowledge_object_refs": ["KO-RS-06-012", "KO-RS-06-002", "KO-RS-06-006", "KO-RS-06-004", "KO-RS-06-008", "KO-RS-06-021", "KO-RS-06-009", "KO-RS-05-001"]},
    "premise": {"hook_ar": "ورقة بحروف مبدلة وجدت بين صفحات كتاب معار، ورسالتان لا يفهمهما أحد. والمشرف مقتنع بأنها خطة غش.",
                "player_role_ar": "أنت متدرب في دار السِّجِل، وطُلب منك أن تقرأ الورقة والرسالتين وتخبر المشرف بما يمكن قوله فعلاً.",
                "setting_ar": "ثانوية القنطرة ومكتبة الجامعة المجاورة، صباح يوم اثنين. سجلات المكتبة والمكتب بتوقيت المبنى.",
                "public_fact_ids": ["f_sheet_found", "f_msgs_posted", "f_maher_suspects"],
                "assumed_general_knowledge_ar": ["في الإبدال الحرفي البسيط يقابل كل حرف حرفاً واحداً ثابتاً", "الحروف العربية لا تتساوى في تكرارها"]},
    "entities": {"characters": chars, "locations": locations, "objects": objects, "organizations": orgs},
    "truth": {"solution": {"culprit_ids": ["rima"], "summary_ar": "لم تُدبَّر مخالفة. أما الورقة فكتبتها ريما للتدرب على لعبة رموز ونسيتها في كتاب معار، وكانت هي وعدنان يرتبان لقاء تكريم سرياً، فاستعملا عبارات اصطلاحية في رسالتين نُشرتا بالخطأ. ظن المشرف أنها خطة غش قبل أن يطّلع على محتوى أو جدول.", "key_fact_ids": ["f_party_plan", "f_not_exam"]},
              "facts": facts, "claims": claims},
    "timeline": timeline, "evidence": ev, "evidence_graph": {"inferences": inf},
    "character_knowledge": ck, "hypotheses": hyps, "misdirection_plan": mis, "learning_objectives": los,
    "mechanics": {"time_budget_units": 40, "actions": A},
    "state_machine": {"id": "c017", "initial": "briefing", "type": "compound", "states": {
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
    "clock": {"epoch_hhmm": "07:00", "zone_label_ar": "توقيت المدرسة"},
    "cover": {"title_ar": "رسالة النوارس", "tagline_ar": "ورقة بحروف مبدلة، وطالبان يتبادلان كلاماً لا يفهمه أحد", "kicker_ar": "الملف السابع عشر · الاستقراء", "glyph": "◬", "accent": "cyan"},
    "cold_open_ar": ["الاثنين، قبل الظهر.", "أعادت طالبة كتاباً إلى مكتبة الجامعة، وبين صفحاته ورقة مليئة بحروف لا تكوّن كلمات.", "وفي سلسلة نقاش الصف رسالتان: «النوارس أورقت، والقارب الأحمر جاهز».", "يقول المشرف إنه يعرف ما هذا. ابدأ بسؤال أبسط: ما الذي تقوله الورقة فعلاً؟ ثم اسأل: وهل هذا هو السؤال المهم؟"],
    "labs": [],
    "source_classes": [
        {"id": "primary_record", "label_ar": "سجل أصلي", "help_ar": "يُنتجه نظام أو شخص لحظة الحدث، كسجل إعارة أو إيصال أو نموذج حجز."},
        {"id": "redisplay", "label_ar": "نسخة معروضة", "help_ar": "معلومة نُقلت من سجل آخر أو أُعيد عرضها، كنص مكتوب بخط اليد."},
        {"id": "claim", "label_ar": "قول أو تصريح", "help_ar": "إفادة شخص؛ تُقاس بالسجلات لا بنبرة صاحبها."},
        {"id": "template", "label_ar": "قالب أو نموذج", "help_ar": "نص جاهز لا يصف الحدث الفعلي بذاته."},
        {"id": "public_document", "label_ar": "وثيقة منشورة", "help_ar": "وثيقة معلنة ومعروف ناشرها، كجدول مرجعي أو إعلان."}],
    "limit_menu": [
        {"id": "l_short_sample", "label_ar": "العينة قصيرة، فبعض أحرف الفك مرجّح من السياق لا من عدد التكرار"},
        {"id": "l_intent", "label_ar": "فك الورقة لا يثبت نية كاتبتها؛ ذلك مستفاد من السجلات والإفادة"},
        {"id": "l_other_sheets", "label_ar": "الأدلة لا تنفي وجود أوراق أخرى مكتوبة بالشفرة نفسها"},
        {"id": "l_invalid_secret", "label_ar": "كتمان الطالبين للسر يثبت أنهما يخفيان مخالفة"},
        {"id": "l_invalid_code", "label_ar": "استعمال الشفرة وحده يدل على الغش"}],
    "mind_change_menu": [
        {"id": "m_exam_notice", "label_ar": "ظهور اختبار مفاجئ كان مقرراً لصف الطالبين في ذلك الأسبوع"},
        {"id": "m_other_text", "label_ar": "ظهور ورقة أخرى بالشفرة نفسها تحوي أسئلة أو إجابات"},
        {"id": "m_booking_fake", "label_ar": "ثبوت أن نموذج الحجز أو إيصال المخبز مصطنع بعد الحادثة"},
        {"id": "m_popular", "label_ar": "كثرة من يظنون أن الورقة خطة غش"}],
    "skills": [{"skill_id": "KO-RS-06-012", "track": "B"}, {"skill_id": "KO-RS-06-002", "track": "B"}, {"skill_id": "KO-RS-06-006", "track": "D"}],
    "stage_hooks_ar": {"briefing": "حروف مبدلة ورسالتان غامضتان… فهل الغموض دليل؟", "investigating": "عدّ الحروف قد يقرأ الورقة، فهل يقرأ صاحبتها أيضاً؟", "review": "قبل أن تغلق الملف: ما الذي لا تعرفه؟", "resolved": "أُغلق الملف. ملف جديد ينتظر في الأرشيف."},
    "character_glyphs": {"maher": "م", "rima": "ر", "adnan": "ع", "sawsan": "س", "hanan": "ح"},
}
sc = {
    "case_id": CID,
    "accepted_conclusions": {"h_party": {"grade": 1, "note_ar": "استنتاج متسق مع الأدلة ويتطلب ذكر حدوده."},
                             "h_cheat": {"grade": 0, "note_ar": "يخلط بين غموض الشكل ودليل الغش، ويتجاهل جدول الامتحانات والحجز."},
                             "h_nonsense": {"grade": 0, "note_ar": "يهمل أن المراتب الأولى للتكرار توافق العربية وأن السجلات تعطي الرسالتين معنى."}},
    "confidence_band": {"h_party": [65, 90], "h_cheat": [0, 15], "h_nonsense": [0, 15]},
    "source_key": {"ev_cipher_sheet": "redisplay", "ev_chat_msgs": "redisplay", "ev_book_loan": "primary_record", "ev_ref_freq": "public_document", "ev_freq_table": "redisplay",
                   "ev_decoded": "redisplay", "ev_hall_booking": "primary_record", "ev_bakery_order": "primary_record", "ev_print_receipt": "primary_record", "ev_exam_schedule": "public_document",
                   "ev_maher_statement": "claim", "ev_rima_statement": "claim", "ev_adnan_statement": "claim", "ev_sawsan_statement": "claim"},
    "link_key": {
        "h_party": {"ev_decoded": "supports", "ev_freq_table": "supports", "ev_ref_freq": "supports", "ev_hall_booking": "supports", "ev_bakery_order": "supports", "ev_print_receipt": "supports", "ev_exam_schedule": "supports", "ev_book_loan": "supports", "ev_chat_msgs": "neutral"},
        "h_cheat": {"ev_chat_msgs": "supports", "ev_exam_schedule": "weakens", "ev_decoded": "weakens", "ev_hall_booking": "weakens", "ev_bakery_order": "weakens"},
        "h_nonsense": {"ev_freq_table": "supports", "ev_decoded": "weakens", "ev_ref_freq": "weakens", "ev_hall_booking": "weakens"},
    },
    "required_limits": ["l_short_sample", "l_intent"], "valid_mind_changers": ["m_exam_notice", "m_other_text", "m_booking_fake"],
    "invalid_limits": ["l_invalid_secret", "l_invalid_code"],
    "decisive_evidence": ["ev_decoded", "ev_hall_booking", "ev_bakery_order", "ev_exam_schedule", "ev_freq_table"],
    "lab_requirement": None,
    "timeline_requirement": [{"evidence_id": "ev_chat_msgs", "utc_minute": 10, "tol": 20}, {"evidence_id": "ev_book_loan", "utc_minute": 90, "tol": 5}],
    "refuted_hypotheses": ["h_cheat", "h_nonsense"],
    "criteria_map": {"c_source": "source_typing", "c_conflict": "conflict_resolution", "c_links": "hypothesis_links", "c_uncertainty": "uncertainty", "c_revision": "revision", "c_elimination": "elimination", "c_justification": "justification_human"},
    "caps": {"no_citations_max": 45, "no_conflict_resolution_max": 70},
}
os.makedirs(OUT, exist_ok=True)
for suf, obj in [("", core), (".ui", ui), (".scoring", sc)]:
    with open(os.path.join(OUT, f"{CID}{suf}.json"), "w", encoding="utf8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
print("ok")
