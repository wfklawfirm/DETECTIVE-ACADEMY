#!/usr/bin/env python3
# Case c022 «المحتسب الصغير: ميزان السوق» — heritage seed S-07 (ARC-28 «المحتسب الصغير» + the ARC-36 two-minute format spirit), age band 13-15.
# Teaches: before accusing the newest vendor, choose the tests that tell explanations APART (empty pan, sealed reference weights, repeated
# readings), notice WHAT KIND of error you see (a constant shift vs a proportional one), and let two independent chains of records
# (office tests vs. bags + stock sheet + loan notebook + opening table) carry the verdict. No-culprit convention: the vendor who put an
# unadjusted borrowed tray on his pan (Hamed) is recorded in culprit_ids; nobody cheated.
# DEVIATIONS from the seed (honest list): the seed is a five-complaint week (scale, "natural salt", candle, weight stone, undated honey) with a
# daily budget of three simulated tests. The engine has one verdict per case, so this case builds the FIRST complaint (the scale that
# shortchanges) in full, in the seed's "vendor innocent" variant; the honey complaint (naturally crystallised honey) is used as the skill-transfer
# task, and the salt/candle/weight-stone complaints are NOT built here. The "three tests per day" budget is expressed as the office's test
# records (each is a separate evidence item and a separate visit), not as an enforced budget. No adulteration recipes, tasting or fire.
# "المحتسب" here is a consumer-protection inspector, not a morals officer (KO-CD-02H-004). Origin card: attributed heritage report
# (hisba books), rebuilt as an original ATHAR story. All names, places and records are fictional.
# Calendar (fictional): minute 0 = Sunday 08:00 (market time). Sat 17:00 = -900; Mon 10:20 = 1580; Tue 17:00 = 3420; Tue 19:00 = 3540; Wed 09:00 = 4380; Wed 10:30 = 4470.
# Usage: gen_c022.py OUT_DIR
import sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
from _lib_c022_c025 import *

OUT = sys.argv[1]
CID = "c022_market_scale"
c = Case(CID)

# ---------------------------------------------------------------- characters
c.ch("layla", "ليلى الحداد", "victim", "زبونة من حي «الأطلال»، تشتري التمر للأسرة",
     "مهذبة وحازمة، تعدّ نفسها دقيقة في المطبخ، وتتألم من الشعور بأنها خُدعت. تتراجع عن الاتهام إذا رأت قياساً واضحاً.",
     ["أن تأخذ حقها", "ألا تظلم بائعاً بلا دليل"],
     [L("ly_greet", "greeting", "اشتريت ثلاث عبوات، وكلها ناقصة. أريد أن أفهم السبب."),
      L("ly_bags", "reveal", "ما زلت أحتفظ بالعبوات الثلاث مغلقة، وزبونان آخران حفظا عبواتهما أيضاً، وميزان مطبخي مستعد للفحص.", ["f_bags_kept"]),
      L("ly_unknown", "deflect_unknown", "لا أعرف أكثر من هذا."),
      L("ly_off", "deflect_offtopic", "اسألني عمّا اشتريته وكيف وزنته."),
      L("ly_bye", "farewell", "أريد عدلاً لا انتقاماً.")])
c.ch("hamed", "حامد الرشيدي", "suspect", "بائع تمور، هذا أسبوعه الأول في السوق",
     "خجول ومرتبك قليلاً لأنه جديد، يجيب بإيجاز وبنبرة اعتذار. ارتباكه ليس دليلاً على شيء، وهو يقول ما يتذكره.",
     ["أن يحافظ على سمعته الجديدة", "أن يعرف ما الخطأ"],
     [L("hm_greet", "greeting", "أنا لا أغشّ أحداً. اسأل عمّا شئت."),
      L("hm_pan", "reveal", "تشققت كفة ميزاني صباح الاثنين، فاستعرت صينية من جارتي ووضعتها فوقها. الميزان نفسه سليم في ظني، ولم ألمس فيه غير ذلك.", ["f_tray_swap"], ["cl_hamed_fine"]),
      L("hm_stock", "reveal", "أدوّن كل يوم في ورقة مخزني: كم كان عندي من التمر، وكم بعت من كل حجم، وكم بقي بعد العدّ.", ["f_stock_sheet_exists"]),
      L("hm_unknown", "deflect_unknown", "لا أعرف."),
      L("hm_off", "deflect_offtopic", "اسألني عن الميزان والتمر."),
      L("hm_bye", "farewell", "افحصوا كل شيء، لا أخشى الفحص.")])
c.ch("umm_samir", "أم سمير الخياط", "witness", "بائعة قديمة في السوق، جارة حامد",
     "ودودة وعملية، تحب أن تساعد الجدد وتدوّن كل ما تعيره. تقول ما رأته ولا تخمّن النيات.",
     ["أن تساعد جارها", "ألا تُنسب إليها مسؤولية لم تقصدها"],
     [L("us_greet", "greeting", "جاري حامد شاب طيب. اسأل."),
      L("us_lent", "reveal", "أعرت حامداً صينية فولاذية صباح الاثنين نحو العاشرة وعشرين دقيقة لأن كفته تشققت.", ["f_tray_lent"]),
      L("us_book", "reveal", "كل ما يُعار بين الأركان يُكتب في دفتر الإعارة عند مكتب السوق، وقد كتبت هذه الإعارة بيدي.", ["f_loan_book_exists"]),
      L("us_unknown", "deflect_unknown", "لا أعرف غير ذلك."),
      L("us_off", "deflect_offtopic", "اسألني عن الإعارة."),
      L("us_bye", "farewell", "أرجو ألا يتضرر جاري.")])
c.ch("nabil", "نبيل الصعيدي", "witness", "بائع قديم في السوق منذ سنوات",
     "واثق ومتكلم، يعمّم من خبرته ويبني حكمه على الانطباع. يتراجع إذا طُلب منه أن يفرّق بين ما رآه وما ظنه.",
     ["ألا تتغير عادات السوق", "أن يكون على صواب"],
     [L("nb_greet", "greeting", "أعرف هذا السوق أكثر من مكتبه."),
      L("nb_new", "reveal", "البائع الجديد يغشّ في أسبوعه الأول، هذا ما تعلمته. ورأيت حامداً صباح الاثنين يغيّر شيئاً في ميزانه.", ["f_nabil_saw_change"], ["cl_nabil_new"]),
      L("nb_open", "reveal", "قبل الافتتاح يفحص المكتب موازين كل الأركان بصنجات مختومة، ويُدوَّن الفحص في جدول.", ["f_opening_table_exists"]),
      L("nb_unknown", "deflect_unknown", "لا أذكر."),
      L("nb_off", "deflect_offtopic", "اسألني عن السوق."),
      L("nb_bye", "farewell", "اسأل غيري أيضاً.")])
