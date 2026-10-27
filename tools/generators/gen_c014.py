#!/usr/bin/env python3
# Case c014 «الوصل ذو الرقمين» — from seed S-04 (heritage-inspired: the over-confident document and the primed witnesses).
# Teaches: tag HOW each person knows a figure (saw / heard), separate agreement from independence, let records that never passed
# through the disputed paper decide, and treat repeated hearing as a memory effect rather than a lie.
# No-culprit convention: the council member who wrote the larger figure believing he was correcting a slip (honest mistake, no intent
# to deceive) is recorded in culprit_ids. Fictional records house; no forgery technique is described (only what an examiner observes).
# Usage: gen_c014.py OUT_DIR
import json, sys, os
OUT = sys.argv[1]
CID = "c014_receipt_two_numbers"

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
ch("salem", "سالم الخطيب", "witness", "متبرع من أهل الحي",
   "هادئ ويتحرّج من الجدال، يتذكر ما دفعه بدقة لأنه جمعه على مدى أسابيع، ولا يحب أن يُفهم كلامه على أنه اتهام.",
   ["أن يُسجَّل تبرعه كما هو", "ألا يتسبب في خلاف بين أعضاء المكتبة"],
   [L("sl_greet", "greeting", "أهلاً بك. لا أريد خلافاً، أريد فقط أن يُكتب تبرعي كما كان."),
    L("sl_paid", "reveal", "سلّمت أمينة الدار مائة وخمسين ديناراً، وكتبت الوصل أمامي وقيّدت المبلغ في دفترها.", ["f_salem_paid"]),
    L("sl_unknown", "deflect_unknown", "لا أعرف ما جرى للوصل بعد أن غادرت الدار."),
    L("sl_off", "deflect_offtopic", "اسألني عمّا دفعته ومتى."),
    L("sl_bye", "farewell", "شكراً لأنك تراجع الأوراق قبل أن تحكم.")])
ch("nabil", "نبيل العاصي", "suspect", "عضو في مجلس مكتبة الحي",
   "متحمس لجمع التبرعات وسريع في الحكم، يميل إلى تذكّر الأرقام الكبيرة كما يتمنى لا كما سُجّلت، ويتراجع بلا عناد إذا واجهته بسجل.",
   ["أن تحصل المكتبة على تبرع كبير", "ألا يُظنّ أنه تعمّد خداع أحد"],
   [L("nb_greet", "greeting", "أنا أمثّل المجلس. الرقم عندنا مكتوب وواضح، وشاهدان يؤكدانه."),
    L("nb_recall", "reveal", "أبلغت المجلس في إحاطة اليوم الأول أن الأستاذ سالم تبرع بألف وخمسمائة دينار؛ هذا ما أذكره من وعده.", ["f_nabil_recall"]),
    L("nb_pledge", "reveal", "أنا متأكد من الرقم، فقد سمعته من المتبرع نفسه قبل يوم التسليم.", None, ["cl_nabil_pledge"]),
    L("nb_refuse", "refuse_secret", "لا أذكر شيئاً آخر عن الوصل بعد تسلّمي له."),
    L("nb_wrote", "reveal", "نعم... رأيت خانة الأرقام تقول مائة وخمسين فظننتها سهواً من الموظفة، فكتبت الرقم كما أذكره بقلمي ولم أنتبه إلى سطر الحروف. لم أقصد خداع أحد.", ["f_nabil_wrote"]),
    L("nb_unknown", "deflect_unknown", "لا أذكر ذلك."),
    L("nb_off", "deflect_offtopic", "ركّز على الوصل والمبلغ لو سمحت."),
    L("nb_bye", "farewell", "أريد أن تُحسم المسألة بالسجلات.")])
ch("huda", "هدى الصيرفي", "witness", "أمينة سر مجلس المكتبة",
   "منظمة وتحتفظ بمحاضر المجلس، تصدق ما سمعته في الاجتماعات ولا تفرّق دائماً بين ما رأته وما سمعته.",
   ["أن تبقى محاضر المجلس سليمة", "ألا تُتّهم بأنها تؤيد رقماً لا تعرف أصله"],
   [L("hd_greet", "greeting", "تفضّل. المحاضر عندي، وأستطيع أن أحدّثك عمّا قيل في الاجتماعات."),
    L("hd_recall", "reveal", "أتذكر أن التبرع كان ألفاً وخمسمائة دينار، وقد كتبت ذلك في إفادتي.", ["f_huda_recall"]),
    L("hd_claim", "reveal", "لا أنسى هذا الرقم، فقد تكرر أمامي مراراً.", None, ["cl_huda_1500"]),
    L("hd_absent", "reveal", "لم أحضر التسليم في دار السِّجِل، ولم أرَ الوصل إلا بعد أن اشتد الخلاف.", ["f_huda_absent"]),
    L("hd_minutes", "reveal", "محاضر الإحاطات اليومية محفوظة عندي، ويمكنك الاطلاع عليها.", ["f_minutes_exist"]),
    L("hd_unknown", "deflect_unknown", "لا أعرف أكثر من ذلك."),
    L("hd_off", "deflect_offtopic", "اسألني عن المحاضر وعن إفادتي."),
    L("hd_bye", "farewell", "أرجو أن يتبيّن الأمر دون أن يُظلم أحد.")])
ch("adel", "عادل المنصور", "witness", "عضو في مجلس المكتبة",
   "ودود ويحب التوافق، يميل إلى الموافقة على ما يردده زملاؤه ثم يتذكره كأنه رآه بنفسه.",
   ["ألا يبدو أنه خالف زملاءه", "أن تنتهي المسألة بسلام"],
   [L("ad_greet", "greeting", "أهلاً. أظن أن الأمر بسيط، فالرقم واضح لنا جميعاً."),
    L("ad_recall", "reveal", "أذكر أن المبلغ ألف وخمسمائة دينار، وهذا ما كتبته في الإفادة.", ["f_adel_recall"]),
    L("ad_claim", "reveal", "كلنا نعرف هذا الرقم منذ اليوم الأول، ولا مجال للخطأ فيه.", None, ["cl_adel_1500"]),
    L("ad_absent", "reveal", "لم أكن في دار السِّجِل يوم التسليم، ولم أرَ الوصل نفسه قبل الخلاف.", ["f_adel_absent"]),
    L("ad_unknown", "deflect_unknown", "لا أذكر شيئاً آخر."),
    L("ad_off", "deflect_offtopic", "هذا لا يخصّ المبلغ. اسألني عن الإفادة."),
    L("ad_bye", "farewell", "إن ظهر خطأ فمن الطبيعي أن نصححه.")])
ch("rana", "رنا الفارس", "expert", "أمينة الصادر في دار السِّجِل",
   "دقيقة ومباشرة، تعرف أشكال وصولات الدار وسجلاتها جيداً، ولا تتكلم إلا فيما قيّدته أو شاهدته بنفسها.",
   ["أن يُفهم كيف تُصدر الدار وصولاتها", "أن تبقى سجلات الدار سليمة"],
   [L("rn_greet", "greeting", "تفضّل. أستطيع أن أبيّن كيف نكتب الوصل ونقيّده، لكنني لا أعرف ما جرى له خارج الدار."),
    L("rn_issue", "reveal", "أصدرت الوصل رقم 412 بعد أن دفع الأستاذ سالم، وكتبت المبلغ رقماً وحروفاً في الدقيقة نفسها وقيّدته في سجل الصادر.", ["f_rana_issue"]),
    L("rn_records", "reveal", "للدار سجل صادر، وسجل إيداع بالتعاون مع مكتبة الحي، وسجل تسليم الحاضرين.", ["f_ledger_exists", "f_deposit_exists", "f_handover_exists"]),
    L("rn_custody", "reveal", "نكتب على بطاقة العهدة كل مرة يغادر فيها الوصل الدار أو يعود إليها، مع حالته.", ["f_custody_exists"]),
    L("rn_compare", "reveal", "مكتب الصيانة عندنا يستطيع أن يعرض عشرة وصولات من الدفتر نفسه للمقارنة، وأن يفحص الحبر بالضوء المائل.", ["f_ten_exists", "f_exam_possible"]),
    L("rn_unknown", "deflect_unknown", "هذا خارج ما قيّدته."),
    L("rn_off", "deflect_offtopic", "اسألني عن الوصولات وسجلاتها."),
    L("rn_bye", "farewell", "السجل لا يجامل أحداً، فاقرأه كما هو.")])

