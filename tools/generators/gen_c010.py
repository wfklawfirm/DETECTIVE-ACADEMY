#!/usr/bin/env python3
# Case c010 «مطرٌ في ليلة صافية» — adapted from the library reference case s001_rain_clear_night (13_CASE_DESIGN_REFERENCE/sample_case_001.json).
# Same story / truth / timeline / evidence graph; adapted to the platform's stricter checks:
#  * key facts must be DERIVABLE through fact-concluding inferences (the source only concluded a hypothesis from the hose facts) -> new inferences
#    i_hose_a / i_hose_b conclude f_hose_majed, and i_present_b gives a second, gate-log-free route to f_majed_on_roof (two disjoint proof paths);
#  * evidence that comes from people (statements, photo) is gated by dialogue-unlocked facts + ask_<char>_<fact> mirror actions;
#  * register is plain MSA; per-character authored lines with purposes; ui + scoring sidecars in the c000/c001 pattern.
# The person who caused the unintended event (Majed) is recorded as culprit_ids per the library convention for no-culprit cases.
import json, sys, os
OUT = sys.argv[1]
CID = "c010_rain_clear_night"

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
def ch(id, name, role, age, persona, motives, lines, forbidden=None, sentences=3):
    chars.append({"id": id, "name_ar": name, "role": role, "age_descriptor_ar": age, "persona_ar": persona, "motives_ar": motives,
                  "speech_constraints": {"register": "msa", "max_sentences_per_turn": sentences, "forbidden_topics_ar": forbidden or []}, "authored_lines": lines})

ch("lama", "لمى", "witness", "15 سنة، قائدة فريق محطة الرصد",
   "منظمة وسريعة الحماس، تتكلم بجمل قصيرة واثقة، وتميل إلى الدفاع عن فريقها.",
   ["إنقاذ مشاركة الفريق في المسابقة", "تخشى أن يُتّهم فريقها بالتلاعب بالبيانات"],
   [L("lm_greet", "greeting", "أخيراً وصلتَ! المحطة تقول إنها أمطرت ليلة الأربعاء، وأنا كنت أنظر إلى النجوم بنفسي. موعد التسليم الساعة العاشرة.", ["f_rain_recorded", "f_deadline"]),
    L("lm_left", "reveal", "خرجت قبل الجميع تقريباً، من البوابة في التاسعة والربع.", ["f_lama_left"]),
    L("lm_rule", "reveal", "قواعد النادي تمنع الصعود إلى السطح بعد السادسة دون إذن المشرف.", ["f_roof_rule"]),
    L("lm_hoodie", "reveal", "السترة الزرقاء وُزّعت على المشاركين كلهم في الورشة، ولا تخصّ أحداً بعينه.", ["f_hoodie_common"]),
    L("lm_station", "reveal", "سجّلت المحطة نحو اثني عشر ملّيمتراً، والسماء كانت صافية. هذا ما يحيّرني.", ["f_rain_recorded"]),
    L("lm_unknown", "deflect_unknown", "لا أعرف. كنت قد غادرت المدرسة حين حدث ذلك."),
    L("lm_off", "deflect_offtopic", "أرجوك، لنبقَ في موضوع المحطة والبيانات."),
    L("lm_bye", "farewell", "أريد أن أعرف ما حدث قبل العاشرة. شكراً لك.")],
   ["حياة اللاعب الشخصية خارج القضية"])
ch("majed", "ماجد", "suspect", "14 سنة، مسؤول صيانة المحطة في الفريق نفسه",
   "لطيف ومتعاون، يعرض المساعدة كثيراً ويقترح أين يجب أن يبحث المحقق؛ هادئ الصوت.",
   ["صنع مؤقت سقاية لحديقة المدرسة ويريد مفاجأة الفريق به", "يخاف أن يُستبعد الفريق لأنه صعد السطح بعد السادسة دون إذن"],
   [L("mj_greet", "greeting", "أي شيء تحتاجه من المحطة فأنا جاهز. ربما تبدأ بفريق مدرسة النخيل؟"),
    L("mj_cover", "lie", "بقيت في غرفة النادي أرتّب الأجهزة، ثم خرجت نحو التاسعة والنصف. لم أصعد إلى السطح أصلاً.", None, ["cl_majed_club_room"]),
    L("mj_reveal", "reveal", "...صحيح. صعدت لأجرّب مؤقت السقاية الذي صنعته، ولم أنتبه إلى أن الرذاذ يصل إلى المقياس. خفت أن يُستبعد الفريق لأني صعدت دون إذن.", ["f_majed_on_roof", "f_hose_majed"], ["cl_majed_club_room"]),
    L("mj_refuse", "refuse_secret", "هذا شيء أفضّل ألا أتحدث عنه الآن."),
    L("mj_unknown", "deflect_unknown", "لا أعرف شيئاً عن ذلك."),
    L("mj_off", "deflect_offtopic", "أظن أن هذا لا يخص المحطة. اسألني عما يفيد التحقيق."),
    L("mj_bye", "farewell", "إن احتجت مساعدة أخرى فأنا هنا.")],
   ["أي طريقة لإخفاء الآثار أو تعديل السجلات"])
ch("ziad", "زياد", "suspect", "14 سنة، عضو فريق «مدرسة النخيل» المشارك في الورشة",
   "خجول، يجيب باختصار، ويقلق من إبلاغ أهله؛ يصبح أكثر انفتاحاً حين يُسأل باحترام وبأسئلة مفتوحة.",
   ["يريد الفوز بالمسابقة بعرض جيد", "يخفي أنه ترك قاعة الورشة ليتدرّب وحده لأنه يخجل من التحدث أمام الناس"],
   [L("zd_greet", "greeting", "أهلاً. هل ستخبرون أهلي بشيء؟"),
    L("zd_cover", "lie", "كنت في قاعة الورشة طوال الوقت، ثم خرجت مع أبي.", None, ["cl_ziad_whole_time"]),
    L("zd_reveal", "reveal", "هذا صوتي... كنت أتدرّب على العرض في غرفة الموسيقى. لم أرد أن يعرف فريقي أنني أخاف الكلام أمام اللجنة.", ["f_ziad_rehearsal"], ["cl_ziad_whole_time"]),
    L("zd_left", "reveal", "جاء أبي فوقّعت ورقة الانصراف وخرجنا معاً، قبل العاشرة بقليل.", ["f_ziad_left"]),
    L("zd_hoodie", "reveal", "كلنا لبسنا السترة الزرقاء نفسها في الورشة.", ["f_hoodie_common"]),
    L("zd_refuse", "refuse_secret", "أفضّل ألا أتحدث عن هذا."),
    L("zd_unknown", "deflect_unknown", "لم أرَ السطح. لا أعرف."),
    L("zd_off", "deflect_offtopic", "لا أعرف كيف يتعلق هذا بالمقياس."),
    L("zd_bye", "farewell", "شكراً لأنك سألتني بهدوء.")],
   ["حياة اللاعب الشخصية خارج القضية"], 2)
ch("wadad", "السيدة وداد", "witness", "قيّمة المدرسة منذ سنوات",
   "دقيقة في التفاصيل المادية، تعرف كل باب وصنبور في المبنى، وتصرّح حين لا تكون متأكدة.",
   ["تريد إبلاغ الصيانة بالبقعة المبللة", "تحرص على أن يبقى السطح مغلقاً بأمان"],
   [L("wd_greet", "greeting", "تفضّل. أنا أعرف هذا المبنى بابًا بابًا، فاسأل ما شئت."),
    L("wd_account", "reveal", "وأنا أنظّف ممر الطابق الأخير سمعت صوت ماء فوق السقف، ثم رأيت شاباً بسترة الورشة الزرقاء ينزل من درج السطح. كان ذلك قرابة العاشرة والنصف، على ما أظن.", ["f_wadad_heard", "f_wadad_saw"], ["cl_wadad_time"]),
    L("wd_patch", "reveal", "حين صعدت في جولة الإغلاق وجدت أرضية السطح جافة إلا بقعة مبللة، فصوّرتها بهاتفي لأبلّغ الصيانة.", ["f_wet_patch"]),
    L("wd_exit", "reveal", "أنهيت جولتي وخرجت من البوابة قرابة العاشرة والنصف ليلاً.", ["f_wadad_exit"]),
    L("wd_unknown", "deflect_unknown", "لم أرَ وجهه؛ كل المشاركين لبسوا السترة نفسها."),
    L("wd_off", "deflect_offtopic", "اسألني عن الأبواب والسطح، فهذا ما أعرفه."),
    L("wd_bye", "farewell", "أبلغوا الصيانة بالبقعة حين تنتهون.")])
ch("noor", "م. نور", "expert", "مهندسة في مختبر «المنظار»",
   "هادئة ومتواضعة معرفياً؛ تشرح بتشبيه قصير، وتذكر دائماً حدّاً واحداً على الأقل لما يثبته الدليل.",
   ["أن تُسلَّم بيانات صادقة حتى لو كانت ناقصة"],
   [L("nr_greet", "greeting", "أهلاً. أستطيع أن أقارن ساعة جهاز بساعة الشبكة إن طلبت، لكنني أذكر دائماً ما لا تثبته المقارنة."),
    L("nr_power", "reveal", "سجل أعطال المحطة يذكر انقطاعاً للكهرباء مدته خمس وعشرون دقيقة مساء الاثنين.", ["f_power_cut"]),
    L("nr_unknown", "deflect_unknown", "هذا الفرق قسناه اليوم. هل كان هو نفسه ليلة الأربعاء؟ نحتاج مصدراً مستقلاً بتوقيت مختلف."),
    L("nr_off", "deflect_offtopic", "أجيب عن الساعات والسجلات الرقمية فقط."),
    L("nr_bye", "farewell", "سجّل دائماً ما قيس وما لم يُقَس.")],
   ["طرق تعديل الطوابع الزمنية أو حذف السجلات", "أي حكم بالذنب على شخص"])
