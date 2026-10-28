#!/usr/bin/env python3
# Case c025 «ظرف النادي: لا يكفي بعد» — archetype ARC-06 «لا يكفي بعد», age band 16-18, difficulty 3.
# Teaches: the right answer can be «the evidence does not yet decide», provided you can SAY what it does establish (a time window; exactly two people with
# access; no record telling them apart), name the evidence that WOULD decide, and keep your confidence calibrated; also that «not enough» is not «innocent».
# DEVIATIONS from ARC-06 (honest list): (1) the archetype wants the «insufficient» option available in EVERY case of the season and correct in this one only,
# so players cannot find it by pattern. The engine offers one hypothesis list per case, so here «insufficient» is a hypothesis of this case alone; the
# anti-pattern protection is therefore weaker than the archetype intends and should be handled at platform level (e.g. add a neutral «غير كافٍ» row to
# every case) if the owner wants it; (2) culprit_ids lists BOTH suspects because the file entails only the pair (one of the two took it) and deliberately
# does not decide between them - there is no hidden «real» culprit in this file, so nothing is withheld from the player; (3) the virtual lab #1
# (latent print with blind verification) is not built: the print result is an evidence item whose limit is «inconclusive», with labs: [].
# The four «sufficient evidence to blame X» hypotheses are refuted in the sense «the available evidence does not suffice», using the key facts only.
# Nothing here is violent; the missing item is a small sum of club money. All names and records are fictional.
# Calendar (fictional): minute 0 = Tuesday 15:00. Tue 15:40 = 40; 15:42 = 42; 15:55 = 55; 16:05 = 65; 16:30 = 90; 17:00 = 120; 17:10 = 130; Wed 08:00 = 1020; Wed 10:00 = 1140.
# Usage: gen_c025.py OUT_DIR
import sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
from _lib_c022_c025 import *

OUT = sys.argv[1]
CID = "c025_club_envelope"
c = Case(CID)

# ---------------------------------------------------------------- characters
c.ch("nada", "نداء السيد", "victim", "أمينة صندوق نادي الرصد المدرسي",
     "دقيقة وغاضبة قليلاً لأن المسؤولية عليها، وتتمسك بالأرقام والتوقيعات. تحاول ألا تتهم أحداً من أصدقائها بلا دليل.",
     ["أن يعود المبلغ", "ألا تضيع صداقة النادي"],
     [L("nd_greet", "greeting", "كان كل شيء مسجلاً، ثم اختفى الظرف."),
      L("nd_count", "reveal", "عددنا الظرف أنا والأستاذ زيد في الثالثة وأربعين دقيقة، وصوّرته على الرف الثاني بهاتفي ووقّعنا ورقة الجرد.", ["f_count_done", "f_photo_taken"]),
      L("nd_found", "reveal", "اكتشفت غيابه في الخامسة وعشر دقائق حين فتحت الخزانة لأدفع ثمن أدوات القياس.", ["f_discovered"]),
      L("nd_rumor", "reveal", "وصلتني رسالة محوّلة في مجموعة النادي تقول إن سامي هو من أخذه، ولا أعرف من كتبها أول مرة.", ["f_rumor_seen"]),
      L("nd_unknown", "deflect_unknown", "لا أعرف أكثر."),
      L("nd_off", "deflect_offtopic", "اسألني عن الظرف والجرد."),
      L("nd_bye", "farewell", "أريد حلاً عادلاً.")])
c.ch("zaid", "زيد الحلبي", "authority", "معلم الفيزياء ومشرف النادي",
     "ودود ومنشغل، يوقّع بسرعة ويثق بطلابه. يحرص على ألا يُظلم طالب بلا دليل.",
     ["حماية النادي", "ألا يُتهم طالب ظلماً"],
     [L("zd_greet", "greeting", "أتمنى أن تنتهي القضية بلا ظلم لأحد."),
      L("zd_class", "reveal", "غادرت المختبر الخامسة إلا عشر دقائق لأدرّس حصة في المبنى الآخر حتى الخامسة، ووقّع طلابي ورقة الحضور.", ["f_zaid_class"]),
      L("zd_trip", "reveal", "رسوم رحلة النادي تُجمع هذا الأسبوع، ولم يدفعها بعد خمسة أعضاء.", ["f_trip_fees"]),
      L("zd_unknown", "deflect_unknown", "لا أعرف أكثر."),
      L("zd_off", "deflect_offtopic", "اسألني عن النادي."),
      L("zd_bye", "farewell", "لنعاملهم كطلاب لا كمتهمين.")])
c.ch("sami", "سامي القاسم", "suspect", "عضو في نادي الرصد، في الصف الحادي عشر",
     "متوتر وكثير الكلام حين يشعر بالاتهام، ويحاول أن يشرح كل شيء. توتره ليس دليلاً على شيء.",
     ["ألا يُنسب إليه ما لم يفعله", "أن يعرف من أخذ الظرف"],
     [L("sm_greet", "greeting", "سمعت الإشاعة، وهي ليست صحيحة."),
      L("sm_says", "reveal", "فتحت الخزانة بمفتاح الفني من الرابعة وخمس دقائق إلى الرابعة وعشرين لآخذ شريط القياس من الرف الأول، ولم أنظر إلى الرف الثاني.", ["f_sami_says"]),
      L("sm_unknown", "deflect_unknown", "لا أعرف."),
      L("sm_off", "deflect_offtopic", "اسألني عن شريط القياس."),
      L("sm_bye", "farewell", "افحصوا كل شيء.")])
c.ch("rami", "رامي الحايك", "suspect", "عضو في نادي الرصد، في الصف الحادي عشر",
     "هادئ ومتحفظ، يجيب بإيجاز وبنبرة ثابتة. هدوؤه ليس دليلاً على شيء.",
     ["أن ينتهي الأمر بسرعة", "ألا يُحرج أمام النادي"],
     [L("rm_greet", "greeting", "أجيب بما فعلته."),
      L("rm_says", "reveal", "فتحت الخزانة بمفتاح الفني من الرابعة والنصف إلى الخامسة إلا عشراً لآخذ الحامل الثلاثي من الرف الأول، ولم أنظر إلى الرف الثاني.", ["f_rami_says"],),
      L("rm_unknown", "deflect_unknown", "لا أعرف."),
      L("rm_off", "deflect_offtopic", "اسألني عن الحامل."),
      L("rm_bye", "farewell", "كل شيء مكتوب.")])
c.ch("amer", "عامر الحداد", "expert", "فني المختبر المدرسي",
     "عملي وصريح، يذكر ما سجّله وما لا يستطيع قوله، ويقول إن الأثر الجزئي لا يكفي وحده. لا يعرف نيات أحد.",
     ["أن تُقرأ السجلات بحدودها"],
     [L("am_greet", "greeting", "أحفظ المفاتيح وأفحص ما يُطلب مني."),
      L("am_keys", "reveal", "مفتاح خزانة النادي يخرج من درجي بتوقيع في ورقة المفاتيح، وأستطيع فحص القفل بحثاً عن خدوش أو فتح بالقوة.", ["f_key_sheet_exists", "f_lock_inspected"]),
      L("am_print", "reveal", "وجدت أثر بصمة جزئياً على حافة الرف الثاني وأرسلته للمقارنة، وكاميرا الممر كانت متوقفة للصيانة ذلك العصر.", ["f_print_found", "f_camera_maint"]),
      L("am_unknown", "deflect_unknown", "هذا خارج ما سجّلته."),
      L("am_off", "deflect_offtopic", "اسألني عن المفاتيح والقفل."),
      L("am_bye", "farewell", "اقرأ كل سجل بحدوده.")])
