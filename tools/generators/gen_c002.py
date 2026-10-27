#!/usr/bin/env python3
# Case c002 «المخطوطة التي اختفت مرتين» — identity-vs-name case. Teaches: a shared short name / local number is not identity,
# compare the unique identifier before blaming anyone, and go back to the original card rather than a cropped snapshot.
# No-culprit convention: the person whose shortcut caused the unintended confusion (the cataloguer) is recorded as culprit_ids.
# Usage: gen_c002.py OUT_DIR
import json, sys, os
OUT = sys.argv[1]
CID = "c002_manuscript_twice"

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

ch("layla", "د. ليلى القاسمي", "victim", "أمينة المعرض، في أواخر الأربعينات",
   "دقيقة وغيورة على المقتنيات، تعوّدت أن تسمع كلمة «الأصل» مفردة فتتوقع شيئاً واحداً بهذا الاسم.",
   ["أن تعرف أين الأصل فعلاً قبل افتتاح المعرض", "ألا يُتّهم أحد من فريقها دون سند"],
   [L("ly_greet", "greeting", "أهلاً بك. في ملفي وثيقتان تتحدثان عن «الأصل»، ولا أفهم كيف يكون في مكانين."),
    L("ly_complaint", "reveal", "كتبتُ مذكرة أبيّن فيها أن السجل الموحّد يضع الأصل في الترميم صباحاً وفي القاعة عصراً.", ["f_layla_complaint"]),
    L("ly_clip", "reveal", "عندي قصاصة من نشرة المتحف نشرنا فيها بطاقة «الأصل» كما وصلتنا. يمكنك الاطلاع عليها.", ["f_layla_clip"]),
    L("ly_twice", "reveal", "أظن أن الأصل اختفى ثم عاد، أو أن أحداً بدّله ثم أعاده. لا أرى تفسيراً آخر الآن.", None, ["cl_layla_twice"]),
    L("ly_unknown", "deflect_unknown", "ليس لدي دليل يدعم ذلك."),
    L("ly_off", "deflect_offtopic", "فلنعد إلى الأصل وبطاقاته، فهذا ما يهمني الآن."),
    L("ly_bye", "farewell", "أرجو أن تقرأ الأوراق قبل أن تحكم على أحد.")],
   ["اتهام موظف بنية معيّنة دون دليل"])
ch("mona", "منى الصيرفي", "suspect", "فنية فهرسة في أوائل الثلاثينات",
   "مجتهدة وتعمل تحت ضغط الموعد، وتخشى أن يُنسب إليها خطأ حين يتعطل نظام جديد.",
   ["ألا تُلام على التباس السجل", "أن تنهي الإدخال قبل الإغلاق"],
   [L("mn_greet", "greeting", "تفضّل. كان يوم نقل الفهرسة طويلاً، وسأقول ما دوّنته."),
    L("mn_memo", "reveal", "كتبتُ مذكرة لرئيس القسم أنبّه فيها إلى أن الاسم المختصر والرقم المحلي لا يكفيان للتمييز بين النسخ.", ["f_memo_exists"]),
    L("mn_migration", "reveal", "في قائمة المراجعة يوم النقل سجّلنا البطاقات التي وجدناها والتي لم نجدها.", ["f_migration_list"]),
    L("mn_nochange", "lie", "لم أغيّر شيئاً في الوصف. نقلتُ البطاقات كما وجدتها.", None, ["cl_mona_nochange"]),
    L("mn_refuse", "refuse_secret", "لا أرى أن في هذا ما يفيد الملف."),
    L("mn_break", "break_down", "نعم... لم أجد بطاقة وصف A-114 قبل الإغلاق، فنسخت وصف B-114 إلى السجل الموحّد مؤقتاً لأكمل الإدخال. نويت أن أصحّحه ثم نسيت أن أعلّمه.", ["f_desc_reused"]),
    L("mn_unknown", "deflect_unknown", "ليس لدي دليل يدعم ذلك."),
    L("mn_off", "deflect_offtopic", "اسألني عن الفهرسة والبطاقات فقط."),
    L("mn_bye", "farewell", "كنت أتمنى لو علّمتُ ذلك الإدخال.")],
   ["اتهام زملاء دون سند"])
ch("saeed", "سعيد الخطيب", "witness", "أمين السجلات في الأربعينات",
   "منظّم وقليل الكلام، يعتمد على الدفاتر ولا يعتمد على الذاكرة.",
   ["أن تبقى سجلات الجرد والنقل سليمة"],
   [L("sd_greet", "greeting", "السجلات أمامي. أقول ما فيها."),
    L("sd_ledger", "reveal", "سجل الجرد يدوّن مكان كل نسخة برقم حفظها الكامل، ويمكنني إخراج صفحة يوم النقل.", ["f_ledger_exists"]),
    L("sd_transfer", "reveal", "نقل المخطوطات إلى القاعة يُدوَّن في محضر يوقّعه اثنان.", ["f_transfer_exists"]),
    L("sd_vault", "reveal", "دخول مخزن المخطوطات يُسجَّل في دفتر الدخول، وهو متاح.", ["f_vault_log_exists"]),
    L("sd_unknown", "deflect_unknown", "ليس لدي دليل يدعم ذلك."),
    L("sd_off", "deflect_offtopic", "اسألني عن الجرد والنقل والمخزن."),
    L("sd_bye", "farewell", "الدفاتر تبقى حيث هي.")])
ch("hasan", "حسن المرمّم", "witness", "مرمّم مخطوطات في مشغل خارجي",
   "هادئ وعملي، يصف ما أمامه بالتفصيل ولا يتحدث عمّا لم يرَه.",
   ["أن يُسلَّم العمل في موعده"],
   [L("hs_greet", "greeting", "أهلاً. نعرف ما استلمناه فقط."),
    L("hs_intake", "reveal", "استلمنا من المتحف نسخة واحدة صباح الاثنين، وسجّلنا حالتها وأوصافها في استمارة استلام بإيصال مرقّم.", ["f_intake_exists"]),
    L("hs_unknown", "deflect_unknown", "ليس لدي دليل يدعم ذلك."),
    L("hs_off", "deflect_offtopic", "لا أعرف شيئاً عن القاعة ولا عن الفهرسة."),
    L("hs_bye", "farewell", "النسخة ما زالت عندنا إلى أن يتم العمل.")])

locations = [{"id": "loc_catalog", "name_ar": "قسم الفهرسة", "description_ar": "البطاقات الورقية والنظام الجديد."},
             {"id": "loc_registry", "name_ar": "سجلات المتحف", "description_ar": "الجرد ومحاضر النقل."},
             {"id": "loc_vault", "name_ar": "مخزن المخطوطات", "description_ar": "حفظ النسخ خارج العرض."},
             {"id": "loc_hall", "name_ar": "قاعة العرض", "description_ar": "الصندوق الزجاجي الذي تُعرض فيه المخطوطة."},
             {"id": "loc_studio", "name_ar": "مشغل الترميم الخارجي", "description_ar": "مشغل يستلم النسخ المتعاقد على ترميمها."}]
objects = [{"id": "obj_copy_a", "name_ar": "نسخة «رحلة الوراق» رقم A-114", "description_ar": "نسخة من مجموعة الوقف القديم."},
           {"id": "obj_copy_b", "name_ar": "نسخة «رحلة الوراق» رقم B-114", "description_ar": "نسخة من مجموعة المدرسة العتيقة."}]
orgs = [{"id": "org_museum", "name_ar": "متحف الوراقين", "description_ar": "متحف خيالي للتراث والمخطوطات."}]

facts = []
def F(id, st, kind, subj, spoiler, time=None, loc=None, ko=None):
    d = {"id": id, "statement_ar": st, "kind": kind, "subject_ids": subj, "spoiler_level": spoiler}
    if time: d["time"] = time
    if loc: d["location_id"] = loc
    if ko: d["science_ko_refs"] = ko
    facts.append(d)