ch("yusuf", "يوسف", "assistant", "متطوع شاب في وحدة «تحقّق» التابعة لشبكة الأثر",
   "سريع وفضولي، يفكر بصوت عالٍ ويتسرّع أحياناً، ثم يعترف بخطئه حين يُعرض عليه دليل.",
   ["أن يتعلم المتدرّب المنهج لا الحل فقط"],
   [L("ys_greet", "greeting", "زياد كان متوتراً جداً... أليس هذا كافياً؟ لا، انتظر؛ هذه ملاحظة عن سلوكه، لا دليل على فعل. ماذا نحتاج لنعرف؟"),
    L("ys_unknown", "deflect_unknown", "لا أعرف بعد. دعنا نبحث عن سجل يجيب."),
    L("ys_off", "deflect_offtopic", "فلنعد إلى القضية: ما الدليل الذي ينقصنا؟"),
    L("ys_bye", "farewell", "أنا معك في الخطوة التالية.")],
   ["ذكر الحل أو أي حقيقة لم يكتشفها اللاعب"], 2)

locations = [
    {"id": "loc_roof", "name_ar": "سطح المدرسة", "aliases_ar": ["السطح"], "description_ar": "عليه محطة الرصد ومقياس المطر، وصنبور لحديقة السطح على بعد نحو ثلاثة أمتار."},
    {"id": "loc_club_room", "name_ar": "غرفة نادي العلوم", "aliases_ar": ["غرفة النادي"], "description_ar": "فيها حاسوب المحطة ودفاتر الفريق."},
    {"id": "loc_music_room", "name_ar": "غرفة الموسيقى", "aliases_ar": ["قاعة الموسيقى"], "description_ar": "غرفة هادئة في طابق الورشة."},
    {"id": "loc_hall", "name_ar": "قاعة الورشة", "aliases_ar": ["القاعة"], "description_ar": "أقيمت فيها الورشة المسائية المشتركة."},
    {"id": "loc_gate", "name_ar": "البوابة الرئيسية", "aliases_ar": ["البوابة"], "description_ar": "البوابة الوحيدة العاملة ليلاً، وتقرأ البطاقات."},
    {"id": "loc_top_corridor", "name_ar": "ممر الطابق الأخير", "aliases_ar": ["الممر العلوي", "درج السطح"], "description_ar": "الممر الذي ينتهي بدرج السطح."}]
objects = [
    {"id": "obj_station", "name_ar": "محطة الرصد", "aliases_ar": ["المحطة", "محطة الطقس"]},
    {"id": "obj_gauge", "name_ar": "مقياس المطر", "aliases_ar": ["المقياس"]},
    {"id": "obj_timer", "name_ar": "مؤقت السقاية", "aliases_ar": ["المؤقت"]},
    {"id": "obj_hose", "name_ar": "خرطوم السطح", "aliases_ar": ["الخرطوم"]},
    {"id": "obj_tablet", "name_ar": "الجهاز اللوحي لغرفة الموسيقى", "aliases_ar": ["اللوحي"]},
    {"id": "obj_hoodie", "name_ar": "سترة الورشة الزرقاء", "aliases_ar": ["السترة الزرقاء"]}]
orgs = [
    {"id": "org_school", "name_ar": "مدرسة ضفاف القنطرة الإعدادية"},
    {"id": "org_rival_school", "name_ar": "مدرسة النخيل"},
    {"id": "org_manzar", "name_ar": "مختبر المنظار"},
    {"id": "org_observatory", "name_ar": "مرصد القنطرة"},
    {"id": "org_athar_network", "name_ar": "شبكة الأثر"}]

facts = []
def F(id, st, kind, subj, spoiler, time=None, loc=None, ko=None):
    d = {"id": id, "statement_ar": st, "kind": kind, "subject_ids": subj, "spoiler_level": spoiler}
    if time: d["time"] = time
    if loc: d["location_id"] = loc
    if ko: d["science_ko_refs"] = ko
    facts.append(d)
F("f_rain_recorded", "محطة الرصد سجّلت نحو 12 ملم من الهطول ليلة الأربعاء، والسماء كانت صافية.", "state", ["obj_station"], 0)
F("f_roof_rule", "قواعد النادي تمنع الصعود إلى السطح بعد السادسة مساءً دون إذن المشرف.", "state", ["loc_roof"], 0)
F("f_single_gate", "بعد الثامنة مساءً تُغلق كل الأبواب عدا البوابة الرئيسية التي تسجّل الدخول والخروج بالبطاقات.", "state", ["loc_gate"], 0)
F("f_deadline", "يجب تسليم بيانات الشهر إلى مختبر المنظار الساعة العاشرة صباح الخميس.", "state", ["org_manzar"], 0)
F("f_power_cut", "انقطعت الكهرباء عن المدرسة 25 دقيقة مساء الاثنين.", "event", ["obj_station"], 1, T(-3060, "exact", -3035))
F("f_station_clock_lag", "ساعة المحطة متوقفة 25 دقيقة منذ انقطاع الاثنين ولم تُضبط، فهي متأخرة 25 دقيقة عن توقيت الشبكة.", "state", ["obj_station"], 2, None, None, ["KO-FC-04-024"])
F("f_true_window", "دخل الماء مقياس المطر بين 21:56 و22:14 بتوقيت الشبكة.", "event", ["obj_gauge"], 2, T(56, "exact", 74), "loc_roof", ["KO-FC-04-024"])
F("f_lama_left", "خرجت لمى من البوابة الساعة 21:15.", "event", ["lama"], 1, T(15), "loc_gate")
F("f_participants_left", "خرج بقية مشاركي الورشة بين 21:45 و21:50، ولم يدخل أحد بعد 20:30.", "event", ["loc_hall"], 1, T(45, "exact", 50), "loc_gate")
F("f_hoodie_common", "وُزّعت سترة الورشة الزرقاء على المشاركين الثلاثين كلهم، ومنهم ماجد وزياد.", "attribute", ["obj_hoodie"], 0, None, None, ["KO-FC-04-011"])
F("f_ziad_rehearsal", "تدرّب زياد وحده على عرض فريقه في غرفة الموسيقى بين 21:20 و21:44.", "event", ["ziad"], 1, T(20, "exact", 44), "loc_music_room")
F("f_ziad_left", "انصرف زياد من قاعة الورشة مع والده 21:47 وخرج من البوابة 21:48.", "event", ["ziad"], 1, T(47, "exact", 48), "loc_gate")
F("f_roof_opened_code", "فُتح باب السطح برمز الصيانة 21:52 وأُغلق 22:17؛ الرمز مسجل للمى وماجد.", "event", ["loc_roof"], 2, T(52, "exact", 77), "loc_roof")
F("f_majed_on_roof", "كان ماجد على السطح من 21:52 إلى 22:17.", "event", ["majed"], 2, T(52, "exact", 77), "loc_roof")
F("f_majed_plan", "كتب ماجد في دفتره خطة «تجربة رشّ ليلية لمؤقت السقاية — 9:50 — صنبور السطح».", "state", ["majed"], 1)
F("f_timer_installed", "مؤقت سقاية يحمل اسم ماجد مركّب على صنبور السطح، وشاشته تعرض أن آخر تشغيل استمر 18 دقيقة.", "state", ["obj_timer"], 1, None, "loc_roof")
F("f_hose_majed", "شغّل ماجد خرطوم الصنبور عبر مؤقته 18 دقيقة، ووصل الرذاذ إلى مقياس المطر.", "event", ["majed", "obj_timer", "obj_gauge"], 3, T(56, "exact", 74), "loc_roof")
F("f_majed_exit", "خرج ماجد من البوابة الساعة 22:21.", "event", ["majed"], 1, T(81), "loc_gate")
F("f_no_city_rain", "لم تسجل أي من محطات مرصد القنطرة الاثنتي عشرة هطولاً ليلة الأربعاء، والسماء صافية.", "state", ["org_observatory"], 1)
F("f_water_in_bottle", "قارورة التجميع أسفل المقياس فيها ماء حقيقي حتى علامة 12 ملم تقريباً.", "state", ["obj_gauge"], 1)
F("f_wet_patch", "في 22:31 كانت أرضية السطح جافة إلا بقعة مبللة تمتد من الصنبور إلى قاعدة المقياس.", "state", ["loc_roof"], 1, T(91), "loc_roof")
F("f_wadad_heard", "سمعت السيدة وداد صوت ماء فوق السقف وهي في ممر الطابق الأخير.", "event", ["wadad"], 1, T(65), "loc_top_corridor")
F("f_wadad_saw", "رأت السيدة وداد شاباً بسترة الورشة الزرقاء ينزل من درج السطح نحو 22:18.", "event", ["wadad", "majed"], 1, T(78), "loc_top_corridor")
F("f_wadad_exit", "خرجت السيدة وداد من البوابة الساعة 22:40.", "event", ["wadad"], 1, T(100), "loc_gate")

claims = [
    {"id": "cl_majed_club_room", "statement_ar": "بقيت في غرفة النادي أرتّب الأجهزة ثم خرجت نحو التاسعة والنصف، ولم أصعد إلى السطح.", "kind": "lie", "held_by": ["majed"], "true_fact_id": "f_majed_on_roof",
     "contradicted_by_evidence_ids": ["ev_gate_log", "ev_roof_door_log", "ev_majed_notebook", "ev_workshop_signout"]},
    {"id": "cl_ziad_whole_time", "statement_ar": "كنت في قاعة الورشة طوال الوقت حتى خرجت مع أبي.", "kind": "half_truth", "held_by": ["ziad"], "true_fact_id": "f_ziad_rehearsal",
     "contradicted_by_evidence_ids": ["ev_ziad_recording"]},
    {"id": "cl_wadad_time", "statement_ar": "سمعت الماء ورأيت الشاب ينزل قرابة العاشرة والنصف.", "kind": "honest_mistake", "held_by": ["wadad"], "true_fact_id": "f_wadad_saw",
     "contradicted_by_evidence_ids": ["ev_chat_alerts", "ev_roof_door_log"]},
]