c.ch("ghassan", "غسان المراكشي", "witness", "عامل تنظيف المختبرات",
     "منظم ومباشر، يقرأ من ورقته ولا يخمّن. يفرّق بين ما رآه وما افترضه.",
     ["أن تبقى ورقته سليمة"],
     [L("gh_greet", "greeting", "أقرأ من ورقة جولتي."),
      L("gh_round", "reveal", "مررت على المختبر الساعة الخامسة، والخزانة كانت مغلقة، والرف الثاني من خلف الزجاج لم يكن فيه ظرف.", ["f_cleaner_round"]),
      L("gh_register", "reveal", "كل من يدخل المختبر يوقّع في سجل الباب، ولا يُدخَل المختبر دون توقيع.", ["f_lab_register"]),
      L("gh_unknown", "deflect_unknown", "لا أعرف."),
      L("gh_off", "deflect_offtopic", "اسألني عن جولتي."),
      L("gh_bye", "farewell", "ورقتي أمامكم.")])

locations = [{"id": "loc_lab", "name_ar": "مختبر النادي", "description_ar": "مختبر فيه خزانة للنادي ذات رفين وقفل بمفتاح."},
             {"id": "loc_tech", "name_ar": "غرفة الفني", "description_ar": "فيها درج المفاتيح وورقة التوقيع."},
             {"id": "loc_corridor", "name_ar": "ممر المختبرات", "description_ar": "ممر فيه كاميرا كانت متوقفة للصيانة."}]
objects = [{"id": "obj_envelope", "name_ar": "ظرف تمويل النادي", "description_ar": "ظرف أبيض بختم النادي فيه 200 وحدة نقدية لشراء أدوات قياس المطر."},
           {"id": "obj_cabinet", "name_ar": "خزانة النادي", "description_ar": "خزانة ذات رفين وقفل بمفتاح واحد وآخر احتياطي مختوم."}]
orgs = [{"id": "org_club", "name_ar": "نادي الرصد المدرسي", "description_ar": "نادٍ علمي يقيس المطر والرياح على سطح المدرسة."}]

# ---------------------------------------------------------------- facts
c.F("f_envelope_gone", "فُقد ظرف تمويل النادي (200 وحدة) من الرف الثاني في خزانة النادي عصر الثلاثاء.", "event", ["obj_envelope", "nada"], 0)
c.F("f_rumor_names", "تداول أعضاء النادي رسالة تنسب أخذ الظرف إلى سامي، ولا يعرف أحد مصدرها الأول.", "attribute", ["sami"], 0)
c.F("f_both_deny", "ينكر سامي ورامي أنهما أخذا الظرف.", "attribute", ["sami", "rami"], 0)
c.F("f_count_done", "عدّت نداء الظرف مع الأستاذ زيد الثلاثاء 15:40 ووقّعا ورقة جرد.", "event", ["nada", "zaid"], 1, T(40), "loc_lab")
c.F("f_photo_taken", "صوّرت نداء الظرف على الرف الثاني بهاتفها قرابة 15:42.", "event", ["nada", "obj_envelope"], 1, T(42), "loc_lab")
c.F("f_discovered", "اكتشفت نداء غياب الظرف نحو 17:10 بعد أن فتحت الخزانة.", "event", ["nada"], 1, T(130), "loc_lab")
c.F("f_rumor_seen", "وصلت نداء رسالة محوّلة في مجموعة النادي تسمّي سامي، ولا تعرف كاتبها الأول.", "event", ["nada", "sami"], 1, T(160))
c.F("f_zaid_class", "غادر الأستاذ زيد المختبر 15:50 وأعطى مفتاحه للفني، ودرّس حصة في مبنى آخر حتى 17:00.", "event", ["zaid"], 1, T(50, "exact", 120))
c.F("f_trip_fees", "لم يدفع خمسة أعضاء رسوم رحلة النادي حتى هذا الأسبوع.", "state", ["org_club"], 1)
c.F("f_sami_says", "يقول سامي إنه فتح الخزانة من 16:05 إلى 16:20 لأخذ شريط القياس من الرف الأول ولم ينظر إلى الرف الثاني.", "attribute", ["sami"], 1, T(65, "exact", 80), "loc_lab")
c.F("f_rami_says", "يقول رامي إنه فتح الخزانة من 16:30 إلى 16:50 لأخذ الحامل الثلاثي من الرف الأول ولم ينظر إلى الرف الثاني.", "attribute", ["rami"], 1, T(90, "exact", 110), "loc_lab")
c.F("f_key_sheet_exists", "يدوّن الفني في ورقة المفاتيح من يستلم مفتاح الخزانة ومتى يعيده.", "state", ["amer"], 1, None, "loc_tech")
c.F("f_lock_inspected", "يستطيع الفني فحص قفل الخزانة بحثاً عن آثار فتح بالقوة.", "state", ["amer", "obj_cabinet"], 1, None, "loc_tech")
c.F("f_print_found", "وجد الفني أثر بصمة جزئياً على حافة الرف الثاني وأرسله للمقارنة.", "event", ["amer", "obj_cabinet"], 1, T(1140), "loc_lab")
c.F("f_camera_maint", "كانت كاميرا الممر متوقفة للصيانة عصر الثلاثاء.", "state", ["loc_corridor"], 1, T(55, "exact", 110), "loc_corridor")
c.F("f_cleaner_round", "مرّ عامل التنظيف الساعة 17:00 فوجد الخزانة مغلقة والرف الثاني بلا ظرف.", "event", ["ghassan", "obj_cabinet"], 1, T(120), "loc_lab")
c.F("f_lab_register", "يوقّع كل داخل إلى المختبر في سجل الباب.", "state", ["loc_lab"], 1, None, "loc_lab")
c.F("f_window", "كان الظرف في الخزانة عند 15:42 وغاب قبل 17:00، فاختفاؤه وقع داخل هذه الفترة والخزانة مغلقة بقفل سليم.", "relation", ["obj_envelope"], 3, T(42, "exact", 120), "loc_lab", ["KO-RS-05-005", "KO-RS-05-004"])
c.F("f_two_access", "لم يفتح الخزانة بمفتاحها في تلك الفترة إلا سامي ورامي، فلا غريب ولا كسر، والدائرة تضيق إلى اثنين.", "relation", ["sami", "rami", "obj_cabinet"], 3, T(65, "exact", 110), "loc_lab", ["KO-RS-05-004", "KO-RS-06-008"])
c.F("f_no_discriminator", "لا يوجد في ما بين أيدينا ما يفرّق بين سامي ورامي: لا تسجيل للممر، وبصمة جزئية غير حاسمة، ولا شاهد، وروايتاهما متماثلتان.", "absence", ["sami", "rami"], 3, T(1140), "loc_lab", ["KO-FC-04-012", "KO-RS-05-013", "KO-RS-05-010"])