# public
F("f_catalog_shows_both", "يضع السجل الموحّد لمخطوطة «رحلة الوراق» موقعين لها في اليوم نفسه: الترميم الخارجي ثم قاعة العرض.", "event", ["org_museum"], 0)
F("f_layla_suspects", "تظن أمينة المعرض أن الأصل اختفى أو بُدّل ثم أُعيد.", "attribute", ["layla"], 0)
F("f_hall_label", "بطاقة العرض في القاعة تقول إن «الأصل» معروض.", "state", ["loc_hall"], 0)
# evidence-level facts
F("f_card_a_id", "تحمل بطاقة مجموعة الوقف القديم رقم الحفظ A-114.", "attribute", ["obj_copy_a"], 1, None, "loc_catalog")
F("f_card_b_id", "تحمل بطاقة مجموعة المدرسة العتيقة رقم الحفظ B-114.", "attribute", ["obj_copy_b"], 1, None, "loc_catalog")
F("f_a_out", "خرجت النسخة A-114 إلى الترميم الخارجي نحو الساعة 09:10 بإيصال مرقّم.", "event", ["obj_copy_a", "hasan"], 1, T(70), "loc_studio")
F("f_a_plain", "سجّل المشغل عند الاستلام أن النسخة A-114 بغلاف جلد بني بسيط بلا ختم و96 ورقة.", "attribute", ["obj_copy_a", "hasan"], 1, T(85), "loc_studio")
F("f_b_to_hall", "نُقلت النسخة B-114 من المخزن إلى قاعة العرض نحو الساعة 15:20 بمحضر موقّع.", "event", ["obj_copy_b", "saeed"], 1, T(440), "loc_hall")
F("f_hall_seal", "على غلاف النسخة المعروضة ختم زخرفي بارز.", "attribute", ["obj_copy_b", "loc_hall"], 1, None, "loc_hall")
F("f_vault_entry", "دخل أمين السجلات مخزن المخطوطات نحو 15:05 وأخرج مخطوطة واحدة دون تدوين رقمها.", "event", ["saeed", "loc_vault"], 1, T(425), "loc_vault")
F("f_shared_local_no", "الاسم المختصر والرقم المحلي 114 يتكرران عند مجموعتين مختلفتين، وقد نبّهت فنية الفهرسة إلى ذلك قبل الظهر.", "state", ["mona", "org_museum"], 1, T(140, "approx"), "loc_catalog")
F("f_a_desc_card_lost", "لم تُعثر على بطاقة الوصف المادي للنسخة A-114 أثناء نقل الفهرسة.", "event", ["obj_copy_a", "mona"], 2, T(180, "approx"), "loc_catalog")
F("f_crop_prefix", "اللقطة المنشورة قصّت من البطاقة اسم المجموعة وحرف رقم الحفظ وأبقت 114 وحدها.", "relation", ["obj_copy_a", "obj_copy_b"], 2, None, "loc_catalog")
F("f_layla_complaint", "كتبت أمينة المعرض مذكرة تعترض فيها على ظهور الأصل في موقعين.", "event", ["layla"], 1, T(1560, "approx"))
F("f_layla_clip", "نشرت نشرة المتحف صورة مقصوصة لبطاقة مكتوب عليها «الأصل».", "event", ["layla", "org_museum"], 1)
F("f_memo_exists", "كتبت فنية الفهرسة مذكرة داخلية عن التباس الاسم المختصر.", "event", ["mona"], 1, T(140, "approx"), "loc_catalog")
F("f_migration_list", "قائمة مراجعة نقل الفهرسة تدوّن البطاقات الموجودة والمفقودة.", "state", ["mona", "loc_catalog"], 1, T(180, "approx"), "loc_catalog")
F("f_ledger_exists", "يدوّن سجل الجرد موقع كل نسخة برقم حفظها الكامل.", "state", ["saeed", "loc_registry"], 1, None, "loc_registry")
F("f_transfer_exists", "يوثّق محضر موقّع كل نقل إلى قاعة العرض.", "state", ["saeed", "loc_registry"], 1, None, "loc_registry")
F("f_vault_log_exists", "يسجّل دفتر دخول المخزن كل دخول وخروج.", "state", ["saeed", "loc_vault"], 1, None, "loc_vault")
F("f_intake_exists", "يملأ المشغل استمارة استلام بإيصال مرقّم لكل نسخة يستلمها.", "state", ["hasan", "loc_studio"], 1, None, "loc_studio")
# key (spoiler 3)
F("f_desc_reused", "كُتب وصف النسخة المعروضة في خانة الوصف الموحّدة بدل وصف النسخة التي غابت بطاقتها، وبقيت الخانة دون تعليم.", "event", ["mona", "obj_copy_b", "obj_copy_a"], 3, T(285), "loc_catalog", ["KO-RS-05-014"])
F("f_two_copies", "في المتحف مخطوطتان مستقلتان لا واحدة: A-114 خارج المبنى، وB-114 معروضة.", "relation", ["obj_copy_a", "obj_copy_b"], 3, None, None, ["KO-RS-06-017"])
F("f_catalog_confusion", "اجتمع تشابه الاسم المختصر وتطابق الرقم المحلي مع ضياع بطاقة وصف إحداهما، فاختلط وصفاهما في السجل الموحّد.", "relation", ["mona", "org_museum"], 3, T(285), "loc_catalog", ["KO-RS-05-004"])
claims = [
    {"id": "cl_layla_twice", "statement_ar": "الأصل اختفى ثم عاد، أو بُدّل ثم أُعيد.", "kind": "honest_mistake", "held_by": ["layla"], "true_fact_id": "f_two_copies", "contradicted_by_evidence_ids": ["ev_inventory", "ev_transfer_minutes"]},
    {"id": "cl_mona_nochange", "statement_ar": "لم أغيّر شيئاً في الوصف؛ نقلت البطاقات كما وجدتها.", "kind": "half_truth", "held_by": ["mona"], "true_fact_id": "f_desc_reused", "contradicted_by_evidence_ids": ["ev_db_record", "ev_restoration_intake"]},
]
timeline = [
    {"id": "te_a_out", "description_ar": "خروج النسخة A-114 إلى مشغل الترميم الخارجي.", "time": T(70), "location_id": "loc_studio", "actor_ids": ["hasan"], "fact_ids": ["f_a_out", "f_a_plain"], "motivated_by_ar": "ترميم متعاقد عليه من قبل"},
    {"id": "te_memo", "description_ar": "مذكرة الفهرسة عن تكرار الاسم المختصر والرقم 114.", "time": T(140, "approx"), "location_id": "loc_catalog", "actor_ids": ["mona"], "fact_ids": ["f_shared_local_no", "f_memo_exists"], "motivated_by_ar": "لاحظت التكرار أثناء الإدخال"},
    {"id": "te_card_lost", "description_ar": "تعذّر العثور على بطاقة وصف A-114 أثناء نقل الفهرسة.", "time": T(180, "approx"), "location_id": "loc_catalog", "actor_ids": [], "fact_ids": ["f_a_desc_card_lost", "f_migration_list"]},
    {"id": "te_record", "description_ar": "إنشاء السجل الموحّد وإدخال الوصف.", "time": T(285), "location_id": "loc_catalog", "actor_ids": ["mona"], "fact_ids": ["f_desc_reused", "f_catalog_confusion"], "motivated_by_ar": "أرادت إنهاء الإدخال قبل الإغلاق"},
    {"id": "te_vault", "description_ar": "دخول أمين السجلات إلى المخزن لإخراج النسخة المقرّر عرضها.", "time": T(425), "location_id": "loc_vault", "actor_ids": ["saeed"], "fact_ids": ["f_vault_entry"], "motivated_by_ar": "تجهيز القاعة لافتتاح المعرض"},
    {"id": "te_hall", "description_ar": "نقل B-114 إلى قاعة العرض بمحضر موقّع.", "time": T(440), "location_id": "loc_hall", "actor_ids": ["saeed"], "fact_ids": ["f_b_to_hall", "f_hall_seal"], "motivated_by_ar": "تركيب النسخة قبل الافتتاح"},
    {"id": "te_complaint", "description_ar": "أمينة المعرض تكتب مذكرتها عن الأصل في موقعين.", "time": T(1560, "approx"), "location_id": "loc_hall", "actor_ids": ["layla"], "fact_ids": ["f_layla_complaint"], "motivated_by_ar": "اطّلعت على السجل الموحّد صباح اليوم التالي"},
]

