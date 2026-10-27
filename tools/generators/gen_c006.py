#!/usr/bin/env python3
# Case c006 «خريطة بلا شمال» — perspective and frames of reference. Two night witnesses on opposite sides of a round plaza say
# "left" and "right"; both are right in their own frame. A rotated, north-less figure is what made it look like a contradiction.
# No-culprit convention: the staffer who rotated the published figure without a north arrow (unintended confusion) is in culprit_ids.
# Original fictional content; all numbers/places are invented. Usage: gen_c006.py OUT_DIR
import json, sys, os
OUT = sys.argv[1]
CID = "c006_map_without_north"

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

ch("muneer", "منير العلي", "witness", "صاحب مقهى الشرفة",
   "هادئ ودقيق في وصف ما يراه من شرفته، ولا ينتبه إلى أن غيره ينظر إلى الساحة من جهة أخرى.",
   ["أن تؤخذ شهادته على محمل الجد", "ألا يُتّهم بأنه أخطأ أو بالغ"],
   [L("mu_greet", "greeting", "تفضّل. كل ما سأقوله رأيته بعيني من الشرفة."),
    L("mu_pos", "reveal", "أقف عادةً على شرفة المقهى المطلّة على الساحة، وأنظر إلى وسطها لأرى ما يمرّ.", ["f_east_position"]),
    L("mu_turn", "reveal", "رأيت المركبة تنعطف إلى اليسار، وبقي ضوؤها الأحمر ظاهراً حتى اختفى عند عمود الساعة، وكان العمود عن يساري.", ["f_east_saw_pole_left"], ["cl_east_left"]),
    L("mu_unknown", "deflect_unknown", "لا أستطيع أن أجزم بأكثر مما رأيت."),
    L("mu_off", "deflect_offtopic", "اسألني عمّا رأيته من الشرفة فقط."),
    L("mu_bye", "farewell", "أرجو أن تُكتب شهادتي كما قلتها.")])
ch("adel", "عادل النمر", "witness", "حارس مكتبة المدينة",
   "منضبط وقليل الكلام، يدوّن ما يراه عند البوابة ولا يحب أن يُقال إنه أخطأ.",
   ["أن تُقبل ملاحظاته كما دوّنها", "ألا يُنسب إليه خطأ في جهة الانعطاف"],
   [L("ad_greet", "greeting", "مساء الخير. أحرس البوابة، وأرى الساحة من أمامها."),
    L("ad_pos", "reveal", "كنت عند بوابة المكتبة أنظر إلى الساحة كلها من جهتي، ولا أحوّل نظري عنها حين تمرّ مركبة.", ["f_west_position"]),
    L("ad_turn", "reveal", "رأيت المركبة تنعطف إلى اليمين، وضوؤها الأحمر اختفى عند عمود الساعة، وكان العمود عن يميني.", ["f_west_saw_pole_right"], ["cl_west_right"]),
    L("ad_unknown", "deflect_unknown", "لم أرَ غير ذلك."),
    L("ad_off", "deflect_offtopic", "اسألني عن البوابة وما رأيته منها."),
    L("ad_bye", "farewell", "مع السلامة.")])
ch("samer", "سامر الخوري", "suspect", "موظف الإصدارات في البلدية",
   "متعجل ويخشى أن يُنسب إليه خطأ في التقرير، فيؤكد أن عمله سليم قبل أن يُسأل عنه.",
   ["ألا يُلام على التباس الشكل المنشور", "إنهاء تقرير اللجنة في موعده"],
   [L("sm_greet", "greeting", "أهلاً. الشكل 2 جاهز منذ أسبوع."),
    L("sm_prep", "reveal", "أنا من أعدّ الشكل 2 من ملف الخريطة. هو الخريطة الرسمية كما هي، لم أغيّر فيها إلا الحجم.", ["f_samer_prepared_fig"], ["cl_samer_same"]),
    L("sm_refuse", "refuse_secret", "الشكل واضح لمن يقرؤه بتمعّن."),
    L("sm_rot", "reveal", "حسناً... أدرتُ الخريطة ربع دورة لتلائم الصفحة الرأسية، ولم أنقل سهم الشمال معها فبقي مخفياً.", ["f_fig_rotated"]),
    L("sm_unknown", "deflect_unknown", "لا أعرف شيئاً عن ذلك."),
    L("sm_off", "deflect_offtopic", "اسألني عن إعداد الشكل فقط."),
    L("sm_bye", "farewell", "سأصحّح الشكل إن لزم.")])

locations = [{"id": "loc_office", "name_ar": "مكتب لجنة السلامة", "description_ar": "مسودة اللجنة وسجل خط البلاغات."},
             {"id": "loc_archive", "name_ar": "أرشيف البلدية", "description_ar": "الخرائط المعتمدة ورسوم قسم المساحة."},
             {"id": "loc_plaza", "name_ar": "ساحة الصنوبر", "description_ar": "ساحة دائرية تحيط بها حلقة سير باتجاه واحد."},
             {"id": "loc_cafe", "name_ar": "شرفة مقهى الشرفة", "description_ar": "تطلّ على الساحة من جهتها الشرقية."},
             {"id": "loc_library", "name_ar": "بوابة مكتبة المدينة", "description_ar": "تطلّ على الساحة من جهتها الغربية."},
             {"id": "loc_publications", "name_ar": "قسم الإصدارات", "description_ar": "ملفات تصميم صفحات التقارير."}]
objects = [{"id": "obj_vehicle", "name_ar": "المركبة الصغيرة البيضاء", "description_ar": "مركبة مرّت في الساحة مساء الخميس."},
           {"id": "obj_clock", "name_ar": "عمود الساعة", "description_ar": "معلم ثابت عند أحد مداخل الساحة."}]
orgs = [{"id": "org_committee", "name_ar": "لجنة السلامة المرورية الليلية", "description_ar": "لجنة بلدية تعدّ ملاحظة عن حركة الساحة."}]

facts = []
def F(id, st, kind, subj, spoiler, time=None, loc=None, ko=None):
    d = {"id": id, "statement_ar": st, "kind": kind, "subject_ids": subj, "spoiler_level": spoiler}
    if time: d["time"] = time
    if loc: d["location_id"] = loc
    if ko: d["science_ko_refs"] = ko
    facts.append(d)
