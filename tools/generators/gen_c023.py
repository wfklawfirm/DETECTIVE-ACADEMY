#!/usr/bin/env python3
# Case c023 «القلم الذي أشار إلى رسالة قديمة» — archetype ARC-21 «الاختبار الدقيق بنسبة 95%» in its 16-18 variant (base rate + likelihood-ratio language),
# age band 16-18, difficulty 3. Teaches: a screening test that is «95% accurate» says little when the target is rare (build the natural-frequency
# table: 20 forged letters in 1000, so about 19 true flags against about 49 false flags); a preliminary result is a reason to run the
# CONFIRMATORY test, not a verdict; and a false flag usually has a mechanical cause that can be found (here a protective coating).
# Uses the Arabic terms «نسبة الترجيح» (likelihood ratio = sensitivity / false-flag rate = 19) and «المعدل الأساسي». The «odds ratio» term is not used.
# No-culprit convention: the conservator who coated the letter in good faith in 2019 (Rana) is recorded in culprit_ids; the donor (Salem) did nothing wrong.
# Deviations from ARC-21 (honest list): the archetype's fictional «المادة س» preliminary test is re-skinned as a fictional UV «quick-screen pen» on old
# letters (museum-gate variant from the archetype's own list is used for the skill-transfer task); the engine has no free-form table-building
# mechanic, so the frequency table is carried by a screening-statistics record + a rule in the evidence graph; and the virtual lab #15 is not built
# (labs: [] - the confirmatory result is an evidence item obtained by interview). Nothing in the case is a drug or a harmful substance.
# Calendar (fictional): minute 0 = Monday 09:00. Tue 10:15 = 1515; Tue 14:00 = 1740; Wed 11:00 = 3000; Wed 11:30 = 3030; Wed 14:00 = 3180.
# Usage: gen_c023.py OUT_DIR
import sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
from _lib_c022_c025 import *

OUT = sys.argv[1]
CID = "c023_quick_screen_pen"
c = Case(CID)

# ---------------------------------------------------------------- characters
c.ch("dalia", "داليا النجار", "authority", "أمينة المجموعات في متحف الأثر",
     "حازمة وسريعة الحكم تحت ضغط الوقت، تثق بالأرقام المكتوبة على الأجهزة وتحب القرارات الواضحة. تراجع رأيها إذا رأت جدولاً مقنعاً.",
     ["حماية المجموعة من التزوير", "ألا تظلم أحداً"],
     [L("dl_greet", "greeting", "الجهاز دقيق بنسبة خمس وتسعين بالمئة، فلا داعي للتأخير."),
      L("dl_claim", "reveal", "إذا كان الجهاز دقيقاً بنسبة 95% وأشار إلى الرسالة، فهي مزورة بنسبة 95% تقريباً.", None, ["cl_pen_95"]),
      L("dl_unknown", "deflect_unknown", "لا أعرف أكثر من تقرير الفرز."),
      L("dl_off", "deflect_offtopic", "اسألني عن قرار تعليق الهبة."),
      L("dl_bye", "farewell", "أريد قراراً مبنياً على أرقام صحيحة.")])
c.ch("salem", "سالم المنصوري", "suspect", "واهب الرسالة، تاجر متقاعد",
     "متأنٍّ ومعتز بإرث عائلته، يتألم من التلميح بأنه مزوّر، ويجيب بهدوء ويقدّم ما عنده من أوراق.",
     ["أن تُحفظ الرسالة في المتحف", "أن تبقى سمعة عائلته"],
     [L("sl_greet", "greeting", "الرسالة كانت في صندوق جدي. لا أخفي شيئاً."),
      L("sl_origin", "reveal", "ورثت الرسالة عن عائلتي، وسلّمتها للمتحف عام 2018 ولم أرمّمها أنا، وحفظ المتحف كل أوراقها.", ["f_donor_says"]),
      L("sl_insure", "reveal", "سألت المتحف الشهر الماضي عن قيمة الرسالة لأن شركة التأمين على بيتي طلبت قائمة بمقتنياتي.", ["f_insurance_asked"]),
      L("sl_unknown", "deflect_unknown", "لا أعرف أكثر."),
      L("sl_off", "deflect_offtopic", "اسألني عن الرسالة وعائلتها."),
      L("sl_bye", "farewell", "أريد أن يُفحص الأمر فحصاً عادلاً.")])
c.ch("rana", "رنا الحسيني", "suspect", "مرمّمة ورق في المتحف",
     "دقيقة ومتحفظة وتكتب كل شيء في سجلها. تتألم إذا ظُن أن عملها أضرّ بالقطعة، وتشرح بالتفصيل حين تُسأل عما فعلته.",
     ["أن يُقرأ سجل الترميم", "ألا يُنسب إليها ما لم تفعله"],
     [L("rn_greet", "greeting", "كل ما فعلته بالرسالة مكتوب في سجلي."),
      L("rn_log", "reveal", "رمّمت الرسالة عام 2019 ووضعت على صفحتها طبقة حماية شفافة رقيقة، ودوّنت ذلك في سجل الترميم.", ["f_coating_applied", "f_restoration_log_exists"]),
      L("rn_unknown", "deflect_unknown", "هذا ليس في سجلي."),
      L("rn_off", "deflect_offtopic", "اسألني عن الترميم."),
      L("rn_bye", "farewell", "السجل أمامكم فاقرؤوه.")])
c.ch("hala", "هالة الشامي", "witness", "أمينة السجل في المتحف",
     "منظمة وهادئة، تقرأ من ملفاتها ولا تخمّن. تفرّق بين ما سُجّل وما افترضه الناس.",
     ["أن تبقى الملفات سليمة"],
     [L("hl_greet", "greeting", "الملفات أمامي، أقرأ منها."),
      L("hl_file", "reveal", "ملف الهبة يضم جرداً عائلياً موثقاً عند كاتب عدل، وسجل التبرع عام 2018. وصُوِّرت الرسالة يومها لدليل المتحف.", ["f_donation_file_exists", "f_photo_2018_exists"]),
      L("hl_unknown", "deflect_unknown", "هذا ليس في ملفاتي."),
      L("hl_off", "deflect_offtopic", "اسأل عن الملفات."),
      L("hl_bye", "farewell", "الملف يبقى كما هو.")])
c.ch("tarek", "طارق البيطار", "expert", "فني مختبر الفحص في المتحف",
     "عملي وصريح، يذكر حدود جهازه قبل نتائجه ويكرر الفحص ويقارن بعينات معلومة. لا يعرف نيات أحد.",
     ["أن تُقرأ نتائج الأجهزة بحدودها"],
     [L("tk_greet", "greeting", "قلم الفرز أداة فرز سريعة، ولا أحكم بها وحدها."),
      L("tk_methods", "reveal", "عندنا فحص تأكيدي بالمجهر للحبر، ومصباح فوق بنفسجي لتصوير الصفحة كلها بدل الخطوط وحدها.", ["f_confirm_available", "f_uv_lamp_available"]),
      L("tk_pen", "reveal", "للقلم دليل استعمال ينص على حساسيته ومحاذيره، وعندنا سجل لرسائل فرزناها العام الماضي ثم أكدناها بالفحص.", ["f_pen_manual_exists", "f_stats_exist"]),
      L("tk_controls", "reveal", "أستطيع أن أجرّب القلم على أوراق قديمة معلومة الأصل، بعضها مطلي وبعضها غير مطلي، وأن أقارن.", ["f_controls_possible"]),
      L("tk_unknown", "deflect_unknown", "هذا خارج ما أقيسه."),
      L("tk_off", "deflect_offtopic", "اسألني عن القلم والفحوص."),
      L("tk_bye", "farewell", "ابدأ بالعدّ قبل أن تثق بالنسبة.")])