c.ch("abu_walid", "أبو وليد المعايِر", "expert", "مختص معايرة في مكتب السوق",
     "هادئ ودقيق، يقيس أكثر مما يتكلم، ويقول إن القياس الواحد لا يكفي. لا يعرف نيات الباعة.",
     ["أن تُقرأ القياسات بحدودها"],
     [L("aw_greet", "greeting", "أقيس ولا أحكم على النيات."),
      L("aw_ref", "reveal", "عندي صنجتان معياريتان مختومتان، خمسمئة غرام وألف غرام، وميزان مرجعي في المكتب. أستطيع فحص أي ميزان وأي غرض به.", ["f_ref_weights"]),
      L("aw_unknown", "deflect_unknown", "هذا خارج ما أقيسه."),
      L("aw_off", "deflect_offtopic", "اسألني عن القياس والصنجات."),
      L("aw_bye", "farewell", "كرّر القياس قبل أن تحكم.")])

locations = [{"id": "loc_stall", "name_ar": "ركن حامد رقم 12", "description_ar": "ركن لبيع التمور في سوق الأطلال، عليه ميزان ذو كفة."},
             {"id": "loc_office", "name_ar": "مكتب السوق", "description_ar": "حيث تُسجَّل الشكاوى والإعارات وتُحفظ الصنجات المعيارية."},
             {"id": "loc_market", "name_ar": "سوق الأطلال", "description_ar": "سوق قديم خيالي يستضيف أسبوع معرض القافلة."}]
objects = [{"id": "obj_scale", "name_ar": "ميزان حامد", "description_ar": "ميزان بكفة ونابض، مختوم من مكتب السوق."},
           {"id": "obj_tray", "name_ar": "الصينية الفولاذية المستعارة", "description_ar": "صينية معدنية استعارها حامد من جارته."}]
orgs = [{"id": "org_market", "name_ar": "إدارة سوق الأطلال", "description_ar": "جهة تنظيم السوق وحماية المستهلك فيه."}]

# ---------------------------------------------------------------- facts
c.F("f_complaint", "اشترت ليلى ثلاث عبوات تمر من ركن حامد عصر الثلاثاء، وتقول إن كل عبوة تنقص نحو ستين غراماً عن المكتوب عليها.", "event", ["layla", "hamed"], 0)
c.F("f_new_vendor", "حامد أحدث بائع في السوق، وهذا أسبوعه الأول.", "attribute", ["hamed"], 0)
c.F("f_hamed_denies", "ينفي حامد أنه غشّ أحداً.", "attribute", ["hamed"], 0)
c.F("f_bags_kept", "احتفظت ليلى بعبواتها مغلقة، ومعها زبونان آخران، وميزان مطبخها صالح للفحص في المكتب.", "state", ["layla"], 1, T(4380), "loc_office")
c.F("f_tray_swap", "استبدل حامد صباح الاثنين كفة ميزانه المتشققة بصينية فولاذية استعارها من جارته، ووضعها فوق الكفة.", "event", ["hamed", "obj_tray", "obj_scale"], 1, T(1580), "loc_stall")
c.F("f_tray_lent", "أعارت أم سمير حامداً الصينية الفولاذية الاثنين نحو الساعة 10:20.", "event", ["umm_samir", "hamed", "obj_tray"], 1, T(1580), "loc_market")
c.F("f_stock_sheet_exists", "يدوّن حامد يومياً ورقة مخزن فيها الكمية والمبيع والمتبقي بعد العد.", "state", ["hamed"], 1, None, "loc_stall")
c.F("f_loan_book_exists", "يحفظ مكتب السوق دفتر إعارة تُكتب فيه الأغراض المتبادلة بين الأركان.", "state", ["org_market"], 1, None, "loc_office")
c.F("f_opening_table_exists", "يفحص مكتب السوق قبل الافتتاح كل الموازين بصنجات مختومة ويدوّن الانحراف ويختم الميزان.", "state", ["org_market"], 1, T(-900), "loc_office")
c.F("f_ref_weights", "يملك المكتب صنجتين معياريتين مختومتين (500 غ و1000 غ) وميزاناً مرجعياً.", "state", ["abu_walid"], 1, None, "loc_office")
c.F("f_nabil_saw_change", "رأى نبيل حامداً صباح الاثنين يغيّر شيئاً في ميزانه.", "event", ["nabil", "hamed"], 1, T(1580), "loc_stall")
c.F("f_offsets_common", "ظهر انحراف في خمسة موازين من أربعة عشر ميزاناً عند فحص الافتتاح، ثلاثة منها لبائعين قدامى.", "state", ["org_market"], 1, T(-900), "loc_office")
c.F("f_offset_constant", "قراءة ميزان حامد تزيد زيادة ثابتة قدرها نحو ستين غراماً مهما كان الحمل، فهي إزاحة للصفر وليست نسبة من الوزن.", "relation", ["obj_scale"], 3, T(4470), "loc_stall", ["KO-RS-06-003", "KO-RS-05-003"])
c.F("f_tray_cause", "سبب الزيادة هو وزن الصينية المستعارة التي لم يُعدَّل الصفر بعد وضعها، لا عبث بآلية الميزان ولا قصد من أحد.", "relation", ["obj_tray", "obj_scale", "hamed"], 3, T(1580), "loc_stall", ["KO-RS-05-003", "KO-FC-04-019"])

c.claims += [
    {"id": "cl_hamed_fine", "statement_ar": "ميزاني سليم ولم أغيّر فيه شيئاً سوى الكفة.", "kind": "honest_mistake", "held_by": ["hamed"], "true_fact_id": "f_tray_cause", "contradicted_by_evidence_ids": ["ev_tray_weight", "ev_empty_test"]},
    {"id": "cl_nabil_new", "statement_ar": "كل بائع جديد يغشّ في أسبوعه الأول.", "kind": "rumour", "held_by": ["nabil"], "true_fact_id": "f_offsets_common", "contradicted_by_evidence_ids": ["ev_opening_table"]},
]

c.timeline += [
    {"id": "te_opening", "description_ar": "فحص الافتتاح لموازين الأركان وختمها.", "time": T(-900), "location_id": "loc_office", "actor_ids": ["abu_walid"], "fact_ids": ["f_opening_table_exists", "f_offsets_common"], "motivated_by_ar": "عمله إعداد السوق للأسبوع"},
    {"id": "te_swap", "description_ar": "حامد يضع الصينية المستعارة فوق كفته المتشققة.", "time": T(1580), "location_id": "loc_stall", "actor_ids": ["hamed", "umm_samir"], "fact_ids": ["f_tray_swap", "f_tray_lent"], "motivated_by_ar": "تشققت كفته ولا يريد أن يتوقف عن البيع"},
    {"id": "te_purchase", "description_ar": "ليلى تشتري ثلاث عبوات تمر.", "time": T(3420), "location_id": "loc_stall", "actor_ids": ["layla"], "fact_ids": ["f_complaint"], "motivated_by_ar": "تشتري تمراً لأسرتها"},
    {"id": "te_complaint", "description_ar": "ليلى تقدّم شكواها في مكتب السوق.", "time": T(4380), "location_id": "loc_office", "actor_ids": ["layla"], "fact_ids": ["f_complaint", "f_bags_kept"], "motivated_by_ar": "تريد أن يتأكد أحد من وزن العبوات"},
    {"id": "te_tests", "description_ar": "أبو وليد يختبر ميزان حامد بالصنجات المعيارية.", "time": T(4470), "location_id": "loc_stall", "actor_ids": ["abu_walid"], "fact_ids": ["f_offset_constant"], "motivated_by_ar": "كلّفه المكتب بفحص الشكوى"},
]

