# جرد الملفات — FILE_INVENTORY (المرحلة 0 · ATHAR | أَثَر)

**تاريخ الإعداد:** 2026-10-27 · **المصدر:** مجلد المستخدم «game learning» كما وصل إلى بيئة العمل، وسجلات الجرد التي أنتجها المحللون السابقون (`all_files.csv` و`inv_A…H.jsonl`) مع إعادة حساب الأعداد والأحجام وبصمات sha256 من `all_files.csv`.

> **قاعدة القراءة:** لا يُذكر هنا أن ملفاً «قُرئ» إلا إذا سجّل محلل سابق ذلك في حقل `read_status`. حالة `structure_only` تعني العناوين والحجم والبنية فقط، و`metadata_only` تعني المقارنة بالحجم أو sha256 دون قراءة المحتوى. لم يُنفَّذ أي سكربت أو ملف قابل للتنفيذ من الحزم (17 ملف `.py` و2 `.mjs` وُصفت قراءةً فقط).

---

## 0. تصحيحات وإفصاحات مهمة

| # | البند | الحقيقة المثبتة | الأثر |
|---|---|---|---|
| 1 | نسخ `LB_*` | يوجد **6 ملفات فقط** باسم `LB_*_METADATA` (3 كتب × نسختان): أحجامها 2,220 / 2,225 (كتاب 741)، 2,283 / 2,291 (كتاب 843)، 2,306 / 2,314 (كتاب 853) بايتاً. كل زوج يختلف في سطر العنوان فقط (فرق 5 أو 8 بايت). | هذه بطاقات وصفية آلية من أداة AIJUR وليست نصوص كتب. |
| 2 | نسخ `LB_` ذات النص الكامل (مثل 469,094 بايتاً) | أُبلغنا بوجود نسخ نصية كاملة بهذا الحجم (ويتسق فرق 8 بايت بين 469,094 و469,102 مع فرق نسختي بطاقة الكتاب 843)، لكن **المجلد المُجهَّز للتحليل لا يحتوي أي ملف بهذا الحجم**: فُحص بـ`ls` في 2026-10-27 فلم يظهر سوى النصوص الأربعة الكاملة (56,146 / 1,995,502 / 465,555 / 685,296 بايتاً) والبطاقات الست. ولا يظهر الحجمان في `all_files.csv`. | **غير مؤكد ومعلّق:** إن كانت النسخ موجودة على جهاز المستخدم فهي لم تُنقل ولم تُقرأ هنا، ولا يجوز بناء قرار على افتراض تطابقها مع النسخ الأخرى حتى تُجهَّز وتُقارن بالبصمة. |
| 3 | `ATHAR_ASSETS_v2_IMAGES.zip` (≈156 MB) | **لم يُنقل (not staged) ولم يُستخرج**، فالصور نفسها **لم تُرَ** ولم تُفحص بصماتها. المتاح فقط هو `IMAGE_ASSET_REGISTER.csv` (600 سجلاً) داخل مكتبة v2. | كل ما يخص الصور في هذه الوثائق مصدره السجل لا الملفات. |
| 4 | `ATHAR_ASSETS_v2_AUDIO_ICONS.zip` (78,594,947 بايتاً) | نُقل لكنه **غير مُدرج في `all_files.csv`**؛ قُرئت قائمته (451 مدخلاً) واستُخرجت ثلاثة ملفات فقط (سجلا الصوت والأيقونات ودليل الصوت). لم يُستمع إلى أي ملف صوتي. | انظر §7. |
| 5 | كتب الطب الشرعي | قُرئت جزئياً فقط (`read_partial` للكتب 741 و843 و853؛ `read_full` لـ04425 حسب سجل المحلل). | لا ملخص فصل بفصل ولا نقل نص (انظر GAP_AND_CONFLICT_REPORT). |

---

## 1. الأعداد الإجمالية

**ما يغطيه `all_files.csv`:** 894 ملفاً في 7 حزم مستخرجة، مجموعها 154,141,975 بايتاً (≈147.0 MiB). يُضاف إليها 22 ملفاً سائباً في المجلد الأعلى (§4) وحزمة الصوت والأيقونات (451 مدخلاً، §7). حزمة الصور غير موجودة (§0).