locations = [{"id": "loc_lab", "name_ar": "مختبر الفحص", "description_ar": "مختبر صغير في متحف الأثر فيه مجهر ومصباح فوق بنفسجي."},
             {"id": "loc_registry", "name_ar": "مكتب السجل", "description_ar": "حيث تُحفظ ملفات الهبات وصور الفهرسة."},
             {"id": "loc_conservation", "name_ar": "ورشة الترميم", "description_ar": "ورشة فيها سجل الترميم."},
             {"id": "loc_office", "name_ar": "مكتب الأمينة", "description_ar": "حيث يُراجَع تقرير الفرز."}]
objects = [{"id": "obj_letter", "name_ar": "الرسالة التجارية المؤرخة 1931", "description_ar": "رسالة بخط اليد على ورق قديم، تبرع بها سالم عام 2018."},
           {"id": "obj_pen", "name_ar": "قلم الفرز فوق البنفسجي", "description_ar": "جهاز فرز سريع يشير إلى «حبر حديث» أو لا."}]
orgs = [{"id": "org_museum", "name_ar": "متحف الأثر", "description_ar": "متحف خيالي في مدينة القنطرة."}]

# ---------------------------------------------------------------- facts
c.F("f_letter_flagged", "أشار قلم الفرز الثلاثاء 10:15 إلى رسالة سالم بعبارة «حبر حديث».", "event", ["obj_letter", "obj_pen"], 0, T(1515), "loc_lab")
c.F("f_spec_claimed", "يقول تقرير الأمينة إن القلم دقيق بنسبة 95%، وتعلّق المتحف قبول الهبة بانتظار القرار.", "attribute", ["dalia", "obj_pen"], 0)
c.F("f_donor_denies", "ينكر سالم أنه زوّر الرسالة أو بدّلها.", "attribute", ["salem"], 0)
c.F("f_donor_says", "يقول سالم إن الرسالة إرث عائلي سلّمه للمتحف عام 2018 دون ترميم منه.", "attribute", ["salem", "obj_letter"], 1)
c.F("f_insurance_asked", "سأل سالم المتحف الشهر الماضي عن قيمة الرسالة لقائمة مقتنيات تطلبها شركة تأمين بيته.", "event", ["salem"], 1)
c.F("f_coating_applied", "وضعت رنا عام 2019 طبقة حماية شفافة رقيقة على صفحة الرسالة كاملة.", "event", ["rana", "obj_letter"], 1, None, "loc_conservation")
c.F("f_restoration_log_exists", "تدوّن رنا كل عمل ترميم في سجل مكتوب بتاريخه ومادته.", "state", ["rana"], 1, None, "loc_conservation")
c.F("f_donation_file_exists", "يضم ملف الهبة جرداً عائلياً موثقاً عند كاتب عدل وسجل التبرع عام 2018.", "state", ["obj_letter", "org_museum"], 1, None, "loc_registry")
c.F("f_photo_2018_exists", "صُوّرت الرسالة عام 2018 لدليل المتحف وحُفظت الصورة بتاريخها.", "state", ["obj_letter"], 1, None, "loc_registry")
c.F("f_confirm_available", "يملك المختبر فحصاً تأكيدياً بالمجهر لحبر الرسائل.", "state", ["tarek"], 1, None, "loc_lab")
c.F("f_uv_lamp_available", "يملك المختبر مصباحاً فوق بنفسجي لتصوير الصفحة كلها.", "state", ["tarek"], 1, None, "loc_lab")
c.F("f_pen_manual_exists", "للقلم دليل استعمال يذكر حساسيته ومعدل الإشارات الكاذبة ومحاذير الاستعمال.", "state", ["obj_pen"], 1, None, "loc_lab")
c.F("f_stats_exist", "يحتفظ المختبر بسجل رسائل فُرزت العام الماضي ثم أُكدت نتيجتها بالفحص التأكيدي.", "state", ["tarek"], 1, None, "loc_lab")
c.F("f_controls_possible", "يستطيع الفني تجربة القلم على أوراق قديمة معلومة الأصل، مطلية وغير مطلية.", "state", ["tarek"], 1, None, "loc_lab")
c.F("f_ppv", "نحو سبعين بالمئة من الرسائل التي يشير إليها القلم في هذا المتحف سليمة، وأقل من ثلثها مزور؛ فالإشارة وحدها ترفع الترجيح ولا تحسمه.", "relation", ["obj_pen"], 2, T(1740), "loc_office", ["KO-RS-06-010", "KO-FC-04-011", "KO-FC-04-009"])
c.F("f_old_letter", "الرسالة قديمة الحبر والأصل، وسجلاتها الموثقة تسبق وجود القلم والشبهة بسنوات، فلا دليل على صنعها حديثاً.", "relation", ["obj_letter"], 3, T(3000), "loc_lab", ["KO-FC-04-019", "KO-RS-05-004"])
c.F("f_coating_cause", "سبب الإشارة هو طبقة الحماية التي وُضعت عند الترميم، فالقلم يتفاعل مع السطح كله لا مع حبر الخطوط.", "relation", ["obj_letter", "obj_pen", "rana"], 3, T(3030), "loc_lab", ["KO-FC-04-019", "KO-RS-06-008"])

c.claims += [
    {"id": "cl_pen_95", "statement_ar": "القلم دقيق بنسبة 95%، فالرسالة التي أشار إليها مزورة بنسبة 95% تقريباً.", "kind": "honest_mistake", "held_by": ["dalia"], "true_fact_id": "f_ppv", "contradicted_by_evidence_ids": ["ev_screening_stats"]},
]
c.timeline += [
    {"id": "te_flag", "description_ar": "الفني يمرّر القلم على الرسالة فيشير إلى «حبر حديث».", "time": T(1515), "location_id": "loc_lab", "actor_ids": ["tarek"], "fact_ids": ["f_letter_flagged"], "motivated_by_ar": "فرز روتيني للهبات الجديدة قبل التسجيل"},
    {"id": "te_report", "description_ar": "الأمينة تكتب تقريرها وتعلّق قبول الهبة.", "time": T(1740), "location_id": "loc_office", "actor_ids": ["dalia"], "fact_ids": ["f_spec_claimed"], "motivated_by_ar": "تريد حماية المجموعة من التزوير"},
    {"id": "te_confirm", "description_ar": "الفني يجري الفحص التأكيدي بالمجهر.", "time": T(3000), "location_id": "loc_lab", "actor_ids": ["tarek"], "fact_ids": ["f_old_letter"], "motivated_by_ar": "طُلب منه تأكيد نتيجة الفرز قبل أي قرار"},
    {"id": "te_uv", "description_ar": "الفني يصوّر الصفحة كلها تحت المصباح فوق البنفسجي.", "time": T(3030), "location_id": "loc_lab", "actor_ids": ["tarek"], "fact_ids": ["f_coating_cause"], "motivated_by_ar": "يريد معرفة هل الإشارة على الخطوط أم على السطح كله"},
    {"id": "te_controls", "description_ar": "الفني يجرّب القلم على أوراق معلومة الأصل.", "time": T(3180), "location_id": "loc_lab", "actor_ids": ["tarek"], "fact_ids": ["f_controls_possible"], "motivated_by_ar": "يريد معايرة سلوك القلم على أوراق معروفة"},
]

