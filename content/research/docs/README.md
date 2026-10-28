# مكتبة أَثَر المعرفية — ATHAR Research & Knowledge Library (v2)

مستودع بحثي موثّق لتصميم **أَثَر (ATHAR)**، وهو **اسم عمل** (انظر قرار الاسم أدناه): منصة عربية للتعلم عبر الغموض والتحقيق والاستدلال للمراهقين والشباب. المرحلة **بحثية**؛ لا تتضمن بناء التطبيق.

**الإصدار:** v2 — 2026-10-27 (الدفعة الأولى + دفعة التوسع الثانية)
**الأرقام:** 1,550 مصدراً فريداً موثقاً (1,475 مؤكد + 75 بحاجة لمراجعة خبير) · 154 بطاقة تحليل معمق · 377 وحدة معرفة · 40 نمط قضية + 12 بذرة تراثية · 123 منافساً · 67 حكاية تراثية و102 عمل في فهرس القصص · مسرد جنائي عربي من 248 مصطلحاً · **أصول محفوظة قانونياً:** 84 نصاً، 600 صورة، 165 ملفاً صوتياً، 232 أيقونة · تدقيقان مستقلان: 0 مصادر مختلقة.

> **تنبيه الاسم:** لا يُنصح باعتماد «أثر/ATHAR» المجرد علامةً تجارية قبل بحث سابقية رسمي (منصة أدلة لشرطة دبي، لعبة بالاسم نفسه في المتاجر العربية، 36+ تطبيقاً). انظر `11_RIGHTS_PRIVACY_AND_SAFETY/NAME_CLEARANCE_ATHAR.md` والقرار D13.

---

## ابدأ من هنا
| إن كنت… | اقرأ أولاً |
|---|---|
| **صاحب القرار** | `14_PRODUCT_RESEARCH_SYNTHESIS/FINAL_STRATEGIC_REPORT.md` (الملخص التنفيذي + «ما الذي غيّرته الدفعة الثانية» + القرارات) ثم `MVP_SCOPE.md` و`00_PROJECT_CONTROL/FINAL_HANDOFF_MANIFEST.md` |
| **كاتب قضايا** | `13_CASE_DESIGN_REFERENCE/CASE_DESIGN_BIBLE.md` (§18 الجديد) ← `CASE_TEMPLATE.md` ← `SAMPLE_CASE_001.md` ← `CASE_ARCHETYPES.md` (40) ← `HERITAGE_CASE_SEEDS.md` ← قوائم الفحص؛ ومصادر الإلهام: `15_STORY_MEDIA_AND_ASSETS/HERITAGE_STORY_INDEX.csv` و`STORY_CORPUS_INDEX.csv` |
| **مستشاراً علمياً** | `04_FORENSIC_SCIENCE/FORENSIC_EXPERT_REVIEW_CHECKLIST.md`، `ARABIC_FORENSIC_GLOSSARY.md`، `BIAS_LAB_ETHICS_FOR_MINORS.md`، `FORENSIC_METHOD_VALIDITY_MATRIX.csv` |
| **مصمم تعلم / خبير قياس** | `14_PRODUCT_RESEARCH_SYNTHESIS/EDUCATIONAL_FRAMEWORK.md` ← `07_LEARNING_SCIENCE/` (ومنها `ARABIC_ASSESSMENT_AND_AI_EVIDENCE.md` و`PILOT_STUDY_ETHICS_AND_PERMISSIONS.md`) ← `06_COGNITIVE_SCIENCE/REASONING_SKILLS_TAXONOMY.md` |
| **مهندساً** | `10_TECHNICAL_ARCHITECTURE/CASE_ENGINE_TECHNICAL_RESEARCH.md`، `case_schema.json`، `AI_CHARACTER_GUARDRAILS.md`، `ARABIC_TOKEN_COST_MEASUREMENT.md`، `RTL_AUTHORING_TOOL_TESTS.md`، و`13_CASE_DESIGN_REFERENCE/tools/check_case.py` |
| **مستشاراً قانونياً** | `11_RIGHTS_PRIVACY_AND_SAFETY/ARAB_MARKET_LAUNCH_COMPLIANCE_MATRIX.md`، `NAME_CLEARANCE_ATHAR.md`، `TRADEMARK_AND_LICENSE_REGISTER.csv`، `INTELLECTUAL_PROPERTY_RESEARCH.md`، و`99_LEGAL_SOURCE_ASSETS/README.md` |
| **مسؤول الأعمال** | `08_ARAB_AUDIENCE_AND_CULTURE/DEMAND_AND_MARKET_EVIDENCE.md`، `09_COMPETITIVE_INTELLIGENCE/UNIT_ECONOMICS_SCENARIOS.md`، `BUSINESS_MODEL_AND_PRICING_EVIDENCE.md`، `FUNDING_AND_PARTNERSHIP_LANDSCAPE.md`، `ATHAR_DEFENSIBILITY_ANALYSIS.md` |
| **مصمماً بصرياً/صوتياً** | `15_STORY_MEDIA_AND_ASSETS/VISUAL_REFERENCE_GUIDE.md`، `SOUND_DESIGN_GUIDE.md`، والسجلات `IMAGE_ASSET_REGISTER.csv` و`AUDIO_ASSET_REGISTER.csv` و`ICON_AND_UI_ASSET_REGISTER.csv` |
| **مستأنفاً للبحث** | `00_PROJECT_CONTROL/PROGRESS_LOG.md` ← `RESEARCH_GAPS.md` (§د أهم عشر الآن) ← `RESEARCH_PROTOCOL.md` + `WAVE2_PROTOCOL_ADDENDUM.md` |