ev = []
def V(id, title, kind, content, acts, supports, rel, limits, contradicts=None, red=False, ko=None, loc=None):
    d = {"id": id, "title_ar": title, "kind": kind, "content_ar": content, "acquired_by_action_ids": acts, "supports_fact_ids": supports, "reliability": rel, "limits_ar": limits}
    if contradicts: d["contradicts_claim_ids"] = contradicts
    if red: d["is_red_herring"] = True
    if ko: d["forensic_ko_ref"] = ko
    if loc: d["location_id"] = loc
    ev.append(d)
V("ev_card_a", "بطاقة مجموعة الوقف القديم", "documentary",
  "متحف الوراقين — بطاقة مجموعة (ورقية)\nالمجموعة: الوقف القديم\nرقم الحفظ: A-114\nالاسم المختصر: رحلة الوراق\nالصفة: أصل بخط المؤلف\nسجل الرحلة: يبدأ بعبارة «خرجنا مع الفجر من باب المدينة…»\nملاحظة: بطاقة الوصف المادي منفصلة عن هذه البطاقة.",
  ["a_read_card_a"], ["f_card_a_id"], "strong", "تثبت رقم الحفظ ومجموعته كما كُتبا على البطاقة؛ لا تثبت مكان النسخة الآن ولا وصفها المادي.", loc="loc_catalog")
V("ev_card_b", "بطاقة مجموعة المدرسة العتيقة", "documentary",
  "متحف الوراقين — بطاقة مجموعة (ورقية)\nالمجموعة: المدرسة العتيقة\nرقم الحفظ: B-114\nالاسم المختصر: رحلة الوراق\nالصفة: أصل بخط المؤلف\nسجل الرحلة: يبدأ بعبارة «خرجنا مع الفجر من باب المدينة…»\nملاحظة: بطاقة الوصف المادي منفصلة عن هذه البطاقة.",
  ["a_read_card_b"], ["f_card_b_id"], "strong", "تثبت رقم الحفظ ومجموعته كما كُتبا على البطاقة؛ لا تثبت مكان النسخة الآن ولا وصفها المادي.", loc="loc_catalog")
V("ev_db_record", "السجل الموحّد في نظام الفهرسة الجديد", "digital",
  "نظام الفهرسة الجديد — سجل موحّد\nالعنوان المختصر: رحلة الوراق\nالمعرّف المحلي: 114\nالوصف المادي: جلد مزخرف بختم بارز على الغلاف، 88 ورقة\nالموقع الحالي: قاعة العرض (حُدّث 15:25)\nسجل المواقع: ترميم خارجي (09:10) ثم قاعة العرض (15:20)\nأُنشئ السجل: 12:45 — فنية الفهرسة",
  ["a_open_record"], ["f_catalog_shows_both"], "moderate", "عرض تجميعي في النظام الجديد، لا مصدر أصلي؛ يضمّ ما نُقل إليه من أكثر من سجل ولا يذكر حرف المجموعة.", contradicts=["cl_mona_nochange"], loc="loc_catalog")
V("ev_gallery_photo", "صورة الصندوق الزجاجي في القاعة", "observation",
  "صورة التُقطت بعد التركيب: المخطوطة المعروضة في الصندوق الزجاجي، وعلى غلافها ختم زخرفي بارز. بطاقة العرض بجانبها تحمل كلمة «الأصل».",
  ["a_view_hall"], ["f_hall_seal", "f_hall_label"], "strong", "تُظهر شكل النسخة المعروضة فقط؛ لا تقول أي رقم حفظ هي ولا ما في المشغل الخارجي.", loc="loc_hall")
V("ev_crop", "قصاصة بطاقة من نشرة المتحف", "documentary",
  "قصاصة من نشرة المتحف (ركن «من كنوزنا»):\n[…]114 | رحلة الوراق | أصل بخط المؤلف\nسجل الرحلة: «خرجنا مع الفجر من باب المدينة…»\n(الجزء العلوي الأيمن من البطاقة مقصوص)",
  ["a_get_clip"], ["f_crop_prefix", "f_layla_clip"], "weak", "لقطة منشورة بعد القص: لا تُظهر المجموعة ولا الحرف السابق للرقم، فلا تكفي لتحديد أي النسختين تقصد.", red=True, loc="loc_catalog")
V("ev_transfer_minutes", "محضر نقل إلى قاعة العرض", "documentary",
  "محضر نقل مخطوطات إلى قاعة العرض — الاثنين 15:20\nالمنقول: رحلة الوراق — رقم الحفظ B-114\nمن: مخزن المخطوطات   إلى: قاعة العرض\nالمسلِّم: س. الخطيب   المستلم: فني العرض\nالتوقيعان: موجودان",
  ["a_get_transfer"], ["f_b_to_hall"], "strong", "يثبت أن B-114 بالذات نُقلت إلى القاعة في ذلك الوقت؛ لا يخبر عن مكان A-114 ولا عن سبب الالتباس في الفهرسة.", contradicts=["cl_layla_twice"], loc="loc_registry")
V("ev_inventory", "سجل جرد المخطوطات (صفحة الاثنين)", "documentary",
  "سجل جرد مخطوطات المتحف — الاثنين\nA-114 | رحلة الوراق | خروج 09:10 إلى مشغل الترميم الخارجي | إيصال R-2207 | موقّع من المشغل\nB-114 | رحلة الوراق | في المخزن حتى 15:20 ثم قاعة العرض",
  ["a_get_ledger"], ["f_a_out"], "strong", "يثبت خروج A-114 بإيصال؛ لا يثبت حالتها المادية ولا يشرح الالتباس في سجل الفهرسة.", contradicts=["cl_layla_twice"], loc="loc_registry")
V("ev_restoration_intake", "استمارة استلام المشغل الخارجي", "documentary",
  "استمارة استلام — مشغل الترميم الخارجي\nالاثنين 09:25 | الإيصال R-2207\nالمستلَم: «رحلة الوراق» — رقم الحفظ A-114 (الوقف القديم)\nالوصف عند الاستلام: غلاف جلد بني بسيط بلا ختم، 96 ورقة\nالمستلِم: ح. المرمّم",
  ["a_get_intake"], ["f_a_plain", "f_a_out"], "strong", "مصدر مستقل عن المتحف يصف النسخة التي استلمها بوصفها وقت التسليم؛ لا يخبر عمّا كُتب في سجل الفهرسة.", contradicts=["cl_mona_nochange"], loc="loc_studio")
V("ev_vault_log", "دفتر دخول مخزن المخطوطات", "documentary",
  "دفتر دخول مخزن المخطوطات — الاثنين\n15:05 | دخول: س. الخطيب | بلا مرافق | إخراج: مخطوطة واحدة (خانة الرقم فارغة)\n15:12 | خروج: س. الخطيب",
  ["a_get_vault"], ["f_vault_entry"], "moderate", "يثبت دخولاً وإخراج مخطوطة واحدة؛ لا رقمها ولا وجهتها، وخانة فارغة تدل على إهمال في التعبئة لا على فعل بعينه.", red=True, loc="loc_vault")
V("ev_index_memo", "مذكرة فهرسة داخلية", "documentary",
  "مذكرة فهرسة داخلية — الاثنين 10:20\nمن: فنية الفهرسة   إلى: رئيس القسم\nالموضوع: الاسم المختصر «رحلة الوراق» يرد في مجموعتين، والنظام الجديد يعطي الرقم المحلي 114 لكليهما. هذا يسبب التباساً، والأصح اعتماد رقم الحفظ كاملاً بحرفه. لم يُنفَّذ بعد.",
  ["a_get_memo"], ["f_shared_local_no", "f_memo_exists"], "strong", "تُظهر أن الالتباس كان معروفاً قبل الظهر؛ لا تقول إنه وقع فعلاً ولا كيف.", loc="loc_catalog")