# ---------------------------------------------------------------- evidence
c.V("ev_curator_report", "تقرير الأمينة", "documentary",
    "متحف الأثر — تقرير داخلي — الثلاثاء 14:00\nالموضوع: رسالة الواهب سالم المنصوري (مؤرخة 1931)\nالنتيجة: أشار قلم الفرز إلى «حبر حديث».\nالتقدير: دليل الجهاز ينص على دقة 95%، أي أن الرسالة مزورة بنسبة تقارب 95%. أوصي بتعليق قبول الهبة ومراجعة بقية ما قدّمه الواهب.",
    None, ["f_spec_claimed", "f_donor_denies"], "moderate",
    "تقدير كتبته الأمينة بعد قراءة رقم واحد من الدليل؛ لم تُجرَ فيه مقارنة بعدد الرسائل المزورة فعلاً، وتفسّر «الدقة» تفسيراً واحداً.",
    "اقرأ تقرير الأمينة", red=True, loc="loc_office")
c.V("ev_pen_log", "سجل قراءة قلم الفرز", "digital",
    "مختبر الفحص — سجل الجهاز — الثلاثاء 10:15\nالجهاز: قلم الفرز فوق البنفسجي\nالعينة: رسالة الواهب س. المنصوري (الصفحة الأولى)\nالنتيجة: إشارة «حبر حديث» (إيجابي)\nعدد القراءات: 1\nملاحظة الفني: لم يُجرَ فحص تأكيدي.",
    None, ["f_letter_flagged"], "strong",
    "قراءة واحدة بأداة فرز؛ تقول إن الجهاز أشار ولا تقول لماذا أشار.",
    "اقرأ سجل قراءة قلم الفرز", loc="loc_lab")
c.V("ev_pen_manual", "دليل استعمال القلم", "documentary",
    "دليل قلم الفرز فوق البنفسجي — فصل الأداء والمحاذير\nالحساسية: يشير إلى 95 من كل 100 رسالة كُتبت بحبر حديث.\nالإشارات الكاذبة: يشير إلى 5 من كل 100 رسالة سليمة.\nمحاذير: قد تُعطي الأسطح المغطاة بطبقات حماية بوليمرية إشارة كاذبة؛ تُفحص الصفحة كلها لا الخطوط وحدها؛ النتيجة الإيجابية تُؤكَّد بفحص آخر قبل أي حكم.",
    "f_pen_manual_exists", ["f_pen_manual_exists", "f_ppv"], "strong",
    "وثيقة صانع الجهاز عن أداء الجهاز في ظروف الاختبار؛ لا تذكر كم رسالة مزورة تمرّ في هذا المتحف.",
    "اطلب دليل استعمال القلم", loc="loc_lab")
c.V("ev_screening_stats", "سجل الفرز والتأكيد للعام الماضي", "documentary",
    "مختبر الفحص — سجل سنوي — رسائل فُحصت بالقلم ثم بالفحص التأكيدي\nعدد الرسائل: 1000\nثبت بالتأكيد أنها مزورة: 20 رسالة (أشار القلم إلى 19 منها)\nثبت أنها سليمة: 980 رسالة (أشار القلم إلى 49 منها)",
    "f_stats_exist", ["f_stats_exist", "f_ppv"], "strong",
    "سجل مختبر عن سنة واحدة وعن الرسائل التي مرت به؛ تتغير النسبة إذا تغيّر ما يصل إلى المتحف.",
    "اطلب سجل الفرز والتأكيد للعام الماضي", ko="KO-FC-04-011", loc="loc_lab")
c.V("ev_ink_confirm", "نتيجة الفحص التأكيدي بالمجهر", "lab_result",
    "مختبر الفحص — فحص تأكيدي بالمجهر — الأربعاء 11:00 — رسالة الواهب سالم المنصوري\nحواف الخطوط: بنية اللون مع هالة باهتة حولها وتغلغل في ألياف الورق.\nالألياف حول الخطوط: متأكسدة بنمط يوافق حبراً عمره عقود.\nلا أثر لحبر صنعي حديث على أي سطر.",
    "f_confirm_available", ["f_old_letter"], "strong",
    "فحص تأكيدي لثلاثة مواضع من الصفحة الأولى لا كل أسطرها؛ يقدّر العمر بمدى لا بسنة محددة، ويُقرأ مع باقي الأدلة.",
    "اطلب نتيجة الفحص التأكيدي بالمجهر", ko="KO-FC-04-019", loc="loc_lab")
c.V("ev_pen_controls", "اختبار القلم على أوراق معلومة الأصل", "lab_result",
    "مختبر الفحص — اختبار ضبط — الأربعاء 14:00 — أوراق تجارية معلومة الأصل من الثلاثينيات\nعشر أوراق غير مطلية: أشار القلم إلى ورقة واحدة\nعشر أوراق مطلية بطبقة الحماية نفسها التي يستعملها المتحف: أشار القلم إلى تسع منها\nجرى الاختبار مرتين بتبديل الفني، والنتيجة نفسها.",
    "f_controls_possible", ["f_coating_cause"], "strong",
    "عشرون ورقة فقط، وليست الرسالة نفسها؛ تبيّن سلوك القلم على الأوراق المطلية ولا تثبت أن رسالة سالم طُليت.",
    "اطلب اختبار القلم على أوراق معلومة الأصل", ko="KO-RS-06-008", loc="loc_lab")
c.V("ev_restoration_log", "سجل الترميم للرسالة", "documentary",
    "متحف الأثر — سجل الترميم — شهر 5/2019\nالقطعة: رسالة تجارية مؤرخة 1931 (من مجموعة الهبات 2018)\nالعمل: تنظيف سطحي، ثم طبقة حماية شفافة رقيقة من بوليمر «ب-3» على الصفحة كاملة.\nالمرمّمة: رنا الحسيني",
    "f_restoration_log_exists", ["f_coating_applied"], "strong",
    "سجل كتبته المرمّمة نفسها في حينه؛ يثبت ما أُضيف وتاريخه، ولا يثبت أن الطبقة هي سبب إشارة القلم.",
    "اطلب سجل الترميم", loc="loc_conservation")
c.V("ev_uv_pattern", "صورة الصفحة تحت المصباح فوق البنفسجي", "observation",
    "مختبر الفحص — تصوير الصفحة الأولى كاملة — الأربعاء 11:30\nيظهر توهج منتظم على الخطوط وعلى الهوامش البيضاء معاً، وتنتهي حدود التوهج عند أطراف الصفحة.\nقياس الشدة: الخطوط 82 والهوامش 80 (وحدات الجهاز)؛ ورقة غير مطلية للمقارنة: الخطوط 40 والهوامش 5.",
    "f_uv_lamp_available", ["f_coating_cause"], "strong",
    "صورة واحدة وفي ظرف إضاءة واحد؛ تبيّن أين يتوهج السطح لا ما المادة التي سبّبت التوهج.",
    "اطلب صورة الصفحة تحت المصباح فوق البنفسجي", loc="loc_lab")