# ---------------------------------------------------------------- evidence
c.V("ev_complaint", "نموذج شكوى ليلى", "documentary",
    "مكتب سوق الأطلال — نموذج شكوى — الأربعاء 09:00\nالمشتكية: ليلى الحداد\nالمشكو منه: ركن 12 (حامد الرشيدي)\nالواقعة: اشتريت عصر الثلاثاء عبوة 1000 غ وعبوتين 500 غ، ووزنتها في بيتي فكانت 940 غ و440 غ و440 غ. أظن أن البائع الجديد يغشّ.\nملاحظة الموظف: ثلاثة زبائن آخرين ذكروا نقصاً مماثلاً شفهياً.",
    None, ["f_complaint", "f_new_vendor", "f_hamed_denies"], "moderate",
    "ادعاء مقدَّم بعد وزن بميزان منزلي لم يُفحص وقتها؛ والجملة الأخيرة ظن من المشتكية لا قياس. اتفاق الزبائن على النقص يؤكد وجود النقص لا سببه.",
    "اقرأ نموذج شكوى ليلى", red=True, loc="loc_office")
c.V("ev_empty_test", "اختبار الكفة الفارغة في ركن حامد", "observation",
    "مكتب السوق — محضر فحص — الأربعاء 10:30 — ركن 12 (الميزان كما وُجد، الصينية الفولاذية فوق الكفة، الختم رقم S-114 سليم)\nقراءة الميزان والكفة فارغة: 60 غ\nأعاد أبو وليد القراءة ثلاث مرات: 60 غ، 60 غ، 61 غ\nالطقس: ركن مظلل، طاولة مستوية.",
    "f_ref_weights", ["f_offset_constant", "f_tray_cause"], "strong",
    "قراءات متكررة لميزان واحد في ظرف واحد؛ تبيّن أن الميزان يقرأ شيئاً والكفة فارغة، ولا تبيّن سبب ذلك وحدها.",
    "اطلب نتيجة اختبار الكفة الفارغة", ko="KO-RS-06-003", loc="loc_stall")
c.V("ev_ref_test", "اختبار الصنجتين المعياريتين", "lab_result",
    "مكتب السوق — فحص بصنجات مختومة — الأربعاء 10:40 — ركن 12 (الصينية في مكانها)\nالصنجة 500 غ: قراءة 560 غ (560 · 560 · 561)\nالصنجة 1000 غ: قراءة 1060 غ (1060 · 1059 · 1060)\nالحد المسموح في لائحة السوق: ±5 غ.",
    "f_ref_weights", ["f_offset_constant"], "strong",
    "يقيس الميزان عند حملين فقط؛ نتيجته تستبعد خطأً نسبياً لكنها لا تفسر مصدر الزيادة وحدها، وتعتمد على سلامة الصنجتين المختومتين.",
    "اطلب نتيجة الصنجتين المعياريتين", ko="KO-FC-04-019", loc="loc_stall")
c.V("ev_tray_weight", "وزن الصينية على الميزان المرجعي", "observation",
    "مكتب السوق — الميزان المرجعي — الأربعاء 11:05\nالصينية الفولاذية المستعارة وحدها: 60 غ (60 · 60 · 61)\nملاحظة: الميزان المرجعي مضبوط على الصفر بصنجة 1000 غ قبل الفحص.",
    "f_ref_weights", ["f_tray_cause"], "strong",
    "يبيّن وزن الصينية لا أنها هي التي وُضعت على الكفة يوم الشراء؛ هذا يحتاج سجلاً مستقلاً بتاريخ الإعارة.",
    "اطلب وزن الصينية على الميزان المرجعي", loc="loc_office")
c.V("ev_bag_reweigh", "إعادة وزن اثنتي عشرة عبوة في المكتب", "observation",
    "مكتب السوق — الميزان المرجعي — الأربعاء 11:00 — عبوات مغلقة من ركن 12 اشتُريت الاثنين بعد العاشرة والنصف والثلاثاء\nعبوات مكتوب عليها 1000 غ (ست): 937 · 940 · 941 · 942 · 938 · 943\nعبوات مكتوب عليها 500 غ (ست): 437 · 440 · 441 · 442 · 438 · 443\nمنها عبوات ليلى الثلاث.",
    "f_bags_kept", ["f_offset_constant"], "strong",
    "عينة من اثنتي عشرة عبوة من زبائن وافقوا على إحضارها، لا كل ما بيع؛ وتقيس النقص لا سببه.",
    "أعد وزن العبوات المحفوظة في المكتب", loc="loc_office")
c.V("ev_stock_sheet", "ورقة مخزن حامد", "documentary",
    "ركن 12 — ورقة المخزن بخط حامد — من الاثنين 10:30 إلى الثلاثاء 19:00\nالمخزون عند 10:30 الاثنين: 100.0 كغ\nالمبيع المسجّل بالعلامات: 30 عبوة 1000 غ، و20 عبوة 500 غ\nالمتبقي بعد العدّ والوزن بميزان المكتب الثلاثاء 19:00: 63.0 كغ",
    "f_stock_sheet_exists", ["f_offset_constant"], "moderate",
    "ورقة بائع عن نفسه، لكنها كُتبت قبل الشكوى ويمكن مطابقتها بإعادة الوزن؛ تُظهر فائضاً في المتبقي دون تفسيره.",
    "اطلب ورقة مخزن حامد", loc="loc_stall")
c.V("ev_loan_book", "دفتر الإعارة في مكتب السوق", "documentary",
    "مكتب السوق — دفتر الإعارة — صفحة الاثنين\n10:20 — الغرض: صينية فولاذية — من: أم سمير (ركن 7) — إلى: حامد (ركن 12) — السبب: كفة الميزان تشققت — الإرجاع: نهاية الأسبوع\nالتوقيع: أم سمير · وتوقيع الموظف بالاستلام",
    "f_loan_book_exists", ["f_tray_swap", "f_tray_cause"], "strong",
    "سجل مكتوب لحظة الإعارة وتوقّع عليه جهة ثالثة؛ يثبت التاريخ والغرض ولا يثبت كيف وُضعت الصينية ولا أن الصفر لم يُعدَّل.",
    "اطلب دفتر الإعارة", loc="loc_office")