c.claims += [
    {"id": "cl_rumor_sami", "statement_ar": "سامي هو من أخذ الظرف، فالجميع يقول ذلك.", "kind": "rumour", "held_by": ["nada"], "true_fact_id": "f_no_discriminator", "contradicted_by_evidence_ids": [], "unresolved_by_design": True},
]
c.timeline += [
    {"id": "te_count", "description_ar": "نداء وزيد يعدّان الظرف ويوقّعان ورقة الجرد.", "time": T(40), "location_id": "loc_lab", "actor_ids": ["nada", "zaid"], "fact_ids": ["f_count_done"], "motivated_by_ar": "جرد دوري لمال النادي"},
    {"id": "te_photo", "description_ar": "نداء تصوّر الظرف على الرف الثاني.", "time": T(42), "location_id": "loc_lab", "actor_ids": ["nada"], "fact_ids": ["f_photo_taken"], "motivated_by_ar": "أرادت توثيق المبلغ قبل المغادرة"},
    {"id": "te_class", "description_ar": "زيد يغادر ويدرّس حصة في المبنى الآخر.", "time": T(50, "exact", 120), "location_id": "loc_corridor", "actor_ids": ["zaid"], "fact_ids": ["f_zaid_class"], "motivated_by_ar": "حصته المقررة"},
    {"id": "te_camera", "description_ar": "كاميرا الممر متوقفة للصيانة.", "time": T(55, "exact", 110), "location_id": "loc_corridor", "actor_ids": [], "fact_ids": ["f_camera_maint"]},
    {"id": "te_sami", "description_ar": "سامي يفتح الخزانة بمفتاح الفني.", "time": T(65, "exact", 80), "location_id": "loc_lab", "actor_ids": ["sami"], "fact_ids": ["f_sami_says"], "motivated_by_ar": "أراد شريط القياس لتجربة الغد"},
    {"id": "te_rami", "description_ar": "رامي يفتح الخزانة بمفتاح الفني.", "time": T(90, "exact", 110), "location_id": "loc_lab", "actor_ids": ["rami"], "fact_ids": ["f_rami_says"], "motivated_by_ar": "أراد الحامل الثلاثي لتجربة الغد"},
    {"id": "te_cleaner", "description_ar": "غسان يمرّ على المختبر في جولته.", "time": T(120), "location_id": "loc_lab", "actor_ids": ["ghassan"], "fact_ids": ["f_cleaner_round"], "motivated_by_ar": "جولة التنظيف اليومية"},
    {"id": "te_report", "description_ar": "نداء تكتشف غياب الظرف وتبلّغ.", "time": T(130), "location_id": "loc_lab", "actor_ids": ["nada"], "fact_ids": ["f_discovered"], "motivated_by_ar": "أرادت دفع ثمن أدوات القياس"},
]

# ---------------------------------------------------------------- evidence
c.V("ev_count_sheet", "ورقة جرد ظرف النادي", "documentary",
    "نادي الرصد — ورقة جرد — الثلاثاء 15:40\nظرف التمويل: 200 وحدة (عشر أوراق من فئة 20)\nالعدّ: نداء السيد · التحقق: الأستاذ زيد الحلبي\nالتوقيعان بخطيهما. بعد الجرد أُقفلت الخزانة وسُلّم مفتاحها إلى الفني الساعة 15:50.",
    "f_count_done", ["f_count_done", "f_window"], "strong",
    "ورقة موقّعة من شخصين وقت الجرد؛ تثبت وجود المبلغ ذلك الوقت ولا تثبت ما حدث بعده.",
    "اطلب ورقة جرد ظرف النادي", loc="loc_lab")
c.V("ev_missing_report", "بلاغ نداء عن فقد الظرف", "documentary",
    "نادي الرصد — بلاغ — الثلاثاء 17:10\nنداء السيد: «أخذت المفتاح من الفني 17:05 وفتحت الخزانة فلم أجد الظرف على الرف الثاني. القفل سليم والخزانة كانت مغلقة.»",
    "f_discovered", ["f_discovered", "f_window", "f_envelope_gone"], "moderate",
    "بلاغ صاحبة الصندوق بوقت كتبته بنفسها؛ يحدد لحظة الاكتشاف لا لحظة الأخذ.",
    "اطلب بلاغ نداء", loc="loc_lab")
c.V("ev_phone_photo", "صورة الظرف من هاتف نداء", "digital",
    "هاتف نداء السيد — بيانات صورة — الثلاثاء 15:42\nالرف الثاني من خزانة النادي: ظرف أبيض بختم النادي، وبجانبه علبة أقلام.\nساعة الهاتف مضبوطة تلقائياً على الشبكة.",
    "f_photo_taken", ["f_photo_taken", "f_window"], "strong",
    "صورة بوقت جهاز مضبوط؛ تثبت وجود الظرف في موضعه وقتها، وقد يدّعي أحد أنها مأخوذة قبلها بدقائق.",
    "اطلب صورة الظرف من هاتف نداء", ko="KO-FC-04-024", loc="loc_lab")
c.V("ev_cleaner_round", "ورقة جولة التنظيف", "documentary",
    "مدرسة القنطرة — ورقة جولة التنظيف — مختبر النادي — الثلاثاء 17:00\nالخزانة مغلقة. من خلف الزجاج الجانبي: الرف الثاني فيه علبة أقلام فقط، ولا ظرف.\nالتوقيع: غسان",
    "f_cleaner_round", ["f_cleaner_round", "f_window"], "strong",
    "ملاحظة عامل من خلف الزجاج لا فتح للخزانة؛ يثبت الغياب وقتها ولا يقول متى حدث.",
    "اطلب ورقة جولة التنظيف", loc="loc_lab")
c.V("ev_key_log", "ورقة مفاتيح الفني", "documentary",
    "غرفة الفني — ورقة تسليم مفتاح خزانة النادي — الثلاثاء\n15:50 — الأستاذ زيد: إيداع المفتاح\n16:05 — سامي القاسم: استلام · 16:20 إعادة\n16:30 — رامي الحايك: استلام · 16:50 إعادة\n17:05 — نداء السيد: استلام\nلا توقيع آخر في هذه الفترة. المفتاح الاحتياطي الوحيد في ظرف مختوم عند الفني.",
    "f_key_sheet_exists", ["f_key_sheet_exists", "f_two_access"], "strong",
    "ورقة كتبها الفني بتوقيع المستلمين؛ تثبت من حمل المفتاح ولا تثبت ما فعله به أو من فتح بقصد الأخذ.",
    "اطلب ورقة مفاتيح الفني", loc="loc_tech")
c.V("ev_lock_check", "فحص قفل الخزانة", "observation",
    "غرفة الفني — محضر فحص — الأربعاء 08:00\nقفل خزانة النادي: لا خدوش، ولا أثر لأداة، ولا تلاعب. المفتاح الاحتياطي في ظرفه المختوم لم يُفتح.\nالخلاصة: فُتحت الخزانة بمفتاحها الأصلي فقط.",
    "f_lock_inspected", ["f_lock_inspected", "f_two_access"], "strong",
    "فحص بصري لفني واحد؛ لا يستبعد نسخة مفتاح مصنوعة سراً، لكن لا دليل عليها.",
    "اطلب فحص قفل الخزانة", loc="loc_tech")
c.V("ev_lab_register", "سجل دخول المختبر", "documentary",
    "مختبر النادي — سجل الباب — الثلاثاء\n15:35 نداء · 15:35 زيد · 15:50 زيد (خروج)\n16:00 سامي (دخول) · 16:25 سامي (خروج)\n16:28 رامي (دخول) · 16:55 رامي (خروج)\n17:00 غسان · 17:03 نداء · 17:05 زيد (عودة)\nلا توقيع غير هذا.",
    "f_lab_register", ["f_lab_register", "f_two_access"], "strong",
    "سجل توقيعات يدوي على الباب؛ يثبت من وقّع لا من دخل دون توقيع.",
    "اطلب سجل دخول المختبر", loc="loc_lab")