c.V("ev_donation_file", "ملف الهبة والجرد العائلي", "documentary",
    "متحف الأثر — ملف الهبة 2018/14\nجرد عائلي موثق عند كاتب عدل عام 1987: «رسالة تجارية مؤرخة 1931، أربعة عشر سطراً، بخط التاجر المنصوري الجد».\nسجل التبرع: سُلّمت الرسالة 12 آذار 2018، وفي الخانة: «حالة جيدة، بلا ترميم من الواهب».",
    "f_donation_file_exists", ["f_donation_file_exists", "f_old_letter"], "strong",
    "يثبت أن رسالة بهذا الوصف سُجّلت قبل وجود القلم بسنوات؛ ولا يثبت وحده أن الرسالة التي بين أيدينا هي نفسها دون صورة تقابلها.",
    "اطلب ملف الهبة والجرد العائلي", loc="loc_registry")
c.V("ev_catalogue_photo", "صورة الفهرسة عام 2018", "digital",
    "متحف الأثر — فهرس الصور — الملف 2018/14 — التاريخ المسجّل 12/3/2018\nالصورة: الصفحة الأولى كاملة. يظهر تمزق في الزاوية العليا اليسرى، وبقعة حبر قرب السطر الرابع، وطيّتان أفقيتان.\nمقارنة الفني بالأصل اليوم: التمزق والبقعة والطيّتان في المواضع نفسها.",
    "f_photo_2018_exists", ["f_photo_2018_exists", "f_old_letter"], "strong",
    "صورة بتاريخ مسجّل في نظام المتحف؛ تثبت اتصال الرسالة الحالية بالسجل ولا تثبت عمر الحبر وحدها.",
    "اطلب صورة الفهرسة عام 2018", loc="loc_registry")
c.V("ev_insurance_inquiry", "رسالة الواهب إلى مكتب الاستعلامات", "documentary",
    "بريد من س. المنصوري إلى المتحف — قبل شهر\n«أرجو إفادتي بالقيمة التقديرية لرسالة جدي المحفوظة عندكم، لأن شركة التأمين على بيتي طلبت قائمة بمقتنياتي وقيمتها.»\nرد المكتب: القيمة التقديرية غير معلنة؛ يمكن إصدار خطاب بإيداع الرسالة.",
    "f_insurance_asked", ["f_insurance_asked"], "weak",
    "سؤال عن قيمة لا يدل على نية؛ والتفسير المعلن مكتوب في البريد نفسه ويمكن التحقق منه، ولم يُطلب من الواهب بيع الرسالة.",
    "اطلب بريد الواهب عن قيمة الرسالة", red=True, loc="loc_office")
c.V("ev_donor_statement", "إفادة سالم (ملخص)", "testimonial",
    "ملخص إفادة سالم المنصوري:\n«الرسالة من صندوق جدي، سلّمتها للمتحف عام 2018 كما هي. لم أكتب فيها ولم أرمّمها، وسؤالي عن قيمتها كان لقائمة التأمين.»",
    "f_donor_says", ["f_donor_says"], "weak",
    "إفادة صاحب الشأن عن نفسه؛ تُقاس بملفات المتحف لا بنبرة صاحبها.",
    "دوّن إفادة سالم", loc="loc_office")
c.V("ev_conservator_statement", "إفادة رنا (ملخص)", "testimonial",
    "ملخص إفادة رنا الحسيني:\n«رمّمت الرسالة عام 2019 وطليت صفحتها بطبقة حماية شفافة، ودوّنت ذلك. لم يطلب أحد مني أن أخبر مختبر الفرز، ولم أتوقع أن يتأثر القلم بها.»",
    "f_coating_applied", ["f_coating_applied"], "moderate",
    "شهادة عن عملها هي، تؤيدها سجلات الورشة؛ ولا تعني أن الطبقة سبب إشارة القلم.",
    "دوّن إفادة رنا", loc="loc_office")

# ---------------------------------------------------------------- inferences
GK = lambda t: P("general_knowledge", t)
c.I("i_flag_base", [E_("ev_screening_stats"), E_("ev_pen_manual")], "fact", "f_ppv", "establishes", "strong",
    "في ألف رسالة 20 مزورة و980 سليمة: القلم يصيب 19 من العشرين ويخطئ في 49 من الباقي، فتكون الإشارات 68 إشارة لا يزيد المزور فيها على 19؛ أي أن نسبة الترجيح (95 إلى 5 = 19 مرة) ترفع الشك ولا تحسمه لأن المعدل الأساسي منخفض.", ["KO-RS-06-010", "KO-FC-04-011", "KO-FC-04-009"])
c.I("i_a_old", [E_("ev_ink_confirm"), GK("الفحص التأكيدي بالمجهر يتقدم على الفرز السريع عند التعارض")], "fact", "f_old_letter", "establishes", "strong",
    "الفحص التأكيدي هو الأقوى هنا، وقد وجد تغلغل الحبر وتأكسد الألياف على نمط عمره عقود ولم يجد حبراً صنعياً.", ["KO-FC-04-019"])
c.I("i_b_old", [E_("ev_donation_file"), E_("ev_catalogue_photo")], "fact", "f_old_letter", "establishes", "strong",
    "جرد موثق عام 1987 وصورة فهرسة عام 2018 بالتمزق والبقعة والطيّتين نفسها؛ مصدران من المتحف والعائلة سبقا القلم والشبهة بسنوات ولا يعتمد أحدهما على المجهر.", ["KO-RS-05-004", "KO-FC-04-024"])
c.I("i_a_coat", [E_("ev_pen_controls"), E_("ev_restoration_log")], "fact", "f_coating_cause", "establishes", "strong",
    "القلم يشير إلى تسع من عشر أوراق مطلية وإلى واحدة من عشر غير مطلية، والسجل يقول إن الرسالة طُليت عام 2019؛ فإشارته عليها متوقعة دون حبر حديث.", ["KO-RS-06-008", "KO-FC-04-019"])
c.I("i_b_coat", [E_("ev_pen_manual"), E_("ev_uv_pattern")], "fact", "f_coating_cause", "establishes", "strong",
    "الدليل يحذّر من الأسطح المغطاة ببوليمر، والتوهج متساوٍ على الخطوط والهوامش البيضاء ويقف عند حدود الصفحة، ولو كان حبراً حديثاً لتركز على الخطوط وحدها.", ["KO-RS-06-001", "KO-RS-06-003"])
c.I("i_support_coating", [Fa("f_old_letter"), Fa("f_coating_cause")], "hypothesis", "h_coating", "supports", "strong",
    "حبر قديم مؤكد، وسبب مادي للإشارة موثق عند الترميم؛ فالتفسير يجمع الأدلة كلها دون افتراض تزوير.", ["KO-RS-06-007"])
c.I("i_rule_forged", [Fa("f_old_letter"), Fa("f_coating_cause")], "hypothesis", "h_forged", "rules_out", "strong",
    "التزوير الحديث يتطلب حبراً حديثاً، وقد نفاه الفحص التأكيدي والسجلات القديمة، وللإشارة سبب بديل موثق.", ["KO-RS-06-008"])