V("ev_migration_log", "قائمة مراجعة نقل الفهرسة", "documentary",
  "قائمة مراجعة نقل الفهرسة — الاثنين\nالبند 37: بطاقة الوصف المادي لـ A-114 — لم تُعثر عليها في الدرج (11:00)\nالبند 38: بطاقة الوصف المادي لـ B-114 — موجودة\nالبند 39: السجل الموحّد «رحلة الوراق / 114» — قيد الإنشاء",
  ["a_get_migration"], ["f_a_desc_card_lost", "f_migration_list"], "strong", "تثبت غياب بطاقة الوصف في ذلك الوقت؛ لا تثبت ما أُدخل في السجل الموحّد بدلاً منها.", loc="loc_catalog")
V("ev_layla_note", "مذكرة أمينة المعرض", "testimonial",
  "مذكرة أمينة المعرض:\n«سجل الفهرسة يضع الأصل في الترميم منذ الصباح وفي القاعة منذ العصر. فإما أنه اختفى مرتين، أو أن أحداً بدّله ثم أعاده. أطلب معرفة من فعل ذلك.»",
  ["a_note_layla"], ["f_layla_complaint", "f_layla_suspects"], "weak", "رأي شخص اطّلع على السجل الموحّد وحده؛ يصف ما بدا له، ولا يستند إلى الأوراق الأصلية.", loc="loc_hall")
V("ev_mona_statement", "إفادة فنية الفهرسة (ملخص)", "testimonial",
  "ملخص إفادة فنية الفهرسة، دوّنه أمين اللجنة:\n«قلت في البداية إنني لم أغيّر وصفاً. الصحيح أنني لم أجد بطاقة وصف A-114، فنسخت وصف B-114 إلى السجل الموحّد لأكمل الإدخال قبل الإغلاق، ونويت تصحيحه ولم أعلّمه.»",
  ["a_note_mona"], ["f_desc_reused"], "moderate", "إقرار شخصي بعد مواجهة بالأوراق؛ يؤيده السجل والاستمارة ولا يحلّ محلهما، ولا يبيّن نيّتها كاملة.", loc="loc_catalog")

def P(t, i): return {"ref_type": t, "ref_id": i}
inf = []
def I(id, prem, ct, concl, rel, strength, rule, ks):
    inf.append({"id": id, "premises": prem, "conclusion": {"ref_type": ct, "ref_id": concl}, "relation": rel, "strength": strength, "rule_ar": rule, "skill_ko_refs": ks})
GK = P("general_knowledge", "unique_id_vs_name")
I("i_two_ids", [P("evidence", "ev_card_a"), P("evidence", "ev_card_b"), GK], "fact", "f_two_copies", "establishes", "strong",
  "البطاقتان الأصليتان تحملان رقمي حفظ مختلفين (A-114 وB-114) لمجموعتين مختلفتين؛ والاسم المختصر المشترك لا يجعل الرقمين الفريدين رقماً واحداً.", ["KO-RS-06-017"])
I("i_two_places", [P("evidence", "ev_inventory"), P("evidence", "ev_transfer_minutes")], "fact", "f_two_copies", "establishes", "conclusive",
  "في اليوم نفسه خرجت A-114 بإيصال إلى المشغل وانتقلت B-114 من المخزن إلى القاعة؛ ما يكون في مكانين معاً نسختان لا نسخة واحدة.", ["KO-RS-06-017", "KO-RS-06-008"])
I("i_confusion_a", [P("evidence", "ev_index_memo"), P("evidence", "ev_migration_log")], "fact", "f_catalog_confusion", "establishes", "strong",
  "الرقم المحلي 114 مشترك بين مجموعتين، وبطاقة وصف A-114 لم تُوجد، وبطاقة B-114 وحدها كانت متاحة وقت إنشاء السجل الموحّد؛ فشروط الخلط قائمة.", ["KO-RS-05-004"])
I("i_confusion_b", [P("evidence", "ev_db_record"), P("evidence", "ev_restoration_intake"), P("evidence", "ev_gallery_photo")], "fact", "f_catalog_confusion", "establishes", "strong",
  "السجل الموحّد يصف غلافاً بختم و88 ورقة، وهذا ما تُظهره صورة القاعة، بينما وصف المشغل A-114 بلا ختم و96 ورقة؛ فوصف السجل ينتمي إلى النسخة المعروضة لا إلى نسخة الترميم.", ["KO-RS-05-014"])
I("i_crop_prefix", [P("evidence", "ev_crop"), P("evidence", "ev_card_a")], "fact", "f_crop_prefix", "establishes", "strong",
  "القصاصة تُبقي 114 وتحذف المجموعة والحرف، أما البطاقة الأصلية فتُظهرهما؛ والحكم يُبنى على الأصل لا على اللقطة.", ["KO-RS-06-004"])
I("i_layla_claim", [P("evidence", "ev_inventory"), P("evidence", "ev_transfer_minutes")], "claim", "cl_layla_twice", "contradicts_claim", "strong",
  "ما ظنّته اختفاءً مرتين هو انتقال نسختين مختلفتين في مكانين مختلفين؛ لا شيء اختفى ولا شيء عاد.", ["KO-RS-05-001"])
I("i_mona_claim", [P("evidence", "ev_db_record"), P("evidence", "ev_restoration_intake")], "claim", "cl_mona_nochange", "contradicts_claim", "strong",
  "وصف السجل الموحّد لا يطابق وصف A-114 عند المشغل؛ فالقول إن البطاقات نُقلت كما هي لا يتفق مع ما في السجل.", ["KO-RS-05-001"])
I("i_rule_tamper_docs", [P("evidence", "ev_card_a"), P("evidence", "ev_card_b"), P("evidence", "ev_index_memo")], "hypothesis", "h_tamper", "rules_out", "strong",
  "بطاقتان لمجموعتين مستقلتين برقمين فريدين، ومذكرة تنبّه إلى تكرار الاسم قبل أي تغيير؛ فكل ما بدا تناقضاً له تفسير إداري ولا يبقى شيء يحتاج إلى تبديل أو تزوير.", ["KO-RS-06-008"])
I("i_rule_tamper_moves", [P("evidence", "ev_inventory"), P("evidence", "ev_transfer_minutes")], "hypothesis", "h_tamper", "rules_out", "strong",
  "A-114 كانت خارج المبنى بإيصال، وB-114 انتقلت إلى القاعة بمحضر موقّع؛ فكل مخطوطة في مكانها الموثّق ولا حاجة إلى افتراض تبديل.", ["KO-RS-06-008"])
I("i_vault_explained", [P("evidence", "ev_vault_log"), P("evidence", "ev_transfer_minutes"), P("evidence", "ev_inventory")], "hypothesis", "h_tamper", "rules_out", "strong",
  "A-114 كانت خارج المبنى قبل دخول المخزن بنحو ست ساعات، والمخطوطة الوحيدة التي أُخرجت هي B-114 بمحضر موقّع؛ فخانة الرقم الفارغة إهمال في التعبئة لا إخراج غير موثّق.", ["KO-RS-06-008"])
I("i_rule_insufficient_docs", [P("evidence", "ev_card_a"), P("evidence", "ev_card_b")], "hypothesis", "h_insufficient", "rules_out", "strong",
  "البطاقتان الأصليتان بحرفيهما ورقميهما كافيتان لتمييز نسختين؛ ولا حاجة لانتظار أصل آخر للسجل.", ["KO-RS-06-001"])
I("i_rule_insufficient_moves", [P("evidence", "ev_inventory"), P("evidence", "ev_transfer_minutes")], "hypothesis", "h_insufficient", "rules_out", "strong",
  "جرد يضع A-114 خارج المبنى ومحضر يضع B-114 في القاعة يكفيان للفصل في الهوية دون أصل آخر.", ["KO-RS-06-001"])
I("i_support_identity", [P("fact", "f_two_copies"), P("fact", "f_catalog_confusion")], "hypothesis", "h_identity", "supports", "strong",
  "نسختان مستقلتان وخلط وصف بسبب اسم مشترك وبطاقة مفقودة يفسّران كل ما بدا تناقضاً من غير افتراض فعل متعمد.", ["KO-RS-05-002"])