F("f_vehicle_night", "مرّت مركبة صغيرة بيضاء في ساحة الصنوبر قرابة الحادية عشرة والربع ليلاً.", "event", ["obj_vehicle", "loc_plaza"], 0, T(12, "approx"), "loc_plaza")
F("f_testimonies_differ", "قال صاحب المقهى إن المركبة انعطفت يساراً، وقال حارس المكتبة إنها انعطفت يميناً.", "event", ["muneer", "adel"], 0)
F("f_committee_draft", "تقترح مسودة اللجنة عدم الاعتماد على الشهادتين لأنهما متعارضتان في الظاهر.", "attribute", ["org_committee"], 0)
F("f_east_position", "يقف صاحب المقهى على الضلع الشرقي من الساحة ووجهه إلى مركزها، أي نحو الغرب.", "state", ["muneer", "loc_cafe"], 1, None, "loc_cafe", ["KO-RS-06-003"])
F("f_west_position", "يقف حارس المكتبة على الضلع الغربي من الساحة ووجهه إلى مركزها، أي نحو الشرق.", "state", ["adel", "loc_library"], 1, None, "loc_library", ["KO-RS-06-003"])
F("f_east_saw_pole_left", "رأى صاحب المقهى الضوء الخلفي للمركبة يختفي عند عمود الساعة، وكان العمود في جهته اليسرى.", "event", ["muneer", "obj_clock"], 1, T(12, "approx"), "loc_cafe")
F("f_west_saw_pole_right", "رأى حارس المكتبة الضوء الخلفي للمركبة يختفي عند عمود الساعة، وكان العمود في جهته اليمنى.", "event", ["adel", "obj_clock"], 1, T(12, "approx"), "loc_library")
F("f_pole_south", "عمود الساعة يقع عند مدخل «شارع الميناء» في الجهة الجنوبية من الساحة.", "attribute", ["obj_clock", "loc_plaza"], 1, None, "loc_plaza")
F("f_ring_oneway", "حلقة السير حول الساحة باتجاه واحد عكس عقارب الساعة، ولا تقاطعات داخلها.", "attribute", ["loc_plaza"], 1, None, "loc_plaza")
F("f_samer_prepared_fig", "أعدّ سامر الخوري الشكل المنشور من ملف الخريطة الأصلية.", "event", ["samer"], 1, None, "loc_publications")
F("f_fig_rotated", "دُوِّر الشكل المنشور ربع دورة ليلائم صفحة رأسية، وبقي سهم الشمال مخفياً.", "event", ["samer", "loc_publications"], 2, None, "loc_publications", ["KO-RS-05-014"])
F("f_exit_south", "غادرت المركبة الساحة عبر «شارع الميناء» بعد دخولها من «طريق السوق»، في مسار واحد.", "event", ["obj_vehicle", "loc_plaza"], 2, T(11, "exact", 12), "loc_plaza")
F("f_east_left_is_south", "كلمة «يسار» على لسان صاحب المقهى، بحكم موضعه واتجاه نظره، تعني الجهة الجنوبية من الساحة.", "relation", ["muneer"], 3, None, "loc_cafe", ["KO-RS-06-008"])
F("f_west_right_is_south", "كلمة «يمين» على لسان حارس المكتبة، بحكم موضعه واتجاه نظره، تعني الجهة الجنوبية من الساحة.", "relation", ["adel"], 3, None, "loc_library", ["KO-RS-06-008"])
claims = [
    {"id": "cl_east_left", "statement_ar": "المركبة انعطفت إلى اليسار.", "kind": "half_truth", "held_by": ["muneer"], "true_fact_id": "f_east_left_is_south", "contradicted_by_evidence_ids": ["ev_sightline", "ev_map_orig"]},
    {"id": "cl_west_right", "statement_ar": "المركبة انعطفت إلى اليمين.", "kind": "half_truth", "held_by": ["adel"], "true_fact_id": "f_west_right_is_south", "contradicted_by_evidence_ids": ["ev_sightline", "ev_map_orig"]},
    {"id": "cl_samer_same", "statement_ar": "الشكل المنشور هو الخريطة الرسمية كما هي، لم يتغير فيه شيء سوى الحجم.", "kind": "half_truth", "held_by": ["samer"], "true_fact_id": "f_fig_rotated", "contradicted_by_evidence_ids": ["ev_layout_meta", "ev_map_orig"]},
]
timeline = [
    {"id": "te_enter", "description_ar": "المركبة تدخل الساحة من طريق السوق.", "time": T(11), "location_id": "loc_plaza", "actor_ids": [], "fact_ids": ["f_exit_south"]},
    {"id": "te_exit", "description_ar": "المركبة تغادر الساحة عبر شارع الميناء عند عمود الساعة.", "time": T(12), "location_id": "loc_plaza", "actor_ids": [], "fact_ids": ["f_exit_south", "f_pole_south"]},
    {"id": "te_east_call", "description_ar": "صاحب المقهى يتصل بخط البلاغات الليلي.", "time": T(14), "location_id": "loc_cafe", "actor_ids": ["muneer"], "fact_ids": ["f_east_saw_pole_left"], "motivated_by_ar": "أراد أن يبلغ عن مركبة بلا شعار مرّت في الساحة"},
    {"id": "te_west_call", "description_ar": "حارس المكتبة يتصل بخط البلاغات الليلي.", "time": T(21), "location_id": "loc_library", "actor_ids": ["adel"], "fact_ids": ["f_west_saw_pole_right"], "motivated_by_ar": "سمع أن مقهى الشرفة بلّغ فأراد أن يضيف ما رآه"},
]

ev = []
def V(id, title, kind, content, acts, supports, rel, limits, contradicts=None, red=False, ko=None, loc=None):
    d = {"id": id, "title_ar": title, "kind": kind, "content_ar": content, "acquired_by_action_ids": acts, "supports_fact_ids": supports, "reliability": rel, "limits_ar": limits}
    if contradicts: d["contradicts_claim_ids"] = contradicts
    if red: d["is_red_herring"] = True
    if ko: d["forensic_ko_ref"] = ko
    if loc: d["location_id"] = loc
    ev.append(d)
V("ev_draft_note", "مسودة ملاحظة اللجنة", "documentary",
  "مسودة ملاحظة لجنة السلامة المرورية الليلية (غير نهائية)\nالبند 3: «أفاد صاحب المقهى بأن المركبة انعطفت يساراً، وأفاد حارس المكتبة بأنها انعطفت يميناً. الإفادتان متعارضتان، ويُقترح عدم الاعتماد عليهما في تحديد مسار المركبة.»",
  ["a_read_draft"], ["f_committee_draft"], "weak", "رأي أولي لكاتب المسودة لا تحليل؛ اعتمد على صياغة مختصرة للإفادتين لا على نصّيهما الأصليين.", loc="loc_office")