c.I("i_rule_95", [Fa("f_old_letter"), Fa("f_coating_cause")], "hypothesis", "h_95", "rules_out", "strong",
    "إذا كانت الرسالة قديمة وللإشارة تفسير مادي، فالقول إنها مزورة بنسبة 95% باطل، وهذا ما يؤكده أيضاً جدول التكرارات.", ["KO-RS-06-010", "KO-FC-04-010"])
c.I("i_rule_95_b", [Fa("f_ppv")], "hypothesis", "h_95", "rules_out", "suggestive",
    "حتى قبل أي فحص آخر، تظهر أرقام المختبر أن الإشارة الواحدة لا ترفع الاحتمال إلى 95%.", ["KO-RS-06-010"])
c.I("i_rule_pen", [Fa("f_old_letter"), Fa("f_coating_cause")], "hypothesis", "h_pen", "rules_out", "strong",
    "القلم أشار بسلوك متوقع على سطح مطلي، وأشار إلى سطح غير مطلي في واحدة من عشر فقط؛ فهو يعمل كما صُمّم وليس معطوباً.", ["KO-RS-06-003", "KO-RS-06-008"])
c.I("i_cl_pen95", [Fa("f_ppv")], "claim", "cl_pen_95", "contradicts_claim", "strong",
    "دقة الجهاز ليست احتمال أن تكون الرسالة المؤشَّر عليها مزورة؛ فذلك يتوقف على نسبة المزور بين ما يصل إلى المتحف.", ["KO-FC-04-010", "KO-RS-06-010"])

c.ck += [
    {"character_id": "dalia", "knows": [], "hides": [], "believes": [{"claim_id": "cl_pen_95", "stance": "sincere"}]},
    {"character_id": "salem", "knows": [K("f_donor_says"), K("f_insurance_asked")], "hides": [], "believes": []},
    {"character_id": "rana", "knows": [K("f_coating_applied"), K("f_restoration_log_exists", "professional")], "hides": [], "believes": []},
    {"character_id": "hala", "knows": [K("f_donation_file_exists", "professional"), K("f_photo_2018_exists", "professional")], "hides": [], "believes": []},
    {"character_id": "tarek", "knows": [K("f_confirm_available", "professional"), K("f_uv_lamp_available", "professional"), K("f_pen_manual_exists", "professional"), K("f_stats_exist", "professional"), K("f_controls_possible", "professional")], "hides": [], "believes": []},
]
hyps = [
    {"id": "h_forged", "statement_ar": "الرسالة مزورة حديثاً، ولذلك أشار القلم، والواهب هو المسؤول.", "is_true": False, "plausibility_at_start": "high", "suspect_id": "salem"},
    {"id": "h_95", "statement_ar": "دقة القلم 95%، فالرسالة المؤشَّر عليها مزورة بنسبة 95% ويكفي هذا للحكم.", "is_true": False, "plausibility_at_start": "medium"},
    {"id": "h_coating", "statement_ar": "الرسالة أصلية قديمة، وإشارة القلم سببها طبقة حماية وُضعت عند ترميمها عام 2019 دون أن يقصد أحد التضليل.", "is_true": True, "plausibility_at_start": "low", "suspect_id": "rana"},
    {"id": "h_pen", "statement_ar": "القلم معطوب ويشير إلى كل رسالة تقريباً، فلا قيمة لنتائجه.", "is_true": False, "plausibility_at_start": "medium"},
]
mis = [
    {"id": "rh_95", "points_to_hypothesis_id": "h_forged", "planted_via_ar": "تقرير الأمينة يحوّل دقة الجهاز 95% إلى احتمال تزوير 95%.", "evidence_ids": ["ev_curator_report", "ev_pen_log"],
     "refuted_by_inference_ids": ["i_flag_base", "i_cl_pen95", "i_rule_forged"],
     "fairness_note_ar": "الدليل نفسه يذكر معدل الإشارات الكاذبة، وسجل المختبر يتيح العدّ، والفحص التأكيدي متاح للاعب قبل الحكم."},
    {"id": "rh_insurance", "points_to_hypothesis_id": "h_forged", "planted_via_ar": "الواهب سأل عن قيمة الرسالة قبل شهر من الإشارة، فيبدو أن له غرضاً مالياً.", "evidence_ids": ["ev_insurance_inquiry"],
     "refuted_by_inference_ids": ["i_rule_forged", "i_a_old", "i_b_old"],
     "fairness_note_ar": "السبب مكتوب في البريد وفي إفادة الواهب، والسجلات القديمة تنفي صنع الرسالة حديثاً قبل أي سؤال عن القيمة."},
    {"id": "rh_pen", "points_to_hypothesis_id": "h_pen", "planted_via_ar": "قلم يشير إلى رسالة قديمة فيبدو معطوباً.", "evidence_ids": ["ev_pen_log"],
     "refuted_by_inference_ids": ["i_rule_pen", "i_a_coat", "i_b_coat"],
     "fairness_note_ar": "اختبار الضبط يُظهر أن القلم يعمل بسلوك متوقع، ودليله يحذّر من الأسطح المطلية."},
]
los = [
    {"id": "lo_source", "statement_ar": "يصنّف التقرير والإفادات أقوالاً، والسجل وفحص المختبر سجلات أصلية، ودليل الصانع وثيقة منشورة.", "skill_ko_ref": "KO-RS-05-001", "observable_behaviors_ar": ["يصنّف الأقوال", "يميّز الوثيقة المنشورة"], "evidence_sources": ["evidence_board"]},
    {"id": "lo_conflict", "statement_ar": "يرتّب أحداث الفرز والتأكيد على الخط الزمني ويلاحظ أن التأكيد جاء بعد الفرز لا قبله.", "skill_ko_ref": "KO-RS-05-005", "observable_behaviors_ar": ["يضع الأدلة في أزمنتها"], "evidence_sources": ["timeline_task", "action_log"]},
    {"id": "lo_links", "statement_ar": "يميّز الاختبار التمهيدي من التأكيدي ويدمج المعدل الأساسي في تقدير ما تعنيه الإشارة.", "skill_ko_ref": "KO-RS-06-010", "observable_behaviors_ar": ["يربط الدليل بالفرضية", "يبني جدول التكرارات ذهنياً"], "evidence_sources": ["evidence_board", "final_justification"]},
    {"id": "lo_calib", "statement_ar": "يصوغ نسبة الترجيح بحدودها دون أن يخلط بين الدقة واحتمال الفرضية.", "skill_ko_ref": "KO-FC-04-009", "observable_behaviors_ar": ["يختار ثقة معقولة", "يذكر حدوداً"], "evidence_sources": ["final_justification"]},
    {"id": "lo_revise", "statement_ar": "يراجع رأيه الأول حين تظهر نتيجة التأكيد.", "skill_ko_ref": "KO-RS-06-009", "observable_behaviors_ar": ["يغيّر فرضيته الرائدة بدليل"], "evidence_sources": ["hypothesis_ledger"]},
    {"id": "lo_elim", "statement_ar": "يبحث عن الاختبار المكذِّب ويستبعد ما تنقضه الأدلة.", "skill_ko_ref": "KO-RS-06-008", "observable_behaviors_ar": ["يضيف فرضيات", "يستبعد بدليل"], "evidence_sources": ["hypothesis_ledger"]},
    {"id": "lo_just", "statement_ar": "يكتب حجة تربط الأدلة بالاستنتاج وتذكر حدود الفرز.", "skill_ko_ref": "KO-RS-06-007", "observable_behaviors_ar": ["يكتب حجة معللة"], "evidence_sources": ["final_justification"]},
]
topics = [
    {"id": "t_claim95", "label_ar": "دقة القلم والحكم", "example_questions_ar": ["ماذا تعني دقة 95% في رأيك؟", "على ماذا بنيتِ تقريرك؟"], "fact_ids": [], "claim_ids": ["cl_pen_95"]},
    {"id": "t_origin", "label_ar": "أصل الرسالة", "example_questions_ar": ["من أين جاءت الرسالة؟", "هل رمّمتها؟"], "fact_ids": ["f_donor_says"]},
    {"id": "t_value", "label_ar": "سؤال القيمة", "example_questions_ar": ["لماذا سألت عن قيمتها؟"], "fact_ids": ["f_insurance_asked"]},
    {"id": "t_restore", "label_ar": "ترميم الرسالة", "example_questions_ar": ["ماذا فعلتِ بالرسالة؟", "هل دوّنتِ عملك؟"], "fact_ids": ["f_coating_applied", "f_restoration_log_exists"]},
    {"id": "t_registry", "label_ar": "ملفات الهبة", "example_questions_ar": ["ما الذي تحفظونه عن الرسالة؟", "هل صُوّرت وقت التبرع؟"], "fact_ids": ["f_donation_file_exists", "f_photo_2018_exists"]},
    {"id": "t_methods", "label_ar": "الفحوص المتاحة", "example_questions_ar": ["ما الفحوص عندكم غير القلم؟", "هل يمكن تصوير الصفحة كلها؟"], "fact_ids": ["f_confirm_available", "f_uv_lamp_available"]},
    {"id": "t_pen", "label_ar": "القلم وأرقامه", "example_questions_ar": ["ماذا يقول دليل القلم؟", "هل عندكم أرقام من العام الماضي؟"], "fact_ids": ["f_pen_manual_exists", "f_stats_exist"]},
    {"id": "t_controls", "label_ar": "اختبار الضبط", "example_questions_ar": ["هل تستطيع تجربة القلم على أوراق معلومة؟"], "fact_ids": ["f_controls_possible"]},
]
he = lambda e: {"has_evidence": e}
al = {"always": True}
c.H("hg1", 1, "metacognitive", "حين تسمع «دقيق بنسبة 95%» اسأل: دقيق في أي شيء؟ وكم من الرسائل في هذا المتحف مزورة أصلاً؟", al, None, 0.02)
c.H("hg2", 2, "focus_area", "تخيّل ألف رسالة: كم منها مزور؟ وكم يُشير القلم إليه من المزور ومن السليم؟ ثم قارن الأعداد.", he("ev_pen_log"), None, 0.04)
c.H("hg3", 3, "pointer", "الإشارة الأولى تستحق فحصاً ثانياً مختلف الأسلوب؛ اسأل فني المختبر ماذا يملك.", he("ev_pen_log"), None, 0.08)
c.H("hc1", 1, "metacognitive", "هل توهّج الصفحة على الخطوط وحدها يشبه توهجها على الصفحة كلها؟ وماذا يعني الفرق؟", he("ev_pen_manual"), "i_b_coat", 0.02)
c.H("hc2", 2, "pointer", "اقرأ في دليل القلم فقرة المحاذير، ثم انظر أين يقف التوهج في صورة المصباح.", he("ev_pen_manual"), "i_b_coat", 0.06)
c.H("hc3", 3, "partial_reveal", "التوهج يشمل الهوامش البيضاء، وهذا يوافق مادة تغطي السطح كله لا حبراً على الخطوط.", he("ev_uv_pattern"), "i_b_coat", 0.1)
c.H("ho1", 1, "metacognitive", "ما الدليل الذي يسبق القلم بسنوات ولا يعتمد على أي جهاز فحص؟", he("ev_pen_log"), "i_b_old", 0.02)
c.H("ho2", 2, "pointer", "اسأل أمينة السجل ماذا حُفظ عن الرسالة يوم التبرع وقبله.", he("ev_pen_log"), "i_b_old", 0.06)