c.V("ev_opening_table", "جدول فحص الافتتاح لأربعة عشر ميزاناً", "documentary",
    "مكتب السوق — جدول فحص الافتتاح — السبت 17:00 (بصنجة 1000 غ)\nركن 12 (حامد، جديد): انحراف 0 غ — الختم S-114 وُضع\nركن 3 (نبيل، قديم): +40 · ركن 7 (أم سمير، قديمة): 0 · ركن 9 (قديم): +20 · ركن 5 (قديم): −30 · ركن 11 (جديد): +20 · ركن 13 (جديد): −10\nبقية الأركان (ثمانية): بين −5 و+5\nستة من الأركان الأربعة عشر لبائعين جدد هذا الأسبوع.",
    "f_opening_table_exists", ["f_offsets_common"], "strong",
    "سجل أصلي لحظة الفحص؛ يصف السبت فقط ولا يقول شيئاً عمّا تغيّر بعده. وضعت الأركان فيه بعد الفحص أرقام أختام جديدة لمن ضُبط ميزانه.",
    "اطلب جدول فحص الافتتاح", contradicts=["cl_nabil_new"], loc="loc_office")
c.V("ev_home_check", "فحص ميزان ليلى المنزلي", "observation",
    "مكتب السوق — الميزان المرجعي — الأربعاء 11:20\nميزان مطبخ ليلى: الصنجة 500 غ تقرأ 501 غ · الصنجة 1000 غ تقرأ 1000 غ\nالخلاصة المكتوبة: انحراف لا يتجاوز غراماً واحداً.",
    "f_bags_kept", ["f_bags_kept"], "strong",
    "يبيّن أن ميزان البيت دقيق في حملين؛ لا يفسّر النقص ولا يكفي وحده لاتهام أو براءة أحد.",
    "افحص ميزان ليلى المنزلي", loc="loc_office")
c.V("ev_hamed_statement", "إفادة حامد (ملخص)", "testimonial",
    "ملخص إفادة حامد الرشيدي:\n«تشققت الكفة صباح الاثنين فاستعرت صينية وضعتها فوقها حتى لا أتوقف عن البيع. لم أفتح الميزان ولم أكسر الختم، ولا أعرف شيئاً عن ضبط الصفر.»",
    "f_tray_swap", ["f_tray_swap"], "weak",
    "إفادة صاحب الشأن عن نفسه؛ تُقاس بسجلات لا يكتبها هو، ولا يدل ارتباكه ولا هدوؤه على صدقه.",
    "دوّن إفادة حامد", loc="loc_office")
c.V("ev_umm_statement", "إفادة أم سمير (ملخص)", "testimonial",
    "ملخص إفادة أم سمير الخياط:\n«أعرت حامداً صينيتي الاثنين العاشرة وعشرين دقيقة وكتبت الإعارة في الدفتر. لم أقل له شيئاً عن الميزان لأنني لم أتخيل أن الصينية ستغيّر القراءة.»",
    "f_tray_lent", ["f_tray_lent"], "moderate",
    "شهادة جارة عن فعلها هي؛ تؤيدها كتابة الدفتر ولا تغني عنه.",
    "دوّن إفادة أم سمير", loc="loc_office")
c.V("ev_nabil_statement", "إفادة نبيل (ملخص)", "testimonial",
    "ملخص إفادة نبيل الصعيدي:\n«البائع الجديد يغشّ في أسبوعه الأول، هذا ما رأيته مراراً. وصباح الاثنين شاهدت حامداً يغيّر شيئاً في ميزانه.»",
    "f_nabil_saw_change", ["f_nabil_saw_change"], "weak",
    "تعميم من تجربة شخصية وانطباع عن فعل لم يُحدَّد؛ لا يقول ما الذي تغيّر ولا يذكر قياساً.",
    "دوّن إفادة نبيل", red=True, loc="loc_office")

# ---------------------------------------------------------------- inferences
c.I("i_a_const", [E_("ev_empty_test"), E_("ev_ref_test")], "fact", "f_offset_constant", "establishes", "strong",
    "القراءة تبلغ 60 والكفة فارغة، وتصير 560 عند 500 و1060 عند 1000؛ فالفرق ثابت عند الأحمال الثلاثة، أي إزاحة للصفر لا خطأ نسبي.", ["KO-RS-06-003", "KO-RS-05-003"])
c.I("i_b_const", [E_("ev_bag_reweigh"), E_("ev_stock_sheet")], "fact", "f_offset_constant", "establishes", "strong",
    "النقص في العبوات 500 غ و1000 غ واحد تقريباً (نحو 60 غ)، والفائض في مخزن البائع 3.0 كغ يساوي 50 عبوة × 60 غ، ولو كان الخطأ نسبياً 6% لبلغ 2.4 كغ فقط.", ["KO-RS-06-003", "KO-RS-06-012"])
c.I("i_a_tray", [E_("ev_tray_weight"), E_("ev_empty_test")], "fact", "f_tray_cause", "establishes", "strong",
    "وزن الصينية على الميزان المرجعي 60 غ، وهو عين ما يقرؤه ميزان حامد فارغاً؛ فالزيادة تفسّرها الصينية.", ["KO-RS-05-003", "KO-FC-04-019"])
c.I("i_b_tray", [Fa("f_offset_constant"), E_("ev_loan_book"), E_("ev_opening_table")], "fact", "f_tray_cause", "establishes", "strong",
    "الميزان كان مضبوطاً ومختوماً السبت، والدفتر يضع تغيير الكفة الاثنين العاشرة وعشرين دقيقة، والإزاحة الثابتة ظهرت بعده؛ فأول ما تغيّر هو الصينية لا الآلية.", ["KO-RS-05-005", "KO-RS-05-004"])
c.I("i_support_tray", [Fa("f_offset_constant"), Fa("f_tray_cause")], "hypothesis", "h_tray", "supports", "strong",
    "إزاحة ثابتة تساوي وزن الصينية الموضوعة بلا ضبط تفسّر النقص كله في العبوات دون افتراض قصد.", ["KO-RS-06-007"])
c.I("i_rule_cheat", [Fa("f_offset_constant"), Fa("f_tray_cause")], "hypothesis", "h_cheat", "rules_out", "strong",
    "الغشّ المتعمد لا يترك ختماً سليماً ولا إزاحة تطابق وزن غرض مستعار مسجّل في دفتر عام؛ وكون البائع الأحدث ليس دليلاً بذاته.", ["KO-RS-06-008", "KO-RS-06-010"])
c.I("i_rule_home", [Fa("f_offset_constant"), Fa("f_tray_cause")], "hypothesis", "h_home", "rules_out", "strong",
    "الميزان المرجعي نفسه وجد الإزاحة في ميزان الركن وفي العبوات، فلا يتوقف الأمر على ميزان البيت.", ["KO-RS-06-008", "KO-RS-06-003"])
