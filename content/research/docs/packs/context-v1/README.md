# مكتبة أَثَر المعرفية — ATHAR Research & Knowledge Library

مستودع بحثي موثّق لتصميم **أَثَر (ATHAR)**: منصة عربية للتعلم عبر الغموض والتحقيق والاستدلال، موجهة للمراهقين والشباب. هذه المرحلة **بحثية**؛ لا تتضمن بناء التطبيق.

**الإصدار:** الدفعة الأولى — 2026-10-27
**الأرقام:** 816 مصدراً فريداً متحققاً منه (786 مؤكد + 30 بحاجة لمراجعة خبير) · 83 بطاقة تحليل معمق · 254 وحدة معرفة · 25 نمط قضية · 111 منتجاً منافساً · 9 نصوص في الملك العام محفوظة قانونياً · تدقيق مستقل: 0 أخطاء جوهرية في عينة 76.

---

## ابدأ من هنا
| إن كنت… | اقرأ أولاً |
|---|---|
| **صاحب القرار** | `14_PRODUCT_RESEARCH_SYNTHESIS/FINAL_STRATEGIC_REPORT.md` (الملخص التنفيذي في الصفحة الأولى) ثم `MVP_SCOPE.md` |
| **كاتب قضايا** | `13_CASE_DESIGN_REFERENCE/CASE_DESIGN_BIBLE.md` ← `CASE_TEMPLATE.md` ← `SAMPLE_CASE_001.md` ← `CASE_ARCHETYPES.md` ← قوائم الفحص الثلاث |
| **مستشاراً علمياً** | `04_FORENSIC_SCIENCE/FORENSIC_EXPERT_REVIEW_CHECKLIST.md` و`FORENSIC_METHOD_VALIDITY_MATRIX.csv` و`13_CASE_DESIGN_REFERENCE/SCIENTIFIC_REVIEW_CHECKLIST.md` |
| **مصمم تعلم أو خبير قياس** | `14_PRODUCT_RESEARCH_SYNTHESIS/EDUCATIONAL_FRAMEWORK.md` ← `07_LEARNING_SCIENCE/` ← `06_COGNITIVE_SCIENCE/REASONING_SKILLS_TAXONOMY.md` |
| **مهندساً** | `10_TECHNICAL_ARCHITECTURE/CASE_ENGINE_TECHNICAL_RESEARCH.md` و`case_schema.json` و`AI_CHARACTER_GUARDRAILS.md` و`13_CASE_DESIGN_REFERENCE/tools/check_case.py` |
| **مستشاراً قانونياً** | `11_RIGHTS_PRIVACY_AND_SAFETY/` و`02_DETECTIVE_LITERATURE/LITERARY_RIGHTS_REGISTER.csv` و`00_PROJECT_CONTROL/RESEARCH_GAPS.md` (G01، G02، G11–G15) |
| **مستأنفاً للبحث** | `00_PROJECT_CONTROL/PROGRESS_LOG.md` ← `RESEARCH_GAPS.md` ← `RESEARCH_PROTOCOL.md` |

## خريطة المستودع
```
00_PROJECT_CONTROL/        الخطة، البروتوكول، سجل التقدم، الفجوات، المصالحة، بيان التسليم، الأدوات
01_SOURCE_CATALOG/         الفهرس الموحد (CSV/JSONL)، الببليوغرافيا، سجل الحقوق، سجل التحقق والتدقيق
02_DETECTIVE_LITERATURE/   أطلس مبادئ أدب التحقيق، أنماط الحبكة، كتاب قواعد العدالة، سجل حقوق الأعمال
03_NARRATIVE_AND_GAME_DESIGN/  دليل التصميم التفاعلي، 39 آلية، لوحة الأدلة، التلميحات والصعوبة
04_FORENSIC_SCIENCE/       أطلس 16 تخصصاً، مصفوفة الصلاحية، 30 مختبراً افتراضياً آمناً، أساطير CSI
05_INVESTIGATIVE_REASONING/  إطار الاستدلال التحقيقي، تقييم الأدلة، الأخطاء الشائعة، الأخلاقيات
06_COGNITIVE_SCIENCE/      24 مهارة استدلال، مكتبة التحيزات، أدوات قياس التفكير النقدي، انتقال التعلم
07_LEARNING_SCIENCE/       الأساس العلمي، نموذج التقييم المرتكز على الأدلة، نموذج الإتقان، خطة التحقق التربوي
08_ARAB_AUDIENCE_AND_CULTURE/  الجمهور العربي، بناء العالم، سياسة الفئات العمرية، اللغة واللهجات، 25 فكرة محلية
09_COMPETITIVE_INTELLIGENCE/  المنافسون عالمياً وعربياً، مصفوفة الفجوات، المساحات البيضاء، القدرة الدفاعية
10_TECHNICAL_ARCHITECTURE/   محرك القضايا، مخطط JSON، حدود شخصيات الذكاء الاصطناعي، أدوات التأليف، المخاطر
11_RIGHTS_PRIVACY_AND_SAFETY/  الملكية الفكرية، مصفوفة الاستخدام التجاري، خصوصية القاصرين، حوكمة المحتوى
12_KNOWLEDGE_OBJECTS/      254 وحدة معرفة في 7 أنواع + 1,735 مقطع RAG
13_CASE_DESIGN_REFERENCE/  دليل تصميم القضايا، القالب، قضية نموذجية كاملة، 25 نمطاً، قوائم الفحص، خط الإنتاج
14_PRODUCT_RESEARCH_SYNTHESIS/  الرؤية، التمايز، الإطار التعليمي، 15 اتجاه ابتكار، التقرير الاستراتيجي، الموسم الأول، MVP
99_LEGAL_SOURCE_ASSETS/    نصوص في الملك العام فقط، مع أساسها القانوني
athar_library.sqlite       قاعدة بحث جاهزة (مصادر، وحدات، مقاطع، بحث نصي كامل)
```

## قواعد قراءة المحتوى
- كل ادعاء مسنود بمعرّف `[ATH-SRC-####]` (الفهرس) أو `KO-…` (وحدة معرفة)، أو موسوم: `[حقيقة موثقة]` · `[تفسير بحثي]` · `[افتراض تصميمي]` · `[استنتاج استثماري]`.
- درجات الأدلة: A معايير ومصادر أولية ومراجعات منهجية · B بحث محكّم · C وثائق رسمية لمنتجات · D آراء وصحافة · E ضعيف (للمراجعة فقط).
- حالة الحقوق لكل مصدر في `01_SOURCE_CATALOG/rights_register.csv`. «متاح للقراءة» لا يعني «مسموح بالاستخدام التجاري».
- لا شيء هنا رأي قانوني أو علمي نهائي.

## البحث في المكتبة
```
sqlite3 athar_library.sqlite "SELECT kind, ref_id, title FROM search WHERE search MATCH 'confirmation' LIMIT 10;"
```
تفاصيل الاستيراد إلى PostgreSQL/Supabase أو نظام RAG: `00_PROJECT_CONTROL/FINAL_HANDOFF_MANIFEST.md` §11.