ck = []
def K(fid, access, cert="certain", src=None):
    d = {"fact_id": fid, "access": access, "certainty": cert}
    if src: d["source_character_id"] = src
    return d
ck = [
    {"character_id": "layla", "knows": [K("f_layla_complaint", "witnessed"), K("f_layla_clip", "witnessed")], "hides": [], "believes": [{"claim_id": "cl_layla_twice", "stance": "sincere"}]},
    {"character_id": "mona", "knows": [K("f_memo_exists", "witnessed"), K("f_migration_list", "witnessed")],
     "hides": [{"fact_id": "f_desc_reused", "reveal_when": {"all": [{"presented": {"evidence_id": "ev_db_record", "to_character": "mona"}}, {"presented": {"evidence_id": "ev_restoration_intake", "to_character": "mona"}}]}, "cover_claim_id": "cl_mona_nochange", "reveal_line_id": "mn_break"}],
     "believes": [{"claim_id": "cl_mona_nochange", "stance": "deliberate_lie"}]},
    {"character_id": "saeed", "knows": [K("f_ledger_exists", "professional"), K("f_transfer_exists", "professional"), K("f_vault_log_exists", "professional")], "hides": [], "believes": []},
    {"character_id": "hasan", "knows": [K("f_intake_exists", "professional")], "hides": [], "believes": []},
]
hyps = [
    {"id": "h_tamper", "statement_ar": "حدث عبث متعمد: بُدّلت المخطوطة الأصلية أو سُرّب وصفها أو زُوّرت إحدى بطاقاتها.", "is_true": False, "plausibility_at_start": "high", "suspect_id": "saeed"},
    {"id": "h_identity", "statement_ar": "التبس الأمر في الفهرسة: نسختان أصليتان مستقلتان تحملان الاسم المختصر نفسه، واختلط وصفاهما حين فُقدت بطاقة إحداهما.", "is_true": True, "plausibility_at_start": "low", "suspect_id": "mona"},
    {"id": "h_insufficient", "statement_ar": "لا تكفي الأدلة للفصل بين العبث والالتباس قبل العثور على أصل آخر للسجل.", "is_true": False, "plausibility_at_start": "medium"},
]
mis = [
    {"id": "rh_vault", "points_to_hypothesis_id": "h_tamper", "planted_via_ar": "دفتر المخزن يُظهر دخولاً منفرداً بلا مرافق وإخراج مخطوطة بلا رقم قبل ظهور الأصل في القاعة.", "evidence_ids": ["ev_vault_log"], "refuted_by_inference_ids": ["i_vault_explained", "i_rule_tamper_moves"],
     "fairness_note_ar": "الجرد ومحضر النقل متاحان لمن يسأل أمين السجلات؛ وهما يضعان A-114 خارج المبنى ويوثّقان نقل B-114 بتوقيعين."},
    {"id": "rh_crop", "points_to_hypothesis_id": "h_insufficient", "planted_via_ar": "القصاصة المنشورة تُظهر 114 وحدها، فتبدو الوثيقتان وصفاً لشيء واحد لا يمكن الفصل فيه.", "evidence_ids": ["ev_crop"], "refuted_by_inference_ids": ["i_crop_prefix", "i_rule_insufficient_docs"],
     "fairness_note_ar": "البطاقتان الأصليتان متاحتان من أول الملف وتحملان الحرف والمجموعة؛ والقصاصة نفسها تنبّه بقولها إن جزءاً منها مقصوص."},
]
los = [
    {"id": "lo_claim", "statement_ar": "يفرّق بين اسم الشيء ومعرّفه الفريد، ويصنّف المصادر قبل الاعتماد عليها.", "skill_ko_ref": "KO-RS-05-001", "observable_behaviors_ar": ["يصنّف البطاقات والإفادات واللقطات", "يقارن الأرقام الفريدة قبل وصف أحد بالخطأ"], "evidence_sources": ["evidence_board"]},
    {"id": "lo_timeline", "statement_ar": "يضع الأحداث على خط زمني ليفسّر التعارض الظاهر.", "skill_ko_ref": "KO-RS-05-005", "observable_behaviors_ar": ["يضع الأدلة في أزمنتها"], "evidence_sources": ["timeline_task", "action_log"]},
    {"id": "lo_hyp", "statement_ar": "يوازن بين فرضيتين على الأقل ويستبعد ما تنقضه الأدلة.", "skill_ko_ref": "KO-RS-05-002", "observable_behaviors_ar": ["يضيف فرضيات", "يستبعد بدليل"], "evidence_sources": ["hypothesis_ledger"]},
    {"id": "lo_diag", "statement_ar": "يقدّر ما يثبته الدليل وما لا يثبته، ويرجع إلى الأصل لا اللقطة المقصوصة.", "skill_ko_ref": "KO-RS-06-001", "observable_behaviors_ar": ["يربط الدليل بالفرضية باتجاه صحيح"], "evidence_sources": ["evidence_board", "final_justification"]},
    {"id": "lo_calib", "statement_ar": "يصوغ ثقته بحدودها.", "skill_ko_ref": "KO-RS-06-021", "observable_behaviors_ar": ["يختار ثقة معقولة", "يذكر حدوداً"], "evidence_sources": ["final_justification"]},
    {"id": "lo_revise", "statement_ar": "يراجع رأيه الأول حين يظهر دليل جديد.", "skill_ko_ref": "KO-RS-06-009", "observable_behaviors_ar": ["يغيّر فرضيته الرائدة بدليل"], "evidence_sources": ["hypothesis_ledger"]},
]
def levels(d): return [{"score": i, "descriptor_ar": t} for i, t in enumerate(d)]
rub = {
    "reference_answer_ar": "لم تختفِ مخطوطة مرتين، ولم يُبدَّل شيء. هناك نسختان أصليتان مستقلتان: A-114 من مجموعة الوقف القديم خرجت إلى الترميم الخارجي بإيصال، وB-114 من المدرسة العتيقة نُقلت إلى القاعة بمحضر موقّع. اشتركت النسختان في الاسم المختصر وفي الرقم المحلي 114، وغابت بطاقة وصف A-114 يوم نقل الفهرسة، فجاء الوصف في السجل الموحّد مطابقاً للنسخة المعروضة. حدود الاستنتاج: لا نعرف كل ما جرى في ذلك اليوم من نية، ولم تُفحص النسختان جنباً إلى جنب.",
    "criteria": [
        {"id": "c_source", "name_ar": "استدعاء مصادر مناسبة وتصنيفها", "objective_ids": ["lo_claim"], "scored_by": "deterministic", "weight": 0.25, "levels": levels(["لم يصنّف", "أخطأ في الأغلب", "نصف صحيح", "معظمه صحيح", "كله صحيح"])},
        {"id": "c_conflict", "name_ar": "تفسير التعارض على الخط الزمني", "objective_ids": ["lo_timeline"], "scored_by": "deterministic", "weight": 0.25, "levels": levels(["لم يضع شيئاً", "وضع قليلاً", "وضع نصفها صحيحاً", "معظمها", "كلها في موضعها"])},
        {"id": "c_links", "name_ar": "ربط الأدلة بالفرضيات", "objective_ids": ["lo_diag"], "scored_by": "deterministic", "weight": 0.12, "levels": levels(["لا روابط", "قليلة", "نصفها صحيح", "معظمها", "كلها دقيقة"])},
        {"id": "c_elimination", "name_ar": "استبعاد الفرضيات الخاطئة", "objective_ids": ["lo_hyp"], "scored_by": "deterministic", "weight": 0.08, "levels": levels(["لم يستبعد", "استبعد خطأً", "فرضية بدليل", "فرضيتين", "كل الخاطئة"])},
        {"id": "c_uncertainty", "name_ar": "التعامل مع عدم اليقين", "objective_ids": ["lo_calib"], "scored_by": "deterministic", "weight": 0.15, "levels": levels(["ثقة مفرطة", "حدود قليلة", "جزئية", "معقولة", "معايَرة كاملة"])},
        {"id": "c_revision", "name_ar": "تصحيح الرأي عند الدليل الجديد", "objective_ids": ["lo_revise"], "scored_by": "deterministic", "weight": 0.15, "levels": levels(["بقي على فرضية مرفوضة", "لم يعلن فرضية", "ثبت على فرضية سليمة", "غيّر بدليل", "غيّر بدليل ووثّق"])},
        {"id": "c_justification", "name_ar": "جودة الحجة المكتوبة (مراجعة بشرية)", "objective_ids": ["lo_diag", "lo_hyp"], "scored_by": "human", "weight": 0.0, "levels": levels(["لا حجة", "ادعاء بلا سند", "أدلة دون ربط", "ربط الأدلة بالاستنتاج", "ربط مع البدائل والحدود"])},
    ],
}
def H(id, lv, kind, text, trig, target=None, w=0.0):
    d = {"id": id, "level": lv, "kind": kind, "text_ar": text, "trigger": trig, "assessment_weight": w}
    if target: d["targets_inference_id"] = target
    return d
