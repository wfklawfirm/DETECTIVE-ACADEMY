#!/usr/bin/env python3
# Case c011 «الطائرة التي لم يرها أحد» — adapted from heritage seed S-01 (pattern: the "lost camel" description inferred from traces; ARC-27 tracking).
# Teaches: separate what someone SAW from what they INFERRED; every detail of a precise description can have a source other than sight;
# class-level traces (two wheel marks of a known spacing) say what kind of object touched down, never who or when.
# No-culprit convention: the person whose (innocent) action started the chain (the pilot who launched with a part-charged battery) is
# recorded in culprit_ids; nobody did anything wrong. Two disjoint proof paths:
#   K1 f_drifted_east  : route A = app log + weather board ; route B = wheel marks + grass strip (+ spec card, orchard keeper's log)
#   K2 f_warad_far     : route A = water-point log + duty sheet ; route B = fair photographer's frame + radio log
# Usage: gen_c011.py OUT_DIR
import json, sys, os
OUT = sys.argv[1]
CID = "c011_unseen_drone"

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
ch("nader", "نادر الحمدان", "victim", "15 سنة، رئيس نادي التصوير وصاحب الطائرة",
   "قلق وسريع الحكم، يظن أن من يصف الشيء بدقة لا بد أنه رآه أو لمسه، ويتراجع إذا واجهته بسجل مكتوب.",
   ["استعادة طائرة النادي قبل نهاية المعرض", "ألا يُلام النادي على ضياع معدّاته"],
   [L("nd_greet", "greeting", "أهلاً. طائرتنا اختفت يوم الافتتاح، وأريد أن أفهم كيف عرف ورد كل هذه التفاصيل."),
    L("nd_pilot", "reveal", "سليم هو من طيّرها من مكتب التحكم عند العاشرة، وأنا طلبت منه ألّا يطيل التحليق.", ["f_salim_flew"]),
    L("nd_only", "reveal", "لا يقول هذا الوصف إلا من رآها أو حملها بيده، فهذا هو الاستنتاج الوحيد المعقول.", None, ["cl_nader_witness"]),
    L("nd_open", "reveal", "والبستان المجاور مفتوح لكل من يريد المرور، فربما التقطها أحد الزوار.", None, ["cl_orchard_open"]),
    L("nd_unknown", "deflect_unknown", "لا أعرف. هذا بعيد عمّا كنت أراقبه."),
    L("nd_off", "deflect_offtopic", "رجاءً، لنبقَ في موضوع الطائرة وما قيل عنها."),
    L("nd_bye", "farewell", "أريد جواباً قبل أن ينتهي المعرض. شكراً لوقتك.")])
ch("warad", "ورد الخطيب", "suspect", "14 سنة، متطوع في شبكة الأثر",
   "ملاحظ هادئ يربط التفاصيل الصغيرة، لكنه يتكلم بصيغة الجزم حين يتوتر فيبدو كأنه يروي ما شاهده بعينه.",
   ["ألا يُحرم من إكمال التطوع في المعرض", "أن يُفهم أنه قال ما قاله بنيّة المساعدة"],
   [L("wd_greet", "greeting", "أنا لم آخذ الطائرة. اسألني عمّا قلته وكيف قلته."),
    L("wd_post", "reveal", "كنت عند نقطة الماء الجنوبية من التاسعة وخمسين دقيقة إلى العاشرة وأربعين دقيقة، وبعدها مشيت إلى مكتب المنسّقة.", ["f_warad_post"]),
    L("wd_route", "reveal", "طريقي إلى المكتب يمرّ بممر البستان، ومررت بطرفه الشرقي بين العاشرة وخمس وأربعين والعاشرة وخمس وخمسين.", ["f_warad_route"]),
    L("wd_marks", "reveal", "هناك رأيت علامات على الأرض قرب الشبك، فصوّرتها بهاتفي لأعرضها على المنسّقة.", ["f_warad_marks_place"]),
    L("wd_feather", "reveal", "نعم، علقت بالطائرة ريشة، هذا ما قلته وأظنه صحيحاً.", None, ["cl_warad_feather"]),
    L("wd_refuse", "refuse_secret", "قلت كل ما عندي في هذه النقطة."),
    L("wd_admit", "reveal", "حسناً... أنا لم أرَ الطائرة نفسها. رأيت الريشة على الشبك فافترضت أنها علقت بها، وقلتها كأنها مؤكدة.", ["f_warad_admits"]),
    L("wd_unknown", "deflect_unknown", "لا أعرف، ولا أحب أن أخمّن."),
    L("wd_off", "deflect_offtopic", "هذا بعيد عن موضوع الطائرة. اسألني عمّا حدث ذلك الصباح."),
    L("wd_bye", "farewell", "شكراً لأنك تسأل عن مصدر كل تفصيل قبل أن تحكم.")])
ch("salim", "سليم البغدادي", "suspect", "15 سنة، عضو في نادي التصوير وقائد الطائرة",
   "لطيف ويعتذر كثيراً، يميل إلى التقليل من شأن أخطائه الصغيرة، ويفضّل أن يعرض السجل على أن يشرح.",
   ["أن تعود الطائرة سالمة", "ألا يظن زملاؤه أنه أهمل في عمله"],
   [L("sl_greet", "greeting", "أنا من كان يطيّرها. يمكنني أن أريك السجل الذي يحفظه التطبيق."),
    L("sl_app", "reveal", "التطبيق يحتفظ بسجل لكل رحلة على هاتفي، ويمكنني تصدير نسخة منه لتقرأها.", ["f_app_log_exists"]),
    L("sl_announce", "reveal", "حين ظهر تنبيه البطارية طلبت من المنسّق أن يعلن للزوار أن الطائرة تعود لانخفاض بطاريتها.", ["f_announce_asked"]),
    L("sl_east", "reveal", "رأيتها تغيب خلف أشجار البستان نحو الشرق، ثم انقطع الاتصال في العاشرة واثنتي عشرة دقيقة.", ["f_salim_saw_east"]),
    L("sl_refuse", "refuse_secret", "بدأت الرحلة بالشكل المعتاد، ولا أذكر شيئاً آخر يخص الشحن."),
    L("sl_charge", "reveal", "نعم... أقلعتُ وبطاريتها نحو خمسة وثلاثين في المئة لأن الشحن لم يكتمل، ولم أخبر نادر بذلك.", ["f_start_battery"]),
    L("sl_unknown", "deflect_unknown", "لا أعرف، لم أرَ أكثر من ذلك."),
    L("sl_off", "deflect_offtopic", "أفضّل أن نبقى في موضوع الرحلة."),
    L("sl_bye", "farewell", "أتمنى أن تعود الطائرة، وأن يُفهم ما حدث.")])
ch("rami", "رامي الشامي", "witness", "مشرف متطوع في نقطة الماء الجنوبية",
   "منظم ودقيق في التوقيع والتسليم، قليل الكلام، ويقول ما في دفتره فقط.",
   ["أن يبقى سجل نقطة الماء سليماً", "أن يُنصف المتطوعون الصغار"],
   [L("rm_greet", "greeting", "تفضّل. سجل المناوبات أمامي، وأقرأ منه فقط."),
    L("rm_log", "reveal", "عندنا سجل تسليم يوقّعه كل متطوع عند الاستلام وعند التسليم.", ["f_water_log_exists"]),
    L("rm_warad", "reveal", "ورد استلم المناوبة عند التاسعة وخمسين دقيقة، وسلّمها لي عند العاشرة وأربعين دقيقة.", ["f_warad_post"]),
    L("rm_unknown", "deflect_unknown", "ليس في سجلي."),
    L("rm_off", "deflect_offtopic", "اسألني عن نقطة الماء فقط."),
    L("rm_bye", "farewell", "مع السلامة.")])
ch("jamil", "جميل الأنصاري", "witness", "حارس البستان المجاور للمعرض",
   "هادئ ومتحفظ، يعتزّ بدفتر يومه ويكتب فيه كل ما يخص البوابة والري والصيانة.",
   ["أن يبقى البستان سليماً", "ألا يُنسب إليه إهمال في الحراسة"],
   [L("jm_greet", "greeting", "أهلاً. البستان في عهدتي منذ الصباح، ودفتري يقول ما جرى."),
    L("jm_log", "reveal", "أدوّن في دفتر اليوم كل ما يخص البوابة والري والجزّ ودخول العربات.", ["f_orchard_log_exists"]),
    L("jm_closed", "reveal", "أقفلت البوابة الرئيسية عند الثامنة ومفتاحها معي حتى الحادية عشرة، ولم تدخل عربات بعد الري.", ["f_orchard_closed"]),
    L("jm_unknown", "deflect_unknown", "لا أعلم، ليس في دفتري."),
    L("jm_off", "deflect_offtopic", "اسألني عن البستان وبوابته."),
    L("jm_bye", "farewell", "تفضّل بزيارتنا متى شئت.")])