timeline = [
    {"id": "t_power_cut", "description_ar": "انقطاع كهرباء عام في الحي مساء الاثنين؛ تتوقف ساعة المحطة 25 دقيقة.", "time": T(-3060, "exact", -3035), "actor_ids": [], "fact_ids": ["f_power_cut", "f_station_clock_lag"]},
    {"id": "t_lama_exit", "description_ar": "لمى تخرج من البوابة.", "time": T(15), "location_id": "loc_gate", "actor_ids": ["lama"], "fact_ids": ["f_lama_left"], "motivated_by_ar": "أنهت مهمتها في الورشة وعادت إلى البيت."},
    {"id": "t_ziad_rehearse", "description_ar": "زياد يتدرّب وحده على العرض ويسجّل صوته على اللوحي.", "time": T(20, "exact", 44), "location_id": "loc_music_room", "actor_ids": ["ziad"], "fact_ids": ["f_ziad_rehearsal"], "motivated_by_ar": "يخجل من التحدث أمام اللجنة ولا يريد أن يراه أحد وهو يتدرب."},
    {"id": "t_participants_exit", "description_ar": "بقية المشاركين يخرجون من البوابة.", "time": T(45, "exact", 50), "location_id": "loc_gate", "actor_ids": [], "fact_ids": ["f_participants_left"]},
    {"id": "t_ziad_signout", "description_ar": "زياد يوقّع ورقة الانصراف ويستلمه والده.", "time": T(47), "location_id": "loc_hall", "actor_ids": ["ziad"], "fact_ids": ["f_ziad_left"], "motivated_by_ar": "وصل والده لاصطحابه."},
    {"id": "t_ziad_exit", "description_ar": "زياد يخرج من البوابة.", "time": T(48), "location_id": "loc_gate", "actor_ids": ["ziad"], "fact_ids": ["f_ziad_left"], "motivated_by_ar": "يغادر مع والده."},
    {"id": "t_majed_opens_roof", "description_ar": "ماجد يفتح باب السطح برمز الصيانة.", "time": T(52), "location_id": "loc_roof", "actor_ids": ["majed"], "fact_ids": ["f_roof_opened_code", "f_majed_on_roof"], "motivated_by_ar": "أراد تجربة مؤقت السقاية الذي صنعه قبل أن يعرضه على الفريق."},
    {"id": "t_hose_run", "description_ar": "ماجد يشغّل الخرطوم عبر المؤقت 18 دقيقة؛ الرذاذ يصل إلى المقياس دون أن ينتبه.", "time": T(56, "exact", 74), "location_id": "loc_roof", "actor_ids": ["majed"], "fact_ids": ["f_hose_majed", "f_true_window"], "motivated_by_ar": "تجربة يدوية لمدى رشّ المؤقت.", "caused_by_event_ids": ["t_majed_opens_roof"]},
    {"id": "t_station_records", "description_ar": "المحطة تسجّل «هطولاً» بساعتها المتأخرة (21:31–21:49) وترسل تنبيهين إلى دردشة الفريق بتوقيت الخادم (21:56 و22:14).", "time": T(56, "exact", 74), "location_id": "loc_roof", "actor_ids": [], "fact_ids": ["f_rain_recorded"], "caused_by_event_ids": ["t_hose_run", "t_power_cut"]},
    {"id": "t_wadad_hears", "description_ar": "السيدة وداد تسمع صوت ماء فوق السقف.", "time": T(65), "location_id": "loc_top_corridor", "actor_ids": [], "witness_ids": ["wadad"], "fact_ids": ["f_wadad_heard"]},
    {"id": "t_majed_closes_roof", "description_ar": "ماجد يغلق باب السطح.", "time": T(77), "location_id": "loc_roof", "actor_ids": ["majed"], "fact_ids": ["f_roof_opened_code"], "motivated_by_ar": "انتهى من التجربة."},
    {"id": "t_majed_descends", "description_ar": "ماجد ينزل من درج السطح بسترة الورشة، وتراه وداد من الخلف.", "time": T(78), "location_id": "loc_top_corridor", "actor_ids": ["majed"], "witness_ids": ["wadad"], "fact_ids": ["f_wadad_saw"], "motivated_by_ar": "النزول بعد إنهاء التجربة."},
    {"id": "t_majed_exit", "description_ar": "ماجد يخرج من البوابة.", "time": T(81), "location_id": "loc_gate", "actor_ids": ["majed"], "fact_ids": ["f_majed_exit"], "motivated_by_ar": "العودة إلى البيت."},
    {"id": "t_wadad_photo", "description_ar": "وداد تفتح السطح ببطاقتها في جولة الإغلاق وتصوّر البقعة المبللة لتبلغ الصيانة.", "time": T(90, "exact", 93), "location_id": "loc_roof", "actor_ids": ["wadad"], "fact_ids": ["f_wet_patch"], "motivated_by_ar": "جولة الإغلاق المعتادة، وأرادت إبلاغ الصيانة بتسرّب محتمل."},
    {"id": "t_wadad_exit", "description_ar": "وداد تخرج من البوابة.", "time": T(100), "location_id": "loc_gate", "actor_ids": ["wadad"], "fact_ids": ["f_wadad_exit"], "motivated_by_ar": "انتهاء دوامها."},
    {"id": "t_morning_discovery", "description_ar": "لمى تكتشف «المطر» في البيانات صباح الخميس.", "time": T(630), "location_id": "loc_club_room", "actor_ids": ["lama"], "fact_ids": ["f_rain_recorded"], "motivated_by_ar": "تفقّد البيانات قبل التسليم."},
    {"id": "t_majed_denies", "description_ar": "ماجد يقول للمى إنه غادر نحو التاسعة والنصف ولم يصعد السطح.", "time": T(640), "location_id": "loc_club_room", "actor_ids": ["majed"], "fact_ids": [], "motivated_by_ar": "خاف أن يُستبعد الفريق لأنه خالف قاعدة السطح."},
]

ev = []
def V(id, title, kind, content, acts, supports, rel, limits, contradicts=None, red=False, ko=None, loc=None):
    d = {"id": id, "title_ar": title, "kind": kind, "content_ar": content, "acquired_by_action_ids": acts, "supports_fact_ids": supports, "reliability": rel, "limits_ar": limits}
    if contradicts: d["contradicts_claim_ids"] = contradicts
    if red: d["is_red_herring"] = True
    if ko: d["forensic_ko_ref"] = ko
    if loc: d["location_id"] = loc
    ev.append(d)
V("ev_station_log", "سجل محطة الرصد", "digital",
  "قراءات هطول متتالية بحسب ساعة المحطة من 21:31 إلى 21:49، مجموعها نحو 12 ملم. بقية الليلة صفر. لا يوجد في السجل ما يدل على مصدر الماء.",
  ["a_open_station_log"], ["f_rain_recorded"], "strong",
  "يسجل ما قاسه الجهاز بحسب ساعته الداخلية؛ لا يحدد مصدر الماء ولا من كان قرب المقياس، ولا يضمن أن ساعة الجهاز مضبوطة.", ko="KO-FC-04-024", loc="loc_club_room")
V("ev_lab_clock_offset", "نتيجة مختبر الخط الزمني الرقمي", "lab_result",
  "مقارنة ساعة المحطة اليوم بساعة الشبكة: المحطة متأخرة 25 دقيقة (±1 دقيقة). سجل أعطال المحطة يذكر انقطاع كهرباء 25 دقيقة مساء الاثنين، ولا يذكر ضبطاً للساعة بعده. (بيانات خيالية)",
  ["a_request_clock_lab"], ["f_station_clock_lag", "f_power_cut"], "strong",
  "يقيس الفرق اليوم فقط؛ افتراض أن الفرق كان نفسه ليلة الأربعاء يحتاج تأكيداً من مصدر مستقل يحمل توقيتاً آخر. ولا يقول شيئاً عمّن كان على السطح.", ko="KO-FC-04-024", loc="loc_club_room")
V("ev_chat_alerts", "تنبيهات المحطة في دردشة الفريق", "digital",
  "رسالتان آليتان من حساب المحطة في مجموعة الفريق: «بدء هطول» بتوقيت الخادم 21:56، و«توقف الهطول» 22:14.",
  ["a_read_club_chat"], ["f_true_window"], "strong",
  "توقيت الخادم يبيّن متى وصلت الرسالة لا ما سبّب القراءة؛ وقد يتأخر الإرسال قليلاً إن ضعف الاتصال.", contradicts=["cl_wadad_time"], ko="KO-FC-04-024")
V("ev_city_bulletin", "نشرة مرصد القنطرة", "documentary",
  "من محرك البحث داخل القضية: نشرة مرصد القنطرة ليوم الخميس — «لا هطول في أي من محطاتنا الاثنتي عشرة ليلة الأربعاء، وسماء صافية فوق المدينة».",
  ["a_search_city_bulletin"], ["f_no_city_rain"], "strong",
  "تغطي محطات المرصد لا سطح المدرسة نفسه؛ تجعل المطر فوق المدرسة بعيداً جداً لكنها لا تقيسه مباشرة.")
V("ev_collector_bottle", "قارورة التجميع", "physical",
  "القارورة الشفافة أسفل المقياس فيها ماء حتى علامة 12 ملم تقريباً، وعلى جدارها الخارجي قطرات جافة الأثر.",
  ["a_examine_gauge"], ["f_water_in_bottle"], "strong",
  "يثبت أن ماءً حقيقياً دخل المقياس، ولا يحدد مصدره ولا وقت دخوله.", loc="loc_roof")
V("ev_roof_photo", "صورة السطح من هاتف وداد", "digital",
  "صورة بتوقيت الشبكة 22:31: أرضية السطح جافة إلا بقعة مبللة تمتد من صنبور الحديقة إلى قاعدة المقياس؛ خرطوم ملفوف بجوار الصنبور، والقارورة الشفافة أسفل المقياس فيها ماء ظاهر.",
  ["a_get_wadad_photo"], ["f_wet_patch", "f_water_in_bottle"], "strong",
  "تُظهر لحظة 22:31 فقط؛ لا تُظهر من شغّل الخرطوم ولا متى بدأ البلل.", loc="loc_roof")
V("ev_gate_log", "سجل بطاقات البوابة", "digital",
  "سجل متزامن آلياً مع الشبكة: لا دخول بعد 20:30. خروج: لمى 21:15 — مشاركو الورشة بين 21:45 و21:50 (منهم زياد 21:48). ثم لا خروج آخر حتى: ماجد 22:21 — وداد 22:40.",
  ["a_request_gate_log"], ["f_lama_left", "f_participants_left", "f_ziad_left", "f_majed_exit", "f_wadad_exit"], "strong",
  "يثبت استخدام البطاقة لا هوية حاملها؛ ولا يقول شيئاً عمّا فعله أحد داخل المبنى.", contradicts=["cl_majed_club_room"], ko="KO-FC-04-024", loc="loc_gate")