steps = [
    (1, "ابدأ بالعدّ لا بالنسبة: في ألف رسالة قلّة قليلة مزورة، فتكثر الإشارات الكاذبة حتى تزيد على الصحيحة، وإشارة واحدة لا تكفي للحكم.", ["ev_screening_stats", "ev_pen_manual"], "i_flag_base"),
    (2, "الفحص التأكيدي بالمجهر يبني عمر الحبر من أثره في الألياف، ويقدَّم على الفرز السريع عند التعارض.", ["ev_ink_confirm"], "i_a_old"),
    (3, "طريق مستقل لعمر الرسالة: جرد موثق يسبق الشبهة بعقود، وصورة فهرسة ما زال فيها التمزق والبقعة في موضعهما.", ["ev_donation_file", "ev_catalogue_photo"], "i_b_old"),
    (4, "ثم يُفسَّر سبب الإشارة: القلم يستجيب لسطح مطلي بالبوليمر على أوراق مجرَّبة، والسجل يقول إن الصفحة طُليت قبل خمس سنوات.", ["ev_pen_controls", "ev_restoration_log"], "i_a_coat"),
    (5, "الطريق المستقل لسبب الإشارة: تحذير الصانع من الأسطح المغطاة، وتوهج منتظم يشمل الهوامش البيضاء ويقف عند حدود الصفحة.", ["ev_pen_manual", "ev_uv_pattern"], "i_b_coat"),
    (6, "فتسقط رواية التزوير، وتسقط معها فكرة أن القلم معطوب، ويبقى القلم أداة فرز تحتاج إلى متابعة.", ["ev_pen_controls", "ev_uv_pattern", "ev_ink_confirm"], "i_rule_pen"),
]
ending = {"steps": steps,
    "alt": ["يكفي طريق المختبر: الفحص التأكيدي واختبار الضبط وسجل الترميم، من غير ملفات السجل ولا صورة المصباح.",
            "ويكفي طريق الملفات: الجرد والصورة القديمة وتحذير الصانع وصورة المصباح، من غير مجهر الحبر؛ والأقوى أن يتفق الطريقان."],
    "limits": ["اختبار الضبط شمل عشرين ورقة، وليست الرسالة منها، فهو يبيّن سلوك القلم ولا يختبر الرسالة نفسها بشكل مباشر.",
               "الفحص التأكيدي أخذ ثلاثة مواضع من الصفحة الأولى، ويقدّر العمر بمدى لا بسنة.",
               "نسبة المزور بين الرسائل (2%) مأخوذة من سنة واحدة في هذا المختبر، وقد تتغير في سنة أخرى.",
               "لا نعرف لماذا لم يُبلَّغ مختبر الفرز بأن الرسالة رُمّمت وطُليت؛ والحل ودّي: يُسجَّل الطلاء في ملف كل قطعة."],
    "notes": ["الدقة ليست الاحتمال: قلم يلتقط 95 من كل 100 مزور ويخطئ في 5 من كل 100 سليم يعطي نسبة ترجيح مقدارها 19 (أي يضرب الأرجحية السابقة في 19). لكن إذا كان المزور رسالتين في كل ألف، فالأرجحية السابقة ضئيلة، ولذلك تبقى الإشارة المنفردة بعيدة عن الحسم.",
              "نسبة الترجيح (likelihood ratio) مقياس لقوة الدليل، وهي غير مقياس الارتباط في الجداول المسمى odds ratio؛ فلا يُخلط المصطلحان.",
              "الاختبار التمهيدي يُنتقي ليلتقط الجميع ويقبل إشارات كاذبة؛ والتأكيدي يُنتقى ليحسم. قرار يترتب عليه اتهام لا يُبنى على التمهيدي وحده.",
              "حين تسمع «إيجابي» فاسأل عمّا يمكن أن يسبب إيجابية بريئة: طبقة، رطوبة، تلوث. وجدنا هنا الجواب في سجل ترميم مكتوب.",
              "لا اتهام لأحد: المرمّمة عملت وفق أصول مهنتها، والواهب سلّم ما ورثه. وإصلاح الضرر أن تُرفع حالة التعليق وتُوثّق الطبقة في ملف الرسالة.",
              "بطاقة الأصل: القضية أصلية من ATHAR، وبنيتها من نمط «الاختبار الدقيق بنسبة 95%» في مكتبة تصميم القضايا؛ لا قلم ولا جهاز حقيقيان فيها."]}