c.I("i_rule_noise", [Fa("f_offset_constant"), Fa("f_tray_cause")], "hypothesis", "h_noise", "rules_out", "strong",
    "القراءات المتكررة تتفاوت بغرام واحد، أما الفرق فستون غراماً وثابت؛ وهو أكبر من الحد المسموح بكثير.", ["KO-RS-06-013", "KO-RS-06-003"])
c.I("i_cl_hamed", [Fa("f_tray_cause")], "claim", "cl_hamed_fine", "contradicts_claim", "strong",
    "قوله إن الميزان سليم صادق في ظنه، لكن القياس يبيّن أن وضع الصينية غيّر القراءة.", ["KO-RS-05-014"])
c.I("i_cl_nabil", [E_("ev_opening_table")], "claim", "cl_nabil_new", "contradicts_claim", "strong",
    "ثلاثة من خمسة موازين منحرفة لبائعين قدامى، ومنها ميزان القائل نفسه، فالجِدّة لا تفسّر الانحراف.", ["KO-RS-06-010"])

# ---------------------------------------------------------------- character knowledge
c.ck += [
    {"character_id": "layla", "knows": [K("f_bags_kept")], "hides": [], "believes": []},
    {"character_id": "hamed", "knows": [K("f_tray_swap"), K("f_stock_sheet_exists")], "hides": [], "believes": [{"claim_id": "cl_hamed_fine", "stance": "sincere"}]},
    {"character_id": "umm_samir", "knows": [K("f_tray_lent"), K("f_loan_book_exists", "professional")], "hides": [], "believes": []},
    {"character_id": "nabil", "knows": [K("f_nabil_saw_change", "witnessed", "unsure"), K("f_opening_table_exists", "common_knowledge")], "hides": [], "believes": [{"claim_id": "cl_nabil_new", "stance": "sincere"}]},
    {"character_id": "abu_walid", "knows": [K("f_ref_weights", "professional")], "hides": [], "believes": []},
]
hyps = [
    {"id": "h_cheat", "statement_ar": "تعمّد حامد التلاعب بميزانه ليبخس الزبائن، فهو الأحدث في السوق.", "is_true": False, "plausibility_at_start": "high", "suspect_id": "hamed"},
    {"id": "h_tray", "statement_ar": "زاد ميزان حامد قراءته زيادة ثابتة لأن صينية مستعارة وُضعت على كفته دون ضبط الصفر، فنقصت العبوات دون قصد من أحد.", "is_true": True, "plausibility_at_start": "low", "suspect_id": "hamed"},
    {"id": "h_home", "statement_ar": "ميزان ليلى المنزلي هو المخطئ، والعبوات سليمة.", "is_true": False, "plausibility_at_start": "medium", "suspect_id": "layla"},
    {"id": "h_noise", "statement_ar": "النقص في حدود التفاوت العادي للقياس ولا يستحق شكوى.", "is_true": False, "plausibility_at_start": "medium"},
]
mis = [
    {"id": "rh_new", "points_to_hypothesis_id": "h_cheat", "planted_via_ar": "نبيل يقول إن الجدد يغشّون، وحامد أحدثهم؛ والشكوى نفسها تسمّيه.", "evidence_ids": ["ev_nabil_statement", "ev_complaint"],
     "refuted_by_inference_ids": ["i_cl_nabil", "i_rule_cheat"],
     "fairness_note_ar": "جدول الافتتاح في متناول اللاعب ويُظهر انحرافاً في موازين قديمة وجديدة، والجِدّة وحدها ليست قياساً."},
    {"id": "rh_change", "points_to_hypothesis_id": "h_cheat", "planted_via_ar": "نبيل رأى حامداً يغيّر شيئاً في ميزانه صباح الاثنين.", "evidence_ids": ["ev_nabil_statement"],
     "refuted_by_inference_ids": ["i_a_tray", "i_b_tray", "i_rule_cheat"],
     "fairness_note_ar": "دفتر الإعارة ووزن الصينية يفسّران ما رآه نبيل بوضوح، وإفادته لا تحدد ما تغيّر."},
    {"id": "rh_home", "points_to_hypothesis_id": "h_home", "planted_via_ar": "ليلى وزنت بميزان مطبخ لم يُفحص وقت الشكوى.", "evidence_ids": ["ev_complaint"],
     "refuted_by_inference_ids": ["i_rule_home", "i_a_const"],
     "fairness_note_ar": "فحص المكتب لميزان الركن وللعبوات يحدث بميزان مرجعي لا علاقة له بميزان البيت."},
]
los = [
    {"id": "lo_source", "statement_ar": "يصنّف الشكوى والإفادات أقوالاً، ويميّز الفحوص المباشرة والسجلات من الأقوال.", "skill_ko_ref": "KO-RS-05-001", "observable_behaviors_ar": ["يصنّف الشكوى والإفادات أقوالاً", "يعدّ محاضر الفحص سجلات أصلية"], "evidence_sources": ["evidence_board"]},
    {"id": "lo_conflict", "statement_ar": "يرتّب الأحداث على خط زمني يضع تغيير الكفة بعد الفحص المختوم وقبل الشراء.", "skill_ko_ref": "KO-RS-05-005", "observable_behaviors_ar": ["يضع الأدلة في أزمنتها"], "evidence_sources": ["timeline_task", "action_log"]},
    {"id": "lo_links", "statement_ar": "يقدّر ما يثبته كل فحص وما لا يثبته ويربطه بالفرضية باتجاه صحيح.", "skill_ko_ref": "KO-RS-06-001", "observable_behaviors_ar": ["يربط الدليل بالفرضية", "يفرّق الإزاحة الثابتة عن الخطأ النسبي"], "evidence_sources": ["evidence_board", "final_justification"]},
    {"id": "lo_calib", "statement_ar": "يصوغ نسبة الترجيح بحدودها ويذكر ما قد يغيّر رأيه.", "skill_ko_ref": "KO-RS-06-021", "observable_behaviors_ar": ["يختار ثقة معقولة", "يذكر حدوداً"], "evidence_sources": ["final_justification"]},
    {"id": "lo_revise", "statement_ar": "يراجع رأيه الأول حين يظهر ما يخالفه.", "skill_ko_ref": "KO-RS-06-009", "observable_behaviors_ar": ["يغيّر فرضيته الرائدة بدليل"], "evidence_sources": ["hypothesis_ledger"]},
    {"id": "lo_elim", "statement_ar": "يختار الاختبار الذي يميّز بين التفسيرات ويستبعد ما تنقضه الأدلة.", "skill_ko_ref": "KO-RS-05-003", "observable_behaviors_ar": ["يضيف فرضيات", "يستبعد بدليل"], "evidence_sources": ["hypothesis_ledger"]},
    {"id": "lo_just", "statement_ar": "يكتب حجة تربط الأدلة بالاستنتاج وتذكر أن الفحص لا يقيس النية.", "skill_ko_ref": "KO-RS-06-007", "observable_behaviors_ar": ["يكتب حجة معللة"], "evidence_sources": ["final_justification"]},
]
topics = [
    {"id": "t_bags", "label_ar": "العبوات المحفوظة", "example_questions_ar": ["هل ما زالت عبواتك عندك؟", "هل يمكن فحص ميزانك؟"], "fact_ids": ["f_bags_kept"]},
    {"id": "t_pan", "label_ar": "الكفة والصينية", "example_questions_ar": ["هل غيّرت شيئاً في ميزانك؟", "ما الذي تشقق؟"], "fact_ids": ["f_tray_swap"], "claim_ids": ["cl_hamed_fine"]},
    {"id": "t_stock", "label_ar": "ورقة المخزن", "example_questions_ar": ["هل تدوّن مبيعاتك؟", "كيف تعدّ المتبقي؟"], "fact_ids": ["f_stock_sheet_exists"]},
    {"id": "t_lent", "label_ar": "إعارة الصينية", "example_questions_ar": ["هل أعرتِ حامداً شيئاً؟", "متى؟"], "fact_ids": ["f_tray_lent"]},
    {"id": "t_book", "label_ar": "دفتر الإعارة", "example_questions_ar": ["أين تُكتب الإعارات؟"], "fact_ids": ["f_loan_book_exists"]},
    {"id": "t_newvendor", "label_ar": "الباعة الجدد", "example_questions_ar": ["ماذا تقول عن البائع الجديد؟", "ماذا رأيت صباح الاثنين؟"], "fact_ids": ["f_nabil_saw_change"], "claim_ids": ["cl_nabil_new"]},
    {"id": "t_opening", "label_ar": "فحص الافتتاح", "example_questions_ar": ["كيف تُفحص الموازين قبل الافتتاح؟"], "fact_ids": ["f_opening_table_exists"]},
    {"id": "t_ref", "label_ar": "الصنجات المعيارية", "example_questions_ar": ["ماذا يملك المكتب للقياس؟", "ماذا يمكنك أن تفحص؟"], "fact_ids": ["f_ref_weights"]},
]

