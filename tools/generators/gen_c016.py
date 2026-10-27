#!/usr/bin/env python3
# Case c016 «الصندوق تحت شجيرة الفل» — from seed S-06 (HS-025-inspired "follow the registers"), ADAPTED to a harmless analogue.
# Seed deviations (documented): the rare plant is a fictional ornamental jasmine cultivar (NOT castor, which is a toxic-seed plant);
# the ending is a misplacement, not a theft: the school gardener moved the buried box while preparing a cutting that a nursery customer
# had ordered, handed it to the office, and nobody told the club. The seed's trap (the customer "knew the place") is kept as a red herring.
# No-culprit convention: the gardener who moved the box (good faith) is recorded in culprit_ids. Records are opened only with written permission.
# Usage: gen_c016.py OUT_DIR
import json, sys, os
OUT = sys.argv[1]
CID = "c016_garden_box"

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
ch("jamil", "جميل العلي", "suspect", "بستاني المدرسة",
   "هادئ وكثير العمل قليل الكتابة، يدوّن أعماله بإيجاز، ويفترض أن الإدارة تتولى إبلاغ أصحاب الأشياء.",
   ["أن تبقى الحديقة سليمة", "ألا يُظنّ أنه أخذ شيئاً ليس له"],
   [L("jm_greet", "greeting", "أهلاً. أنا أعمل في الحديقة منذ سنوات، واسألني عمّا عملته."),
    L("jm_dug", "reveal", "حفرت يوم الخميس حول جذع شجيرة الفل مع فني المشتل لقص العقلة، ثم رددت التربة وسوّيتها.", ["f_jamil_dug"]),
    L("jm_refuse", "refuse_secret", "لا أذكر شيئاً آخر مما وجدته."),
    L("jm_box", "reveal", "نعم... ظهر عند الجذع صندوق معدني عليه ملصق، فظننت أن أحداً نسيه مدفوناً وسلمته لمكتب الإدارة نحو 10:25، ولم أدوّنه في سجلي.", ["f_jamil_found"]),
    L("jm_claim", "reveal", "ظننت أن المكتب سيبلغ صاحبه، فهذا عمل الإدارة.", None, ["cl_jamil_assumed"]),
    L("jm_unknown", "deflect_unknown", "لا أعرف."),
    L("jm_off", "deflect_offtopic", "اسألني عن الحديقة وعن الشجيرة."),
    L("jm_bye", "farewell", "كان ينبغي أن أكتب كل شيء في سجلي.")])
ch("sanaa", "سناء الراشد", "witness", "موظفة مكتب إدارة المدرسة",
   "منظمة وتحترم الإجراءات، تدوّن كل ما يُسلَّم إلى المكتب وتنتظر أن يسأل عنه أصحابه.",
   ["أن تبقى سجلات المفقودات سليمة", "ألا تُلام على انتظار صاحب الصندوق"],
   [L("sn_greet", "greeting", "تفضّل. كل ما يُسلَّم إلى المكتب أدوّنه في سجل المفقودات."),
    L("sn_recv", "reveal", "استلمت من جميل نحو 10:25 صندوقاً معدنياً صغيراً، دوّنته في السجل ووضعته في الخزنة دون أن أفتحه.", ["f_sanaa_received"]),
    L("sn_label", "reveal", "على الملصق حرفان فقط، فلم أعرف صاحبه، وانتظرت أن يسأل عنه أحد.", ["f_sanaa_label"]),
    L("sn_unknown", "deflect_unknown", "لا أعرف أكثر مما دوّنته."),
    L("sn_off", "deflect_offtopic", "اسألني عن سجل المفقودات."),
    L("sn_bye", "farewell", "سنضيف خطوة إبلاغ للمشرفين بعد هذا.")])
ch("thaer", "ثائر الحداد", "suspect", "ولي أمر طلب عقلة من المشتل",
   "ودود ويحب الحدائق، لا يعرف شيئاً عن النادي ولا عن الصندوق، ويتضايق حين يُظنّ أنه دخل المدرسة.",
   ["أن يحصل على عقلته", "ألا يُتّهم بما لا علاقة له به"],
   [L("th_greet", "greeting", "أنا طلبت عقلة فقط. ما علاقتي بصندوق؟"),
    L("th_order", "reveal", "طلبت عقلة من فل الفجر لحديقة بيتي، وتسلمتها من المشتل نحو 11:30 ووقعت على الاستلام.", ["f_thaer_order"]),
    L("th_off_site", "reveal", "لم أدخل المدرسة هذا الأسبوع إطلاقاً، فالقص يتم عند المدرسة وأنا أتسلم من المشتل.", ["f_thaer_offsite"]),
    L("th_unknown", "deflect_unknown", "لا أعرف شيئاً عن ذلك."),
    L("th_off", "deflect_offtopic", "اسألني عن العقلة فقط."),
    L("th_bye", "farewell", "أتمنى أن يُعثر على الصندوق.")])
ch("ghassan", "غسان الفارس", "witness", "أمين صندوق نادي البيئة (طالب)",
   "حريص على أموال الرحلة ومتأثر لضياعها، يميل إلى الظن بأن أحداً عرف الموضع وسرق، ويصحح ظنه إذا واجهته بسجل.",
   ["أن تعود أموال الرحلة", "أن يعرف النادي ما جرى"],
   [L("gh_greet", "greeting", "أهلاً. أنا أمين الصندوق، والصندوق ضاع من تحت الشجيرة."),
    L("gh_buried", "reveal", "دفنّا الصندوق يوم الاثنين عند جذع الشجيرة بعد عدّ المال، ولا يعرف الموضع غير ثلاثة منا.", ["f_club_buried"]),
    L("gh_claim", "reveal", "التربة مقلوبة والصندوق غير موجود؛ فمن المؤكد أن أحداً عرف الموضع وسرقه.", None, ["cl_ghassan_theft"]),
    L("gh_unknown", "deflect_unknown", "لا أعرف ما جرى بعد دفننا له."),
    L("gh_off", "deflect_offtopic", "اسألني عن الصندوق وما فيه."),
    L("gh_bye", "farewell", "أريد أن أعرف أين المال.")])
ch("maha", "مها القاسم", "expert", "منسقة طلبات مشتل الندى",
   "دقيقة ومنظمة، تشرح كيف يُباع هذا الصنف وكيف تُقص عقلته، ولا تعرف شيئاً عن النادي.",
   ["أن يُفهم نظام الطلبات المسبقة", "أن تبقى سجلات المشتل سليمة"],
   [L("mh_greet", "greeting", "تفضّل. أستطيع أن أشرح كيف نبيع هذا الصنف، لا أكثر."),
    L("mh_process", "reveal", "فل الفجر لا يُباع إلا بطلب مسبق، ونقص عقلته من النبتة الأم في حديقة المدرسة بموجب اتفاق مع الإدارة، ولا يدخل الحديقة غير فني المشتل والبستاني.", ["f_maha_process"]),
    L("mh_records", "reveal", "نسجل كل طلب وكل محطة توصيل واستلام، ولدينا نسخة بإذن من الإدارة.", ["f_order_exists", "f_delivery_exists"]),
    L("mh_unknown", "deflect_unknown", "هذا خارج ما أعرفه."),
    L("mh_off", "deflect_offtopic", "اسألني عن الطلبات والتوصيل."),
    L("mh_bye", "farewell", "السجل يجيب أفضل مني.")])