V("ev_workshop_signout", "ورقة انصراف الورشة", "documentary",
  "ورقة يدوية بتوقيع منسق الورشة: «تسلّم المشاركون الثلاثون سترة الورشة الزرقاء». في الانصراف: «زياد — 9:47 — استلمه والده»، وآخر توقيع للمشاركين 9:50. ملاحظات الفريق المضيف: «لمى — 9:15 — انصرفت»، «ماجد — بقي لترتيب الأجهزة».",
  ["a_examine_signout"], ["f_ziad_left", "f_hoodie_common", "f_participants_left"], "moderate",
  "الأوقات مكتوبة بخط اليد وتعتمد على ساعة المنسق؛ تثبت الانصراف من القاعة كما سجله المنسق، لا ما حدث بعده.", contradicts=["cl_majed_club_room"], loc="loc_hall")
V("ev_roof_door_log", "سجل قفل باب السطح", "digital",
  "قفل إلكتروني متزامن مع الشبكة: فتح برمز الصيانة 21:52 — إغلاق 22:17 — فتح ببطاقة القيّمة 22:30 — إغلاق 22:33. رمز الصيانة مسجل لفريق المحطة: لمى وماجد.",
  ["a_request_roof_log"], ["f_roof_opened_code"], "strong",
  "يثبت استخدام الرمز لا هوية مستخدمه؛ من يعرف الرمز قد يكون أخبر به غيره.", contradicts=["cl_majed_club_room", "cl_wadad_time"], ko="KO-FC-04-024", loc="loc_roof")
V("ev_timer_device", "مؤقت السقاية على صنبور السطح", "physical",
  "جهاز صغير مركّب على صنبور السطح وموصول بالخرطوم، عليه ملصق «مشروع سقاية الحديقة — ماجد»، وشاشته تعرض «آخر تشغيل: 18 دقيقة».",
  ["a_search_roof"], ["f_timer_installed", "f_hose_majed"], "strong",
  "الملصق يدل على صاحب الجهاز لا على من شغّله؛ ومدة التشغيل لا تحدد وقته.", loc="loc_roof")
V("ev_majed_notebook", "صفحة من دفتر ماجد", "documentary",
  "في دفتر مشاريع ماجد بغرفة النادي: «تجربة رشّ ليلية لمؤقت السقاية — 9:50 — صنبور السطح — المدى 3 أمتار؟»",
  ["a_search_club_room"], ["f_majed_plan", "f_hose_majed"], "moderate",
  "الدفتر يثبت خطة لا تنفيذاً؛ الخطط قد تتغير أو تُؤجَّل.", contradicts=["cl_majed_club_room"], loc="loc_club_room")
V("ev_wadad_testimony", "إفادة السيدة وداد", "testimonial",
  "«وأنا أنظف ممر الطابق الأخير سمعت صوت ماء فوق السقف، ثم رأيت شاباً بسترة الورشة الزرقاء ينزل من درج السطح، قرابة العاشرة والنصف على ما أظن. لم أرَ وجهه.»",
  ["a_note_wadad"], ["f_wadad_heard", "f_wadad_saw"], "moderate",
  "الوقت تقدير من الذاكرة دون ساعة؛ ولم ترَ الوجه، والسترة لبسها المشاركون الثلاثون كلهم.", loc="loc_top_corridor")
V("ev_ziad_demeanour", "ملاحظة: سلوك زياد في المقابلة", "observation",
  "يجيب زياد باختصار، وينظر إلى الأرض أكثر مما ينظر إليك، ويسأل مرتين إن كان «سيُبلَّغ أهله».",
  ["a_note_ziad_manner"], [], "weak",
  "السلوك أثناء المقابلة ليس دليلاً على الصدق أو الكذب؛ للتوتر أسباب كثيرة لا علاقة لها بالحادثة.", red=True)
V("ev_ziad_recording", "ملف صوتي على لوحي غرفة الموسيقى", "digital",
  "ملف «تدريب_العرض» أُنشئ 21:20 وانتهى 21:44 بتوقيت الشبكة، فيه صوت يتدرّب على عرض مشروع «مدرسة النخيل».",
  ["a_examine_music_tablet"], ["f_ziad_rehearsal"], "moderate",
  "وجود الملف على الجهاز لا يثبت وحده من سجّله؛ والتعرف على الصوت بالأذن حكم تقريبي لا يقين.", contradicts=["cl_ziad_whole_time"], ko="KO-FC-04-024", loc="loc_music_room")

def P(t, i): return {"ref_type": t, "ref_id": i}
inf = []
def I(id, prem, ct, concl, rel, strength, rule, ks):
    inf.append({"id": id, "premises": prem, "conclusion": {"ref_type": ct, "ref_id": concl}, "relation": rel, "strength": strength, "rule_ar": rule, "skill_ko_refs": ks})
GK = P("general_knowledge", "gk_rain_wets_open_roof")
I("i_offset_window", [P("evidence", "ev_station_log"), P("evidence", "ev_lab_clock_offset")], "fact", "f_true_window", "establishes", "strong",
  "إذا كانت ساعة المحطة متأخرة 25 دقيقة فالقراءات المسجلة 21:31–21:49 حدثت فعلاً بين 21:56 و22:14 بتوقيت الشبكة.", ["KO-RS-06-017", "KO-RS-05-005"])
I("i_chat_window", [P("evidence", "ev_chat_alerts")], "fact", "f_true_window", "establishes", "strong",
  "رسالتا المحطة تحملان توقيت الخادم المضبوط، فالهطول المسجل بدأ 21:56 وتوقف 22:14.", ["KO-RS-06-017"])
I("i_no_city_rain", [P("evidence", "ev_city_bulletin")], "hypothesis", "h_real_rain", "rules_out", "strong",
  "لا مطر في أي محطة بالمدينة والسماء صافية، فالمطر الحقيقي فوق المدرسة وحدها مستبعد جداً.", ["KO-RS-06-001"])
I("i_dry_roof", [P("evidence", "ev_roof_photo"), GK], "hypothesis", "h_real_rain", "rules_out", "strong",
  "المطر يبلّل السطح المكشوف كله، والصورة تُظهر بللاً محصوراً بين الصنبور والمقياس.", ["KO-RS-06-001"])
I("i_real_water", [P("evidence", "ev_collector_bottle")], "hypothesis", "h_sensor_fault", "rules_out", "strong",
  "في القارورة ماء حقيقي بقدر القراءة تقريباً، فالقراءة ليست خللاً إلكترونياً اخترع مطراً.", ["KO-RS-06-001"])
I("i_wet_gauge", [P("evidence", "ev_roof_photo")], "hypothesis", "h_sensor_fault", "rules_out", "strong",
  "الصورة تُظهر ماءً في القارورة وبللاً عند قاعدة المقياس قبل الصباح، فالماء كان حاضراً فعلاً.", ["KO-RS-06-001"])
I("i_ziad_left_gate", [P("evidence", "ev_gate_log"), P("fact", "f_true_window")], "hypothesis", "h_ziad_sabotage", "rules_out", "strong",
  "خرج زياد من البوابة الوحيدة 21:48 ولم يدخل أحد بعدها، والماء دخل المقياس من 21:56؛ فلم يكن في المبنى وقتها.", ["KO-RS-06-017", "KO-RS-05-005"])
I("i_ziad_signed_out", [P("evidence", "ev_workshop_signout"), P("fact", "f_true_window")], "hypothesis", "h_ziad_sabotage", "rules_out", "strong",
  "انصرف زياد مع والده 9:47 بحسب المنسق، أي قبل بدء الهطول الفعلي 21:56 بتسع دقائق.", ["KO-RS-06-017"])
I("i_codeholder", [P("evidence", "ev_roof_door_log"), P("evidence", "ev_gate_log")], "fact", "f_majed_on_roof", "establishes", "strong",
  "الرمز للمى وماجد؛ لمى خرجت 21:15 قبل فتح الباب 21:52، ولا خروج بين 21:51 و22:20، فلم يكن في المبنى عند 21:52 إلا ماجد والقيّمة، والقيّمة تفتح ببطاقتها لا بالرمز.", ["KO-RS-05-005", "KO-RS-05-002"])
I("i_present_b", [P("evidence", "ev_workshop_signout"), P("evidence", "ev_wadad_testimony"), P("evidence", "ev_majed_notebook")], "fact", "f_majed_on_roof", "establishes", "strong",
  "الورقة تقول إن المشاركين انصرفوا بحلول 9:50 وبقي ماجد وحده، وهو من خطّط في دفتره لتجربة رشّ على السطح، ووداد رأت صاحب سترة ينزل من درج السطح بعد ذلك؛ فالأرجح أنه ماجد.", ["KO-RS-05-002", "KO-RS-06-001"])
I("i_hose_a", [P("fact", "f_majed_on_roof"), P("evidence", "ev_timer_device"), P("fact", "f_true_window")], "fact", "f_hose_majed", "establishes", "strong",
  "ماجد وحده كان على السطح، ومؤقته على الصنبور عمل 18 دقيقة، وهي مدة الهطول المسجل نفسها (21:56–22:14).", ["KO-RS-06-001", "KO-RS-06-017"])
I("i_hose_b", [P("fact", "f_majed_on_roof"), P("evidence", "ev_majed_notebook"), P("evidence", "ev_roof_photo"), P("fact", "f_true_window")], "fact", "f_hose_majed", "establishes", "strong",
  "خطة ماجد لتجربة رشّ من صنبور السطح نحو 9:50، والبلل يمتد من الصنبور إلى المقياس، والهطول بدأ 21:56؛ فالماء جاء من خرطوم تجربته.", ["KO-RS-06-001"])
I("i_support_majed_a", [P("fact", "f_majed_on_roof"), P("evidence", "ev_timer_device"), P("fact", "f_true_window")], "hypothesis", "h_majed_hose", "supports", "strong",
  "تشغيل خرطوم الصنبور في نافذة الهطول هو التفسير الذي يجمع وجود ماجد وحده على السطح ومدة تشغيل مؤقته مع مدة الهطول.", ["KO-RS-06-001"])
I("i_support_majed_b", [P("fact", "f_majed_on_roof"), P("evidence", "ev_majed_notebook"), P("evidence", "ev_roof_photo"), P("fact", "f_true_window")], "hypothesis", "h_majed_hose", "supports", "strong",
  "خطة التجربة في الدفتر والبلل الممتد من الصنبور إلى المقياس يجمعهما تفسير واحد: ماء الخرطوم في نافذة الهطول.", ["KO-RS-06-001"])