# ---------------------------------------------------------------- hints
he = lambda e: {"has_evidence": e}
al = {"always": True}
c.H("hg1", 1, "metacognitive", "قبل أن تحكم على البائع الأحدث: ما التفسيرات الأخرى الممكنة للنقص نفسه؟", al, None, 0.02)
c.H("hg2", 2, "focus_area", "اختر اختباراً يعطي نتيجة مختلفة إذا كان التفسير هذا لا ذاك، لا اختباراً يوافق الجميع.", he("ev_complaint"), None, 0.04)
c.H("hg3", 3, "pointer", "اسأل صاحب القياس عن أدواته، ثم قارن قراءة الكفة الفارغة بقراءتها عند حملين مختلفين.", he("ev_complaint"), None, 0.08)
c.H("ht1", 1, "metacognitive", "هل الفرق يكبر مع الوزن أم يبقى كما هو؟ ماذا يعني كل منهما؟", he("ev_empty_test"), "i_a_tray", 0.02)
c.H("ht2", 2, "pointer", "قارن مقدار القراءة والكفة فارغة بوزن الصينية على الميزان المرجعي.", he("ev_empty_test"), "i_a_tray", 0.06)
c.H("ht3", 3, "partial_reveal", "الرقمان متساويان: 60 غ، فاسأل متى وُضع الغرض الذي وزنه ستون غراماً على الكفة.", he("ev_tray_weight"), "i_a_tray", 0.1)
c.H("hb1", 1, "metacognitive", "ما الذي تغيّر في هذا الركن بين فحص السبت ويوم الشراء؟", he("ev_opening_table"), "i_b_tray", 0.02)
c.H("hb2", 2, "pointer", "ابحث عن سجل يكتبه طرف ثالث لا علاقة له بحامد ولا بليلى.", he("ev_opening_table"), "i_b_tray", 0.06)

# ---------------------------------------------------------------- build
steps = [
    (1, "ابدأ بنوع الخطأ لا بالمتهم: ميزان الركن يقرأ زيادة متساوية عند الصفر وعند الحملين المعياريين، فالإزاحة ثابتة.", ["ev_empty_test", "ev_ref_test"], "i_a_const"),
    (2, "الطريق المستقل لنوع الخطأ: العبوات الصغيرة والكبيرة ينقصها المقدار نفسه تقريباً، وفائض مخزن البائع يطابق هذا المقدار مضروباً في عدد العبوات.", ["ev_bag_reweigh", "ev_stock_sheet"], "i_b_const"),
    (3, "ما يعادل هذه الإزاحة موجود: صينية مستعارة وزنها يطابق القراءة الفارغة، وهذا يُبعد فكرة تلاعب بالنابض.", ["ev_tray_weight", "ev_empty_test"], "i_a_tray"),
    (4, "السجلات الثلاثة المستقلة تضع التغيير في موضعه: ضبط وختم يوم السبت، ثم إعارة مكتوبة يوم الاثنين، ثم قراءة ثابتة الزيادة.", ["ev_opening_table", "ev_loan_book"], "i_b_tray"),
    (5, "الجِدّة ليست قياساً: بين الموازين المنحرفة موازين لباعة قدامى، فالتعميم عن الجدد لا يفسّر ميزان حامد.", ["ev_opening_table", "ev_nabil_statement"], "i_cl_nabil"),
    (6, "البدائل تسقط بالقياس نفسه: ميزان البيت دقيق ولا يقرّر النتيجة، والتفاوت العادي غرام واحد لا ستين.", ["ev_home_check", "ev_bag_reweigh", "ev_ref_test"], "i_rule_noise"),
]
ending = {"steps": steps,
    "alt": ["يكفي طريق المكتب وحده: الكفة الفارغة والصنجتان ووزن الصينية، من غير إعادة وزن العبوات.",
            "ويكفي طريق السجلات وحده: العبوات المحفوظة وورقة المخزن ودفتر الإعارة وجدول السبت، من غير قياسات المكتب في الركن؛ والأقوى أن يتفق الطريقان."],
    "limits": ["القياسات تثبت سبباً ميكانيكياً وتسلسلاً زمنياً، ولا تقيس نية أحد؛ نستنتج غياب القصد من اجتماع السبب البسيط مع الختم السليم.",
               "فحصنا عبوات من زبائن وافقوا على إحضارها، لا كل ما بيع في الأسبوع.",
               "لا نعرف كم زبوناً اشترى بعد الاثنين وتضرر، ولا نعرف إن كان يمكن تعويضهم كلهم."],
    "notes": ["عند الشك في ميزان ابدأ بالكفة الفارغة ثم بوزنين معياريين: إزاحة ثابتة تعني خطأ صفر، وزيادة تكبر مع الوزن تعني خطأ نسبياً، وكل منهما سبب مختلف وعلاج مختلف.",
              "الاختبار المميِّز مقدَّم على الاتهامي: اختبار يعطي النتيجة نفسها سواء غشّ البائع أو لم يغشّ لا يفيد.",
              "التكرار يكشف التفاوت العادي: ثلاث قراءات تتفاوت بغرام، فلا يصح أن نسمّي فرق ستين غراماً تفاوتاً.",
              "المحتسب في هذه القضية مفتش حماية مستهلك: يقيس ويُبلّغ ويصلح، ولا يتهم أحداً قبل الفحص.",
              "الحل الودّي: تُضبط الكفة بعد وضع الصينية أو تُعاد الكفة المتشققة، ويُعوَّض الزبائن عن النقص، ويُسجَّل في دفتر الإعارة أن أي غرض يوضع على الكفة يستلزم إعادة الضبط.",
              "بطاقة الأصل: القضية أصلية من ATHAR، وبنيتها مستلهمة من أخبار منسوبة في كتب الحسبة عن الموازين والصنج (نسبتها مختلف فيها)."]}