meta = {"title_ar": "القلم الذي أشار إلى رسالة قديمة", "title_en": "The Pen That Flagged an Old Letter", "age_band": "16-18", "locale": "ar", "dialogue_register": "msa", "estimated_minutes": 30, "difficulty": 3,
        "content_flags": ["fraud", "science_lab"], "authors": ["فريق أثر التحريري (مسودة بمساعدة الذكاء الاصطناعي، لم تُراجَع بشرياً بعد)"],
        "knowledge_object_refs": ["KO-RS-06-010", "KO-RS-06-008", "KO-RS-06-001", "KO-RS-06-003", "KO-RS-06-021", "KO-RS-06-009", "KO-RS-05-001", "KO-RS-05-004", "KO-RS-05-005", "KO-RS-06-007", "KO-FC-04-009", "KO-FC-04-010", "KO-FC-04-011", "KO-FC-04-019", "KO-FC-04-024"]}
premise = {"hook_ar": "جهاز فرز «دقيق بنسبة 95%» أشار إلى رسالة عمرها تسعون عاماً بأنها «حبر حديث». هل يعني هذا أنها مزورة بنسبة 95%؟",
           "player_role_ar": "أنت مراجع مستقل في متحف الأثر، طُلب منك رأي معلّل في هبة موقوفة قبل أن يتخذ المتحف قراراً بحق الواهب.",
           "setting_ar": "متحف الأثر في مدينة القنطرة، من الاثنين إلى الأربعاء. توقيت المتحف هو ساعة المختبر والمكتب.",
           "public_fact_ids": ["f_letter_flagged", "f_spec_claimed", "f_donor_denies"],
           "assumed_general_knowledge_ar": ["الاختبار السريع قد يعطي إشارات كاذبة", "عدد الأمثلة المزورة بين كل الأمثلة يغيّر معنى الإشارة", "ما يترتب عليه اتهام يحتاج إلى فحص أقوى من الفرز"]}
solution = {"culprit_ids": ["rana"], "summary_ar": "الرسالة أصلية وليست مزورة. أشار القلم إلى طبقة حماية وضعتها المرمّمة عام 2019 دون سوء قصد، والقلم يستجيب لهذه الطبقة، ودقته المعلنة لا تعني أن الرسالة المؤشَّر عليها مزورة بنسبة 95%.",
            "key_fact_ids": ["f_old_letter", "f_coating_cause"]}