locations = [{"id": "loc_house", "name_ar": "دار السِّجِل", "description_ar": "دار تصدر الوصولات الرسمية وتحتفظ بسجلاتها."},
             {"id": "loc_hall", "name_ar": "قاعة مجلس مكتبة الحي", "description_ar": "حيث تُعقد إحاطات المجلس اليومية خلال معرض الكتاب."},
             {"id": "loc_desk", "name_ar": "مكتب الصيانة في الدار", "description_ar": "مكتب يفحص الوثائق ويقارنها."}]
objects = [{"id": "obj_receipt", "name_ar": "الوصل رقم 412", "description_ar": "وصل تبرع لمكتبة حيّ النخيل، يحمل رقمين مختلفين."}]
orgs = [{"id": "org_house", "name_ar": "دار السِّجِل", "description_ar": "مؤسسة خيالية تُصدر الوصولات وتحفظ سجلاتها."},
        {"id": "org_library", "name_ar": "مكتبة حيّ النخيل", "description_ar": "مكتبة حيّ خيالية يديرها مجلس من الأهالي."}]

# ---------------------------------------------------------------- facts
facts = []
def F(id, st, kind, subj, spoiler, time=None, loc=None, ko=None):
    d = {"id": id, "statement_ar": st, "kind": kind, "subject_ids": subj, "spoiler_level": spoiler}
    if time: d["time"] = time
    if loc: d["location_id"] = loc
    if ko: d["science_ko_refs"] = ko
    facts.append(d)
F("f_dispute", "اختلف المتبرع ومجلس المكتبة على مبلغ التبرع المدوّن في الوصل رقم 412.", "event", ["obj_receipt", "salem", "org_library"], 0)
F("f_council_claims", "يتمسك المجلس بأن المبلغ ألف وخمسمائة دينار، ويقول إن شاهدين من أعضائه يذكران الرقم نفسه.", "attribute", ["nabil", "huda", "adel"], 0)
F("f_donor_recalls", "يذكر المتبرع أنه دفع مبلغاً أقل بكثير مما يقوله المجلس.", "attribute", ["salem"], 0)
F("f_salem_paid", "دفع سالم مائة وخمسين ديناراً لأمينة الصادر في دار السِّجِل.", "event", ["salem", "rana"], 1, T(80), "loc_house")
F("f_rana_issue", "أصدرت أمينة الصادر الوصل 412 وكتبت المبلغ رقماً وحروفاً وقيّدته في سجل الصادر.", "event", ["rana", "obj_receipt"], 1, T(100), "loc_house")
F("f_nabil_recall", "يذكر نبيل أن المتبرع وعد بألف وخمسمائة دينار، وأنه أبلغ المجلس بذلك في إحاطة اليوم الأول.", "attribute", ["nabil"], 1, T(480), "loc_hall")
F("f_huda_recall", "تذكر هدى أن التبرع ألف وخمسمائة دينار وقد دوّنت ذلك في إفادتها.", "attribute", ["huda"], 1)
F("f_adel_recall", "يذكر عادل أن التبرع ألف وخمسمائة دينار وقد دوّن ذلك في إفادته.", "attribute", ["adel"], 1)
F("f_huda_absent", "لم تحضر هدى التسليم في دار السِّجِل ولم ترَ الوصل قبل الخلاف.", "state", ["huda"], 2)
F("f_adel_absent", "لم يحضر عادل التسليم في دار السِّجِل ولم ير الوصل قبل الخلاف.", "state", ["adel"], 2)
F("f_ledger_exists", "للدار سجل صادر يقيّد كل وصل بمبلغه وصاحبه ووقته.", "state", ["org_house"], 1, None, "loc_house")
F("f_deposit_exists", "تودع الدار التبرعات في حساب المكتبة ويصدر عن ذلك إشعار إيداع.", "state", ["org_house", "org_library"], 1, None, "loc_house")
F("f_handover_exists", "للدار سجل يدوّن من حضر كل تسليم.", "state", ["org_house"], 1, None, "loc_house")
F("f_custody_exists", "للدار بطاقة عهدة لكل وصل تدوّن من تسلّمه ومتى وفي أي حالة.", "state", ["org_house", "obj_receipt"], 1, None, "loc_house")
F("f_minutes_exist", "تحتفظ أمينة السر بمحاضر الإحاطات اليومية لمجلس المكتبة.", "state", ["huda"], 1, None, "loc_hall")
F("f_ten_exists", "يستطيع مكتب الصيانة عرض عشرة وصولات من الدفتر نفسه للمقارنة.", "state", ["rana", "loc_desk"], 1, None, "loc_desk")
F("f_exam_possible", "يستطيع مكتب الصيانة فحص الحبر والورق بالضوء المائل وبالتكبير.", "state", ["rana", "loc_desk"], 1, None, "loc_desk")
F("f_nabil_wrote", "كتب نبيل الرقم 1500 في خانة الأرقام بقلمه بعد أن تسلّم الوصل، ظناً منه أن الموظفة سهت.", "event", ["nabil", "obj_receipt"], 3, T(300, "approx", 3450), "loc_hall", ["KO-RS-05-014"])
F("f_issued_150", "صدر الوصل 412 بمبلغ مائة وخمسين ديناراً، وهذا هو المبلغ المدفوع والمقيّد.", "relation", ["obj_receipt", "salem"], 3, T(80, "exact", 245), None, ["KO-RS-05-001", "KO-RS-06-002"])
F("f_numeral_later", "الرقم 1500 في خانة الأرقام كُتب بعد صدور الوصل وبعد خروجه من الدار.", "relation", ["obj_receipt"], 3, T(120, "exact", 3450), None, ["KO-RS-06-004", "KO-RS-05-005"])
F("f_no_firsthand", "لم يشهد الشاهدان دفع المبلغ ولم يريا الوصل قبل الخلاف، فمعرفتهما بالرقم منقولة لا مباشرة.", "relation", ["huda", "adel"], 3, None, None, ["KO-RS-05-001", "KO-RS-05-004"])
F("f_figure_spread", "تردد الرقم 1500 في الإحاطات اليومية على لسان عضو المجلس قبل أن يشك فيه أحد.", "relation", ["nabil", "huda", "adel"], 2, T(480, "exact", 3360), "loc_hall", ["KO-RS-05-004"])