core_meta = {"title_ar": "المحتسب الصغير: ميزان السوق", "title_en": "The Little Inspector: The Market Scale", "age_band": "13-15", "locale": "ar", "dialogue_register": "msa", "estimated_minutes": 30, "difficulty": 2,
             "content_flags": ["no_violence"], "authors": ["فريق أثر التحريري (مسودة بمساعدة الذكاء الاصطناعي، لم تُراجَع بشرياً بعد)"],
             "knowledge_object_refs": ["KO-RS-05-003", "KO-RS-06-008", "KO-RS-06-010", "KO-RS-06-003", "KO-RS-05-001", "KO-RS-05-005", "KO-RS-05-004", "KO-RS-06-001", "KO-RS-06-021", "KO-RS-06-009", "KO-RS-06-012", "KO-RS-06-013", "KO-FC-04-019", "KO-CD-02H-004"]}
premise = {"hook_ar": "ثلاثة زبائن يقولون إن عبواتهم ناقصة، وكل الأنظار على البائع الأحدث في السوق. لكنك محتسب صغير: تقيس أولاً ثم تحكم.",
           "player_role_ar": "أنت محتسب صغير متدرب في مكتب سوق الأطلال، مهمتك حماية الزبائن بالقياس لا بالتخمين، وعندك ميزان مرجعي وصنجتان معياريتان.",
           "setting_ar": "سوق الأطلال خلال أسبوع معرض القافلة، من السبت قبل الافتتاح إلى صباح الأربعاء. أوقات المكتب بساعة السوق.",
           "public_fact_ids": ["f_complaint", "f_new_vendor", "f_hamed_denies"],
           "assumed_general_knowledge_ar": ["القياس الواحد قد يخطئ فيُكرَّر", "الميزان قد يقرأ زيادة ثابتة أو زيادة تكبر مع الوزن", "كون البائع جديداً لا يدل على شيء"]}
solution = {"culprit_ids": ["hamed"], "summary_ar": "لم يغشّ أحد. وضع حامد صينية مستعارة فوق كفته المتشققة ولم يعرف أن الصفر يحتاج إلى ضبط، فصار الميزان يقرأ ستين غراماً زائدة في كل وزنة وخرجت العبوات ناقصة بالمقدار نفسه.",
            "key_fact_ids": ["f_offset_constant", "f_tray_cause"]}