locations = [{"id": "loc_fair", "name_ar": "ساحة المعرض ومكتب التحكم", "description_ar": "حيث يعمل مكتب التحكم ومكبّر الصوت."},
             {"id": "loc_orchard", "name_ar": "البستان المجاور", "description_ar": "بستان بعشب ممتد يفصله شبك عن القناة."},
             {"id": "loc_water", "name_ar": "نقطة الماء الجنوبية", "description_ar": "عند بوابة المعرض الجنوبية، وتبعد نحو ستمئة متر عن البستان."},
             {"id": "loc_desk", "name_ar": "مكتب المنسّقة", "description_ar": "حيث يسجّل المتطوعون وصولهم."},
             {"id": "loc_canal", "name_ar": "ضفة القناة", "description_ar": "حافة القناة خلف الشبك الشرقي للبستان."}]
objects = [{"id": "obj_aircraft", "name_ar": "طائرة التصوير الصغيرة", "description_ar": "طائرة خفيفة بعجلتي هبوط تملكها نادي التصوير."}]
orgs = [{"id": "org_club", "name_ar": "نادي التصوير", "description_ar": "نادٍ طلابي يشارك في معرض القافلة."},
        {"id": "org_net", "name_ar": "شبكة الأثر", "description_ar": "شبكة متطوعين خيالية تساعد في تنظيم المعرض."}]

# ---------------------------------------------------------------- facts
facts = []
def F(id, st, kind, subj, spoiler, time=None, loc=None, ko=None):
    d = {"id": id, "statement_ar": st, "kind": kind, "subject_ids": subj, "spoiler_level": spoiler}
    if time: d["time"] = time
    if loc: d["location_id"] = loc
    if ko: d["science_ko_refs"] = ko
    facts.append(d)
F("f_aircraft_missing", "فُقد الاتصال بطائرة التصوير الصغيرة يوم افتتاح معرض القافلة ولم يُعثر عليها.", "event", ["obj_aircraft"], 0)
F("f_nader_accuses", "يتهم نادر ورد بأنه أخذ الطائرة لأنه وصفها بدقة.", "attribute", ["nader", "warad"], 0)
F("f_warad_described", "وصف ورد الطائرة بأن بطاريتها منخفضة وأنها تميل إلى اليسار وأن ريشة علقت بها وأنها حطّت قرب الماء.", "event", ["warad", "obj_aircraft"], 0, T(58), "loc_desk")
F("f_salim_flew", "أقلع سليم بالطائرة من مكتب التحكم عند الساعة 10:00 تقريباً.", "event", ["salim", "obj_aircraft"], 1, T(0), "loc_fair")
F("f_start_battery", "كانت بطارية الطائرة نحو 35% عند الإقلاع لأن الشحن لم يكتمل.", "state", ["salim", "obj_aircraft"], 2, T(0), "loc_fair")
F("f_app_log_exists", "يحتفظ تطبيق التحكم بسجل لكل رحلة يمكن تصديره.", "state", ["salim"], 1)
F("f_announce_asked", "طلب سليم من المنسّق أن يعلن للزوار عودة الطائرة لانخفاض بطاريتها.", "event", ["salim"], 1, T(8), "loc_fair")
F("f_battery_public", "أُعلن للزوار عبر مكبّر الصوت عند 10:09 أن بطارية الطائرة منخفضة وأنها تعود.", "event", ["obj_aircraft"], 2, T(9), "loc_fair")
F("f_salim_saw_east", "رأى سليم الطائرة تغيب خلف أشجار البستان نحو الشرق قبل أن ينقطع الاتصال عند 10:12.", "event", ["salim", "obj_aircraft"], 1, T(12), "loc_orchard")
F("f_warad_post", "كان ورد عند نقطة الماء الجنوبية من 09:50 إلى 10:40.", "event", ["warad", "loc_water"], 1, T(-10, "exact", 40), "loc_water")
F("f_water_log_exists", "لنقطة الماء الجنوبية سجل تسليم يوقّعه كل متطوع.", "state", ["rami", "loc_water"], 1)
F("f_warad_far", "كان ورد عند نقطة الماء الجنوبية، على بعد نحو 600 م من البستان، وقت انقطاع الاتصال، فلم يشهد الحدث.", "relation", ["warad", "loc_water", "obj_aircraft"], 2, T(12), "loc_water", ["KO-RS-06-004"])
F("f_warad_route", "مرّ ورد بالطرف الشرقي للبستان بين 10:45 و10:55 وسجّل وصوله إلى مكتب المنسّقة عند 10:58.", "event", ["warad"], 1, T(45, "approx", 55), "loc_orchard")
F("f_warad_marks_place", "رأى ورد علامات على الأرض قرب الشبك عند الطرف الشرقي للبستان وصوّرها.", "event", ["warad", "loc_orchard"], 1, T(50, "approx"), "loc_orchard")
F("f_orchard_log_exists", "لحارس البستان دفتر يومي يدوّن فيه البوابة والري والجزّ ودخول العربات.", "state", ["jamil", "loc_orchard"], 1)
F("f_orchard_closed", "بوابة البستان الرئيسية مقفلة من 08:00 إلى 11:00، ولم يُجزّ العشب، ولم تدخل عربات بعد الري.", "state", ["jamil", "loc_orchard"], 1, T(-120, "exact", 60), "loc_orchard")
F("f_wind_east", "كانت الرياح غربية وتشتد إلى نحو 22 كم/س بين 10:00 و10:30.", "state", ["loc_orchard"], 1, T(0, "approx", 30))
F("f_link_lost", "انقطع اتصال الطائرة عند 10:12 وهي فوق الطرف الشرقي للبستان متجهة شرقاً.", "event", ["obj_aircraft"], 1, T(12), "loc_orchard")
F("f_gear_mark", "في تربة الطرف الشرقي للبستان أثران متوازيان لعجلتين، الأيسر أعمق من الأيمن.", "state", ["loc_orchard"], 1, None, "loc_orchard", ["KO-FC-04-015"])
F("f_mark_is_aircraft", "مسافة الأثرين تطابق عجلتي الطائرة، فالأثر لها لا لعربة، ويدل على ملامسة مائلة إلى اليسار.", "relation", ["obj_aircraft", "loc_orchard"], 2, None, "loc_orchard", ["KO-FC-04-015"])
F("f_grass_strip", "العشب مائل نحو الشرق في شريط طوله نحو 25 م من الأثر إلى الشبك، بلا آثار أقدام.", "state", ["loc_orchard"], 1, None, "loc_orchard")
F("f_grass_wind", "ميل العشب سببه الريح لا أقدام ولا جزّ ولا ري.", "relation", ["loc_orchard"], 2, None, "loc_orchard", ["KO-RS-06-015"])
F("f_feather", "ريشة طائر مائي عالقة بشبك الطرف الشرقي قرب القناة.", "state", ["loc_canal"], 1, None, "loc_canal")
F("f_warad_admits", "لم يرَ ورد الطائرة، وافترض أن الريشة التي رآها على الشبك علقت بها.", "attribute", ["warad"], 2)
F("f_drifted_east", "فقدت الطائرة الاتصال بعد انخفاض بطاريتها، وحملتها الرياح الغربية شرقاً نحو ضفة القناة.", "event", ["obj_aircraft", "loc_canal"], 3, T(12, "approx", 20), "loc_canal", ["KO-NP-02H-001"])
F("f_details_sourced", "لكل تفصيل في وصف ورد مصدر غير رؤية الطائرة: نداء عام عن البطارية، وأثر العجلتين، وميل العشب، وريشة على الشبك.", "relation", ["warad", "obj_aircraft"], 3, None, None, ["KO-RS-06-004", "KO-NP-02H-001"])