I("i_lure_ziad", [P("evidence", "ev_station_log"), P("evidence", "ev_wadad_testimony")], "hypothesis", "h_ziad_sabotage", "supports", "suggestive",
  "القراءة الساذجة: «المطر» بحسب ساعة المحطة 21:31–21:49 حين كان زياد ما يزال في المبنى، ووداد رأت شاباً بسترة الورشة؛ استدلال مغرٍ يسقط عند تصحيح الساعة وعند ملاحظة أن السترة لبسها ثلاثون.", ["KO-RS-06-001", "KO-RS-06-017"])
I("i_majed_claim_false", [P("evidence", "ev_gate_log")], "claim", "cl_majed_club_room", "contradicts_claim", "conclusive",
  "ماجد قال إنه خرج نحو 21:30، والبوابة سجلت خروجه 22:21.", ["KO-RS-05-007"])
I("i_ziad_claim_false", [P("evidence", "ev_ziad_recording")], "claim", "cl_ziad_whole_time", "contradicts_claim", "strong",
  "زياد قال إنه بقي في القاعة، والملف يضعه في غرفة الموسيقى 21:20–21:44؛ كذبته تخص التدريب لا المقياس.", ["KO-RS-05-007"])
I("i_wadad_time_off", [P("evidence", "ev_chat_alerts")], "claim", "cl_wadad_time", "contradicts_claim", "strong",
  "الماء توقف 22:14 بحسب الخادم، فتقدير «العاشرة والنصف» متأخر؛ خطأ صادق في تقدير الوقت لا كذب.", ["KO-RS-05-005"])

K = lambda f, a, c=None: ({"fact_id": f, "access": a} if c is None else {"fact_id": f, "access": a, "certainty": c})
reveal_majed = {"any": [{"presented": {"evidence_id": e, "to_character": "majed"}} for e in ("ev_roof_door_log", "ev_majed_notebook", "ev_gate_log", "ev_timer_device")]}
ck = [
    {"character_id": "lama", "knows": [K("f_rain_recorded", "witnessed"), K("f_lama_left", "witnessed"), K("f_deadline", "common_knowledge"), K("f_roof_rule", "common_knowledge"), K("f_hoodie_common", "witnessed")],
     "hides": [], "believes": [], "opinions_ar": ["أظن أن فريق مدرسة النخيل يغار منا."]},
    {"character_id": "majed", "knows": [K("f_roof_rule", "common_knowledge"), K("f_majed_exit", "witnessed"), K("f_majed_plan", "witnessed"), K("f_hoodie_common", "witnessed")],
     "hides": [{"fact_id": "f_majed_on_roof", "reveal_when": reveal_majed, "cover_claim_id": "cl_majed_club_room", "reveal_line_id": "mj_reveal"},
               {"fact_id": "f_hose_majed", "reveal_when": reveal_majed, "cover_claim_id": "cl_majed_club_room", "reveal_line_id": "mj_reveal"}],
     "believes": [{"claim_id": "cl_majed_club_room", "stance": "deliberate_lie"}], "opinions_ar": ["ربما فعلها أحد من فريق النخيل."]},
    {"character_id": "ziad", "knows": [K("f_ziad_left", "witnessed"), K("f_hoodie_common", "witnessed")],
     "hides": [{"fact_id": "f_ziad_rehearsal", "reveal_when": {"presented": {"evidence_id": "ev_ziad_recording", "to_character": "ziad"}}, "cover_claim_id": "cl_ziad_whole_time", "reveal_line_id": "zd_reveal"}],
     "believes": [{"claim_id": "cl_ziad_whole_time", "stance": "deliberate_lie"}]},
    {"character_id": "wadad", "knows": [K("f_wadad_heard", "witnessed", "certain"), K("f_wadad_saw", "witnessed", "fairly_sure"), K("f_wet_patch", "witnessed"), K("f_wadad_exit", "witnessed"), K("f_single_gate", "professional")],
     "hides": [], "believes": [{"claim_id": "cl_wadad_time", "stance": "sincere"}]},
    {"character_id": "noor", "knows": [{"fact_id": "f_rain_recorded", "access": "told_by", "source_character_id": "lama"}, K("f_deadline", "professional"), K("f_power_cut", "professional")], "hides": [], "believes": []},
    {"character_id": "yusuf", "knows": [K("f_rain_recorded", "common_knowledge"), K("f_deadline", "common_knowledge")], "hides": [], "believes": [],
     "opinions_ar": ["زياد بدا متوتراً جداً — هل هذا يعني شيئاً؟ (فرضية لا دليل)"]},
]
hyps = [
    {"id": "h_ziad_sabotage", "statement_ar": "زياد صبّ ماءً في المقياس ليُفسد بيانات فريق منافس.", "is_true": False, "plausibility_at_start": "high", "suspect_id": "ziad"},
    {"id": "h_real_rain", "statement_ar": "أمطرت فعلاً فوق المدرسة وحدها.", "is_true": False, "plausibility_at_start": "medium"},
    {"id": "h_sensor_fault", "statement_ar": "عطل إلكتروني في الحساس سجّل مطراً لم يحدث.", "is_true": False, "plausibility_at_start": "medium"},
    {"id": "h_majed_hose", "statement_ar": "الماء جاء من خرطوم صنبور السطح الذي شغّله ماجد في تجربة مؤقته.", "is_true": True, "plausibility_at_start": "low", "suspect_id": "majed"},
]
mis = [
    {"id": "rh_ziad_nervous", "points_to_hypothesis_id": "h_ziad_sabotage", "planted_via_ar": "زياد منافس، ويبدو متوتراً ويكذب بشأن مكانه، وساعة المحطة غير المصححة تضع «المطر» في وقت كان فيه داخل المبنى.",
     "evidence_ids": ["ev_ziad_demeanour", "ev_station_log"], "refuted_by_inference_ids": ["i_ziad_left_gate", "i_ziad_signed_out"],
     "fairness_note_ar": "المعلومة الظاهرة (توقيت المحطة) تُساء قراءتها ولا تُحجب؛ تصحيح الساعة متاح بطريقين، وكذبة زياد لها دافع بريء يُكشف بالملف الصوتي، والتوتر مُعلَّم في الواجهة «ملاحظة لا دليل»."},
    {"id": "rh_hoodie", "points_to_hypothesis_id": "h_ziad_sabotage", "planted_via_ar": "وداد رأت «شاباً بسترة الورشة الزرقاء»، وزياد كان يلبسها.",
     "evidence_ids": ["ev_wadad_testimony"], "refuted_by_inference_ids": ["i_ziad_left_gate", "i_ziad_signed_out"],
     "fairness_note_ar": "السترة صفة مشتركة بين ثلاثين مشاركاً (العدد مذكور في ورقة الانصراف)، فهي غير مميِّزة؛ ووقت الرؤية الفعلي بعد خروج زياد."},
]
def levels(d): return [{"score": i, "descriptor_ar": t} for i, t in enumerate(d)]
los = [
    {"id": "lo_timeline", "statement_ar": "يعيد بناء الخط الزمني بتصحيح فرق ساعة جهاز، ويكشف التعارض بين مصدرين زمنيين قبل أن يحكم.", "skill_ko_ref": "KO-RS-06-017",
     "observable_behaviors_ar": ["يضع نافذة الهطول المصححة (21:56–22:14) على الخط الزمني", "يوسم تعارض «ساعة المحطة مقابل توقيت الخادم» دون تلميح", "يستبعد زياد بربط خروجه بالنافذة المصححة"], "evidence_sources": ["timeline_task", "evidence_board", "hypothesis_ledger"]},
    {"id": "lo_diagnostic", "statement_ar": "يميز الدليل المميِّز من غير المميِّز، فلا يبني الاتهام على صفة يشترك فيها كثيرون.", "skill_ko_ref": "KO-RS-06-001",
     "observable_behaviors_ar": ["يوسم إفادة السترة بأنها «لا تميّز بين المشتبه بهم»", "لا يرفق السترة بدعم أي فرضية في التقرير الختامي", "يستشهد بدليل مميِّز (المؤقت، سجل الباب، الدفتر) لدعم الفرضية الصحيحة"], "evidence_sources": ["evidence_board", "final_justification"]},
    {"id": "lo_lie_cues", "statement_ar": "يرفض استخدام التوتر دليلاً على الكذب، ويحوّل الشك إلى مطابقة الإفادة بدليل مستقل.", "skill_ko_ref": "KO-RS-05-007",
     "observable_behaviors_ar": ["لا يثبّت ملاحظة سلوك زياد دليلاً داعماً", "يعرض دليلاً مستقلاً على زياد أو ماجد بدل الضغط", "يفسّر كذبتي ماجد وزياد بدافعيهما دون أن يعدّ الكذبة وحدها دليل فعل"], "evidence_sources": ["action_log", "evidence_board", "final_justification"]},
    {"id": "lo_hyp", "statement_ar": "يوازن بين فرضيتين على الأقل ويستبعد ما تنقضه الأدلة.", "skill_ko_ref": "KO-RS-05-002", "observable_behaviors_ar": ["يضيف فرضيات", "يستبعد بدليل"], "evidence_sources": ["hypothesis_ledger"]},
    {"id": "lo_calib", "statement_ar": "يصوغ نسبة الترجيح بحدودها.", "skill_ko_ref": "KO-RS-06-021", "observable_behaviors_ar": ["يختار ثقة معقولة", "يذكر حدوداً"], "evidence_sources": ["final_justification"]},
    {"id": "lo_revise", "statement_ar": "يراجع رأيه الأول حين يظهر ما يخالفه.", "skill_ko_ref": "KO-RS-06-009", "observable_behaviors_ar": ["يغيّر فرضيته الرائدة بدليل"], "evidence_sources": ["hypothesis_ledger"]},
]
rub = {
    "reference_answer_ar": "لم تمطر. ساعة المحطة متأخرة 25 دقيقة، فالهطول الحقيقي كان 21:56–22:14 (يؤكده المختبر مع سجل المحطة، أو تنبيهات الخادم وحدها). زياد خرج 21:48 قبل ذلك، والسترة صفة مشتركة والتوتر ليس دليلاً. باب السطح فُتح برمز لمى وماجد 21:52 ولمى كانت قد خرجت، ومؤقت ماجد عمل 18 دقيقة بمقدار نافذة الهطول نفسها (أو: دفتر خطته مع صورة البلل من الصنبور). نشرة المرصد وصورة السطح تستبعدان المطر، والقارورة تستبعد العطل. نسبة الترجيح: مرجّح جداً. ما لا تثبته الأدلة: نية التخريب — الأرجح أنها تجربة غير مقصودة.",
    "criteria": [
        {"id": "c_source", "name_ar": "تصنيف المصادر", "objective_ids": ["lo_diagnostic"], "scored_by": "deterministic", "weight": 0.15, "levels": levels(["لم يصنّف", "أخطأ في الأغلب", "نصف صحيح", "معظمه صحيح", "كله صحيح"])},
        {"id": "c_conflict", "name_ar": "تصحيح نافذة الزمن على الخط الزمني", "objective_ids": ["lo_timeline"], "scored_by": "deterministic", "weight": 0.25, "levels": levels(["لم يضع شيئاً", "وضع قليلاً", "وضع نصفها صحيحاً", "معظمها", "كلها في موضعها"])},
        {"id": "c_links", "name_ar": "ربط الأدلة بالفرضيات", "objective_ids": ["lo_diagnostic", "lo_lie_cues"], "scored_by": "deterministic", "weight": 0.15, "levels": levels(["لا روابط", "قليلة", "نصفها صحيح", "معظمها", "كلها دقيقة"])},
        {"id": "c_uncertainty", "name_ar": "معايرة الثقة", "objective_ids": ["lo_calib"], "scored_by": "deterministic", "weight": 0.15, "levels": levels(["ثقة مفرطة", "حدود قليلة", "جزئية", "معقولة", "معايَرة كاملة"])},
        {"id": "c_revision", "name_ar": "مراجعة الرأي", "objective_ids": ["lo_revise"], "scored_by": "deterministic", "weight": 0.1, "levels": levels(["بقي على فرضية مرفوضة", "لم يعلن فرضية", "ثبت على فرضية سليمة", "غيّر بدليل", "غيّر بدليل ووثّق"])},
        {"id": "c_elimination", "name_ar": "استبعاد الفرضيات الخاطئة", "objective_ids": ["lo_hyp"], "scored_by": "deterministic", "weight": 0.1, "levels": levels(["لم يستبعد", "استبعد خطأً", "فرضية بدليل", "فرضيتين", "كل الخاطئة"])},
        {"id": "c_justification", "name_ar": "جودة الحجة المكتوبة", "objective_ids": ["lo_timeline", "lo_diagnostic", "lo_lie_cues"], "scored_by": "human", "weight": 0.1, "levels": levels(["لا حجة", "ادعاء بلا سند", "أدلة دون ربط", "ربط الأدلة بالاستنتاج", "ربط مع البدائل والحدود"])},
    ],
}
def H(id, lv, kind, text, trig, target=None, w=0.0):
    d = {"id": id, "level": lv, "kind": kind, "text_ar": text, "trigger": trig, "assessment_weight": w}
    if target: d["targets_inference_id"] = target
    return d