c.V("ev_class_timetable", "ورقة حضور حصة الأستاذ زيد", "documentary",
    "مدرسة القنطرة — ورقة حضور حصة الكيمياء — المبنى الآخر — الثلاثاء 15:50–17:00\nالأستاذ زيد: توقيع حضور 16:00 بخطه، أربعة وعشرون طالباً.",
    "f_zaid_class", ["f_zaid_class", "f_two_access"], "strong",
    "ورقة موقّعة من طرف مستقل عن النادي؛ تضع المشرف في مكان آخر وقتها ولا تتحدث عن غيره.",
    "اطلب ورقة حضور حصة الأستاذ زيد", loc="loc_corridor")
c.V("ev_partial_print", "تقرير مقارنة أثر البصمة", "lab_result",
    "مختبر المدرسة — مقارنة أثر كامن — الأربعاء 10:00\nالأثر: حافة الرف الثاني، ست نقاط تمييز فقط.\nالمقارنة: لا يُستبعد منه سامي ولا رامي ولا نداء. الأثر لا يكفي لتحديد صاحبه.\nالنتيجة: غير حاسمة.",
    "f_print_found", ["f_print_found", "f_no_discriminator"], "moderate",
    "أثر جزئي وعدد قليل من النقاط؛ ونتيجته «غير حاسمة» مشروعة، وقد يعود إلى أي يد لمست الرف في أي يوم.",
    "اطلب تقرير مقارنة أثر البصمة", ko="KO-FC-04-012", loc="loc_lab")
c.V("ev_camera_gap", "سجل صيانة كاميرا الممر", "digital",
    "ممر المختبرات — سجل الكاميرا — الثلاثاء\n15:55 — توقف التسجيل (تحديث مجدول)\n16:50 — استئناف التسجيل\nلا ملفات للفترة بين الوقتين.",
    "f_camera_maint", ["f_camera_maint", "f_no_discriminator"], "strong",
    "سجل نظام لا يدلّ على من مرّ بالممر؛ غياب التسجيل ليس دليلاً على شيء بذاته.",
    "اطلب سجل صيانة كاميرا الممر", ko="KO-RS-05-013", loc="loc_corridor")
c.V("ev_sami_statement", "إفادة سامي (ملخص)", "testimonial",
    "ملخص إفادة سامي القاسم:\n«فتحت الخزانة من 16:05 إلى 16:20 لأخذ شريط القياس من الرف الأول، ولم أنظر إلى الرف الثاني. لم آخذ الظرف.»",
    "f_sami_says", ["f_sami_says", "f_no_discriminator"], "weak",
    "إفادة صاحب الشأن عن نفسه تتفق مع ورقة المفاتيح في الوقت، ولا يمكن التحقق من نظره إلى الرف.",
    "دوّن إفادة سامي", loc="loc_lab")
c.V("ev_rami_statement", "إفادة رامي (ملخص)", "testimonial",
    "ملخص إفادة رامي الحايك:\n«فتحت الخزانة من 16:30 إلى 16:50 لأخذ الحامل الثلاثي من الرف الأول، ولم أنظر إلى الرف الثاني. لم آخذ الظرف.»",
    "f_rami_says", ["f_rami_says", "f_no_discriminator"], "weak",
    "إفادة صاحب الشأن عن نفسه تتفق مع ورقة المفاتيح في الوقت، ولا يمكن التحقق من نظره إلى الرف.",
    "دوّن إفادة رامي", loc="loc_lab")
c.V("ev_group_rumor", "رسالة محوّلة في مجموعة النادي", "digital",
    "لقطة شاشة — مجموعة نادي الرصد — الثلاثاء 17:40\nرسالة محوّلة (أربع مرات): «سمعت أن سامي هو من أخذ الظرف».\nلا يظهر اسم كاتب الرسالة الأول.",
    "f_rumor_seen", ["f_rumor_seen", "f_rumor_names"], "weak",
    "رسالة بلا مصدر أول؛ تكرار تحويلها لا يزيد وزنها، ولا نعرف هل بُنيت على رؤية أو على ظن.",
    "اطلب لقطة الرسالة المحوّلة", red=True, loc="loc_lab")
c.V("ev_trip_list", "قائمة رسوم رحلة النادي", "documentary",
    "نادي الرصد — قائمة الرسوم — هذا الأسبوع\nالمطلوب 30 وحدة من كل عضو قبل الخميس.\nلم يدفع: سامي القاسم · رامي الحايك · ثلاثة أعضاء آخرون.",
    "f_trip_fees", ["f_trip_fees"], "weak",
    "حاجة خمسة أعضاء إلى المال لا تخص واحداً منهم؛ ولا تدل على فعل.",
    "اطلب قائمة رسوم رحلة النادي", red=True, loc="loc_lab")

# ---------------------------------------------------------------- inferences
c.I("i_a_window", [E_("ev_count_sheet"), E_("ev_missing_report")], "fact", "f_window", "establishes", "strong",
    "الجرد الموقّع 15:40 يثبت وجود المبلغ، وبلاغ نداء 17:10 يثبت غيابه والقفل سليم؛ فالاختفاء وقع بين الوقتين.", ["KO-RS-05-005"])
c.I("i_b_window", [E_("ev_phone_photo"), E_("ev_cleaner_round")], "fact", "f_window", "establishes", "strong",
    "صورة بوقت مضبوط تضع الظرف على الرف 15:42، وعامل التنظيف يراه غائباً 17:00 من خلف الزجاج؛ مصدران لا يشتركان في كاتب ولا جهاز.", ["KO-RS-05-004", "KO-FC-04-024"])
c.I("i_a_access", [E_("ev_key_log"), E_("ev_lock_check")], "fact", "f_two_access", "establishes", "strong",
    "ورقة الفني تُظهر مفتاحاً واحداً لم يستلمه في الفترة سوى سامي ثم رامي، وفحص القفل ينفي الكسر والنسخة الاحتياطية المختومة.", ["KO-RS-05-004"])
c.I("i_b_access", [E_("ev_lab_register"), E_("ev_class_timetable")], "fact", "f_two_access", "establishes", "strong",
    "سجل الباب لا يضم في الفترة سوى سامي ورامي، وورقة الحصة تضع المشرف خارج المختبر؛ نظامان مستقلان عن ورقة المفاتيح.", ["KO-RS-05-004", "KO-RS-05-005"])
c.I("i_a_nodisc", [E_("ev_partial_print"), E_("ev_camera_gap")], "fact", "f_no_discriminator", "establishes", "strong",
    "الأثر الجزئي لا يستبعد أحداً من الثلاثة، والكاميرا لم تسجّل أصلاً؛ فالغياب هنا غياب تسجيل لا غياب فعل.", ["KO-FC-04-012", "KO-RS-05-013"])
c.I("i_b_nodisc", [E_("ev_sami_statement"), E_("ev_rami_statement")], "fact", "f_no_discriminator", "establishes", "strong",
    "روايتان متماثلتان في الشكل والمضمون، كلتاهما تتفق مع ورقة المفاتيح ولا تجد من يؤيدها أو ينقضها؛ فلا ترجيح بينهما.", ["KO-RS-05-009", "KO-RS-05-010"])
c.I("i_support_insufficient", [Fa("f_window"), Fa("f_two_access"), Fa("f_no_discriminator")], "hypothesis", "h_insufficient", "supports", "strong",
    "الدليل حدّد الفترة وضيّق الدائرة إلى اثنين ولم يفرّق بينهما؛ فالحكم المسؤول هو أن الأدلة لا تكفي بعد، مع تسمية ما يحسم.", ["KO-RS-06-021", "KO-RS-05-010"])