claims = [
    {"id": "cl_nader_witness", "statement_ar": "لا يصف الطائرة بهذه التفاصيل إلا من رآها أو حملها.", "kind": "half_truth", "held_by": ["nader"], "true_fact_id": "f_details_sourced", "contradicted_by_evidence_ids": ["ev_announce_sheet", "ev_gear_photo", "ev_grass_photo", "ev_water_log"]},
    {"id": "cl_orchard_open", "statement_ar": "البستان مفتوح لكل من يريد المرور فيه.", "kind": "rumour", "held_by": ["nader"], "true_fact_id": "f_orchard_closed", "contradicted_by_evidence_ids": ["ev_orchard_log", "ev_security_round"]},
    {"id": "cl_warad_feather", "statement_ar": "علقت بالطائرة ريشة.", "kind": "honest_mistake", "held_by": ["warad"], "true_fact_id": "f_feather", "contradicted_by_evidence_ids": ["ev_feather_photo"]},
]
timeline = [
    {"id": "te_water_post", "description_ar": "ورد يعمل في نقطة الماء الجنوبية.", "time": T(-10, "exact", 40), "location_id": "loc_water", "actor_ids": ["warad"], "fact_ids": ["f_warad_post"], "motivated_by_ar": "مناوبته المحددة في جدول المتطوعين"},
    {"id": "te_launch", "description_ar": "سليم يقلع بالطائرة من مكتب التحكم.", "time": T(0), "location_id": "loc_fair", "actor_ids": ["salim"], "fact_ids": ["f_salim_flew", "f_start_battery"], "motivated_by_ar": "أراد تصوير افتتاح المعرض من الجو"},
    {"id": "te_announce", "description_ar": "النداء العام عن انخفاض البطارية وعودة الطائرة.", "time": T(9), "location_id": "loc_fair", "actor_ids": ["salim"], "fact_ids": ["f_announce_asked", "f_battery_public"], "motivated_by_ar": "طلب من المنسّق تنبيه الزوار بعد ظهور تحذير البطارية"},
    {"id": "te_lost", "description_ar": "انقطاع اتصال الطائرة فوق الطرف الشرقي للبستان.", "time": T(12), "location_id": "loc_orchard", "actor_ids": [], "fact_ids": ["f_link_lost", "f_salim_saw_east", "f_wind_east"]},
    {"id": "te_walk", "description_ar": "ورد يمرّ بالطرف الشرقي للبستان ويصوّر العلامات.", "time": T(45, "approx", 55), "location_id": "loc_orchard", "actor_ids": ["warad"], "fact_ids": ["f_warad_route", "f_warad_marks_place"], "motivated_by_ar": "طريقه المعتاد إلى مكتب المنسّقة بعد انتهاء المناوبة"},
    {"id": "te_desk", "description_ar": "ورد يصل مكتب المنسّقة ويصف ما استنتجه.", "time": T(58), "location_id": "loc_desk", "actor_ids": ["warad"], "fact_ids": ["f_warad_described"], "motivated_by_ar": "أراد مساعدة النادي بما لاحظه في الطريق"},
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
V("ev_app_log", "سجل رحلة طائرة التحكم", "digital",
  "سجل التطبيق المصدَّر من هاتف سليم (الأوقات بساعة هاتفه)\n10:00 إقلاع — البطارية 35%\n10:08 تنبيه: البطارية منخفضة 14%\n10:11 بدء العودة التلقائية — البطارية 9%\n10:12 انقطع الاتصال — آخر موضع معروف: الطرف الشرقي للبستان، الاتجاه شرقاً، نحو 40 م من ضفة القناة",
  ["a_get_app"], ["f_link_lost", "f_start_battery"], "strong",
  "يثبت آخر موضع أبلغت عنه الطائرة قبل انقطاع الاتصال، لا موضع هبوطها ولا ما جرى بعد ذلك؛ وساعة الهاتف لم تُقارن بساعة المعرض.", loc="loc_fair")
V("ev_weather_board", "لوحة الطقس عند مدخل المعرض", "documentary",
  "لوحة الطقس (تُحدَّث كل عشر دقائق)\n10:00 — رياح غربية 14 كم/س\n10:10 — رياح غربية 22 كم/س، هبّات متقطعة\n10:20 — رياح غربية 20 كم/س",
  ["a_read_weather"], ["f_wind_east"], "strong",
  "قراءة عند مدخل المعرض على بعد نحو 300 م من البستان؛ لا تقيس الريح فوق الطرف الشرقي للبستان نفسه.", loc="loc_fair")
V("ev_announce_sheet", "ورقة نداءات المعرض", "documentary",
  "ورقة النداءات (يقرؤها المنسّق عبر مكبّر الصوت)\n10:09 — «تنبيه للزوار: طائرة التصوير تعود إلى مكتب التحكم لانخفاض بطاريتها. نرجو إبقاء الساحة الشرقية خالية.»\n10:15 — «افتتاح معرض القافلة، تفضّلوا إلى قاعة الصور.»",
  ["a_read_announce"], ["f_battery_public"], "strong",
  "تثبت أن النداء أُعلن في ذلك الوقت؛ لا تثبت أن ورد سمعه ولا أين انتهت الطائرة.", contradicts=["cl_nader_witness"], loc="loc_fair")
V("ev_spec_sheet", "بطاقة جرد طائرة النادي", "documentary",
  "بطاقة جرد النادي — طائرة التصوير الصغيرة\nالوزن: 900 غ\nعدد عجلات الهبوط: 2\nالمسافة بين مركزي العجلتين: 18 سم\nقطر العجلة: 2 سم",
  ["a_read_spec"], ["f_mark_is_aircraft"], "moderate",
  "بيانات عامة عن نموذج الطائرة، ولا تدل على أن هذه الطائرة بعينها هي التي ترك أثرها؛ عجلات أخرى قد تتشابه معها في القياس.", loc="loc_fair")
V("ev_gear_photo", "صورة أثر العجلتين", "physical",
  "صورة بمسطرة لأثرين متوازيين في تربة الطرف الشرقي للبستان (الاتجاه من الغرب إلى الشرق)\nالأثر الأيسر: عمق نحو 2.5 سم\nالأثر الأيمن: عمق نحو 0.8 سم\nالمسافة بين مركزي الأثرين: 18 سم\nقطر كل أثر: نحو 2 سم",
  ["a_search_orchard"], ["f_gear_mark"], "strong",
  "تدل على ملامسة عجلتين بهذه المسافة وبهذا الفرق في العمق؛ لا تدل على وقت الملامسة ولا على بقاء الطائرة هناك، وهي خصائص فئوية لا تفرّد جسماً بعينه.", ko="KO-FC-04-015", loc="loc_orchard")
V("ev_grass_photo", "صورة شريط العشب المائل", "physical",
  "صورتان لشريط العشب بين الأثرين وشبك القناة: السيقان مائلة نحو الشرق على امتداد نحو 25 م، وبعرض نحو نصف متر. لا آثار أقدام داخل الشريط ولا آثار عجلات عربات.",
  ["a_search_orchard"], ["f_grass_strip"], "strong",
  "تبيّن اتجاه الميل وخلوّه من آثار الأقدام؛ لا تبيّن ما الذي أمال العشب ولا متى، والعشب قد يرتد بعد ساعات.", loc="loc_orchard")
V("ev_feather_photo", "صورة الريشة على الشبك", "physical",
  "صورة لريشة رمادية بيضاء طولها نحو 12 سم عالقة بشبك السياج الشرقي قرب القناة. لم يُعثر على ريش مشابه في الشريط ولا في ممر البستان.",
  ["a_search_orchard"], ["f_feather"], "moderate",
  "تدل على وجود ريشة على الشبك؛ لا تدل على أنها لامست الطائرة، فالطيور المائية تُسقط ريشها قرب الماء كل يوم.", contradicts=["cl_warad_feather"], loc="loc_canal")
V("ev_orchard_log", "دفتر حارس البستان", "documentary",
  "دفتر الحارس — يوم الافتتاح\n08:00 — أُقفلت البوابة الرئيسية بالمفتاح، والمفتاح معي.\n08:30 — ريّ العشب بالرشاش (انتهى 09:00).\nلا جزّ اليوم. لا دخول لعربات الخدمة بعد الري.\n11:00 — فُتحت البوابة لدخول فريق المعرض.",
  ["a_get_orchard_log"], ["f_orchard_closed"], "strong",
  "يخص البوابة الرئيسية فقط؛ لا يشمل الشبك الشرقي المطل على القناة، ولا يثبت أن أحداً لم يقترب من الضفة نفسها.", contradicts=["cl_orchard_open"], loc="loc_orchard")
V("ev_water_log", "سجل تسليم نقطة الماء", "documentary",
  "سجل تسليم نقطة الماء الجنوبية\n09:50 — ورد (متطوع رقم 27) استلم المناوبة\n10:05 — استلام 12 قارورة ماء مثلجة، التوقيع: ورد\n10:40 — انتهاء مناوبة ورد، وتوقيع رامي بالتسلّم",
  ["a_get_water_log"], ["f_warad_post"], "strong",
  "يثبت توقيعاً عند الاستلام وعند التسليم؛ لا يثبت أن ورد لم يبتعد دقائق بين التوقيعين.", contradicts=["cl_nader_witness"], loc="loc_water")
V("ev_duty_sheet", "جدول متطوعي شبكة الأثر", "documentary",
  "جدول متطوعي شبكة الأثر ليوم الافتتاح\nمتطوع 27 (ورد): نقطة الماء الجنوبية 09:50–10:40، ثم التوجه إلى مكتب المنسّقة عبر ممر البستان.\nمسافة نقطة الماء إلى الطرف الشرقي للبستان: نحو 600 م.\nتسجيل الوصول إلى مكتب المنسّقة: 10:58 (توقيع المنسّقة).",
  ["a_read_duty"], ["f_warad_post", "f_warad_route"], "strong",
  "جدول مخطّط وتوقيع وصول؛ لا يتتبع خطوات ورد بين المحطتين ولا يقول أين وقف.", loc="loc_desk")
V("ev_fair_photo", "صورة مصوّر المعرض عند نقطة الماء", "digital",
  "صورة من مصوّر المعرض الرسمي — بياناتها الوصفية: 10:14:20، الموقع: نقطة الماء الجنوبية.\nفي الصورة متطوع بسترة رقم 27 يسكب الماء من قارورة خلف الطاولة، وخلفه لافتة «البوابة الجنوبية».",
  ["a_get_fair_photo"], ["f_warad_far"], "strong",
  "لحظة واحدة في الصورة؛ لا تتبع حركة المتطوع قبلها أو بعدها، ورقم السترة لا يغني عن التحقق من لابسها.", loc="loc_water")
V("ev_radio_log", "سجل لاسلكي مكتب المنسّقة", "documentary",
  "سجل الاتصال اللاسلكي — مكتب المنسّقة\n10:13 — من نقطة الماء الجنوبية: «هنا المتطوع 27، ورد، نحتاج ثلجاً إضافياً.»\n10:58 — المتطوع 27: «وصلتُ المكتب، ولدي ملاحظة عن علامات في أرض البستان.»",
  ["a_read_radio"], ["f_warad_far", "f_warad_route"], "strong",
  "يثبت ما قيل وبأي وقت؛ لا يثبت موقع المتكلم بذاته، ويحتاج إلى مصدر آخر يؤيد المكان.", loc="loc_desk")
V("ev_nader_statement", "إفادة نادر (ملخص)", "testimonial",
  "ملخص إفادة نادر الحمدان:\n«ورد وصف الطائرة: بطاريتها منخفضة، وهي تميل إلى اليسار، وعلقت بها ريشة، وحطّت قرب الماء. لا يقول هذا إلا من رآها أو حملها. والبستان مفتوح لأي زائر.»",
  ["a_note_nader"], ["f_nader_accuses"], "weak",
  "إفادة صاحب الطائرة وهو قلق؛ عبارة «لا يقول هذا إلا من رآها» رأي لا ملاحظة، وقوله عن البستان يُقاس بدفتر الحارس.", loc="loc_desk")
V("ev_warad_said", "ما قاله ورد عند مكتب المنسّقة", "testimonial",
  "نقل ما قاله ورد لنادر عند 10:58:\n«بطارية الطائرة منخفضة، وهي تميل إلى اليسار، وعلقت بها ريشة، وحطّت قرب الماء.»",
  ["a_note_warad"], ["f_warad_described"], "weak",
  "عبارة قيلت بصيغة الجزم دون ذكر المصدر؛ ولم تُسجَّل أسئلة تتبعها، فلا تفرّق بين ما شُوهد وما استُنتج.", red=True, loc="loc_desk")
V("ev_security_round", "سجل جولة أمن المعرض", "documentary",
  "سجل جولة أمن المعرض على بوابة البستان (توقيع الحارس المناوب)\n09:30 — البوابة مقفلة بقفلها، لا أحد عندها.\n10:00 — البوابة مقفلة بقفلها، لا أحد عندها.\n10:20 — البوابة مقفلة بقفلها، لا أحد عندها.\n10:40 — البوابة مقفلة بقفلها، لا أحد عندها.",
  ["a_read_security"], ["f_orchard_closed"], "strong",
  "يثبت أن البوابة كانت مقفلة عند كل مرور؛ لا يغطي الدقائق بين المرورين ولا الشبك المطل على القناة.", contradicts=["cl_orchard_open"], loc="loc_orchard")

# ---------------------------------------------------------------- inferences
def P(t, i): return {"ref_type": t, "ref_id": i}
inf = []
def I(id, prem, ct, concl, rel, strength, rule, ks):
    inf.append({"id": id, "premises": prem, "conclusion": {"ref_type": ct, "ref_id": concl}, "relation": rel, "strength": strength, "rule_ar": rule, "skill_ko_refs": ks})
# K1 route A (records)
I("i_a_drift", [P("evidence", "ev_app_log"), P("evidence", "ev_weather_board")], "fact", "f_drifted_east", "establishes", "strong",
  "آخر موضع للطائرة كان فوق طرف البستان متجهة شرقاً على بعد نحو 40 م من الضفة، والرياح غربية وتشتد إلى 22 كم/س؛ فالتفسير الأقرب أن الريح حملتها شرقاً بعد انقطاع الاتصال.", ["KO-FC-04-024", "KO-RS-06-001"])
# K1 route B (traces)
I("i_b_mark", [P("evidence", "ev_gear_photo"), P("evidence", "ev_spec_sheet")], "fact", "f_mark_is_aircraft", "establishes", "strong",
  "مسافة 18 سم بين مركزي الأثرين تطابق عجلتي هذا النموذج، والأثر الأيسر أعمق؛ فالجسم الذي لامس التربة كان من هذه الفئة ومائلاً إلى اليسار لحظتها.", ["KO-FC-04-015"])
I("i_b_grass", [P("evidence", "ev_grass_photo"), P("evidence", "ev_orchard_log")], "fact", "f_grass_wind", "establishes", "strong",
  "الشريط مائل بانتظام ولا فيه أقدام، والبستان مقفل بلا جزّ ولا عربات بعد الري؛ فالريح هي السبب الباقي لميل العشب نحو الشرق.", ["KO-RS-06-015"])
I("i_b_drift", [P("fact", "f_mark_is_aircraft"), P("fact", "f_grass_wind")], "fact", "f_drifted_east", "establishes", "strong",
  "ملامسة الطائرة للتربة ثم ميل العشب بالريح من الأثر نحو شبك القناة يوافقان حركة شرقية بالريح، وتؤكدها أن الأثر يقع في آخر موضع معروف لها.", ["KO-RS-06-007"])
# K2 route A (duty records)
I("i_a_far", [P("evidence", "ev_water_log"), P("evidence", "ev_duty_sheet")], "fact", "f_warad_far", "establishes", "strong",
  "السجل يضع توقيع ورد عند نقطة الماء 10:05 و10:40، والجدول يجعل مناوبته هناك بين 09:50 و10:40 على بعد نحو 600 م من البستان؛ فلم يكن حاضراً حين انقطع الاتصال عند 10:12.", ["KO-RS-06-017"])
# K2 route B (independent)
I("i_b_far", [P("evidence", "ev_fair_photo"), P("evidence", "ev_radio_log")], "fact", "f_warad_far", "establishes", "strong",
  "نداء 10:13 اللاسلكي من نقطة الماء وصورة المصوّر 10:14 عند الطاولة نفسها بسترة رقم 27 يتفقان من مصدرين مستقلين على أن ورد كان بعيداً عن البستان بعد الانقطاع بدقيقة.", ["KO-RS-06-017", "KO-RS-05-004"])
# how he could know (non-key)
I("i_src_battery", [P("evidence", "ev_announce_sheet")], "fact", "f_battery_public", "establishes", "strong",
  "ما أُعلن بمكبّر الصوت يسمعه من في المعرض، فمعرفة انخفاض البطارية لا تستلزم رؤية الطائرة.", ["KO-RS-06-004"])
I("i_src_all", [P("fact", "f_battery_public"), P("fact", "f_mark_is_aircraft"), P("fact", "f_grass_wind"), P("evidence", "ev_feather_photo")], "fact", "f_details_sourced", "establishes", "strong",
  "البطارية من النداء، والميل إلى اليسار من عمق الأثر الأيسر، والقرب من الماء من اتجاه العشب نحو القناة، والريشة وُجدت على الشبك؛ فلكل تفصيل مصدر سوى رؤية الطائرة.", ["KO-RS-06-004", "KO-NP-02H-001"])
I("i_nader_claim", [P("fact", "f_details_sourced"), P("fact", "f_warad_far")], "claim", "cl_nader_witness", "contradicts_claim", "strong",
  "من وصف الطائرة قد يكون استنتج تفاصيلها من آثار ونداء عام، وورد كان بعيداً عنها؛ فاحتمال الرؤية أو الحمل ليس التفسير الوحيد.", ["KO-RS-06-004", "KO-RS-05-014"])
I("i_orchard_claim", [P("evidence", "ev_orchard_log"), P("evidence", "ev_security_round")], "claim", "cl_orchard_open", "contradicts_claim", "strong",
  "دفتر الحارس وسجل جولة الأمن، وهما مصدران مستقلان، يسجلان إقفال البوابة الرئيسية في الفترة كلها.", ["KO-RS-05-014"])
I("i_feather_claim", [P("evidence", "ev_feather_photo")], "claim", "cl_warad_feather", "contradicts_claim", "suggestive",
  "الريشة مصوّرة على الشبك لا على الطائرة، والطيور المائية تُسقط ريشها قرب القناة؛ فالقول بأنها علقت بها فرض بلا سند.", ["KO-RS-06-004"])
I("i_support_drift", [P("fact", "f_drifted_east")], "hypothesis", "h_drift", "supports", "strong",
  "انجراف الطائرة بالريح يفسّر غيابها عن الموضع الذي انقطع فيه الاتصال ويتفق مع كل ما سُجّل عنها.", ["KO-RS-06-006"])
I("i_rule_took", [P("fact", "f_warad_far")], "hypothesis", "h_took", "rules_out", "strong",
  "من كان بعيداً عن البستان لحظة انقطاع الاتصال لا يمكن أن يكون أخذ الطائرة عند هبوطها فيه؛ ودقة وصفه لا تعوّض غيابه.", ["KO-RS-06-008", "KO-RS-05-007"])
I("i_rule_took_src", [P("fact", "f_details_sourced")], "hypothesis", "h_took", "rules_out", "strong",
  "إذا كان لكل تفصيل في الوصف مصدر غير الحمل، فدقة الوصف لا تدعم فرضية الأخذ أكثر مما تدعم أي فرضية أخرى.", ["KO-RS-06-001"])
I("i_rule_outsider_a", [P("evidence", "ev_security_round")], "hypothesis", "h_outsider", "rules_out", "strong",
  "جولة الأمن وجدت البوابة مقفلة في كل مرور من 09:30 إلى 10:40، فلم يدخل زائر عبرها إلى البستان في الفترة التي هبطت فيها الطائرة.", ["KO-RS-06-008"])
I("i_rule_outsider_b", [P("evidence", "ev_orchard_log"), P("evidence", "ev_grass_photo")], "hypothesis", "h_outsider", "rules_out", "strong",
  "الحارس يسجّل الإقفال، وشريط العشب بين موضع الملامسة والشبك بلا آثار أقدام؛ فلا أثر لزائر اقترب من الموضع.", ["KO-RS-06-008"])

# ---------------------------------------------------------------- character knowledge
K = lambda f, a="witnessed", c="certain": {"fact_id": f, "access": a, "certainty": c}
ck = [
    {"character_id": "nader", "knows": [K("f_salim_flew", "common_knowledge")], "hides": [], "believes": [{"claim_id": "cl_nader_witness", "stance": "sincere"}, {"claim_id": "cl_orchard_open", "stance": "sincere"}]},
    {"character_id": "warad", "knows": [K("f_warad_post"), K("f_warad_route"), K("f_warad_marks_place")],
     "hides": [{"fact_id": "f_warad_admits", "reveal_when": {"presented": {"evidence_id": "ev_feather_photo", "to_character": "warad"}}, "cover_claim_id": "cl_warad_feather", "reveal_line_id": "wd_admit"}],
     "believes": [{"claim_id": "cl_warad_feather", "stance": "sincere"}]},
    {"character_id": "salim", "knows": [K("f_app_log_exists"), K("f_announce_asked"), K("f_salim_saw_east")],
     "hides": [{"fact_id": "f_start_battery", "reveal_when": {"presented": {"evidence_id": "ev_app_log", "to_character": "salim"}}, "cover_claim_id": None, "reveal_line_id": "sl_charge"}], "believes": []},
    {"character_id": "rami", "knows": [K("f_water_log_exists", "professional"), K("f_warad_post")], "hides": [], "believes": []},
    {"character_id": "jamil", "knows": [K("f_orchard_log_exists", "professional"), K("f_orchard_closed", "professional")], "hides": [], "believes": []},
]
hyps = [
    {"id": "h_took", "statement_ar": "أخذ ورد الطائرة حين هبطت ثم أخفاها، ودقة وصفه لها دليل على ذلك.", "is_true": False, "plausibility_at_start": "high", "suspect_id": "warad"},
    {"id": "h_outsider", "statement_ar": "التقط أحد الزوار الطائرة من أرض البستان بعد هبوطها فيه.", "is_true": False, "plausibility_at_start": "medium"},
    {"id": "h_drift", "statement_ar": "انخفضت بطارية الطائرة وفُقد الاتصال بها فحملتها الرياح نحو القناة، وعرف ورد تفاصيلها من آثار ونداء عام لا من رؤيتها.", "is_true": True, "plausibility_at_start": "low", "suspect_id": "salim"},
]
mis = [
    {"id": "rh_precise", "points_to_hypothesis_id": "h_took", "planted_via_ar": "ورد قال أربع تفاصيل متتابعة بصيغة الجزم، منها الريشة التي لم يذكرها أحد غيره.",
     "evidence_ids": ["ev_warad_said", "ev_nader_statement"], "refuted_by_inference_ids": ["i_rule_took", "i_rule_took_src", "i_nader_claim", "i_src_all"],
     "fairness_note_ar": "كل تفصيل له مصدر متاح للاعب (نداء مدوّن، وأثر مصوّر، واتجاه عشب، وريشة على الشبك)، وسجلان مستقلان يضعان ورد بعيداً عن البستان وقت الانقطاع؛ وتوتر ورد في المقابلة لا يُحسب دليلاً."},
    {"id": "rh_open_gate", "points_to_hypothesis_id": "h_outsider", "planted_via_ar": "نادر يقول إن البستان مفتوح لكل زائر.",
     "evidence_ids": ["ev_nader_statement"], "refuted_by_inference_ids": ["i_orchard_claim", "i_rule_outsider_a", "i_rule_outsider_b"],
     "fairness_note_ar": "دفتر الحارس متاح ويسجّل الإقفال، وصورة العشب تظهر شريطاً بلا آثار أقدام؛ ويبقى حد الأدلة مذكوراً في قائمة الحدود: لا تنفي من يلتقط الطائرة من ضفة القناة."},
]
los = [
    {"id": "lo_obs", "statement_ar": "يفصل بين ما شاهده الشخص وما استنتجه، ويسأل عن مصدر كل تفصيل في الوصف.", "skill_ko_ref": "KO-RS-06-004", "observable_behaviors_ar": ["يصنّف إفادة ورد قولاً لا سجلاً", "يربط كل تفصيل بمصدره"], "evidence_sources": ["evidence_board", "final_justification"]},
    {"id": "lo_hyp", "statement_ar": "يولّد فرضيات متعددة ويستبعد ما تنقضه الأدلة.", "skill_ko_ref": "KO-RS-06-006", "observable_behaviors_ar": ["يضيف فرضيات", "يستبعد بدليل"], "evidence_sources": ["hypothesis_ledger"]},
    {"id": "lo_diag", "statement_ar": "يقدّر القوة التشخيصية للأثر الفئوي، ويعرف أنه لا يفرّد جسماً بعينه.", "skill_ko_ref": "KO-RS-06-001", "observable_behaviors_ar": ["يربط الدليل بالفرضية باتجاه صحيح", "يذكر حد الأثر في الحجة"], "evidence_sources": ["evidence_board", "final_justification"]},
    {"id": "lo_timeline", "statement_ar": "يرتّب سجلات الأوقات المستقلة على خط واحد ليختبر من كان حاضراً.", "skill_ko_ref": "KO-RS-05-005", "observable_behaviors_ar": ["يضع الأدلة في أزمنتها"], "evidence_sources": ["timeline_task", "action_log"]},
    {"id": "lo_calib", "statement_ar": "يصوغ نسبة الترجيح بحدودها.", "skill_ko_ref": "KO-RS-06-021", "observable_behaviors_ar": ["يختار ثقة معقولة", "يذكر حدوداً"], "evidence_sources": ["final_justification"]},
    {"id": "lo_revise", "statement_ar": "يراجع رأيه الأول حين يظهر ما يخالفه.", "skill_ko_ref": "KO-RS-06-009", "observable_behaviors_ar": ["يغيّر فرضيته الرائدة بدليل"], "evidence_sources": ["hypothesis_ledger"]},
]
def levels(d): return [{"score": i, "descriptor_ar": t} for i, t in enumerate(d)]
rub = {
    "reference_answer_ar": "لا دليل على أن ورد أخذ الطائرة. كان عند نقطة الماء الجنوبية حين انقطع اتصال الطائرة 10:12 (سجل التسليم والجدول، أو سجل اللاسلكي وصورة المصوّر)، ولكل تفصيل في وصفه مصدر آخر: النداء العام عن البطارية، وعمق الأثر الأيسر للميل، واتجاه العشب نحو القناة، والريشة على الشبك. الأرجح أن الطائرة فقدت الاتصال بعد انخفاض بطاريتها فحملتها الرياح الغربية شرقاً نحو الضفة. حدود الاستنتاج: لم يُعثر على الطائرة، والريشة لا تثبت ملامستها، ولا تنفي الأدلة أن يلتقطها أحد من جهة القناة.",
    "criteria": [
        {"id": "c_source", "name_ar": "تصنيف المصادر", "objective_ids": ["lo_obs"], "scored_by": "deterministic", "weight": 0.15, "levels": levels(["لم يصنّف", "أخطأ في الأغلب", "نصف صحيح", "معظمه صحيح", "كله صحيح"])},
        {"id": "c_conflict", "name_ar": "ترتيب الأوقات على الخط الزمني", "objective_ids": ["lo_timeline"], "scored_by": "deterministic", "weight": 0.2, "levels": levels(["لم يضع شيئاً", "وضع قليلاً", "وضع نصفها صحيحاً", "معظمها", "كلها في موضعها"])},
        {"id": "c_links", "name_ar": "ربط الأدلة بالفرضيات", "objective_ids": ["lo_diag"], "scored_by": "deterministic", "weight": 0.2, "levels": levels(["لا روابط", "قليلة", "نصفها صحيح", "معظمها", "كلها دقيقة"])},
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
    H("hg1", 1, "metacognitive", "حين يصف شخص شيئاً بدقة، اسأل: ما مصدر كل تفصيل؟ أرأى بعينه أم قرأ أثراً أم سمع من غيره؟", al, None, 0.02),
    H("hg2", 2, "focus_area", "اكتب تفاصيل وصف ورد الأربعة في عمود، وضع بجانب كل واحد ما يمكن أن يكون مصدره غير الرؤية.", he("ev_warad_said"), None, 0.04),
    H("hf1", 1, "metacognitive", "أين كان ورد حين انقطع الاتصال بالطائرة؟ وهل يوجد سجلان يخبرانك بذلك بلا علاقة بينهما؟", he("ev_nader_statement"), "i_a_far", 0.02),
    H("hf2", 2, "pointer", "قارن توقيع نقطة الماء وجدول المتطوعين بوقت الانقطاع في سجل التطبيق.", he("ev_nader_statement"), "i_a_far", 0.05),
    H("hd1", 1, "metacognitive", "ما الذي يستطيع أثر عجلتين أن يقوله عن الجسم الذي تركه، وما الذي لا يستطيع؟", he("ev_gear_photo"), "i_b_mark", 0.02),
    H("hd2", 2, "focus_area", "قارن المسافة بين الأثرين ببطاقة جرد النادي، ثم قارن عمق الأثرين.", he("ev_gear_photo"), "i_b_mark", 0.05),
    H("hd3", 1, "focus_area", "قبل أن تنسب ميل العشب إلى الريح، ابحث عن دليل يستبعد الأقدام والجزّ والعربات.", he("ev_grass_photo"), "i_b_grass", 0.06),
]
# ---------------------------------------------------------------- actions
A = []
def Act(id, typ, label, pre, effects, target=None, tel=None, cost=1):
    d = {"id": id, "type": typ, "label_ar": label, "precondition": pre, "effects": effects, "time_cost_units": cost}
    if target: d["target_id"] = target
    if tel: d["telemetry_code"] = tel
    A.append(d)
G = lambda e: {"op": "grant_evidence", "ref_id": e}
U = lambda f: {"op": "unlock_fact", "ref_id": f}
fu = lambda f: {"fact_unlocked": f}
Act("a_read_weather", "examine", "اقرأ لوحة الطقس عند مدخل المعرض", al, [G("ev_weather_board")], "loc_fair", "READ_WEATHER")
Act("a_read_announce", "examine", "اطلب ورقة نداءات المنسّق", al, [G("ev_announce_sheet")], "loc_fair", "READ_ANNOUNCE")
Act("a_read_spec", "examine", "اطلع على بطاقة جرد طائرة النادي", al, [G("ev_spec_sheet")], "obj_aircraft", "READ_SPEC")
Act("a_read_duty", "examine", "اطلب جدول متطوعي شبكة الأثر", al, [G("ev_duty_sheet")], "loc_desk", "READ_DUTY")
Act("a_read_security", "examine", "اطلب سجل جولة الأمن على بوابة البستان", al, [G("ev_security_round")], "loc_orchard", "READ_SECURITY")
Act("a_read_radio", "examine", "اطلب سجل اللاسلكي من مكتب المنسّقة", al, [G("ev_radio_log")], "loc_desk", "READ_RADIO")
Act("a_get_fair_photo", "examine", "اطلب إطار مصوّر المعرض الرسمي الأقرب إلى 10:14", al, [G("ev_fair_photo")], "loc_water", "GET_FAIR_PHOTO")
for cid, lab in [("nader", "نادر"), ("warad", "ورد"), ("salim", "سليم"), ("rami", "رامي"), ("jamil", "جميل")]:
    Act(f"a_int_{cid}", "interview", f"ابدأ مقابلة {lab}", al, [{"op": "raise_trust", "ref_id": cid, "amount": 1}], cid, f"INT_{cid.upper()}")
Act("a_get_app", "examine", "اطلب تصدير سجل رحلة التطبيق", fu("f_app_log_exists"), [G("ev_app_log")], "salim", "GET_APP")
Act("a_get_water_log", "examine", "اطلب سجل تسليم نقطة الماء", fu("f_water_log_exists"), [G("ev_water_log")], "rami", "GET_WATER_LOG")
Act("a_get_orchard_log", "examine", "اطلب دفتر حارس البستان", fu("f_orchard_log_exists"), [G("ev_orchard_log")], "jamil", "GET_ORCHARD_LOG")
Act("a_search_orchard", "search_location", "تفقّد الطرف الشرقي للبستان مع الحارس", fu("f_warad_marks_place"), [G("ev_gear_photo"), G("ev_grass_photo"), G("ev_feather_photo")], "loc_orchard", "SEARCH_ORCHARD")
Act("a_note_nader", "examine", "دوّن إفادة نادر", fu("f_salim_flew"), [G("ev_nader_statement")], "nader", "NOTE_NADER")
Act("a_note_warad", "examine", "دوّن ما قاله ورد عند المكتب", fu("f_warad_described"), [G("ev_warad_said")], "warad", "NOTE_WARAD")
Act("p_feather_warad", "present_evidence", "اعرض صورة الريشة على ورد", {"presented": {"evidence_id": "ev_feather_photo", "to_character": "warad"}}, [{"op": "emit_event", "ref_id": "PRESENTED_FEATHER"}], "warad", "P_FEATHER_WARAD", 0)
Act("p_app_salim", "present_evidence", "اعرض سجل الرحلة على سليم", {"presented": {"evidence_id": "ev_app_log", "to_character": "salim"}}, [{"op": "emit_event", "ref_id": "PRESENTED_APP"}], "salim", "P_APP_SALIM", 0)
Act("p_orchard_nader", "present_evidence", "اعرض دفتر الحارس على نادر", {"presented": {"evidence_id": "ev_orchard_log", "to_character": "nader"}}, [{"op": "emit_event", "ref_id": "PRESENTED_ORCHARD"}], "nader", "P_ORCHARD_NADER", 0)
Act("a_hint", "request_hint", "اطلب تلميحاً", al, [], None, "REQUEST_HINT", 0)
Act("a_accuse", "final_accusation", "قدّم الاستنتاج النهائي", al, [{"op": "emit_event", "ref_id": "SUBMIT"}], None, "FINAL_ACCUSATION", 0)

topics = [
    {"id": "t_nader", "label_ar": "الطيران واتهام ورد", "example_questions_ar": ["من كان يطيّر الطائرة؟", "لماذا تظن أن ورد أخذها؟"], "fact_ids": ["f_salim_flew"], "claim_ids": ["cl_nader_witness", "cl_orchard_open"]},
    {"id": "t_post", "label_ar": "أين كنت صباح الافتتاح؟", "example_questions_ar": ["أين كنت وقت اختفاء الطائرة؟", "ما طريقك إلى مكتب المنسّقة؟"], "fact_ids": ["f_warad_post", "f_warad_route"]},
    {"id": "t_marks", "label_ar": "العلامات على الأرض", "example_questions_ar": ["ماذا رأيت في البستان؟", "هل علقت بالطائرة ريشة حقاً؟"], "fact_ids": ["f_warad_marks_place", "f_warad_admits"], "claim_ids": ["cl_warad_feather"]},
    {"id": "t_flight", "label_ar": "الرحلة والعودة", "example_questions_ar": ["كيف بدأت الرحلة؟", "ماذا رأيت قبل انقطاع الاتصال؟", "هل يحفظ التطبيق سجلاً؟"], "fact_ids": ["f_app_log_exists", "f_announce_asked", "f_salim_saw_east", "f_start_battery"]},
    {"id": "t_water", "label_ar": "نقطة الماء", "example_questions_ar": ["من وقّع عندك صباح الافتتاح؟", "هل لديكم سجل تسليم؟"], "fact_ids": ["f_water_log_exists", "f_warad_post"]},
    {"id": "t_orchard", "label_ar": "بوابة البستان", "example_questions_ar": ["هل دخل أحد البستان؟", "هل لديك دفتر يومي؟"], "fact_ids": ["f_orchard_log_exists", "f_orchard_closed"]},
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
    (1, "ورد وقّع عند نقطة الماء 10:05 و10:40، وجدول المتطوعين يضع مناوبته هناك، على بعد نحو 600 م من البستان وقت انقطاع الاتصال.", ["ev_water_log", "ev_duty_sheet"], "i_a_far"),
    (2, "مسار مستقل يؤدي إلى النتيجة نفسها: نداء ورد اللاسلكي 10:13 وصورة المصوّر 10:14 عند الطاولة ذاتها بسترة رقم 27.", ["ev_fair_photo", "ev_radio_log"], "i_b_far"),
    (3, "سجل التطبيق يضع آخر موضع للطائرة فوق طرف البستان متجهة شرقاً، ولوحة الطقس تسجّل رياحاً غربية متصاعدة: الأرجح أنها انجرفت نحو الضفة.", ["ev_app_log", "ev_weather_board"], "i_a_drift"),
    (4, "مسار الآثار يوافقه: أثر العجلتين بالمسافة المعروفة وعمق أيسر أكبر، ثم ميل العشب بالريح نحو القناة بعد أن استُبعد المشي والجزّ والعربات.", ["ev_gear_photo", "ev_spec_sheet", "ev_grass_photo", "ev_orchard_log"], "i_b_drift"),
    (5, "الآن يظهر مصدر كل تفصيل في وصف ورد: نداء البطارية، وعمق الأثر الأيسر، واتجاه العشب نحو الماء، وريشة وجدت على الشبك لا على الطائرة.", ["ev_announce_sheet", "ev_gear_photo", "ev_grass_photo", "ev_feather_photo"], "i_src_all"),
    (6, "إذن لا تدل دقة الوصف على أن صاحبه حمل الطائرة: لم يكن حاضراً عند هبوطها، وما قاله استنتاج قرأه من الأرض ومن نداء سمعه الجميع.", ["ev_water_log", "ev_duty_sheet"], "i_rule_took"),
    (7, "ولا أثر لزائر اقترب من موضع الملامسة: بوابة البستان مقفلة في سجلين مستقلين، وشريط العشب بلا أقدام.", ["ev_security_round", "ev_orchard_log", "ev_grass_photo"], "i_rule_outsider_a"),
]
ending = {
    "steps": [{"order": o, "text_ar": t, "uses_evidence_ids": u, "inference_id": i} for o, t, u, i in steps],
    "alternative_paths_ar": [
        "يمكن بلوغ النتيجة من السجلات وحدها: سجل التطبيق ولوحة الطقس للاتجاه، وسجل نقطة الماء وجدول المتطوعين لغياب ورد.",
        "ويمكن بلوغها من الآثار والصورة والسجل اللاسلكي وحدها، دون سجل التطبيق؛ والأقوى أن يتفق المساران.",
    ],
    "what_evidence_could_not_show_ar": [
        "لم يُعثر على الطائرة؛ الأدلة ترجّح اتجاهها ولا تثبت موضعها الآن.",
        "الريشة على الشبك لا تثبت أنها لامست الطائرة، ولا تنفي الأدلة أن يلتقطها أحد من جهة القناة بعد وصولها.",
        "لا تبيّن الأدلة لماذا قال ورد ما قاله بصيغة الجزم.",
    ],
    "science_notes_ar": [
        "أثر العجلتين خاصية فئوية: يدل على نوع الجسم الذي لامس التربة (مسافة وقطر وعمق) ولا يفرّد جسماً بعينه، ولا يحدد وقت الملامسة.",
        "الفصل بين الملاحظة والاستنتاج: وصف دقيق لا يعني أن صاحبه رأى. اسأل دائماً من أين جاء كل تفصيل، ثم قارنه بسجل.",
        "سجل رحلة التطبيق نسخة مصدَّرة من هاتف؛ يبقى الحفاظ على سلسلة العهدة من الهاتف إلى المحقق شرطاً لوزنه.",
        "تختم القضية بمساءلة مؤسسية لا بتشهير: يعتذر النادي لورد، ويعتمد قائمة فحص للبطارية قبل كل إقلاع، ويبلّغ إدارة المعرض للبحث عند الضفة.",
        "ما نسميه نسبة الترجيح حكم مبني على سجلات يمكن تتبّعها، وليس ثقة بمجرد أن الوصف دقيق.",
    ],
}
core = {
    "schema_version": "0.1.0", "case_id": CID, "case_version": "0.1.0",
    "meta": {"title_ar": "الطائرة التي لم يرها أحد", "title_en": "The Aircraft Nobody Saw", "age_band": "13-15", "locale": "ar", "dialogue_register": "msa", "estimated_minutes": 28, "difficulty": 2,
             "content_flags": ["no_violence"], "authors": ["فريق أثر التحريري (مسودة بمساعدة الذكاء الاصطناعي، عن بذرة من قضايا التراث، لم تُراجَع بشرياً بعد)"],
             "knowledge_object_refs": ["KO-RS-06-004", "KO-RS-06-006", "KO-RS-06-001", "KO-RS-05-005", "KO-RS-05-007", "KO-RS-06-009", "KO-RS-06-021", "KO-FC-04-015", "KO-FC-04-024", "KO-NP-02H-001"]},
    "premise": {"hook_ar": "طائرة صغيرة تضيع يوم الافتتاح، وطالب يصفها وصفاً لم يسمعه أحد قبله. هل يكفي أن تكون دقيقاً لتكون قد رأيت؟",
                "player_role_ar": "أنت مراجع في لجنة معرض القافلة، وطُلب منك أن تحسم كيف عرف ورد تفاصيل الطائرة قبل أن يُحرم من المعرض.",
                "setting_ar": "معرض القافلة وبستانه المجاور، صباح يوم الافتتاح. كل الأوقات بساعة المعرض وفرق الدقيقة تُذكر عند الحاجة.",
                "public_fact_ids": ["f_aircraft_missing", "f_nader_accuses", "f_warad_described"],
                "assumed_general_knowledge_ar": ["الريح تحمل الأجسام الخفيفة في اتجاه هبوبها", "ما يُعلن بمكبّر الصوت يسمعه كل من في المعرض"]},
    "entities": {"characters": chars, "locations": locations, "objects": objects, "organizations": orgs},
    "truth": {"solution": {"culprit_ids": ["salim"], "summary_ar": "لم تُؤخذ الطائرة. أقلعت ببطارية لم يكتمل شحنها، فانخفضت وانقطع الاتصال بها فوق طرف البستان، ثم دفعتها الرياح الغربية نحو القناة. ورد لم يرَها: كان بعيداً عند نقطة الماء، وأخذ تفاصيل وصفه من نداء عام ومن آثار في الأرض مرّ بها بعد ذلك.", "key_fact_ids": ["f_drifted_east", "f_warad_far"]},
              "facts": facts, "claims": claims},
    "timeline": timeline, "evidence": ev, "evidence_graph": {"inferences": inf},
    "character_knowledge": ck, "hypotheses": hyps, "misdirection_plan": mis, "learning_objectives": los,
    "mechanics": {"time_budget_units": 40, "actions": A},
    "state_machine": {"id": "c011", "initial": "briefing", "type": "compound", "states": {
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
    "clock": {"epoch_hhmm": "10:00", "zone_label_ar": "ساعة المعرض"},
    "cover": {"title_ar": "الطائرة التي لم يرها أحد", "tagline_ar": "وصفٌ دقيق، ومتّهم لم يرَ شيئاً… فمن أين جاءت التفاصيل؟", "kicker_ar": "الملف الحادي عشر · قراءة الأثر", "glyph": "✈", "accent": "green"},
    "cold_open_ar": ["الجمعة، افتتاح معرض القافلة.", "اختفت طائرة التصوير الصغيرة التابعة للنادي، وصاحبها واثق من أن ورد أخذها لأنه وصفها كأنه حملها.",
                     "ورد يقول إنه لم يأخذ شيئاً. وبين يديك أوراق وسجلات وصور لأرض البستان.",
                     "ابدأ بسؤال واحد: من أين جاء كل تفصيل في الوصف؟"],
    "labs": [],
    "source_classes": [
        {"id": "primary_record", "label_ar": "سجل أصلي", "help_ar": "يُنتجه نظام أو شخص لحظة الحدث دون وسيط، كسجل تطبيق أو دفتر حارس أو صورة بمسطرة."},
        {"id": "redisplay", "label_ar": "نسخة معروضة", "help_ar": "معلومة أُعيد عرضها أو نُقلت من مصدر آخر."},
        {"id": "claim", "label_ar": "قول أو تصريح", "help_ar": "إفادة شخص؛ تُقاس بالسجلات والآثار لا بنبرة صاحبها ولا بدقة وصفه."},
        {"id": "template", "label_ar": "قالب أو نموذج", "help_ar": "نص جاهز لا يصف الحدث الفعلي بذاته."},
        {"id": "public_document", "label_ar": "وثيقة منشورة", "help_ar": "وثيقة معلنة ومعروف ناشرها، كلوحة الطقس أو ورقة النداءات أو بطاقة الجرد."}],
    "limit_menu": [
        {"id": "l_not_found", "label_ar": "لم يُعثر على الطائرة: الأدلة ترجّح اتجاهها ولا تثبت موضعها"},
        {"id": "l_feather", "label_ar": "الريشة على الشبك لا تثبت أنها لامست الطائرة"},
        {"id": "l_canal_side", "label_ar": "لا تنفي الأدلة أن يلتقط أحد الطائرة من جهة القناة بعد وصولها"},
        {"id": "l_invalid_tension", "label_ar": "توتر ورد في المقابلة يدل على أنه يخفي شيئاً"},
        {"id": "l_invalid_detail", "label_ar": "دقة وصف ورد تثبت أنه رأى الطائرة"}],
    "mind_change_menu": [
        {"id": "m_elsewhere", "label_ar": "العثور على الطائرة في موضع يخالف اتجاه الريح"},
        {"id": "m_leave_post", "label_ar": "ظهور دليل مستقل بأن ورد غادر نقطة الماء قبل 10:12"},
        {"id": "m_gate_open", "label_ar": "ثبوت أن بوابة البستان فُتحت قبل الحادية عشرة"},
        {"id": "m_popular", "label_ar": "كثرة من يظنون أن ورد هو الفاعل"}],
    "skills": [{"skill_id": "KO-RS-06-004", "track": "B"}, {"skill_id": "KO-RS-06-006", "track": "D"}, {"skill_id": "KO-FC-04-015", "track": "E"}],
    "stage_hooks_ar": {"briefing": "وصفٌ بالغ الدقة… فهل صاحبه رأى أم قرأ؟", "investigating": "كل تفصيل في الوصف يحتاج إلى مصدر.", "review": "قبل أن تغلق الملف: ما الذي لا تعرفه عن الطائرة؟", "resolved": "أُغلق الملف. في الأرشيف بقية الأوراق."},
    "character_glyphs": {"nader": "ن", "warad": "و", "salim": "س", "rami": "ر", "jamil": "ج"},
}
sc = {
    "case_id": CID,
    "accepted_conclusions": {"h_drift": {"grade": 1, "note_ar": "استنتاج متسق مع الأدلة ويتطلب ذكر حدوده."},
                             "h_took": {"grade": 0, "note_ar": "يعدّ دقة الوصف دليل رؤية أو حمل، ويتجاهل أن لكل تفصيل مصدراً وأن ورد كان بعيداً."},
                             "h_outsider": {"grade": 0, "note_ar": "يتجاهل إقفال البوابة وخلوّ شريط العشب من آثار الأقدام."}},
    "confidence_band": {"h_drift": [60, 88], "h_took": [0, 15], "h_outsider": [0, 20]},
    "source_key": {"ev_app_log": "primary_record", "ev_weather_board": "public_document", "ev_announce_sheet": "public_document", "ev_spec_sheet": "public_document",
                   "ev_gear_photo": "primary_record", "ev_grass_photo": "primary_record", "ev_feather_photo": "primary_record", "ev_orchard_log": "primary_record",
                   "ev_water_log": "primary_record", "ev_duty_sheet": "primary_record", "ev_fair_photo": "primary_record", "ev_radio_log": "primary_record",
                   "ev_nader_statement": "claim", "ev_warad_said": "claim", "ev_security_round": "primary_record"},
    "link_key": {
        "h_drift": {"ev_app_log": "supports", "ev_weather_board": "supports", "ev_gear_photo": "supports", "ev_grass_photo": "supports", "ev_spec_sheet": "supports", "ev_orchard_log": "supports", "ev_announce_sheet": "supports", "ev_water_log": "supports", "ev_feather_photo": "neutral"},
        "h_took": {"ev_water_log": "weakens", "ev_duty_sheet": "weakens", "ev_fair_photo": "weakens", "ev_radio_log": "weakens", "ev_announce_sheet": "weakens", "ev_gear_photo": "weakens", "ev_warad_said": "neutral"},
        "h_outsider": {"ev_orchard_log": "weakens", "ev_security_round": "weakens", "ev_grass_photo": "weakens", "ev_nader_statement": "neutral"},
    },
    "required_limits": ["l_not_found", "l_feather"], "valid_mind_changers": ["m_elsewhere", "m_leave_post", "m_gate_open"],
    "invalid_limits": ["l_invalid_tension", "l_invalid_detail"],
    "decisive_evidence": ["ev_app_log", "ev_weather_board", "ev_water_log", "ev_duty_sheet", "ev_gear_photo", "ev_announce_sheet"],
    "lab_requirement": None,
    "timeline_requirement": [{"evidence_id": "ev_announce_sheet", "utc_minute": 9, "tol": 3}, {"evidence_id": "ev_app_log", "utc_minute": 12, "tol": 3}, {"evidence_id": "ev_radio_log", "utc_minute": 13, "tol": 3}, {"evidence_id": "ev_fair_photo", "utc_minute": 14, "tol": 3}],
    "refuted_hypotheses": ["h_took", "h_outsider"],
    "criteria_map": {"c_source": "source_typing", "c_conflict": "conflict_resolution", "c_links": "hypothesis_links", "c_uncertainty": "uncertainty", "c_revision": "revision", "c_elimination": "elimination", "c_justification": "justification_human"},
    "caps": {"no_citations_max": 45, "no_conflict_resolution_max": 65},
}
os.makedirs(OUT, exist_ok=True)
for suf, obj in [("", core), (".ui", ui), (".scoring", sc)]:
    with open(os.path.join(OUT, f"{CID}{suf}.json"), "w", encoding="utf8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
print("ok")