## خريطة المستودع
```
00_PROJECT_CONTROL/        الخطة، البروتوكول وملحقه، سجل التقدم، الفجوات، التصحيحات C1–C20، المصالحة، بيان التسليم، الأدوات
01_SOURCE_CATALOG/         الفهرس الموحد (1,550)، الببليوغرافيا، سجل الحقوق، سجلّا التدقيق المستقل
02_DETECTIVE_LITERATURE/   الأطلس (50 مبدأ + ATLAS-51…74 + HER-01…20)، أنماط الحبكة، كتاب قواعد العدالة، التراث العربي في الاستدلال، الأدب العالمي واليافعين، سجل حقوق الأعمال
03_NARRATIVE_AND_GAME_DESIGN/  دليل التصميم التفاعلي، 39 آلية، لوحة الأدلة، التلميحات والصعوبة، تحديث الأدلة
04_FORENSIC_SCIENCE/       أطلس 16 تخصصاً، مصفوفة الصلاحية، 30 مختبراً آمناً، المسرد العربي، المؤسسات العربية، أخلاقيات مختبرات التحيز
05_INVESTIGATIVE_REASONING/  إطار الاستدلال التحقيقي، تقييم الأدلة، الأخطاء، الأخلاقيات، السياق الإجرائي العربي
06_COGNITIVE_SCIENCE/      24 مهارة، مكتبة التحيزات، أدوات قياس التفكير النقدي، انتقال التعلم
07_LEARNING_SCIENCE/       الأساس العلمي، التقييم المرتكز على الأدلة، نموذج الإتقان، خطة التحقق، الأدلة العربية، أخلاقيات التجارب وقوالبها
08_ARAB_AUDIENCE_AND_CULTURE/  الجمهور، الطلب والسوق، بناء العالم، سياسة الفئات العمرية، اللغة واللهجات، الأدلة البحثية العربية
09_COMPETITIVE_INTELLIGENCE/  المنافسون، مصفوفة الفجوات، المساحات البيضاء، القدرة الدفاعية، قائمة المراقبة، الأعمال والتسعير والتمويل
10_TECHNICAL_ARCHITECTURE/   محرك القضايا، مخطط JSON، حدود الشخصيات، أدوات التأليف واختبارات RTL، قياس كلفة الرموز، المخاطر
11_RIGHTS_PRIVACY_AND_SAFETY/  الملكية الفكرية، الاستخدام التجاري، خصوصية القاصرين، مصفوفة الإطلاق العربية، فحص الاسم، العلامات والتراخيص، خطوط المساعدة
12_KNOWLEDGE_OBJECTS/      377 وحدة معرفة في 7 أنواع + 2,978 مقطع RAG
13_CASE_DESIGN_REFERENCE/  دستور القضايا، القالب، قضية نموذجية، 40 نمطاً، 12 بذرة تراثية، قوائم الفحص، خط الإنتاج، أداة الفحص الآلي
14_PRODUCT_RESEARCH_SYNTHESIS/  الرؤية، التمايز، الإطار التعليمي، 15 اتجاه ابتكار، التقرير الاستراتيجي، الموسم الأول، MVP، الأسئلة المفتوحة، المراجع الأساسية (70)
15_STORY_MEDIA_AND_ASSETS/ فهارس القصص والتراث والمراجع الإعلامية، سجلات الصور والصوت والأيقونات، أدلة المرجع البصري والصوتي
99_LEGAL_SOURCE_ASSETS/    نصوص وصور وأصوات وأيقونات بالملك العام أو تراخيص مفتوحة فقط، مع أساسها القانوني
athar_library.sqlite       قاعدة بحث جاهزة (مصادر، وحدات، مقاطع، بحث نصي كامل)
```

## قواعد قراءة المحتوى
- كل ادعاء مسنود بمعرّف `[ATH-SRC-####]` أو `KO-…` أو معرّف فهرس (ARC، HS، SC، MR، IMG، AUD…)، أو موسوم: `[حقيقة موثقة]` · `[تفسير بحثي]` · `[افتراض تصميمي]` · `[استنتاج استثماري]`.
- علامات التحديث: «تحديث الدفعة الثانية»، «…في الدفعة الثانية»، «(صُحح: C19)»، «(AUDIT-W2)» — تُبيّن ما تغيّر ولماذا.
- درجات الأدلة: A معايير ومصادر أولية ومراجعات منهجية · B بحث محكّم · C وثائق رسمية لمنتجات · D آراء وصحافة · E ضعيف (للمراجعة فقط).
- «متاح للقراءة» لا يعني «مسموح بالاستخدام التجاري» — راجع سجلات الحقوق والأصول.
- لا شيء هنا رأي قانوني أو علمي نهائي.

## البحث في المكتبة
```
python3 -c "import sqlite3; db=sqlite3.connect('athar_library.sqlite'); print(db.execute(\"SELECT kind, ref_id, title FROM search WHERE search MATCH 'confirmation' LIMIT 10\").fetchall())"
```
تفاصيل الاستيراد إلى PostgreSQL/Supabase أو نظام RAG: `00_PROJECT_CONTROL/FINAL_HANDOFF_MANIFEST.md` §13.
