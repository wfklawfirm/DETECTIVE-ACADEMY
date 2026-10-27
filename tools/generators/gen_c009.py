#!/usr/bin/env python3
# Case c009 «المخطوطة والاقتباس المقلوب» — source criticism and quotation checking. Teaches: trace a quotation to its original place,
# compare the context of each part, and do not let a discrepancy between sources turn into "all sources are worthless".
# No-culprit convention: the page editor who (without intent to deceive) pasted two separate lines into one quotation is recorded in
# culprit_ids. All manuscripts, translators, cities and persons are fictional. Usage: gen_c009.py OUT_DIR
import json, sys, os
OUT = sys.argv[1]
CID = "c009_inverted_quote"

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
ch("amina", "أمينة الصبّاغ", "expert", "أمينة مكتبة الأبحاث في المدينة",
   "منظمة ودقيقة، تحب أن تقول ما في الفهارس والسجلات فقط، ولا تعرف من بدأ نشر المنشور.",
   ["أن يُرجع إلى الكتب نفسها قبل الحكم عليها"],
   [L("am_greet", "greeting", "أهلاً بك. الفهرس أمامي، وأستطيع أن أدلّك على النسخ والطبعات."),
    L("am_a", "reveal", "عندنا الترجمة (أ) كاملة، ويمكنك الرجوع إلى فصلها الرابع.", ["f_has_trans_a"]),
    L("am_b", "reveal", "وعندنا الترجمة (ب) أيضاً، ويمكنك الرجوع إلى فصلها التاسع.", ["f_has_trans_b"]),
    L("am_fac", "reveal", "للمكتبة نسخة مصورة من المخطوطة نفسها، ولها فهرس يحدد مواضع الأبواب.", ["f_has_facsimile"]),
    L("am_cat", "reveal", "السجل الفهرسي يصف الطبعتين والمترجمين، وأستطيع أن أخرجه لك.", ["f_has_catalogue"]),
    L("am_nojoint", "reveal", "لم أجد في الفهرس طبعة تضع العبارتين متجاورتين؛ كل منهما في موضعها.", ["f_no_joint_edition"]),
    L("am_unknown", "deflect_unknown", "هذا خارج ما في الفهرس."),
    L("am_off", "deflect_offtopic", "اسألني عن النسخ والطبعات."),
    L("am_bye", "farewell", "ارجع إلى الأصل كلما استطعت.")])
ch("nabil", "نبيل الخطيب", "suspect", "محرر الصفحة الثقافية التي نشرت المنشور",
   "متحمس وسريع الكتابة، يخاف أن يُتّهم بالتضليل فيقلّل من شأن خطوة اختصر بها الطريق.",
   ["ألا يُتّهم بتضليل القراء", "أن يبقى المنشور صالحاً للدفاع عنه"],
   [L("nb_greet", "greeting", "أنا نقلت الجملة من كتاب مطبوع. اسألني ما شئت."),
    L("nb_cited", "reveal", "قرأتها في ترجمة مطبوعة، وظننتها نصاً واحداً متصلاً.", None, ["cl_nabil_original"]),
    L("nb_notes", "reveal", "أحتفظ بملف ملاحظات لكل مقال، وفيه بطاقات المصادر.", ["f_notes_exist"]),
    L("nb_refuse", "refuse_secret", "لا أذكر شيئاً آخر عن طريقة كتابة الاقتباس."),
    L("nb_joined", "reveal", "نعم... نسخت العبارة الأولى من ترجمة والثانية من ترجمة أخرى، ولصقتهما معاً في بطاقة واحدة قبل النشر بقليل. كنت أنوي مراجعة الأصل ولم أفعل.", ["f_joined_by_writer"]),
    L("nb_unknown", "deflect_unknown", "لا أذكر ذلك."),
    L("nb_off", "deflect_offtopic", "اسألني عن المنشور وعن مصدره."),
    L("nb_bye", "farewell", "أريد أن أصحّح ما يجب تصحيحه.")])
ch("rana", "د. رنا العلي", "expert", "مؤرخة متخصصة في أدب الرحلات القديم",
   "هادئة وصبورة، تفرّق بين ما في النص وما يُقال عنه، ولا تعرف من نشر المنشور أولاً.",
   ["أن تُقرأ النصوص القديمة في سياقها"],
   [L("rn_greet", "greeting", "تفضّل. النص القديم لا يُفهم بسطر واحد مقتطع."),
    L("rn_fig", "reveal", "الفصل التاسع في الرحلة كله أمثال تضرب لتواضع النفس، والمدينة فيه صورة مجازية لا خبر عن مكان.", ["f_second_figurative"]),
    L("rn_preface", "reveal", "مترجمة الطبعة (ب) كتبت مقدمة تشرح فيها منهجها وقراءاتها، فاقرأها.", ["f_preface_exists"]),
    L("rn_unknown", "deflect_unknown", "لا أستطيع الجزم بذلك."),
    L("rn_off", "deflect_offtopic", "اسألني عن النص وسياقه."),
    L("rn_bye", "farewell", "اقرأ السياق قبل أن تستنتج.")])
ch("salim", "سليم الفرّاء", "witness", "متابع متحمس لنظريات المدن المفقودة",
   "صادق الحماسة، يبني حكمه على المنشور وحده، ويتراجع إن وجد أمامه الصفحة الأصلية.",
   ["أن يثبت وجود المدينة التي يبحث عنها"],
   [L("sl_greet", "greeting", "الجملة واضحة وضوح الشمس!"),
    L("sl_source", "reveal", "لم أقرأ الكتاب نفسه؛ قرأت المنشور ونسخت منه.", ["f_salim_source"]),
    L("sl_city", "reveal", "الرحالة يذكر ساحلاً ثم مدينة فيه، فلا بد أن المدينة حقيقية.", None, ["cl_salim_city"]),
    L("sl_unknown", "deflect_unknown", "لا أعرف أكثر من المنشور."),
    L("sl_off", "deflect_offtopic", "حدثني عن المدينة والمنشور."),
    L("sl_bye", "farewell", "سأقرأ الأصل إذا دللتني عليه.")])

locations = [{"id": "loc_library", "name_ar": "مكتبة الأبحاث", "description_ar": "الفهارس والنسخ المصورة والطبعات."},
             {"id": "loc_desk", "name_ar": "مكتب محرر الصفحة الثقافية", "description_ar": "ملف الملاحظات وبطاقات المصادر."},
             {"id": "loc_page", "name_ar": "الصفحة الثقافية على الشبكة", "description_ar": "حيث نُشر المنشور."},
             {"id": "loc_ms", "name_ar": "المخطوطة المصورة", "description_ar": "نسخة مصورة لمخطوطة الرحالة الخيالي."}]
objects = [{"id": "obj_quote", "name_ar": "الاقتباس المنسوب إلى الرحالة", "description_ar": "جملة نُشرت منسوبة إلى سالم بن نصر."},
           {"id": "obj_ms", "name_ar": "مخطوطة «نزهة الأسفار»", "description_ar": "رحلة خيالية لسالم بن نصر."}]