he = lambda e: {"has_evidence": e}
al = {"always": True}
hints = [
    H("hn_general_1", 1, "metacognitive", "ما الذي تعرفه بالمشاهدة، وما الذي استنتجته؟ اكتب الاثنين منفصلين.", al, None, 0.0),
    H("hn_win_1", 1, "metacognitive", "كل جهاز يحمل ساعته الخاصة. هل كل الساعات في هذه القضية تقول الشيء نفسه؟", he("ev_station_log"), "i_offset_window", 0.0),
    H("hn_win_2", 2, "focus_area", "قارن وقت «المطر» في سجل المحطة بوقت أي مصدر آخر يحمل توقيت الشبكة.", {"not": he("ev_lab_clock_offset")}, "i_offset_window", 0.02),
    H("hn_win_3", 3, "pointer", "مختبر المنظار يستطيع مقارنة ساعة المحطة بساعة الشبكة. وتنبيهات المحطة في دردشة الفريق تحمل توقيت الخادم.", he("ev_station_log"), "i_offset_window", 0.05),
    H("hn_win_4", 4, "partial_reveal", "ساعة المحطة متأخرة 25 دقيقة. أضفها إلى كل قراءة: متى حدث «المطر» فعلاً؟", he("ev_station_log"), "i_offset_window", 0.08),
    H("hn_win_5", 5, "full_reveal", "الهطول الفعلي كان بين 21:56 و22:14 بتوقيت الشبكة، لأن ساعة المحطة توقفت 25 دقيقة يوم الاثنين ولم تُضبط.", he("ev_station_log"), "i_offset_window", 0.1),
    H("hn_ziad_1", 1, "metacognitive", "التوتر يحتاج تفسيراً، لكنه ليس دليلاً. ما الذي يضع شخصاً في مكان ما في وقت ما؟", he("ev_ziad_demeanour"), "i_ziad_left_gate", 0.0),
    H("hn_ziad_2", 2, "focus_area", "للمدرسة ليلاً بوابة واحدة. أي سجل يعرف متى خرج كل شخص؟", {"not": he("ev_gate_log")}, "i_ziad_left_gate", 0.02),
    H("hn_ziad_3", 3, "pointer", "ضع خروج زياد ونافذة الهطول المصححة على الخط الزمني نفسه.", he("ev_gate_log"), "i_ziad_left_gate", 0.05),
    H("hn_code_1", 1, "metacognitive", "من كان يستطيع الوصول إلى السطح في نافذة الهطول، لا من كان يرغب في ذلك؟", al, "i_codeholder", 0.0),
    H("hn_code_2", 2, "focus_area", "باب السطح إلكتروني. القيّمة تعرف أين يُحفظ سجله.", {"not": he("ev_roof_door_log")}, "i_codeholder", 0.02),
    H("hn_code_3", 3, "pointer", "الرمز لشخصين فقط. قارن وقت فتح الباب بأوقات خروجهما من البوابة.", he("ev_roof_door_log"), "i_codeholder", 0.05),
]

A = []
def Act(id, typ, label, pre, effects, target=None, tel=None, cost=1):
    d = {"id": id, "type": typ, "label_ar": label, "precondition": pre, "effects": effects, "time_cost_units": cost}
    if target: d["target_id"] = target
    if tel: d["telemetry_code"] = tel
    A.append(d)
G = lambda e: {"op": "grant_evidence", "ref_id": e}
U = lambda f: {"op": "unlock_fact", "ref_id": f}
fu = lambda f: {"fact_unlocked": f}
Act("a_open_station_log", "examine", "افتح سجل المحطة", al, [G("ev_station_log")], "obj_station", "OPEN_STATION_LOG")
Act("a_request_clock_lab", "request_lab_test", "اطلب من مختبر المنظار مقارنة ساعة المحطة بساعة الشبكة", he("ev_station_log"), [G("ev_lab_clock_offset")], "obj_station", "LAB_CLOCK_OFFSET")
Act("a_read_club_chat", "examine", "اقرأ دردشة الفريق (بإذن لمى)", al, [G("ev_chat_alerts")], "lama", "READ_CLUB_CHAT")
Act("a_search_city_bulletin", "examine", "ابحث في أرشيف مرصد القنطرة", al, [G("ev_city_bulletin")], "org_observatory", "SEARCH_CITY_BULLETIN")
Act("a_examine_gauge", "examine", "افحص مقياس المطر وقارورته", al, [G("ev_collector_bottle")], "obj_gauge", "EXAMINE_GAUGE")
Act("a_search_roof", "search_location", "تفقّد السطح مع السيدة وداد", al, [G("ev_timer_device")], "loc_roof", "SEARCH_ROOF")
Act("a_search_club_room", "search_location", "تفقّد غرفة النادي", al, [G("ev_majed_notebook")], "loc_club_room", "SEARCH_CLUB_ROOM")
Act("a_examine_signout", "examine", "اطلع على ورقة انصراف الورشة", al, [G("ev_workshop_signout")], "loc_hall", "EXAMINE_SIGNOUT")
Act("a_request_gate_log", "examine", "اطلب سجل بطاقات البوابة من الإدارة", al, [G("ev_gate_log")], "loc_gate", "REQUEST_GATE_LOG")
Act("a_request_roof_log", "examine", "اطلب من القيّمة سجل قفل باب السطح", {"any": [he("ev_station_log"), he("ev_timer_device"), he("ev_wadad_testimony")]}, [G("ev_roof_door_log")], "wadad", "REQUEST_ROOF_LOG")
for cid, lab, pre in [("lama", "لمى", al), ("majed", "ماجد", al), ("ziad", "زياد", al), ("wadad", "السيدة وداد", al), ("noor", "م. نور", he("ev_station_log")), ("yusuf", "يوسف", al)]:
    Act(f"a_int_{cid}", "interview", f"ابدأ مقابلة {lab}", pre, [{"op": "raise_trust", "ref_id": cid, "amount": 1}], cid, f"INT_{cid.upper()}")
Act("a_note_wadad", "examine", "دوّن إفادة السيدة وداد", fu("f_wadad_saw"), [G("ev_wadad_testimony")], "wadad", "NOTE_WADAD")
Act("a_get_wadad_photo", "interview", "اطلب من وداد صورة البقعة المبللة", fu("f_wet_patch"), [G("ev_roof_photo")], "wadad", "WADAD_PHOTO")
Act("a_note_ziad_manner", "examine", "دوّن ملاحظة عن سلوك زياد في المقابلة", fu("f_ziad_left"), [G("ev_ziad_demeanour")], "ziad", "NOTE_ZIAD_MANNER")
Act("a_examine_music_tablet", "search_location", "تفقّد غرفة الموسيقى", {"any": [he("ev_ziad_demeanour"), he("ev_workshop_signout")]}, [G("ev_ziad_recording")], "loc_music_room", "EXAMINE_MUSIC_TABLET")
for e, t, c in [("ev_ziad_recording", "الملف الصوتي", "ziad"), ("ev_gate_log", "سجل البوابة", "majed"), ("ev_roof_door_log", "سجل باب السطح", "majed"), ("ev_majed_notebook", "صفحة الدفتر", "majed"), ("ev_timer_device", "صورة المؤقت", "majed")]:
    Act(f"p_{e[3:]}_{c}", "present_evidence", f"اعرض {t} على {'زياد' if c == 'ziad' else 'ماجد'}", {"presented": {"evidence_id": e, "to_character": c}}, [{"op": "emit_event", "ref_id": f"PRESENTED_{e[3:].upper()}"}], c, f"P_{e[3:].upper()}_{c.upper()}", 0)
