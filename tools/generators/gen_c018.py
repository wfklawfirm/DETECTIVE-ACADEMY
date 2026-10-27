#!/usr/bin/env python3
# Case c018 «الضوء في مرآة المرصد» — seed S-09 (age band 13-15). Teaches: change ONE factor at a time and repeat the observation before you
# trust a result; a test that could have failed (the blocked tube) is worth more than one that only confirms; and accepting two accurate posts
# about the observatory is part of sound doubt (do not doubt everything). The ratio of accurate documents in the case is well above 40%.
# Mechanic note: the engine has no measuring-instrument simulator, so each experiment run is a player-visible request action (request_lab_test)
# that grants a run-record evidence item, as c009 did for its passage comparison; the records state what was changed, what was held, and how
# many times the run was repeated. No-culprit convention: the restaurant manager who (innocently) lit a glass facade is recorded in culprit_ids.
# All people, places, institutions and documents are fictional. Usage: gen_c018.py OUT_DIR
import json, sys, os
OUT = sys.argv[1]
CID = "c018_blocked_tube"

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
ch("yazan", "يزن العبدالله", "witness", "طالب في الصف التاسع، يهوى الفلك ونشر مقاطعه",
   "متحمس وصادق، يصدّق ما يصوّره بعينيه، ويتراجع بلا حرج إذا أراه أحد تجربة مضبوطة.",
   ["أن يكون مقطعه اكتشافاً", "ألا يُتّهم بالتزييف"],
   [L("yz_greet", "greeting", "هل رأيت المقطع؟ ضوء غريب في المرآة، وفي الليالي الصافية فقط!"),
    L("yz_claim", "reveal", "صوّرت اللقطتين بهاتفي المثبّت على العينية، الأولى عند الثامنة والعاشرة والثانية عند العاشرة وأربعين دقيقة، والضوء في الموضع نفسه، بينما النجوم تتحرك.", ["f_clip_frames"], ["cl_yazan_mystery"]),
    L("yz_unknown", "deflect_unknown", "لا أعرف، لم أفكر بهذا."),
    L("yz_off", "deflect_offtopic", "اسألني عن المقطع نفسه."),
    L("yz_bye", "farewell", "إن ثبت أنني مخطئ فسأنشر التصحيح بنفسي.")])
ch("hisham", "هشام القاسم", "witness", "مشرف الرصد الليلي في مرصد الأطلال",
   "هادئ ودقيق، يدوّن كل ليلة في سجله ما رآه، ويكره التخمين فوق السجل.",
   ["أن يبقى سجل الرصد سليماً", "ألا يُنسب إلى المرصد ما لم يثبت"],
   [L("hs_greet", "greeting", "أهلاً. سجل الرصد أمامي، وما فيه هو ما أستطيع قوله."),
    L("hs_log", "reveal", "أدوّن كل ليلة رصد في سجل، وفيه حالة السماء وما لاحظناه في الصورة.", ["f_log_exists"]),
    L("hs_posts", "reveal", "نشر المرصد بيانين: أحدهما عن إغلاق القبة في الليالي الغائمة، والآخر عن إعادة تلبيس المرآة.", ["f_posts_exist"]),
    L("hs_map", "reveal", "عندنا مخطط الموقع الذي يبين اتجاه المنافذ الجانبية للأنبوب ومباني المدينة المقابلة.", ["f_map_exists"]),
    L("hs_unknown", "deflect_unknown", "ليس في سجلي شيء عن هذا."),
    L("hs_off", "deflect_offtopic", "اسألني عن الرصد وسجلاته."),
    L("hs_bye", "farewell", "السجل يتكلم قبلي.")])
ch("lina", "لينا الحاج", "expert", "فنية في مختبر «المنظار» للمحاكاة",
   "صبورة وتحب أن تغيّر شيئاً واحداً في كل مرة، وتقول دائماً إن المحاكاة تنبّه ولا تحكم.",
   ["أن تُجرى التجربة بعامل واحد متغيّر", "ألا يُبالغ في ما تثبته المحاكاة"],
   [L("ln_greet", "greeting", "تفضّل إلى المنظار. عندنا نموذج مصغّر للمرصد."),
    L("ln_sim", "reveal", "يمكنني تشغيل النموذج: أنبوب ومرآة ومنفذان جانبيان، ومصدر ضوء على سكة، وأكرر كل حالة مرتين على الأقل.", ["f_sim_available"]),
    L("ln_unknown", "deflect_unknown", "المحاكاة لا تجيب عن هذا."),
    L("ln_off", "deflect_offtopic", "اسألني عن النموذج وكيف يُشغَّل."),
    L("ln_bye", "farewell", "غيّر عاملاً واحداً ثم كرّر.")])
ch("jamil", "جميل الراشد", "suspect", "مدير مطعم «الشرفة» قرب المرصد",
   "ودود ومشغول، يخاف أن يُلام على إزعاج الجيران، ويظن أن إضاءة مطعمه لا تصل بعيداً.",
   ["ألا يُنسب إلى مطعمه ضرر", "أن يعرف الحقيقة إن كانت إضاءته السبب"],
   [L("jm_greet", "greeting", "أهلاً. إن كنت تسأل عن إضاءة الواجهة فقد ركبناها لتجذب الزبائن، لا لتزعج أحداً."),
    L("jm_claim", "reveal", "مطعمي بعيد، فلا أظن أن ضوءه يصل إلى المرصد.", None, ["cl_jamil_far"]),
    L("jm_refuse", "refuse_secret", "لا أريد الحديث عن أوراق الواجهة."),
    L("jm_permit", "reveal", "نعم... ركّبنا واجهة زجاجية مضاءة قبل خمسة عشر يوماً، وتعمل بمؤقت من السابعة وخمسين دقيقة مساءً حتى الحادية عشرة وربع. ورخصة التركيب عندي.", ["f_permit_exists"]),
    L("jm_unknown", "deflect_unknown", "لا أعرف."),
    L("jm_off", "deflect_offtopic", "اسألني عن المطعم وإضاءته."),
    L("jm_bye", "farewell", "إن كان ضوئي السبب فسأعدّله.")])

locations = [{"id": "loc_obs", "name_ar": "مرصد الأطلال", "description_ar": "القبة والمرآة وسجل الرصد."},
             {"id": "loc_lab", "name_ar": "مختبر المنظار", "description_ar": "نموذج المحاكاة والتجارب المكررة."},
             {"id": "loc_resto", "name_ar": "مطعم الشرفة", "description_ar": "مطعم جديد الواجهة في الجهة الغربية من المدينة."},
             {"id": "loc_web", "name_ar": "منصة المقاطع", "description_ar": "حيث نُشر المقطع وانتشر."}]
objects = [{"id": "obj_clip", "name_ar": "المقطع المنتشر", "description_ar": "مقطع قصير يُظهر بقعة ضوء في صورة مرآة المرصد."},
           {"id": "obj_mirror", "name_ar": "مرآة المرصد", "description_ar": "المرآة الكبيرة في أنبوب المقراب."}]
orgs = [{"id": "org_obs", "name_ar": "مرصد الأطلال", "description_ar": "مرصد خيالي يفتح للجمهور ليالي محددة."}]

