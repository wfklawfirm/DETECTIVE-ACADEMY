#!/usr/bin/env python3
# Case c013 «المشط والوشاح» — adapted from heritage seed S-03 (pattern: transferred trace, "the comb and the two velvets"; ARC-04 nothing was stolen + KO-NP-02H-006).
# Teaches: fibres on a cap show CONTACT, not OWNERSHIP (Locard simplified: a trace can be a background trace, and absence does not prove absence of contact);
# when the physical traces fit both claimants, a descriptive record that matches the object (serial number on the purchase receipt = serial on the label) decides.
# No-culprit convention: the volunteer whose innocent tidying put the two scarves together (Layan) is recorded in culprit_ids; nobody did anything wrong.
# All numbers in the fibre lab are ILLUSTRATIVE (fictional spread rule), and the lab says so. Two disjoint proof paths:
#   A = Mazen's receipt + scarf label (serial) + cap fibre counts + fibre-lab result
#   B = departure photo + close-up of the embroidered fringe + bus lost-property log (سلسلة العهدة) + school shop ledger
# Usage: gen_c013.py OUT_DIR
import json, sys, os
OUT = sys.argv[1]
CID = "c013_two_scarves"

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
ch("mazen", "مازن الحلبي", "victim", "14 سنة، طالب في الصف التاسع",
   "هادئ وواثق من وشاحه، لكنه يتحدث ببطء حين يُشكَّك فيه، ويفضّل أن يُري الأوراق على أن يجادل.",
   ["استعادة وشاحه الذي اشتراه مع أمه", "ألا يتحول الأمر إلى خصومة مع زميله"],
   [L("mz_greet", "greeting", "الوشاح الأزرق وشاحي، وأمي تحتفظ بوصل شرائه."),
    L("mz_receipt", "reveal", "اشترينا الوشاح من متجر المدرسة في نوفمبر، ووصل الشراء محفوظ عند أمي.", ["f_mazen_receipt_exists"]),
    L("mz_embroidery", "reveal", "طلبنا عند الشراء أن يُطرَّز حرف الميم بخيط برتقالي عند الهدب.", ["f_mazen_embroidery"]),
    L("mz_unknown", "deflect_unknown", "لا أعرف، لم أنتبه لذلك."),
    L("mz_off", "deflect_offtopic", "رجاءً، لنبقَ في موضوع الوشاحين."),
    L("mz_bye", "farewell", "أريد أن يُحل الأمر دون أن يزعل أحد.")])
ch("yasser", "ياسر العلي", "suspect", "14 سنة، طالب في الصف التاسع",
   "حماسي وسريع الجزم، يتمسك بأول دليل يخطر له، لكنه يعترف بالخطأ حين يرى سجلاً واضحاً.",
   ["استعادة وشاح أزرق ظن أنه له", "أن يُنصف في الخلاف"],
   [L("ys_greet", "greeting", "الوشاح الأزرق لي، ومعي ما يثبت ذلك."),
    L("ys_receipt", "reveal", "عندي وصل شراء لوشاح أزرق صوفي من متجر المدرسة، فهو وشاحي.", None, ["cl_yasser_receipt"]),
    L("ys_receipt_exists", "reveal", "وصل الشراء محفوظ في ملف أمي، وأستطيع أن أريه لك.", ["f_yasser_receipt_exists"]),
    L("ys_fibres", "reveal", "وقبعتي فيها ألياف زرقاء كثيرة، وهذا يثبت أنها لامست وشاحي الأزرق.", None, ["cl_yasser_fibres"]),
    L("ys_green", "reveal", "والوشاح الأخضر القطني عليه اسمي بخط أمي، وأنا أعرف أنه لي أيضاً.", ["f_green_is_yassers"]),
    L("ys_refuse", "refuse_secret", "قلت ما عندي: وصلي وقبعتي."),
    L("ys_realise", "reveal", "انتظر... وصلي يذكر مقاس 150 سم ورقماً تسلسلياً آخر. ربما وشاحي الأزرق ما زال في البيت.", ["f_yasser_realises"]),
    L("ys_unknown", "deflect_unknown", "لا أعرف، ولا أحب أن أخمّن."),
    L("ys_off", "deflect_offtopic", "لنبقَ في موضوع الوشاحين."),
    L("ys_bye", "farewell", "شكراً لأنك تنظر في الأوراق لا في الأصوات العالية.")])
ch("layan", "ليان الخطيب", "suspect", "15 سنة، متطوعة لأمانات الحافلة",
   "مجتهدة وحريصة على أن تنتهي الرحلة بلا فقدان، فتجمع الأغراض بسرعة وتظن أنها لا تغيّر شيئاً.",
   ["ألا يُنسب إليها إهمال في الأمانات", "أن يستعيد كل طالب غرضه"],
   [L("ly_greet", "greeting", "أنا من يجمع الأغراض المنسية في الحافلة، وعندي سجل بذلك."),
    L("ly_collect", "reveal", "جمعت الوشاحين عند الخامسة وخمس دقائق مساء، أحدهما من المقعد التاسع والآخر من المقعد الرابع عشر.", ["f_layan_collect"]),
    L("ly_log", "reveal", "أدوّن في سجل الأمانات كل غرض أجمعه، وتراجعه المعلمة منى.", ["f_bus_log_exists"]),
    L("ly_same", "reveal", "تركت كل وشاح في مكانه كما وجدته، ولم أغيّر شيئاً.", None, ["cl_layan_separate"]),
    L("ly_refuse", "refuse_secret", "لا أذكر شيئاً آخر عن الوشاحين."),
    L("ly_pile", "reveal", "حسناً... وضعتهما معاً على المقعد الرابع عشر بجانب حقيبتي لأحملهما إلى المعلمة، ولم أنتبه إلى أن ذلك قد يربك أصحابهما.", ["f_layan_pile"]),
    L("ly_unknown", "deflect_unknown", "لا أعرف، لم أرَ أكثر من ذلك."),
    L("ly_off", "deflect_offtopic", "أفضّل أن نتكلم عن الأمانات والوشاحين."),
    L("ly_bye", "farewell", "آسفة إن كنت سبّبت التباساً دون قصد.")])
ch("mona", "الأستاذة منى", "authority", "معلمة ومشرفة الرحلة",
   "حازمة وهادئة، تجمع الوثائق والصور وتترك للمحقق أن يستنتج.",
   ["أن تنتهي الرحلة بخلاصة عادلة", "أن تُحفظ سجلات الرحلة"],
   [L("mn_greet", "greeting", "الرحلة موثّقة، وسأعطيك ما عندي من سجلات."),
    L("mn_photo", "reveal", "التقطت صباحاً صورة للطلاب عند صعود الحافلة، وهي محفوظة بوقتها.", ["f_departure_photo_exists"]),
    L("mn_log", "reveal", "سجل أمانات الحافلة تكتبه ليان وأراجعه أنا في نهاية الرحلة.", ["f_bus_log_exists"]),
    L("mn_samples", "reveal", "وافق الطالبان على أخذ عينات لاصقة من قبعتيهما، ووافقت ليان على عينة من حقيبتها.", ["f_samples_allowed"]),
    L("mn_unknown", "deflect_unknown", "هذا ليس عندي."),
    L("mn_off", "deflect_offtopic", "لنبقَ في موضوع الرحلة والوشاحين."),
    L("mn_bye", "farewell", "أريد أن يتعلم الطلاب كيف يُحسم الخلاف بالسجلات.")])
ch("karim", "كريم الصباغ", "expert", "موظف متجر المدرسة",
   "منظم وواضح، يشرح طريقة تسجيل المبيعات ولا يحكم في ملكية أحد.",
   ["أن يُفهم كيف تُسجَّل مبيعات المتجر"],
   [L("kr_greet", "greeting", "أستطيع أن أشرح كيف نسجّل مبيعاتنا، ولا أحكم في خلاف بين طالبين."),
    L("kr_serial", "reveal", "لكل وشاح صوفي مدرسي بطاقة برقم تسلسلي فريد، ونكتب الرقم نفسه في وصل الشراء.", ["f_shop_serial"]),
    L("kr_ledger", "reveal", "ونحتفظ بسجل يعدّ المبيعات حسب اللون والدفعة والطول.", ["f_shop_ledger_exists"]),
    L("kr_unknown", "deflect_unknown", "ليس في سجلي."),
    L("kr_off", "deflect_offtopic", "اسألني عن المتجر ومبيعاته."),
    L("kr_bye", "farewell", "تفضّل بزيارتنا متى شئت.")])