locations = [{"id": "loc_garden", "name_ar": "حديقة المدرسة", "description_ar": "فيها شجيرة فل الفجر، النبتة الأم الوحيدة في المنطقة."},
             {"id": "loc_office", "name_ar": "إدارة المدرسة", "description_ar": "فيها سجل المفقودات والخزنة."},
             {"id": "loc_gate", "name_ar": "بوابة المدرسة", "description_ar": "سجل الدخول والخروج."},
             {"id": "loc_nursery", "name_ar": "مشتل الندى", "description_ar": "مشتل يبيع النبتة بطلب مسبق ويحتفظ بسجل طلباته وتوصيله."},
             {"id": "loc_clubroom", "name_ar": "غرفة نادي البيئة", "description_ar": "مدونة النادي وسجل أنشطته."}]
objects = [{"id": "obj_box", "name_ar": "صندوق رحلة نادي البيئة", "description_ar": "صندوق معدني صغير بقفل، عليه ملصق بحرفين."},
           {"id": "obj_shrub", "name_ar": "شجيرة فل الفجر", "description_ar": "نبتة زينة نادرة (نوع خيالي) في حديقة المدرسة، لا تُباع إلا من مشتل الندى."}]
orgs = [{"id": "org_school", "name_ar": "ثانوية الأطلال", "description_ar": "مدرسة خيالية فيها نادي للبيئة."},
        {"id": "org_nursery", "name_ar": "مشتل الندى", "description_ar": "مشتل خيالي يبيع نبتة نادرة بطلب مسبق."}]

# ---------------------------------------------------------------- facts
facts = []
def F(id, st, kind, subj, spoiler, time=None, loc=None, ko=None):
    d = {"id": id, "statement_ar": st, "kind": kind, "subject_ids": subj, "spoiler_level": spoiler}
    if time: d["time"] = time
    if loc: d["location_id"] = loc
    if ko: d["science_ko_refs"] = ko
    facts.append(d)
F("f_box_missing", "وجد نادي البيئة موضع الدفن عند جذع الشجيرة مردوماً والصندوق غير موجود صباح الجمعة.", "event", ["obj_box", "obj_shrub", "ghassan"], 0, T(1500), "loc_garden")
F("f_no_witness", "لا شهود على ما جرى، ولا أثر لكسر في السور أو البوابة.", "state", ["loc_garden"], 0)
F("f_rare_plant", "الشجيرة نبتة نادرة لا يبيعها إلا مشتل الندى وبطلب مسبق.", "attribute", ["obj_shrub", "org_nursery"], 0)
F("f_club_buried", "دفن النادي الصندوق يوم الاثنين عند جذع الشجيرة بعد عدّ المال، ولا يعرف الموضع غير ثلاثة أعضاء.", "event", ["ghassan", "obj_box"], 1, None, "loc_garden")
F("f_jamil_dug", "حفر البستاني مع فني المشتل حول جذع الشجيرة يوم الخميس لقص عقلة ثم ردّ التربة.", "event", ["jamil", "obj_shrub"], 1, T(100, "exact", 130), "loc_garden")
F("f_jamil_found", "وجد البستاني عند الجذع صندوقاً معدنياً مدفوناً، فظنه منسياً وسلّمه لمكتب الإدارة نحو 10:25.", "event", ["jamil", "obj_box"], 3, T(145, "approx"), "loc_office", ["KO-RS-05-005"])
F("f_sanaa_received", "استلمت موظفة المكتب الصندوق نحو 10:25 ودوّنته في سجل المفقودات ووضعته في الخزنة دون فتحه.", "event", ["sanaa", "obj_box"], 1, T(145, "approx"), "loc_office")
F("f_sanaa_label", "الملصق على الصندوق حرفان فقط، فلم تعرف الموظفة صاحبه وانتظرت أن يسأل عنه أحد.", "state", ["sanaa", "obj_box"], 1, None, "loc_office")
F("f_thaer_order", "طلب ثائر عقلة من الصنف نفسه وتسلمها من المشتل نحو 11:30 ووقّع على الاستلام.", "event", ["thaer", "org_nursery"], 1, T(210, "approx"), "loc_nursery")
F("f_thaer_offsite", "يقول ثائر إنه لم يدخل المدرسة هذا الأسبوع، وإن القص يتم عند المدرسة بيد فني المشتل.", "attribute", ["thaer"], 1)
F("f_maha_process", "يُقص هذا الصنف من النبتة الأم في حديقة المدرسة بموجب اتفاق، ولا يدخل الحديقة غير فني المشتل والبستاني.", "state", ["maha", "org_nursery", "obj_shrub"], 1, None, "loc_nursery")
F("f_order_exists", "للمشتل سجل طلبات يحفظ كل طلب ومكان القص وموعده.", "state", ["org_nursery"], 1, None, "loc_nursery")
F("f_delivery_exists", "للمشتل قائمة توصيل واستلام تحفظ كل محطة ووقتها وتوقيع المستلم.", "state", ["org_nursery"], 1, None, "loc_nursery")
F("f_dug_thursday", "جرى حفر عند أصل الشجيرة صباح الخميس لقص عقلة طُلبت من المشتل، وهذا ما يفسّر الموضع المقلوب.", "relation", ["obj_shrub", "jamil"], 3, T(100, "exact", 130), "loc_garden", ["KO-RS-05-005", "KO-RS-06-004"])
F("f_box_in_office", "الصندوق ومعه المال كاملاً في خزنة إدارة المدرسة منذ الخميس 10:25 بعد أن سلّمه البستاني، ولم يُبلَّغ النادي.", "relation", ["obj_box", "jamil", "sanaa"], 3, T(145, "exact", 1500), "loc_office", ["KO-RS-05-005", "KO-RS-06-001"])
F("f_buyer_off_site", "طالب العقلة لم يدخل المدرسة، وتسلم عقلته من المشتل بعد انتهاء القص.", "relation", ["thaer"], 3, T(130, "exact", 210), None, ["KO-RS-06-001", "KO-RS-06-004"])