### حسب الحزمة

| الحزمة | الملفات | الحجم (MiB) | الوصف |
|---|---:|---:|---|
| `ATHAR_LIBRARY_v2_CORE` | 529 | 114.98 | المكتبة الأحدث والمرجع (تحوي أيضاً zip v1 المتداخل، 9,210,772 بايتاً) |
| `ATHAR_RESEARCH_LIBRARY_v1_2026-10-27` | 242 | 29.05 | المكتبة الأقدم (نسخة مستخرجة من الـzip المتداخل) |
| `ATHAR_CONTEXT_PACK_v2` | 31 | 1.66 | مجموعة فرعية من v2 للتسليم (31 من 31 مطابقة بايتياً لملفات v2) |
| `ATHAR_CONTEXT_PACK` | 21 | 0.80 | مجموعة فرعية قديمة (21 من 21 مطابقة لملفات v1؛ 3 منها مطابقة لـv2 أيضاً) |
| `ATHAR_Master_Knowledge_and_Content_2026-10-27` | 32 | 0.29 | حزمة المعرفة والمحتوى (Dossier وAddendum + نسخة من Content v02) |
| `ATHAR_Content_and_Case_Engine_v02` | 24 | 0.15 | حزمة المحتوى والقضايا التسع |
| `ATHAR_V1_Implementation_Kit` | 15 | 0.08 | حزمة التسليم الأولى (نموذج `index.html` وقضايا) |
| **المجموع** | **894** | **147.00** | |

### حسب النوع

| النوع | الملفات | الحجم (MiB) | ملاحظة |
|---|---:|---:|---|
| `.md` | 558 | 10.63 | وثائق وبطاقات مصادر (`cards/*.md`) |
| `.jsonl` | 103 | 19.76 | كائنات المعرفة وـRAG (`rag_chunks.jsonl` وحده 6.1 MB في v2) |
| `.txt` | 103 | 62.01 | نصوص ملك عام وOpenITI في `99_LEGAL_SOURCE_ASSETS` |
| `.csv` | 54 | 9.09 | سجلات الحقوق والمصادر والمنافسين |
| `.json` | 23 | 0.52 | السكيما والتقارير |
| `.py` | 17 | 0.17 | أدوات المكتبة (لم يُنفَّذ أيٌّ منها) |
| `.sqlite` | 2 | 35.95 | `athar_library.sqlite` (v2: 24,342,528 · v1: 13,357,056 بايتاً) |
| `.yarn` | 15 | ≈0 | تجهيزات اختبار RTL (ليست محتوى) |
| `.lp` | 12 | 0.01 | قواعد ASP لفاحص العدالة |
| `.png` | 2 | 0.07 | صورتان تابعتان لنص Ranpo الياباني |
| `.mjs` | 2 | ≈0 | تجهيزات اختبار ink (لم تُشغَّل) |
| `.zip` | 1 | 8.78 | نسخة v1 المتداخلة |
| `.ink` | 1 | ≈0 | تجهيز اختبار |
| `.html` | 1 | 0.02 | `prototype/index.html` في حزمة V1 |

### حالة القراءة (حسب سجلات المحللين: 600 سجلاً تغطي الـ894 ملفاً بعضها مجموعات)

| `read_status` | السجلات | المعنى العملي |
|---|---:|---|
| `read_full` | 204 | قرأه المحلل كاملاً |
| `read_partial` | 85 | قُرئت أجزاء منه (عناوين ومقاطع مستهدفة) |
| `structure_only` | 223 | بنية/أعمدة/إحصاء فقط (ينطبق على الفهارس الكبيرة وCSV/JSONL والنسخ المكررة) |
| `metadata_only` | 87 | حجم وبصمة دون قراءة (غالباً نسخ v1/CONTEXT_PACK المطابقة أو الأقدم) |
| `unreadable` | 1 | حزمة الصور (غير منقولة) |