c.I("i_rule_sami", [Fa("f_two_access"), Fa("f_no_discriminator")], "hypothesis", "h_sami", "rules_out", "strong",
    "ما يشير إلى سامي يشير بالقدر نفسه إلى رامي، وما يميّز بينهما غير موجود؛ فلا تكفي الأدلة لتحميله وحده.", ["KO-FC-04-010", "KO-RS-06-008"])
c.I("i_rule_rami", [Fa("f_two_access"), Fa("f_no_discriminator")], "hypothesis", "h_rami", "rules_out", "strong",
    "ترتيب دخوله الأخير في الفترة لا دليل فيه، وما يشير إليه يشير بالقدر نفسه إلى سامي؛ فلا تكفي الأدلة لتحميله وحده.", ["KO-FC-04-010", "KO-RS-06-008"])
c.I("i_rule_outsider", [Fa("f_window"), Fa("f_two_access")], "hypothesis", "h_outsider", "rules_out", "strong",
    "قفل سليم وسجل باب وورقة مفاتيح لا تضم أحداً غير الاثنين؛ والغريب لا يترك أثراً في ثلاثة سجلات مستقلة.", ["KO-RS-06-008"])
c.I("i_rule_never", [Fa("f_window"), Fa("f_two_access")], "hypothesis", "h_never", "rules_out", "strong",
    "الظرف مجرود ومصوّر قبل الفترة وغائب بعدها، فلا يصح أن يقال إنه لم يكن موجوداً.", ["KO-RS-06-008"])

# ---------------------------------------------------------------- character knowledge
c.ck += [
    {"character_id": "nada", "knows": [K("f_count_done"), K("f_photo_taken"), K("f_discovered"), K("f_rumor_seen")], "hides": [], "believes": [{"claim_id": "cl_rumor_sami", "stance": "sincere"}]},
    {"character_id": "zaid", "knows": [K("f_zaid_class"), K("f_trip_fees", "common_knowledge")], "hides": [], "believes": []},
    {"character_id": "sami", "knows": [K("f_sami_says")], "hides": [], "believes": []},
    {"character_id": "rami", "knows": [K("f_rami_says")], "hides": [], "believes": []},
    {"character_id": "amer", "knows": [K("f_key_sheet_exists", "professional"), K("f_lock_inspected", "professional"), K("f_print_found", "professional"), K("f_camera_maint", "professional")], "hides": [], "believes": []},
    {"character_id": "ghassan", "knows": [K("f_cleaner_round"), K("f_lab_register", "professional")], "hides": [], "believes": []},
]
hyps = [
    {"id": "h_sami", "statement_ar": "الأدلة التي بين أيدينا تكفي لتحميل سامي مسؤولية فقد الظرف.", "is_true": False, "plausibility_at_start": "high", "suspect_id": "sami"},
    {"id": "h_rami", "statement_ar": "الأدلة التي بين أيدينا تكفي لتحميل رامي مسؤولية فقد الظرف.", "is_true": False, "plausibility_at_start": "medium", "suspect_id": "rami"},
    {"id": "h_outsider", "statement_ar": "أخذ الظرف شخص من خارج من فتحوا الخزانة.", "is_true": False, "plausibility_at_start": "low"},
    {"id": "h_never", "statement_ar": "لم يكن في الخزانة ظرف أصلاً، وبلاغ نداء خطأ.", "is_true": False, "plausibility_at_start": "low"},
    {"id": "h_insufficient", "statement_ar": "الأدلة الحالية تحدّد الفترة والدائرة ولا تكفي للحكم على أحد؛ والدليل الذي يحسم ما زال غائباً.", "is_true": True, "plausibility_at_start": "low"},
]
mis = [
    {"id": "rh_rumor", "points_to_hypothesis_id": "h_sami", "planted_via_ar": "الجميع يقول إن سامي هو الفاعل، والرسالة حُوّلت أربع مرات.", "evidence_ids": ["ev_group_rumor"],
     "refuted_by_inference_ids": ["i_rule_sami", "i_a_nodisc", "i_b_nodisc"],
     "fairness_note_ar": "الرسالة تظهر بلا مصدر أول ويقرأ اللاعب حدودها في بطاقة الدليل، وسجلات الملف لا تفرّق بين سامي ورامي."},
    {"id": "rh_money", "points_to_hypothesis_id": "h_rami", "planted_via_ar": "رامي وسامي لم يدفعا رسوم الرحلة، فلهما حاجة إلى المال.", "evidence_ids": ["ev_trip_list"],
     "refuted_by_inference_ids": ["i_rule_rami", "i_rule_sami"],
     "fairness_note_ar": "القائمة تضم خمسة أعضاء لم يدفعوا، فالحاجة لا تخص أحداً بعينه."},
    {"id": "rh_order", "points_to_hypothesis_id": "h_rami", "planted_via_ar": "رامي كان آخر من استلم المفتاح قبل الاكتشاف، فهو الأقرب زمنياً.", "evidence_ids": ["ev_key_log", "ev_lab_register"],
     "refuted_by_inference_ids": ["i_rule_rami", "i_a_nodisc"],
     "fairness_note_ar": "الترتيب الزمني لا يقول متى غاب الظرف بين 15:42 و17:00، فقد يكون غاب في أي وقت داخل الفترة."},
]
los = [
    {"id": "lo_source", "statement_ar": "يصنّف الإشاعة والإفادات أقوالاً، والسجلات والأوراق الموقعة سجلات أصلية.", "skill_ko_ref": "KO-RS-05-001", "observable_behaviors_ar": ["يصنّف الإشاعة قولاً بلا مصدر أول", "يعدّ الأوراق الموقعة سجلات"], "evidence_sources": ["evidence_board"]},
    {"id": "lo_conflict", "statement_ar": "يرتّب سجلات الجرد والمفاتيح والباب على خط زمني ويحدد الفترة الممكنة للاختفاء.", "skill_ko_ref": "KO-RS-05-005", "observable_behaviors_ar": ["يضع الأدلة في أزمنتها"], "evidence_sources": ["timeline_task", "action_log"]},
    {"id": "lo_links", "statement_ar": "يربط الدليل بالفرضية باتجاه صحيح ويدرك أن ما يشير إلى اثنين بالقدر نفسه لا يرجّح أحدهما.", "skill_ko_ref": "KO-RS-06-001", "observable_behaviors_ar": ["يربط الدليل بالفرضية", "يميز ما يفرّق مما لا يفرّق"], "evidence_sources": ["evidence_board", "final_justification"]},
    {"id": "lo_calib", "statement_ar": "يعبّر عن «غير كافٍ» بثقة معايَرة، ويسمّي الدليل الذي سيحسم.", "skill_ko_ref": "KO-RS-05-010", "observable_behaviors_ar": ["يختار ثقة معقولة", "يسمّي الدليل الناقص"], "evidence_sources": ["final_justification"]},
    {"id": "lo_revise", "statement_ar": "يراجع ميله الأول إلى اتهام سامي حين تتساوى الدلائل.", "skill_ko_ref": "KO-RS-06-009", "observable_behaviors_ar": ["يغيّر فرضيته الرائدة بدليل"], "evidence_sources": ["hypothesis_ledger"]},
    {"id": "lo_elim", "statement_ar": "يستبعد الغريب وانعدام الظرف بالسجلات، ويستبعد كفاية الأدلة لاتهام أي من الاثنين.", "skill_ko_ref": "KO-RS-06-008", "observable_behaviors_ar": ["يضيف فرضيات", "يستبعد بدليل"], "evidence_sources": ["hypothesis_ledger"]},
    {"id": "lo_just", "statement_ar": "يكتب حجة تقول ما أُثبت وما لم يُثبت وما الذي سيحسم، دون الخلط بين غير كافٍ وبريء.", "skill_ko_ref": "KO-RS-06-021", "observable_behaviors_ar": ["يكتب حجة معللة"], "evidence_sources": ["final_justification"]},
]
topics = [
    {"id": "t_count", "label_ar": "جرد الظرف وصورته", "example_questions_ar": ["متى جرد الظرف؟", "هل صوّرتِه؟"], "fact_ids": ["f_count_done", "f_photo_taken"]},
    {"id": "t_found", "label_ar": "اكتشاف الغياب", "example_questions_ar": ["متى اكتشفتِ أنه مفقود؟"], "fact_ids": ["f_discovered"]},
    {"id": "t_rumor", "label_ar": "الرسالة المحوّلة", "example_questions_ar": ["ما الرسالة التي وصلتك؟", "ماذا يقول الناس؟"], "fact_ids": ["f_rumor_seen"], "claim_ids": ["cl_rumor_sami"]},
    {"id": "t_class", "label_ar": "حصتي وعودتي", "example_questions_ar": ["أين كنتَ عصر الثلاثاء؟"], "fact_ids": ["f_zaid_class"]},
    {"id": "t_trip", "label_ar": "رسوم الرحلة", "example_questions_ar": ["من لم يدفع رسوم الرحلة؟"], "fact_ids": ["f_trip_fees"]},
    {"id": "t_sami", "label_ar": "ما فعله سامي في المختبر", "example_questions_ar": ["لماذا فتحتَ الخزانة؟", "ماذا أخذت؟"], "fact_ids": ["f_sami_says"]},
    {"id": "t_rami", "label_ar": "ما فعله رامي في المختبر", "example_questions_ar": ["لماذا فتحتَ الخزانة؟", "ماذا أخذت؟"], "fact_ids": ["f_rami_says"]},
    {"id": "t_keys", "label_ar": "المفاتيح والقفل", "example_questions_ar": ["كيف يخرج المفتاح؟", "هل يمكن فحص القفل؟"], "fact_ids": ["f_key_sheet_exists", "f_lock_inspected"]},
    {"id": "t_print", "label_ar": "الأثر والكاميرا", "example_questions_ar": ["هل وجدتَ أثراً؟", "ماذا عن كاميرا الممر؟"], "fact_ids": ["f_print_found", "f_camera_maint"]},
    {"id": "t_round", "label_ar": "جولة التنظيف", "example_questions_ar": ["ماذا رأيتَ في المختبر؟"], "fact_ids": ["f_cleaner_round"]},
    {"id": "t_register", "label_ar": "سجل الباب", "example_questions_ar": ["هل يوقّع الداخلون؟"], "fact_ids": ["f_lab_register"]},
]
he = lambda e: {"has_evidence": e}
al = {"always": True}
c.H("hg1", 1, "metacognitive", "ما الذي تستطيع أن تثبته فعلاً، وما الذي تحتاج إليه لتثبت أكثر؟ هل يكفي أن تضيّق الدائرة؟", al, None, 0.02)
c.H("hg2", 2, "focus_area", "اسأل عن كل دليل: هل يشير إلى سامي دون رامي، أم إلى الاثنين بالقدر نفسه؟", he("ev_missing_report"), None, 0.04)
c.H("hg3", 3, "pointer", "ابحث عن سجل يحدد الفترة، وسجل يحدد من وصل إلى الخزانة، ثم اسأل ما الذي سيفرّق بين من وصل.", he("ev_missing_report"), None, 0.08)
c.H("hn1", 1, "metacognitive", "هل غياب التسجيل يعني غياب الفعل؟", he("ev_camera_gap"), "i_a_nodisc", 0.02)
c.H("hn2", 2, "pointer", "اقرأ حدود نتيجة البصمة: هل تستبعد أحداً؟", he("ev_partial_print"), "i_a_nodisc", 0.06)
c.H("hw1", 1, "metacognitive", "ما الدليل الذي يحدد بدء الفترة، وما الذي يحدد نهايتها؟", he("ev_count_sheet"), "i_a_window", 0.02)