V("ev_fig_rotated", "الشكل 2 من تقرير اللجنة", "documentary",
  "الشكل 2 (صفحة رأسية؛ لا سهم شمال ولا مقياس رسم)\nدائرة تمثّل الساحة. في أعلى الصفحة: «مقهى الشرفة». في أسفلها: «مكتبة المدينة». على يسار الصفحة مدخل «طريق السوق»، وعلى يمينها مخرج «شارع الميناء».\nخط المسار يبدأ من يسار الصفحة، ويمرّ بالجهة السفلى من الدائرة، وينتهي عند يمين الصفحة.\nلا علامة على موضع أي شاهد ولا على جهة نظره.",
  ["a_read_fig"], [], "moderate", "رسم منشور بلا اتجاه مرجعي؛ لا تُعرف منه جهة الشمال، ولا هل هو الأصل أم نسخة معدّلة منه.", loc="loc_office")
V("ev_map_orig", "الخريطة المعتمدة لساحة الصنوبر", "documentary",
  "خريطة البلدية المعتمدة (سهم الشمال مرسوم إلى أعلى الخريطة)\n- الساحة جزيرة دائرية تحيط بها حلقة سير باتجاه واحد عكس عقارب الساعة.\n- أربعة مداخل ومخارج: شمالاً «طريق السوق»، جنوباً «شارع الميناء»، شرقاً «شارع الجسر»، غرباً «شارع المستودعات».\n- على الضلع الشرقي «مقهى الشرفة»، وعلى الضلع الغربي «مكتبة المدينة».\n- عمود الساعة عند مدخل «شارع الميناء» في الجنوب.",
  ["a_search_archive"], ["f_pole_south", "f_ring_oneway"], "strong", "تثبت مواضع المعالم والاتجاهات الثابتة، ولا تثبت ما جرى تلك الليلة ولا أين وقف كل شاهد على وجه التحديد.", contradicts=["cl_samer_same"], loc="loc_archive")
V("ev_east_call", "سجل خط البلاغات: الاتصال الأول", "documentary",
  "سجل خط البلاغات الليلي\n23:14 — المتصل: صاحب مقهى الشرفة\nالنص المدوَّن: «مرّت مركبة بيضاء صغيرة في الساحة، ثم انعطفت إلى اليسار واختفت.»\nملاحظة المستقبِل: لم يُسأل المتصل من أين رأى.",
  ["a_read_east_call"], ["f_testimonies_differ", "f_vehicle_night"], "moderate", "تدوين مختصر لكلام المتصل؛ لا يحدد موضع وقوفه ولا جهة نظره، ولا ما يقصده بكلمة «اليسار».", loc="loc_office")
V("ev_west_call", "سجل خط البلاغات: الاتصال الثاني", "documentary",
  "سجل خط البلاغات الليلي\n23:21 — المتصل: حارس مكتبة المدينة\nالنص المدوَّن: «رأيت مركبة بيضاء صغيرة تدور في الساحة ثم تنعطف إلى اليمين.»\nملاحظة المستقبِل: لم يُسأل المتصل من أين رأى.",
  ["a_read_west_call"], ["f_testimonies_differ", "f_vehicle_night"], "moderate", "تدوين مختصر لكلام المتصل؛ لا يحدد موضع وقوفه ولا جهة نظره، ولا ما يقصده بكلمة «اليمين».", loc="loc_office")
V("ev_east_note", "إفادة صاحب المقهى الموسّعة", "testimonial",
  "ملخص إفادة منير العلي:\n«كنت على الشرفة أنظر إلى وسط الساحة. مرّت المركبة أمامي وبقي ضوؤها الأحمر ظاهراً حتى اختفى عند عمود الساعة، وكان العمود عن يساري.»",
  ["a_note_muneer"], ["f_east_saw_pole_left"], "moderate", "ذاكرة شخص عن مشهد ليلي قصير؛ تحتاج إلى خريطة تحدد أين يقع عمود الساعة من الساحة.", loc="loc_cafe")
V("ev_west_note", "إفادة حارس المكتبة الموسّعة", "testimonial",
  "ملخص إفادة عادل النمر:\n«كنت عند بوابة المكتبة أنظر إلى الساحة. تحرّكت المركبة أمامي وبقي ضوؤها الأحمر ظاهراً حتى اختفى عند عمود الساعة، وكان العمود عن يميني.»",
  ["a_note_adel"], ["f_west_saw_pole_right"], "moderate", "ذاكرة شخص عن مشهد ليلي قصير؛ تحتاج إلى خريطة تحدد أين يقع عمود الساعة من الساحة.", loc="loc_library")
V("ev_sightline", "رسم خطوط الرؤية", "documentary",
  "رسم قسم المساحة (الشمال إلى أعلى الرسم)\nالموقع م: شرفة مقهى الشرفة على الضلع الشرقي، وخط الرؤية متجه إلى مركز الساحة نحو الغرب.\nالموقع ك: بوابة مكتبة المدينة على الضلع الغربي، وخط الرؤية متجه إلى مركز الساحة نحو الشرق.\nمخرج «شارع الميناء» عند أسفل الرسم.",
  ["a_survey"], ["f_east_position", "f_west_position"], "strong", "يحدد موضعي الوقوف واتجاه النظر بحسب معاينة القسم، ولا يثبت ما رآه كل شاهد فعلاً.", loc="loc_archive")
V("ev_counter", "سجل عدّاد الحركة عند الساحة", "digital",
  "سجل عدّاد الحركة عند مداخل الساحة ومخارجها (من 23:05 إلى 23:20)\n23:11 — دخول عبر «طريق السوق»\n23:12 — خروج عبر «شارع الميناء»\nلا تسجيلات أخرى في أي مدخل أو مخرج خلال المدة.",
  ["a_counter"], ["f_exit_south"], "strong", "يعدّ عبوراً عند المداخل والمخارج فقط؛ لا يحدد هوية المركبة ولا يخبر بما رآه الشاهدان.", loc="loc_plaza")