القيمة `used_in_build` في السجلات: `reference_only` 214 · `seed_data` 136 · `spec` 121 · `discarded` 81 (نسخ أقدم) · `not_used` 46.
**تنبيه تسوية:** طابقتُ سجلات الجرد مع `all_files.csv` برمجياً؛ ثبت 846 ملفاً بسجل فردي أو مجموعة، والـ48 المتبقية: 22 ملفاً في `ATHAR_CONTEXT_PACK_v2` مطابقة بايتياً (sha256) لملفات v2 المسجَّلة، وzip v1 المتداخل في جذر v2 (1)، و25 ملفاً في v1 داخل المجلدات 07 و08 و11 (تغطيها مجموعات `cards/` و`_data/` وملفات v2 المناظرة). لم أعد فتح الملفات نفسها.

---

## 2. المجموعات العليا لمكتبة v2 مقابل v1

(عدد الملفات وحجمها بـMiB؛ v1 لا يحوي المجلد 15 إطلاقاً.)

| المجموعة | ملفات v2 | MiB v2 | ملفات v1 | MiB v1 |
|---|---:|---:|---:|---:|
| (جذر: README وsqlite…) | 3 | 32.01 | 2 | 12.74 |
| 00_PROJECT_CONTROL | 18 | 0.59 | 12 | 0.23 |
| 01_SOURCE_CATALOG | 11 | 6.26 | 8 | 3.17 |
| 02_DETECTIVE_LITERATURE | 36 | 0.97 | 17 | 0.45 |
| 03_NARRATIVE_AND_GAME_DESIGN | 24 | 0.44 | 21 | 0.40 |
| 04_FORENSIC_SCIENCE | 32 | 0.72 | 18 | 0.30 |
| 05_INVESTIGATIVE_REASONING | 17 | 0.31 | 14 | 0.28 |
| 06_COGNITIVE_SCIENCE | 15 | 0.35 | 15 | 0.35 |
| 07_LEARNING_SCIENCE | 42 | 0.85 | 16 | 0.32 |
| 08_ARAB_AUDIENCE_AND_CULTURE | 26 | 1.81 | 15 | 0.32 |
| 09_COMPETITIVE_INTELLIGENCE | 45 | 1.21 | 23 | 0.58 |
| 10_TECHNICAL_ARCHITECTURE | 64 | 0.68 | 24 | 0.34 |
| 11_RIGHTS_PRIVACY_AND_SAFETY | 37 | 1.65 | 15 | 0.79 |
| 12_KNOWLEDGE_OBJECTS | 9 | 6.37 | 9 | 3.45 |
| 13_CASE_DESIGN_REFERENCE | 14 | 0.72 | 13 | 0.48 |
| 14_PRODUCT_RESEARCH_SYNTHESIS | 10 | 0.83 | 10 | 0.42 |
| 15_STORY_MEDIA_AND_ASSETS | 28 | 1.48 | 0 | 0.00 |
| 99_LEGAL_SOURCE_ASSETS | 98 | 57.74 | 10 | 4.41 |
| **المجموع** | **529** | | **242** | |

## 3. الملفات البارزة لكل مجموعة (مكتبة v2؛ الأحجام بالبايت من `all_files.csv`)