locations = [{"id": "loc_school", "name_ar": "ساحة المدرسة", "description_ar": "حيث صعد الطلاب إلى الحافلة صباحاً."},
             {"id": "loc_bus", "name_ar": "حافلة رحلة الأطلال", "description_ar": "الحافلة التي عادت بعد الظهر."},
             {"id": "loc_lab", "name_ar": "مختبر المنظار", "description_ar": "مختبر خيالي لفحص العينات المجهرية."},
             {"id": "loc_shop", "name_ar": "متجر المدرسة", "description_ar": "حيث تُباع الأوشحة وتُسجَّل مبيعاتها."}]
objects = [{"id": "obj_blue", "name_ar": "الوشاح الأزرق الصوفي", "description_ar": "وشاح صوفي أزرق وُجد على المقعد الرابع عشر."},
           {"id": "obj_green", "name_ar": "الوشاح الأخضر القطني", "description_ar": "وشاح قطني أخضر وُجد بجانب الأزرق."}]
orgs = [{"id": "org_school", "name_ar": "مدرسة الأطلال", "description_ar": "مدرسة خيالية نظمت رحلة إلى موقع الأطلال."}]

# ---------------------------------------------------------------- facts
facts = []
def F(id, st, kind, subj, spoiler, time=None, loc=None, ko=None):
    d = {"id": id, "statement_ar": st, "kind": kind, "subject_ids": subj, "spoiler_level": spoiler}
    if time: d["time"] = time
    if loc: d["location_id"] = loc
    if ko: d["science_ko_refs"] = ko
    facts.append(d)
F("f_dispute", "بعد رحلة الأطلال يتنازع مازن وياسر وشاحين تُركا على مقعد في الحافلة، وكل منهما يقول إن الأزرق الصوفي له.", "event", ["mazen", "yasser", "obj_blue", "obj_green"], 0)
F("f_two_scarves", "الوشاحان متشابهان من بعيد: أزرق صوفي وأخضر قطني.", "state", ["obj_blue", "obj_green"], 0)
F("f_fibres_claim", "يقول ياسر إن الألياف الزرقاء الكثيرة على قبعته تثبت أن الوشاح الأزرق له.", "attribute", ["yasser"], 0)
F("f_departure_photo_exists", "التقطت المعلمة منى صورة للطلاب عند صعود الحافلة صباحاً.", "state", ["mona", "loc_school"], 1)
F("f_bus_log_exists", "لحافلة الرحلة سجل أمانات تدوّن فيه ليان ما تجمعه وتراجعه المعلمة.", "state", ["layan", "mona", "loc_bus"], 1)
F("f_samples_allowed", "وافق الطالبان وليان على أخذ عينات لاصقة من قبعتيهما وحقيبتها لفحصها.", "state", ["mona"], 1)
F("f_layan_collect", "جمعت ليان الوشاحين عند 17:05، الأزرق من المقعد 9 والأخضر من المقعد 14.", "event", ["layan", "obj_blue", "obj_green"], 1, T(605), "loc_bus")
F("f_layan_pile", "وضعت ليان الوشاحين معاً على المقعد 14 بجانب حقيبتها قبل حضور الطالبين.", "event", ["layan", "obj_blue", "obj_green"], 2, T(606, "approx", 620), "loc_bus")
F("f_mazen_receipt_exists", "لدى أم مازن وصل شراء وشاحه من متجر المدرسة.", "state", ["mazen"], 1)
F("f_mazen_embroidery", "طُرّز حرف «م» بخيط برتقالي عند هدب وشاح مازن عند الشراء.", "attribute", ["mazen", "obj_blue"], 1)
F("f_yasser_receipt_exists", "لدى أم ياسر وصل شراء وشاح أزرق صوفي لياسر.", "state", ["yasser"], 1)
F("f_green_is_yassers", "بطاقة الوشاح الأخضر القطني مكتوب عليها اسم ياسر بخط أمه.", "attribute", ["yasser", "obj_green"], 1)
F("f_yasser_realises", "أدرك ياسر أن وصله لوشاح أزرق آخر بمقاس ورقم مختلفين.", "event", ["yasser"], 2)
F("f_shop_serial", "لكل وشاح صوفي مدرسي بطاقة برقم تسلسلي فريد يُدوَّن في وصل الشراء.", "state", ["loc_shop"], 1)
F("f_shop_ledger_exists", "للمتجر سجل مبيعات يعدّ الأوشحة حسب اللون والدفعة والطول.", "state", ["loc_shop"], 1)
F("f_fibres_traveled", "وُجدت ألياف زرقاء صوفية على القبعتين والمقعد وحقيبة ليان، وهذه الأخيرة لا تخص صاحب وشاح.", "relation", ["obj_blue"], 2, None, "loc_bus", ["KO-NP-02H-006"])
F("f_yasser_receipt_other", "وصل ياسر يخص وشاحاً أزرق آخر: الطول 150 سم، والدفعة B5، ورقم تسلسلي غير رقم الوشاح الموجود.", "relation", ["yasser", "obj_blue"], 2)
F("f_blue_is_mazens", "الوشاح الأزرق الصوفي المحفوظ ملك مازن: رقمه التسلسلي في وصله، وحرفه المطرّز على هدبه، وصورة الصباح.", "relation", ["mazen", "obj_blue"], 3, None, None, ["KO-RS-06-001"])
F("f_fibres_not_discriminating", "أعداد الألياف على القبعتين تتفق مع أي من الطالبين، فهي تدل على ملامسة لا على ملكية.", "relation", ["obj_blue", "yasser", "mazen"], 3, None, None, ["KO-FC-04-018", "KO-FC-04-011"])