steps = [
    (1, "حدّد النافذة: جرد موقّع ثم صورة بوقت مضبوط يضعان الظرف في موضعه قبل أن تتولى المفاتيح أيدي الطلاب، وبلاغ وورقة تنظيف تضعانه غائباً قبل الخامسة.", ["ev_count_sheet", "ev_missing_report", "ev_phone_photo", "ev_cleaner_round"], "i_a_window"),
    (2, "ضيّق الدائرة بمصدرين مستقلين: ورقة المفاتيح مع فحص القفل، وسجل الباب مع ورقة حصة المشرف؛ كلها تقصر الوصول على طالبين.", ["ev_key_log", "ev_lock_check", "ev_lab_register", "ev_class_timetable"], "i_a_access"),
    (3, "ثم اسأل عمّا يفرّق بينهما: أثر جزئي لا يستبعد أحداً، وكاميرا لم تسجّل، وروايتان متماثلتان؛ فلا شيء يفرّق.", ["ev_partial_print", "ev_camera_gap", "ev_sami_statement", "ev_rami_statement"], "i_a_nodisc"),
    (4, "فلا يصح اتهام أحدهما: ما يُقال عن سامي يصدق على رامي، والإشاعة بلا مصدر، وحاجة المال تعمّ خمسة أعضاء.", ["ev_group_rumor", "ev_trip_list"], "i_rule_sami"),
    (5, "الحكم المسؤول هو «غير كافٍ بعد»، مع تسمية ما يحسم: تسجيل الممر لو وُجد، أو أثر المبلغ نفسه إنفاقاً أو إيداعاً، أو بصمة كاملة.", ["ev_key_log", "ev_camera_gap", "ev_partial_print"], "i_support_insufficient"),
]
ending = {"steps": steps,
    "alt": ["يكفي طريق الجرد والمفاتيح والأثر لتحديد الفترة والدائرة وعدم التفريق، من غير الصورة وسجل الباب والإفادات.",
            "ويكفي طريق الصورة وجولة التنظيف وسجل الباب وحصة المشرف والإفادتين، من غير الجرد والمفاتيح والأثر؛ والأقوى أن يتفق الطريقان."],
    "limits": ["لا نعرف متى بين 15:42 و17:00 غاب الظرف على وجه التحديد.",
               "لا نعرف أن أحداً لم يصنع نسخة من المفتاح؛ فحص القفل ينفي الكسر لا النسخ.",
               "لا تعني عبارة «غير كافٍ» أن الاثنين بريئان؛ تعني أن ما بين أيدينا لا يسمح بحكم على أحد.",
               "الدليل الذي قد يحسم غائب عن الملف اليوم: تسجيل كاميرا لو وُجد، أو أثر للمبلغ نفسه إنفاقاً أو إيداعاً، أو بصمة كاملة قابلة للمقارنة."],
    "notes": ["«غير كافٍ» جواب علمي كامل حين تسنده بما أثبتّ: نافذة زمنية، ودائرة من اثنين، ولا دليل يفرّق بينهما. الجواب بلا هذه الثلاثة تهرّب لا معايرة.",
              "ما يصدق بالقدر نفسه على شخصين لا يرجّح أحدهما: ورقة المفاتيح، وسجل الباب، والحاجة إلى المال، كلها تعمّ الاثنين، ولذلك لا نحمّل أحداً أكثر مما نثبت.",
              "الإشاعة لا تكتسب وزناً بكثرة تحويلها؛ ابحث عن مصدرها الأول، فإن لم تجده فهي خبر بلا سند.",
              "الأثر الجزئي نتيجته «غير حاسمة» مشروعة ولا تُعدّ فشلاً؛ والخطر أن نقرأها كأنها حاسمة.",
              "حفاظاً على الإنصاف، يقدّم المشرف طلباً ودياً لمن أخذ الظرف أن يعيده دون مساءلة، ويُضاف إلى النادي سجل لحفظ المال بمفتاحين.",
              "الملف لا يسمّي الفاعل لأنه لا يعرفه: أحد الطالبين أخذه على الأرجح، ولا ثالث؛ والعبرة أن «غير كافٍ» ليست «بريء»، وأن التخمين ولو أصاب لا يساوي الإثبات.",
              "بطاقة الأصل: القضية أصلية من ATHAR، وبنيتها من نمط «لا يكفي بعد» في مكتبة تصميم القضايا؛ لا أحداث حقيقية فيها."]}