| المجموعة | ملفات بارزة | ملاحظة |
|---|---|---|
| 00_PROJECT_CONTROL | `FINAL_HANDOFF_MANIFEST.md`، `W2_CORRECTIONS_APPLIED.md`، `WAVE2_CORRECTIONS_TO_PROPAGATE.md`، `RESEARCH_GAPS.md` (123,627)، `CROSS_LIBRARY_RECONCILIATION.md` (5,245)، `MASTER_PROMPT_ORIGINAL.md` (55,724)، `FILE_INVENTORY.csv` (198,638) | خرائط التسليم والتصحيحات؛ `FINAL_HANDOFF_MANIFEST_v1_archive.md` أرشيف |
| 01_SOURCE_CATALOG | `sources_master.csv/.jsonl` (≈2.0 / 3.0 MB)، `rights_register.csv` (962,304)، `bibliography.md` (428,132)، سجلات التحقق | 1,550 مصدراً؛ حللتها الأدوات إحصائياً فقط |
| 02_DETECTIVE_LITERATURE | `FAIR_PLAY_MYSTERY_RULEBOOK.md`، `MYSTERY_PLOT_PATTERNS.md`، `ARABIC_CLASSICAL_INFERENCE_HERITAGE.md`، `DETECTIVE_LITERATURE_ATLAS.md` (67,424)، `LITERARY_RIGHTS_REGISTER.csv` | الأطلس: عناوينه فقط قُرئت |
| 03_NARRATIVE_AND_GAME_DESIGN | `HINT_AND_DIFFICULTY_SYSTEM.md`، `INTERACTIVE_MYSTERY_DESIGN_BIBLE.md`، `GAME_MECHANICS_PATTERN_LIBRARY.md`، `EVIDENCE_BOARD_UX_RESEARCH.md`، `DESIGN_EVIDENCE_UPDATE_W2.md` | سلّم التلميح 5 مستويات + L0 |
| 04_FORENSIC_SCIENCE | `ARABIC_FORENSIC_GLOSSARY.md` + `.csv` (248 مصطلحاً)، `FORENSIC_METHOD_VALIDITY_MATRIX.csv` (24 طريقة)، `SAFE_VIRTUAL_LABS_CATALOG.md` (30 مختبراً)، `BIAS_LAB_ETHICS_FOR_MINORS.md`، `CSI_MYTHS_AND_SCIENTIFIC_CORRECTIONS.md` | v2 يصحح مصطلحاً (LR) |
| 05_INVESTIGATIVE_REASONING | `INVESTIGATIVE_REASONING_FRAMEWORK.md`، `COMMON_REASONING_ERRORS.md`، `EVIDENCE_EVALUATION_GUIDE.md`، `ETHICAL_INVESTIGATION_PRINCIPLES.md`، `ARAB_CRIMINAL_PROCEDURE_CONTEXT.md` | الأخير موجود في v2 فقط |
| 06_COGNITIVE_SCIENCE | `REASONING_SKILLS_TAXONOMY.md`، `CRITICAL_THINKING_ASSESSMENT_FRAMEWORK.md` (v1: 21,899 ← v2: 27,170)، `LEARNING_TRANSFER_RESEARCH.md`، `COGNITIVE_BIAS_CASE_LIBRARY.md` | |
| 07_LEARNING_SCIENCE | `EVIDENCE_CENTERED_ASSESSMENT_MODEL.md`، `LEARNER_MASTERY_MODEL.md`، `EDUCATIONAL_VALIDATION_PLAN.md`، `PILOT_STUDY_ETHICS_AND_PERMISSIONS.md`، `TEEN_USER_RESEARCH_PLAYBOOK.md`، `LEARNING_OUTCOMES_TO_GAMEPLAY_MAP.csv`، `templates/` (5 قوالب موافقة AR/EN) | 26 ملفاً في v2 فقط |
| 08_ARAB_AUDIENCE_AND_CULTURE | `AGE_APPROPRIATE_CONTENT_POLICY.md`، `ARABIC_LANGUAGE_AND_DIALECT_STRATEGY.md`، `DEMAND_AND_MARKET_EVIDENCE.md`، `ARAB_AUDIENCE_RESEARCH.md`، `LOCAL_STORY_OPPORTUNITIES.md`، `ARABIC_MYSTERY_WORLD_BUILDING.md` | |
| 09_COMPETITIVE_INTELLIGENCE | `GLOBAL_COMPETITOR_INTELLIGENCE.md` (GC-001…072)، `ARAB_COMPETITOR_INTELLIGENCE.md` (COMP-A-001…051)، `FEATURE_GAP_MATRIX.csv`، `ATHAR_DEFENSIBILITY_ANALYSIS.md`، `WHITE_SPACE_OPPORTUNITIES.md`، `UNIT_ECONOMICS_SCENARIOS.md`، `_data/pricing_benchmarks.csv` | أرقام تقييمات وأسعار «لقطة» |
| 10_TECHNICAL_ARCHITECTURE | `case_schema.json` (29,770)، `CASE_SCHEMA_PROPOSAL.md`، `AI_CHARACTER_GUARDRAILS.md`، `CASE_ENGINE_TECHNICAL_RESEARCH.md`، `ARABIC_TOKEN_COST_MEASUREMENT.md`، `RTL_AUTHORING_TOOL_TESTS.md`، `prototypes/asp/*.lp` (12)، `_data/rtl_test_fixtures/` | 40 ملفاً جديداً في v2 |
| 11_RIGHTS_PRIVACY_AND_SAFETY | `NAME_CLEARANCE_ATHAR.md`، `CHILD_AND_TEEN_PRIVACY_REQUIREMENTS.md`، `ARAB_MARKET_LAUNCH_COMPLIANCE_MATRIX.md`، `INTELLECTUAL_PROPERTY_RESEARCH.md`، `CONTENT_AND_SAFETY_GOVERNANCE.md`، `COMMERCIAL_USE_DECISION_MATRIX.md`، `YOUTH_HELPLINE_REGISTER.csv`، `TRADEMARK_AND_LICENSE_REGISTER.csv`، `SOURCE_RIGHTS_REGISTER.csv` | كلها «بحث أولي» لا رأي محامٍ |
| 12_KNOWLEDGE_OBJECTS | `reasoning_skills.jsonl` (39)، `forensic_concepts.jsonl` (40)، `case_mechanics.jsonl` (58)، `learning_assessments.jsonl` (56)، `character_design_patterns.jsonl` (44)، `narrative_patterns.jsonl` (83)، `product_opportunities.jsonl` (57)، `rag_chunks.jsonl` (2,978)، `orphan_references.json` (`[]`) | v1: 38/32/46/35/29/46/28 و1,735 قطعة |
| 13_CASE_DESIGN_REFERENCE | `CASE_DESIGN_BIBLE.md` (115,268)، `CASE_ARCHETYPES.md` (161,771) + `case_archetypes.jsonl` (40 نمطاً)، `CASE_TEMPLATE.md`، `SAMPLE_CASE_001.md` + `sample_case_001.json` (87,874)، `HERITAGE_CASE_SEEDS.md`، `tools/check_case.py` (38,253) | القضية النموذجية بلا مراجعة بشرية |
| 14_PRODUCT_RESEARCH_SYNTHESIS | `FINAL_STRATEGIC_REPORT.md` (146,308)، `MVP_SCOPE.md` (89,164)، `FIRST_SEASON_RECOMMENDATIONS.md` (90,989)، `EDUCATIONAL_FRAMEWORK.md` (68,917)، `PRODUCT_DIFFERENTIATION.md`، `INNOVATION_DIRECTIONS.md`، `ATHAR_VISION_RECOMMENDATIONS.md`، `OPEN_QUESTIONS_FOR_NEXT_PHASE.md`، `CORE_REFERENCES_V1.md` | وثائق القرار الرئيسة |
| 15_STORY_MEDIA_AND_ASSETS | `IMAGE_ASSET_REGISTER.csv` (767,182؛ 600 صورة)، `AUDIO_ASSET_REGISTER.csv` (165)، `ICON_AND_UI_ASSET_REGISTER.csv` (6 مجموعات)، `SOUND_DESIGN_GUIDE.md`، `VISUAL_REFERENCE_GUIDE.md`، `STORY_CORPUS_INDEX.csv`، `HERITAGE_STORY_INDEX.csv` | سجلات فقط، بلا ملفات الصور |
| 99_LEGAL_SOURCE_ASSETS | `PUBLIC_DOMAIN_VERIFIED/` (57 مجلداً، 94 ملف `.txt` حسب محلل المجموعة E)، `OPEN_LICENSE/arabic_heritage*` (OpenITI: 11 نصاً، 22 ملفاً، ≈28.9 MB، CC BY-NC-SA 4.0)، `ASSET_MANIFEST_W2_TEXTS.csv` (84 صفاً)، `README.md` | OpenITI للبحث الداخلي فقط |