claims = [
    {"id": "cl_nabil_pledge", "statement_ar": "سمعت المتبرع بنفسي يعد بألف وخمسمائة دينار.", "kind": "honest_mistake", "held_by": ["nabil"], "true_fact_id": "f_issued_150", "contradicted_by_evidence_ids": ["ev_ledger", "ev_deposit"]},
    {"id": "cl_huda_1500", "statement_ar": "أذكر الرقم ألفاً وخمسمائة بيقين لأنه تكرر أمامي كثيراً.", "kind": "honest_mistake", "held_by": ["huda"], "true_fact_id": "f_no_firsthand", "contradicted_by_evidence_ids": ["ev_ledger", "ev_handover_log"]},
    {"id": "cl_adel_1500", "statement_ar": "كلنا نعرف الرقم منذ اليوم الأول ولا مجال للخطأ فيه.", "kind": "honest_mistake", "held_by": ["adel"], "true_fact_id": "f_no_firsthand", "contradicted_by_evidence_ids": ["ev_ledger", "ev_handover_log"]},
]
timeline = [
    {"id": "te_pay", "description_ar": "سالم يسلّم المبلغ، وأمينة الصادر تكتب الوصل 412 رقماً وحروفاً.", "time": T(80), "location_id": "loc_house", "actor_ids": ["salem", "rana"], "fact_ids": ["f_salem_paid", "f_rana_issue"], "motivated_by_ar": "أراد التبرع للمكتبة وأن يحصل على وصل رسمي"},
    {"id": "te_ledger", "description_ar": "قيد الوصل في سجل الصادر.", "time": T(100), "location_id": "loc_house", "actor_ids": ["rana"], "fact_ids": ["f_rana_issue"], "motivated_by_ar": "قاعدة الدار أن يُقيَّد كل وصل فور إصداره"},
    {"id": "te_custody", "description_ar": "نبيل يتسلّم نسخة المجلس من الوصل لتوضع في ملف المجلس.", "time": T(120), "location_id": "loc_house", "actor_ids": ["nabil", "rana"], "fact_ids": ["f_custody_exists"], "motivated_by_ar": "طلب المجلس نسخته من الوصل"},
    {"id": "te_deposit", "description_ar": "إيداع المبلغ في حساب المكتبة وصدور إشعار الإيداع.", "time": T(245), "location_id": "loc_house", "actor_ids": [], "fact_ids": ["f_deposit_exists"]},
    {"id": "te_brief1", "description_ar": "إحاطة المجلس الأولى: نبيل يذكر الرقم 1500.", "time": T(480), "location_id": "loc_hall", "actor_ids": ["nabil", "huda", "adel"], "fact_ids": ["f_nabil_recall", "f_figure_spread"], "motivated_by_ar": "إطلاع المجلس على مستجدات التبرعات خلال المعرض"},
    {"id": "te_brief3", "description_ar": "إحاطة المجلس الثالثة: يتكرر الرقم عند صياغة لوحة الشكر.", "time": T(3360), "location_id": "loc_hall", "actor_ids": ["nabil", "huda", "adel"], "fact_ids": ["f_figure_spread"], "motivated_by_ar": "إعداد لوحة شكر للمتبرعين"},
    {"id": "te_dispute", "description_ar": "المتبرع يرى لوحة الشكر ويعترض على المبلغ.", "time": T(3420), "location_id": "loc_hall", "actor_ids": ["salem"], "fact_ids": ["f_dispute"], "motivated_by_ar": "أراد أن يُذكر تبرعه كما هو"},
    {"id": "te_return", "description_ar": "نبيل يعيد الوصل إلى الدار للفحص، وتُسجَّل حالته على بطاقة العهدة.", "time": T(3450), "location_id": "loc_house", "actor_ids": ["nabil", "rana"], "fact_ids": ["f_custody_exists"], "motivated_by_ar": "طلب المجلس والمتبرع فحص الوصل"},
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
V("ev_receipt", "الوصل المتنازع عليه رقم 412", "documentary",
  "دار السِّجِل — وصل تبرع رقم 412 (نسخة المجلس)\nإلى: مكتبة حيّ النخيل\nالدافع: سالم الخطيب\nالمبلغ بالأرقام: 1500 (بحبر أزرق داكن)\nالمبلغ بالحروف: مائة وخمسون ديناراً فقط لا غير (بحبر أسود)\nالختم: ختم الدار أسفل النص\nتوقيع الموظفة: ر. الفارس",
  ["a_read_receipt"], ["f_issued_150"], "strong",
  "وثيقة واحدة تحمل رقمين، ولا تقول بنفسها أيّهما الأصلي ولا من كتب أحدهما ولا متى.", loc="loc_house")
V("ev_ink_note", "مذكرة فحص مكتب الصيانة", "documentary",
  "مذكرة مكتب الصيانة بالدار — فحص الوصل 412 بالضوء المائل وبالتكبير\n1) سطر الحروف: حبر أسود يطابق حبر باقي النص.\n2) خانة الأرقام: حبر أزرق داكن، ولمعانه يختلف عن بقية الوصل.\n3) سطح الورق داخل الخانة أخشن من محيطه، وفيه أثر ضغط قلم تحت الحبر الأزرق.\nالوصف: كُتبت خانة الأرقام في حدث كتابة مختلف عن حدث كتابة بقية الوصل.",
  ["a_get_ink"], ["f_numeral_later"], "strong",
  "تصف خصائص فئوية للحبر والورق ولا تحدد من كتب الخانة ولا متى بالضبط ولا نيته.", ko="KO-FC-04B-004", loc="loc_desk")
V("ev_ten_receipts", "عشرة وصولات من الدفتر نفسه", "documentary",
  "ورقة مقارنة من مكتب الصيانة: الوصولات 402 إلى 411 من الدفتر نفسه.\nفي كل منها: خانة الأرقام وسطر الحروف بحبر واحد وبقيمة واحدة.\nفي كل منها: ينتهي سطر الحروف بعبارة «فقط لا غير»، والختم أسفل النص.\nلا وصل منها يحمل رقمين مختلفين.",
  ["a_get_ten"], ["f_issued_150"], "moderate",
  "عشرة وصولات تبيّن عادة الدار ولا تفرض قاعدة؛ ولا تقول شيئاً مباشراً عن الوصل 412.", loc="loc_desk")
V("ev_ledger", "سجل الصادر في الدار", "documentary",
  "سجل الصادر — دار السِّجِل\nرقم الوصل: 412 | الوقت: 10:40 | الجهة: تبرع لمكتبة حيّ النخيل\nالدافع: سالم الخطيب | المبلغ: 150 ديناراً\nالموظفة: رنا الفارس | الحالة: مودَع",
  ["a_get_ledger"], ["f_issued_150"], "strong",
  "سجل صنعته الدار نفسها ولم يمرّ عبر الوصل؛ لا يثبت وحده أن المبلغ دُفع فعلاً، ويحتاج إلى سند مستقل مثل الإيداع.",
  contradicts=["cl_nabil_pledge", "cl_huda_1500", "cl_adel_1500"], loc="loc_house")
V("ev_deposit", "إشعار إيداع في حساب المكتبة", "documentary",
  "إشعار إيداع — حساب مكتبة حيّ النخيل\nالتاريخ: يوم التسليم، 13:05\nالمبلغ: 150 ديناراً\nالمودِع: صندوق دار السِّجِل\nالمرجع: وصل 412",
  ["a_get_deposit"], ["f_issued_150"], "strong",
  "يثبت دخول مبلغ إلى حساب المكتبة ومرجعه؛ لا يثبت من دفعه ولا ما كُتب في خانات الوصل.", contradicts=["cl_nabil_pledge"], loc="loc_house")
V("ev_custody_card", "بطاقة العهدة للوصل 412", "documentary",
  "بطاقة العهدة — الوصل 412 (نسخة المجلس)\n10:20 صدر من الدار | الحالة: الرقمان بالأرقام والحروف 150 بحبر واحد | رنا الفارس\n11:00 سُلّم لنبيل العاصي لوضعه في ملف المجلس | الحالة: بلا تغيير\nاليوم الثالث 18:30 أُعيد إلى الدار للفحص بيد نبيل العاصي | الحالة: خانة الأرقام 1500، سطر الحروف مائة وخمسون | رنا الفارس\nاليوم الثالث 18:35 اطّلع عليه في حضور أمينة الصادر: هدى الصيرفي وعادل المنصور (أول اطلاع لهما)",
  ["a_get_custody"], ["f_numeral_later", "f_no_firsthand"], "strong",
  "تسجّل من حمل الوصل وحالته عند كل تسليم، لكنها لا تبيّن ما حدث بين التسليمين ولا من كتب الرقم.", loc="loc_house")
V("ev_handover_log", "سجل حضور التسليم", "documentary",
  "سجل الدار — حضور التسليم (رقم 412)\nالحاضرون: سالم الخطيب (المتبرع)، رنا الفارس (أمينة الصادر)، فادي الحداد (أمين صندوق الدار)\nالوقت: 10:20 إلى 10:40\nملاحظة: لم يحضر أحد من مجلس المكتبة.",
  ["a_get_handover"], ["f_no_firsthand"], "strong",
  "يثبت من كان في الدار وقت التسليم ولا ينفي أن يكون أحدهم سمع بالمبلغ بطريق آخر.", contradicts=["cl_huda_1500", "cl_adel_1500"], loc="loc_house")
V("ev_minutes", "محاضر الإحاطات الثلاث", "documentary",
  "محاضر إحاطات مجلس مكتبة حيّ النخيل — معرض الكتاب\nالإحاطة 1 (17:00، يوم التسليم): بند التبرعات — «أبلغ نبيل العاصي بتبرع الأستاذ سالم بألف وخمسمائة دينار».\nالإحاطة 2 (17:00، اليوم التالي): «ذكّر نبيل العاصي بالتبرع الكبير وطلب لوحة شكر».\nالإحاطة 3 (17:00، اليوم الثالث): «اقترح نبيل العاصي أن تُكتب اللوحة: ألف وخمسمائة دينار».\nالحاضرون في الثلاث: نبيل العاصي، هدى الصيرفي، عادل المنصور.",
  ["a_get_minutes"], ["f_figure_spread"], "strong",
  "تثبت ما قيل في الاجتماعات ومن حضر، لا صحة ما قيل ولا من أين جاء به قائله.", loc="loc_hall")
V("ev_stamp_check", "فحص الختم", "documentary",
  "تقرير مكتب الصيانة — الختم على الوصل 412\nالختم مطابق لختم الدار المعتمد في الشكل والموضع.\nلا أثر لختم ثانٍ أو لإعادة ختم.",
  ["a_get_stamp"], [], "strong",
  "يثبت أن الورقة صدرت عن الدار فعلاً؛ لا يقول شيئاً عمّا كُتب فيها بعد الختم.", red=True, loc="loc_desk")
V("ev_salem_statement", "إفادة سالم الخطيب (ملخص)", "testimonial",
  "ملخص إفادة سالم الخطيب:\n«دفعت مائة وخمسين ديناراً لأمينة الدار في الدار نفسها. لم أرَ الوصل بعد ذلك حتى ظهرت لوحة الشكر.»",
  ["a_note_salem"], ["f_salem_paid"], "moderate",
  "إفادة صاحب مصلحة في المبلغ؛ تؤيدها سجلات الدار ولا تغني عنها.", loc="loc_house")
V("ev_nabil_statement", "إفادة نبيل العاصي (ملخص)", "testimonial",
  "ملخص إفادة نبيل العاصي:\n«سمعت من المتبرع قبل يوم التسليم أنه سيتبرع بألف وخمسمائة. أبلغت المجلس بذلك، والوصل في ملف المجلس يؤكد الرقم.»",
  ["a_note_nabil"], ["f_nabil_recall"], "weak",
  "ذاكرة صاحب مصلحة في الرقم الكبير؛ لا سجل يؤيد الوعد المزعوم، وتُقاس بسجلات الدار.", loc="loc_hall")
V("ev_huda_form", "نموذج إفادة هدى الصيرفي", "testimonial",
  "نموذج إفادة (تملؤه الشاهدة) — هدى الصيرفي\nما المبلغ الذي تذكرينه؟ ألف وخمسمائة دينار.\nهل حضرتِ التسليم في الدار؟ لا.\nمتى رأيتِ الوصل أول مرة؟ بعد الخلاف.\nكيف عرفتِ المبلغ؟ سمعته في الإحاطات اليومية.",
  ["a_note_huda"], ["f_huda_recall", "f_huda_absent"], "moderate",
  "تصف مصدر معرفة الشاهدة بلسانها؛ تعبّر عن ذاكرتها لا عن صحة الرقم.", red=True, loc="loc_hall")
V("ev_adel_form", "نموذج إفادة عادل المنصور", "testimonial",
  "نموذج إفادة (يملؤه الشاهد) — عادل المنصور\nما المبلغ الذي تذكره؟ ألف وخمسمائة دينار.\nهل حضرت التسليم في الدار؟ لا.\nمتى رأيت الوصل أول مرة؟ بعد الخلاف.\nكيف عرفت المبلغ؟ سمعته في الإحاطات، وكان الجميع يذكره.",
  ["a_note_adel"], ["f_adel_recall", "f_adel_absent"], "moderate",
  "يصف مصدر معرفة الشاهد بلسانه؛ يعبّر عن ذاكرته لا عن صحة الرقم.", red=True, loc="loc_hall")
V("ev_rana_statement", "إفادة رنا الفارس (ملخص)", "testimonial",
  "ملخص إفادة رنا الفارس، أمينة الصادر:\n«كتبت المبلغ رقماً وحروفاً بحبر الدار في الدقيقة نفسها وقيّدته فور ذلك. لا أعرف ما جرى للوصل خارج الدار.»",
  ["a_note_rana"], ["f_rana_issue"], "moderate",
  "إفادة موظفة الدار صاحبة الإصدار؛ تؤيدها سجلات الدار ولا تثبت ما جرى خارجها.", loc="loc_house")

# ---------------------------------------------------------------- inferences
def P(t, i): return {"ref_type": t, "ref_id": i}
inf = []
def I(id, prem, ct, concl, rel, strength, rule, ks):
    inf.append({"id": id, "premises": prem, "conclusion": {"ref_type": ct, "ref_id": concl}, "relation": rel, "strength": strength, "rule_ar": rule, "skill_ko_refs": ks})
# path A: the paper itself and the witnesses' own forms
I("i_a_later", [P("evidence", "ev_receipt"), P("evidence", "ev_ink_note")], "fact", "f_numeral_later", "establishes", "strong",
  "الحبر والورق في خانة الأرقام يختلفان عن بقية الوصل، وتحت الحبر أثر ضغط سابق؛ فالخانة كُتبت في حدث كتابة آخر غير الذي كُتب فيه سطر الحروف.", ["KO-RS-06-004"])
I("i_a_150", [P("evidence", "ev_receipt"), P("evidence", "ev_ink_note"), P("evidence", "ev_ten_receipts")], "fact", "f_issued_150", "establishes", "strong",
  "في عشرة وصولات من الدفتر نفسه يتطابق السطران حبراً وقيمة؛ وهنا السطر الذي يطابق حبر الدار هو سطر الحروف، فما صدر أصلاً هو مائة وخمسون.", ["KO-RS-05-001", "KO-RS-06-002"])
I("i_a_nofh", [P("evidence", "ev_huda_form"), P("evidence", "ev_adel_form")], "fact", "f_no_firsthand", "establishes", "strong",
  "الشاهدان يجيبان بأنفسهما أنهما لم يحضرا التسليم ولم يريا الوصل قبل الخلاف؛ فمعرفتهما بالرقم لا تأتي من معاينة.", ["KO-RS-05-001"])
I("i_a_spread", [P("evidence", "ev_huda_form"), P("evidence", "ev_adel_form")], "fact", "f_figure_spread", "establishes", "strong",
  "الشاهدان يذكران أن مصدر الرقم هو ما سمعاه في الإحاطات، ويقول أحدهما إن الجميع كان يذكره؛ فالرقم انتشر بالتكرار في المجلس.", ["KO-RS-05-004"])
# path B: records that never passed through the disputed paper
I("i_b_150", [P("evidence", "ev_ledger"), P("evidence", "ev_deposit")], "fact", "f_issued_150", "establishes", "strong",
  "سجل الصادر وإشعار الإيداع جهتان مختلفتان، ولم يمرّ أيٌّ منهما بالوصل؛ وكلاهما يضع المبلغ مائة وخمسين.", ["KO-RS-06-002", "KO-RS-05-004"])
I("i_b_later", [P("evidence", "ev_custody_card"), P("evidence", "ev_ledger")], "fact", "f_numeral_later", "establishes", "strong",
  "بطاقة العهدة تثبت أن الخانة كانت 150 عند الإصدار وعند التسليم الأول وصارت 1500 عند الإعادة، وسجل الصادر يوافق الحالة الأولى؛ فالتغيير جرى بعد خروج الوصل من الدار.", ["KO-RS-05-005", "KO-RS-06-004"])
I("i_b_nofh", [P("evidence", "ev_handover_log"), P("evidence", "ev_custody_card")], "fact", "f_no_firsthand", "establishes", "strong",
  "سجل الحضور يخلو من أعضاء المجلس، وبطاقة العهدة تضع أول اطلاع لهما على الوصل بعد الخلاف؛ فلم يعاينا الدفع ولا الوصل.", ["KO-RS-05-001", "KO-RS-05-004"])
I("i_b_spread", [P("evidence", "ev_minutes")], "fact", "f_figure_spread", "establishes", "strong",
  "المحاضر تضع الرقم في الإحاطات الثلاث على لسان العضو نفسه، وبحضور الشاهدين، قبل أي اعتراض.", ["KO-RS-05-004"])
# hypothesis ledger (premises are facts that either path derives)
I("i_support_added", [P("fact", "f_issued_150"), P("fact", "f_numeral_later")], "hypothesis", "h_added", "supports", "strong",
  "ما صدر وقُيّد هو مائة وخمسون، والرقم الأكبر ظهر لاحقاً في الخانة بعد خروج الوصل؛ فالرقم الأكبر إضافة لاحقة لا مبلغ مدفوع.", ["KO-RS-06-001"])
I("i_support_nabil", [P("evidence", "ev_custody_card")], "hypothesis", "h_added", "supports", "suggestive",
  "الوصل بقي في ملف المجلس بين التسليم الأول والإعادة، وعضو المجلس هو من سلّمه عند الإعادة؛ هذا يحصر الفترة والجهة التي تغيّرت فيها الخانة ولا يثبت من كتب.", ["KO-RS-06-001"])
I("i_rule_large", [P("fact", "f_issued_150"), P("fact", "f_numeral_later")], "hypothesis", "h_large", "rules_out", "conclusive",
  "إذا كان المبلغ المدفوع والمقيّد مائة وخمسين وكان الرقم الأكبر لاحقاً للإصدار فلا يصح أن يكون المبلغ الحقيقي ألفاً وخمسمائة.", ["KO-RS-06-008"])
I("i_rule_lie", [P("fact", "f_no_firsthand"), P("fact", "f_figure_spread")], "hypothesis", "h_lie", "rules_out", "strong",
  "من لم يعاين الدفع ولا الوصل ويسمع رقماً يتكرر في كل إحاطة سيتذكره بثقة؛ هذا يفسّر اتفاق الشاهدين دون افتراض اتفاق مسبق على الكذب، وهما قالا مصدر معرفتهما بلا مواربة.", ["KO-RS-05-007", "KO-RS-05-004"])
I("i_claim_nabil", [P("fact", "f_issued_150"), P("fact", "f_numeral_later")], "claim", "cl_nabil_pledge", "contradicts_claim", "strong",
  "السجلان المستقلان يضعان المبلغ مائة وخمسين، وما يسنده من الوصل كُتب لاحقاً؛ فوعد الألف وخمسمائة لا سند له في أي سجل.", ["KO-RS-05-014"])
I("i_claim_witness", [P("fact", "f_no_firsthand")], "claim", "cl_huda_1500", "contradicts_claim", "strong",
  "ثقة الشاهدة في الرقم لا تدل على أنها رأته؛ وهي لم تحضر ولم ترَ الوصل.", ["KO-RS-05-001"])
I("i_claim_witness2", [P("fact", "f_no_firsthand")], "claim", "cl_adel_1500", "contradicts_claim", "strong",
  "إجماع المجلس على الرقم لا يقيس صحته إذا كان مصدره واحداً؛ والشاهد لم يحضر ولم ير الوصل.", ["KO-RS-05-004"])

# ---------------------------------------------------------------- character knowledge
K = lambda f, a="witnessed", c="certain": {"fact_id": f, "access": a, "certainty": c}
ck = [
    {"character_id": "salem", "knows": [K("f_salem_paid")], "hides": [], "believes": []},
    {"character_id": "nabil", "knows": [K("f_nabil_recall", "inferred", "fairly_sure")],
     "hides": [{"fact_id": "f_nabil_wrote", "reveal_when": {"presented": {"evidence_id": "ev_custody_card", "to_character": "nabil"}}, "cover_claim_id": "cl_nabil_pledge", "reveal_line_id": "nb_wrote"}],
     "believes": [{"claim_id": "cl_nabil_pledge", "stance": "sincere"}]},
    {"character_id": "huda", "knows": [K("f_huda_recall", "told_by", "fairly_sure"), K("f_huda_absent"), K("f_minutes_exist")], "hides": [], "believes": [{"claim_id": "cl_huda_1500", "stance": "sincere"}]},
    {"character_id": "adel", "knows": [K("f_adel_recall", "told_by", "fairly_sure"), K("f_adel_absent")], "hides": [], "believes": [{"claim_id": "cl_adel_1500", "stance": "sincere"}]},
    {"character_id": "rana", "knows": [K("f_rana_issue"), K("f_ledger_exists", "professional"), K("f_deposit_exists", "professional"), K("f_handover_exists", "professional"), K("f_custody_exists", "professional"),
                                      K("f_ten_exists", "professional"), K("f_exam_possible", "professional")], "hides": [], "believes": []},
]
# told_by needs a source character
for k in ck:
    for kn in k["knows"]:
        if kn["access"] == "told_by": kn["source_character_id"] = "nabil"
hyps = [
    {"id": "h_added", "statement_ar": "كُتب الرقم الكبير في خانة الأرقام بعد صدور الوصل ولا يمثل المبلغ المدفوع؛ والأرجح أن عضو المجلس كتبه ظناً منه أنه يصحح سهواً.", "is_true": True, "plausibility_at_start": "low", "suspect_id": "nabil"},
    {"id": "h_large", "statement_ar": "المبلغ الحقيقي ألف وخمسمائة دينار والمتبرع هو الذي يخطئ في تذكر ما دفع.", "is_true": False, "plausibility_at_start": "high"},
    {"id": "h_lie", "statement_ar": "الشاهدان اتفقا عمداً على قول غير صحيح لتأييد المجلس.", "is_true": False, "plausibility_at_start": "medium"},
]
mis = [
    {"id": "rh_agree", "points_to_hypothesis_id": "h_large", "planted_via_ar": "شاهدان من المجلس يذكران الرقم نفسه بثقة، فيبدو أن اتفاقهما دليل على صحته.", "evidence_ids": ["ev_huda_form", "ev_adel_form"],
     "refuted_by_inference_ids": ["i_rule_large", "i_rule_lie", "i_a_nofh", "i_b_nofh"],
     "fairness_note_ar": "نموذجا الإفادة نفسهما يقولان إن الشاهدين لم يحضرا ولم يريا الوصل وإن مصدرهما ما سمعاه في الإحاطات؛ والمحاضر وسجل الحضور يؤكدان ذلك دون الاعتماد عليهما."},
    {"id": "rh_stamp", "points_to_hypothesis_id": "h_large", "planted_via_ar": "الختم سليم ومطابق، فيبدو أن الوصل صحيح بما فيه رقمه الكبير.", "evidence_ids": ["ev_stamp_check"],
     "refuted_by_inference_ids": ["i_rule_large", "i_a_later", "i_b_later"],
     "fairness_note_ar": "سلامة الختم تثبت أن الورقة صدرت عن الدار، وسجل الصادر وبطاقة العهدة ومذكرة الفحص تبيّن أن تغييراً في خانة الأرقام وقع بعد الختم دون أن يمسّه."},
]
los = [
    {"id": "lo_claim", "statement_ar": "يسأل «كيف عرف هذا الشخص؟» ويفرّق بين من رأى ومن سمع، ويقيس القول بسجل.", "skill_ko_ref": "KO-RS-05-001", "observable_behaviors_ar": ["يصنّف الإفادات أقوالاً", "يقرأ حقل مصدر المعرفة في نموذج الإفادة"], "evidence_sources": ["evidence_board"]},
    {"id": "lo_timeline", "statement_ar": "يرتّب أحداث الوصل على خط زمني ليعرف متى كان الرقم الأصلي ومتى ظهر الأكبر.", "skill_ko_ref": "KO-RS-05-005", "observable_behaviors_ar": ["يضع التسليم والقيد والإيداع في أزمنتها"], "evidence_sources": ["timeline_task", "action_log"]},
    {"id": "lo_hyp", "statement_ar": "يوازن بين فرضيتين على الأقل ويستبعد ما تنقضه الأدلة.", "skill_ko_ref": "KO-RS-05-002", "observable_behaviors_ar": ["يضيف فرضيات", "يستبعد بدليل"], "evidence_sources": ["hypothesis_ledger"]},
    {"id": "lo_diag", "statement_ar": "يقدّر ما يثبته كل دليل وما لا يثبته، ويتحقق من استقلال الأدلة قبل عدّها.", "skill_ko_ref": "KO-RS-05-004", "observable_behaviors_ar": ["لا يعدّ اتفاق شاهدين مصدرهما واحد دليلين", "يربط الدليل بالفرضية باتجاه صحيح"], "evidence_sources": ["evidence_board", "final_justification"]},
    {"id": "lo_calib", "statement_ar": "يصوغ نسبة الترجيح بحدودها.", "skill_ko_ref": "KO-RS-06-021", "observable_behaviors_ar": ["يختار ثقة معقولة", "يذكر حدوداً"], "evidence_sources": ["final_justification"]},
    {"id": "lo_revise", "statement_ar": "يراجع رأيه الأول حين يظهر ما يخالفه.", "skill_ko_ref": "KO-RS-06-009", "observable_behaviors_ar": ["يغيّر فرضيته الرائدة بدليل"], "evidence_sources": ["hypothesis_ledger"]},
]
def levels(d): return [{"score": i, "descriptor_ar": t} for i, t in enumerate(d)]
rub = {
    "reference_answer_ar": "المبلغ المدفوع والمقيّد مائة وخمسون ديناراً: هذا ما في سطر الحروف بحبر الدار، وما في سجل الصادر، وما في إشعار الإيداع، وما سُجّل على بطاقة العهدة عند الإصدار. أما الرقم الأكبر فكُتب في خانة الأرقام بحبر آخر بعد خروج الوصل من الدار وأثناء وجوده في ملف المجلس. والشاهدان لم يكذبا: لم يحضرا الدفع ولم يريا الوصل، وإنما كرّرا ما سمعاه في الإحاطات. حدود الاستنتاج: لا تثبت الأدلة من كتب الرقم بيده ولا نيته ولا لحظته، والأرجح أن عضو المجلس كتبه ظناً منه أنه يصحح، ولا تنفي الأدلة أن يكون المتبرع قال كلاماً آخر في حديث لا سجل له.",
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
    H("hg1", 1, "metacognitive", "حين يتفق شخصان على رقم، اسأل: كيف عرف كلٌّ منهما؟ هل رأى بنفسه أم سمع؟", {"always": True}, None, 0.02),
    H("hg2", 2, "focus_area", "اقرأ في كل إفادة السؤال عن «كيف عرفت؟» قبل أن تعدّ الإفادتين دليلين.", he("ev_huda_form"), None, 0.04),
    H("hg3", 3, "pointer", "ابحث عن سجلات لم يمرّ بها الوصل نفسه، وقارن أرقامها برقم الوصل.", he("ev_huda_form"), None, 0.08),
    H("hl1", 1, "metacognitive", "في الوصل رقمان؛ أيهما يطابق بقية الوصل في الحبر وفي عادة الدار؟", he("ev_receipt"), "i_a_150", 0.02),
    H("hl2", 2, "pointer", "قارن الوصل بوصولات الدفتر نفسه، وانظر ماذا يقول مكتب الصيانة عن الحبر في كل خانة.", he("ev_receipt"), "i_a_150", 0.06),
    H("hl3", 3, "partial_reveal", "اطلب سجل الصادر وإشعار الإيداع: ينبغي أن يتفقا مع أحد الرقمين دون أن يمرّا بالوصل.", he("ev_receipt"), "i_a_150", 0.1),
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
Act("a_read_receipt", "examine", "افحص الوصل 412 بإذن مجلس المكتبة", al, [G("ev_receipt")], "loc_house", "READ_RECEIPT")
Act("a_get_ink", "examine", "اطلب مذكرة فحص مكتب الصيانة", al, [G("ev_ink_note")], "loc_desk", "GET_INK")
Act("a_get_ten", "examine", "اطلب ورقة مقارنة الوصولات العشرة", al, [G("ev_ten_receipts")], "loc_desk", "GET_TEN")
Act("a_get_stamp", "examine", "اطلب تقرير فحص الختم", al, [G("ev_stamp_check")], "loc_desk", "GET_STAMP")
Act("a_get_ledger", "examine", "اقرأ سجل الصادر بإذن إدارة الدار", al, [G("ev_ledger")], "loc_house", "GET_LEDGER")
Act("a_get_deposit", "examine", "اطلب إشعار الإيداع بإذن إدارة الدار", al, [G("ev_deposit")], "loc_house", "GET_DEPOSIT")
Act("a_get_custody", "examine", "اطلب بطاقة العهدة للوصل", al, [G("ev_custody_card")], "loc_house", "GET_CUSTODY")
Act("a_get_handover", "examine", "اقرأ سجل حضور التسليم", al, [G("ev_handover_log")], "loc_house", "GET_HANDOVER")
Act("a_get_minutes", "examine", "اطلب محاضر الإحاطات بإذن المجلس", al, [G("ev_minutes")], "loc_hall", "GET_MINUTES")
for cid, lab in [("salem", "سالم"), ("nabil", "نبيل"), ("huda", "هدى"), ("adel", "عادل"), ("rana", "رنا")]:
    Act(f"a_int_{cid}", "interview", f"ابدأ مقابلة {lab}", al, [{"op": "raise_trust", "ref_id": cid, "amount": 1}], cid, f"INT_{cid.upper()}")
Act("a_note_salem", "examine", "دوّن إفادة سالم", fu("f_salem_paid"), [G("ev_salem_statement")], "salem", "NOTE_SALEM")
Act("a_note_nabil", "examine", "دوّن إفادة نبيل", fu("f_nabil_recall"), [G("ev_nabil_statement")], "nabil", "NOTE_NABIL")
Act("a_note_huda", "examine", "اطلب نموذج إفادة هدى", fu("f_huda_recall"), [G("ev_huda_form")], "huda", "NOTE_HUDA")
Act("a_note_adel", "examine", "اطلب نموذج إفادة عادل", fu("f_adel_recall"), [G("ev_adel_form")], "adel", "NOTE_ADEL")
Act("a_note_rana", "examine", "دوّن إفادة رنا", fu("f_rana_issue"), [G("ev_rana_statement")], "rana", "NOTE_RANA")
Act("p_custody_nabil", "present_evidence", "اعرض بطاقة العهدة على نبيل", {"presented": {"evidence_id": "ev_custody_card", "to_character": "nabil"}}, [{"op": "emit_event", "ref_id": "PRESENTED_CUSTODY"}], "nabil", "P_CUSTODY_NABIL", 0)
Act("a_hint", "request_hint", "اطلب تلميحاً", al, [], None, "REQUEST_HINT", 0)
Act("a_accuse", "final_accusation", "قدّم الاستنتاج النهائي", al, [{"op": "emit_event", "ref_id": "SUBMIT"}], None, "FINAL_ACCUSATION", 0)

topics = [
    {"id": "t_amount", "label_ar": "المبلغ المتنازع عليه", "example_questions_ar": ["ما المبلغ الذي تذكره؟", "كم دفعت أو كم سمعت؟"], "fact_ids": ["f_salem_paid", "f_nabil_recall", "f_huda_recall", "f_adel_recall"], "claim_ids": ["cl_nabil_pledge", "cl_huda_1500", "cl_adel_1500"]},
    {"id": "t_presence", "label_ar": "الحضور ورؤية الوصل", "example_questions_ar": ["هل حضرت التسليم؟", "متى رأيت الوصل أول مرة؟"], "fact_ids": ["f_huda_absent", "f_adel_absent"]},
    {"id": "t_issue", "label_ar": "إصدار الوصل وتقييده", "example_questions_ar": ["كيف أُصدر الوصل؟", "أين قُيّد؟"], "fact_ids": ["f_rana_issue", "f_ledger_exists", "f_deposit_exists", "f_handover_exists", "f_custody_exists"]},
    {"id": "t_compare", "label_ar": "المقارنة والفحص", "example_questions_ar": ["هل يمكن مقارنة الوصل بوصولات أخرى؟", "هل يُفحص الحبر؟"], "fact_ids": ["f_ten_exists", "f_exam_possible"]},
    {"id": "t_minutes", "label_ar": "محاضر المجلس", "example_questions_ar": ["أين محاضر الإحاطات؟"], "fact_ids": ["f_minutes_exist"]},
    {"id": "t_after", "label_ar": "ما جرى للوصل بعد تسلّمه", "example_questions_ar": ["هل غيّر أحد شيئاً في الوصل؟"], "fact_ids": ["f_nabil_wrote"]},
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
    (1, "في الوصل رقمان، لكن سطر الحروف يطابق حبر الدار، أما خانة الأرقام فحبرها وورقها مختلفان وتحتها أثر ضغط سابق؛ والوصولات العشرة من الدفتر نفسه لا يختلف فيها السطران.", ["ev_receipt", "ev_ink_note", "ev_ten_receipts"], "i_a_150"),
    (2, "سجل الصادر وإشعار الإيداع جهتان مختلفتان لم يمرّا بالوصل، وكلاهما يقول مائة وخمسين.", ["ev_ledger", "ev_deposit"], "i_b_150"),
    (3, "بطاقة العهدة تضبط التغيير: الخانة كانت 150 عند الإصدار وعند أول تسليم، وصارت 1500 حين عاد الوصل من ملف المجلس.", ["ev_custody_card", "ev_ledger"], "i_b_later"),
    (4, "الشاهدان أجابا بأنفسهما بأنهما لم يحضرا ولم يريا الوصل قبل الخلاف، وسجل الحضور وبطاقة العهدة يؤكدان ذلك من خارجهما.", ["ev_huda_form", "ev_adel_form", "ev_handover_log", "ev_custody_card"], "i_a_nofh"),
    (5, "الرقم الكبير تردد في ثلاث إحاطات متتالية على لسان عضو واحد وبحضورهما؛ فاتفاقهما أثر التكرار لا استقلال شهادتين.", ["ev_minutes"], "i_b_spread"),
    (6, "إذن لا حاجة لافتراض كذب: تفسير بسيط يجمع كل شيء، فالمبلغ مائة وخمسون، والرقم الأكبر أُضيف لاحقاً.", ["ev_ledger", "ev_custody_card"], "i_support_added"),
]
ending = {
    "steps": [{"order": o, "text_ar": t, "uses_evidence_ids": u, "inference_id": i} for o, t, u, i in steps],
    "alternative_paths_ar": [
        "يمكن الوصول إلى النتيجة من سجل الصادر وإشعار الإيداع وبطاقة العهدة وحدها دون فحص الحبر؛ ومن يفعل ذلك يبقى عليه أن يفسّر لماذا يتفق شاهدان على الرقم الآخر.",
        "ويمكن الوصول إليها من فحص الوصل نفسه ومقارنته بالدفتر ومن نموذجي الإفادة، لكن الأقوى أن يتفق المساران.",
    ],
    "what_evidence_could_not_show_ar": [
        "لا تثبت الأدلة من كتب الرقم بيده ولا لحظة كتابته بالدقيقة؛ تحصر الفترة فقط بين التسليم الأول والإعادة.",
        "لا تثبت الأدلة نية أحد؛ إقرار صاحب الرقم بأنه ظنّ أنه يصحح لا يقاس بدليل مادي.",
        "لا تنفي الأدلة أن المتبرع قال كلاماً آخر في حديث شفوي قبل التسليم؛ هي تنفي أن يكون المبلغ المدفوع غير مائة وخمسين.",
    ],
    "science_notes_ar": [
        "ذاكرة الشاهد تتشكّل بما يتكرر على مسامعه؛ قد يتذكر بثقة عالية شيئاً سمعه ولم يره، ولا يعني ذلك أنه يكذب.",
        "اتفاق شاهدين لا يعني استقلالهما: اسأل عن مصدر معرفة كل منهما قبل أن تعدّ الإفادتين دليلين.",
        "بطاقة العهدة (سلسلة العهدة) تتيح تتبّع من حمل الوثيقة ومتى وفي أي حالة؛ وتبقى نسبة الترجيح حكماً مبنياً على سجلات يمكن تتبعها.",
    ],
}
core = {
    "schema_version": "0.1.0", "case_id": CID, "case_version": "0.1.0",
    "meta": {"title_ar": "الوصل ذو الرقمين", "title_en": "The Receipt with Two Numbers", "age_band": "13-15", "locale": "ar", "dialogue_register": "msa", "estimated_minutes": 30, "difficulty": 2,
             "content_flags": ["no_violence", "fraud"], "authors": ["فريق أثر التحريري (مسودة بمساعدة الذكاء الاصطناعي، لم تُراجَع بشرياً بعد)"],
             "knowledge_object_refs": ["KO-RS-06-002", "KO-RS-06-004", "KO-RS-05-001", "KO-RS-05-004", "KO-RS-05-005", "KO-RS-05-002", "KO-RS-06-001", "KO-RS-06-009", "KO-RS-06-021"]},
    "premise": {"hook_ar": "وصل تبرع واحد يحمل رقمين، وشاهدان يتفقان على أحدهما بثقة. فهل اتفاقهما يكفي؟",
                "player_role_ar": "أنت متدرب في دار السِّجِل، وكلّفتك إدارة الدار بمراجعة وصل تبرع اعترض عليه المتبرع.",
                "setting_ar": "دار السِّجِل ومكتبة حيّ النخيل في القنطرة، خلال أيام معرض الكتاب. بإذن مكتوب من إدارة الدار ومجلس المكتبة تطّلع على الوصل وسجلاتهما فقط.",
                "public_fact_ids": ["f_dispute", "f_council_claims", "f_donor_recalls"],
                "assumed_general_knowledge_ar": ["الوصل الرسمي يُكتب مبلغه رقماً وحروفاً", "السجل الذي لا يمرّ بالوثيقة المتنازع عليها يصلح للمقارنة بها"]},
    "entities": {"characters": chars, "locations": locations, "objects": objects, "organizations": orgs},
    "truth": {"solution": {"culprit_ids": ["nabil"], "summary_ar": "لم يتبرع سالم إلا بمائة وخمسين ديناراً. الرقم الأكبر لم يكن جزءا من الوصل يوم صدوره؛ أضافه عضو المجلس بعد استلامه، ظنا منه أنه يصحح خطأ، دون نية خداع. والشاهدان صادقان في ما يذكران لكن علمهما مسموع لا مرئي.", "key_fact_ids": ["f_issued_150", "f_numeral_later", "f_no_firsthand", "f_figure_spread"]},
              "facts": facts, "claims": claims},
    "timeline": timeline, "evidence": ev, "evidence_graph": {"inferences": inf},
    "character_knowledge": ck, "hypotheses": hyps, "misdirection_plan": mis, "learning_objectives": los,
    "mechanics": {"time_budget_units": 40, "actions": A},
    "state_machine": {"id": "c014", "initial": "briefing", "type": "compound", "states": {
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
    "clock": {"epoch_hhmm": "09:00", "zone_label_ar": "توقيت الدار (يوم التسليم)"},
    "cover": {"title_ar": "الوصل ذو الرقمين", "tagline_ar": "شاهدان يتفقان بثقة… فهل يكفي أن يتفقا؟", "kicker_ar": "الملف الرابع عشر · مصدر المعرفة", "glyph": "✎", "accent": "amber"},
    "cold_open_ar": ["مساء اليوم الثالث لمعرض الكتاب.", "ظهرت لوحة شكر لمكتبة الحي بمبلغ كبير، فاعترض المتبرع: «هذا ليس ما دفعته».",
                     "المجلس يقول إن الوصل يحمل الرقم الكبير، وإن شاهدين من أعضائه يؤكدانه.",
                     "أمامك وصل وسجلات وإفادات. ابدأ بسؤال واحد عن كل إفادة: كيف عرف صاحبها؟"],
    "labs": [],
    "source_classes": [
        {"id": "primary_record", "label_ar": "سجل أصلي", "help_ar": "يُنتجه نظام أو شخص لحظة الحدث دون وسيط، كسجل صادر أو إشعار إيداع أو بطاقة عهدة."},
        {"id": "redisplay", "label_ar": "نسخة معروضة", "help_ar": "معلومة نُقلت من سجل آخر أو أُعيد عرضها."},
        {"id": "claim", "label_ar": "قول أو تصريح", "help_ar": "إفادة شخص؛ تُقاس بالسجلات لا بثقة صاحبها."},
        {"id": "template", "label_ar": "قالب أو نموذج", "help_ar": "نص جاهز لا يصف الحدث الفعلي بذاته."},
        {"id": "public_document", "label_ar": "وثيقة منشورة", "help_ar": "وثيقة معلنة ومعروف ناشرها."}],
    "limit_menu": [
        {"id": "l_who", "label_ar": "الأدلة لا تثبت من كتب الرقم الأكبر بيده ولا لحظة كتابته"},
        {"id": "l_oral", "label_ar": "الأدلة لا تنفي أن المتبرع قال كلاماً آخر في حديث شفوي لا سجل له"},
        {"id": "l_intent", "label_ar": "الأدلة لا تقيس نية من غيّر الخانة"},
        {"id": "l_invalid_confident", "label_ar": "ثقة الشاهدين الكبيرة في الرقم تدل على أنه صحيح"},
        {"id": "l_invalid_liar", "label_ar": "اتفاق الشاهدين يثبت أنهما كاذبان"}],
    "mind_change_menu": [
        {"id": "m_other_record", "label_ar": "ظهور سجل مستقل يضع المبلغ المدفوع ألفاً وخمسمائة"},
        {"id": "m_witness_saw", "label_ar": "ثبوت أن أحد الشاهدين حضر التسليم ورأى الوصل يوم صدوره"},
        {"id": "m_custody_wrong", "label_ar": "ثبوت أن بطاقة العهدة كُتبت بعد الخلاف لا في وقت التسليم"},
        {"id": "m_popular", "label_ar": "كثرة من يصدقون رواية المجلس"}],
    "skills": [{"skill_id": "KO-RS-05-001", "track": "B"}, {"skill_id": "KO-RS-05-004", "track": "B"}, {"skill_id": "KO-RS-05-005", "track": "B"}, {"skill_id": "KO-RS-06-002", "track": "D"}],
    "stage_hooks_ar": {"briefing": "رقمان على ورقة واحدة… وأيهما صدر أولاً؟", "investigating": "لا تعدّ الأصوات؛ اسأل من أين جاء كل صوت.", "review": "قبل أن تغلق الملف: ما الذي لا تعرفه؟", "resolved": "أُغلق ملف الوصل. في الأرشيف نسخة تحمل أثر مفتاح ما زال يبحث عن بابه."},
    "character_glyphs": {"salem": "س", "nabil": "ن", "huda": "هـ", "adel": "ع", "rana": "ر"},
}
sc = {
    "case_id": CID,
    "accepted_conclusions": {"h_added": {"grade": 1, "note_ar": "استنتاج متسق مع الأدلة ويتطلب ذكر حدوده."},
                             "h_large": {"grade": 0, "note_ar": "يعدّ اتفاق شاهدين مصدرهما واحد دليلاً مستقلاً ويتجاهل سجلين لم يمرّا بالوصل."},
                             "h_lie": {"grade": 0, "note_ar": "يقفز من الاتفاق إلى الكذب؛ التكرار يفسّر الاتفاق دون افتراض تواطؤ."}},
    "confidence_band": {"h_added": [65, 90], "h_large": [0, 15], "h_lie": [0, 15]},
    "source_key": {"ev_receipt": "primary_record", "ev_ink_note": "primary_record", "ev_ten_receipts": "primary_record", "ev_ledger": "primary_record", "ev_deposit": "primary_record",
                   "ev_custody_card": "primary_record", "ev_handover_log": "primary_record", "ev_minutes": "primary_record", "ev_stamp_check": "primary_record",
                   "ev_salem_statement": "claim", "ev_nabil_statement": "claim", "ev_huda_form": "claim", "ev_adel_form": "claim", "ev_rana_statement": "claim"},
    "link_key": {
        "h_added": {"ev_receipt": "supports", "ev_ink_note": "supports", "ev_ten_receipts": "supports", "ev_ledger": "supports", "ev_deposit": "supports", "ev_custody_card": "supports", "ev_handover_log": "supports", "ev_minutes": "supports", "ev_stamp_check": "neutral"},
        "h_large": {"ev_huda_form": "supports", "ev_stamp_check": "supports", "ev_ledger": "weakens", "ev_deposit": "weakens", "ev_ink_note": "weakens", "ev_custody_card": "weakens"},
        "h_lie": {"ev_huda_form": "weakens", "ev_adel_form": "weakens", "ev_minutes": "weakens", "ev_handover_log": "weakens"},
    },
    "required_limits": ["l_who", "l_oral"], "valid_mind_changers": ["m_other_record", "m_witness_saw", "m_custody_wrong"], "invalid_limits": ["l_invalid_confident", "l_invalid_liar"],
    "decisive_evidence": ["ev_ledger", "ev_deposit", "ev_custody_card", "ev_ink_note", "ev_handover_log"],
    "lab_requirement": None,
    "timeline_requirement": [{"evidence_id": "ev_handover_log", "utc_minute": 80, "tol": 15}, {"evidence_id": "ev_ledger", "utc_minute": 100, "tol": 15}, {"evidence_id": "ev_deposit", "utc_minute": 245, "tol": 15}],
    "refuted_hypotheses": ["h_large", "h_lie"],
    "criteria_map": {"c_source": "source_typing", "c_conflict": "conflict_resolution", "c_links": "hypothesis_links", "c_uncertainty": "uncertainty", "c_revision": "revision", "c_elimination": "elimination", "c_justification": "justification_human"},
    "caps": {"no_citations_max": 45, "no_conflict_resolution_max": 70},
}
os.makedirs(OUT, exist_ok=True)
for suf, obj in [("", core), (".ui", ui), (".scoring", sc)]:
    with open(os.path.join(OUT, f"{CID}{suf}.json"), "w", encoding="utf8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
print("ok")