orgs = [{"id": "org_page", "name_ar": "صفحة «أسرار الأزمنة»", "description_ar": "صفحة ثقافية شعبية على الشبكة."}]

# ---------------------------------------------------------------- facts
facts = []
def F(id, st, kind, subj, spoiler, time=None, loc=None, ko=None):
    d = {"id": id, "statement_ar": st, "kind": kind, "subject_ids": subj, "spoiler_level": spoiler}
    if time: d["time"] = time
    if loc: d["location_id"] = loc
    if ko: d["science_ko_refs"] = ko
    facts.append(d)
F("f_post_published", "نشرت صفحة ثقافية جملة منسوبة إلى الرحالة سالم بن نصر، وقالت إنها تثبت وجود مدينة الفيروز المفقودة.", "event", ["obj_quote", "org_page"], 0, T(132), "loc_page")
F("f_fan_theory", "يرى سليم أن الجملة دليل على وجود المدينة.", "attribute", ["salim"], 0)
F("f_writer_says", "يقول نبيل إنه نقل الجملة من كتاب مطبوع.", "attribute", ["nabil"], 0)
F("f_has_trans_a", "تحتفظ المكتبة بالترجمة (أ) ويمكن الرجوع إلى فصلها الرابع.", "state", ["loc_library"], 1)
F("f_has_trans_b", "تحتفظ المكتبة بالترجمة (ب) ويمكن الرجوع إلى فصلها التاسع.", "state", ["loc_library"], 1)
F("f_has_facsimile", "للمكتبة نسخة مصورة من المخطوطة مع فهرس لمواضع أبوابها.", "state", ["loc_library", "obj_ms"], 1)
F("f_has_catalogue", "للمكتبة سجل فهرسي يصف طبعات الرحلة ومترجميها.", "state", ["loc_library"], 1)
F("f_no_joint_edition", "لا توجد في الفهرس طبعة تضع العبارتين متجاورتين.", "absence", ["loc_library"], 2, None, "loc_library", ["KO-RS-05-004"])
F("f_notes_exist", "يحتفظ نبيل بملف ملاحظات فيه بطاقات مصادر كل مقال.", "state", ["nabil", "loc_desk"], 1, None, "loc_desk")
F("f_preface_exists", "كتبت مترجمة الطبعة (ب) مقدمة تشرح فيها منهجها وقراءاتها.", "state", ["loc_library"], 1)
F("f_salim_source", "اعتمد سليم على المنشور وحده ولم يرجع إلى الكتاب.", "state", ["salim"], 1)
F("f_second_figurative", "العبارة الثانية جزء من مثل مضروب في تواضع النفس، لا خبر عن مكان.", "attribute", ["obj_quote", "obj_ms"], 2, None, "loc_ms", ["KO-RS-05-001"])
F("f_joined_by_writer", "نسخ نبيل العبارة الأولى من الترجمة (أ) والثانية من الترجمة (ب) ولصقهما في بطاقة واحدة الساعة 08:20.", "event", ["nabil", "obj_quote"], 2, T(80), "loc_desk", ["KO-RS-06-017"])
F("f_two_places", "وردت العبارتان في فصلين مختلفين تفصل بينهما فصول وعشرات الصفحات، لا في سياق واحد.", "relation", ["obj_quote", "obj_ms"], 3, None, "loc_ms", ["KO-RS-05-004", "KO-RS-05-001"])
F("f_composite_phrase", "الصيغة الموحدة التي نشرها نبيل مركبة من عبارتين بنصّي الترجمتين، ولا ترد بهذه الصيغة في أي طبعة ولا في المخطوطة.", "relation", ["obj_quote", "nabil"], 3, None, None, ["KO-RS-05-004", "KO-RS-06-017"])