---

## 4. الملفات السائبة في المجلد الأعلى «game learning» (22 ملفاً مُجهَّزاً + حزمة غير مُجهَّزة)

| الملف | الحجم (بايت) | ما هو | الحالة |
|---|---:|---|---|
| `04425_طرق الإنجاب في الطب الحديث وحكمها الشرعي.txt` | 56,146 | كتاب فقه إنجاب (غير ذي صلة بالمنتج) | قُرئ (حسب المحلل H) |
| `741 الطب الشرعي ومسرح الجريمة والبحث الجنائي (أحمد بسيوني أبو الروس، مديحة الخضري).txt` | 1,995,502 | كتاب ط2 2008، 7,789 سطراً، مصري المحتوى | قراءة جزئية (F) |
| `843 الأسلحة النارية في الطب الشرعي - حسين شحرور.txt` | 465,555 | كتاب 2004، 2,218 سطراً | قراءة جزئية (G) |
| `853 الطب الشرعي العملي (الياس الصائغ).txt` | 685,296 | كتاب ج1 1997، 2,776 سطراً | قراءة جزئية (G) |
| 6 بطاقات `LB_*_METADATA` | 2,220–2,314 | بطاقات AIJUR وصفية خاطئة التصنيف | قُرئت كاملة |
| `ATHAR_LIBRARY_v2_CORE.zip` | 43,334,957 | المكتبة الأحدث | مستخرجة |
| `ATHAR_RESEARCH_LIBRARY_v1_2026-10-27.zip` | 9,210,772 | المكتبة الأقدم | مستخرجة |
| `ATHAR_CONTEXT_PACK_v2.zip` / `ATHAR_CONTEXT_PACK.zip` | 529,979 / 255,230 | مجموعات فرعية | مستخرجة |
| `ATHAR_Master_Knowledge_and_Content_2026-10-27.zip` | 86,126 | Dossier + Addendum + Content v02 | مستخرجة |
| `ATHAR_Content_and_Case_Engine_v02.zip` | 52,692 | القضايا التسع | مستخرجة |
| `ATHAR_V1_Implementation_Kit.zip` | 35,284 | النموذج الأولي | مستخرجة |
| `ATHAR_ASSETS_v2_AUDIO_ICONS.zip` | 78,594,947 | صوت وأيقونات | قائمة + 3 ملفات (§7) |
| `ATHAR_Research_Dossier.md` | 43,419 | مطابق لنسخة حزمة Master (حسب المحلل E) | قراءة جزئية |
| `ATHAR_Research_Starter_2026-10-27.md` | 14,044 | مطابق لنسخة Content v02 | قُرئ |
| `index.html` | 18,429 | نموذج قضية «الرصد الأخير» (مطابق لنموذج حزمة V1) | قُرئ؛ نظيف من الحقن حسب H |
| `aijur-skills-platform-tools.md` | 13,200 | وصف مكدّس منصة AIJUR Skills (الملف الفريد بين المرفوعات) | قُرئ؛ نظيف حسب H |
| `ATHAR_ASSETS_v2_IMAGES.zip` | ≈156 MB (تقريبي، من الموجز) | حزمة صور | **غير منقولة** (§0) |