ref = "لا دليل على أن الرسالة مزورة. القلم أداة فرز تلتقط خمساً وتسعين بالمئة من المزور وتشير خطأً إلى خمس بالمئة من السليم، ولأن المزور نادر في هذا المتحف (نحو عشرين من ألف) تكثر الإشارات الكاذبة حتى تزيد على ضعف الصحيحة. الفحص التأكيدي وجد حبراً قديماً، والجرد الموثق وصورة الفهرسة تسبقان القلم بسنوات، واختبار الضبط وسجل الترميم ودليل الصانع وصورة المصباح تفسّر الإشارة بطبقة حماية وُضعت قبل خمس سنوات. حدود الاستنتاج: اختبار الضبط على أوراق أخرى، والمجهر على مواضع قليلة، ونسبة المزور من سنة واحدة."
ui = {
    "clock": {"epoch_hhmm": "09:00", "zone_label_ar": "ساعة المتحف (الاثنين 09:00 = البداية)"},
    "cover": {"title_ar": "القلم الذي أشار إلى رسالة قديمة", "tagline_ar": "جهاز «دقيق بنسبة 95%» قال كلمته… فهل تكفي؟", "kicker_ar": "الملف الثالث والعشرون · العدّ قبل الحكم", "glyph": "◈", "accent": "cyan"},
    "cold_open_ar": ["الأربعاء، متحف الأثر.", "رسالة تجارية عمرها تسعون عاماً أشار إليها قلم الفرز بعبارة «حبر حديث». الأمينة واثقة: الجهاز دقيق بنسبة 95%، والهبة موقوفة.",
                     "الواهب يقول إنها إرث جده. وقبل أن تتخذ موقفاً: كم رسالة مزورة تصل إلى هذا المتحف أصلاً؟ وما الفحص الذي يأتي بعد الفرز؟"],
    "limit_menu": [
        {"id": "l_controls_small", "label_ar": "اختبار الضبط شمل عشرين ورقة ليست الرسالة منها، فيبيّن سلوك القلم ولا يختبر الرسالة مباشرة"},
        {"id": "l_screen_tool", "label_ar": "القلم أداة فرز تعمل كما صُمّمت، وإشارته تستوجب فحصاً تأكيدياً لا حكماً"},
        {"id": "l_base_rate_year", "label_ar": "نسبة المزور بين الرسائل مأخوذة من سنة واحدة وقد تتغير"},
        {"id": "l_invalid_95", "label_ar": "دقة 95% تعني أن الرسالة المؤشَّر عليها مزورة بنسبة 95%"},
        {"id": "l_invalid_insure", "label_ar": "سؤال الواهب عن القيمة يدل على نية تزوير"},
        {"id": "l_invalid_useless", "label_ar": "القلم معطوب ولا يصلح لأي شيء"}],
    "mind_change_menu": [
        {"id": "m_not_coated", "label_ar": "ظهور أن الرسالة لم تُطلَ أصلاً عام 2019"},
        {"id": "m_ink_modern", "label_ar": "ظهور حبر صنعي حديث تحت الطبقة في فحص تأكيدي آخر"},
        {"id": "m_stats_other", "label_ar": "ظهور أن سجل الفرز لا يمثل الرسائل التي تصل إلى المتحف"},
        {"id": "m_popular", "label_ar": "كثرة من يرددون أن الجهاز دقيق"}],
    "transfer": {
        "id": "tr_gate", "title_ar": "اختبار نقل المهارة: كاشف بوابة المعرض",
        "scenario_ar": "كاشف عند بوابة معرض خيالي يطلق إنذاراً. أمامك وثيقتان من واقعة لا علاقة لها بالقضية.",
        "documents": [
            {"title_ar": "ورقة مواصفات الكاشف", "body_ar": "يطلق إنذاراً لـ95 من كل 100 زائر يحمل غرضاً معدنياً محظوراً، ولـ5 من كل 100 زائر لا يحمل شيئاً."},
            {"title_ar": "إحصاء البوابة", "body_ar": "بين كل 1000 زائر يوم أمس، حمل 10 زوار فقط غرضاً محظوراً، وأُطلق الإنذار 59 مرة بحسب عدّاد البوابة."}],
        "prompt_ar": "اختر الخطوات التي تصلح لتقدير ما يعنيه إنذار الكاشف لزائر معيّن (يمكنك اختيار أكثر من خطوة).",
        "options": [
            {"id": "o1", "text_ar": "بناء جدول بأعداد الزوار: كم حمل غرضاً وكم أُنذر من الحاملين ومن غير الحاملين"},
            {"id": "o2", "text_ar": "ملاحظة أن أكثر الإنذارات هنا ستكون كاذبة لأن الحاملين قلة"},
            {"id": "o3", "text_ar": "طلب فحص يدوي مؤكد قبل أي إجراء بحق الزائر"},
            {"id": "o4", "text_ar": "عدّ الإنذارات الصحيحة والكاذبة قبل تفسير النسبة 95%"},
            {"id": "o5", "text_ar": "اعتبار الإنذار يعني أن الزائر يحمل غرضاً محظوراً بنسبة 95%"},
            {"id": "o6", "text_ar": "تجاهل الكاشف كله لأنه يخطئ في 5%"},
            {"id": "o7", "text_ar": "منع الزائر من الدخول فوراً دون أي فحص آخر"}],
        "free_text_prompt_ar": "اكتب في ثلاثة أسطر كيف تقرّر نسبة الترجيح بأن زائراً أُطلق الإنذار عليه يحمل غرضاً محظوراً بالفعل.",
    },
    "skills": [{"skill_id": "KO-RS-06-010", "track": "D"}, {"skill_id": "KO-FC-04-009", "track": "E"}, {"skill_id": "KO-FC-04-011", "track": "E"}, {"skill_id": "KO-FC-04-019", "track": "E"}, {"skill_id": "KO-RS-06-008", "track": "D"}],
    "stage_hooks_ar": {"briefing": "«دقيق بنسبة 95%» عبارة تُغري بالتصديق… فاعدّ قبل أن تصدّق.", "investigating": "الإشارة الأولى باب، لا حكم. أي فحص يأتي بعدها؟", "review": "قبل أن تغلق الملف: ماذا يبيّن اختبار الضبط وماذا لا يبيّن؟", "resolved": "أُغلق الملف. رُفعت الشبهة عن الرسالة، وبقي سؤال عن جهاز آخر يعطي إنذاراً."},
    "character_glyphs": {"dalia": "د", "salem": "س", "rana": "ر", "hala": "هـ", "tarek": "ط"},
}
sc = {
    "case_id": CID,
    "accepted_conclusions": {
        "h_coating": {"grade": 1, "note_ar": "استنتاج متسق مع الفحص التأكيدي والسجلات ويتطلب ذكر حدوده."},
        "h_forged": {"grade": 0, "note_ar": "يبني الاتهام على إشارة فرز واحدة ويتجاهل المعدل الأساسي والفحص التأكيدي والسجلات القديمة."},
        "h_95": {"grade": 0, "note_ar": "يخلط بين دقة الجهاز واحتمال صحة الفرضية بعد الإشارة."},
        "h_pen": {"grade": 0, "note_ar": "القلم يعمل كما صُمّم وسلوكه على الأسطح المطلية متوقع."}},
    "confidence_band": {"h_coating": [65, 90], "h_forged": [0, 15], "h_95": [0, 10], "h_pen": [0, 15]},
    "source_key": {"ev_curator_report": "claim", "ev_pen_log": "primary_record", "ev_pen_manual": "public_document", "ev_screening_stats": "primary_record", "ev_ink_confirm": "primary_record",
                   "ev_pen_controls": "primary_record", "ev_restoration_log": "primary_record", "ev_uv_pattern": "primary_record", "ev_donation_file": "primary_record", "ev_catalogue_photo": "primary_record",
                   "ev_insurance_inquiry": "claim", "ev_donor_statement": "claim", "ev_conservator_statement": "claim"},
    "link_key": {
        "h_coating": {"ev_pen_manual": "supports", "ev_ink_confirm": "supports", "ev_pen_controls": "supports", "ev_restoration_log": "supports", "ev_uv_pattern": "supports",
                      "ev_donation_file": "supports", "ev_catalogue_photo": "supports", "ev_screening_stats": "supports", "ev_conservator_statement": "supports"},
        "h_forged": {"ev_curator_report": "supports", "ev_pen_log": "supports", "ev_insurance_inquiry": "supports", "ev_ink_confirm": "weakens", "ev_donation_file": "weakens", "ev_catalogue_photo": "weakens", "ev_uv_pattern": "weakens", "ev_pen_controls": "weakens"},
        "h_95": {"ev_curator_report": "supports", "ev_screening_stats": "weakens", "ev_ink_confirm": "weakens", "ev_pen_controls": "weakens"},
        "h_pen": {"ev_pen_log": "supports", "ev_pen_controls": "weakens", "ev_uv_pattern": "weakens", "ev_pen_manual": "weakens"},
    },
    "required_limits": ["l_controls_small", "l_screen_tool"], "valid_mind_changers": ["m_not_coated", "m_ink_modern", "m_stats_other"],
    "invalid_limits": ["l_invalid_95", "l_invalid_insure", "l_invalid_useless"],
    "decisive_evidence": ["ev_ink_confirm", "ev_pen_controls", "ev_restoration_log", "ev_pen_manual", "ev_uv_pattern", "ev_donation_file", "ev_catalogue_photo"],
    "lab_requirement": None,
    "timeline_requirement": [{"evidence_id": "ev_pen_log", "utc_minute": 1515, "tol": 20}, {"evidence_id": "ev_curator_report", "utc_minute": 1740, "tol": 20},
                             {"evidence_id": "ev_ink_confirm", "utc_minute": 3000, "tol": 20}, {"evidence_id": "ev_uv_pattern", "utc_minute": 3030, "tol": 20}, {"evidence_id": "ev_pen_controls", "utc_minute": 3180, "tol": 20}],
    "refuted_hypotheses": ["h_forged", "h_95", "h_pen"],
    "criteria_map": {"c_source": "source_typing", "c_conflict": "conflict_resolution", "c_links": "hypothesis_links", "c_uncertainty": "uncertainty", "c_revision": "revision", "c_elimination": "elimination", "c_justification": "justification_human"},
    "transfer_key": {"valid": ["o1", "o2", "o3", "o4"], "invalid": ["o5", "o6", "o7"]},
    "caps": {"no_citations_max": 45, "no_conflict_resolution_max": 65},
}
c.build(OUT, meta=meta, premise=premise, solution=solution, locations=locations, objects=objects, orgs=orgs, hyps=hyps, mis=mis, los=los, reference_answer=ref, ending=ending, ui=ui, sc=sc, topics=topics)