meta = {"title_ar": "ظرف النادي: لا يكفي بعد", "title_en": "The Club Envelope: Not Enough Yet", "age_band": "16-18", "locale": "ar", "dialogue_register": "msa", "estimated_minutes": 30, "difficulty": 3,
        "content_flags": ["theft"], "authors": ["فريق أثر التحريري (مسودة بمساعدة الذكاء الاصطناعي، لم تُراجَع بشرياً بعد)"],
        "knowledge_object_refs": ["KO-RS-06-021", "KO-RS-05-010", "KO-RS-05-013", "KO-RS-05-004", "KO-RS-05-005", "KO-RS-05-001", "KO-RS-05-009", "KO-RS-06-001", "KO-RS-06-008", "KO-RS-06-009", "KO-FC-04-012", "KO-FC-04-010", "KO-FC-04-024"]}
premise = {"hook_ar": "ظرف مال اختفى من خزانة مغلقة، وشخصان فقط فتحاها في الفترة الممكنة، وإشاعة تسمّي أحدهما، وكاميرا كانت متوقفة. السؤال الأصعب: هل لديك ما يكفي لتحكم؟",
           "player_role_ar": "أنت مراجع طلابي مستقل، طُلب منك رأي معلّل في فقد ظرف النادي قبل أن يقرر المشرف أي إجراء بحق أحد.",
           "setting_ar": "مدرسة القنطرة، عصر الثلاثاء إلى صباح الأربعاء. أوقات الورقات والسجلات بساعة المدرسة.",
           "public_fact_ids": ["f_envelope_gone", "f_rumor_names", "f_both_deny"],
           "assumed_general_knowledge_ar": ["لا يكفي أن يكون المرء هو الأرجح ظاهرياً لنحكم عليه", "الإشاعة المحوّلة بلا مصدر أول ليست دليلاً", "النتيجة «غير حاسمة» مشروعة ولا تُقرأ كأنها حاسمة"]}
solution = {"culprit_ids": ["sami", "rami"], "summary_ar": "الذي يثبته الملف أن الظرف أُخذ من خزانة مقفلة في نافذة زمنية محددة على يد أحد طالبين لا ثالث لهما، وليس فيه ما يفرّق بينهما. فالجواب الصحيح أن الأدلة حددت الفترة وحصرت الدائرة ولم تحسم، وأن الدليل الحاسم غائب.",
            "key_fact_ids": ["f_window", "f_two_access", "f_no_discriminator"]}