---

## 5. الملفات غير المقروءة أو المتخطاة وأسبابها

| الملف/المجموعة | السبب | الأثر |
|---|---|---|
| `ATHAR_ASSETS_v2_IMAGES.zip` | انتهت مهلة النقل؛ لم يُجهَّز | الصور (600 في السجل) غير مرئية، لا تحقق من بصمات ولا جودة ولا أمان |
| نسخ `LB_` الكاملة بحجم ≈469 KB | غير موجودة في المجلد المُجهَّز | معلّقة (§0-2) |
| ملفات الصوت (165 `.ogg`) | لم يُستخرج منها شيء ولم يُستمع إليها؛ السجل يقول إن 45 مقطعاً «not auditioned by ear» | فحص سمعي بشري إلزامي قبل الشحن |
| 232 ملف `.svg` (أيقونات) | قائمة فقط | سجل المجموعات (6 صفوف) لا الملفات |
| `bibliography.md` (428,132) و`sources_master.csv/jsonl` و`rights_register.csv` و`IMAGE_ASSET_REGISTER.csv` و`rag_chunks.jsonl` | `structure_only`: أعمدة وإحصاء وعينات | لا يُدّعى مراجعة سجل سجل |
| `athar_library.sqlite` (24.3 MB) و`FILE_INVENTORY.csv` | بنية وجداول واستعلامات للقراءة فقط | |
| `cards/*.md` في 07 و08 و11 (22 و12 و18 بطاقة) و`_data/` | لم تُقرأ فرادى (المحلل D) | قد تحوي قرارات غير ملتقطة |
| `02_DETECTIVE_LITERATURE/DETECTIVE_LITERATURE_ATLAS.md` ومتن `CASE_ARCHETYPES.md` بعد السطر 90 و`SAMPLE_CASE_001.md` | عناوين فقط (المحلل B) | |
| ملفات Content v02: `02_SKILLS.md` و`03_STORY_PATTERNS.md` و`04_SAFE_LABS.md` | بنية فقط (نسخ نثرية محتملة من `data/*.jsonl`) | |
| `.py` (17) و`.mjs` (2) و`.yarn`/`.ink`/`.lp` | قراءة نص فقط، لا تنفيذ (سياسة السلامة) | `check_case.py` لم يُشغَّل |
| نصوص `PUBLIC_DOMAIN_VERIFIED` وOpenITI (≈62 MB `.txt`) | بنية/أسماء/أحجام فقط | لا قراءة نصية |