Act("a_hint", "request_hint", "أحتاج مساعدة", al, [], None, "REQUEST_HINT", 0)
Act("a_accuse", "final_accusation", "قدّم تقريرك في «غرفة التحرير»", al, [{"op": "emit_event", "ref_id": "SUBMIT"}], None, "FINAL_ACCUSATION", 0)

topics = [
    {"id": "t_night", "label_ar": "ماذا فعلت بعد الورشة؟", "example_questions_ar": ["احكِ لي ما فعلته بعد الورشة من البداية.", "أين كنت أثناء الورشة؟"], "fact_ids": ["f_ziad_rehearsal", "f_majed_on_roof", "f_hose_majed"], "claim_ids": ["cl_majed_club_room", "cl_ziad_whole_time"]},
    {"id": "t_leaving", "label_ar": "متى غادرت المدرسة؟", "example_questions_ar": ["متى غادرت المدرسة؟", "متى خرجت من البوابة؟"], "fact_ids": ["f_lama_left", "f_ziad_left", "f_majed_exit", "f_wadad_exit"], "claim_ids": ["cl_majed_club_room"]},
    {"id": "t_roof", "label_ar": "السطح ومقياس المطر", "example_questions_ar": ["من يستطيع فتح باب السطح؟", "ماذا يوجد قرب المقياس؟"], "fact_ids": ["f_roof_rule", "f_wet_patch", "f_majed_on_roof", "f_hose_majed"], "claim_ids": ["cl_majed_club_room"]},
    {"id": "t_heard", "label_ar": "ما سمعته وما رأيته", "example_questions_ar": ["ماذا سمعتِ بالضبط؟", "كيف عرفتِ الوقت؟"], "fact_ids": ["f_wadad_heard", "f_wadad_saw"], "claim_ids": ["cl_wadad_time"]},
    {"id": "t_hoodie", "label_ar": "سترة الورشة", "example_questions_ar": ["كم شخصاً لبس هذه السترة؟"], "fact_ids": ["f_hoodie_common"], "claim_ids": []},
    {"id": "t_station", "label_ar": "المحطة والبيانات المسجلة", "example_questions_ar": ["ماذا سجّلت المحطة؟", "ما الذي حدث للمحطة قبل الأربعاء؟", "هل ساعة المحطة مضبوطة؟"], "fact_ids": ["f_rain_recorded", "f_power_cut"], "claim_ids": []},
]
# declarative mirrors of dialogue unlocks (hidden from play; telemetry ASK_*)
_pre = {a["target_id"]: a["precondition"] for a in A if a["type"] == "interview" and a["id"].startswith("a_int_")}
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
    (1, "نشرة المرصد: لا مطر في المدينة كلها. وصورة وداد: البلل محصور بين الصنبور والمقياس. إذن لم تمطر.", ["ev_city_bulletin", "ev_roof_photo"], "i_no_city_rain"),
    (2, "القارورة فيها ماء حقيقي بقدر القراءة؛ فليست القراءة عطلاً اخترع مطراً.", ["ev_collector_bottle"], "i_real_water"),
    (3, "ساعة المحطة متأخرة 25 دقيقة منذ انقطاع الاثنين: «21:31–21:49» تعني فعلاً 21:56–22:14. وتنبيهات الخادم تقول الشيء نفسه من طريق مستقل.", ["ev_station_log", "ev_lab_clock_offset", "ev_chat_alerts"], "i_offset_window"),
    (4, "زياد خرج 21:48، قبل بدء الرش بثماني دقائق. توتره وكذبته كانا عن تدريبه السري، لا عن المقياس.", ["ev_gate_log", "ev_workshop_signout", "ev_ziad_recording"], "i_ziad_left_gate"),
    (5, "باب السطح فُتح برمز لمى وماجد 21:52، ولمى خرجت 21:15؛ لم يبقَ إلا ماجد.", ["ev_roof_door_log", "ev_gate_log"], "i_codeholder"),
    (6, "مؤقت ماجد عمل 18 دقيقة، وهي مدة الهطول نفسها؛ ودفتره يخطط لتجربة رشّ من صنبور السطح.", ["ev_timer_device", "ev_majed_notebook"], "i_hose_a"),
]
ending = {
    "steps": [{"order": o, "text_ar": t, "uses_evidence_ids": u, "inference_id": i} for o, t, u, i in steps],
    "alternative_paths_ar": [
        "المسار (ب) دون المختبر ودون سجل البوابة: تنبيهات الخادم + ورقة الانصراف + إفادة وداد + دفتر ماجد + صورة وداد تكفي للحل بنسبة ترجيح «مرجّح جداً».",
        "لاعب بدأ بالمختبر أولاً يصل إلى النافذة المصححة قبل أن يقابل أحداً؛ هذا ترتيب مقبول بالكامل."],
    "what_evidence_could_not_show_ar": [
        "لا يثبت أي دليل أن ماجد قصد التخريب؛ الأدلة تتسق أكثر مع تجربة غير مقصودة.",
        "سجل البوابة وسجل الباب يثبتان استخدام بطاقة ورمز، لا هوية صاحب اليد؛ القوة جاءت من اجتماع الأدلة.",
        "السترة الزرقاء لم تميّز أحداً: لبسها ثلاثون شخصاً."],
    "science_notes_ar": [
        "الأدلة الرقمية موثوقة عند التطبيق السليم، لكن ساعة الجهاز قد تكون خاطئة، ووجود السجل لا يثبت من استخدم الجهاز.",
        "مقارنة مصدرين مستقلين بتوقيتين مختلفين (المختبر والخادم) أقوى من مصدر واحد، وهكذا تُبنى نسبة الترجيح.",
        "القرار العلمي الصحيح للفريق: وسم قراءات 21:56–22:14 بأنها ملوّثة وشرح السبب، لا حذفها بصمت ولا الإبقاء عليها.",
        "حين تُسلَّم البيانات إلى جهة أخرى تُسجَّل سلسلة العهدة: من حمل السجل ومتى، وما الذي تغيّر فيه."],
}
core = {
    "schema_version": "0.1.0", "case_id": CID, "case_version": "0.1.0",
    "meta": {"title_ar": "مطرٌ في ليلة صافية", "title_en": "Rain on a Clear Night", "age_band": "13-15", "locale": "ar", "dialogue_register": "msa", "estimated_minutes": 30, "difficulty": 2,
             "content_flags": ["no_violence", "science_lab"], "authors": ["فريق أثر التحريري (مسودة بمساعدة الذكاء الاصطناعي، عن قضية مرجعية من المكتبة، لم تُراجَع بشرياً بعد)"],
             "knowledge_object_refs": ["KO-RS-06-017", "KO-RS-06-001", "KO-RS-05-007", "KO-RS-05-005", "KO-RS-05-002", "KO-RS-06-009", "KO-RS-06-021", "KO-FC-04-024", "KO-FC-04-011"]},
    "premise": {"hook_ar": "سجّلت محطة الرصد على سطح المدرسة نحو 12 ملم من المطر ليلة الأربعاء، مع أن السماء كانت صافية فوق القنطرة كلها. وبيانات الشهر يجب أن تُسلَّم إلى مختبر «المنظار» في العاشرة صباحاً. لمى، قائدة الفريق، تشك في فريق مدرسة منافسة. والمطلوب: ماذا حدث فعلاً، ومن المسؤول، وما الذي نفعله بالبيانات؟",
                "player_role_ar": "متدرّب/ة في «شبكة الأثر» التطوعية، يعمل/تعمل مع نادي العلوم في المدرسة، بلا أي صلاحيات تأديبية أو أمنية",
                "setting_ar": "مدينة «القنطرة» المتخيّلة؛ «مدرسة ضفاف القنطرة الإعدادية» (متخيّلة)، صباح الخميس، بعد ورشة علمية مسائية مشتركة مع فريق «مدرسة النخيل» (متخيّلة). للمدرسة ليلاً بوابة واحدة تعمل بالبطاقات.",
                "public_fact_ids": ["f_rain_recorded", "f_roof_rule", "f_single_gate", "f_deadline"],
                "assumed_general_knowledge_ar": ["المطر الحقيقي يبلّل السطح المكشوف كله تقريباً، لا بقعة صغيرة حول صنبور ماء.", "الأجهزة المختلفة قد تحمل ساعات غير متطابقة، والساعة الشبكية للخادم هي المرجع داخل القضية.", "من خرج من البوابة الوحيدة ولم يدخل بعدها لم يعد في المبنى."]},
    "entities": {"characters": chars, "locations": locations, "objects": objects, "organizations": orgs},
    "truth": {"solution": {"culprit_ids": ["majed"],
                           "summary_ar": "لم تمطر. صعد ماجد إلى السطح برمز الصيانة الساعة 21:52 دون إذن المشرف ليجرّب مؤقت سقاية صنعه، فشغّل خرطوم الصنبور 18 دقيقة (21:56–22:14 بتوقيت الشبكة)، ووصل الرذاذ إلى مقياس المطر. ساعة المحطة متأخرة 25 دقيقة منذ انقطاع كهرباء يوم الاثنين، فسجّلت «المطر» بين 21:31 و21:49، وهي فترة كان زياد فيها داخل المبنى، فبدا الأمر كأنه فعله. لم يقصد ماجد التخريب، لكنه كذب خوفاً من استبعاد الفريق. زياد بريء: انصرف 21:47 وخرج 21:48، وتوتره سببه أنه كان يتدرّب سراً على العرض.",
                           "key_fact_ids": ["f_hose_majed", "f_true_window", "f_majed_on_roof"]},
              "facts": facts, "claims": claims},
    "timeline": timeline, "evidence": ev, "evidence_graph": {"inferences": inf},
    "character_knowledge": ck, "hypotheses": hyps, "misdirection_plan": mis, "learning_objectives": los,
    "mechanics": {"time_budget_units": 40, "actions": A},
    "state_machine": {"id": "c010", "initial": "briefing", "type": "compound", "states": {
        "briefing": {"description_ar": "الإحاطة", "type": "atomic", "on": {"START": {"target": "investigating"}}},
        "investigating": {"description_ar": "التحقيق", "type": "compound", "initial": "gathering",
                          "states": {"gathering": {"type": "atomic", "on": {"OPEN_DEDUCTION": {"target": "deducing"}}}, "deducing": {"type": "atomic", "on": {"BACK": {"target": "gathering"}}}},
                          "on": {"SUBMIT": {"target": "review"}}},
        "review": {"description_ar": "مراجعة", "type": "atomic", "on": {"CLOSE": {"target": "resolved"}}},
        "resolved": {"description_ar": "إغلاق", "type": "final"}}},
    "dialogue": {"max_turns_per_interview": 12, "llm_enabled": False, "topics": topics},
    "rubric": rub, "hint_ladder": hints,
    "fairness_test": {"requirements": {"min_disjoint_proof_paths": 2, "max_inference_depth": 2, "all_red_herrings_refutable": True, "culprit_uniquely_entailed": True, "no_hidden_fact_dependency": True, "max_required_actions": 12}, "runs": []},
    "ending_explanation": ending,
    "expert_review": [{"role": r, "reviewer": "—", "status": "pending", "content_hash": "unbound", "date": "2026-10-27", "notes_ar": "بانتظار مراجعة بشرية؛ لم يُجرَ أي اعتماد."} for r in
                      ["narrative_editor", "scientific_reviewer", "learning_designer", "age_appropriateness", "cultural_reviewer", "legal_rights", "safety"]],
}
ui = {
    "case_id": CID,
    "clock": {"epoch_hhmm": "21:00", "zone_label_ar": "توقيت الشبكة"},
    "cover": {"title_ar": "مطرٌ في ليلة صافية", "tagline_ar": "السماء صافية… والمقياس يقول إنها أمطرت", "kicker_ar": "ملف المدرسة · محطة السطح", "glyph": "☂", "accent": "cyan"},
    "cold_open_ar": ["صباح الخميس، قبل موعد التسليم بساعتين.", "على سطح المدرسة محطة صغيرة تقيس المطر، وقد كتبت في سجلها أنها أمطرت ليلة الأربعاء.", "لمى كانت تنظر إلى النجوم تلك الليلة، وتقول إن السماء لم تكن فيها غيمة واحدة.", "في ملفك سجلات بساعات مختلفة. ابدأ بسؤال بسيط: ماذا حدث، ومتى بالضبط؟"],
    "labs": [],
    "source_classes": [
        {"id": "primary_record", "label_ar": "سجل أصلي", "help_ar": "يُنتجه جهاز أو نظام لحظة الحدث دون وسيط، كسجل محطة أو سجل قفل."},
        {"id": "redisplay", "label_ar": "نسخة معروضة", "help_ar": "معلومة نُقلت أو أُعيد عرضها من سجل آخر."},
        {"id": "claim", "label_ar": "قول أو تصريح", "help_ar": "إفادة شخص؛ تُقاس بالسجلات لا بنبرة صاحبها."},
        {"id": "template", "label_ar": "قالب أو نموذج", "help_ar": "نص جاهز لا يصف الحدث الفعلي بذاته."},
        {"id": "public_document", "label_ar": "وثيقة منشورة", "help_ar": "وثيقة معلنة للعموم ومعروف ناشرها، كنشرة المرصد."}],
    "limit_menu": [
        {"id": "l_intent", "label_ar": "الأدلة لا تثبت أن ماجداً قصد إفساد البيانات"},
        {"id": "l_identity", "label_ar": "سجل الباب وسجل البوابة يثبتان استخدام رمز وبطاقة لا هوية صاحب اليد"},
        {"id": "l_clock_now", "label_ar": "فرق الساعة قيس اليوم، فيلزم مصدر مستقل يؤكد أنه كان كذلك ليلة الأربعاء"},
        {"id": "l_handwriting", "label_ar": "ورقة الانصراف مكتوبة بخط اليد وبساعة المنسق"},
        {"id": "l_invalid_demeanor", "label_ar": "توتر زياد في المقابلة يدل على أنه يكذب في كل شيء"},
        {"id": "l_invalid_hoodie", "label_ar": "ارتداء ماجد السترة الزرقاء يثبت أنه الفاعل"},
        {"id": "l_invalid_lie", "label_ar": "كذب ماجد وحده يكفي دليلاً على ما فعله"}],
    "mind_change_menu": [
        {"id": "m_other_user", "label_ar": "ثبوت أن شخصاً آخر استخدم رمز الصيانة الساعة 21:52"},
        {"id": "m_clock_fixed", "label_ar": "ثبوت أن ساعة المحطة ضُبطت بعد انقطاع الاثنين وقبل ليلة الأربعاء"},
        {"id": "m_timer_other_run", "label_ar": "ثبوت أن مؤقت السقاية شُغّل مرة أخرى بعد خروج ماجد"},
        {"id": "m_other_water", "label_ar": "ظهور مصدر ماء آخر على السطح غير الخرطوم في نافذة الهطول"},
        {"id": "m_popularity", "label_ar": "كثرة من يشكّون في فريق المدرسة المنافسة"}],
    "skills": [{"skill_id": "KO-RS-06-017", "track": "D"}, {"skill_id": "KO-RS-05-005", "track": "D"}, {"skill_id": "KO-RS-05-007", "track": "D"}, {"skill_id": "KO-RS-06-001", "track": "B"},
               {"skill_id": "KO-RS-05-002", "track": "B"}, {"skill_id": "KO-RS-06-009", "track": "D"}, {"skill_id": "KO-RS-06-021", "track": "F"}, {"skill_id": "KO-FC-04-024", "track": "C"}],
    "stage_hooks_ar": {"briefing": "مطرٌ لا غيمة فيه… فمن أين جاء الماء؟", "investigating": "كل جهاز يحمل ساعته الخاصة، فاقرأ الأرقام قبل أن تثق بها.", "review": "قبل أن تغلق الملف: ما الذي لا تستطيع الأدلة إثباته؟", "resolved": "أُغلق الملف. في الأرشيف ملف آخر لم يُفتح بعد."},
    "character_glyphs": {"lama": "ل", "majed": "م", "ziad": "ز", "wadad": "و", "noor": "ن", "yusuf": "ي"},
}
sc = {
    "case_id": CID,
    "accepted_conclusions": {
        "h_majed_hose": {"grade": 1, "note_ar": "استنتاج متسق مع الأدلة ويتطلب ذكر حدوده (النية لا تثبت)."},
        "h_ziad_sabotage": {"grade": 0, "note_ar": "قائم على قراءة ساعة المحطة دون تصحيح وعلى صفة السترة المشتركة."},
        "h_real_rain": {"grade": 0, "note_ar": "تنقضه نشرة المرصد والبلل المحصور بين الصنبور والمقياس."},
        "h_sensor_fault": {"grade": 0, "note_ar": "في القارورة ماء حقيقي، فالقراءة ليست عطلاً."}},
    "confidence_band": {"h_majed_hose": [65, 90], "h_ziad_sabotage": [0, 15], "h_real_rain": [0, 15], "h_sensor_fault": [0, 15]},
    "source_key": {"ev_station_log": "primary_record", "ev_lab_clock_offset": "primary_record", "ev_chat_alerts": "primary_record", "ev_city_bulletin": "public_document", "ev_collector_bottle": "primary_record",
                   "ev_roof_photo": "primary_record", "ev_gate_log": "primary_record", "ev_workshop_signout": "primary_record", "ev_roof_door_log": "primary_record", "ev_timer_device": "primary_record",
                   "ev_majed_notebook": "primary_record", "ev_wadad_testimony": "claim", "ev_ziad_recording": "primary_record"},
    "link_key": {
        "h_majed_hose": {"ev_roof_door_log": "supports", "ev_gate_log": "supports", "ev_timer_device": "supports", "ev_majed_notebook": "supports", "ev_roof_photo": "supports", "ev_chat_alerts": "supports",
                         "ev_lab_clock_offset": "supports", "ev_workshop_signout": "supports", "ev_ziad_recording": "neutral", "ev_ziad_demeanour": "neutral", "ev_city_bulletin": "neutral", "ev_collector_bottle": "neutral"},
        "h_ziad_sabotage": {"ev_gate_log": "weakens", "ev_workshop_signout": "weakens", "ev_chat_alerts": "weakens", "ev_lab_clock_offset": "weakens", "ev_wadad_testimony": "neutral", "ev_ziad_demeanour": "neutral"},
        "h_real_rain": {"ev_city_bulletin": "weakens", "ev_roof_photo": "weakens", "ev_collector_bottle": "neutral"},
        "h_sensor_fault": {"ev_collector_bottle": "weakens", "ev_roof_photo": "weakens"}},
    "required_limits": ["l_intent", "l_identity", "l_clock_now"],
    "valid_mind_changers": ["m_other_user", "m_clock_fixed", "m_timer_other_run", "m_other_water"],
    "invalid_limits": ["l_invalid_demeanor", "l_invalid_hoodie", "l_invalid_lie"],
    "decisive_evidence": ["ev_roof_door_log", "ev_gate_log", "ev_timer_device", "ev_chat_alerts", "ev_lab_clock_offset"],
    "lab_requirement": None,
    "timeline_requirement": [{"evidence_id": "ev_station_log", "utc_minute": 56, "tol": 3}, {"evidence_id": "ev_chat_alerts", "utc_minute": 56, "tol": 3}, {"evidence_id": "ev_roof_door_log", "utc_minute": 52, "tol": 3},
                             {"evidence_id": "ev_gate_log", "utc_minute": 48, "tol": 3}, {"evidence_id": "ev_workshop_signout", "utc_minute": 47, "tol": 3}],
    "refuted_hypotheses": ["h_ziad_sabotage", "h_real_rain", "h_sensor_fault"],
    "criteria_map": {"c_source": "source_typing", "c_conflict": "conflict_resolution", "c_links": "hypothesis_links", "c_uncertainty": "uncertainty", "c_revision": "revision", "c_elimination": "elimination", "c_justification": "justification_human"},
    "caps": {"no_citations_max": 45, "no_conflict_resolution_max": 70},
}
os.makedirs(OUT, exist_ok=True)
for suf, obj in [("", core), (".ui", ui), (".scoring", sc)]:
    with open(os.path.join(OUT, f"{CID}{suf}.json"), "w", encoding="utf8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
print("ok")