ref = "لا دليل على أن حامداً غشّ. ميزانه يقرأ زيادة ثابتة نحو 60 غ والكفة فارغة وعند 500 غ وعند 1000 غ، والعبوات الصغيرة والكبيرة تنقص بالمقدار نفسه، وهذا شأن إزاحة صفر لا خطأ نسبي. وزن الصينية المستعارة يطابق الزيادة، ودفتر الإعارة يضعها يوم الاثنين بعد فحص السبت المختوم. وجِدّة البائع ليست دليلاً، فبين الموازين المنحرفة موازين قديمة. حدود الاستنتاج: القياس لا يثبت النية، وعينة العبوات محدودة بمن أحضرها."
ui = {
    "clock": {"epoch_hhmm": "08:00", "zone_label_ar": "ساعة السوق (الأحد 08:00 = البداية)"},
    "cover": {"title_ar": "المحتسب الصغير: ميزان السوق", "tagline_ar": "ثلاث عبوات ناقصة… ومن الأسهل أن تتهم الأحدث.", "kicker_ar": "الملف الثاني والعشرون · القياس قبل الحكم", "glyph": "⚖", "accent": "amber"},
    "cold_open_ar": ["الأربعاء صباحاً، مكتب سوق الأطلال.", "ليلى تضع ثلاث عبوات تمر أمامك، وتقول إنها ناقصة. صاحب الركن بائع جديد في أسبوعه الأول، وبعض الباعة القدامى متأكدون أنه يغشّ.",
                     "عندك ميزان مرجعي وصنجتان مختومتان. أي قياس يفرّق بين الغش وبين خطأ بريء؟"],
    "limit_menu": [
        {"id": "l_intent", "label_ar": "القياسات تثبت سبباً ميكانيكياً وتسلسلاً زمنياً ولا تقيس نية البائع"},
        {"id": "l_sample", "label_ar": "فحصنا عينة من العبوات وبعض الموازين، لا كل ما بيع في الأسبوع"},
        {"id": "l_unknown_buyers", "label_ar": "لا نعرف كم زبوناً تضرر بعد الاثنين"},
        {"id": "l_invalid_new", "label_ar": "كون حامد أحدث بائع يرجّح أنه تعمّد النقص"},
        {"id": "l_invalid_three", "label_ar": "اتفاق ثلاثة زبائن على النقص يثبت أن البائع تعمّد ذلك"},
        {"id": "l_invalid_nervous", "label_ar": "ارتباك حامد أثناء المقابلة يدل على إخفائه شيئاً"}],
    "mind_change_menu": [
        {"id": "m_tray_light", "label_ar": "ظهور أن الصينية تزن أقل بكثير من 60 غراماً"},
        {"id": "m_seal_broken", "label_ar": "ظهور أثر فتح الميزان أو كسر ختمه بعد السبت"},
        {"id": "m_loan_date", "label_ar": "ظهور أن الإعارة وقعت بعد يوم الشراء لا قبله"},
        {"id": "m_popular", "label_ar": "كثرة من يرددون أن الباعة الجدد يغشّون"}],
    "transfer": {
        "id": "tr_honey", "title_ar": "اختبار نقل المهارة: العسل الذي تبلور",
        "scenario_ar": "زبون يقول إن عسلاً اشتراه صار أبيض خشناً بعد أسبوعين، ويتهم البائع بأنه غشّه بسكر. أمامك وثيقتان من واقعة خيالية لا علاقة لها بالقضية.",
        "documents": [
            {"title_ar": "ملاحظة المكتب", "body_ar": "العسل الطبيعي كثيراً ما يتبلور مع الوقت أو مع البرودة، وليس كل تبلور علامة غش. البرطمانات المحفوظة في دفء ثابت تتأخر في التبلور."},
            {"title_ar": "سجل البائع", "body_ar": "حفظ البائع برطمانين من الدفعة نفسها في خزانة المكتب المختومة، أحدهما في ركن بارد والآخر في ركن دافئ. تتبلور الأول بعد أسبوعين، وبقي الثاني صافياً بعد شهر."}],
        "prompt_ar": "اختر الخطوات التي تصلح لتقرير ما إذا كان التبلور يدل على غش (يمكنك اختيار أكثر من خطوة).",
        "options": [
            {"id": "o1", "text_ar": "مقارنة عينتين من الدفعة نفسها بظروف حفظ مختلفة"},
            {"id": "o2", "text_ar": "البحث عن تفسير طبيعي معروف للتبلور قبل الاتهام"},
            {"id": "o3", "text_ar": "طلب اختبار تأكيدي من جهة مختصة قبل أي حكم"},
            {"id": "o4", "text_ar": "تكرار الملاحظة على عدة برطمانات لا على برطمان واحد"},
            {"id": "o5", "text_ar": "اعتبار تبلور العسل دليلاً على الغش"},
            {"id": "o6", "text_ar": "الحكم على البائع لأنه الأحدث في السوق"},
            {"id": "o7", "text_ar": "تذوّق العسل للحكم على صدقه"}],
        "free_text_prompt_ar": "اكتب في ثلاثة أسطر كيف تقرّر نسبة الترجيح بأن البائع غشّ، ولماذا لا تكفي الملاحظة الواحدة.",
    },
    "skills": [{"skill_id": "KO-RS-05-003", "track": "B"}, {"skill_id": "KO-RS-06-008", "track": "D"}, {"skill_id": "KO-RS-06-003", "track": "B"}, {"skill_id": "KO-RS-06-010", "track": "D"}, {"skill_id": "KO-FC-04-019", "track": "E"}],
    "stage_hooks_ar": {"briefing": "ثلاث عبوات ناقصة… فما الاختبار الذي يفرّق بين الغشّ والخطأ؟", "investigating": "قِس الكفة وهي فارغة، ثم قِس بالصنجات؛ الشكل الذي يظهر يخبرك بنوع الخطأ.", "review": "قبل الحكم: ماذا تثبت قياساتك وماذا لا تثبت؟", "resolved": "أُغلق الملف. الزبائن عُوّضوا، وبقي سؤال عن شكوى أخرى في السوق."},
    "character_glyphs": {"layla": "ل", "hamed": "ح", "umm_samir": "أ", "nabil": "ن", "abu_walid": "و"},
}
sc = {
    "case_id": CID,
    "accepted_conclusions": {
        "h_tray": {"grade": 1, "note_ar": "استنتاج متسق مع القياسات والسجلات ويتطلب ذكر حدوده."},
        "h_cheat": {"grade": 0, "note_ar": "يبني الاتهام على جدّة البائع وانطباع جاره، ويتجاهل الختم السليم وتطابق الإزاحة مع وزن الصينية."},
        "h_home": {"grade": 0, "note_ar": "ميزان البيت دقيق، والميزان المرجعي وجد الإزاحة في ميزان الركن نفسه."},
        "h_noise": {"grade": 0, "note_ar": "التفاوت العادي غرام واحد، والفرق هنا ستون غراماً وثابت."}},
    "confidence_band": {"h_tray": [65, 90], "h_cheat": [0, 15], "h_home": [0, 15], "h_noise": [0, 15]},
    "source_key": {"ev_complaint": "claim", "ev_empty_test": "primary_record", "ev_ref_test": "primary_record", "ev_tray_weight": "primary_record", "ev_bag_reweigh": "primary_record", "ev_stock_sheet": "primary_record",
                   "ev_loan_book": "primary_record", "ev_opening_table": "primary_record", "ev_home_check": "primary_record", "ev_hamed_statement": "claim", "ev_umm_statement": "claim", "ev_nabil_statement": "claim"},
    "link_key": {
        "h_tray": {"ev_empty_test": "supports", "ev_ref_test": "supports", "ev_tray_weight": "supports", "ev_bag_reweigh": "supports", "ev_stock_sheet": "supports", "ev_loan_book": "supports",
                   "ev_opening_table": "supports", "ev_umm_statement": "supports", "ev_hamed_statement": "supports", "ev_nabil_statement": "neutral"},
        "h_cheat": {"ev_complaint": "supports", "ev_nabil_statement": "supports", "ev_empty_test": "weakens", "ev_tray_weight": "weakens", "ev_loan_book": "weakens", "ev_opening_table": "weakens", "ev_stock_sheet": "neutral"},
        "h_home": {"ev_complaint": "supports", "ev_home_check": "weakens", "ev_bag_reweigh": "weakens", "ev_ref_test": "weakens"},
        "h_noise": {"ev_empty_test": "weakens", "ev_ref_test": "weakens", "ev_bag_reweigh": "weakens", "ev_stock_sheet": "weakens"},
    },
    "required_limits": ["l_intent", "l_sample"], "valid_mind_changers": ["m_tray_light", "m_seal_broken", "m_loan_date"],
    "invalid_limits": ["l_invalid_new", "l_invalid_three", "l_invalid_nervous"],
    "decisive_evidence": ["ev_empty_test", "ev_ref_test", "ev_tray_weight", "ev_bag_reweigh", "ev_stock_sheet", "ev_loan_book", "ev_opening_table"],
    "lab_requirement": None,
    "timeline_requirement": [{"evidence_id": "ev_opening_table", "utc_minute": -900, "tol": 30}, {"evidence_id": "ev_loan_book", "utc_minute": 1580, "tol": 20},
                             {"evidence_id": "ev_complaint", "utc_minute": 4380, "tol": 20}, {"evidence_id": "ev_empty_test", "utc_minute": 4470, "tol": 20}, {"evidence_id": "ev_tray_weight", "utc_minute": 4505, "tol": 20}],
    "refuted_hypotheses": ["h_cheat", "h_home", "h_noise"],
    "criteria_map": {"c_source": "source_typing", "c_conflict": "conflict_resolution", "c_links": "hypothesis_links", "c_uncertainty": "uncertainty", "c_revision": "revision", "c_elimination": "elimination", "c_justification": "justification_human"},
    "transfer_key": {"valid": ["o1", "o2", "o3", "o4"], "invalid": ["o5", "o6", "o7"]},
    "caps": {"no_citations_max": 45, "no_conflict_resolution_max": 65},
}
c.build(OUT, meta=core_meta, premise=premise, solution=solution, locations=locations, objects=objects, orgs=orgs, hyps=hyps, mis=mis, los=los, reference_answer=ref, ending=ending, ui=ui, sc=sc, topics=topics)