---

## 6. التكرارات والتعارضات بين الإصدارات

### التكرارات (حسب sha256 في `all_files.csv`)
- **223 مجموعة بصمة مكررة تضم 462 ملفاً (239 نسخة زائدة).**

| أطراف التكرار | المجموعات |
|---|---:|
| v2_CORE ↔ v1 | 146 |
| CONTEXT_PACK_v2 ↔ v2_CORE | 29 |
| CONTEXT_PACK ↔ v1 | 18 |
| Content_and_Case_Engine ↔ Master/CONTENT_v02 | 15 |
| Content_and_Case_Engine ↔ Master ↔ V1_Kit | 9 |
| CONTEXT_PACK ↔ CONTEXT_PACK_v2 ↔ v2 ↔ v1 | 2 |
| CONTEXT_PACK ↔ v2 ↔ v1 | 1 |
| مكررة داخل v2 نفسها | 2 |
| مكررة داخل v1 نفسها | 1 |

- الحزمة `ATHAR_Master_Knowledge…/CONTENT_v02` (24 ملفاً) مطابقة بايتياً لـ`ATHAR_Content_and_Case_Engine_v02` (24 من 24)؛ و9 من 15 ملفاً في V1_Kit مطابقة لهما.
- `sample_case_001.json` (87,874 بايتاً) **بصمة واحدة** في v1 وv2 وCONTEXT_PACK، بينما تغيّر تقرير الفحص والمدقق (انظر الأسفل).

### تعارضات الإصدار: v1 مقابل v2
- مسارات مشتركة: 242 (كل مسارات v1 موجودة في v2؛ **لا ملف حصري لـv1 على مستوى المسار**). منها **149 مطابقة بايتياً** و**93 مختلفة**: 92 منها أكبر في v2، وواحد أصغر (`00_PROJECT_CONTROL/FINAL_HANDOFF_MANIFEST.md`: 23,809 ← 22,265 بايتاً).
- v2 يضيف **287 مساراً** غير موجود في v1: 99_LEGAL (88)، 10_TECHNICAL (40)، 15_STORY_MEDIA (28)، 07 (26)، 09 (22)، 11 (22)، 02 (19)، 04 (14)، 08 (11)، 00 (6)، وغيرها.

أكبر تغييرات الحجم (v1 ← v2، بايت):

| الملف | v1 | v2 |
|---|---:|---:|
| `athar_library.sqlite` | 13,357,056 | 24,342,528 |
| `12_KNOWLEDGE_OBJECTS/rag_chunks.jsonl` | 3,264,585 | 6,104,855 |
| `01_SOURCE_CATALOG/sources_master.jsonl` | 1,559,397 | 3,036,744 |
| `01_SOURCE_CATALOG/rights_register.csv` | 490,004 | 962,304 |
| `14_PRODUCT_RESEARCH_SYNTHESIS/FINAL_STRATEGIC_REPORT.md` | 65,078 | 146,308 |
| `13_CASE_DESIGN_REFERENCE/CASE_ARCHETYPES.md` | 87,608 | 161,771 |
| `14_PRODUCT_RESEARCH_SYNTHESIS/MVP_SCOPE.md` | 36,594 | 89,164 |
| `14_PRODUCT_RESEARCH_SYNTHESIS/FIRST_SEASON_RECOMMENDATIONS.md` | 32,144 | 90,989 |
| `13_CASE_DESIGN_REFERENCE/CASE_DESIGN_BIBLE.md` | 69,295 | 115,268 |
| `06_COGNITIVE_SCIENCE/CRITICAL_THINKING_ASSESSMENT_FRAMEWORK.md` | 21,899 | 27,170 |