claims = [
    {"id": "cl_salim_city", "statement_ar": "الرحالة يذكر ساحلاً ثم مدينة فيه، فالمدينة حقيقية.", "kind": "half_truth", "held_by": ["salim"], "true_fact_id": "f_two_places", "contradicted_by_evidence_ids": ["ev_facsimile", "ev_trans_a"]},
    {"id": "cl_nabil_original", "statement_ar": "الجملة وردت متصلة كما هي في الكتاب.", "kind": "honest_mistake", "held_by": ["nabil"], "true_fact_id": "f_composite_phrase", "contradicted_by_evidence_ids": ["ev_note_log", "ev_catalogue"]},
]
timeline = [
    {"id": "te_card_a", "description_ar": "نبيل ينسخ عبارة الساحل من الترجمة (أ) في بطاقة.", "time": T(40, "approx"), "location_id": "loc_desk", "actor_ids": ["nabil"], "fact_ids": [], "motivated_by_ar": "يجمع مادة مقال عن الرحلة"},
    {"id": "te_card_b", "description_ar": "نبيل ينسخ عبارة المدينة من الترجمة (ب) في بطاقة أخرى.", "time": T(65, "approx"), "location_id": "loc_desk", "actor_ids": ["nabil"], "fact_ids": [], "motivated_by_ar": "يبحث عما يزيّن مقاله"},
    {"id": "te_join", "description_ar": "نبيل يلصق العبارتين معاً في بطاقة «اقتباس للنشر».", "time": T(80), "location_id": "loc_desk", "actor_ids": ["nabil"], "fact_ids": ["f_joined_by_writer"], "motivated_by_ar": "أراد صياغة اقتباس مؤثر قبل موعد النشر"},
    {"id": "te_post", "description_ar": "نشر المنشور على الصفحة الثقافية.", "time": T(132), "location_id": "loc_page", "actor_ids": ["nabil"], "fact_ids": ["f_post_published"], "motivated_by_ar": "حان موعد النشر اليومي"},
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
V("ev_post", "منشور «أسرار الأزمنة»", "digital",
  "منشور على صفحة «أسرار الأزمنة» (نُشر 09:12)\n«قال الرحالة سالم بن نصر في مخطوطته: ‹بلغنا ساحلاً تحرسه الأمواج، وفيه مدينةٌ لا يراها إلا من جاء بلا سيف›. إنها مدينة الفيروز التي أخفاها التاريخ، والنص الأصلي يشهد!»\nكتبه: نبيل الخطيب، محرر الصفحة الثقافية\nعدد المشاركات: 4300",
  ["a_read_post"], ["f_post_published"], "weak",
  "منشور ثانوي يسوق اقتباساً بلا إحالة إلى فصل أو صفحة؛ لا يثبت وجود هذه الصيغة في المصدر.", red=True, loc="loc_page")
V("ev_trans_a", "الترجمة (أ) — الفصل الرابع «ركوب البحر»", "documentary",
  "الترجمة (أ)، الفصل الرابع «ركوب البحر»، ص 88:\n«ثم بلغنا ساحلاً تحرسه الأمواج، فرسونا عليه ثلاثة أيام نملأ الماء ونرمّم الشراع، وكان صخراً لا زرع فيه ولا أثر لساكن.»",
  ["a_get_trans_a"], ["f_two_places"], "moderate",
  "ترجمة لا أصل؛ تنقل مقطعاً واحداً من الفصل الرابع، وقد تختلف صياغتها عن غيرها في الألفاظ.", contradicts=["cl_salim_city"], loc="loc_library")
V("ev_trans_b", "الترجمة (ب) — الفصل التاسع «مقامات الصمت»", "documentary",
  "الترجمة (ب)، الفصل التاسع «مقامات الصمت»، ص 211:\n«ويضرب الشيخ مثلاً للقلب إذا تواضع، فيقول: كمدينةٍ لا يراها إلا من جاء بلا سيف، ولا يدخلها إلا من ترك الكبر عند بابها.»",
  ["a_get_trans_b"], ["f_two_places", "f_second_figurative"], "moderate",
  "ترجمة لا أصل؛ تنقل مقطعاً واحداً من الفصل التاسع، وتصف المقطع كما فهمه مترجمه.", loc="loc_library")
V("ev_facsimile", "النسخة المصورة للمخطوطة", "documentary",
  "فهرس النسخة المصورة لمخطوطة «نزهة الأسفار»:\nالورقة 14ب، السطر 3 — باب «في ركوب البحر»: قراءة السطر: «…ثم بلغنا ساحلاً حرسته الأمواج، فرسونا عليه…»\nالورقة 63أ، السطر 9 — باب «ما ضربه الشيخ مثلاً»: قراءة السطر: «…كمدينةٍ لا يراها إلا من جاء بلا سيف…»\nبين الموضعين 48 ورقة وثلاثة أبواب. لا علامة في المخطوطة تصل أحد الموضعين بالآخر.",
  ["a_get_facsimile"], ["f_two_places"], "strong",
  "نسخة مصورة لمخطوطة واحدة؛ تفيد في تحديد المواضع ولا تثبت وحدها ما أراده مؤلفها بها.", contradicts=["cl_salim_city"], loc="loc_ms")
V("ev_catalogue", "السجل الفهرسي للطبعات", "documentary",
  "السجل الفهرسي لمكتبة الأبحاث — «نزهة الأسفار»:\nالطبعة (أ): ترجمة، 1961، المترجم حمدان الريس.\nالطبعة (ب): ترجمة، 1989، المترجمة سوسن البدري.\nكلتا الطبعتين عن المخطوطة نفسها، وتتبعان ترتيب أبوابها.\nلا طبعة في المكتبة تضع عبارة الساحل وعبارة المدينة في موضع واحد.",
  ["a_get_catalogue"], ["f_no_joint_edition", "f_two_places"], "strong",
  "فهرس مكتبة واحدة؛ يصف ما تملكه وما سُجّل فيه ولا يحصي كل طبعة في العالم.", contradicts=["cl_nabil_original"], loc="loc_library")
V("ev_note_log", "ملف ملاحظات نبيل الخطيب", "digital",
  "ملف ملاحظات المقال — نبيل الخطيب\nبطاقة 1 — المصدر: الترجمة (أ)، الفصل الرابع، ص 88 — «ساحلاً تحرسه الأمواج»\nبطاقة 2 — المصدر: الترجمة (ب)، الفصل التاسع، ص 211 — «مدينةٌ لا يراها إلا من جاء بلا سيف»\nبطاقة 3 — «اقتباس للنشر»: نُسخت من البطاقتين ولُصقتا معاً، وأُنشئت 08:20\nملاحظة: «أراجع الأصل في المكتبة لاحقاً»",
  ["a_get_notes"], ["f_joined_by_writer", "f_composite_phrase"], "strong",
  "سجل خاص بصاحبه يثبت ترتيب عمله ومصدر كل بطاقة؛ لا يثبت سبب اختصاره الطريق.", contradicts=["cl_nabil_original"], loc="loc_desk")
V("ev_preface_b", "مقدمة المترجمة (ب)", "documentary",
  "من مقدمة الطبعة (ب):\n«اختلفت قراءتي عن الترجمة الأولى في ثلاث كلمات من الباب الأول، ولم يختلف النصان في الفصلين الرابع والتاسع. والفصل التاسع كله أمثال تضرب في تهذيب النفس، ولا يرد فيه وصف لرحلة أو مكان.»",
  ["a_get_preface"], ["f_second_figurative"], "moderate",
  "مقدمة صاحبة ترجمة تصف منهجها؛ تفيد في سياق الفصل وفي حدود الاختلاف بين الترجمتين، ولا تغني عن الرجوع إلى الأصل.", loc="loc_library")
V("ev_context_table", "جدول مقارنة سياق المقطعين", "lab_result",
  "جدول مقارنة السياق:\nالمقطع الأول: الفصل الرابع، باب السفر، وصف حسي: ساحل صخري بلا ساكن.\nالمقطع الثاني: الفصل التاسع، باب الأمثال، وصف مجازي: مثل لحال القلب.\nالسياقان مختلفان في النوع والموضع، ولا رابط نصياً بينهما في المخطوطة.",
  ["a_compare_passages"], ["f_two_places", "f_second_figurative"], "moderate",
  "ملخص مقارنة بين المقطعين كما ظهرا في الأدلة التي بين يديك؛ لا يغني عن الرجوع إلى المخطوطة نفسها.", contradicts=["cl_salim_city"], ko="KO-RS-05-004", loc="loc_library")
V("ev_amina_statement", "إفادة أمينة الصبّاغ (ملخص)", "testimonial",
  "ملخص إفادة أمينة الصبّاغ:\n«الطبعتان عن المخطوطة نفسها، والعبارتان في موضعين متباعدين. لم أجد طبعة تضعهما معاً. ولا أعرف من نشر المنشور.»",
  ["a_note_amina"], ["f_no_joint_edition"], "moderate",
  "إفادة موظفة مختصة عن حدود ما في الفهرس؛ تؤيد السجل ولا تحل محله.", loc="loc_library")
V("ev_rana_statement", "إفادة د. رنا العلي (ملخص)", "testimonial",
  "ملخص إفادة د. رنا العلي:\n«الفصل التاسع أمثال في تواضع النفس. والمدينة فيه صورة مجازية. لا أعرف من نشر المنشور ولا من ركّب الصيغة.»",
  ["a_note_rana"], ["f_second_figurative"], "moderate",
  "رأي مؤرخة مختصة في سياق نوع النص؛ يقاس بالنص نفسه وبما تقوله الطبعات.", loc="loc_library")
V("ev_nabil_statement", "إفادة نبيل الخطيب (ملخص)", "testimonial",
  "ملخص إفادة نبيل الخطيب:\n«نسخت العبارة الأولى من الترجمة (أ) والثانية من الترجمة (ب) ولصقتهما في بطاقة واحدة، وكنت أنوي مراجعة الأصل ولم أفعل.»",
  ["a_note_nabil"], ["f_joined_by_writer"], "weak",
  "إفادة صاحب الشأن بعد أن عُرض عليه ملفه؛ تؤيدها السجلات ولا تغني عنها.", loc="loc_desk")
V("ev_salim_statement", "إفادة سليم الفرّاء (ملخص)", "testimonial",
  "ملخص إفادة سليم الفرّاء:\n«لم أقرأ الكتاب. قرأت المنشور ورأيت فيه ساحلاً ثم مدينة، فاعتقدت أن المدينة حقيقية.»",
  ["a_note_salim"], ["f_salim_source"], "weak",
  "رأي متابع يعتمد على المنشور وحده؛ يصلح مثالاً لانتشار الاقتباس لا دليلاً على صحته.", loc="loc_page")

# ---------------------------------------------------------------- inferences
def P(t, i): return {"ref_type": t, "ref_id": i}
inf = []
def I(id, prem, ct, concl, rel, strength, rule, ks):
    inf.append({"id": id, "premises": prem, "conclusion": {"ref_type": ct, "ref_id": concl}, "relation": rel, "strength": strength, "rule_ar": rule, "skill_ko_refs": ks})
I("i_a_places", [P("evidence", "ev_trans_a"), P("evidence", "ev_trans_b")], "fact", "f_two_places", "establishes", "strong",
  "الترجمتان تذكران العبارتين في فصلين مختلفين (الرابع ص 88 والتاسع ص 211) وبعنوانين مختلفين؛ فهما ليستا من سياق واحد.", ["KO-RS-05-004"])
I("i_b_places", [P("evidence", "ev_facsimile"), P("evidence", "ev_catalogue")], "fact", "f_two_places", "establishes", "strong",
  "الفهرس يقول إن الطبعتين عن المخطوطة نفسها، وفهرس النسخة المصورة يضع الموضعين في الورقتين 14ب و63أ في بابين مختلفين بينهما 48 ورقة.", ["KO-RS-05-004", "KO-RS-05-001"])
I("i_a_comp", [P("evidence", "ev_post"), P("evidence", "ev_trans_a"), P("evidence", "ev_trans_b")], "fact", "f_composite_phrase", "establishes", "strong",
  "عبارة المنشور تجمع لفظ الترجمة (أ) ولفظ الترجمة (ب) بحرف وصل لا يرد في أي منهما، فهي صيغة موحدة ليست في أي من النصين.", ["KO-RS-06-017"])
I("i_b_comp", [P("evidence", "ev_note_log"), P("evidence", "ev_catalogue")], "fact", "f_composite_phrase", "establishes", "strong",
  "ملف الملاحظات يبيّن أن «الاقتباس» بطاقة لُصقت من بطاقتين من مصدرين، والفهرس لا يذكر طبعة تحمل الصيغة الموحدة؛ فالتركيب جاء من خارج الطبعات.", ["KO-RS-06-017", "KO-RS-05-004"])
I("i_figurative", [P("evidence", "ev_preface_b"), P("evidence", "ev_rana_statement")], "fact", "f_second_figurative", "establishes", "strong",
  "مقدمة المترجمة ورأي المؤرخة يتفقان على أن الفصل التاسع أمثال مجازية في تهذيب النفس، فالمدينة فيه صورة لا موضع.", ["KO-RS-05-001"])
I("i_salim_claim", [P("fact", "f_two_places"), P("fact", "f_second_figurative")], "claim", "cl_salim_city", "contradicts_claim", "strong",
  "العبارة الأولى في وصف سفر والثانية في مثل مجازي من فصل آخر؛ فليس في المخطوطة ساحل «فيه» مدينة، وهذا قفز من عبارتين إلى خبر واحد.", ["KO-RS-05-001", "KO-RS-05-007"])
I("i_nabil_claim", [P("fact", "f_composite_phrase")], "claim", "cl_nabil_original", "contradicts_claim", "strong",
  "القول إن الجملة وردت متصلة يخالف أن الصيغة الموحدة غير موجودة في أي طبعة وأنها لُصقت من بطاقتين؛ هو خطأ فهم من الكاتب لا ادعاء كاذب.", ["KO-RS-05-014"])
I("i_support_comp", [P("fact", "f_two_places"), P("fact", "f_composite_phrase")], "hypothesis", "h_composite", "supports", "strong",
  "عبارتان من فصلين مختلفين، تُركبان في جملة لا توجد في أي مصدر، تفسّر كل ما بين أيدينا: المنشور، والترجمتين، والمخطوطة، وملف الكاتب.", ["KO-RS-05-002"])
I("i_rule_history", [P("fact", "f_two_places"), P("fact", "f_composite_phrase")], "hypothesis", "h_history", "rules_out", "conclusive",
  "لا يصح أن يدعم الاقتباس حقيقة تاريخية وهو غير موجود بهذه الصيغة في أي مصدر، وعباراته من سياقين مختلفين.", ["KO-RS-06-008"])
I("i_rule_history_fig", [P("fact", "f_second_figurative")], "hypothesis", "h_history", "rules_out", "strong",
  "العبارة الثانية مثل مجازي في تهذيب النفس، فلا تُقرأ خبراً عن موضع جغرافي.", ["KO-RS-06-008"])
I("i_rule_worthless", [P("fact", "f_composite_phrase"), P("fact", "f_two_places")], "hypothesis", "h_worthless", "rules_out", "strong",
  "الترجمتان والمخطوطة والفهرس هي ما كشف التركيب نفسه؛ فالمصادر لم تكن عديمة القيمة، بل كانت سبيل التحقق.", ["KO-RS-06-008"])

# ---------------------------------------------------------------- character knowledge
K = lambda f, a="witnessed", c="certain": {"fact_id": f, "access": a, "certainty": c}
ck = [
    {"character_id": "amina", "knows": [K("f_has_trans_a", "professional"), K("f_has_trans_b", "professional"), K("f_has_facsimile", "professional"), K("f_has_catalogue", "professional"), K("f_no_joint_edition", "professional")], "hides": [], "believes": []},
    {"character_id": "rana", "knows": [K("f_second_figurative", "professional"), K("f_preface_exists", "professional")], "hides": [], "believes": []},
    {"character_id": "salim", "knows": [K("f_salim_source")], "hides": [], "believes": [{"claim_id": "cl_salim_city", "stance": "sincere"}]},
    {"character_id": "nabil", "knows": [K("f_notes_exist"), K("f_joined_by_writer")],
     "hides": [{"fact_id": "f_joined_by_writer", "reveal_when": {"presented": {"evidence_id": "ev_note_log", "to_character": "nabil"}}, "cover_claim_id": None, "reveal_line_id": "nb_joined"}],
     "believes": [{"claim_id": "cl_nabil_original", "stance": "sincere"}]},
]
hyps = [
    {"id": "h_history", "statement_ar": "الاقتباس نص أصلي واحد، فهو يدعم وجود مدينة مفقودة حقيقية.", "is_true": False, "plausibility_at_start": "high"},
    {"id": "h_composite", "statement_ar": "الاقتباس مركب من عبارتين متباعدتين ومضلل، والمصادر الأصلية لا تدعم وجود المدينة.", "is_true": True, "plausibility_at_start": "low", "suspect_id": "nabil"},
    {"id": "h_worthless", "statement_ar": "كل المصادر التاريخية بلا قيمة، فلا يمكن معرفة شيء عن الرحلة.", "is_true": False, "plausibility_at_start": "medium"},
]
mis = [
    {"id": "rh_post", "points_to_hypothesis_id": "h_history", "planted_via_ar": "المنشور يضع «ساحلاً» و«مدينة» في جملة واحدة وينسبها إلى المخطوطة ويجمع آلاف المشاركات.", "evidence_ids": ["ev_post"],
     "refuted_by_inference_ids": ["i_rule_history", "i_rule_history_fig", "i_a_comp", "i_salim_claim"],
     "fairness_note_ar": "الترجمتان مع الفصلين وصفحاتهما في متناول اللاعب، وكذلك فهرس النسخة المصورة وملف الكاتب؛ لا يتطلب الحل غير مقارنة الألفاظ والمواضع."},
    {"id": "rh_preface", "points_to_hypothesis_id": "h_worthless", "planted_via_ar": "مقدمة المترجمة تعترف باختلاف قراءتها عن الترجمة الأولى في ثلاث كلمات، فيبدو أن النصوص غير مستقرة.", "evidence_ids": ["ev_preface_b"],
     "refuted_by_inference_ids": ["i_rule_worthless"],
     "fairness_note_ar": "المقدمة نفسها تنص على أن النصين لم يختلفا في الفصلين الرابع والتاسع، فالاختلاف المذكور لا يمس المقطعين محل البحث."},
]
los = [
    {"id": "lo_claim", "statement_ar": "يفرّق بين الاقتباس الثانوي والنص الأصلي والفهرس، ويصنف مصدر كل معلومة.", "skill_ko_ref": "KO-RS-05-001", "observable_behaviors_ar": ["يصنّف المصادر", "يقابل الاقتباس بالأصل"], "evidence_sources": ["evidence_board"]},
    {"id": "lo_timeline", "statement_ar": "يرتّب مراحل صنع الاقتباس ونشره ليعرف متى وُجدت الصيغة الموحدة.", "skill_ko_ref": "KO-RS-05-005", "observable_behaviors_ar": ["يضع ملف الملاحظات والمنشور في موضعيهما"], "evidence_sources": ["timeline_task", "action_log"]},
    {"id": "lo_hyp", "statement_ar": "يوازن بين فرضيتين على الأقل ويستبعد ما تنقضه الأدلة، ومنها التشكيك الشامل.", "skill_ko_ref": "KO-RS-05-002", "observable_behaviors_ar": ["يضيف فرضيات", "يستبعد بدليل"], "evidence_sources": ["hypothesis_ledger"]},
    {"id": "lo_diag", "statement_ar": "يقدّر ما يثبته كل مصدر وما لا يثبته، ويربط الدليل بالفرضية باتجاه صحيح.", "skill_ko_ref": "KO-RS-06-001", "observable_behaviors_ar": ["يقارن سياق المقطعين", "يربط الدليل بالفرضية"], "evidence_sources": ["evidence_board", "final_justification"]},
    {"id": "lo_calib", "statement_ar": "يصوغ نسبة الترجيح بحدودها.", "skill_ko_ref": "KO-RS-06-021", "observable_behaviors_ar": ["يختار ثقة معقولة", "يذكر حدوداً"], "evidence_sources": ["final_justification"]},
    {"id": "lo_revise", "statement_ar": "يراجع رأيه الأول حين يظهر ما يخالفه.", "skill_ko_ref": "KO-RS-06-009", "observable_behaviors_ar": ["يغيّر فرضيته الرائدة بدليل"], "evidence_sources": ["hypothesis_ledger"]},
]
def levels(d): return [{"score": i, "descriptor_ar": t} for i, t in enumerate(d)]
rub = {
    "reference_answer_ar": "الاقتباس المنسوب إلى الرحالة ليس نصاً واحداً. عبارة الساحل في الفصل الرابع (ص 88 في الترجمة أ، والورقة 14ب في المصورة)، وعبارة المدينة مثل مجازي في الفصل التاسع (ص 211 في الترجمة ب، والورقة 63أ)، وتفصل بينهما أبواب وأوراق كثيرة. ركّب المحرر الصيغة الموحدة بنسخ العبارتين من ترجمتين ولصقهما في بطاقة قبل النشر الساعة 08:20، ولا توجد هذه الصيغة في أي طبعة. لا يدعم المصدر الأصلي وجود مدينة مخفية، لكن المصادر نفسها صالحة للتحقق منها. حدود الاستنتاج: لا ينفي هذا وجود مدينة حقيقية بأدلة أخرى، ولم نفحص إلا ما في المكتبة، ولا نعرف نية المحرر.",
    "criteria": [
        {"id": "c_source", "name_ar": "تصنيف المصادر", "objective_ids": ["lo_claim"], "scored_by": "deterministic", "weight": 0.15, "levels": levels(["لم يصنّف", "أخطأ في الأغلب", "نصف صحيح", "معظمه صحيح", "كله صحيح"])},
        {"id": "c_conflict", "name_ar": "ترتيب مراحل صنع الاقتباس", "objective_ids": ["lo_timeline"], "scored_by": "deterministic", "weight": 0.25, "levels": levels(["لم يضع شيئاً", "وضع قليلاً", "وضع نصفها صحيحاً", "معظمها", "كلها في موضعها"])},
        {"id": "c_links", "name_ar": "ربط الأدلة بالفرضيات", "objective_ids": ["lo_diag"], "scored_by": "deterministic", "weight": 0.15, "levels": levels(["لا روابط", "قليلة", "نصفها صحيح", "معظمها", "كلها دقيقة"])},
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
    H("hg1", 1, "metacognitive", "أين ينتهي ما قاله المصدر وتبدأ طريقة من نقله في عرضه؟", {"always": True}, None, 0.02),
    H("hg2", 2, "focus_area", "ضع كل معلومة في جدول: أصل مصوَّر، أم ترجمة، أم منشور، أم فهرس؟", he("ev_post"), None, 0.04),
    H("hg3", 3, "pointer", "راجع تحديداً موضع كل عبارة في الكتاب: في أي فصل وفي أي صفحة؟", he("ev_post"), None, 0.08),
    H("hc1", 1, "metacognitive", "هل ترد عبارة المنشور بحروفها متصلة في أي مصدر عندك؟", he("ev_trans_b"), "i_a_comp", 0.02),
    H("hc2", 2, "pointer", "قارن لفظ المنشور بلفظ الترجمة (أ) ثم بلفظ الترجمة (ب)، وانتبه إلى ما يصل بينهما.", he("ev_trans_b"), "i_a_comp", 0.06),
    H("hc3", 3, "partial_reveal", "ضع الفصلين وصفحتيهما جنباً إلى جنب، وستعرف أن ما اتصل في المنشور لم يتصل في الكتاب.", he("ev_trans_b"), "i_a_comp", 0.1),
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
Act("a_read_post", "examine", "اقرأ المنشور المتداول", al, [G("ev_post")], "loc_page", "READ_POST")
for cid, lab in [("amina", "أمينة المكتبة"), ("nabil", "نبيل"), ("rana", "د. رنا"), ("salim", "سليم")]:
    Act(f"a_int_{cid}", "interview", f"ابدأ مقابلة {lab}", al, [{"op": "raise_trust", "ref_id": cid, "amount": 1}], cid, f"INT_{cid.upper()}")
Act("a_get_trans_a", "examine", "اطلب الترجمة (أ)، الفصل الرابع", fu("f_has_trans_a"), [G("ev_trans_a")], "loc_library", "GET_TRANS_A")
Act("a_get_trans_b", "examine", "اطلب الترجمة (ب)، الفصل التاسع", fu("f_has_trans_b"), [G("ev_trans_b")], "loc_library", "GET_TRANS_B")
Act("a_get_facsimile", "examine", "اطلب فهرس النسخة المصورة", fu("f_has_facsimile"), [G("ev_facsimile")], "loc_ms", "GET_FACSIMILE")
Act("a_get_catalogue", "examine", "اطلب السجل الفهرسي للطبعات", fu("f_has_catalogue"), [G("ev_catalogue")], "loc_library", "GET_CATALOGUE")
Act("a_get_notes", "examine", "اطلب ملف ملاحظات نبيل", fu("f_notes_exist"), [G("ev_note_log")], "loc_desk", "GET_NOTES")
Act("a_get_preface", "examine", "اقرأ مقدمة الطبعة (ب)", fu("f_preface_exists"), [G("ev_preface_b")], "loc_library", "GET_PREFACE")
Act("a_compare_passages", "request_lab_test", "قارن سياق المقطعين", {"all": [he("ev_trans_a"), he("ev_trans_b"), he("ev_facsimile")]}, [G("ev_context_table")], "loc_library", "COMPARE_PASSAGES")
Act("a_note_amina", "examine", "دوّن إفادة أمينة", fu("f_no_joint_edition"), [G("ev_amina_statement")], "amina", "NOTE_AMINA")
Act("a_note_rana", "examine", "دوّن إفادة د. رنا", fu("f_second_figurative"), [G("ev_rana_statement")], "rana", "NOTE_RANA")
Act("a_note_nabil", "examine", "دوّن إفادة نبيل", fu("f_joined_by_writer"), [G("ev_nabil_statement")], "nabil", "NOTE_NABIL")
Act("a_note_salim", "examine", "دوّن إفادة سليم", fu("f_salim_source"), [G("ev_salim_statement")], "salim", "NOTE_SALIM")
Act("p_notes_nabil", "present_evidence", "اعرض ملف الملاحظات على نبيل", {"presented": {"evidence_id": "ev_note_log", "to_character": "nabil"}}, [{"op": "emit_event", "ref_id": "PRESENTED_NOTES"}], "nabil", "P_NOTES_NABIL", 0)
Act("a_hint", "request_hint", "اطلب تلميحاً", al, [], None, "REQUEST_HINT", 0)
Act("a_accuse", "final_accusation", "قدّم الاستنتاج النهائي", al, [{"op": "emit_event", "ref_id": "SUBMIT"}], None, "FINAL_ACCUSATION", 0)

topics = [
    {"id": "t_editions", "label_ar": "النسخ والطبعات", "example_questions_ar": ["أي ترجمات عندكم؟", "هل لديكم نسخة مصورة؟", "هل يوجد سجل بالطبعات؟"], "fact_ids": ["f_has_trans_a", "f_has_trans_b", "f_has_facsimile", "f_has_catalogue"]},
    {"id": "t_joint", "label_ar": "هل العبارتان معاً في طبعة؟", "example_questions_ar": ["هل في أي طبعة العبارتان متجاورتان؟"], "fact_ids": ["f_no_joint_edition"]},
    {"id": "t_context", "label_ar": "سياق الفصل التاسع", "example_questions_ar": ["ما نوع الفصل التاسع؟", "هل من مقدمة تشرح منهج الترجمة؟"], "fact_ids": ["f_second_figurative", "f_preface_exists"]},
    {"id": "t_writing", "label_ar": "كيف كُتب الاقتباس", "example_questions_ar": ["من أين نقلت الجملة؟", "هل تحتفظ بملف ملاحظات؟", "كيف جمعت العبارتين؟"], "fact_ids": ["f_notes_exist", "f_joined_by_writer"], "claim_ids": ["cl_nabil_original"]},
    {"id": "t_theory", "label_ar": "نظرية المدينة", "example_questions_ar": ["من أين عرفت الجملة؟", "ماذا تعني لك المدينة؟"], "fact_ids": ["f_salim_source"], "claim_ids": ["cl_salim_city"]},
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
    (1, "الترجمتان تضعان العبارتين في فصلين مختلفين (الرابع ص 88 والتاسع ص 211)، وفهرس المصورة يضعهما في الورقتين 14ب و63أ بين بابين وبينهما 48 ورقة.", ["ev_trans_a", "ev_trans_b", "ev_facsimile", "ev_catalogue"], "i_b_places"),
    (2, "عبارة الساحل وصف سفر صخري بلا ساكن، وعبارة المدينة مثل مجازي في تواضع النفس؛ فلا يصلهما سياق واحد ولا تثبتان مدينة.", ["ev_preface_b", "ev_rana_statement", "ev_trans_a"], "i_figurative"),
    (3, "عبارة المنشور تجمع لفظ الترجمة (أ) ولفظ الترجمة (ب) بحرف وصل لا يرد في أي منهما.", ["ev_post", "ev_trans_a", "ev_trans_b"], "i_a_comp"),
    (4, "ملف الملاحظات يبيّن أن «الاقتباس» بطاقة لُصقت 08:20 من بطاقتين من مصدرين، قبل نشر المنشور 09:12، والفهرس لا يذكر طبعة بالصيغة الموحدة.", ["ev_note_log", "ev_catalogue", "ev_post"], "i_b_comp"),
    (5, "إذن الاقتباس مركب ومضلل لا مزوّر عن عمد: كاتبه أراد مراجعة الأصل لاحقاً ولم يفعل.", ["ev_note_log", "ev_nabil_statement"], "i_support_comp"),
    (6, "ولا يعني ذلك أن المصادر بلا قيمة، فالمصادر نفسها هي التي كشفت التركيب.", ["ev_facsimile", "ev_catalogue", "ev_preface_b"], "i_rule_worthless"),
]
ending = {
    "steps": [{"order": o, "text_ar": t, "uses_evidence_ids": u, "inference_id": i} for o, t, u, i in steps],
    "alternative_paths_ar": [
        "يمكن الوصول إلى النتيجة من الترجمتين والمنشور وحدها دون المخطوطة، لكن من يفعل ذلك لا يعرف إن كان المترجمان نقلا الموضعين بأمانة.",
        "ويمكن الوصول إليها من فهرس النسخة المصورة وملف الملاحظات والسجل الفهرسي دون الترجمتين؛ والأقوى أن يتفق المساران.",
    ],
    "what_evidence_could_not_show_ar": [
        "لا ينفي هذا وجود مدينة حقيقية بأدلة أخرى؛ هو ينفي أن هذا الاقتباس يثبتها.",
        "اقتصر الفحص على الطبعتين والنسخة المصورة المتاحة، ولا يستبعد وجود نسخة أخرى لم تُفحص.",
        "لا تبيّن الأدلة قصد المحرر؛ تبيّن ما فعله لا لماذا فعله.",
    ],
    "science_notes_ar": [
        "الاقتباس الصحيح له إحالة: عنوان وفصل وصفحة، فإن غابت الإحالة فابحث عن الموضع قبل أن تصدق.",
        "الاختلاف بين مصدرين لا يعني أن أحدهما كاذب، وبطلان الثقة بكل المصادر ليس نتيجة منطقية لخطأ في واحد منها.",
        "حفظ النسخ الأصلية ومن تناولها يسمى سلسلة العهدة، وهو ما يجعل المقارنة بين النص الأصلي ونسخه ممكنة، وترتبط به نسبة الترجيح التي نمنحها لأي ادعاء.",
    ],
}
core = {
    "schema_version": "0.1.0", "case_id": CID, "case_version": "0.1.0",
    "meta": {"title_ar": "المخطوطة والاقتباس المقلوب", "title_en": "The Manuscript and the Stitched Quote", "age_band": "16-18", "locale": "ar", "dialogue_register": "msa", "estimated_minutes": 25, "difficulty": 2,
             "content_flags": ["no_violence", "historical"], "authors": ["فريق أثر التحريري (مسودة بمساعدة الذكاء الاصطناعي، لم تُراجَع بشرياً بعد)"],
             "knowledge_object_refs": ["KO-RS-05-001", "KO-RS-05-005", "KO-RS-05-002", "KO-RS-06-001", "KO-RS-06-009", "KO-RS-06-021"]},
    "premise": {"hook_ar": "جملة واحدة تتناقلها الصفحات منسوبة إلى رحالة قديم، وعليها تقوم نظرية كاملة عن مدينة مفقودة.",
                "player_role_ar": "أنت باحث توثيق في مكتبة الأبحاث، وطُلب منك أن تحقق في الجملة المنسوبة إلى سالم بن نصر قبل أن يستند إليها أحد.",
                "setting_ar": "مكتبة أبحاث في مدينة معاصرة، وصباح يوم نُشر فيه المنشور. المخطوطة ومؤلفها وكل الأسماء خيالية.",
                "public_fact_ids": ["f_post_published", "f_fan_theory", "f_writer_says"],
                "assumed_general_knowledge_ar": ["الترجمة نص ثانوي منقول عن الأصل", "الاقتباس الموثق يُحال إلى فصل وصفحة"]},
    "entities": {"characters": chars, "locations": locations, "objects": objects, "organizations": orgs},
    "truth": {"solution": {"culprit_ids": ["nabil"], "summary_ar": "الجملة المنشورة ليست نصاً واحداً في الرحلة. ركّبها محرر الصفحة من عبارتين بنصّي ترجمتين مختلفتين، وكل منهما في فصل مستقل، والثانية مثل مجازي. لا تدعم المصادر وجود مدينة مخفية، لكنها هي التي أتاحت كشف التركيب.", "key_fact_ids": ["f_two_places", "f_composite_phrase"]},
              "facts": facts, "claims": claims},
    "timeline": timeline, "evidence": ev, "evidence_graph": {"inferences": inf},
    "character_knowledge": ck, "hypotheses": hyps, "misdirection_plan": mis, "learning_objectives": los,
    "mechanics": {"time_budget_units": 40, "actions": A},
    "state_machine": {"id": "c009", "initial": "briefing", "type": "compound", "states": {
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
    "clock": {"epoch_hhmm": "07:00", "zone_label_ar": "توقيت مكتب الصفحة الثقافية"},
    "cover": {"title_ar": "المخطوطة والاقتباس المقلوب", "tagline_ar": "جملة واحدة، ومدينة مفقودة، وسطران لا يلتقيان في الكتاب", "kicker_ar": "الملف التاسع · نقد المصادر", "glyph": "❦", "accent": "amber"},
    "cold_open_ar": ["صباح يوم الأحد.", "صفحة ثقافية شعبية تنشر جملة منسوبة إلى رحالة قديم، وتقول إن «النص الأصلي يشهد» بوجود مدينة أخفاها التاريخ.",
                     "آلاف المشاركات، ومتابع متحمس يقول إن الجملة واضحة وضوح الشمس.",
                     "المنشور لا يذكر فصلاً ولا صفحة. فما الذي يمكنك أن تتحقق منه قبل أن تحكم؟"],
    "labs": [],
    "source_classes": [
        {"id": "primary_record", "label_ar": "سجل أصلي", "help_ar": "يُنتجه صاحبه لحظة العمل دون وسيط، كنسخة مصورة للمخطوطة أو ملف ملاحظات."},
        {"id": "redisplay", "label_ar": "نسخة معروضة", "help_ar": "نص أُعيد عرضه أو ترجمته عن مصدر آخر، كاقتباس منشور أو ترجمة."},
        {"id": "claim", "label_ar": "قول أو تصريح", "help_ar": "إفادة شخص؛ تُقاس بالنصوص والسجلات لا بنبرة صاحبها."},
        {"id": "template", "label_ar": "قالب أو نموذج", "help_ar": "نص جاهز لا يصف الحدث الفعلي بذاته."},
        {"id": "public_document", "label_ar": "وثيقة منشورة", "help_ar": "وثيقة معلنة ومعروف ناشرها، كفهرس مكتبة أو طبعة مترجمة بمقدمتها."}],
    "limit_menu": [
        {"id": "l_no_city_proof", "label_ar": "الأدلة تنفي أن هذه الصيغة تثبت المدينة، ولا تنفي وجود مدينة حقيقية بأدلة أخرى"},
        {"id": "l_scope", "label_ar": "الفحص اقتصر على الطبعتين والنسخة المصورة المتاحة، ولا يستبعد وجود نسخة أخرى لم تُفحص"},
        {"id": "l_intent", "label_ar": "الأدلة لا تثبت قصد المحرر، بل ما فعله فقط"},
        {"id": "l_invalid_diff", "label_ar": "اختلاف الترجمتين في الألفاظ يعني أن الأصل مزوَّر"},
        {"id": "l_invalid_viral", "label_ar": "كثرة مشاركات المنشور ترجّح صدق الاقتباس"}],
    "mind_change_menu": [
        {"id": "m_other_ms", "label_ar": "ظهور مخطوطة أخرى مستقلة تجمع العبارتين في سياق واحد"},
        {"id": "m_edition", "label_ar": "ظهور طبعة موثّقة تضع العبارتين متجاورتين بالصيغة الموحدة"},
        {"id": "m_notes_late", "label_ar": "ثبوت أن ملف الملاحظات أُنشئ بعد نشر المنشور لا قبله"},
        {"id": "m_viral", "label_ar": "ارتفاع عدد من يشاركون المنشور"}],
    "transfer": {
        "id": "tr_unit", "title_ar": "اختبار نقل المهارة: رسالة البحّار",
        "scenario_ar": "جملة تُنسب إلى بحّار قديم في رسالة خيالية لا علاقة لها بالقضية. أمامك وثيقتان تنقلان الجملة نفسها بوصفين مختلفين.",
        "documents": [
            {"title_ar": "مقال صحفي", "body_ar": "«كتب البحّار: سرنا في اليوم الواحد عشرة أميال.»"},
            {"title_ar": "طبعة علمية للرسالة", "body_ar": "«كتب البحّار: سرنا في اليوم الواحد عشرة فراسخ.» هامش المحقق: الفرسخ وحدة قديمة يختلف مقدارها بين المدن، وقد يعني هنا مسافة البحر المعتادة."}],
        "prompt_ar": "اختر الخطوات التي تصلح لمعرفة ما قصده البحّار (يمكنك اختيار أكثر من خطوة).",
        "options": [
            {"id": "o1", "text_ar": "طلب صورة الرسالة الأصلية أو قراءتها المحققة"},
            {"id": "o2", "text_ar": "معرفة ما تعنيه الوحدة المذكورة في زمن الرسالة ومكانها"},
            {"id": "o3", "text_ar": "تمييز ما هو نص الرسالة وما هو تعليق المحقق أو الصحفي"},
            {"id": "o4", "text_ar": "البحث عن نص ثالث مستقل يذكر المسافة نفسها"},
            {"id": "o5", "text_ar": "أخذ متوسط العددين"},
            {"id": "o6", "text_ar": "تفضيل المقال لأنه أحدث نشراً"},
            {"id": "o7", "text_ar": "اعتبار الوثيقتين باطلتين لأنهما تختلفان"}],
        "free_text_prompt_ar": "اكتب في ثلاثة أسطر كيف تقرّر نسبة الترجيح لما قصده البحّار، وما الذي ينقصك.",
    },
    "skills": [{"skill_id": "KO-RS-05-001", "track": "B"}, {"skill_id": "KO-RS-05-005", "track": "B"}, {"skill_id": "KO-RS-05-002", "track": "D"}, {"skill_id": "KO-RS-06-001", "track": "C"}],
    "stage_hooks_ar": {"briefing": "جملة تُنسب إلى رحالة… فأين هي في كتابه؟", "investigating": "لا تسأل هل الاقتباس جميل، اسأل: أين موضعه؟", "review": "قبل أن تغلق الملف: ما الذي لم تفحصه؟", "resolved": "أُغلق الملف. الدرس: لكل اقتباس مكان في كتاب."},
    "character_glyphs": {"amina": "أ", "nabil": "ن", "rana": "ر", "salim": "س"},
}
sc = {
    "case_id": CID,
    "accepted_conclusions": {"h_composite": {"grade": 1, "note_ar": "استنتاج متسق مع الأدلة ويتطلب ذكر حدوده."},
                             "h_history": {"grade": 0, "note_ar": "يعامل منشوراً ثانوياً على أنه نص أصلي ويتجاهل موضع العبارتين."},
                             "h_worthless": {"grade": 0, "note_ar": "يقفز من اختلاف الصياغة إلى بطلان كل المصادر، والمصادر هي التي كشفت التركيب."}},
    "confidence_band": {"h_composite": [65, 92], "h_history": [0, 15], "h_worthless": [0, 15]},
    "source_key": {"ev_post": "redisplay", "ev_trans_a": "redisplay", "ev_trans_b": "redisplay", "ev_facsimile": "primary_record", "ev_catalogue": "public_document",
                   "ev_note_log": "primary_record", "ev_preface_b": "public_document",
                   "ev_amina_statement": "claim", "ev_rana_statement": "claim", "ev_nabil_statement": "claim", "ev_salim_statement": "claim"},
    "link_key": {
        "h_composite": {"ev_facsimile": "supports", "ev_catalogue": "supports", "ev_note_log": "supports", "ev_trans_a": "supports", "ev_trans_b": "supports", "ev_preface_b": "supports", "ev_context_table": "supports", "ev_rana_statement": "supports", "ev_post": "neutral"},
        "h_history": {"ev_post": "supports", "ev_salim_statement": "neutral", "ev_facsimile": "weakens", "ev_trans_a": "weakens", "ev_trans_b": "weakens", "ev_note_log": "weakens", "ev_catalogue": "weakens", "ev_context_table": "weakens"},
        "h_worthless": {"ev_preface_b": "supports", "ev_facsimile": "weakens", "ev_catalogue": "weakens", "ev_trans_a": "weakens", "ev_trans_b": "weakens"},
    },
    "required_limits": ["l_no_city_proof", "l_scope"], "valid_mind_changers": ["m_other_ms", "m_edition", "m_notes_late"],
    "invalid_limits": ["l_invalid_diff", "l_invalid_viral"],
    "decisive_evidence": ["ev_facsimile", "ev_catalogue", "ev_note_log", "ev_trans_a", "ev_trans_b"],
    "lab_requirement": None,
    "timeline_requirement": [{"evidence_id": "ev_note_log", "utc_minute": 80, "tol": 3}, {"evidence_id": "ev_post", "utc_minute": 132, "tol": 3}],
    "refuted_hypotheses": ["h_history", "h_worthless"],
    "criteria_map": {"c_source": "source_typing", "c_conflict": "conflict_resolution", "c_links": "hypothesis_links", "c_uncertainty": "uncertainty", "c_revision": "revision", "c_elimination": "elimination", "c_justification": "justification_human"},
    "transfer_key": {"valid": ["o1", "o2", "o3", "o4"], "invalid": ["o5", "o6", "o7"]},
    "caps": {"no_citations_max": 45, "no_conflict_resolution_max": 70},
}
os.makedirs(OUT, exist_ok=True)
for suf, obj in [("", core), (".ui", ui), (".scoring", sc)]:
    with open(os.path.join(OUT, f"{CID}{suf}.json"), "w", encoding="utf8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
print("ok")