# ---------------------------------------------------------------- facts
facts = []
def F(id, st, kind, subj, spoiler, time=None, loc=None, ko=None):
    d = {"id": id, "statement_ar": st, "kind": kind, "subject_ids": subj, "spoiler_level": spoiler}
    if time: d["time"] = time
    if loc: d["location_id"] = loc
    if ko: d["science_ko_refs"] = ko
    facts.append(d)
F("f_clip_viral", "انتشر مقطع يزعم أن مرآة المرصد تُظهر «ضوءاً غامضاً» في الليالي الصافية.", "event", ["obj_clip", "obj_mirror"], 0)
F("f_yazan_filmed", "صوّر يزن المقطع بهاتف مثبّت على عينية المقراب ونشره.", "event", ["yazan", "obj_clip"], 0)
F("f_posts_circulate", "تتداول المنصة منشورين عن المرصد: أحدهما عن إغلاق القبة في الليالي الغائمة والآخر عن إعادة تلبيس المرآة.", "state", ["org_obs"], 0)
F("f_clip_frames", "اللقطتان 20:10 و22:40 تُظهران بقعة الضوء في الموضع نفسه من الصورة بينما تنتقل النجوم عبرها.", "event", ["yazan", "obj_clip"], 1, T(130, "exact", 280), "loc_web")
F("f_log_exists", "للمرصد سجل رصد ليلي يدوّن حالة السماء وما لوحظ في الصورة.", "state", ["hisham", "loc_obs"], 1)
F("f_posts_exist", "نشر المرصد بيانين رسميين يمكن الرجوع إليهما.", "state", ["org_obs"], 1)
F("f_map_exists", "للمرصد مخطط موقع يبيّن اتجاهات المنفذين الجانبيين وما يقابلهما من مبانٍ.", "state", ["loc_obs"], 1)
F("f_sim_available", "في مختبر المنظار نموذج محاكاة مصغّر يتيح تغيير عامل واحد وتكرار كل حالة.", "state", ["lina", "loc_lab"], 1)
F("f_permit_exists", "لدى مدير المطعم رخصة تركيب واجهته المضاءة.", "state", ["jamil", "loc_resto"], 1)
F("f_cloudy_closed", "تُغلق القبة في الليالي الغائمة فلا يسجَّل فيها رصد، فلا تُحصى ليلة غائمة بين ليالي ظهور الضوء.", "relation", ["org_obs", "obj_clip"], 1)
F("f_recoat_before", "أُعيد تلبيس المرآة قبل ستة أسابيع، ومرت اثنتان وعشرون ليلة رصد صافية بعدها دون أي بقعة ضوء.", "relation", ["obj_mirror", "hisham"], 2, None, "loc_obs")
F("f_lights_installed", "ركّب المطعم واجهة زجاجية مضاءة قبل خمسة عشر يوماً، وتُضاء من 19:50 إلى 23:15 كل ليلة.", "state", ["jamil", "loc_resto"], 1, T(110, "exact", 315), "loc_resto")
F("f_terrestrial_source", "مصدر الضوء أرضي يدخل من المنفذ الجانبي المواجه للمدينة، لا من السماء ولا من عيب في المرآة.", "relation", ["obj_clip", "obj_mirror"], 3, None, None, ["KO-RS-06-008", "KO-RS-06-015"])
F("f_source_is_facade", "مصدر البقعة هو انعكاس واجهة المطعم الزجاجية المضاءة حديثاً.", "relation", ["obj_clip", "jamil", "loc_resto"], 3, T(130, "exact", 315), "loc_resto", ["KO-RS-06-015", "KO-RS-06-005"])
claims = [
    {"id": "cl_yazan_mystery", "statement_ar": "الضوء يظهر في الليالي الصافية وحدها، فلا تفسير أرضياً له.", "kind": "honest_mistake", "held_by": ["yazan"], "true_fact_id": "f_cloudy_closed", "contradicted_by_evidence_ids": ["ev_post_cloudy", "ev_obs_log", "ev_run_move"]},
    {"id": "cl_jamil_far", "statement_ar": "مطعمي بعيد، فلا يصل ضوء واجهته إلى المرصد.", "kind": "honest_mistake", "held_by": ["jamil"], "true_fact_id": "f_source_is_facade", "contradicted_by_evidence_ids": ["ev_site_map", "ev_run_baseline"]},
]
timeline = [
    {"id": "te_lights_on", "description_ar": "مؤقت الواجهة يضيء زجاج المطعم.", "time": T(110), "location_id": "loc_resto", "actor_ids": ["jamil"], "fact_ids": ["f_lights_installed"], "motivated_by_ar": "ضبط المؤقت ليجذب الزبائن مساءً"},
    {"id": "te_spot_on", "description_ar": "اللقطة الأولى في المقطع تُظهر البقعة.", "time": T(130), "location_id": "loc_obs", "actor_ids": ["yazan"], "fact_ids": ["f_clip_frames"], "motivated_by_ar": "صوّر الصورة عبر العينية في ليلة صافية"},
    {"id": "te_spot_late", "description_ar": "اللقطة الثانية تُظهر البقعة في الموضع نفسه والنجوم تحرّكت.", "time": T(280), "location_id": "loc_obs", "actor_ids": ["yazan"], "fact_ids": ["f_clip_frames"], "motivated_by_ar": "أكمل التصوير ليرى إن كان الضوء يتحرك"},
    {"id": "te_lights_off", "description_ar": "يطفئ المؤقت واجهة المطعم عند الإغلاق.", "time": T(315), "location_id": "loc_resto", "actor_ids": ["jamil"], "fact_ids": ["f_lights_installed"], "motivated_by_ar": "إغلاق المطعم آخر الليل"},
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
V("ev_clip", "المقطع المنتشر عن مرآة المرصد", "digital",
  "مقطع مدته 41 ثانية، التعليق: «ضوء غامض يظهر في مرآة المرصد في الليالي الصافية!»\nاللقطة الأولى (20:10): بقعة ضوء بيضاء في الربع السفلي الأيسر من الصورة.\nاللقطة الثانية (22:40): البقعة في الموضع نفسه، وقد انتقلت النجوم عن مواضعها.\nلا يذكر المقطع تاريخ التصوير ولا أي ليلة أخرى.",
  ["a_get_clip"], ["f_clip_frames"], "moderate",
  "يعرض ما التقطته كاميرا واحدة في ليلة واحدة؛ العنوان استنتاج صاحب المقطع لا وصف للصورة.", red=True, loc="loc_web")
V("ev_obs_log", "سجل الرصد الليلي للمرصد", "documentary",
  "مرصد الأطلال — سجل الرصد (اختصار)\nقبل 15 يوماً وما سبقها: 22 ليلة رصد صافية، لا بقعة ضوء في أي منها.\nمنذ الليلة التالية لقبل 15 يوماً: 9 ليالٍ صافية رُصدت، وفي كل منها بقعة ضوء في الموضع نفسه من الصورة (بكسل 412 × 880)، تظهر نحو 20:10 وتختفي نحو 23:15.\n5 ليالٍ غائمة: القبة مغلقة، لا رصد.\nمواضع النجوم في الصورة تنتقل من ليلة إلى أخرى ومن ساعة إلى أخرى، أما البقعة فلا تنتقل.\nالبقعة ظهرت في كاميرا المرصد الرسمية وفي هاتف زائر ثانٍ، لا في هاتف واحد فقط.",
  ["a_get_log"], ["f_clip_frames", "f_recoat_before", "f_cloudy_closed"], "strong",
  "سجل يدوي لمشرف واحد؛ يبيّن متى ظهرت البقعة ولا يبيّن مصدرها، ويكتب «صافية» بتقدير الراصد.", ko="KO-RS-06-005", loc="loc_obs")
V("ev_post_cloudy", "بيان المرصد: القبة مغلقة في الليالي الغائمة", "documentary",
  "بيان رسمي منشور من مرصد الأطلال\n«نغلق القبة في الليالي الغائمة ولا نسجّل رصداً فيها. وتقتصر أمسيات الجمهور على الليالي الصافية.»",
  ["a_get_posts"], ["f_cloudy_closed"], "strong",
  "بيان صحيح ومعلن من الجهة نفسها؛ يفسر لماذا لا تُسجَّل البقعة في الليالي الغائمة، ولا يتناول مصدر البقعة.", loc="loc_obs")
V("ev_post_recoat", "بيان المرصد: إعادة تلبيس المرآة", "documentary",
  "بيان رسمي منشور من مرصد الأطلال\n«أُعيد تلبيس المرآة الرئيسة قبل ستة أسابيع بطبقة جديدة، وهي تعكس الضوء أفضل من قبل.»",
  ["a_get_posts"], ["f_recoat_before"], "strong",
  "بيان صحيح عن واقعة حقيقية؛ لا يقول إن لها أثراً في البقعة، ويُقاس أثرها بالسجل.", red=True, loc="loc_obs")
V("ev_site_map", "مخطط موقع المرصد", "documentary",
  "مخطط موقع مرصد الأطلال (مقياس مبسّط)\nالمنفذ الجانبي (أ): يواجه الاتجاه 245° (جهة المدينة).\nالمنفذ الجانبي (ب): يواجه الشمال 000°.\nعلى بعد 400 م في الاتجاه 247°: مطعم الشرفة، واجهته زجاجية مواجهة للمرصد.\nعلى بعد 900 م في الاتجاه 000°: برج مياه بلا إضاءة.",
  ["a_get_map"], ["f_terrestrial_source"], "strong",
  "مخطط من المرصد؛ يبيّن الاتجاهات والمسافات، لا يبيّن أن الضوء دخل من منفذ بعينه فعلاً.", contradicts=["cl_jamil_far"], loc="loc_obs")
V("ev_restaurant_permit", "رخصة تركيب واجهة مطعم الشرفة", "documentary",
  "رخصة تركيب واجهة زجاجية مضاءة — بلدية الأطلال\nالمنشأة: مطعم الشرفة\nتاريخ التركيب: قبل 15 يوماً\nتشغيل الإضاءة بمؤقت: من 19:50 حتى 23:15 يومياً\nالمدير: جميل الراشد",
  ["a_get_permit"], ["f_lights_installed"], "strong",
  "وثيقة بلدية تثبت تاريخ التركيب وساعات التشغيل؛ لا تثبت أن ضوء الواجهة يصل إلى المرصد.", loc="loc_resto")
V("ev_run_baseline", "تجربة المحاكاة: الحالة الأساسية", "lab_result",
  "مختبر المنظار — نموذج مصغّر للمرصد (محاكاة، لا مرصد حقيقي)\nالعامل المتغيّر: مصدر الضوء فقط، وكل ما عداه ثابت.\nالحالة 1: المصدر مطفأ — المحاولة الأولى: لا بقعة؛ الثانية: لا بقعة.\nالحالة 2: المصدر مضاء عند الاتجاه 247° وارتفاع منخفض — الأولى: بقعة بيضاء في الربع السفلي الأيسر؛ الثانية: البقعة في الموضع نفسه.\nالنجم الصناعي يدور في الحالتين والبقعة لا تدور معه.",
  ["a_run_baseline"], ["f_terrestrial_source"], "strong",
  "نموذج مصغّر لا يطابق المرصد في كل تفصيل؛ كل حالة مكررة مرتين فقط، فالنتيجة تنبيه إلى تفسير محتمل لا برهان عليه وحده.", ko="KO-RS-06-008", loc="loc_lab")
V("ev_run_shield", "تجربة المحاكاة: سد المنفذ المواجه للمدينة", "lab_result",
  "مختبر المنظار — محاكاة\nالعامل المتغيّر: غطاء على المنفذ الجانبي (أ) فقط، والمصدر مضاء عند 247° في الحالات كلها.\nالحالة 1: الغطاء موضوع — الأولى: لا بقعة؛ الثانية: لا بقعة.\nالحالة 2: الغطاء مرفوع — الأولى: بقعة؛ الثانية: بقعة في الموضع نفسه.\nالغطاء على المنفذ (ب) وحده لا يغيّر شيئاً (مرتان).",
  ["a_run_shield"], ["f_terrestrial_source"], "strong",
  "اختبار كان يمكن أن يفشل ولم يفشل؛ لكنه جرى في نموذج، وبعدد محاولات قليل، ولا يثبت أن المنفذ (أ) في المرصد هو ما دخل منه الضوء ليلة التصوير.", ko="KO-RS-06-008", loc="loc_lab")
V("ev_run_lens", "تجربة المحاكاة: تبديل الكاميرا والغطاء", "lab_result",
  "مختبر المنظار — محاكاة\nالعامل المتغيّر: الكاميرا فقط (كاميرا ثانية بغطاء عدسة واقٍ)، والمصدر مضاء عند 247°.\nالأولى: البقعة موجودة في الموضع نفسه.\nالثانية: البقعة موجودة في الموضع نفسه.",
  ["a_run_lens"], ["f_terrestrial_source"], "moderate",
  "ينفي أن البقعة من عدسة كاميرا بعينها في النموذج؛ لا ينفي خللاً في هاتف يزن نفسه.", ko="KO-RS-06-008", loc="loc_lab")
V("ev_run_move", "تجربة المحاكاة: تحريك مصدر الضوء على السكة", "lab_result",
  "مختبر المنظار — محاكاة\nالعامل المتغيّر: موضع المصدر على السكة فقط، والغطاء مرفوع.\n247° (موضع واجهة المطعم): بقعة في الربع السفلي الأيسر — مرتان.\n227°: البقعة تنزاح إلى الأعلى وتخفت — مرتان.\n000° (جهة برج الماء) والمصدر في السماء فوق الأنبوب: لا بقعة — مرتان لكل موضع.\nالنجم الصناعي لا يتأثر بتحريك المصدر.",
  ["a_run_move"], ["f_source_is_facade"], "strong",
  "تبيّن أن البقعة تتبع اتجاه المصدر الأرضي في النموذج؛ لا تحدد أي مبنى بعينه في الواقع إلا بربطها بالمخطط والسجلات.", contradicts=["cl_yazan_mystery"], ko="KO-RS-06-008", loc="loc_lab")
V("ev_yazan_statement", "إفادة يزن العبدالله (ملخص)", "testimonial",
  "ملخص إفادة يزن العبدالله:\n«صورت اللقطتين بهاتفي على العينية في ليلة صافية. ظننت أن الضوء من السماء لأنني لا أراه في الليالي الغائمة.»",
  ["a_note_yazan"], ["f_clip_frames"], "weak",
  "إفادة صاحب المقطع؛ تصف ما صوّره وتضيف استنتاجه، ولا تقيس غياب الضوء في ليالٍ كان المرصد فيها مغلقاً.", loc="loc_web")
V("ev_hisham_statement", "إفادة هشام القاسم (ملخص)", "testimonial",
  "ملخص إفادة هشام القاسم:\n«كل ما لاحظته مدوّن في السجل. لم أر البقعة قبل خمسة عشر يوماً، وأراها كل ليلة صافية منذ ذلك. لا أعرف مصدرها.»",
  ["a_note_hisham"], ["f_log_exists"], "moderate",
  "إفادة المشرف نفسه؛ يؤيدها السجل ولا تتجاوزه إلى تفسير.", loc="loc_obs")
V("ev_lina_statement", "إفادة لينا الحاج (ملخص)", "testimonial",
  "ملخص إفادة لينا الحاج:\n«غيّرنا عاملاً واحداً في كل مرة وكررنا كل حالة مرتين. المحاكاة تقول ما هو ممكن، وتحتاج إلى سجلات الواقع لتقول ما حدث.»",
  ["a_note_lina"], ["f_sim_available"], "moderate",
  "إفادة خبيرة بالنموذج؛ تعرّف حدود المحاكاة ولا تفسّر ما جرى في المرصد.", loc="loc_lab")
V("ev_jamil_statement", "إفادة جميل الراشد (ملخص)", "testimonial",
  "ملخص إفادة جميل الراشد:\n«ركبت الواجهة قبل خمسة عشر يوماً وضبطت المؤقت. لم أكن أعلم أن المرصد يقابلها.»",
  ["a_note_jamil"], ["f_permit_exists"], "weak",
  "إفادة صاحب المنشأة؛ يؤيدها بعضها في الرخصة، ولا تثبت وحدها أثر الواجهة في المرصد.", loc="loc_resto")

# ---------------------------------------------------------------- inferences
def P(t, i): return {"ref_type": t, "ref_id": i}
inf = []
def I(id, prem, ct, concl, rel, strength, rule, ks):
    inf.append({"id": id, "premises": prem, "conclusion": {"ref_type": ct, "ref_id": concl}, "relation": rel, "strength": strength, "rule_ar": rule, "skill_ko_refs": ks})
# path A: the controlled runs
I("i_a_side", [P("evidence", "ev_run_baseline"), P("evidence", "ev_run_shield")], "fact", "f_terrestrial_source", "establishes", "strong",
  "حين غيّرنا الغطاء وحده اختفت البقعة مرتين وعادت مرتين، وحين أطفأنا المصدر اختفت؛ فالضوء يدخل من المنفذ المواجه للمدينة من مصدر أرضي.", ["KO-RS-06-008"])
I("i_a_facade", [P("fact", "f_terrestrial_source"), P("evidence", "ev_run_move")], "fact", "f_source_is_facade", "establishes", "strong",
  "حين حرّكنا المصدر وحده تبعته البقعة، وعند الاتجاه 247° وحده طابقت موضعها في الصورة؛ فالمصدر في اتجاه واجهة المطعم.", ["KO-RS-06-008", "KO-RS-06-015"])
# path B: the records
I("i_b_side", [P("evidence", "ev_obs_log"), P("evidence", "ev_site_map")], "fact", "f_terrestrial_source", "establishes", "strong",
  "البقعة ثابتة في الصورة بينما تتحرك النجوم، فهي مرتبطة بالأنبوب لا بالسماء؛ والمخطط يبيّن منفذاً جانبياً يقابل المدينة.", ["KO-RS-06-015"])
I("i_b_facade", [P("evidence", "ev_restaurant_permit"), P("evidence", "ev_obs_log")], "fact", "f_source_is_facade", "establishes", "strong",
  "ظهرت البقعة في أول ليلة صافية بعد تركيب الواجهة بعد اثنتين وعشرين ليلة بلا بقعة، وتظهر مع ساعات تشغيل الإضاءة وتختفي عند إطفائها.", ["KO-RS-06-015", "KO-RS-06-005"])
I("i_lens", [P("evidence", "ev_run_lens")], "hypothesis", "h_lens", "rules_out", "strong",
  "تبديل الكاميرا لم يغيّر الموضع ولا الشدة في المحاولتين؛ فالبقعة ليست وهج عدسة بعينها.", ["KO-RS-06-008"])
I("i_recoat", [P("evidence", "ev_post_recoat"), P("evidence", "ev_obs_log")], "hypothesis", "h_recoat", "rules_out", "strong",
  "التلبيس صحيح لكنه سبق الظاهرة بشهر ونصف، ومرت اثنتان وعشرون ليلة صافية بعده بلا بقعة؛ فالتوقيت لا يوافق.", ["KO-RS-06-015", "KO-RS-06-005"])
I("i_rule_lens_b", [P("fact", "f_terrestrial_source")], "hypothesis", "h_lens", "rules_out", "strong",
  "ضوء يدخل الأنبوب من منفذ جانبي تراه أجهزة مختلفة؛ أما وهج العدسة فيخص كاميرا واحدة ولا يزول بسد منفذ في الأنبوب.", ["KO-RS-06-008"])
I("i_rule_recoat_b", [P("fact", "f_source_is_facade")], "hypothesis", "h_recoat", "rules_out", "strong",
  "إذا عُرف مصدر ضوء أرضي محدد تتبعه البقعة فلا حاجة إلى تغيير في طبقة المرآة تفسيراً، وتجاور الأحداث في الزمن لا يصنع سبباً.", ["KO-RS-06-015"])
I("i_rule_mystery", [P("fact", "f_source_is_facade")], "hypothesis", "h_mystery", "rules_out", "conclusive",
  "إذا عُرف مصدر أرضي محدد تتبعه البقعة، فلا حاجة إلى مصدر سماوي مجهول لتفسيرها.", ["KO-RS-06-008"])
I("i_rule_mystery_b", [P("fact", "f_terrestrial_source")], "hypothesis", "h_mystery", "rules_out", "strong",
  "الضوء الداخل من منفذ جانبي ثابت في الصورة لا يتحرك مع النجوم؛ فليس من السماء.", ["KO-RS-06-008"])
I("i_support_refl", [P("fact", "f_source_is_facade")], "hypothesis", "h_reflection", "supports", "strong",
  "الواجهة المضاءة تفسر الموضع والتوقيت وغياب الظاهرة قبل التركيب، وتصمد أمام الاختبار المكذِّب.", ["KO-RS-06-015"])
I("i_claim_yazan", [P("evidence", "ev_post_cloudy"), P("evidence", "ev_obs_log")], "claim", "cl_yazan_mystery", "contradicts_claim", "strong",
  "لا يُسجَّل رصد في الليالي الغائمة أصلاً؛ فغياب البقعة فيها لا يدل على أنها «صافية فقط» بل على أن القبة مغلقة.", ["KO-RS-06-005"])
I("i_claim_jamil", [P("evidence", "ev_site_map"), P("evidence", "ev_run_baseline")], "claim", "cl_jamil_far", "contradicts_claim", "strong",
  "المطعم على بعد 400 م في الاتجاه المقابل للمنفذ، وفي النموذج أنتج المصدر عند ذلك الاتجاه البقعة؛ فالبعد لا يمنع وصول الضوء.", ["KO-RS-05-014"])

# ---------------------------------------------------------------- character knowledge
K = lambda f, a="witnessed", c="certain": {"fact_id": f, "access": a, "certainty": c}
ck = [
    {"character_id": "yazan", "knows": [K("f_clip_frames")], "hides": [], "believes": [{"claim_id": "cl_yazan_mystery", "stance": "sincere"}]},
    {"character_id": "hisham", "knows": [K("f_log_exists", "professional"), K("f_posts_exist", "professional"), K("f_map_exists", "professional")], "hides": [], "believes": []},
    {"character_id": "lina", "knows": [K("f_sim_available", "professional")], "hides": [], "believes": []},
    {"character_id": "jamil", "knows": [],
     "hides": [{"fact_id": "f_permit_exists", "reveal_when": {"presented": {"evidence_id": "ev_clip", "to_character": "jamil"}}, "cover_claim_id": "cl_jamil_far", "reveal_line_id": "jm_permit"}],
     "believes": [{"claim_id": "cl_jamil_far", "stance": "sincere"}]},
]
hyps = [
    {"id": "h_mystery", "statement_ar": "الضوء مصدره الفضاء أو المرآة نفسها ولا تفسير أرضياً له.", "is_true": False, "plausibility_at_start": "high"},
    {"id": "h_lens", "statement_ar": "البقعة وهج في عدسة كاميرا يزن، لا ضوء دخل المقراب.", "is_true": False, "plausibility_at_start": "medium"},
    {"id": "h_reflection", "statement_ar": "البقعة انعكاس من واجهة المطعم المضاءة حديثاً يدخل من منفذ جانبي للأنبوب.", "is_true": True, "plausibility_at_start": "low", "suspect_id": "jamil"},
    {"id": "h_recoat", "statement_ar": "إعادة تلبيس المرآة هي التي صنعت البقعة.", "is_true": False, "plausibility_at_start": "medium"},
]
mis = [
    {"id": "rh_clip", "points_to_hypothesis_id": "h_mystery", "planted_via_ar": "مقطع منتشر بتعليق مثير: ضوء في الليالي الصافية فقط.", "evidence_ids": ["ev_clip"],
     "refuted_by_inference_ids": ["i_rule_mystery", "i_rule_mystery_b", "i_claim_yazan"],
     "fairness_note_ar": "المقطع نفسه يُظهر النجوم تتحرك والبقعة ثابتة، وبيان المرصد وسجله يفسران غياب الرصد في الليالي الغائمة، والتجارب المكررة متاحة للاعب."},
    {"id": "rh_recoat", "points_to_hypothesis_id": "h_recoat", "planted_via_ar": "بيان صحيح عن مرآة أُعيد تلبيسها، فتبدو صلة زمنية.", "evidence_ids": ["ev_post_recoat"],
     "refuted_by_inference_ids": ["i_recoat", "i_a_side", "i_b_facade"],
     "fairness_note_ar": "البيان صحيح ويبقى صحيحاً؛ لكن سجل الرصد يبيّن اثنتين وعشرين ليلة صافية بعد التلبيس بلا بقعة، فالتوقيت لا يوافق."},
]
los = [
    {"id": "lo_test", "statement_ar": "يبحث عن اختبار قد يكذّب فرضيته، ويغيّر عاملاً واحداً في كل مرة ويكرر الملاحظة.", "skill_ko_ref": "KO-RS-06-008", "observable_behaviors_ar": ["يشغّل تجارب المحاكاة", "يربط التجربة بالفرضية"], "evidence_sources": ["action_log", "evidence_board"]},
    {"id": "lo_causal", "statement_ar": "يفرّق بين الاقتران في الزمن والآلية السببية.", "skill_ko_ref": "KO-RS-06-015", "observable_behaviors_ar": ["لا يربط التلبيس بالبقعة لمجرد تجاورهما", "يطلب آلية"], "evidence_sources": ["evidence_board", "final_justification"]},
    {"id": "lo_doubt", "statement_ar": "يقبل المعلومة الصحيحة ويرفض المضللة دون شك شامل في كل شيء.", "skill_ko_ref": "KO-RS-06-005", "observable_behaviors_ar": ["يقبل البيانين الصحيحين", "لا يتهم كل المصادر"], "evidence_sources": ["evidence_board"]},
    {"id": "lo_hyp", "statement_ar": "يوازن بين فرضيات متنافسة ويستبعد ما تنقضه الأدلة.", "skill_ko_ref": "KO-RS-06-006", "observable_behaviors_ar": ["يضيف فرضيات", "يستبعد بدليل"], "evidence_sources": ["hypothesis_ledger"]},
    {"id": "lo_calib", "statement_ar": "يصوغ نسبة الترجيح بحدودها.", "skill_ko_ref": "KO-RS-06-021", "observable_behaviors_ar": ["يختار ثقة معقولة", "يذكر حدوداً"], "evidence_sources": ["final_justification"]},
    {"id": "lo_revise", "statement_ar": "يراجع رأيه الأول حين يظهر ما يخالفه.", "skill_ko_ref": "KO-RS-06-009", "observable_behaviors_ar": ["يغيّر فرضيته الرائدة بدليل"], "evidence_sources": ["hypothesis_ledger"]},
]
def levels(d): return [{"score": i, "descriptor_ar": t} for i, t in enumerate(d)]
rub = {
    "reference_answer_ar": "لا ضوء غامضاً في المرآة. البقعة انعكاس من واجهة زجاجية مضاءة حديثاً في مطعم قرب المرصد، يدخل من المنفذ الجانبي المواجه للمدينة. اجتمع على ذلك مساران مستقلان: تجارب محاكاة غيّرت عاملاً واحداً وكررت كل حالة (إطفاء المصدر، وسد المنفذ، وتحريك المصدر، وتبديل الكاميرا)، وسجلات تبيّن أن البقعة ثابتة بينما تدور النجوم، وأنها ظهرت بعد تركيب الواجهة وتختفي عند إطفائها. والبيانان الصحيحان عن المرصد يبقيان صحيحين: إغلاق القبة عند الغيم وإعادة تلبيس المرآة، لكنهما لا يفسران البقعة. حدود الاستنتاج: المحاكاة نموذج وعدد محاولاتها قليل، ولم يُطفأ المؤقت فعلياً ليلة اختبار في الموقع، ولا يثبت السجل شيئاً عن ليالٍ لم يُفتح فيها المرصد.",
    "criteria": [
        {"id": "c_source", "name_ar": "تصنيف المصادر", "objective_ids": ["lo_doubt"], "scored_by": "deterministic", "weight": 0.15, "levels": levels(["لم يصنّف", "أخطأ في الأغلب", "نصف صحيح", "معظمه صحيح", "كله صحيح"])},
        {"id": "c_conflict", "name_ar": "ترتيب الأدلة على الخط الزمني", "objective_ids": ["lo_causal"], "scored_by": "deterministic", "weight": 0.15, "levels": levels(["لم يضع شيئاً", "وضع قليلاً", "وضع نصفها صحيحاً", "معظمها", "كلها في موضعها"])},
        {"id": "c_links", "name_ar": "ربط الأدلة بالفرضيات", "objective_ids": ["lo_test", "lo_causal"], "scored_by": "deterministic", "weight": 0.25, "levels": levels(["لا روابط", "قليلة", "نصفها صحيح", "معظمها", "كلها دقيقة"])},
        {"id": "c_uncertainty", "name_ar": "معايرة الثقة", "objective_ids": ["lo_calib"], "scored_by": "deterministic", "weight": 0.15, "levels": levels(["ثقة مفرطة", "حدود قليلة", "جزئية", "معقولة", "معايَرة كاملة"])},
        {"id": "c_revision", "name_ar": "مراجعة الرأي", "objective_ids": ["lo_revise"], "scored_by": "deterministic", "weight": 0.1, "levels": levels(["بقي على فرضية مرفوضة", "لم يعلن فرضية", "ثبت على فرضية سليمة", "غيّر بدليل", "غيّر بدليل ووثّق"])},
        {"id": "c_elimination", "name_ar": "استبعاد الفرضيات الخاطئة", "objective_ids": ["lo_hyp"], "scored_by": "deterministic", "weight": 0.1, "levels": levels(["لم يستبعد", "استبعد خطأً", "فرضية بدليل", "فرضيتين", "كل الخاطئة"])},
        {"id": "c_justification", "name_ar": "جودة الحجة المكتوبة", "objective_ids": ["lo_test", "lo_hyp"], "scored_by": "human", "weight": 0.1, "levels": levels(["لا حجة", "ادعاء بلا سند", "أدلة دون ربط", "ربط الأدلة بالاستنتاج", "ربط مع البدائل والحدود"])},
    ],
}
def H(id, lv, kind, text, trig, target=None, w=0.0):
    d = {"id": id, "level": lv, "kind": kind, "text_ar": text, "trigger": trig, "assessment_weight": w}
    if target: d["targets_inference_id"] = target
    return d
he = lambda e: {"has_evidence": e}
hints = [
    H("hg1", 1, "metacognitive", "حين يتقدم تفسير مثير، اسأل: ما الاختبار الذي كان يمكن أن يكذّبه؟", {"always": True}, None, 0.02),
    H("hg2", 2, "focus_area", "اجمع ما يصح في المنشورات عن المرصد، ثم اسأل لكل منها: هل يفسر البقعة أم يكتفي بأنه صحيح؟", he("ev_clip"), None, 0.04),
    H("ha1", 1, "metacognitive", "إذا غيّرت عاملين معاً فكيف تعرف أيهما فعل؟", he("ev_run_baseline"), "i_a_side", 0.02),
    H("ha2", 2, "pointer", "جرّب سد كل منفذ جانبي على حدة، وكرر كل حالة مرتين على الأقل.", he("ev_run_baseline"), "i_a_side", 0.06),
    H("ha3", 3, "partial_reveal", "اطلب من لينا تجربة الغطاء ثم تجربة تحريك المصدر، وقارن مواضع البقعة.", he("ev_run_baseline"), "i_a_side", 0.1),
    H("hb1", 1, "metacognitive", "متى ظهرت البقعة أول مرة؟ وما الذي تغيّر في المدينة قبل ذلك بقليل؟", he("ev_clip"), "i_b_facade", 0.02),
    H("hb2", 2, "pointer", "اسأل هشام عن السجل والمخطط، واسأل صاحب المطعم عن أوراق واجهته.", he("ev_clip"), "i_b_facade", 0.06),
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
Act("a_get_clip", "examine", "شاهد المقطع المنتشر", al, [G("ev_clip")], "loc_web", "GET_CLIP")
for cid, lab in [("yazan", "يزن"), ("hisham", "هشام"), ("lina", "لينا"), ("jamil", "جميل")]:
    Act(f"a_int_{cid}", "interview", f"ابدأ مقابلة {lab}", al, [{"op": "raise_trust", "ref_id": cid, "amount": 1}], cid, f"INT_{cid.upper()}")
Act("a_get_log", "examine", "اطلب سجل الرصد الليلي", fu("f_log_exists"), [G("ev_obs_log")], "loc_obs", "GET_LOG")
Act("a_get_posts", "examine", "اقرأ بيانَي المرصد المنشورين", fu("f_posts_exist"), [G("ev_post_cloudy"), G("ev_post_recoat")], "loc_obs", "GET_POSTS")
Act("a_get_map", "examine", "اطلب مخطط موقع المرصد", fu("f_map_exists"), [G("ev_site_map")], "loc_obs", "GET_MAP")
Act("a_get_permit", "examine", "اطلب رخصة الواجهة من جميل", fu("f_permit_exists"), [G("ev_restaurant_permit")], "loc_resto", "GET_PERMIT")
Act("a_run_baseline", "request_lab_test", "شغّل المحاكاة: مصدر مطفأ ثم مضاء (مرتان لكل حالة)", fu("f_sim_available"), [G("ev_run_baseline")], "loc_lab", "RUN_BASELINE")
Act("a_run_shield", "request_lab_test", "شغّل المحاكاة: غطِّ منفذاً جانبياً واحداً (مرتان)", he("ev_run_baseline"), [G("ev_run_shield")], "loc_lab", "RUN_SHIELD")
Act("a_run_lens", "request_lab_test", "شغّل المحاكاة: بدّل الكاميرا فقط (مرتان)", he("ev_run_baseline"), [G("ev_run_lens")], "loc_lab", "RUN_LENS")
Act("a_run_move", "request_lab_test", "شغّل المحاكاة: حرّك المصدر على السكة (مرتان لكل موضع)", he("ev_run_baseline"), [G("ev_run_move")], "loc_lab", "RUN_MOVE")
Act("a_note_yazan", "examine", "دوّن إفادة يزن", fu("f_clip_frames"), [G("ev_yazan_statement")], "yazan", "NOTE_YAZAN")
Act("a_note_hisham", "examine", "دوّن إفادة هشام", fu("f_log_exists"), [G("ev_hisham_statement")], "hisham", "NOTE_HISHAM")
Act("a_note_lina", "examine", "دوّن إفادة لينا", fu("f_sim_available"), [G("ev_lina_statement")], "lina", "NOTE_LINA")
Act("a_note_jamil", "examine", "دوّن إفادة جميل", fu("f_permit_exists"), [G("ev_jamil_statement")], "jamil", "NOTE_JAMIL")
Act("p_clip_jamil", "present_evidence", "اعرض المقطع على جميل", {"presented": {"evidence_id": "ev_clip", "to_character": "jamil"}}, [{"op": "emit_event", "ref_id": "PRESENTED_CLIP_JAMIL"}], "jamil", "P_CLIP_JAMIL", 0)
Act("a_hint", "request_hint", "اطلب تلميحاً", al, [], None, "REQUEST_HINT", 0)
Act("a_accuse", "final_accusation", "قدّم الاستنتاج النهائي", al, [{"op": "emit_event", "ref_id": "SUBMIT"}], None, "FINAL_ACCUSATION", 0)

topics = [
    {"id": "t_clip", "label_ar": "كيف صُوّر المقطع", "example_questions_ar": ["كيف صوّرت اللقطتين؟", "لماذا ظننت أن الضوء من السماء؟"], "fact_ids": ["f_clip_frames"], "claim_ids": ["cl_yazan_mystery"]},
    {"id": "t_records", "label_ar": "سجلات المرصد", "example_questions_ar": ["هل يوجد سجل رصد؟", "ما البيانان المنشوران؟", "هل لديكم مخطط للموقع؟"], "fact_ids": ["f_log_exists", "f_posts_exist", "f_map_exists"]},
    {"id": "t_sim", "label_ar": "نموذج المحاكاة", "example_questions_ar": ["هل عندكم نموذج للمرصد؟", "كيف تجرون التجربة؟"], "fact_ids": ["f_sim_available"]},
    {"id": "t_facade", "label_ar": "واجهة المطعم", "example_questions_ar": ["متى ركبتم الواجهة؟", "هل تصل إضاءتها إلى المرصد؟"], "fact_ids": ["f_permit_exists"], "claim_ids": ["cl_jamil_far"]},
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
    (1, "بإطفاء المصدر في النموذج اختفت البقعة، وبسد المنفذ المواجه للمدينة وحده اختفت أيضاً، وعاد ظهورها برفع الغطاء؛ كل حالة كُررت مرتين.", ["ev_run_baseline", "ev_run_shield"], "i_a_side"),
    (2, "حين حُرّك المصدر وحده تبعته البقعة، ومطابقتها لموضعها في المقطع جاءت عند اتجاه واجهة المطعم.", ["ev_run_move"], "i_a_facade"),
    (3, "مسار السجلات المستقل: البقعة ثابتة في الصورة بينما تتحرك النجوم، والمخطط يبيّن منفذاً جانبياً يقابل المدينة.", ["ev_obs_log", "ev_site_map"], "i_b_side"),
    (4, "الرخصة تحدد تاريخ تركيب الواجهة وساعات تشغيلها، والسجل يضع ظهور البقعة بعد التركيب مباشرة واختفاءها مع إطفاء المؤقت.", ["ev_restaurant_permit", "ev_obs_log"], "i_b_facade"),
    (5, "تبديل الكاميرا لم يغيّر شيئاً، فالبقعة ليست من العدسة.", ["ev_run_lens"], "i_lens"),
    (6, "البيانان الصحيحان قُبلا ولم يُفسرا أكثر مما يقولان: القبة مغلقة في الغيم، والتلبيس سبق الظاهرة بزمن طويل.", ["ev_post_cloudy", "ev_post_recoat", "ev_obs_log"], "i_recoat"),
]
ending = {
    "steps": [{"order": o, "text_ar": t, "uses_evidence_ids": u, "inference_id": i} for o, t, u, i in steps],
    "alternative_paths_ar": [
        "يمكن الوصول إلى النتيجة من السجلات وحدها (سجل الرصد والمخطط والرخصة) دون تشغيل المحاكاة، لكنك حينئذ لم تجرّب ما كان يمكن أن يكذّب تفسيرك.",
        "ويمكن الوصول إليها من التجارب المكررة وحدها، لكن الأقوى أن تتفق التجربة مع سجلات الواقع.",
    ],
    "what_evidence_could_not_show_ar": [
        "المحاكاة نموذج مصغّر وعدد محاولات كل حالة قليل، فتبين ما هو ممكن لا ما حدث بالضبط.",
        "لم يُطفأ مؤقت الواجهة فعلياً في ليلة اختبار داخل الموقع؛ ذلك اختبار مقترح يعزز الاستنتاج.",
        "لا يثبت السجل شيئاً عن ليالٍ لم يُفتح فيها المرصد.",
    ],
    "science_notes_ar": [
        "الاختبار المفيد هو الذي يمكن أن يفشل: سدّ المنفذ كان سيُبقي البقعة لو كان المصدر في السماء.",
        "غيّر عاملاً واحداً في كل مرة وكرّر الملاحظة؛ فلا يُحكم بمحاولة وحيدة.",
        "قبول البيانين الصحيحين جزء من الشك السليم: نرفض المضلل ونقبل الصحيح، ثم نسأل هل الصحيح يفسر الظاهرة.",
        "كل ما استندنا إليه يمكن تتبّع أصله بسلسلة العهدة (سجل المرصد، رخصة البلدية، سجل التجربة)، وتُعلن نسبة الترجيح بحدودها.",
        "بطاقة الأصل (خبر تراثي منسوب): تذكر الحكاية القديمة عالماً يسدّ أنبوباً ليختبر مسار الضوء، وقد أُعيدت صياغتها كلها في موقف خيالي دون نسبة «اختراع المنهج العلمي» إلى أحد.",
    ],
}
core = {
    "schema_version": "0.1.0", "case_id": CID, "case_version": "0.1.0",
    "meta": {"title_ar": "الضوء في مرآة المرصد", "title_en": "The Light in the Observatory Mirror", "age_band": "13-15", "locale": "ar", "dialogue_register": "msa", "estimated_minutes": 30, "difficulty": 2,
             "content_flags": ["no_violence", "science_lab"], "authors": ["فريق أثر التحريري (مسودة بمساعدة الذكاء الاصطناعي، لم تُراجَع بشرياً بعد)"],
             "knowledge_object_refs": ["KO-RS-06-008", "KO-RS-06-015", "KO-RS-06-005", "KO-RS-06-006", "KO-RS-06-021", "KO-RS-06-009"]},
    "premise": {"hook_ar": "مقطع منتشر يقول إن مرآة المرصد تُظهر ضوءاً لا يفسره أحد، ويظهر كلما صفت السماء.",
                "player_role_ar": "أنت متدرب في مختبر «المنظار» وطُلب منك أن تقول بالتجربة والسجلات ما الذي تُظهره هذه المرآة فعلاً.",
                "setting_ar": "مرصد الأطلال ومختبر المنظار، وتاريخ الأحداث قبل أسبوعين وبعدها. أوقات السجلات بتوقيت المرصد.",
                "public_fact_ids": ["f_clip_viral", "f_yazan_filmed", "f_posts_circulate"],
                "assumed_general_knowledge_ar": ["النجوم تنتقل في الصورة مع دوران الأرض", "الضوء ينتقل في خط مستقيم ويمكن حجبه"]},
    "entities": {"characters": chars, "locations": locations, "objects": objects, "organizations": orgs},
    "truth": {"solution": {"culprit_ids": ["jamil"], "summary_ar": "لا ضوء غامضاً. أضاءت واجهة جديدة في مطعم مجاور زجاجها كل مساء، فانعكس شعاعها في المنفذ الجانبي للأنبوب وصنع بقعة ثابتة في الصورة. لم يقصد مدير المطعم شيئاً من ذلك، وظلت منشورات المرصد صحيحة لكنها لم تكن تفسيراً.", "key_fact_ids": ["f_terrestrial_source", "f_source_is_facade"]},
              "facts": facts, "claims": claims},
    "timeline": timeline, "evidence": ev, "evidence_graph": {"inferences": inf},
    "character_knowledge": ck, "hypotheses": hyps, "misdirection_plan": mis, "learning_objectives": los,
    "mechanics": {"time_budget_units": 40, "actions": A},
    "state_machine": {"id": "c018", "initial": "briefing", "type": "compound", "states": {
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
    "clock": {"epoch_hhmm": "18:00", "zone_label_ar": "توقيت المرصد"},
    "cover": {"title_ar": "الضوء في مرآة المرصد", "tagline_ar": "ضوء يظهر في الليالي الصافية، وتجربة يمكن أن تفشل", "kicker_ar": "الملف الثامن عشر · الاختبار المكذِّب", "glyph": "◎", "accent": "green"},
    "cold_open_ar": ["ليلة صافية في الأطلال.", "مقطع قصير يملأ المنصات: بقعة ضوء بيضاء في صورة مرآة المرصد، وتعليق يقول إنها لا تفسير لها.", "في ملفك بيانان رسميان من المرصد، ومختبر محاكاة يتيح لك أن تغيّر عاملاً واحداً وتكرر.", "ابدأ بسؤال: ما الاختبار الذي كان يمكن أن يُظهر أن هذا التفسير خاطئ؟"],
    "labs": [],
    "source_classes": [
        {"id": "primary_record", "label_ar": "سجل أصلي", "help_ar": "يُنتجه شخص أو نظام لحظة الحدث، كسجل رصد أو رخصة بلدية أو سجل تجربة."},
        {"id": "redisplay", "label_ar": "نسخة معروضة", "help_ar": "مقطع أو لقطة أو نتيجة محاكاة أُعيد عرضها وتتأثر بطريقة التصوير والعرض."},
        {"id": "claim", "label_ar": "قول أو تصريح", "help_ar": "إفادة شخص؛ تُقاس بالسجلات لا بنبرة صاحبها."},
        {"id": "template", "label_ar": "قالب أو نموذج", "help_ar": "نص جاهز لا يصف الحدث الفعلي بذاته."},
        {"id": "public_document", "label_ar": "وثيقة منشورة", "help_ar": "وثيقة معلنة ومعروف ناشرها، كبيان رسمي أو مخطط."}],
    "limit_menu": [
        {"id": "l_model", "label_ar": "المحاكاة نموذج مصغّر، وكل حالة كُررت مرتين فقط، فهي تدل على الممكن لا على ما حدث"},
        {"id": "l_no_onsite", "label_ar": "لم يُجرَ اختبار في الموقع بإطفاء الواجهة فعلاً، وهو ما يعزز الاستنتاج"},
        {"id": "l_closed_nights", "label_ar": "السجل لا يقول شيئاً عن ليالٍ لم يُفتح فيها المرصد"},
        {"id": "l_invalid_posts", "label_ar": "بيانا المرصد غير موثوقين لأنهما لا يفسران البقعة"},
        {"id": "l_invalid_viral", "label_ar": "كثرة مشاهدات المقطع تثبت أن الضوء حقيقي وغامض"}],
    "mind_change_menu": [
        {"id": "m_onsite_off", "label_ar": "إطفاء الواجهة فعلياً ثم استمرار البقعة في ليلة صافية"},
        {"id": "m_cloudy_spot", "label_ar": "ظهور البقعة في ليلة غائمة رُصدت فعلاً"},
        {"id": "m_old_spot", "label_ar": "ظهور البقعة في سجل المرصد قبل تركيب الواجهة"},
        {"id": "m_popular", "label_ar": "كثرة المتابعين الذين يصدقون المقطع"}],
    "skills": [{"skill_id": "KO-RS-06-008", "track": "B"}, {"skill_id": "KO-RS-06-015", "track": "D"}, {"skill_id": "KO-RS-06-005", "track": "B"}],
    "stage_hooks_ar": {"briefing": "ضوء غامض في مرآة المرصد… فهل تكفي الدهشة؟", "investigating": "غيّر عاملاً واحداً، وكرر، ثم اسأل ماذا كان سيحدث لو كنت مخطئاً.", "review": "قبل أن تغلق الملف: ما الذي لم تختبره؟", "resolved": "أُغلق الملف. ملف جديد ينتظر في الأرشيف."},
    "character_glyphs": {"yazan": "ي", "hisham": "هـ", "lina": "ل", "jamil": "ج"},
}
sc = {
    "case_id": CID,
    "accepted_conclusions": {"h_reflection": {"grade": 1, "note_ar": "استنتاج متسق مع التجارب والسجلات ويتطلب ذكر حدوده."},
                             "h_mystery": {"grade": 0, "note_ar": "يتجاهل أن البقعة ثابتة بينما تتحرك النجوم، وأن سد المنفذ أزالها."},
                             "h_lens": {"grade": 0, "note_ar": "تبديل الكاميرا لم يغيّر البقعة."},
                             "h_recoat": {"grade": 0, "note_ar": "يخلط بين التجاور في الزمن والسببية؛ مرّت اثنتان وعشرون ليلة صافية بعد التلبيس بلا بقعة."}},
    "confidence_band": {"h_reflection": [65, 90], "h_mystery": [0, 15], "h_lens": [0, 15], "h_recoat": [0, 15]},
    "source_key": {"ev_clip": "redisplay", "ev_obs_log": "primary_record", "ev_post_cloudy": "public_document", "ev_post_recoat": "public_document", "ev_site_map": "public_document",
                   "ev_restaurant_permit": "primary_record", "ev_run_baseline": "primary_record", "ev_run_shield": "primary_record", "ev_run_lens": "primary_record", "ev_run_move": "primary_record",
                   "ev_yazan_statement": "claim", "ev_hisham_statement": "claim", "ev_lina_statement": "claim", "ev_jamil_statement": "claim"},
    "link_key": {
        "h_reflection": {"ev_run_baseline": "supports", "ev_run_shield": "supports", "ev_run_move": "supports", "ev_obs_log": "supports", "ev_site_map": "supports", "ev_restaurant_permit": "supports", "ev_post_recoat": "neutral", "ev_clip": "neutral"},
        "h_mystery": {"ev_clip": "supports", "ev_run_shield": "weakens", "ev_run_move": "weakens", "ev_obs_log": "weakens", "ev_restaurant_permit": "weakens", "ev_post_cloudy": "weakens"},
        "h_lens": {"ev_run_lens": "weakens", "ev_obs_log": "weakens", "ev_run_shield": "weakens"},
        "h_recoat": {"ev_post_recoat": "supports", "ev_obs_log": "weakens", "ev_restaurant_permit": "weakens", "ev_run_shield": "weakens"},
    },
    "required_limits": ["l_model", "l_no_onsite"], "valid_mind_changers": ["m_onsite_off", "m_cloudy_spot", "m_old_spot"],
    "invalid_limits": ["l_invalid_posts", "l_invalid_viral"],
    "decisive_evidence": ["ev_run_baseline", "ev_run_shield", "ev_run_move", "ev_obs_log", "ev_restaurant_permit", "ev_site_map"],
    "lab_requirement": None,
    "timeline_requirement": [{"evidence_id": "ev_restaurant_permit", "utc_minute": 110, "tol": 5}, {"evidence_id": "ev_clip", "utc_minute": 130, "tol": 5}],
    "refuted_hypotheses": ["h_mystery", "h_lens", "h_recoat"],
    "criteria_map": {"c_source": "source_typing", "c_conflict": "conflict_resolution", "c_links": "hypothesis_links", "c_uncertainty": "uncertainty", "c_revision": "revision", "c_elimination": "elimination", "c_justification": "justification_human"},
    "caps": {"no_citations_max": 45, "no_conflict_resolution_max": 70},
}
os.makedirs(OUT, exist_ok=True)
for suf, obj in [("", core), (".ui", ui), (".scoring", sc)]:
    with open(os.path.join(OUT, f"{CID}{suf}.json"), "w", encoding="utf8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
print("ok")