الفروق ذات الأثر على البناء (حسب المحللين C وB وD):
1. **المصطلح:** v1 يكتب likelihood ratio «نسبة الأرجحية» و chain of custody «سلسلة الحيازة»؛ v2 يصحح إلى «نسبة الترجيح» و«سلسلة العهدة» (لكن `rag_chunks.jsonl` في v2 ما زال يحمل 39 قطعة بـ«الأرجحية» و17 بـ«الحيازة»).
2. **Bad News:** `KO-PO-09A-005` في v1 يقول بلا نسخة عربية؛ v2 يصحح (نسخة عربية رسمية، `ATH-SRC-2074`).
3. **طول الجملة:** v1 «نحو 20 كلمة»؛ v2 يعتمد معايرة BAREC (19 مستوى). ثلاثة ملفات في `ATHAR_CONTEXT_PACK` مطابقة لـv1 فتفتقر لإضافات v2.
4. **المدقق:** `sample_case_001.json` ثابت لكن تقرير الفحص وSAMPLE_CASE_001.md وcheck_case.py تغيّرت؛ لم يؤكد المحلل B أن تقرير v2 بُني على المحتوى نفسه (غير مؤكد).
5. **قرار:** v2 هو المعتمد في كل الحالات؛ v1 لا يحمل معرّف KO غير موجود في v2 (`orphan_references=[]`).

### أرقام داخل مكتبة v2 نفسها (غير متسقة)
README يقول 154 بطاقة ملف و179 سجلاً في CSV؛ 1,475 مصدراً verified و75 needs_expert_review مقابل «1,476/74» في RESEARCH_GAPS؛ ترويسة GLOBAL_COMPETITOR_INTELLIGENCE «65» بينما الجدول 72 صفاً. تفاصيلها في GAP_AND_CONFLICT_REPORT.

---

## 7. حزمة `ATHAR_ASSETS_v2_AUDIO_ICONS.zip` — القائمة (451 مدخلاً، 425 ملفاً)

| المسار داخل الحزمة | الملفات | المحتوى |
|---|---:|---|
| `15_STORY_MEDIA_AND_ASSETS/` | 3 | `AUDIO_ASSET_REGISTER.csv` (165 صفاً، 195,948 بايتاً)، `ICON_AND_UI_ASSET_REGISTER.csv` (6 صفوف، 6,555)، `SOUND_DESIGN_GUIDE.md` (30,111) |
| `99_LEGAL_SOURCE_ASSETS/OPEN_LICENSE/` | 302 | 232 `.svg` أيقونات (6 مكتبات) + 57 `.ogg` + 13 `.txt` رخص |
| `99_LEGAL_SOURCE_ASSETS/PUBLIC_DOMAIN_VERIFIED/` | 120 | 108 `.ogg` (CC0) + 12 `.txt` |

سجل الصوت (165): CC0 = 108 (Kenney 67، Musopen/شوبان 11، OpenGameArt 30)، PDM = 52 (radio aporee)، CC BY 3.0 = 4 (`AUD-0075` و`0109` و`0111` و`0116`)، PD قديم = 1 (`AUD-0163`، داخلي فقط). أيقونات: Material (Apache-2.0)، Lucide (ISC)، Phosphor/Tabler/Heroicons/Fluent (MIT).
**لم يُستمع إلى أي ملف؛ 45 مقطعاً موسوم «not auditioned by ear»؛ 11 مقطعاً بقفزات جهارة 12–28 LU.**

## 8. حالة الشفرة المبنية (للتمييز عن الجرد)
مستودع `/home/claude/athar` ليس جزءاً من الجرد؛ يُشار إليه في RESEARCH_TO_PRODUCT_MAP فقط.