he = lambda e: {"has_evidence": e}
hints = [
    H("hg1", 1, "metacognitive", "حين تتشابه وثيقتان في الاسم، اسأل: ما الذي يميّز كل واحدة عن الأخرى تمييزاً لا يتكرر؟", {"always": True}, None, 0.02),
    H("hg2", 2, "focus_area", "اقرأ البطاقتين الأصليتين سطراً سطراً، وقارن الخانات التي تختلف بينهما.", he("ev_card_b"), None, 0.04),
    H("hk1", 1, "metacognitive", "قبل أن تقول إن شخصاً أخطأ، هل قارنت الأرقام الفريدة في الأوراق؟", he("ev_db_record"), "i_two_ids", 0.02),
    H("hk2", 2, "pointer", "انظر إلى الحرف الذي يسبق 114 في كل بطاقة، ثم إلى سجل الجرد يوم النقل.", he("ev_db_record"), "i_two_ids", 0.06),
    H("hk3", 3, "partial_reveal", "إن كان رقم الحفظ في البطاقتين مختلفاً وكل رقم له موقع موثّق، فهل الحديث عن شيء واحد أم عن شيئين؟", he("ev_db_record"), "i_two_ids", 0.1),
    H("hc1", 1, "metacognitive", "هل الوصف المكتوب في السجل الموحّد يطابق ما كتبه المشغل عن النسخة التي استلمها؟", he("ev_restoration_intake"), "i_confusion_b", 0.02),
    H("hc2", 2, "pointer", "قارن الوصف المادي في السجل الموحّد باستمارة المشغل وبصورة القاعة: أيّهما يشبه؟", he("ev_restoration_intake"), "i_confusion_b", 0.06),
    H("hc3", 3, "partial_reveal", "اعرض السجل الموحّد واستمارة المشغل على فنية الفهرسة، وسترى كيف يتغير ما تقوله.", he("ev_restoration_intake"), "i_confusion_b", 0.1),
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
Act("a_read_card_a", "examine", "اقرأ بطاقة مجموعة الوقف القديم", al, [G("ev_card_a")], "loc_catalog", "READ_CARD_A")
Act("a_read_card_b", "examine", "اقرأ بطاقة مجموعة المدرسة العتيقة", al, [G("ev_card_b")], "loc_catalog", "READ_CARD_B")
Act("a_open_record", "examine", "افتح السجل الموحّد في نظام الفهرسة الجديد", al, [G("ev_db_record")], "loc_catalog", "OPEN_RECORD")
Act("a_view_hall", "search_location", "عاين الصندوق الزجاجي في قاعة العرض", al, [G("ev_gallery_photo")], "loc_hall", "VIEW_HALL")
Act("a_get_clip", "examine", "اطلب قصاصة النشرة من الأمينة", fu("f_layla_clip"), [G("ev_crop")], "layla", "GET_CLIP")
Act("a_note_layla", "examine", "دوّن مذكرة الأمينة", fu("f_layla_complaint"), [G("ev_layla_note")], "layla", "NOTE_LAYLA")
Act("a_get_ledger", "examine", "اطلب صفحة الجرد من أمين السجلات", fu("f_ledger_exists"), [G("ev_inventory")], "loc_registry", "GET_LEDGER")
Act("a_get_transfer", "examine", "اطلب محضر النقل", fu("f_transfer_exists"), [G("ev_transfer_minutes")], "loc_registry", "GET_TRANSFER")
Act("a_get_vault", "search_location", "اطلب دفتر دخول المخزن", fu("f_vault_log_exists"), [G("ev_vault_log")], "loc_vault", "GET_VAULT")
Act("a_get_memo", "examine", "اطلب مذكرة الفهرسة", fu("f_memo_exists"), [G("ev_index_memo")], "loc_catalog", "GET_MEMO")
Act("a_get_migration", "examine", "اطلب قائمة مراجعة نقل الفهرسة", fu("f_migration_list"), [G("ev_migration_log")], "loc_catalog", "GET_MIGRATION")
Act("a_get_intake", "examine", "اطلب استمارة الاستلام من المشغل", fu("f_intake_exists"), [G("ev_restoration_intake")], "loc_studio", "GET_INTAKE")
Act("a_note_mona", "examine", "دوّن إفادة فنية الفهرسة", fu("f_desc_reused"), [G("ev_mona_statement")], "mona", "NOTE_MONA")
for cid, lab, pre in [("layla", "د. ليلى", al), ("saeed", "سعيد", al), ("mona", "منى", al), ("hasan", "حسن", he("ev_inventory"))]:
    Act(f"a_int_{cid}", "interview", f"ابدأ مقابلة {lab}", pre, [{"op": "raise_trust", "ref_id": cid, "amount": 1}], cid, f"INT_{cid.upper()}")
Act("p_record_mona", "present_evidence", "اعرض السجل الموحّد على منى", {"presented": {"evidence_id": "ev_db_record", "to_character": "mona"}}, [{"op": "emit_event", "ref_id": "PRESENTED_RECORD_MONA"}], "mona", "P_RECORD_MONA", 0)
Act("p_intake_mona", "present_evidence", "اعرض استمارة المشغل على منى", {"presented": {"evidence_id": "ev_restoration_intake", "to_character": "mona"}}, [{"op": "emit_event", "ref_id": "PRESENTED_INTAKE_MONA"}], "mona", "P_INTAKE_MONA", 0)
Act("a_hint", "request_hint", "اطلب تلميحاً", al, [], None, "REQUEST_HINT", 0)
Act("a_accuse", "final_accusation", "قدّم الاستنتاج النهائي", al, [{"op": "emit_event", "ref_id": "SUBMIT"}], None, "FINAL_ACCUSATION", 0)

topics = [
    {"id": "t_complaint", "label_ar": "اعتراض الأمينة", "example_questions_ar": ["ما الذي أزعجك في السجل؟", "من أين جاءت صورة البطاقة؟"], "fact_ids": ["f_layla_complaint", "f_layla_clip"], "claim_ids": ["cl_layla_twice"]},
    {"id": "t_records", "label_ar": "الجرد والنقل والمخزن", "example_questions_ar": ["أين تُدوَّن مواقع النسخ؟", "من يوقّع نقل المخطوطات؟", "هل يُسجَّل دخول المخزن؟"], "fact_ids": ["f_ledger_exists", "f_transfer_exists", "f_vault_log_exists"]},
    {"id": "t_catalog", "label_ar": "الفهرسة ونقل النظام", "example_questions_ar": ["ماذا حدث يوم نقل الفهرسة؟", "هل غيّرتِ شيئاً في الوصف؟"], "fact_ids": ["f_memo_exists", "f_migration_list", "f_desc_reused"], "claim_ids": ["cl_mona_nochange"]},
    {"id": "t_studio", "label_ar": "استلام المشغل", "example_questions_ar": ["ماذا استلمتم من المتحف؟", "كيف تسجّلون ما تستلمونه؟"], "fact_ids": ["f_intake_exists"]},
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
    (1, "البطاقتان الأصليتان تحملان رقمين مختلفين: A-114 لمجموعة الوقف القديم وB-114 للمدرسة العتيقة؛ تطابق الاسم المختصر والرقم المحلي لا يعني تطابق الهوية.", ["ev_card_a", "ev_card_b"], "i_two_ids"),
    (2, "الجرد يضع A-114 خارج المبنى منذ 09:10 بإيصال، ومحضر النقل يضع B-114 في القاعة 15:20؛ فنسختان في مكانين، لا نسخة واحدة تنتقل.", ["ev_inventory", "ev_transfer_minutes"], "i_two_places"),
    (3, "القصاصة المنشورة قصّت الحرف والمجموعة، فبدت البطاقتان بلا فرق؛ والرجوع إلى الأصل يعيد الفرق.", ["ev_crop", "ev_card_a"], "i_crop_prefix"),
    (4, "وصف السجل الموحّد (ختم و88 ورقة) هو وصف النسخة المعروضة كما في الصورة، لا وصف A-114 عند المشغل (بلا ختم و96 ورقة)؛ وقد غابت بطاقة وصف A-114 وقت إنشاء السجل.", ["ev_db_record", "ev_restoration_intake", "ev_gallery_photo", "ev_migration_log"], "i_confusion_b"),
    (5, "دخول المخزن المنفرد أخرج مخطوطة واحدة هي المنقولة بمحضر موقّع؛ لا دليل على تبديل أو تسريب.", ["ev_vault_log", "ev_transfer_minutes", "ev_inventory"], "i_vault_explained"),
    (6, "نسبة الترجيح هنا عالية للتباس في الفهرسة وفي هوية الوثيقة، لا اختفاء ولا تزوير؛ وهي مبنية على سجلات، لا حكم على نية أحد.", ["ev_card_a", "ev_card_b", "ev_inventory", "ev_restoration_intake"], "i_support_identity"),
]
ending = {
    "steps": [{"order": o, "text_ar": t, "uses_evidence_ids": u, "inference_id": i} for o, t, u, i in steps],
    "alternative_paths_ar": ["يمكن الوصول إلى النتيجة من الأوراق وحدها (البطاقتان والمذكرة وقائمة النقل)، أو من الجرد ومحضر النقل واستمارة المشغل وصورة القاعة، دون الاعتماد على إقرار أحد."],
    "what_evidence_could_not_show_ar": ["لا تثبت الأدلة لماذا لم تُعلَّم الخانة المنسوخة ولا ما كانت تنوي الفنية فعله بعد ذلك.", "لم تُفحص النسختان جنباً إلى جنب؛ الاعتماد على أوراق وصور ووصف مشغل مستقل."],
    "science_notes_ar": ["الاسم المختصر ليس معرّفاً: ما يميّز الشيء رقمه الفريد وسلسلة العهدة الموثّقة له.", "اللقطة المقصوصة لا تغني عن أصل الوثيقة؛ والنتيجة المدعومة بالأدلة ليست دائماً اتهاماً لأحد."],
}
core = {
    "schema_version": "0.1.0", "case_id": CID, "case_version": "0.1.0",
    "meta": {"title_ar": "المخطوطة التي اختفت مرتين", "title_en": "The Manuscript That Vanished Twice", "age_band": "16-18", "locale": "ar", "dialogue_register": "msa", "estimated_minutes": 25, "difficulty": 2,
             "content_flags": ["no_violence", "historical"], "authors": ["فريق أثر التحريري (مسودة بمساعدة الذكاء الاصطناعي، لم تُراجَع بشرياً بعد)"],
             "knowledge_object_refs": ["KO-RS-05-001", "KO-RS-05-005", "KO-RS-05-002", "KO-RS-05-004", "KO-RS-06-001", "KO-RS-06-004", "KO-RS-06-008", "KO-RS-06-009", "KO-RS-06-017", "KO-RS-06-021", "KO-RS-05-014"]},
    "premise": {"hook_ar": "وثيقتان تقولان إن «الأصل» في مكانين في اليوم نفسه. هل اختفى مرتين، أم أن أحداً بدّل شيئاً؟",
                "player_role_ar": "أنت مراجع ملفات في متحف الوراقين، وطُلب منك أن تقدّم تفسيراً تبرره الأدلة قبل افتتاح المعرض.",
                "setting_ar": "متحف خيالي للتراث والمخطوطات، يوم إغلاق للصيانة ونقل نظام الفهرسة ثم صباح الافتتاح. توقيت المتحف المحلي هو توقيت كل السجلات.",
                "public_fact_ids": ["f_catalog_shows_both", "f_layla_suspects", "f_hall_label"],
                "assumed_general_knowledge_ar": ["رقم الحفظ يُعطى لقطعة واحدة بعينها", "لقطة الشاشة أو القصاصة قد تحذف أجزاء من الوثيقة الأصلية"]},
    "entities": {"characters": chars, "locations": locations, "objects": objects, "organizations": orgs},
    "truth": {"solution": {"culprit_ids": ["mona"], "summary_ar": "لم تختفِ مخطوطة ولم يُبدَّل شيء. نسختان مستقلتان تشتركان في الاسم المختصر والرقم المحلي: إحداهما في الترميم، والأخرى في القاعة. وقد التبس وصفهما في السجل الموحّد بعد ضياع بطاقة وصف إحداهما.",
                          "key_fact_ids": ["f_two_copies", "f_catalog_confusion"]},
              "facts": facts, "claims": claims},
    "timeline": timeline, "evidence": ev, "evidence_graph": {"inferences": inf},
    "character_knowledge": ck, "hypotheses": hyps, "misdirection_plan": mis, "learning_objectives": los,
    "mechanics": {"time_budget_units": 30, "actions": A},
    "state_machine": {"id": "c002", "initial": "briefing", "type": "compound", "states": {
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
    "clock": {"epoch_hhmm": "08:00", "zone_label_ar": "توقيت المتحف (يوم الإغلاق)"},
    "cover": {"title_ar": "المخطوطة التي اختفت مرتين", "tagline_ar": "وثيقتان تتحدثان عن «الأصل»… ولا تتفقان على مكانه", "kicker_ar": "الملف الثاني · متحف الوراقين", "glyph": "❖", "accent": "rose"},
    "cold_open_ar": ["صباح الافتتاح في متحف الوراقين.", "في السجل الجديد، مخطوطة «رحلة الوراق» في الترميم منذ الصباح، وفي قاعة العرض منذ العصر.", "أمينة المعرض تسأل: هل اختفى الأصل مرتين؟ أم بدّله أحد ثم أعاده؟", "مطلوب منك تفسير تبرره الأوراق، لا اتهام يبنيه الشك."],
    "labs": [],
    "source_classes": [
        {"id": "primary_record", "label_ar": "سجل أصلي", "help_ar": "يُنتجه شخص أو نظام لحظة الحدث دون وسيط، كبطاقة أو محضر أو إيصال."},
        {"id": "redisplay", "label_ar": "نسخة معروضة", "help_ar": "معلومة نُقلت أو أُعيد عرضها من سجلات أخرى، كلقطة أو قصاصة أو عرض تجميعي."},
        {"id": "claim", "label_ar": "قول أو تصريح", "help_ar": "إفادة شخص أو مذكرة رأي؛ تُقاس بالسجلات لا بمكانة صاحبها."},
        {"id": "template", "label_ar": "قالب أو نموذج", "help_ar": "نص جاهز لا يصف الحدث الفعلي بذاته."},
        {"id": "public_document", "label_ar": "وثيقة منشورة", "help_ar": "وثيقة معلنة ومعروف ناشرها."}],
    "limit_menu": [
        {"id": "l_intent", "label_ar": "الأدلة لا تثبت نيّة أحد ولا تفسّر لماذا لم تُعلَّم الخانة المنسوخة"},
        {"id": "l_physical", "label_ar": "لم تُفحص النسختان مادياً جنباً إلى جنب؛ الاستنتاج مبني على أوراق وصور ووصف مشغل"},
        {"id": "l_invalid_name", "label_ar": "تطابق الاسم المختصر يثبت أن النسختين واحدة"},
        {"id": "l_invalid_entry", "label_ar": "دخول المخزن منفرداً وبلا رقم يثبت وقوع عبث"},
        {"id": "l_invalid_all", "label_ar": "لا حاجة لذكر حدود ما دامت الأوراق كلها متفقة معي"}],
    "mind_change_menu": [
        {"id": "m_same_number", "label_ar": "ظهور وثيقة أصلية تثبت أن A-114 وB-114 رقمان لنسخة واحدة"},
        {"id": "m_receipt_forged", "label_ar": "ثبوت أن إيصال المشغل أو استمارته لم تُكتب يوم النقل"},
        {"id": "m_vault_other", "label_ar": "ثبوت أن المخطوطة التي أُخرجت من المخزن لم تكن B-114"},
        {"id": "m_popular", "label_ar": "كثرة من يظنون أن الأصل اختفى مرتين"}],
    "transfer": {
        "id": "tr_forklift", "title_ar": "اختبار نقل المهارة: الرافعة الشوكية",
        "scenario_ar": "في شركة خيالية للمعدات، ثلاث وثائق تتحدث عن «الرافعة الشوكية من الطراز X» وتبدو متضاربة.",
        "documents": [
            {"title_ar": "فاتورة الشراء", "body_ar": "رافعة شوكية، الطراز X، الرقم التسلسلي 5-2207. تاريخ التسليم: 3 مارس."},
            {"title_ar": "سجل الصيانة", "body_ar": "رافعة شوكية، الطراز X، الرقم التسلسلي 5-2270. في الورشة منذ الأسبوع الماضي. (لقطة شاشة، الزاوية العليا مقصوصة)"},
            {"title_ar": "لوحة الأسطول", "body_ar": "الطراز X: تعمل الآن في المستودع الشرقي."},
        ],
        "prompt_ar": "اختر الخطوات التي تصلح لتحديد ما يحدث فعلاً (يمكنك اختيار أكثر من خطوة).",
        "options": [
            {"id": "o1", "text_ar": "مقارنة الرقم التسلسلي الفريد بدل الاعتماد على اسم الطراز"},
            {"id": "o2", "text_ar": "طلب أصل سجل الصيانة بدل لقطة الشاشة المقصوصة"},
            {"id": "o3", "text_ar": "التحقق من أي نظام أنتج كل وثيقة ومتى"},
            {"id": "o4", "text_ar": "البحث عن مصدر مستقل كإيصال الورشة"},
            {"id": "o5", "text_ar": "افتراض أن تشابه اسم الطراز يعني جهازاً واحداً"},
            {"id": "o6", "text_ar": "اتهام مسؤول الصيانة قبل مقارنة الأرقام"},
            {"id": "o7", "text_ar": "اعتماد الوثيقة الأحدث دائماً مهما كان مصدرها"},
            {"id": "o8", "text_ar": "تجاهل فارق الرقمين لأنه خطأ مطبعي حتماً"}],
        "free_text_prompt_ar": "اكتب في ثلاثة أسطر ما تحتاجه من وثائق إضافية قبل أن تقول إن الرافعتين واحدة أو اثنتان."},
    "skills": [{"skill_id": "KO-RS-05-001", "track": "B"}, {"skill_id": "KO-RS-05-005", "track": "B"}, {"skill_id": "KO-RS-05-002", "track": "D"}, {"skill_id": "KO-RS-06-001", "track": "C"}],
    "stage_hooks_ar": {"briefing": "«الأصل» في مكانين… فما الذي تعنيه الكلمة فعلاً؟", "investigating": "كل ورقة تقول شيئاً، لكن هل تقول الشيء نفسه عن الشيء نفسه؟", "review": "قبل أن تغلق الملف: ما الذي لا تستطيع الأوراق إثباته؟", "resolved": "أُغلق الملف. الملف التالي يدور حول ساعة لا تتفق مع غيرها."},
    "character_glyphs": {"layla": "ل", "mona": "م", "saeed": "س", "hasan": "ح"},
}
sc = {
    "case_id": CID,
    "accepted_conclusions": {
        "h_identity": {"grade": 1, "note_ar": "استنتاج متسق مع الأدلة ويتطلب ذكر حدوده."},
        "h_tamper": {"grade": 0, "note_ar": "يبني على الاسم المشترك ويتجاهل أن الجرد ومحضر النقل يفرّقان بين نسختين."},
        "h_insufficient": {"grade": 0, "note_ar": "تحفّظ مفرط: الأدلة المتاحة تكفي للفصل، والتحفظ المقبول هو ما يتعلق بالنيّة لا بالهوية."}},
    "confidence_band": {"h_identity": [65, 90], "h_tamper": [0, 15], "h_insufficient": [0, 25]},
    "source_key": {"ev_card_a": "primary_record", "ev_card_b": "primary_record", "ev_db_record": "redisplay", "ev_gallery_photo": "primary_record", "ev_crop": "redisplay",
                   "ev_transfer_minutes": "primary_record", "ev_inventory": "primary_record", "ev_restoration_intake": "primary_record", "ev_vault_log": "primary_record",
                   "ev_index_memo": "primary_record", "ev_migration_log": "primary_record", "ev_layla_note": "claim", "ev_mona_statement": "claim"},
    "link_key": {
        "h_identity": {"ev_card_a": "supports", "ev_card_b": "supports", "ev_inventory": "supports", "ev_transfer_minutes": "supports", "ev_restoration_intake": "supports", "ev_gallery_photo": "supports",
                       "ev_index_memo": "supports", "ev_migration_log": "supports", "ev_db_record": "supports", "ev_mona_statement": "supports", "ev_vault_log": "neutral", "ev_crop": "neutral", "ev_layla_note": "neutral"},
        "h_tamper": {"ev_card_a": "weakens", "ev_card_b": "weakens", "ev_inventory": "weakens", "ev_transfer_minutes": "weakens", "ev_restoration_intake": "weakens", "ev_migration_log": "weakens",
                     "ev_vault_log": "supports", "ev_db_record": "supports", "ev_layla_note": "neutral", "ev_crop": "neutral"},
        "h_insufficient": {"ev_card_a": "weakens", "ev_card_b": "weakens", "ev_inventory": "weakens", "ev_crop": "supports", "ev_db_record": "neutral", "ev_layla_note": "neutral"},
    },
    "required_limits": ["l_intent", "l_physical"],
    "valid_mind_changers": ["m_same_number", "m_receipt_forged", "m_vault_other"],
    "invalid_limits": ["l_invalid_name", "l_invalid_entry", "l_invalid_all"],
    "decisive_evidence": ["ev_card_a", "ev_card_b", "ev_inventory", "ev_transfer_minutes", "ev_restoration_intake"],
    "lab_requirement": None,
    "timeline_requirement": [{"evidence_id": "ev_inventory", "utc_minute": 70, "tol": 10}, {"evidence_id": "ev_db_record", "utc_minute": 285, "tol": 10},
                             {"evidence_id": "ev_vault_log", "utc_minute": 425, "tol": 10}, {"evidence_id": "ev_transfer_minutes", "utc_minute": 440, "tol": 10}],
    "refuted_hypotheses": ["h_tamper", "h_insufficient"],
    "criteria_map": {"c_source": "source_typing", "c_conflict": "conflict_resolution", "c_links": "hypothesis_links", "c_elimination": "elimination", "c_uncertainty": "uncertainty", "c_revision": "revision", "c_justification": "justification_human"},
    "transfer_key": {"valid": ["o1", "o2", "o3", "o4"], "invalid": ["o5", "o6", "o7", "o8"]},
    "caps": {"no_citations_max": 45, "no_conflict_resolution_max": 70},
}
os.makedirs(OUT, exist_ok=True)
for suf, obj in [("", core), (".ui", ui), (".scoring", sc)]:
    with open(os.path.join(OUT, f"{CID}{suf}.json"), "w", encoding="utf8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
print("ok")