claims = [
    {"id": "cl_yasser_fibres", "statement_ar": "الألياف الزرقاء الكثيرة على قبعتي تثبت أن الوشاح الأزرق لي.", "kind": "honest_mistake", "held_by": ["yasser"], "true_fact_id": "f_fibres_not_discriminating", "contradicted_by_evidence_ids": ["ev_fibre_lab", "ev_shop_count", "ev_bus_log"]},
    {"id": "cl_yasser_receipt", "statement_ar": "وصل الشراء الذي معي لوشاح أزرق، فالوشاح الأزرق هذا وشاحي.", "kind": "honest_mistake", "held_by": ["yasser"], "true_fact_id": "f_yasser_receipt_other", "contradicted_by_evidence_ids": ["ev_yasser_receipt", "ev_scarf_tag"]},
    {"id": "cl_layan_separate", "statement_ar": "تركت كل وشاح في مكانه كما وجدته.", "kind": "honest_mistake", "held_by": ["layan"], "true_fact_id": "f_layan_pile", "contradicted_by_evidence_ids": ["ev_bus_log"]},
]
timeline = [
    {"id": "te_depart", "description_ar": "مازن وياسر يصعدان إلى الحافلة ومعهما وشاحاهما.", "time": T(42), "location_id": "loc_school", "actor_ids": ["mazen", "yasser"], "fact_ids": ["f_departure_photo_exists", "f_green_is_yassers"], "motivated_by_ar": "انطلاق الرحلة المدرسية صباحاً"},
    {"id": "te_collect", "description_ar": "ليان تجمع الوشاحين من المقعدين 9 و14.", "time": T(605), "location_id": "loc_bus", "actor_ids": ["layan"], "fact_ids": ["f_layan_collect"], "motivated_by_ar": "مهمتها جمع الأغراض المنسية قبل نزول الطلاب"},
    {"id": "te_pile", "description_ar": "ليان تضع الوشاحين معاً على المقعد 14 بجانب حقيبتها.", "time": T(606, "approx", 619), "location_id": "loc_bus", "actor_ids": ["layan"], "fact_ids": ["f_layan_pile"], "motivated_by_ar": "أرادت حملهما معاً إلى المعلمة"},
    {"id": "te_arrive", "description_ar": "مازن وياسر يعودان إلى الحافلة ويجدان الوشاحين معاً.", "time": T(620), "location_id": "loc_bus", "actor_ids": ["mazen", "yasser"], "fact_ids": ["f_dispute"], "motivated_by_ar": "عادا ليأخذا ما نسياه"},
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
V("ev_cap_fibres", "عينات الألياف من القبعتين", "physical",
  "فحص مجهري لعينات لاصقة أُخذت بموافقة صاحبيها (الأرقام توضيحية للتعلم)\nقبعة ياسر: 14 ليفاً أزرق صوفياً، و5 ألياف خضراء قطنية\nقبعة مازن: 6 ألياف زرقاء صوفية، ولا ألياف خضراء\nعينة لاصقة واحدة لكل قبعة",
  ["a_sample_fibres"], ["f_fibres_traveled"], "moderate",
  "يبيّن وجود الألياف وعددها في عينة واحدة؛ لا يبيّن كيف وصلت ولا متى، وغياب لون لا يثبت غياب التلامس.", red=True, loc="loc_lab")
V("ev_seat_fibres", "عينة الألياف من مسند المقعد 14", "physical",
  "عينة لاصقة من مسند المقعد 14 (الأرقام توضيحية)\n30 ليفاً أزرق صوفياً\n12 ليفاً أخضر قطنياً",
  ["a_sample_fibres"], ["f_fibres_traveled"], "moderate",
  "تدل على أن الوشاحين أو أحدهما مرّ بالمقعد؛ لا تدل على من لمسه ولا على صاحب أي منهما.", loc="loc_bus")
V("ev_bag_fibres", "عينة الألياف من حقيبة ليان", "physical",
  "عينة لاصقة من حقيبة المتطوعة ليان، بموافقتها (الأرقام توضيحية)\n9 ألياف زرقاء صوفية\n4 ألياف خضراء قطنية",
  ["a_sample_fibres"], ["f_fibres_traveled"], "moderate",
  "تدل على تلامس الحقيبة بالوشاحين أو بسطح لامسهما؛ لا تدل على أن الحقيبة تخص صاحب وشاح.", loc="loc_lab")
V("ev_fibre_lab", "تقرير مختبر المنظار عن مدى الألياف", "lab_result",
  "تقرير مختبر المنظار (قاعدة انتشار خيالية، الأرقام توضيحية)\nقبعة لامست وشاحاً صوفياً خمس دقائق: 10–20 ليفاً\nارتداء وشاح صوفي ساعات قرب القبعة: 3–10 ألياف\nنقل ثانوي من مقعد أو يد إلى القبعة: 2–8 ألياف\nقبعة ياسر (14 ليفاً) ضمن مدى الملامسة القصيرة، وقبعة مازن (6 ألياف) ضمن مدى الارتداء ومدى النقل الثانوي. المدى متداخل.",
  ["a_request_fibre_lab"], ["f_fibres_not_discriminating"], "strong",
  "أرقامه توضيحية لغرض التعلم لا قياس حقيقي؛ ويبيّن ما يتسق مع ماذا لا من الفاعل، وغياب الألياف لا يثبت غياب التلامس ووجودها لا يثبت الملكية.", contradicts=["cl_yasser_fibres"], ko="KO-FC-04-018", loc="loc_lab")
V("ev_mazen_receipt", "وصل شراء وشاح مازن", "documentary",
  "وصل شراء — متجر المدرسة\nالتاريخ: 03/11\nالصنف: وشاح صوف أزرق — الطول 180 سم — الدفعة B7 — الرقم التسلسلي S-0187\nخدمة إضافية: تطريز حرف «م» بخيط برتقالي عند الهدب\nالمشتري: ولي أمر الطالب مازن الحلبي (بطاقة الطالب 2315)",
  ["a_get_receipts"], ["f_mazen_receipt_exists", "f_mazen_embroidery"], "strong",
  "يثبت شراء وشاح بهذه المواصفات والرقم؛ لا يثبت أن المشتري أو ابنه ما زال صاحبه ولا أنه هو من تركه على المقعد.", loc="loc_shop")
V("ev_yasser_receipt", "وصل شراء وشاح ياسر", "documentary",
  "وصل شراء — متجر المدرسة\nالتاريخ: 04/10\nالصنف: وشاح صوف أزرق — الطول 150 سم — الدفعة B5 — الرقم التسلسلي S-0121\nالمشتري: ولي أمر الطالب ياسر العلي (بطاقة الطالب 2290)",
  ["a_get_receipts"], ["f_yasser_receipt_exists"], "strong",
  "يثبت شراء وشاح أزرق آخر؛ وصل لوشاح أزرق ليس وصلاً لهذا الوشاح بعينه ما لم تتطابق المواصفات والرقم.", red=True, loc="loc_shop")
V("ev_scarf_tag", "بطاقة الوشاح الأزرق المحفوظ", "physical",
  "صورة بطاقة الوشاح الأزرق المحفوظ عند أمانة الحافلة\nصوف 100%\nالطول: 180 سم\nالدفعة: B7\nالرقم التسلسلي: S-0187",
  ["a_photo_tag"], ["f_blue_is_mazens"], "strong",
  "تعرّف الوشاح بنموذجه ودفعته ورقمه؛ يتطابق الرقم مع وصل واحد في سجل المتجر، لكن البطاقة وحدها لا تبيّن من يملكه الآن.", contradicts=["cl_yasser_receipt"], loc="loc_bus")
V("ev_scarf_patch", "صورة مقربة لهدب الوشاح الأزرق", "physical",
  "صورة مقربة لهدب الوشاح الأزرق المحفوظ: حرف «م» مطرّز بخيط برتقالي، حجمه نحو 3 سم.",
  ["a_photo_fringe"], ["f_blue_is_mazens", "f_mazen_embroidery"], "strong",
  "حرف مطرّز علامة مميِّزة لكنها ليست فريدة بالضرورة؛ فقد يطلب غير مازن حرفاً مماثلاً.", loc="loc_bus")
V("ev_departure_photo", "صورة صعود الحافلة صباحاً", "digital",
  "صورة التقطتها المعلمة منى عند صعود الحافلة (بياناتها الوصفية: 07:42)\nيظهر مازن بوشاح أزرق صوفي على هدبه علامة برتقالية صغيرة، ويظهر ياسر بوشاح أخضر قطني.",
  ["a_get_departure_photo"], ["f_green_is_yassers", "f_blue_is_mazens"], "strong",
  "صورة صغيرة الحجم تعرض اللون والعلامة؛ لا تقرأ الأرقام التسلسلية ولا تبيّن من خلع وشاحه لاحقاً.", loc="loc_school")
V("ev_bus_log", "سجل أمانات الحافلة", "documentary",
  "سجل أمانات الحافلة (توقيع ليان الخطيب، ومراجعة الأستاذة منى)\n17:05 — مقعد 9: وشاح أزرق صوفي — جُمع إلى الأمانات\n17:05 — مقعد 14: وشاح أخضر قطني — جُمع إلى الأمانات\n17:20 — عند حضور الطالبين: الوشاحان معاً على المقعد 14\nملاحظة: الجلوس كان حراً في هذه الرحلة ولا تخصيص للمقاعد.",
  ["a_get_bus_log"], ["f_layan_collect", "f_layan_pile"], "strong",
  "سجل عهدة للأغراض المنسية؛ يبيّن موضع كل غرض ووقته، لا يبيّن من جلس في أي مقعد ولا لمن الغرض.", contradicts=["cl_layan_separate", "cl_yasser_fibres"], ko="KO-FC-04B-002", loc="loc_bus")
V("ev_shop_count", "سجل مبيعات متجر المدرسة", "documentary",
  "سجل مبيعات متجر المدرسة — الموسم الحالي\nأوشحة صوفية زرقاء مباعة: 31\n  الدفعة B7، الطول 180 سم: 9\n  الدفعة B5، الطول 150 سم: 22\nأوشحة قطنية خضراء مباعة: 14\nلكل وشاح صوفي بطاقة برقم تسلسلي فريد يُدوَّن في الوصل.",
  ["a_get_shop_ledger"], ["f_shop_serial", "f_shop_ledger_exists"], "strong",
  "يعدّ مبيعات المتجر المدرسي فقط ولا يشمل أوشحة اشتُريت من خارجه؛ ويبيّن كثرة الأوشحة المتشابهة لا صاحب أحدها.", contradicts=["cl_yasser_fibres"], ko="KO-FC-04-011", loc="loc_shop")
V("ev_green_label", "بطاقة الوشاح الأخضر القطني", "physical",
  "صورة البطاقة الداخلية للوشاح القطني الأخضر: «ياسر ع.» بخط يدوي.",
  ["a_photo_green"], ["f_green_is_yassers"], "moderate",
  "خط اليد يدل على من وسم الوشاح لا على من يملكه الآن؛ ولا علاقة له بالوشاح الأزرق.", loc="loc_bus")
V("ev_mazen_statement", "إفادة مازن (ملخص)", "testimonial",
  "ملخص إفادة مازن الحلبي:\n«وشاحي الأزرق اشتريته مع أمي في نوفمبر، وطلبنا تطريز حرف الميم عند الهدب. خلعته قرب النافذة ونسيته.»",
  ["a_note_mazen"], ["f_mazen_receipt_exists", "f_mazen_embroidery"], "weak",
  "إفادة صاحب مصلحة؛ يؤيدها الوصل والصورة ولا تغني عنهما.", loc="loc_bus")
V("ev_yasser_statement", "إفادة ياسر (ملخص)", "testimonial",
  "ملخص إفادة ياسر العلي:\n«عندي وصل لوشاح أزرق صوفي، وقبعتي فيها ألياف زرقاء أكثر من قبعة مازن، فالأزرق لي.»",
  ["a_note_yasser"], ["f_yasser_receipt_exists"], "weak",
  "إفادة صاحب مصلحة تجمع دليلين لا يميّزان بين الطالبين؛ وتُقاس بالبطاقة الفعلية وبمدى الألياف.", loc="loc_bus")
V("ev_layan_statement", "إفادة ليان (ملخص)", "testimonial",
  "ملخص إفادة ليان الخطيب:\n«جمعت الوشاحين عند الخامسة وخمس دقائق، وتركت كل وشاح في مكانه كما وجدته.»",
  ["a_note_layan"], ["f_layan_collect"], "weak",
  "تصف ما ظنت أنها فعلته؛ ويُقاس قولها «تركته في مكانه» بسجل الأمانات.", loc="loc_bus")

# ---------------------------------------------------------------- inferences
def P(t, i): return {"ref_type": t, "ref_id": i}
inf = []
def I(id, prem, ct, concl, rel, strength, rule, ks):
    inf.append({"id": id, "premises": prem, "conclusion": {"ref_type": ct, "ref_id": concl}, "relation": rel, "strength": strength, "rule_ar": rule, "skill_ko_refs": ks})
# K1 f_blue_is_mazens
I("i_a_owner", [P("evidence", "ev_mazen_receipt"), P("evidence", "ev_scarf_tag")], "fact", "f_blue_is_mazens", "establishes", "strong",
  "الرقم التسلسلي والطول والدفعة على بطاقة الوشاح الأزرق تطابق ما في وصل مازن؛ والرقم فريد لوشاح واحد في سجل المتجر.", ["KO-RS-06-001", "KO-NP-02H-006"])
I("i_b_owner", [P("evidence", "ev_departure_photo"), P("evidence", "ev_scarf_patch")], "fact", "f_blue_is_mazens", "establishes", "strong",
  "صورة الصباح تضع على وشاح مازن علامة برتقالية عند الهدب، والوشاح الأزرق المحفوظ عليه حرف مطرّز بالخيط نفسه في الموضع نفسه.", ["KO-RS-06-001", "KO-RS-06-004"])
# K2 f_fibres_not_discriminating
I("i_a_fibres", [P("evidence", "ev_cap_fibres"), P("evidence", "ev_fibre_lab")], "fact", "f_fibres_not_discriminating", "establishes", "strong",
  "عدد الألياف على كل قبعة يقع ضمن مدى تفسير بريء مختلف (ملامسة قصيرة أو ارتداء أو نقل ثانوي)، والمدى يتداخل؛ فالعدد لا يفرّق بين الطالبين.", ["KO-FC-04-018", "KO-RS-06-015"])
I("i_b_fibres", [P("evidence", "ev_bus_log"), P("evidence", "ev_shop_count")], "fact", "f_fibres_not_discriminating", "establishes", "strong",
  "الوشاحان اجتمعا على مقعد واحد قبل حضور الطالبين، وفي المدرسة تسعة أوشحة من النوع نفسه على الأقل؛ فوجود الألياف لا يعيّن صاحبها.", ["KO-FC-04-011", "KO-RS-06-015"])
I("i_transfer", [P("evidence", "ev_seat_fibres"), P("evidence", "ev_bag_fibres"), P("evidence", "ev_cap_fibres")], "fact", "f_fibres_traveled", "establishes", "suggestive",
  "ألياف الوشاح موجودة على مقعد وحقيبة لا يملكان وشاحاً، إذن تنتقل الألياف بالتلامس غير المباشر فلا تدل على الملكية.", ["KO-NP-02H-006"])
I("i_mismatch", [P("evidence", "ev_yasser_receipt"), P("evidence", "ev_scarf_tag")], "fact", "f_yasser_receipt_other", "establishes", "strong",
  "وصل ياسر يذكر 150 سم والدفعة B5 والرقم S-0121، وبطاقة الوشاح الموجود تذكر 180 سم والدفعة B7 والرقم S-0187؛ فهما وشاحان مختلفان.", ["KO-RS-06-001"])
I("i_layan_mixed", [P("evidence", "ev_bus_log")], "fact", "f_layan_pile", "establishes", "strong",
  "السجل يضع الوشاحين في مقعدين مختلفين عند الجمع ثم معاً على المقعد 14 عند الحضور؛ فلا بد أن أحداً نقل أحدهما.", ["KO-FC-04B-002", "KO-RS-06-017"])
# claims
I("i_yasser_fibre_claim", [P("fact", "f_fibres_not_discriminating")], "claim", "cl_yasser_fibres", "contradicts_claim", "strong",
  "ما دامت الأعداد تتفق مع الملامسة القصيرة فالكثرة لا تثبت الملكية.", ["KO-RS-06-015", "KO-RS-05-014"])
I("i_yasser_receipt_claim", [P("fact", "f_yasser_receipt_other")], "claim", "cl_yasser_receipt", "contradicts_claim", "strong",
  "وصله مطابق لوشاح آخر؛ والمطابقة تُطلب في الرقم والمواصفات لا في اللون وحده.", ["KO-RS-05-014"])
I("i_layan_claim", [P("fact", "f_layan_pile")], "claim", "cl_layan_separate", "contradicts_claim", "strong",
  "قولها إنها تركت كل وشاح في مكانه يخالف أن الوشاحين وُجدا معاً على مقعد واحد.", ["KO-RS-05-014"])
# hypotheses
I("i_support_mazen", [P("fact", "f_blue_is_mazens"), P("fact", "f_fibres_not_discriminating")], "hypothesis", "h_mazen", "supports", "strong",
  "وصل مطابق ببيانات فريدة، وألياف لا تفرّق بين الطالبين؛ فتفسير الملكية هو الوحيد المتسق مع السجلات كلها.", ["KO-RS-06-006"])
I("i_rule_yasser", [P("fact", "f_blue_is_mazens")], "hypothesis", "h_yasser", "rules_out", "conclusive",
  "إذا كان الوشاح الأزرق ملكاً لمازن بمطابقة وصف فريد، فلا يكون ملكاً لياسر.", ["KO-RS-06-008"])
I("i_rule_yasser_fibres", [P("fact", "f_fibres_not_discriminating"), P("fact", "f_yasser_receipt_other")], "hypothesis", "h_yasser", "rules_out", "strong",
  "الألياف تتفق مع ملامسة قصيرة، ووصله لا يطابق الوشاح؛ فلا يبقى لدعواه سند.", ["KO-RS-06-001"])
I("i_rule_undecided", [P("fact", "f_blue_is_mazens")], "hypothesis", "h_undecided", "rules_out", "strong",
  "الأدلة تتسق بالألياف مع الطالبين، لكن الرقم التسلسلي والعلامة المطرزة يحسمان الملكية؛ فالقول بأن الحسم مستحيل غير صحيح.", ["KO-RS-06-008"])

# ---------------------------------------------------------------- character knowledge
K = lambda f, a="witnessed", c="certain": {"fact_id": f, "access": a, "certainty": c}
ck = [
    {"character_id": "mazen", "knows": [K("f_mazen_receipt_exists"), K("f_mazen_embroidery")], "hides": [], "believes": []},
    {"character_id": "yasser", "knows": [K("f_yasser_receipt_exists"), K("f_green_is_yassers")],
     "hides": [{"fact_id": "f_yasser_realises", "reveal_when": {"presented": {"evidence_id": "ev_scarf_tag", "to_character": "yasser"}}, "cover_claim_id": "cl_yasser_receipt", "reveal_line_id": "ys_realise"}],
     "believes": [{"claim_id": "cl_yasser_receipt", "stance": "sincere"}, {"claim_id": "cl_yasser_fibres", "stance": "sincere"}]},
    {"character_id": "layan", "knows": [K("f_layan_collect"), K("f_bus_log_exists")],
     "hides": [{"fact_id": "f_layan_pile", "reveal_when": {"presented": {"evidence_id": "ev_bus_log", "to_character": "layan"}}, "cover_claim_id": "cl_layan_separate", "reveal_line_id": "ly_pile"}],
     "believes": [{"claim_id": "cl_layan_separate", "stance": "sincere"}]},
    {"character_id": "mona", "knows": [K("f_departure_photo_exists", "professional"), K("f_bus_log_exists", "professional"), K("f_samples_allowed", "professional")], "hides": [], "believes": []},
    {"character_id": "karim", "knows": [K("f_shop_serial", "professional"), K("f_shop_ledger_exists", "professional")], "hides": [], "believes": []},
]
hyps = [
    {"id": "h_yasser", "statement_ar": "الوشاح الأزرق ملك ياسر، وكثرة الألياف على قبعته ووصله دليلان على ذلك.", "is_true": False, "plausibility_at_start": "high", "suspect_id": "yasser"},
    {"id": "h_undecided", "statement_ar": "الأدلة تتسق مع الطالبين معاً، فلا سبيل إلى معرفة صاحب الوشاح الأزرق.", "is_true": False, "plausibility_at_start": "medium"},
    {"id": "h_mazen", "statement_ar": "الوشاح الأزرق ملك مازن، وقد التبس الأمر لأن الوشاحين جُمعا ووُضعا معاً دون قصد.", "is_true": True, "plausibility_at_start": "low", "suspect_id": "layan"},
]
mis = [
    {"id": "rh_fibres", "points_to_hypothesis_id": "h_yasser", "planted_via_ar": "قبعة ياسر عليها ألياف زرقاء أكثر من ضعف ما على قبعة مازن.",
     "evidence_ids": ["ev_cap_fibres"], "refuted_by_inference_ids": ["i_rule_yasser", "i_rule_yasser_fibres", "i_yasser_fibre_claim"],
     "fairness_note_ar": "تقرير المختبر يبيّن أن العددين يقعان ضمن تفسيرات بريئة متداخلة، وسجل الأمانات يبيّن أن الوشاحين اجتمعا على مقعد واحد، وسجل المتجر يبيّن كثرة الأوشحة المماثلة؛ وتنبيه «الأرقام توضيحية» ظاهر في الدليل."},
    {"id": "rh_receipt", "points_to_hypothesis_id": "h_undecided", "planted_via_ar": "لكل من الطالبين وصل شراء لوشاح أزرق صوفي، فيبدو أن الأوراق لا تحسم.",
     "evidence_ids": ["ev_yasser_receipt"], "refuted_by_inference_ids": ["i_rule_undecided", "i_mismatch", "i_yasser_receipt_claim"],
     "fairness_note_ar": "الوصلان يختلفان في الطول والدفعة والرقم التسلسلي، والبطاقة الفعلية للوشاح متاحة للمقارنة ولا تطابق إلا وصلاً واحداً."},
]
los = [
    {"id": "lo_corr", "statement_ar": "يفرّق بين الارتباط والسببية: وجود الأثر على شيء يدل على ملامسة لا على ملكية، ويطلب آلية الانتقال.", "skill_ko_ref": "KO-RS-06-015", "observable_behaviors_ar": ["لا يعدّ كثرة الألياف دليل ملكية", "يسأل كيف وصلت الألياف"], "evidence_sources": ["evidence_board", "hypothesis_ledger"]},
    {"id": "lo_diag", "statement_ar": "يقدّر القوة التشخيصية للدليل ويفضّل ما يحمل بيانات مميِّزة (رقم تسلسلي) على ما يشترك فيه كثيرون (اللون والنوع).", "skill_ko_ref": "KO-RS-06-001", "observable_behaviors_ar": ["يربط الدليل بالفرضية باتجاه صحيح", "يقارن الوصل بالبطاقة الفعلية"], "evidence_sources": ["evidence_board", "final_justification"]},
    {"id": "lo_obs", "statement_ar": "يفصل بين الملاحظة والاستنتاج في أعداد الألياف وفي أقوال الطالبين.", "skill_ko_ref": "KO-RS-06-004", "observable_behaviors_ar": ["يصنّف الإفادات أقوالاً", "يميّز العدّ من التفسير"], "evidence_sources": ["evidence_board"]},
    {"id": "lo_hyp", "statement_ar": "يوازن بين فرضيتين على الأقل ويستبعد ما تنقضه الأدلة.", "skill_ko_ref": "KO-RS-05-002", "observable_behaviors_ar": ["يضيف فرضيات", "يستبعد بدليل"], "evidence_sources": ["hypothesis_ledger"]},
    {"id": "lo_calib", "statement_ar": "يصوغ نسبة الترجيح بحدودها.", "skill_ko_ref": "KO-RS-06-021", "observable_behaviors_ar": ["يختار ثقة معقولة", "يذكر حدوداً"], "evidence_sources": ["final_justification"]},
    {"id": "lo_revise", "statement_ar": "يراجع رأيه الأول حين يظهر ما يخالفه.", "skill_ko_ref": "KO-RS-06-009", "observable_behaviors_ar": ["يغيّر فرضيته الرائدة بدليل"], "evidence_sources": ["hypothesis_ledger"]},
]
def levels(d): return [{"score": i, "descriptor_ar": t} for i, t in enumerate(d)]
rub = {
    "reference_answer_ar": "الوشاح الأزرق الصوفي ملك مازن. رقمه التسلسلي S-0187 وطوله ودفعته تطابق وصل مازن، وعند هدبه علامة الميم البرتقالية نفسها التي تظهر في صورة الصباح، أما وصل ياسر فلوشاح آخر بمقاس ورقم مختلفين. وكثرة الألياف على قبعة ياسر لا تثبت ملكيته: عدداها على القبعتين يتفقان مع ملامسة قصيرة أو ارتداء أو نقل ثانوي، والوشاحان اجتمعا على مقعد واحد حين جمعتهما ليان دون قصد. حدود الاستنتاج: الوصل يثبت الشراء لا أن الوشاح بقي عند صاحبه، أرقام المختبر توضيحية، ولا تنفي الأدلة أن يكون لياسر وشاح أزرق آخر في بيته.",
    "criteria": [
        {"id": "c_source", "name_ar": "تصنيف المصادر", "objective_ids": ["lo_obs"], "scored_by": "deterministic", "weight": 0.15, "levels": levels(["لم يصنّف", "أخطأ في الأغلب", "نصف صحيح", "معظمه صحيح", "كله صحيح"])},
        {"id": "c_conflict", "name_ar": "ترتيب الأحداث على الخط الزمني", "objective_ids": ["lo_corr"], "scored_by": "deterministic", "weight": 0.15, "levels": levels(["لم يضع شيئاً", "وضع قليلاً", "وضع نصفها صحيحاً", "معظمها", "كلها في موضعها"])},
        {"id": "c_links", "name_ar": "ربط الأدلة بالفرضيات", "objective_ids": ["lo_diag", "lo_corr"], "scored_by": "deterministic", "weight": 0.25, "levels": levels(["لا روابط", "قليلة", "نصفها صحيح", "معظمها", "كلها دقيقة"])},
        {"id": "c_uncertainty", "name_ar": "معايرة الثقة", "objective_ids": ["lo_calib"], "scored_by": "deterministic", "weight": 0.15, "levels": levels(["ثقة مفرطة", "حدود قليلة", "جزئية", "معقولة", "معايَرة كاملة"])},
        {"id": "c_revision", "name_ar": "مراجعة الرأي", "objective_ids": ["lo_revise"], "scored_by": "deterministic", "weight": 0.1, "levels": levels(["بقي على فرضية مرفوضة", "لم يعلن فرضية", "ثبت على فرضية سليمة", "غيّر بدليل", "غيّر بدليل ووثّق"])},
        {"id": "c_elimination", "name_ar": "استبعاد الفرضيات الخاطئة", "objective_ids": ["lo_hyp"], "scored_by": "deterministic", "weight": 0.1, "levels": levels(["لم يستبعد", "استبعد خطأً", "فرضية بدليل", "فرضيتين", "كل الخاطئة"])},
        {"id": "c_justification", "name_ar": "جودة الحجة المكتوبة", "objective_ids": ["lo_diag", "lo_hyp", "lo_obs"], "scored_by": "human", "weight": 0.1, "levels": levels(["لا حجة", "ادعاء بلا سند", "أدلة دون ربط", "ربط الأدلة بالاستنتاج", "ربط مع البدائل والحدود"])},
    ],
}
def H(id, lv, kind, text, trig, target=None, w=0.0):
    d = {"id": id, "level": lv, "kind": kind, "text_ar": text, "trigger": trig, "assessment_weight": w}
    if target: d["targets_inference_id"] = target
    return d
he = lambda e: {"has_evidence": e}
al = {"always": True}
hints = [
    H("hg1", 1, "metacognitive", "حين تجد أثراً على شيء، اسأل: هل يدل على أن صاحب الشيء لامس الأثر، أم أن أي أحد قد يكون لامسه؟", al, None, 0.02),
    H("hg2", 2, "focus_area", "ضع الأدلة في عمودين: ما يتشابه فيه الطالبان، وما يختلف فيه ويميّز أحدهما.", he("ev_cap_fibres"), None, 0.04),
    H("hf1", 1, "metacognitive", "ما الذي يستطيع عدّ الألياف أن يقوله، وما الذي لا يستطيع؟", he("ev_cap_fibres"), "i_a_fibres", 0.02),
    H("hf2", 2, "pointer", "اطلب من مختبر المنظار مقارنة العددين بمدى التلامس الممكن، وقارن المدى بكل قبعة.", he("ev_cap_fibres"), "i_a_fibres", 0.05),
    H("hf3", 3, "partial_reveal", "المدى متداخل: عدد ياسر يناسب ملامسة قصيرة، وعدد مازن يناسب الارتداء أو النقل الثانوي.", he("ev_fibre_lab"), "i_a_fibres", 0.08),
    H("ho1", 1, "metacognitive", "أي معلومة في الوصل تتفرد بوشاح واحد دون سائر الأوشحة الزرقاء؟", he("ev_yasser_receipt"), "i_a_owner", 0.02),
    H("ho2", 2, "pointer", "قارن الطول والدفعة والرقم التسلسلي في كل وصل ببطاقة الوشاح الفعلي.", he("ev_yasser_receipt"), "i_a_owner", 0.05),
    H("hb1", 1, "metacognitive", "من نقل الوشاحين، وأين كان كل منهما حين جُمع؟", he("ev_layan_statement"), "i_layan_mixed", 0.02),
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
Act("a_photo_tag", "examine", "صوّر بطاقة الوشاح الأزرق المحفوظ", al, [G("ev_scarf_tag")], "obj_blue", "PHOTO_TAG")
Act("a_photo_fringe", "examine", "صوّر هدب الوشاح الأزرق عن قرب", al, [G("ev_scarf_patch")], "obj_blue", "PHOTO_FRINGE")
Act("a_photo_green", "examine", "افحص بطاقة الوشاح الأخضر القطني", al, [G("ev_green_label")], "obj_green", "PHOTO_GREEN")
Act("a_get_receipts", "examine", "اطلب نسخ وصلات الشراء من متجر المدرسة", {"all": [fu("f_shop_serial"), {"any": [fu("f_mazen_receipt_exists"), fu("f_yasser_receipt_exists")]}]}, [G("ev_mazen_receipt"), G("ev_yasser_receipt")], "loc_shop", "GET_RECEIPTS")
Act("a_get_shop_ledger", "examine", "اطلب سجل المبيعات من المتجر", fu("f_shop_ledger_exists"), [G("ev_shop_count")], "loc_shop", "GET_SHOP_LEDGER")
Act("a_get_departure_photo", "examine", "اطلب صورة صعود الحافلة من الأستاذة منى", fu("f_departure_photo_exists"), [G("ev_departure_photo")], "loc_school", "GET_DEPARTURE_PHOTO")
Act("a_get_bus_log", "examine", "اطلب سجل أمانات الحافلة", fu("f_bus_log_exists"), [G("ev_bus_log")], "loc_bus", "GET_BUS_LOG")
Act("a_sample_fibres", "examine", "خذ عينات لاصقة (بموافقة أصحابها) من القبعتين والمقعد والحقيبة", fu("f_samples_allowed"), [G("ev_cap_fibres"), G("ev_seat_fibres"), G("ev_bag_fibres")], "loc_lab", "SAMPLE_FIBRES")
Act("a_request_fibre_lab", "request_lab_test", "اطلب من مختبر المنظار مقارنة أعداد الألياف بمدى التلامس الممكن", he("ev_cap_fibres"), [G("ev_fibre_lab")], "loc_lab", "LAB_FIBRES")
for cid, lab in [("mazen", "مازن"), ("yasser", "ياسر"), ("layan", "ليان"), ("mona", "الأستاذة منى"), ("karim", "كريم")]:
    Act(f"a_int_{cid}", "interview", f"ابدأ مقابلة {lab}", al, [{"op": "raise_trust", "ref_id": cid, "amount": 1}], cid, f"INT_{cid.upper()}")
Act("a_note_mazen", "examine", "دوّن إفادة مازن", fu("f_mazen_embroidery"), [G("ev_mazen_statement")], "mazen", "NOTE_MAZEN")
Act("a_note_yasser", "examine", "دوّن إفادة ياسر", fu("f_yasser_receipt_exists"), [G("ev_yasser_statement")], "yasser", "NOTE_YASSER")
Act("a_note_layan", "examine", "دوّن إفادة ليان", fu("f_layan_collect"), [G("ev_layan_statement")], "layan", "NOTE_LAYAN")
Act("p_tag_yasser", "present_evidence", "اعرض بطاقة الوشاح على ياسر", {"presented": {"evidence_id": "ev_scarf_tag", "to_character": "yasser"}}, [{"op": "emit_event", "ref_id": "PRESENTED_TAG"}], "yasser", "P_TAG_YASSER", 0)
Act("p_log_layan", "present_evidence", "اعرض سجل الأمانات على ليان", {"presented": {"evidence_id": "ev_bus_log", "to_character": "layan"}}, [{"op": "emit_event", "ref_id": "PRESENTED_LOG"}], "layan", "P_LOG_LAYAN", 0)
Act("a_hint", "request_hint", "اطلب تلميحاً", al, [], None, "REQUEST_HINT", 0)
Act("a_accuse", "final_accusation", "قدّم الاستنتاج النهائي", al, [{"op": "emit_event", "ref_id": "SUBMIT"}], None, "FINAL_ACCUSATION", 0)

topics = [
    {"id": "t_mazen", "label_ar": "شراء وشاح مازن", "example_questions_ar": ["كيف اشتريت وشاحك؟", "هل فيه علامة خاصة؟"], "fact_ids": ["f_mazen_receipt_exists", "f_mazen_embroidery"]},
    {"id": "t_yasser", "label_ar": "حجة ياسر", "example_questions_ar": ["لماذا تظن أن الأزرق لك؟", "هل معك وصل؟", "ما شأن الوشاح الأخضر؟"], "fact_ids": ["f_yasser_receipt_exists", "f_green_is_yassers", "f_yasser_realises"], "claim_ids": ["cl_yasser_receipt", "cl_yasser_fibres"]},
    {"id": "t_collect", "label_ar": "جمع الأغراض في الحافلة", "example_questions_ar": ["متى جمعت الوشاحين؟", "أين كان كل منهما؟", "أين وضعتهما؟"], "fact_ids": ["f_layan_collect", "f_bus_log_exists", "f_layan_pile"], "claim_ids": ["cl_layan_separate"]},
    {"id": "t_trip", "label_ar": "سجلات الرحلة", "example_questions_ar": ["هل توجد صورة للصعود؟", "هل أُخذت عينات؟", "هل لدينا سجل للأمانات؟"], "fact_ids": ["f_departure_photo_exists", "f_bus_log_exists", "f_samples_allowed"]},
    {"id": "t_shop", "label_ar": "تسجيل مبيعات المتجر", "example_questions_ar": ["كيف تميّزون الأوشحة؟", "هل لديكم سجل للمبيعات؟"], "fact_ids": ["f_shop_serial", "f_shop_ledger_exists"]},
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
    (1, "بطاقة الوشاح الأزرق تحمل الرقم S-0187 والطول 180 سم والدفعة B7، وهذه المواصفات نفسها في وصل مازن؛ والرقم يخص وشاحاً واحداً في سجل المتجر.", ["ev_scarf_tag", "ev_mazen_receipt"], "i_a_owner"),
    (2, "مسار مستقل يتفق معه: صورة الصباح تضع علامة برتقالية على هدب وشاح مازن، وعلى الوشاح المحفوظ حرف «م» مطرّز بالخيط نفسه.", ["ev_departure_photo", "ev_scarf_patch"], "i_b_owner"),
    (3, "وصل ياسر لوشاح أزرق آخر بمقاس 150 سم ودفعة B5 ورقم مختلف؛ فتشابه اللون لا يعني تطابق الوصل.", ["ev_yasser_receipt", "ev_scarf_tag"], "i_mismatch"),
    (4, "أعداد الألياف على القبعتين تقع ضمن مدى تفسيرات بريئة متداخلة، فلا تفرّق بين الطالبين.", ["ev_cap_fibres", "ev_fibre_lab"], "i_a_fibres"),
    (5, "ومن جهة أخرى: الوشاحان اجتمعا على مقعد واحد قبل حضور الطالبين، وفي المدرسة أوشحة كثيرة من النوع نفسه، فوجود الألياف لا يعيّن صاحبها.", ["ev_bus_log", "ev_shop_count"], "i_b_fibres"),
    (6, "وجود الألياف الزرقاء على المقعد وحقيبة ليان يبيّن أن الألياف تنتقل بالتلامس غير المباشر.", ["ev_seat_fibres", "ev_bag_fibres", "ev_cap_fibres"], "i_transfer"),
    (7, "ليان جمعت الوشاحين من مقعدين ثم وُجدا معاً، فالتبس الأمر دون قصد من أحد.", ["ev_bus_log"], "i_layan_mixed"),
    (8, "إذن الوشاح الأزرق لمازن، والوشاح الأخضر لياسر، ولم يُسرق شيء.", ["ev_scarf_tag", "ev_mazen_receipt", "ev_green_label"], "i_support_mazen"),
]
ending = {
    "steps": [{"order": o, "text_ar": t, "uses_evidence_ids": u, "inference_id": i} for o, t, u, i in steps],
    "alternative_paths_ar": [
        "يمكن بلوغ النتيجة من الوصل والبطاقة وعينات القبعتين وتقرير المختبر وحدها.",
        "ويمكن بلوغها من صورة الصباح وصورة الهدب وسجل الأمانات وسجل المتجر وحدها، دون المختبر؛ والأقوى أن يتفق المساران.",
    ],
    "what_evidence_could_not_show_ar": [
        "الوصل يثبت الشراء لا أن الوشاح بقي عند صاحبه؛ ولو أعاره مازن لغيره لما تغيّر الوصل.",
        "أرقام المختبر توضيحية، وغياب الألياف لا يثبت غياب التلامس.",
        "لا تنفي الأدلة أن يكون لياسر وشاح أزرق آخر في بيته.",
    ],
    "science_notes_ar": [
        "الألياف أثر تلامس، وقد تنتقل بالواسطة (مقعد أو يد أو حقيبة) فتكون خلفية لا دليل ملكية؛ وتبسيط مبدأ لوكار لا يعني أن كل أثر يدل على صاحب الشيء.",
        "عندما تتفق الآثار الفيزيائية مع المتنازعين معاً، يُرجع إلى سجل وصفي يتفرد بالشيء: رقم تسلسلي أو علامة خاصة.",
        "سجل الأمانات يحفظ سلسلة العهدة للأغراض المنسية، ويظهر أن نقل شيء بحسن نية قد يغيّر السياق الذي يقرأ به الناس الآثار.",
        "تُختم القضية بمساءلة مؤسسية لا بتشهير: تضع المدرسة قاعدة بألا تُجمع الأغراض المنسية على مقعد واحد، وتكتب موضع كل غرض، وتعتذر ليان وياسر لبعضهما.",
        "ما نسميه نسبة الترجيح حكم مبني على سجلات يمكن تتبّعها، لا على كثرة الآثار.",
    ],
}
core = {
    "schema_version": "0.1.0", "case_id": CID, "case_version": "0.1.0",
    "meta": {"title_ar": "المشط والوشاح", "title_en": "The Comb and the Scarf", "age_band": "13-15", "locale": "ar", "dialogue_register": "msa", "estimated_minutes": 30, "difficulty": 2,
             "content_flags": ["no_violence", "science_lab"], "authors": ["فريق أثر التحريري (مسودة بمساعدة الذكاء الاصطناعي، عن بذرة من قضايا التراث، لم تُراجَع بشرياً بعد)"],
             "knowledge_object_refs": ["KO-RS-06-001", "KO-RS-06-015", "KO-RS-06-004", "KO-RS-05-002", "KO-RS-06-009", "KO-RS-06-021", "KO-FC-04-018", "KO-FC-04-011", "KO-FC-04B-002", "KO-NP-02H-006"]},
    "premise": {"hook_ar": "وشاحان متشابهان على مقعد واحد، وطالبان يقول كل منهما إن الأزرق له. وعلى القبعتين خيوط صغيرة لا تقول من صاحبها.",
                "player_role_ar": "أنت مراجع في لجنة الأمانات المدرسية، وطُلب منك أن تحسم لمن الوشاح الأزرق بالأدلة لا بأعلى الصوتين.",
                "setting_ar": "مدرسة الأطلال، مساء يوم رحلة مدرسية إلى موقع الأطلال. كل الأوقات بتوقيت المدرسة.",
                "public_fact_ids": ["f_dispute", "f_two_scarves", "f_fibres_claim"],
                "assumed_general_knowledge_ar": ["الألياف تنتقل بالتلامس المباشر وغير المباشر", "غياب الأثر لا يثبت غياب التلامس"]},
    "entities": {"characters": chars, "locations": locations, "objects": objects, "organizations": orgs},
    "truth": {"solution": {"culprit_ids": ["layan"], "summary_ar": "لم يسرق أحد شيئاً. الوشاح الأزرق ملك مازن بحسب رقمه ومواصفاته وعلامته المطرزة، والوشاح الأخضر ملك ياسر. التبس الأمر لأن متطوعة الأمانات جمعت الوشاحين من مقعدين ووضعتهما معاً بحسن نية، فانتقلت الألياف بينهما وإلى ما حولهما، وصارت كثرتها على قبعة لا تدل على صاحبها.", "key_fact_ids": ["f_blue_is_mazens", "f_fibres_not_discriminating"]},
              "facts": facts, "claims": claims},
    "timeline": timeline, "evidence": ev, "evidence_graph": {"inferences": inf},
    "character_knowledge": ck, "hypotheses": hyps, "misdirection_plan": mis, "learning_objectives": los,
    "mechanics": {"time_budget_units": 40, "actions": A},
    "state_machine": {"id": "c013", "initial": "briefing", "type": "compound", "states": {
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
    "cover": {"title_ar": "المشط والوشاح", "tagline_ar": "وشاحان، وطالبان، وخيوط صغيرة لا تعرف لمن هي", "kicker_ar": "الملف الثالث عشر · الأثر المنتقل", "glyph": "◈", "accent": "rose"},
    "cold_open_ar": ["الأحد، مساء رحلة الأطلال.", "عادت الحافلة إلى المدرسة، وعلى المقعد الرابع عشر وشاحان: أزرق صوفي وأخضر قطني.",
                     "مازن وياسر يقول كل منهما إن الأزرق له، وفي ملفك عينات من قبعتيهما ومن المقعد ومن حقيبة ثالثة.",
                     "قبل أن تعدّ الألياف، اسأل: ماذا يستطيع هذا العدد أن يقوله فعلاً؟"],
    "labs": [],
    "source_classes": [
        {"id": "primary_record", "label_ar": "سجل أصلي", "help_ar": "يُنتجه نظام أو شخص لحظة الحدث دون وسيط، كوصل شراء أو سجل أمانات أو صورة مؤرخة."},
        {"id": "redisplay", "label_ar": "نسخة معروضة", "help_ar": "معلومة نُقلت من سجل آخر أو أُعيد عرضها."},
        {"id": "claim", "label_ar": "قول أو تصريح", "help_ar": "إفادة شخص؛ تُقاس بالسجلات لا بنبرة صاحبها."},
        {"id": "template", "label_ar": "قالب أو نموذج", "help_ar": "نص جاهز لا يصف الحدث الفعلي بذاته."},
        {"id": "public_document", "label_ar": "وثيقة منشورة", "help_ar": "وثيقة معلنة ومعروف ناشرها."}],
    "limit_menu": [
        {"id": "l_receipt", "label_ar": "الوصل يثبت الشراء لا أن الوشاح بقي عند صاحبه"},
        {"id": "l_illustrative", "label_ar": "أرقام المختبر توضيحية وغياب الألياف لا يثبت غياب التلامس"},
        {"id": "l_other_scarf", "label_ar": "لا تنفي الأدلة أن يكون لياسر وشاح أزرق آخر في بيته"},
        {"id": "l_invalid_count", "label_ar": "كثرة الألياف على قبعة ياسر تدل على أن الوشاح وشاحه"},
        {"id": "l_invalid_loud", "label_ar": "إصرار ياسر على دعواه يدل على أنه صادق"}],
    "mind_change_menu": [
        {"id": "m_serial", "label_ar": "ثبوت أن الرقم S-0187 مسجّل في المتجر لوصل آخر غير وصل مازن"},
        {"id": "m_embroidery", "label_ar": "ظهور وشاح أزرق آخر عليه الحرف المطرّز نفسه من الخيط نفسه"},
        {"id": "m_loaned", "label_ar": "ثبوت أن مازن أعار وشاحه لغيره قبل الرحلة"},
        {"id": "m_popular", "label_ar": "كثرة الطلاب الذين يؤيدون رواية ياسر"}],
    "skills": [{"skill_id": "KO-RS-06-001", "track": "B"}, {"skill_id": "KO-RS-06-015", "track": "D"}, {"skill_id": "KO-FC-04-018", "track": "E"}],
    "stage_hooks_ar": {"briefing": "وشاحان على مقعد… ومن يقول «لي» أكثر من واحد.", "investigating": "الأثر يخبرك بالملامسة، فمن يخبرك بالملكية؟", "review": "قبل أن تغلق الملف: ما الذي لا تعرفه؟", "resolved": "أُغلق الملف. في الأرشيف ملفات أكبر."},
    "character_glyphs": {"mazen": "م", "yasser": "ي", "layan": "ل", "mona": "من", "karim": "ك"},
}
sc = {
    "case_id": CID,
    "accepted_conclusions": {"h_mazen": {"grade": 1, "note_ar": "استنتاج متسق مع الأدلة ويتطلب ذكر حدوده."},
                             "h_yasser": {"grade": 0, "note_ar": "يخلط بين كثرة الألياف على القبعة والملكية، ويقبل وصلاً لوشاح آخر."},
                             "h_undecided": {"grade": 0, "note_ar": "يتوقف عند الألياف ولا يستعمل الرقم التسلسلي والعلامة المطرزة اللذين يحسمان."}},
    "confidence_band": {"h_mazen": [65, 90], "h_yasser": [0, 15], "h_undecided": [0, 20]},
    "source_key": {"ev_cap_fibres": "primary_record", "ev_seat_fibres": "primary_record", "ev_bag_fibres": "primary_record", "ev_fibre_lab": "primary_record",
                   "ev_mazen_receipt": "primary_record", "ev_yasser_receipt": "primary_record", "ev_scarf_tag": "primary_record", "ev_scarf_patch": "primary_record",
                   "ev_departure_photo": "primary_record", "ev_bus_log": "primary_record", "ev_shop_count": "primary_record", "ev_green_label": "primary_record",
                   "ev_mazen_statement": "claim", "ev_yasser_statement": "claim", "ev_layan_statement": "claim"},
    "link_key": {
        "h_mazen": {"ev_mazen_receipt": "supports", "ev_scarf_tag": "supports", "ev_departure_photo": "supports", "ev_scarf_patch": "supports", "ev_fibre_lab": "supports", "ev_bus_log": "supports", "ev_shop_count": "supports", "ev_cap_fibres": "neutral"},
        "h_yasser": {"ev_cap_fibres": "supports", "ev_yasser_receipt": "supports", "ev_scarf_tag": "weakens", "ev_mazen_receipt": "weakens", "ev_fibre_lab": "weakens", "ev_scarf_patch": "weakens"},
        "h_undecided": {"ev_cap_fibres": "supports", "ev_yasser_receipt": "supports", "ev_scarf_tag": "weakens", "ev_mazen_receipt": "weakens", "ev_scarf_patch": "weakens"},
    },
    "required_limits": ["l_receipt", "l_illustrative"], "valid_mind_changers": ["m_serial", "m_embroidery", "m_loaned"],
    "invalid_limits": ["l_invalid_count", "l_invalid_loud"],
    "decisive_evidence": ["ev_mazen_receipt", "ev_scarf_tag", "ev_departure_photo", "ev_scarf_patch", "ev_fibre_lab", "ev_bus_log"],
    "lab_requirement": None,
    "timeline_requirement": [{"evidence_id": "ev_departure_photo", "utc_minute": 42, "tol": 3}, {"evidence_id": "ev_bus_log", "utc_minute": 605, "tol": 5}],
    "refuted_hypotheses": ["h_yasser", "h_undecided"],
    "criteria_map": {"c_source": "source_typing", "c_conflict": "conflict_resolution", "c_links": "hypothesis_links", "c_uncertainty": "uncertainty", "c_revision": "revision", "c_elimination": "elimination", "c_justification": "justification_human"},
    "caps": {"no_citations_max": 45, "no_conflict_resolution_max": 65},
}
os.makedirs(OUT, exist_ok=True)
for suf, obj in [("", core), (".ui", ui), (".scoring", sc)]:
    with open(os.path.join(OUT, f"{CID}{suf}.json"), "w", encoding="utf8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
print("ok")