V("ev_layout_meta", "خصائص صفحة الشكل 2", "documentary",
  "ملف تصميم الشكل 2 — قسم الإصدارات\n- اتجاه الصفحة: رأسي.\n- تدوير الخريطة: ربع دورة عكس عقارب الساعة.\n- طبقة «سهم الشمال»: مخفية.\n- ملاحظة المصمّم: «أُدير الرسم ليلائم الصفحة».",
  ["a_get_layout"], ["f_fig_rotated"], "strong", "ملف إنتاج يصف كيف رُتّبت الصفحة، ولا يصف الحادثة ولا ما رآه أي شاهد.", loc="loc_publications")
V("ev_samer_stmt", "إفادة موظف الإصدارات", "testimonial",
  "ملخص إفادة سامر الخوري:\n«الشكل 2 هو الخريطة الرسمية كما هي، لم أغيّر فيه شيئاً سوى الحجم. من يقرؤه يفهم الاتجاهات.»",
  ["a_note_samer"], ["f_samer_prepared_fig"], "weak", "إفادة صاحب علاقة بالتصميم؛ تُقاس بملف التصميم وبالخريطة المعتمدة.", contradicts=["cl_samer_same"], loc="loc_publications")

def P(t, i): return {"ref_type": t, "ref_id": i}
inf = []
def I(id, prem, ct, concl, rel, strength, rule, ks):
    inf.append({"id": id, "premises": prem, "conclusion": {"ref_type": ct, "ref_id": concl}, "relation": rel, "strength": strength, "rule_ar": rule, "skill_ko_refs": ks})
E = lambda x: P("evidence", x)
Fa = lambda x: P("fact", x)
# path A (frame reasoning): hotline records + the sight-line drawing
I("i_east_a", [E("ev_east_call"), E("ev_sightline")], "fact", "f_east_left_is_south", "establishes", "strong",
  "رسم المساحة يضع صاحب المقهى في الشرق ناظراً إلى الغرب؛ والجنوب عن يسار من ينظر إلى الغرب، فكلمته تصف الجهة الجنوبية.", ["KO-RS-06-008"])
I("i_west_a", [E("ev_west_call"), E("ev_sightline")], "fact", "f_west_right_is_south", "establishes", "strong",
  "رسم المساحة يضع حارس المكتبة في الغرب ناظراً إلى الشرق؛ والجنوب عن يمين من ينظر إلى الشرق، فكلمته تصف الجهة الجنوبية.", ["KO-RS-06-008"])
# path B (landmark reasoning): the extended statements + the approved map
I("i_east_b", [E("ev_east_note"), E("ev_map_orig")], "fact", "f_east_left_is_south", "establishes", "strong",
  "إفادته تحدد أن العمود كان عن يساره، والخريطة المعتمدة تضع العمود في الجنوب؛ فيسار الشاهد هو جهة المعلم الجنوبي.", ["KO-RS-06-008"])
I("i_west_b", [E("ev_west_note"), E("ev_map_orig")], "fact", "f_west_right_is_south", "establishes", "strong",
  "إفادته تحدد أن العمود كان عن يمينه، والخريطة المعتمدة تضع العمود في الجنوب؛ فيمين الشاهد هو جهة المعلم الجنوبي.", ["KO-RS-06-008"])
I("i_rotated_a", [E("ev_fig_rotated"), E("ev_map_orig")], "fact", "f_fig_rotated", "establishes", "strong",
  "المعالم نفسها في الشكلين بعلاقاتها نفسها، لكن الأعلى في الشكل المنشور هو الشرق في الخريطة المعتمدة؛ فالرسم مُدار.", ["KO-RS-05-014"])
I("i_rotated_b", [E("ev_layout_meta")], "fact", "f_fig_rotated", "establishes", "strong",
  "ملف التصميم يسجّل تدوير الصفحة وإخفاء سهم الشمال.", ["KO-RS-05-014"])
I("i_exit_south", [E("ev_counter"), E("ev_map_orig")], "fact", "f_exit_south", "establishes", "strong",
  "العدّاد سجّل دخولاً واحداً وخروجاً واحداً، والخريطة تبيّن أن الحلقة باتجاه واحد؛ فالمسار واحد.", ["KO-RS-06-003"])
I("i_support_frames", [Fa("f_east_left_is_south"), Fa("f_west_right_is_south")], "hypothesis", "h_frames", "supports", "strong",
  "كلمتا «يسار» و«يمين» تدلان على الجهة نفسها حين تُقاسان من موضعي الشاهدين المتقابلين؛ فلا تعارض في الواقعة.", ["KO-RS-05-002"])
I("i_rule_liar", [Fa("f_east_left_is_south"), Fa("f_west_right_is_south")], "hypothesis", "h_liar", "rules_out", "strong",
  "إذا اتفق الوصفان على الجهة نفسها فاختلاف الكلمتين وحده لا يدل على أن أحدهما مخطئ أو كاذب.", ["KO-RS-06-009"])
I("i_rule_twice_a", [E("ev_counter")], "hypothesis", "h_twice", "rules_out", "strong",
  "العدّاد سجّل دخولاً واحداً وخروجاً واحداً ولا عبوراً آخر؛ فلا مخرجان ولا انعطافتان متعاكستان.", ["KO-RS-06-009"])
I("i_rule_twice_b", [E("ev_east_note"), E("ev_west_note")], "hypothesis", "h_twice", "rules_out", "strong",
  "كلا الشاهدين يسمّي المعلم نفسه، عمود الساعة، موضعاً لاختفاء الضوء؛ فالمخرج واحد وليس مخرجين.", ["KO-RS-06-009"])
I("i_east_claim", [E("ev_east_call"), E("ev_sightline")], "claim", "cl_east_left", "contradicts_claim", "suggestive",
  "الكلمة صحيحة بالنسبة إلى موضع قائلها فقط؛ ولا تصلح اتجاهاً عاماً قبل معرفة موضعه.", ["KO-RS-05-001"])
I("i_west_claim", [E("ev_west_call"), E("ev_sightline")], "claim", "cl_west_right", "contradicts_claim", "suggestive",
  "الكلمة صحيحة بالنسبة إلى موضع قائلها فقط؛ ولا تصلح اتجاهاً عاماً قبل معرفة موضعه.", ["KO-RS-05-001"])
I("i_samer_claim", [E("ev_layout_meta"), E("ev_samer_stmt")], "claim", "cl_samer_same", "contradicts_claim", "strong",
  "ملف التصميم يسجّل تدويراً وإخفاء لسهم الشمال، وهذا ينقض قوله إن شيئاً لم يتغير سوى الحجم.", ["KO-RS-05-001"])