claims = [
    {"id": "cl_ghassan_theft", "statement_ar": "التربة مقلوبة والصندوق غير موجود، فمن المؤكد أن أحداً عرف الموضع وسرقه.", "kind": "honest_mistake", "held_by": ["ghassan"], "true_fact_id": "f_box_in_office", "contradicted_by_evidence_ids": ["ev_office_ledger", "ev_count_slip", "ev_clerk_statement"]},
    {"id": "cl_jamil_assumed", "statement_ar": "المكتب سيبلغ صاحب الصندوق، فهذا عمل الإدارة.", "kind": "honest_mistake", "held_by": ["jamil"], "true_fact_id": "f_box_in_office", "contradicted_by_evidence_ids": ["ev_office_ledger"]},
]
timeline = [
    {"id": "te_van", "description_ar": "شاحنة المشتل تدخل البوابة.", "time": T(90), "location_id": "loc_gate", "actor_ids": [], "fact_ids": ["f_maha_process"]},
    {"id": "te_dig", "description_ar": "البستاني وفني المشتل يحفران حول جذع الشجيرة لقص العقلة ثم يردّان التربة.", "time": T(100, "exact", 130), "location_id": "loc_garden", "actor_ids": ["jamil"], "fact_ids": ["f_jamil_dug", "f_dug_thursday"], "motivated_by_ar": "طلب المشتل قص عقلة من النبتة الأم"},
    {"id": "te_box", "description_ar": "البستاني يسلّم الصندوق لموظفة المكتب، وتدوّنه في سجل المفقودات.", "time": T(145, "approx"), "location_id": "loc_office", "actor_ids": ["jamil", "sanaa"], "fact_ids": ["f_jamil_found", "f_sanaa_received", "f_box_in_office"], "motivated_by_ar": "ظنّ الصندوق منسياً فسلّمه لمن يحفظ المفقودات"},
    {"id": "te_pickup", "description_ar": "ثائر يتسلم عقلته من المشتل ويوقّع.", "time": T(210, "approx"), "location_id": "loc_nursery", "actor_ids": ["thaer"], "fact_ids": ["f_thaer_order", "f_buyer_off_site"], "motivated_by_ar": "أراد غرس العقلة في حديقة بيته"},
    {"id": "te_club_visit", "description_ar": "النادي يزور الموضع فيجده مردوماً والصندوق غير موجود.", "time": T(1500), "location_id": "loc_garden", "actor_ids": ["ghassan"], "fact_ids": ["f_box_missing"], "motivated_by_ar": "أراد النادي تفقد صندوق الرحلة قبل الرحلة"},
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
V("ev_club_note", "مدونة نادي البيئة", "documentary",
  "مدونة نادي البيئة — ثانوية الأطلال\nالاثنين: دفنّا صندوق نقود الرحلة (340 ديناراً بعد عدّها بحضور المشرفة) عند جذع شجيرة فل الفجر في حديقة المدرسة. على الصندوق ملصق بالحرفين «ن.ب» فقط. يعرف الموضع: غسان ولين وسلمان.\nالجمعة 09:00: فتحنا الموضع فوجدنا التربة مقلوبة والصندوق غير موجود.",
  ["a_get_club"], ["f_club_buried", "f_box_missing"], "moderate",
  "مدونة النادي نفسه؛ تثبت ما دفنه وما وجده، ولا تبيّن ما جرى بين اليومين.", loc="loc_clubroom")
V("ev_hole_note", "محضر معاينة الموضع", "observation",
  "محضر مشرفة النادي، الجمعة 09:20:\nالتربة حول جذع الشجيرة مقلوبة وأُعيد ردمها وتسويتها، والصندوق غير موجود. لا أثر لكسر في السور أو قفل البوابة.",
  ["a_get_hole"], ["f_box_missing", "f_no_witness"], "moderate",
  "يصف حال الموضع يوم الجمعة فقط؛ لا يبيّن متى قُلبت التربة ولا من فعل ذلك.", red=True, loc="loc_garden")
V("ev_nursery_orders", "سجل طلبات مشتل الندى", "documentary",
  "سجل طلبات مشتل الندى (نسخة بإذن من إدارة المدرسة)\nالطلب 311: فل الفجر — عُقلة واحدة — الطالب: ثائر الحداد\nمكان القص: النبتة الأم في حديقة ثانوية الأطلال بموجب اتفاق مع الإدارة\nموعد القص: الخميس 09:40 | الاستلام: من المشتل بعد القص",
  ["a_get_orders"], ["f_dug_thursday", "f_buyer_off_site", "f_thaer_order"], "strong",
  "يثبت من طلب العقلة وأين ومتى تُقص ومن أين تُستلم؛ لا يبيّن من حضر القص فعلاً.", red=True, loc="loc_nursery")
V("ev_delivery_list", "قائمة توصيل واستلام المشتل", "documentary",
  "قائمة توصيل واستلام مشتل الندى — الخميس\nالمحطة 3: ثانوية الأطلال — دخول الحديقة 09:40 — قص عقلة للطلب 311 — الانتهاء 10:10\nالمحطة 5: المشتل — تسليم عقلة الطلب 311 للطالب ثائر الحداد 11:30 — توقيع المستلم: ث. الحداد",
  ["a_get_delivery"], ["f_dug_thursday", "f_buyer_off_site", "f_thaer_order"], "strong",
  "تثبت مواعيد المحطات وتوقيع المستلم في المشتل؛ لا تبيّن ما وُجد في التربة ولا من كان في الحديقة غير فني المشتل.", loc="loc_nursery")
V("ev_gardener_log", "سجل أعمال البستاني", "documentary",
  "سجل أعمال البستاني جميل العلي — الخميس\n09:40 إلى 10:10: حفر حول جذع شجيرة الفل بالتعاون مع فني المشتل لقص عقلة، ثم رد التربة وتسويتها.\n10:30: سقي العشب أمام المبنى.",
  ["a_get_gardener_log"], ["f_dug_thursday", "f_jamil_dug"], "moderate",
  "سجل مقتضب بخط صاحبه؛ يثبت أعماله المدوّنة ولا يذكر كل ما حدث أثناءها.", loc="loc_garden")
V("ev_gate_log", "سجل بوابة المدرسة", "documentary",
  "سجل بوابة المدرسة — الخميس\n09:30 دخول: شاحنة مشتل الندى (الفني: ماهر)\n10:32 خروج: شاحنة مشتل الندى\nلا زوار غير المعتادين بين 08:00 و12:00، ولا اسم «ثائر الحداد» في سجل الزوار.",
  ["a_get_gate"], ["f_dug_thursday", "f_buyer_off_site"], "strong",
  "يسجل ما مرّ من البوابة الرئيسية؛ لا يرى من يدخل من منفذ آخر ولا يبيّن ما فعله الداخل.", loc="loc_gate")
V("ev_office_ledger", "سجل المفقودات في إدارة المدرسة", "documentary",
  "سجل المفقودات — إدارة ثانوية الأطلال\nالخميس 10:25: صندوق معدني صغير بقفل، ملصق «ن.ب»، سلّمه البستاني جميل العلي، وجده مدفوناً عند جذع شجيرة في الحديقة.\nالحالة: محفوظ في خزنة الإدارة.\nإبلاغ صاحبه: لم يُبلَّغ بعد (لا اسم كامل على الملصق).\nالموظفة: سناء الراشد",
  ["a_get_ledger"], ["f_box_in_office"], "strong",
  "يثبت أن الصندوق سُلّم وحُفظ، لا ما في داخله ولا هل هو صندوق النادي بعينه؛ ذلك تحسمه ورقة العدّ.",
  contradicts=["cl_ghassan_theft", "cl_jamil_assumed"], loc="loc_office")
V("ev_count_slip", "ورقة عدّ المحتويات", "documentary",
  "ورقة عدّ — إدارة ثانوية الأطلال، الجمعة 11:00\nفُتح الصندوق في حضور مشرفة النادي وموظفة المكتب.\nالعدّ: 340 ديناراً، مطابق لقيد النادي.\nلا نقص ولا زيادة.",
  ["a_get_count"], ["f_box_in_office"], "strong",
  "تثبت المبلغ عند الفتح يوم الجمعة وتطابقه مع قيد النادي؛ ولا تبيّن بنفسها متى دخل الصندوق الخزنة.", contradicts=["cl_ghassan_theft"], loc="loc_office")
V("ev_gardener_statement", "إفادة جميل العلي (ملخص)", "testimonial",
  "ملخص إفادة جميل العلي:\n«حفرت مع فني المشتل حول جذع الفل لقص العقلة، فظهر صندوق معدني عليه ملصق، فظننت أن أحداً نسيه مدفوناً وسلمته إلى المكتب نحو 10:25. ظننت أن المكتب سيبلغ صاحبه، ولم أدوّنه في سجلي.»",
  ["a_note_gardener"], ["f_jamil_found", "f_jamil_dug"], "moderate",
  "إفادة صاحب الشأن عن فعله؛ تؤيدها سجلات المكتب والمشتل ولا تغني عنها.", loc="loc_garden")
V("ev_clerk_statement", "إفادة سناء الراشد (ملخص)", "testimonial",
  "ملخص إفادة سناء الراشد:\n«استلمت الصندوق من جميل نحو 10:25، ودوّنته في سجل المفقودات، ووضعته في الخزنة دون أن أفتحه. لم أعرف صاحبه لأن الملصق حرفان فقط، وانتظرت أن يسأل عنه أحد.»",
  ["a_note_clerk"], ["f_sanaa_received", "f_sanaa_label"], "moderate",
  "إفادة موظفة المكتب عن ما استلمته؛ ولا تعرف ما جرى للصندوق قبل تسليمه.", contradicts=["cl_ghassan_theft"], loc="loc_office")
V("ev_buyer_statement", "إفادة ثائر الحداد (ملخص)", "testimonial",
  "ملخص إفادة ثائر الحداد:\n«طلبت عقلة من فل الفجر لحديقة بيتي وتسلمتها من المشتل نحو 11:30 ووقعت. لم أدخل المدرسة هذا الأسبوع، ولا أعرف شيئاً عن صندوق.»",
  ["a_note_buyer"], ["f_thaer_order", "f_thaer_offsite"], "weak",
  "إفادة من وُجّهت إليه الشبهة؛ تؤيدها قائمة المشتل وسجل البوابة ولا تغني عنهما.", loc="loc_nursery")
V("ev_ghassan_statement", "إفادة غسان الفارس (ملخص)", "testimonial",
  "ملخص إفادة غسان الفارس، أمين صندوق النادي:\n«دفنّا الصندوق يوم الاثنين بعد عدّ المال، ولا يعرف الموضع غير ثلاثة منا. وجدنا الجمعة التربة مقلوبة والصندوق غير موجود، فظننت أن أحداً عرف الموضع وسرقه.»",
  ["a_note_ghassan"], ["f_club_buried"], "weak",
  "إفادة متضرر يفسّر ما رآه بظن؛ الظن يُقاس بالسجلات.", loc="loc_clubroom")
V("ev_maha_statement", "إفادة مها القاسم (ملخص)", "testimonial",
  "ملخص إفادة مها القاسم، منسقة طلبات المشتل:\n«هذا الصنف لا يُباع إلا بطلب مسبق، ونقص عقلته من النبتة الأم في حديقة المدرسة بموجب اتفاق مع الإدارة، ولا يدخل الحديقة غير فني المشتل والبستاني.»",
  ["a_note_maha"], ["f_maha_process"], "moderate",
  "تصف نظام المشتل لا ما جرى يوم الخميس.", loc="loc_nursery")

# ---------------------------------------------------------------- inferences
def P(t, i): return {"ref_type": t, "ref_id": i}
inf = []
def I(id, prem, ct, concl, rel, strength, rule, ks):
    inf.append({"id": id, "premises": prem, "conclusion": {"ref_type": ct, "ref_id": concl}, "relation": rel, "strength": strength, "rule_ar": rule, "skill_ko_refs": ks})
# path A: the nursery's and the office's own records
I("i_a_dug", [P("evidence", "ev_nursery_orders"), P("evidence", "ev_delivery_list")], "fact", "f_dug_thursday", "establishes", "strong",
  "الطلب 311 يحدد قص العقلة من النبتة الأم في المدرسة الخميس 09:40، وقائمة التوصيل تثبت دخول الحديقة 09:40 والانتهاء 10:10؛ فالحفر حول الجذع صباح الخميس له سبب مسجل.", ["KO-RS-05-005", "KO-RS-06-004"])
I("i_a_box", [P("evidence", "ev_office_ledger"), P("evidence", "ev_count_slip")], "fact", "f_box_in_office", "establishes", "strong",
  "سجل المفقودات يقيّد صندوقاً مدفوناً سلّمه البستاني الخميس 10:25 وحُفظ في الخزنة، وورقة العدّ تُظهر المبلغ كاملاً مطابقاً لقيد النادي؛ فهو صندوق النادي ولم يُمسّ.", ["KO-RS-05-005", "KO-RS-06-001"])
I("i_a_buyer", [P("evidence", "ev_delivery_list"), P("evidence", "ev_nursery_orders")], "fact", "f_buyer_off_site", "establishes", "strong",
  "الطلب ينص على أن الاستلام من المشتل بعد القص، والقائمة تسجل توقيع ثائر في المشتل 11:30 بعد انتهاء محطة المدرسة 10:10؛ فلا حاجة لحضوره الحديقة ولا دليل عليه.", ["KO-RS-06-001", "KO-RS-06-004"])
# path B: the gardener's log, the gate, and people's own accounts
I("i_b_dug", [P("evidence", "ev_gardener_log"), P("evidence", "ev_gate_log")], "fact", "f_dug_thursday", "establishes", "strong",
  "البستاني دوّن حفره حول الجذع 09:40 إلى 10:10 لقص عقلة، وسجل البوابة يضع دخول شاحنة المشتل 09:30؛ فالتربة قُلبت الخميس بسبب القص.", ["KO-RS-05-005", "KO-RS-06-004"])
I("i_b_box", [P("evidence", "ev_gardener_statement"), P("evidence", "ev_clerk_statement")], "fact", "f_box_in_office", "establishes", "strong",
  "البستاني يقول إنه سلّم الصندوق، والموظفة تقول إنها استلمته 10:25 وحفظته دون فتحه؛ روايتان من شخصين مستقلين تتفقان في الوقت والمكان والفعل.", ["KO-RS-05-004", "KO-RS-05-005"])
I("i_b_buyer", [P("evidence", "ev_gate_log"), P("evidence", "ev_buyer_statement")], "fact", "f_buyer_off_site", "establishes", "strong",
  "سجل البوابة لا يحتوي اسمه بين الزوار، وهو يقول إنه لم يدخل المدرسة؛ والاثنان لا يمرّان بسجلات المشتل.", ["KO-RS-06-001", "KO-RS-05-007"])
# hypothesis ledger
I("i_support_jamil", [P("fact", "f_dug_thursday"), P("fact", "f_box_in_office")], "hypothesis", "h_gardener", "supports", "strong",
  "الحفر الخميس له سبب مسجل، والصندوق في خزنة الإدارة منذ الخميس بمبلغه كاملاً؛ فأبسط تفسير أن البستاني وجده أثناء الحفر ونقله إلى المكتب ولم يبلَّغ النادي.", ["KO-RS-06-001"])
I("i_rule_theft", [P("fact", "f_box_in_office")], "hypothesis", "h_theft", "rules_out", "conclusive",
  "إذا كان الصندوق ومعه المال كاملاً محفوظاً في الخزنة فلم يُسرق منه شيء.", ["KO-RS-06-008"])
I("i_rule_buyer", [P("fact", "f_buyer_off_site"), P("fact", "f_box_in_office")], "hypothesis", "h_buyer", "rules_out", "conclusive",
  "من لم يدخل الحديقة لا يصح أن يكون هو من حمل الصندوق، والصندوق وُجد وحُفظ بلا نقص؛ فمعرفة موضع الشجيرة بسبب الطلب لا تدل على فعل.", ["KO-RS-06-008"])
I("i_rule_member", [P("fact", "f_box_in_office"), P("fact", "f_dug_thursday")], "hypothesis", "h_member", "rules_out", "strong",
  "الصندوق بقي في موضعه حتى حُفر الخميس ثم صار في خزنة الإدارة بمبلغه كاملاً؛ فلم يأخذه عضو من النادي ولا حاجة لافتراض ذلك.", ["KO-RS-06-008"])
I("i_claim_ghassan", [P("fact", "f_box_in_office"), P("fact", "f_dug_thursday")], "claim", "cl_ghassan_theft", "contradicts_claim", "strong",
  "التربة المقلوبة لها سبب مسجل غير السرقة، والصندوق سليم في الخزنة؛ فالاستنتاج من الموضع الفارغ إلى السرقة قفز فوق التفسير الأبسط.", ["KO-RS-05-001", "KO-RS-06-004"])
I("i_claim_jamil", [P("evidence", "ev_office_ledger")], "claim", "cl_jamil_assumed", "contradicts_claim", "strong",
  "سجل المفقودات يقول إن صاحب الصندوق لم يُبلَّغ بعد؛ فالافتراض أن المكتب سيبلغه لم يتحقق.", ["KO-RS-05-014"])

# ---------------------------------------------------------------- character knowledge
K = lambda f, a="witnessed", c="certain": {"fact_id": f, "access": a, "certainty": c}
ck = [
    {"character_id": "jamil", "knows": [K("f_jamil_dug")],
     "hides": [{"fact_id": "f_jamil_found", "reveal_when": {"presented": {"evidence_id": "ev_gardener_log", "to_character": "jamil"}}, "cover_claim_id": None, "reveal_line_id": "jm_box"}],
     "believes": [{"claim_id": "cl_jamil_assumed", "stance": "sincere"}]},
    {"character_id": "sanaa", "knows": [K("f_sanaa_received"), K("f_sanaa_label")], "hides": [], "believes": []},
    {"character_id": "thaer", "knows": [K("f_thaer_order"), K("f_thaer_offsite")], "hides": [], "believes": []},
    {"character_id": "ghassan", "knows": [K("f_club_buried")], "hides": [], "believes": [{"claim_id": "cl_ghassan_theft", "stance": "sincere"}]},
    {"character_id": "maha", "knows": [K("f_maha_process", "professional"), K("f_order_exists", "professional"), K("f_delivery_exists", "professional")], "hides": [], "believes": []},
]
hyps = [
    {"id": "h_gardener", "statement_ar": "وجد البستاني الصندوق أثناء الحفر لقص العقلة فنقله إلى مكتب الإدارة ولم يُبلَّغ النادي.", "is_true": True, "plausibility_at_start": "low", "suspect_id": "jamil"},
    {"id": "h_buyer", "statement_ar": "ثائر الذي طلب العقلة عرف موضع الشجيرة حين جاء ليأخذها، فأخذ الصندوق.", "is_true": False, "plausibility_at_start": "high", "suspect_id": "thaer"},
    {"id": "h_member", "statement_ar": "أخذ أحد الأعضاء الثلاثة الذين يعرفون الموضع الصندوق.", "is_true": False, "plausibility_at_start": "medium", "suspect_id": "ghassan"},
    {"id": "h_theft", "statement_ar": "سرق شخص مجهول من خارج المدرسة الصندوق ومعه المال.", "is_true": False, "plausibility_at_start": "medium"},
]
mis = [
    {"id": "rh_order", "points_to_hypothesis_id": "h_buyer", "planted_via_ar": "شخص طلب عقلة من النبتة نفسها هذا الموسم، فيبدو أنه كان يعرف المكان.", "evidence_ids": ["ev_nursery_orders"],
     "refuted_by_inference_ids": ["i_rule_buyer", "i_a_buyer", "i_b_buyer"],
     "fairness_note_ar": "الطلب نفسه يقول إن القص من النبتة الأم بيد فني المشتل وإن الاستلام من المشتل، وقائمة التوصيل وسجل البوابة تضعان الطالب خارج المدرسة؛ فمعرفة موضع النبتة لا تدل على دخوله."},
    {"id": "rh_hole", "points_to_hypothesis_id": "h_member", "planted_via_ar": "الموضع مقلوب والصندوق غير موجود ولا شهود، فيبدو أن أحداً من العارفين بالموضع أخذه.", "evidence_ids": ["ev_hole_note"],
     "refuted_by_inference_ids": ["i_rule_member", "i_rule_theft", "i_claim_ghassan", "i_a_dug", "i_b_dug"],
     "fairness_note_ar": "المحضر يصف حال الموضع يوم الجمعة فقط؛ وسجلات الحفر ليوم الخميس وسجل المفقودات يفسّران قلب التربة واختفاء الصندوق دون سرقة."},
]
los = [
    {"id": "lo_claim", "statement_ar": "يفرّق بين الظن الذي يفسّر موضعاً فارغاً والسجل الذي يبيّن ما جرى، ويقيس القول بسجل.", "skill_ko_ref": "KO-RS-05-001", "observable_behaviors_ar": ["يصنّف الإفادات أقوالاً", "لا يعدّ الموضع الفارغ دليلاً على سرقة"], "evidence_sources": ["evidence_board"]},
    {"id": "lo_timeline", "statement_ar": "يرتّب سجلات الطلب والتوصيل والحفر والتسليم على خط زمني واحد.", "skill_ko_ref": "KO-RS-05-005", "observable_behaviors_ar": ["يضع الدفن والحفر والتسليم والاكتشاف في أزمنتها"], "evidence_sources": ["timeline_task", "action_log"]},
    {"id": "lo_hyp", "statement_ar": "يوازن بين عدة فرضيات ويستبعد ما تنقضه الأدلة، ويطلب الاختبار الذي يميّز بينها.", "skill_ko_ref": "KO-RS-05-003", "observable_behaviors_ar": ["يضيف فرضيات", "يستبعد بدليل", "يختار السجل الذي يفرّق بين فرضيتين"], "evidence_sources": ["hypothesis_ledger"]},
    {"id": "lo_diag", "statement_ar": "يقدّر ما يثبته كل سجل وما لا يثبته، ويربط الدليل بالفرضية باتجاه صحيح.", "skill_ko_ref": "KO-RS-06-001", "observable_behaviors_ar": ["لا يحوّل معرفة المكان إلى دليل فعل", "يربط الدليل بالفرضية"], "evidence_sources": ["evidence_board", "final_justification"]},
    {"id": "lo_calib", "statement_ar": "يصوغ نسبة الترجيح بحدودها.", "skill_ko_ref": "KO-RS-06-021", "observable_behaviors_ar": ["يختار ثقة معقولة", "يذكر حدوداً"], "evidence_sources": ["final_justification"]},
    {"id": "lo_revise", "statement_ar": "يراجع رأيه الأول حين يظهر ما يخالفه.", "skill_ko_ref": "KO-RS-06-009", "observable_behaviors_ar": ["يغيّر فرضيته الرائدة بدليل"], "evidence_sources": ["hypothesis_ledger"]},
]
def levels(d): return [{"score": i, "descriptor_ar": t} for i, t in enumerate(d)]
rub = {
    "reference_answer_ar": "لم يُسرق الصندوق. جرى الحفر عند أصل الشجيرة صباح الخميس لقص عقلة طلبها زبون من المشتل، وهذا مسجل في طلبات المشتل وقائمة توصيله وسجل البستاني والبوابة. وجد البستاني الصندوق أثناء الحفر فظنه منسياً وسلّمه لمكتب الإدارة نحو 10:25، فقيّدته الموظفة في سجل المفقودات وحفظته بمبلغه كاملاً، ولم يُبلَّغ النادي لأن الملصق لا يحمل اسماً كاملاً. وطالب العقلة لم يدخل المدرسة وتسلم عقلته من المشتل. حدود الاستنتاج: لا يبيّن أي سجل هل كان في الحفر أحد غير البستاني وفني المشتل، ولا يثبت أن ما وُجد هو الصندوق نفسه إلا بمطابقة المبلغ والملصق، ويبقى احتمال ضعيف لأمر لم تغطه السجلات.",
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
    H("hg1", 1, "metacognitive", "حين يختفي شيء، اسأل أولاً: هل يوجد تفسير بلا سرقة؟ وما السجل الذي يميّز بين التفسيرين؟", {"always": True}, None, 0.02),
    H("hg2", 2, "focus_area", "اتبع السجلات بالترتيب: من طلب؟ من وصّل؟ من عمل في الحديقة؟ ثم أين ذهب ما وُجد؟", he("ev_hole_note"), None, 0.04),
    H("hg3", 3, "pointer", "ابحث عن سجل في الإدارة يدوّن ما يُسلَّم إليها، وقارنه بوقت الحفر.", he("ev_hole_note"), None, 0.08),
    H("hd1", 1, "metacognitive", "لماذا قُلب الموضع عند الشجيرة يوم الخميس؟ هل لذلك سبب مسجل؟", he("ev_nursery_orders"), "i_a_dug", 0.02),
    H("hd2", 2, "pointer", "اقرأ في الطلب 311 مكان القص وموعده، ثم قارنهما بقائمة التوصيل.", he("ev_nursery_orders"), "i_a_dug", 0.06),
    H("hd3", 3, "partial_reveal", "اسأل البستاني ماذا ظهر حين حفر، وانظر هل سجّل ذلك في دفتره.", he("ev_nursery_orders"), "i_a_dug", 0.1),
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
Act("a_get_club", "examine", "اقرأ مدونة نادي البيئة", al, [G("ev_club_note")], "loc_clubroom", "GET_CLUB")
Act("a_get_hole", "examine", "اقرأ محضر معاينة الموضع", al, [G("ev_hole_note")], "loc_garden", "GET_HOLE")
Act("a_get_orders", "examine", "اطلب سجل طلبات المشتل بإذن الإدارة", al, [G("ev_nursery_orders")], "loc_nursery", "GET_ORDERS")
Act("a_get_delivery", "examine", "اطلب قائمة التوصيل والاستلام بإذن الإدارة", al, [G("ev_delivery_list")], "loc_nursery", "GET_DELIVERY")
Act("a_get_gardener_log", "examine", "اطلب سجل أعمال البستاني بإذن الإدارة", al, [G("ev_gardener_log")], "loc_garden", "GET_GARDENER_LOG")
Act("a_get_gate", "examine", "اطلب سجل بوابة المدرسة بإذن الإدارة", al, [G("ev_gate_log")], "loc_gate", "GET_GATE")
Act("a_get_ledger", "examine", "اطلب سجل المفقودات بإذن الإدارة", al, [G("ev_office_ledger")], "loc_office", "GET_LEDGER")
Act("a_get_count", "examine", "اطلب ورقة عدّ المحتويات", al, [G("ev_count_slip")], "loc_office", "GET_COUNT")
for cid, lab in [("jamil", "جميل"), ("sanaa", "سناء"), ("thaer", "ثائر"), ("ghassan", "غسان"), ("maha", "مها")]:
    Act(f"a_int_{cid}", "interview", f"ابدأ مقابلة {lab}", al, [{"op": "raise_trust", "ref_id": cid, "amount": 1}], cid, f"INT_{cid.upper()}")
Act("a_note_gardener", "examine", "دوّن إفادة جميل", fu("f_jamil_found"), [G("ev_gardener_statement")], "jamil", "NOTE_GARDENER")
Act("a_note_clerk", "examine", "دوّن إفادة سناء", fu("f_sanaa_received"), [G("ev_clerk_statement")], "sanaa", "NOTE_CLERK")
Act("a_note_buyer", "examine", "دوّن إفادة ثائر", fu("f_thaer_offsite"), [G("ev_buyer_statement")], "thaer", "NOTE_BUYER")
Act("a_note_ghassan", "examine", "دوّن إفادة غسان", fu("f_club_buried"), [G("ev_ghassan_statement")], "ghassan", "NOTE_GHASSAN")
Act("a_note_maha", "examine", "دوّن إفادة مها", fu("f_maha_process"), [G("ev_maha_statement")], "maha", "NOTE_MAHA")
Act("p_log_jamil", "present_evidence", "اعرض سجل أعمال البستاني عليه", {"presented": {"evidence_id": "ev_gardener_log", "to_character": "jamil"}}, [{"op": "emit_event", "ref_id": "PRESENTED_GARDENER_LOG"}], "jamil", "P_LOG_JAMIL", 0)
Act("a_hint", "request_hint", "اطلب تلميحاً", al, [], None, "REQUEST_HINT", 0)
Act("a_accuse", "final_accusation", "قدّم الاستنتاج النهائي", al, [{"op": "emit_event", "ref_id": "SUBMIT"}], None, "FINAL_ACCUSATION", 0)

topics = [
    {"id": "t_burial", "label_ar": "دفن الصندوق", "example_questions_ar": ["أين دُفن الصندوق؟", "من يعرف الموضع؟"], "fact_ids": ["f_club_buried"], "claim_ids": ["cl_ghassan_theft"]},
    {"id": "t_digging", "label_ar": "الحفر عند الشجيرة", "example_questions_ar": ["ماذا فعلت عند الشجيرة؟", "هل حفرت حول الجذع؟"], "fact_ids": ["f_jamil_dug", "f_jamil_found"], "claim_ids": ["cl_jamil_assumed"]},
    {"id": "t_office", "label_ar": "المكتب والمفقودات", "example_questions_ar": ["هل سُلّم إليك شيء؟", "لماذا لم يُبلَّغ أحد؟"], "fact_ids": ["f_sanaa_received", "f_sanaa_label"]},
    {"id": "t_order", "label_ar": "طلب العقلة", "example_questions_ar": ["ماذا طلبت؟", "هل دخلت المدرسة؟"], "fact_ids": ["f_thaer_order", "f_thaer_offsite"]},
    {"id": "t_nursery", "label_ar": "نظام المشتل وسجلاته", "example_questions_ar": ["كيف يُباع هذا الصنف؟", "ما السجلات التي تحتفظون بها؟"], "fact_ids": ["f_maha_process", "f_order_exists", "f_delivery_exists"]},
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
    (1, "الموضع المقلوب له سبب مسجل: الطلب 311 يحدد قص عقلة من النبتة الأم الخميس 09:40، وقائمة التوصيل تثبت دخول الحديقة والانتهاء 10:10.", ["ev_nursery_orders", "ev_delivery_list"], "i_a_dug"),
    (2, "سجل البستاني وسجل البوابة يؤكدان الحفر حول الجذع في الوقت نفسه من مصدرين لا يمرّان بالمشتل.", ["ev_gardener_log", "ev_gate_log"], "i_b_dug"),
    (3, "سجل المفقودات يقيّد صندوقاً مدفوناً سلّمه البستاني الخميس 10:25، وورقة العدّ تُظهر المبلغ كاملاً مطابقاً لقيد النادي.", ["ev_office_ledger", "ev_count_slip"], "i_a_box"),
    (4, "إفادتا البستاني وموظفة المكتب، وهما مستقلتان، تتفقان في الوقت والمكان والفعل.", ["ev_gardener_statement", "ev_clerk_statement"], "i_b_box"),
    (5, "الزبون الذي طلب العقلة لم يدخل المدرسة: تسلمها من المشتل بعد انتهاء القص، ولا اسم له في سجل البوابة.", ["ev_delivery_list", "ev_nursery_orders", "ev_gate_log", "ev_buyer_statement"], "i_a_buyer"),
    (6, "إذن لم تقع سرقة: وجد البستاني الصندوق أثناء الحفر المسجل ونقله بحسن نية، وبقي النادي غير مبلَّغ.", ["ev_office_ledger", "ev_nursery_orders"], "i_support_jamil"),
]
ending = {
    "steps": [{"order": o, "text_ar": t, "uses_evidence_ids": u, "inference_id": i} for o, t, u, i in steps],
    "alternative_paths_ar": [
        "يمكن الوصول إلى النتيجة من سجل المفقودات وورقة العدّ مباشرة لو سأل اللاعب المكتب أولاً، لكنه يبقى بلا تفسير لقلب التربة ما لم يتبع الطلب والتوصيل.",
        "ويمكن الوصول إليها من سجل البستاني وسجل البوابة وإفادتي البستاني وموظفة المكتب دون سجلات المشتل؛ والأقوى أن يتفق المساران.",
    ],
    "what_evidence_could_not_show_ar": [
        "لا يبيّن أي سجل هل كان في الحفر أحد غير البستاني وفني المشتل؛ يعتمد ذلك على اتفاق المشتل وإفادة البستاني.",
        "لا تثبت ورقة العدّ بنفسها متى دخل الصندوق الخزنة؛ يثبته سجل المفقودات المؤرّخ قبلها.",
        "لا تنفي السجلات أن يكون أحدهم قد حرّك الصندوق قبل الخميس؛ تنفي فقط أن يكون قد فُقد منه شيء.",
    ],
    "science_notes_ar": [
        "الموضع الفارغ والتربة المقلوبة ملاحظتان، أما «السرقة» فاستنتاج؛ افصل بين ما رأيته وما فسّرته به قبل أن تحكم.",
        "اتّباع السجلات بالترتيب (الطلب ثم التوصيل ثم سجل العامل ثم سجل الاستلام) أقوى من تخمين من يعرف المكان، وهو شبيه بسلسلة العهدة.",
        "معرفة شخص بمكان ما لا تدل على أنه فعل شيئاً فيه؛ تبقى نسبة الترجيح حكماً مبنياً على سجلات يمكن تتبعها.",
    ],
}
core = {
    "schema_version": "0.1.0", "case_id": CID, "case_version": "0.1.0",
    "meta": {"title_ar": "الصندوق تحت شجيرة الفل", "title_en": "The Box Under the Jasmine Shrub", "age_band": "13-15", "locale": "ar", "dialogue_register": "msa", "estimated_minutes": 30, "difficulty": 2,
             "content_flags": ["no_violence"], "authors": ["فريق أثر التحريري (مسودة بمساعدة الذكاء الاصطناعي، لم تُراجَع بشرياً بعد)"],
             "knowledge_object_refs": ["KO-RS-05-001", "KO-RS-05-003", "KO-RS-05-005", "KO-RS-05-002", "KO-RS-05-004", "KO-RS-06-001", "KO-RS-06-009", "KO-RS-06-021"]},
    "premise": {"hook_ar": "صندوق نقود دُفن تحت نبتة نادرة ثم اختفى، ولا شهود ولا كسر. وعند هذه النبتة بالذات قصّ أحدهم عقلة هذا الأسبوع.",
                "player_role_ar": "أنت متدرب في إدارة ثانوية الأطلال، وطلبت مشرفة نادي البيئة منك أن تتتبع السجلات المأذون بها لمعرفة ما جرى للصندوق.",
                "setting_ar": "ثانوية الأطلال، صباح الجمعة. تطّلع بإذن مكتوب من مدير المدرسة على سجلات الإدارة والبوابة والبستاني ونسخة من سجلات المشتل المتصلة بالمدرسة، ولا تفتح غيرها.",
                "public_fact_ids": ["f_box_missing", "f_no_witness", "f_rare_plant"],
                "assumed_general_knowledge_ar": ["الأشياء التي تُسلَّم إلى مكتب المدرسة تُقيَّد في سجل", "قص عقلة من نبتة قد يقتضي الحفر حول جذعها"]},
    "entities": {"characters": chars, "locations": locations, "objects": objects, "organizations": orgs},
    "truth": {"solution": {"culprit_ids": ["jamil"], "summary_ar": "لم يضع الصندوق في سرقة. نقله البستاني بحسن نية حين كان يحفر ليجهّز عقلة طلبها زبون، وظنه منسياً فأودعه مكتب الإدارة، ولم تصل الرسالة إلى النادي. المال محفوظ كاملاً، وصاحب الطلب لم يدخل المدرسة أصلاً.", "key_fact_ids": ["f_dug_thursday", "f_box_in_office", "f_buyer_off_site"]},
              "facts": facts, "claims": claims},
    "timeline": timeline, "evidence": ev, "evidence_graph": {"inferences": inf},
    "character_knowledge": ck, "hypotheses": hyps, "misdirection_plan": mis, "learning_objectives": los,
    "mechanics": {"time_budget_units": 40, "actions": A},
    "state_machine": {"id": "c016", "initial": "briefing", "type": "compound", "states": {
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
    "clock": {"epoch_hhmm": "08:00", "zone_label_ar": "توقيت المدرسة (الخميس)"},
    "cover": {"title_ar": "الصندوق تحت شجيرة الفل", "tagline_ar": "موضع فارغ، ولا شهود… فاتبع السجلات", "kicker_ar": "الملف السادس عشر · اتبع السجلات", "glyph": "❦", "accent": "green"},
    "cold_open_ar": ["صباح الجمعة في ثانوية الأطلال.", "فتح نادي البيئة الموضع الذي دفن فيه صندوق نقود الرحلة تحت شجيرة نادرة، فوجد التربة مقلوبة والصندوق غير موجود.",
                     "لا شهود، ولا كسر في السور. والشجيرة لا تُباع إلا من مشتل واحد بطلب مسبق.",
                     "بإذن مكتوب من المدير، ابدأ من السجلات: من طلب؟ ومن وصّل؟ ومن عمل في الحديقة؟"],
    "labs": [],
    "source_classes": [
        {"id": "primary_record", "label_ar": "سجل أصلي", "help_ar": "يُنتجه نظام أو شخص لحظة الحدث دون وسيط، كسجل طلبات أو سجل بوابة أو سجل مفقودات."},
        {"id": "redisplay", "label_ar": "نسخة معروضة", "help_ar": "معلومة نُقلت من سجل آخر أو لُخّصت منه."},
        {"id": "claim", "label_ar": "قول أو تصريح", "help_ar": "إفادة شخص؛ تُقاس بالسجلات لا بنبرة صاحبها."},
        {"id": "template", "label_ar": "قالب أو نموذج", "help_ar": "نص جاهز لا يصف الحدث الفعلي بذاته."},
        {"id": "public_document", "label_ar": "وثيقة منشورة", "help_ar": "وثيقة معلنة ومعروف ناشرها."}],
    "limit_menu": [
        {"id": "l_others", "label_ar": "لا يبيّن أي سجل هل كان في الحفر أحد غير البستاني وفني المشتل"},
        {"id": "l_before", "label_ar": "السجلات لا تنفي أن يكون أحدهم قد حرّك الصندوق قبل الخميس"},
        {"id": "l_same_box", "label_ar": "مطابقة الصندوق المسلَّم لصندوق النادي تعتمد على المبلغ والملصق لا على سجل واحد"},
        {"id": "l_invalid_known", "label_ar": "معرفة الزبون بموضع الشجيرة تثبت أنه أخذ الصندوق"},
        {"id": "l_invalid_empty", "label_ar": "الموضع الفارغ يثبت أن سرقة وقعت"}],
    "mind_change_menu": [
        {"id": "m_ledger_late", "label_ar": "ثبوت أن قيد الصندوق في سجل المفقودات كُتب بعد يوم الخميس"},
        {"id": "m_other_digger", "label_ar": "ظهور دليل على أن شخصاً آخر حفر في الموضع قبل الخميس"},
        {"id": "m_count_diff", "label_ar": "ثبوت أن المبلغ في ورقة العدّ لا يطابق قيد النادي"},
        {"id": "m_popular", "label_ar": "كثرة من يظنون أن سرقة وقعت"}],
    "skills": [{"skill_id": "KO-RS-05-001", "track": "B"}, {"skill_id": "KO-RS-05-005", "track": "B"}, {"skill_id": "KO-RS-05-003", "track": "D"}, {"skill_id": "KO-RS-06-001", "track": "D"}],
    "stage_hooks_ar": {"briefing": "موضع فارغ… وليس كل فراغ سرقة.", "investigating": "اتبع السجلات بالترتيب، ولا تتبع الأشخاص.", "review": "قبل أن تغلق الملف: ما الذي لا تعرفه؟", "resolved": "عاد الصندوق إلى النادي، وبقيت قاعدة جديدة للإبلاغ عن المفقودات."},
    "character_glyphs": {"jamil": "ج", "sanaa": "س", "thaer": "ث", "ghassan": "غ", "maha": "م"},
}
sc = {
    "case_id": CID,
    "accepted_conclusions": {"h_gardener": {"grade": 1, "note_ar": "استنتاج متسق مع الأدلة ويتطلب ذكر حدوده."},
                             "h_buyer": {"grade": 0, "note_ar": "يحوّل معرفة المكان إلى دليل فعل، ويتجاهل أن الزبون لم يدخل المدرسة."},
                             "h_member": {"grade": 0, "note_ar": "الصندوق بقي في موضعه حتى الحفر ثم حُفظ في الخزنة كاملاً."},
                             "h_theft": {"grade": 0, "note_ar": "المال محفوظ كاملاً، فلم يُسرق شيء."}},
    "confidence_band": {"h_gardener": [65, 90], "h_buyer": [0, 15], "h_member": [0, 15], "h_theft": [0, 15]},
    "source_key": {"ev_club_note": "primary_record", "ev_hole_note": "primary_record", "ev_nursery_orders": "primary_record", "ev_delivery_list": "primary_record", "ev_gardener_log": "primary_record",
                   "ev_gate_log": "primary_record", "ev_office_ledger": "primary_record", "ev_count_slip": "primary_record",
                   "ev_gardener_statement": "claim", "ev_clerk_statement": "claim", "ev_buyer_statement": "claim", "ev_ghassan_statement": "claim", "ev_maha_statement": "claim"},
    "link_key": {
        "h_gardener": {"ev_nursery_orders": "supports", "ev_delivery_list": "supports", "ev_gardener_log": "supports", "ev_office_ledger": "supports", "ev_count_slip": "supports", "ev_clerk_statement": "supports", "ev_gardener_statement": "supports", "ev_hole_note": "neutral"},
        "h_buyer": {"ev_nursery_orders": "supports", "ev_delivery_list": "weakens", "ev_gate_log": "weakens", "ev_office_ledger": "weakens", "ev_buyer_statement": "neutral"},
        "h_member": {"ev_hole_note": "supports", "ev_office_ledger": "weakens", "ev_count_slip": "weakens", "ev_gardener_log": "weakens"},
        "h_theft": {"ev_hole_note": "supports", "ev_count_slip": "weakens", "ev_office_ledger": "weakens"},
    },
    "required_limits": ["l_others", "l_same_box"], "valid_mind_changers": ["m_ledger_late", "m_other_digger", "m_count_diff"], "invalid_limits": ["l_invalid_known", "l_invalid_empty"],
    "decisive_evidence": ["ev_nursery_orders", "ev_delivery_list", "ev_office_ledger", "ev_count_slip", "ev_gardener_log"],
    "lab_requirement": None,
    "timeline_requirement": [{"evidence_id": "ev_gate_log", "utc_minute": 90, "tol": 10}, {"evidence_id": "ev_gardener_log", "utc_minute": 100, "tol": 15}, {"evidence_id": "ev_office_ledger", "utc_minute": 145, "tol": 10}],
    "refuted_hypotheses": ["h_buyer", "h_member", "h_theft"],
    "criteria_map": {"c_source": "source_typing", "c_conflict": "conflict_resolution", "c_links": "hypothesis_links", "c_uncertainty": "uncertainty", "c_revision": "revision", "c_elimination": "elimination", "c_justification": "justification_human"},
    "caps": {"no_citations_max": 45, "no_conflict_resolution_max": 70},
}
os.makedirs(OUT, exist_ok=True)
for suf, obj in [("", core), (".ui", ui), (".scoring", sc)]:
    with open(os.path.join(OUT, f"{CID}{suf}.json"), "w", encoding="utf8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
print("ok")