ref = "الأدلة لا تكفي بعد للحكم على أحد. ثبت أن الظرف كان في الخزانة بعد الجرد والتصوير وأنه غاب قبل جولة التنظيف، وأن القفل سليم، وأن الاثنين وحدهما حملا المفتاح ودخلا المختبر في تلك المدة. ولا شيء في الملف يفرّق بينهما: الكاميرا لم تسجّل، والأثر الجزئي غير حاسم، والروايتان متماثلتان، والإشاعة بلا مصدر أول، والحاجة إلى المال تشمل خمسة أعضاء. والدليل الذي قد يحسم: تسجيل للممر لو وُجد، أو أثر للمبلغ إنفاقاً أو إيداعاً، أو بصمة كاملة. حدود الاستنتاج: لا نعرف وقت الأخذ بدقة، ولا نستبعد نسخة مفتاح، و«غير كافٍ» لا تعني «بريء»."
ui = {
    "clock": {"epoch_hhmm": "15:00", "zone_label_ar": "ساعة المدرسة (الثلاثاء 15:00 = البداية)"},
    "cover": {"title_ar": "ظرف النادي: لا يكفي بعد", "tagline_ar": "هل الجواب الصحيح أحياناً: «لا أعرف بعد»؟", "kicker_ar": "الملف الخامس والعشرون · حد الإثبات", "glyph": "…", "accent": "green"},
    "cold_open_ar": ["الأربعاء صباحاً، مكتب مشرف النادي.", "ظرف فيه مئتا وحدة اختفى من خزانة سليمة القفل. طالبان فقط فتحاها في الفترة الممكنة، وإشاعة محوّلة تسمّي أحدهما، وكاميرا الممر كانت متوقفة.",
                     "الجميع ينتظر اسماً. وقبل أن تكتب شيئاً: ما الذي ثبت فعلاً؟ وما الذي كان يمكن أن يغيّر الصورة؟"],
    "limit_menu": [
        {"id": "l_no_discriminator", "label_ar": "ما بين أيدينا لا يفرّق بين الطالبين: ما يشير إلى أحدهما يشير إلى الآخر بالقدر نفسه"},
        {"id": "l_print_inconclusive", "label_ar": "نتيجة البصمة غير حاسمة، وقد تعود إلى أي يد لمست الرف في أي يوم"},
        {"id": "l_not_innocent", "label_ar": "«غير كافٍ» لا تعني أن الطالبين بريئان ولا أنهما متهمان"},
        {"id": "l_invalid_access", "label_ar": "من فتح الخزانة فهو الأرجح أنه أخذ الظرف"},
        {"id": "l_invalid_rumor", "label_ar": "كثرة تحويل الإشاعة ترجّح صحتها"},
        {"id": "l_invalid_money", "label_ar": "حاجة العضو إلى المال تثبت أنه أخذ الظرف"}],
    "mind_change_menu": [
        {"id": "m_camera_clip", "label_ar": "ظهور تسجيل لممر المختبرات يغطي الفترة 15:55–16:50"},
        {"id": "m_cash_trail", "label_ar": "ظهور أثر للمبلغ نفسه، إنفاقاً أو إيداعاً، يُنسب إلى أحد الطالبين"},
        {"id": "m_full_print", "label_ar": "ظهور بصمة كاملة قابلة للمقارنة على الرف الثاني"},
        {"id": "m_more_rumours", "label_ar": "ورود رسائل أخرى تردد الإشاعة نفسها"}],
    "transfer": {
        "id": "tr_forward", "title_ar": "اختبار نقل المهارة: الرسالة المحوّلة",
        "scenario_ar": "رسالة محوّلة في مجموعة صفية تقول إن طالباً سرّب أسئلة اختبار. عدد من الطلاب حوّلها. أمامك وثيقتان من واقعة خيالية لا علاقة لها بالقضية.",
        "documents": [
            {"title_ar": "لقطة الرسالة", "body_ar": "«سمعت أن فلاناً سرّب الأسئلة» — محوّلة ست مرات — لا يظهر مصدرها الأول."},
            {"title_ar": "مذكرة المعلم", "body_ar": "طُبعت الأسئلة في الغرفة المغلقة، وفتحها ثلاثة معلمين وطالبان مساعدان. لا سجل كاميرا للغرفة، ولم يُطلب من أحد توقيع الدخول."}],
        "prompt_ar": "اختر الخطوات التي تصلح لتقرير ماذا يمكن قوله الآن (يمكنك اختيار أكثر من خطوة).",
        "options": [
            {"id": "o1", "text_ar": "البحث عن المصدر الأول للرسالة قبل الاعتداد بها"},
            {"id": "o2", "text_ar": "تحديد ما يثبته الملف فعلاً: من استطاع الوصول ومتى"},
            {"id": "o3", "text_ar": "تسمية الدليل الذي سيحسم إن وُجد، كسجل دخول أو تسجيل"},
            {"id": "o4", "text_ar": "القول إن الأدلة لا تكفي بعد دون اتهام أحد"},
            {"id": "o5", "text_ar": "اعتبار كثرة التحويل دليلاً على صحة الرسالة"},
            {"id": "o6", "text_ar": "اتهام الطالب الذي يبدو الأرجح من بين المشتبه بهم"},
            {"id": "o7", "text_ar": "انتظار اعتراف أحد ثم حسم الأمر به"}],
        "free_text_prompt_ar": "اكتب في ثلاثة أسطر كيف تقرّر نسبة الترجيح بأن طالباً بعينه هو المسرّب، ولماذا تختار هذه الثقة.",
    },
    "skills": [{"skill_id": "KO-RS-06-021", "track": "D"}, {"skill_id": "KO-RS-05-010", "track": "B"}, {"skill_id": "KO-RS-05-013", "track": "B"}, {"skill_id": "KO-RS-05-004", "track": "B"}, {"skill_id": "KO-FC-04-012", "track": "E"}],
    "stage_hooks_ar": {"briefing": "الجميع ينتظر اسماً… وقد يكون الجواب الأمين أنك لا تملك ما يكفي بعد.", "investigating": "ضيّق الدائرة ثم اسأل: ما الذي يفرّق بين من بقي؟", "review": "قبل أن تغلق الملف: ما الذي ثبت، وما الذي سيحسم؟", "resolved": "أُغلق الملف بلا اسم. وبقي السؤال: ما الدليل الذي لو وصل غيّر كل شيء؟"},
    "character_glyphs": {"nada": "ن", "zaid": "ز", "sami": "س", "rami": "ر", "amer": "ع", "ghassan": "غ"},
}
sc = {
    "case_id": CID,
    "accepted_conclusions": {
        "h_insufficient": {"grade": 1, "note_ar": "استنتاج متسق مع الأدلة؛ ويتطلب ذكر ما ثبت وما الذي يحسم."},
        "h_sami": {"grade": 0, "note_ar": "يبني الاتهام على إشاعة بلا مصدر أول وعلى ما يصدق بالقدر نفسه على رامي."},
        "h_rami": {"grade": 0, "note_ar": "يبني الاتهام على ترتيب الدخول وحاجة المال، وكلاهما لا يفرّق بين الطالبين."},
        "h_outsider": {"grade": 0, "note_ar": "القفل سليم والسجلات الثلاثة لا تضم غريباً."},
        "h_never": {"grade": 0, "note_ar": "الظرف مجرود ومصوّر وغائب بعد ذلك."}},
    "confidence_band": {"h_insufficient": [65, 90], "h_sami": [0, 15], "h_rami": [0, 15], "h_outsider": [0, 10], "h_never": [0, 10]},
    "source_key": {"ev_count_sheet": "primary_record", "ev_missing_report": "claim", "ev_phone_photo": "primary_record", "ev_cleaner_round": "primary_record", "ev_key_log": "primary_record",
                   "ev_lock_check": "primary_record", "ev_lab_register": "primary_record", "ev_class_timetable": "primary_record", "ev_partial_print": "primary_record", "ev_camera_gap": "primary_record",
                   "ev_sami_statement": "claim", "ev_rami_statement": "claim", "ev_group_rumor": "claim", "ev_trip_list": "primary_record"},
    "link_key": {
        "h_insufficient": {"ev_count_sheet": "supports", "ev_phone_photo": "supports", "ev_cleaner_round": "supports", "ev_key_log": "supports", "ev_lock_check": "supports", "ev_lab_register": "supports",
                           "ev_class_timetable": "supports", "ev_partial_print": "supports", "ev_camera_gap": "supports", "ev_sami_statement": "supports", "ev_rami_statement": "supports", "ev_group_rumor": "weakens"},
        "h_sami": {"ev_group_rumor": "supports", "ev_trip_list": "supports", "ev_partial_print": "weakens", "ev_camera_gap": "weakens", "ev_sami_statement": "neutral"},
        "h_rami": {"ev_trip_list": "supports", "ev_key_log": "supports", "ev_partial_print": "weakens", "ev_camera_gap": "weakens", "ev_rami_statement": "neutral"},
        "h_outsider": {"ev_lock_check": "weakens", "ev_lab_register": "weakens", "ev_key_log": "weakens"},
        "h_never": {"ev_count_sheet": "weakens", "ev_phone_photo": "weakens", "ev_cleaner_round": "weakens"},
    },
    "required_limits": ["l_no_discriminator", "l_not_innocent"], "valid_mind_changers": ["m_camera_clip", "m_cash_trail", "m_full_print"],
    "invalid_limits": ["l_invalid_access", "l_invalid_rumor", "l_invalid_money"],
    "decisive_evidence": ["ev_count_sheet", "ev_missing_report", "ev_phone_photo", "ev_cleaner_round", "ev_key_log", "ev_lock_check", "ev_lab_register", "ev_class_timetable", "ev_partial_print", "ev_camera_gap", "ev_sami_statement", "ev_rami_statement"],
    "lab_requirement": None,
    "timeline_requirement": [{"evidence_id": "ev_count_sheet", "utc_minute": 40, "tol": 4}, {"evidence_id": "ev_phone_photo", "utc_minute": 42, "tol": 4}, {"evidence_id": "ev_camera_gap", "utc_minute": 55, "tol": 4},
                             {"evidence_id": "ev_key_log", "utc_minute": 65, "tol": 6}, {"evidence_id": "ev_cleaner_round", "utc_minute": 120, "tol": 4}, {"evidence_id": "ev_missing_report", "utc_minute": 130, "tol": 4}],
    "refuted_hypotheses": ["h_sami", "h_rami", "h_outsider", "h_never"],
    "criteria_map": {"c_source": "source_typing", "c_conflict": "conflict_resolution", "c_links": "hypothesis_links", "c_uncertainty": "uncertainty", "c_revision": "revision", "c_elimination": "elimination", "c_justification": "justification_human"},
    "transfer_key": {"valid": ["o1", "o2", "o3", "o4"], "invalid": ["o5", "o6", "o7"]},
    "caps": {"no_citations_max": 45, "no_conflict_resolution_max": 65},
}
c.build(OUT, meta=meta, premise=premise, solution=solution, locations=locations, objects=objects, orgs=orgs, hyps=hyps, mis=mis, los=los, reference_answer=ref, ending=ending, ui=ui, sc=sc, topics=topics)