ck = [
    {"character_id": "muneer", "knows": [{"fact_id": "f_east_position", "access": "witnessed", "certainty": "certain"}, {"fact_id": "f_east_saw_pole_left", "access": "witnessed", "certainty": "fairly_sure"}], "hides": [], "believes": [{"claim_id": "cl_east_left", "stance": "sincere"}]},
    {"character_id": "adel", "knows": [{"fact_id": "f_west_position", "access": "witnessed", "certainty": "certain"}, {"fact_id": "f_west_saw_pole_right", "access": "witnessed", "certainty": "fairly_sure"}], "hides": [], "believes": [{"claim_id": "cl_west_right", "stance": "sincere"}]},
    {"character_id": "samer", "knows": [{"fact_id": "f_samer_prepared_fig", "access": "witnessed", "certainty": "certain"}],
     "hides": [{"fact_id": "f_fig_rotated", "reveal_when": {"presented": {"evidence_id": "ev_map_orig", "to_character": "samer"}}, "cover_claim_id": None, "reveal_line_id": "sm_rot"}],
     "believes": [{"claim_id": "cl_samer_same", "stance": "sincere"}]},
]
hyps = [
    {"id": "h_liar", "statement_ar": "أحد الشاهدين أخطأ أو كذب في وصف جهة الانعطاف، ولذلك تعارضت شهادتاهما.", "is_true": False, "plausibility_at_start": "high"},
    {"id": "h_frames", "statement_ar": "الشاهدان وصفا الحدث نفسه بإطارين مرجعيين مختلفين، فلا تناقض بين شهادتيهما.", "is_true": True, "plausibility_at_start": "low"},
    {"id": "h_twice", "statement_ar": "غيّرت المركبة اتجاهها مرتين فسلكت مخرجين مختلفين، فرأى كل شاهد انعطافة مختلفة.", "is_true": False, "plausibility_at_start": "medium"},
]
mis = [
    {"id": "rh_opposite", "points_to_hypothesis_id": "h_liar", "planted_via_ar": "السجلان يدوّنان كلمتين متعاكستين، «يسار» و«يمين»، والشكل المنشور بلا اتجاه مرجعي.", "evidence_ids": ["ev_east_call", "ev_west_call", "ev_fig_rotated"], "refuted_by_inference_ids": ["i_rule_liar"],
     "fairness_note_ar": "السجلان لا يحددان موضع القائل، والرسم والخريطة المعتمدة والإفادات الموسّعة متاحة كلها قبل الاستنتاج."},
    {"id": "rh_two_turns", "points_to_hypothesis_id": "h_twice", "planted_via_ar": "كل شهادة تذكر انعطافة واحدة بوصف مختلف، فقد يُظن أنهما انعطافتان.", "evidence_ids": ["ev_east_call", "ev_west_call"], "refuted_by_inference_ids": ["i_rule_twice_a", "i_rule_twice_b"],
     "fairness_note_ar": "سجل العدّاد والإفادتان الموسّعتان متاحة كلها بالإجراءات العادية، وكل منها وحده يدل على مخرج واحد."},
]
los = [
    {"id": "lo_claim", "statement_ar": "يفرّق بين ما شاهده الشخص وبين طريقته في وصفه، ويصنّف المصدر.", "skill_ko_ref": "KO-RS-05-001", "observable_behaviors_ar": ["يصنّف السجلات والإفادات", "يقابل القول بالسجل"], "evidence_sources": ["evidence_board"]},
    {"id": "lo_timeline", "statement_ar": "يرتّب الأحداث على خط زمني ليتحقق من تتابع الدخول والخروج والبلاغات.", "skill_ko_ref": "KO-RS-05-005", "observable_behaviors_ar": ["يضع الأدلة في أزمنتها"], "evidence_sources": ["timeline_task", "action_log"]},
    {"id": "lo_hyp", "statement_ar": "يوازن بين فرضيتين على الأقل ويستبعد ما تنقضه الأدلة.", "skill_ko_ref": "KO-RS-05-002", "observable_behaviors_ar": ["يضيف فرضيات", "يستبعد بدليل"], "evidence_sources": ["hypothesis_ledger"]},
    {"id": "lo_diag", "statement_ar": "يميّز بين الاتجاه النسبي إلى الواقف (يمين/يسار) والاتجاه الثابت (شمال/جنوب).", "skill_ko_ref": "KO-RS-06-001", "observable_behaviors_ar": ["يربط الدليل بالفرضية باتجاه صحيح"], "evidence_sources": ["evidence_board", "final_justification"]},
    {"id": "lo_calib", "statement_ar": "يصوغ ثقته بحدودها.", "skill_ko_ref": "KO-RS-06-021", "observable_behaviors_ar": ["يختار ثقة معقولة", "يذكر حدوداً"], "evidence_sources": ["final_justification"]},
    {"id": "lo_revise", "statement_ar": "يراجع رأيه الأول حين يظهر ما يخالفه.", "skill_ko_ref": "KO-RS-06-009", "observable_behaviors_ar": ["يغيّر فرضيته الرائدة بدليل"], "evidence_sources": ["hypothesis_ledger"]},
]
def levels(d): return [{"score": i, "descriptor_ar": t} for i, t in enumerate(d)]
rub = {
    "reference_answer_ar": "لا حاجة إلى افتراض أن أحد الشاهدين أخطأ. وقف صاحب المقهى في شرق الساحة ناظراً إلى مركزها، ووقف حارس المكتبة في غربها ناظراً إلى مركزها من الجهة المقابلة؛ فقال الأول «يسار» وقال الثاني «يمين» وكلاهما يصف الجهة الجنوبية حيث عمود الساعة ومخرج شارع الميناء. وسجل العدّاد يثبت عبوراً واحداً، ولا دليل على مسار ثانٍ. أما التباس القارئ فمنشؤه شكل منشور أُدير ربع دورة وأُخفي فيه سهم الشمال. حدود الاستنتاج: لا نعرف هوية المركبة ولا سبب مرورها، ولا نملك ما يضبط تفاصيل أخرى رآها الشاهدان ليلاً.",
    "criteria": [
        {"id": "c_source", "name_ar": "تصنيف المصادر", "objective_ids": ["lo_claim"], "scored_by": "deterministic", "weight": 0.15, "levels": levels(["لم يصنّف", "أخطأ في الأغلب", "نصف صحيح", "معظمه صحيح", "كله صحيح"])},
        {"id": "c_conflict", "name_ar": "التحقق من تتابع الأحداث على الخط الزمني", "objective_ids": ["lo_timeline"], "scored_by": "deterministic", "weight": 0.2, "levels": levels(["لم يضع شيئاً", "وضع قليلاً", "وضع نصفها صحيحاً", "معظمها", "كلها في موضعها"])},
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
    H("hg1", 1, "metacognitive", "أين ينتهي ما شاهده الشخص وتبدأ طريقته في وصفه؟", {"always": True}, None, 0.02),
    H("hg2", 2, "focus_area", "ضع كل معلومة في جدول: مصدر أصلي أم نسخة أم تعليق؟", he("ev_fig_rotated"), None, 0.04),
    H("hg3", 3, "pointer", "راجع تحديداً الدليل الذي يوضح سياق الاتجاه أو الموضع أو الوثيقة.", he("ev_west_call"), None, 0.06),
    H("hm1", 1, "metacognitive", "من أي جهة من الساحة كان كل شاهد ينظر إليها؟", he("ev_west_call"), "i_east_a", 0.02),
    H("hm2", 2, "pointer", "يمين الواقف ويساره يتبدلان إن وقف في الجهة المقابلة. ما الذي لا يتبدل؟", he("ev_west_call"), "i_east_a", 0.05),
    H("hm3", 3, "partial_reveal", "اطلب رسم خطوط الرؤية وابحث في الأرشيف عن الخريطة المعتمدة، ثم قارن موضعي الشاهدين.", he("ev_map_orig"), "i_east_a", 0.1),
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
Act("a_read_draft", "examine", "اقرأ مسودة ملاحظة اللجنة", al, [G("ev_draft_note")], "loc_office", "READ_DRAFT")
Act("a_read_fig", "examine", "افتح الشكل 2 من تقرير اللجنة", al, [G("ev_fig_rotated")], "loc_office", "READ_FIG")
Act("a_read_east_call", "examine", "اقرأ الاتصال الأول في سجل البلاغات", al, [G("ev_east_call")], "loc_office", "READ_EAST_CALL")
Act("a_read_west_call", "examine", "اقرأ الاتصال الثاني في سجل البلاغات", he("ev_east_call"), [G("ev_west_call")], "loc_office", "READ_WEST_CALL")
Act("a_search_archive", "search_location", "ابحث في أرشيف البلدية عن الخريطة المعتمدة", he("ev_fig_rotated"), [G("ev_map_orig")], "loc_archive", "SEARCH_ARCHIVE")
Act("a_survey", "examine", "اطلب رسم خطوط الرؤية من قسم المساحة", he("ev_east_call"), [G("ev_sightline")], "loc_archive", "SURVEY")
Act("a_counter", "examine", "اطلب سجل عدّاد الحركة عند الساحة", he("ev_east_call"), [G("ev_counter")], "loc_plaza", "COUNTER")
Act("a_int_muneer", "interview", "ابدأ مقابلة منير", al, [{"op": "raise_trust", "ref_id": "muneer", "amount": 1}], "muneer", "INT_MUNEER")
Act("a_int_adel", "interview", "ابدأ مقابلة عادل", al, [{"op": "raise_trust", "ref_id": "adel", "amount": 1}], "adel", "INT_ADEL")
Act("a_int_samer", "interview", "ابدأ مقابلة سامر", he("ev_fig_rotated"), [{"op": "raise_trust", "ref_id": "samer", "amount": 1}], "samer", "INT_SAMER")
Act("a_note_muneer", "examine", "دوّن إفادة منير الموسّعة", fu("f_east_saw_pole_left"), [G("ev_east_note")], "muneer", "NOTE_MUNEER")
Act("a_note_adel", "examine", "دوّن إفادة عادل الموسّعة", fu("f_west_saw_pole_right"), [G("ev_west_note")], "adel", "NOTE_ADEL")
Act("a_note_samer", "examine", "دوّن إفادة سامر", fu("f_samer_prepared_fig"), [G("ev_samer_stmt")], "samer", "NOTE_SAMER")
Act("a_get_layout", "search_location", "اطلب ملف تصميم الشكل من قسم الإصدارات", fu("f_fig_rotated"), [G("ev_layout_meta")], "loc_publications", "GET_LAYOUT")
Act("p_map_samer", "present_evidence", "اعرض الخريطة المعتمدة على سامر", {"presented": {"evidence_id": "ev_map_orig", "to_character": "samer"}}, [{"op": "emit_event", "ref_id": "PRESENTED_MAP"}], "samer", "P_MAP_SAMER", 0)
Act("a_hint", "request_hint", "اطلب تلميحاً", al, [], None, "REQUEST_HINT", 0)
Act("a_accuse", "final_accusation", "قدّم الاستنتاج النهائي", al, [{"op": "emit_event", "ref_id": "SUBMIT"}], None, "FINAL_ACCUSATION", 0)

topics = [
    {"id": "t_where", "label_ar": "موضع الوقوف ووجهة النظر", "example_questions_ar": ["من أين كنت تنظر؟", "أين كنت واقفاً؟"], "fact_ids": ["f_east_position", "f_west_position"]},
    {"id": "t_turn", "label_ar": "اتجاه الانعطاف", "example_questions_ar": ["إلى أي جهة انعطفت المركبة؟", "ماذا رأيت عند عمود الساعة؟"], "fact_ids": ["f_east_saw_pole_left", "f_west_saw_pole_right"], "claim_ids": ["cl_east_left", "cl_west_right"]},
    {"id": "t_fig", "label_ar": "إعداد الشكل المنشور", "example_questions_ar": ["كيف أُعدّ الشكل 2؟", "هل تغيّر شيء في الخريطة؟"], "fact_ids": ["f_samer_prepared_fig", "f_fig_rotated"], "claim_ids": ["cl_samer_same"]},
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
    (1, "السجلان يدوّنان كلمتين متعاكستين دون موضع القائل، والشكل المنشور بلا سهم شمال؛ فالتعارض ظاهر في الورق لا في الواقعة بعد.", ["ev_east_call", "ev_west_call", "ev_fig_rotated"], "i_rotated_a"),
    (2, "رسم المساحة يضع الشاهدين على جانبين متقابلين ينظر كل منهما إلى وسط الساحة؛ فالجنوب عن يسار الشرقي وعن يمين الغربي.", ["ev_sightline", "ev_east_call", "ev_west_call"], "i_east_a"),
    (3, "الطريق الثاني: الإفادتان الموسّعتان تسميان المعلم نفسه، عمود الساعة، والخريطة المعتمدة تضعه في الجنوب.", ["ev_east_note", "ev_west_note", "ev_map_orig"], "i_east_b"),
    (4, "إذن لا تعارض في الواقعة: الكلمتان تصفان الجهة نفسها من موضعين مختلفين، وسجل العدّاد لا يُظهر مساراً آخر.", ["ev_counter", "ev_east_note", "ev_west_note"], "i_rule_twice_a"),
    (5, "اختلاف الكلمتين وحده لا يدل على أن أحدهما أخطأ أو كذب.", ["ev_sightline", "ev_map_orig"], "i_rule_liar"),
]
ending = {
    "steps": [{"order": o, "text_ar": t, "uses_evidence_ids": u, "inference_id": i} for o, t, u, i in steps],
    "alternative_paths_ar": ["يمكن الوصول إلى النتيجة بمسارين مستقلين: رسم خطوط الرؤية مع السجلين، أو الإفادتين الموسّعتين مع الخريطة المعتمدة؛ والثاني يبيّن أن المعلم الثابت يوحّد الوصفين."],
    "what_evidence_could_not_show_ar": ["لا تحدد الأدلة هوية المركبة ولا سبب مرورها.", "كلا الشاهدين رأى مشهداً ليلياً قصيراً من بعيد؛ فتبقى التفاصيل الدقيقة مثل السرعة والوقت غير مضبوطة."],
    "science_notes_ar": ["اليمين واليسار يتبدلان بتبدل موضع الواقف واتجاه نظره، أما الجهات الأصلية فثابتة على الخريطة.", "الخريطة المنشورة بلا سهم شمال قد تكون مُدارة؛ تحقق من اتجاهها قبل أن تقارنها بإفادة."],
}
core = {
    "schema_version": "0.1.0", "case_id": CID, "case_version": "0.1.0",
    "meta": {"title_ar": "خريطة بلا شمال", "title_en": "A Map Without North", "age_band": "16-18", "locale": "ar", "dialogue_register": "msa", "estimated_minutes": 25, "difficulty": 2,
             "content_flags": ["no_violence", "science_lab"], "authors": ["فريق أثر التحريري (مسودة بمساعدة الذكاء الاصطناعي، لم تُراجَع بشرياً بعد)"],
             "knowledge_object_refs": ["KO-RS-05-001", "KO-RS-05-005", "KO-RS-05-002", "KO-RS-06-001", "KO-RS-06-009", "KO-RS-06-021"]},
    "premise": {"hook_ar": "شاهدان رأيا مركبة واحدة في ليلة واحدة، لكن أحدهما قال «يسار» والآخر قال «يمين». فهل يكذب أحدهما؟",
                "player_role_ar": "أنت محلّل ملفات في لجنة السلامة المرورية الليلية، وعليك أن تحسم هل تتناقض الشهادتان فعلاً قبل أن تُقرّ اللجنة مسودتها.",
                "setting_ar": "ساحة الصنوبر، ساحة دائرية في مدينة متخيَّلة، مساء الخميس. توقيت البلدية هو توقيت كل السجلات.",
                "public_fact_ids": ["f_vehicle_night", "f_testimonies_differ", "f_committee_draft"],
                "assumed_general_knowledge_ar": ["الاتجاهات الأربعة (شمال، جنوب، شرق، غرب) ثابتة على الخريطة", "الرسم المنشور قد يختلف عن أصله في الحجم أو الاتجاه"]},
    "entities": {"characters": chars, "locations": locations, "objects": objects, "organizations": orgs},
    "truth": {"solution": {"culprit_ids": ["samer"], "summary_ar": "لا كذب ولا مسار مختلف في هذه القضية. الشاهدان وقفا على جانبين متقابلين من الساحة، فوصف كل منهما الجهة الجنوبية نفسها بكلمة تخص موضعه. وسبب ظهور تناقض في الورق شكل مُدار نُشر بلا سهم شمال، وقد أعدّه موظف الإصدارات دون قصد التضليل.",
                                  "key_fact_ids": ["f_east_left_is_south", "f_west_right_is_south"]},
              "facts": facts, "claims": claims},
    "timeline": timeline, "evidence": ev, "evidence_graph": {"inferences": inf},
    "character_knowledge": ck, "hypotheses": hyps, "misdirection_plan": mis, "learning_objectives": los,
    "mechanics": {"time_budget_units": 30, "actions": A},
    "state_machine": {"id": "c006", "initial": "briefing", "type": "compound", "states": {
        "briefing": {"description_ar": "الإحاطة", "type": "atomic", "on": {"START": {"target": "investigating"}}},
        "investigating": {"description_ar": "التحقيق", "type": "compound", "initial": "gathering",
                          "states": {"gathering": {"type": "atomic", "on": {"OPEN_DEDUCTION": {"target": "deducing"}}}, "deducing": {"type": "atomic", "on": {"BACK": {"target": "gathering"}}}},
                          "on": {"SUBMIT": {"target": "review"}}},
        "review": {"description_ar": "مراجعة", "type": "atomic", "on": {"CLOSE": {"target": "resolved"}}},
        "resolved": {"description_ar": "إغلاق", "type": "final"}}},
    "dialogue": {"max_turns_per_interview": 10, "llm_enabled": False, "topics": topics},
    "rubric": rub, "hint_ladder": hints,
    "fairness_test": {"requirements": {"min_disjoint_proof_paths": 2, "max_inference_depth": 3, "all_red_herrings_refutable": True, "culprit_uniquely_entailed": True, "no_hidden_fact_dependency": True, "max_required_actions": 30}, "runs": []},
    "ending_explanation": ending,
    "expert_review": [{"role": r, "reviewer": "—", "status": "pending", "content_hash": "unbound", "date": "2026-10-27", "notes_ar": "بانتظار مراجعة بشرية؛ لم يُجرَ أي اعتماد."} for r in
                      ["narrative_editor", "scientific_reviewer", "learning_designer", "age_appropriateness", "cultural_reviewer", "legal_rights", "safety"]],
}
ui = {
    "case_id": CID,
    "clock": {"epoch_hhmm": "23:00", "zone_label_ar": "توقيت البلدية"},
    "cover": {"title_ar": "خريطة بلا شمال", "tagline_ar": "يسار ويمين… وأحدهما فقط هو الصحيح؟", "kicker_ar": "الملف السادس · المنظور", "glyph": "◇", "accent": "green"},
    "cold_open_ar": ["الخميس، قرابة الحادية عشرة ليلاً.", "مركبة بيضاء صغيرة مرّت في الساحة الدائرية، ولدى اللجنة روايتان: «يسار» و«يمين».", "المسودة جاهزة، وفيها اقتراح باستبعاد الشهادتين معاً.", "قبل أن توقّع: هل تعارضت الروايتان في الواقعة نفسها، أم في الورق فقط؟"],
    "labs": [],
    "source_classes": [
        {"id": "primary_record", "label_ar": "سجل أصلي", "help_ar": "يُنتجه نظام أو شخص لحظة الحدث دون وسيط، كسجل عدّاد أو خريطة معتمدة."},
        {"id": "redisplay", "label_ar": "نسخة معروضة", "help_ar": "رسم أو معلومة نُقلت من مصدر آخر وقد تغيّرت في العرض."},
        {"id": "claim", "label_ar": "قول أو تصريح", "help_ar": "إفادة شخص؛ تُقاس بالسجلات لا بنبرة صاحبها."},
        {"id": "template", "label_ar": "قالب أو نموذج", "help_ar": "نص جاهز لا يصف الحدث الفعلي بذاته."},
        {"id": "public_document", "label_ar": "وثيقة منشورة", "help_ar": "وثيقة معلنة ومعروف ناشرها."}],
    "limit_menu": [
        {"id": "l_vehicle", "label_ar": "الأدلة لا تحدد هوية المركبة ولا سبب مرورها"},
        {"id": "l_night", "label_ar": "الشاهدان رأيا مشهداً ليلياً قصيراً من بعيد، فتبقى تفاصيل صغيرة غير مضبوطة"},
        {"id": "l_invalid_tone", "label_ar": "ثقة نبرة أحد الشاهدين تدل على أنه الأصدق"},
        {"id": "l_invalid_page", "label_ar": "ما يظهر على الصفحة يميناً ويساراً هو ما حدث فعلاً"}],
    "mind_change_menu": [
        {"id": "m_other_exit", "label_ar": "ظهور تسجيل مستقل يُظهر المركبة تخرج من مخرج غير الجنوبي"},
        {"id": "m_stand_swap", "label_ar": "ثبوت أن أحد الشاهدين كان في موضع غير الموضع المسجّل"},
        {"id": "m_popular", "label_ar": "كثرة من يظنون أن أحد الشاهدين مخطئ"}],
    "skills": [{"skill_id": "KO-RS-05-001", "track": "B"}, {"skill_id": "KO-RS-05-005", "track": "B"}, {"skill_id": "KO-RS-05-002", "track": "D"}, {"skill_id": "KO-RS-06-001", "track": "C"}],
    "stage_hooks_ar": {"briefing": "كلمتان متعاكستان… فهل المشكلة في الواقعة أم في طريقة وصفها؟", "investigating": "اسأل دائماً: من أين كان ينظر، وماذا بقي ثابتاً؟", "review": "قبل أن تُغلق الملف: ما الذي لا تعرفه؟", "resolved": "أُغلق الملف. في الأرشيف ملف آخر ينتظر."},
    "character_glyphs": {"muneer": "م", "adel": "ع", "samer": "س"},
}
sc = {
    "case_id": CID,
    "accepted_conclusions": {"h_liar": {"grade": 0, "note_ar": "يعامل اختلاف الكلمتين كأنه اختلاف في الواقعة، دون معرفة موضع كل قائل."},
                             "h_frames": {"grade": 1, "note_ar": "استنتاج متسق مع الأدلة ويتطلب ذكر حدوده."},
                             "h_twice": {"grade": 0, "note_ar": "سجل العدّاد والحلقة ذات الاتجاه الواحد لا يتركان مجالاً لمسارين."}},
    "confidence_band": {"h_liar": [0, 15], "h_frames": [65, 90], "h_twice": [0, 15]},
    "source_key": {"ev_map_orig": "primary_record", "ev_sightline": "primary_record", "ev_counter": "primary_record", "ev_layout_meta": "primary_record",
                   "ev_east_call": "primary_record", "ev_west_call": "primary_record", "ev_fig_rotated": "redisplay",
                   "ev_draft_note": "claim", "ev_east_note": "claim", "ev_west_note": "claim", "ev_samer_stmt": "claim"},
    "link_key": {
        "h_frames": {"ev_sightline": "supports", "ev_map_orig": "supports", "ev_east_note": "supports", "ev_west_note": "supports", "ev_counter": "supports", "ev_layout_meta": "supports", "ev_draft_note": "neutral"},
        "h_liar": {"ev_east_call": "supports", "ev_west_call": "supports", "ev_sightline": "weakens", "ev_map_orig": "weakens", "ev_east_note": "weakens", "ev_west_note": "weakens", "ev_draft_note": "supports"},
        "h_twice": {"ev_counter": "weakens", "ev_map_orig": "weakens", "ev_east_call": "supports", "ev_west_call": "supports"},
    },
    "required_limits": ["l_vehicle", "l_night"], "valid_mind_changers": ["m_other_exit", "m_stand_swap"], "invalid_limits": ["l_invalid_tone", "l_invalid_page"],
    "decisive_evidence": ["ev_sightline", "ev_map_orig", "ev_east_call", "ev_west_call", "ev_counter"],
    "lab_requirement": None,
    "timeline_requirement": [{"evidence_id": "ev_counter", "utc_minute": 12, "tol": 2}, {"evidence_id": "ev_east_call", "utc_minute": 14, "tol": 2}, {"evidence_id": "ev_west_call", "utc_minute": 21, "tol": 2}],
    "refuted_hypotheses": ["h_liar", "h_twice"],
    "criteria_map": {"c_source": "source_typing", "c_conflict": "conflict_resolution", "c_links": "hypothesis_links", "c_uncertainty": "uncertainty", "c_revision": "revision", "c_elimination": "elimination", "c_justification": "justification_human"},
    "caps": {"no_citations_max": 45, "no_conflict_resolution_max": 70},
}
os.makedirs(OUT, exist_ok=True)
for suf, obj in [("", core), (".ui", ui), (".scoring", sc)]:
    with open(os.path.join(OUT, f"{CID}{suf}.json"), "w", encoding="utf8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
print("ok")
