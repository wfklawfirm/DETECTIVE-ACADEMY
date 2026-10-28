> **أرشيف:** بيان تسليم الدفعة الأولى (2026-10-27 صباحاً). البيان الحالي هو `FINAL_HANDOFF_MANIFEST.md` (v2).

# FINAL HANDOFF MANIFEST — مكتبة أَثَر المعرفية (ATHAR Research & Knowledge Library)

**تاريخ التسليم:** 2026-10-27 · **الحالة:** الدفعة الأولى مكتملة (تأسيس + بحث + سد فجوات + تركيب + تدقيق مستقل). المكتبة قابلة للاستعمال في قرارات التصميم، مع فجوات موثقة تمنع قرارات الإطلاق والاستثمار النهائية (انظر §9).
كل الأرقام أدناه مولّدة آلياً من `01_SOURCE_CATALOG/merge_report.json` و`tools/library_stats.py`، لا مكتوبة يدوياً.

---

## 1. الأرقام مقابل مستهدفات الموجز (§2)

| المستهدف في الموجز | المطلوب | المتحقق | ملاحظة |
|---|---|---|---|
| سجلات مصادر فريدة موثقة | 250–400 | **816** فريداً (847 سجلاً خاماً؛ 31 تكراراً دُمج) | 786 «متحقق منه»، 30 «بحاجة لمراجعة خبير» |
| بطاقات تحليل معمقة | 60–100 | **83** ملف بطاقة تغطي 108 مصادر | بعض البطاقات تحلل مصادر مترابطة معاً |
| أعمال أدب بوليسي للتحليل المقارن | 25–40 | **67** عملاً في المكتبة 02 | + 20 مرجعاً نقدياً/نظرياً/قانونياً |
| مراجع تصميم الغموض والألعاب | 25–40 | **45** مرجعاً + **34** لعبة | |
| مراجع علمية في الأدلة والعلوم الجنائية | 40–60 | **63** | 16 بطاقة تخصص، مصفوفة صلاحية 24 طريقة |
| التفكير النقدي والتعلم والتقييم | 35–50 | **141** (06: 76 + 07: 65) | |
| منتجات منافسة | 40–60 | **111** (65 عالمياً + 46 عربياً) | مصفوفة فجوات لأهم 35 |
| مصادر الجمهور العربي | 20–30 | **86** | |
| نماذج أصلية لأنماط القضايا | 25 | **25** (ARC-01…ARC-25) | 2 فقط قريبة من القتل (8%) |
| مراجع أساسية للنسخة الأولى | 30–50 | **49** | 24 A، 18 B، 7 C |

**تنبيه على تجاوز المستهدفات:** التجاوز ليس حشواً؛ كل سجل مرّ بالتحقق ويحمل رابط التحقق. لكن توزيع الدرجات يوضح أن جزءاً كبيراً وثائق منتجات ومنافسين: **A 214 · B 237 · C 282 · D 82 · E 1**. للحقائق العلمية اعتمد على A وB فقط.

## 2. حالة المصادر

| البند | العدد |
|---|---|
| إجمالي المصادر الفريدة | 816 |
| متحقق منها (`verified`) | 786 |
| بحاجة لمراجعة خبير (موجودة لكن لم يُستخرج محتواها كاملاً) | 30 — جدول كامل في `RESEARCH_GAPS.md` |
| مرشحون لم يمكن التحقق منهم فاستُبعدوا من الفهرس | نحو 200 سطر في قوائم «Unverified candidates» في تقارير الفرق الأحد عشر (`*/_data/agent_report*.md`)؛ بعضها تحقق لاحقاً في جولة سد الفجوات. **لم يدخل الفهرس أي مصدر دون تحقق.** |
| طرق التحقق | جلب صفحة رسمية 488 · سجل DOI/فهرس 208 · ويكيبيديا للبيانات الببليوغرافية فقط 92 · صفحة ناشر 19 · نتيجة بحث 9 |
| التدقيق المستقل | عينة 76 سجلاً: 58 سليم، 18 طفيف، **0 جوهري، 0 مختلق** (فاصل Wilson 95% للأخطاء الجوهرية: 0–4.8%). صُحح 23 سجلاً. `01_SOURCE_CATALOG/verification_log.md` |

## 3. الملفات الأصلية المحفوظة قانونياً
**9 نصوص** في الملك العام عالمياً (Doyle ×6، Collins، Chesterton ×2) في `99_LEGAL_SOURCE_ASSETS/PUBLIC_DOMAIN_VERIFIED/` مع ترويسة ترخيص Project Gutenberg وبصمات SHA-256 والأساس القانوني لكل ولاية قضائية (`99_LEGAL_SOURCE_ASSETS/README.md`). لا نصوص محمية؛ لا نصوص لكريستي. نصوص Poe لم تُحفظ (فجوة G14).

## 4. وحدات المعرفة المستخرجة

| النوع | الملف | العدد |
|---|---|---|
| أنماط سردية (NP) | `12_KNOWLEDGE_OBJECTS/narrative_patterns.jsonl` | 46 |
| مهارات استدلال (RS) | `reasoning_skills.jsonl` | 38 |
| مفاهيم جنائية (FC) | `forensic_concepts.jsonl` | 32 |
| آليات قضايا (CM) | `case_mechanics.jsonl` | 46 |
| تقييمات تعلم (LA) | `learning_assessments.jsonl` | 35 |
| أنماط تصميم الشخصيات (CD) | `character_design_patterns.jsonl` | 29 |
| فرص منتج (PO) | `product_opportunities.jsonl` | 28 |
| **المجموع** | | **254** — كلها مرتبطة بمصادر الفهرس (0 مراجع يتيمة) |
| نماذج قضايا | `13_CASE_DESIGN_REFERENCE/case_archetypes.jsonl` | 25 |
| مقاطع RAG من كل الوثائق | `12_KNOWLEDGE_OBJECTS/rag_chunks.jsonl` | 1,735 |

## 5. حالة حقوق المصادر

| الحالة | العدد | المعنى العملي |
|---|---|---|
| COPYRIGHTED_RESTRICTED | 577 | تحليل وإحالة واقتباس قصير فقط |
| UNKNOWN | 123 | لا يُفترض أي إذن |
| PUBLIC_DOMAIN | 62 | مع تحديد الولاية القضائية لكل سجل — كثير منها «الولايات المتحدة فقط» |
| OPEN_LICENSE | 53 | بحسب نوع الترخيص (CC BY / BY-NC-ND / MIT / OGL…) |
| LICENSED | 1 | |
| يُسمح بإعادة الاستخدام التجاري صراحة | 50 | |
| يُسمح بالتخزين الداخلي صراحة | 89 | |

السجل الكامل مع قواعد الاستخدام لكل حالة: `01_SOURCE_CATALOG/rights_register.csv` = `11_RIGHTS_PRIVACY_AND_SAFETY/SOURCE_RIGHTS_REGISTER.csv`. **كل ذلك بحث قانوني يحتاج مراجعة محامٍ مرخّص في كل ولاية قضائية.**

## 6. أهم النتائج المؤكدة
1. **السوق العربية لم تعد فارغة، والآليات ليست خندقاً.** سبعة إطلاقات تحقيق عربية بين يوليو وأكتوبر 2026، أقربها Homicide Desk [ATH-SRC-1153]؛ كل آلية لعب متصورة لـ ATHAR موجودة عند منافس. (`09/ATHAR_DEFENSIBILITY_ANALYSIS.md`)
2. **الفراغ مؤسسي وقياسي:** بين 23 منتج تحقيق، لا أحد يقيّم عملية الاستدلال بمعايير معلنة، ولا وضع معلم كامل، ولا تقييم متحقق منه، ولا تصميم معلن للمراهقين. (`09/FEATURE_GAP_MATRIX.csv`)
3. **مدخل مدرسي موثق:** مادة «التفكير الناقد» في الخطط الدراسية السعودية [ATH-SRC-0758].
4. **حل الألغاز وحده لا ينقل المهارة:** الانتقال البعيد يتلاشى تقريباً مع تحسن تصميم الدراسات [ATH-SRC-0533]؛ ما ينتقل هو المبدأ المسمّى والمعلَّم صراحة مع تغذية راجعة، وبأثر صغير (تحليل بعدي 2025 لـ 54 تجربة عشوائية لإزالة التحيز: g = 0.26) [ATH-SRC-0574]. (`06/LEARNING_TRANSFER_RESEARCH.md`)
5. **قضية واحدة لا تقيس مهارة:** المطلوب 6–10 قضايا لكل مهارة مع عرض عدم اليقين؛ تسمية الجاني دليل ضعيف بسبب التخمين. (`07/ATHAR_LEARNING_SCIENCE_FOUNDATION.md`)
6. **موثوقية العلوم الجنائية طيف لا حكم واحد:** من قوية (DNA أحادي المصدر) إلى غير مدعومة (مقارنة عضات الأسنان) [ATH-SRC-0301][ATH-SRC-0304][ATH-SRC-0305]؛ أخطاء التقرير والشهادة أكثر ضرراً من أخطاء المختبر. (`04/FORENSIC_METHOD_VALIDITY_MATRIX.csv`)
7. **لغة الجسد ليست دليلاً على الكذب** (دقة البشر نحو 54%)؛ الاستجواب الاتهامي يزيد الاعترافات الكاذبة، والمراهقون أكثر عرضة. (`05/ETHICAL_INVESTIGATION_PRINCIPLES.md`)
8. **النموذج اللغوي لا يحفظ الأسرار ولا يمنع الاختلاق بالتوجيه وحده:** الحقيقة يجب أن تبقى خارج النموذج؛ وعدالة القضية قابلة للفحص الآلي قبل النشر (فاحص مجرّب على 6 نسخ معيبة). (`10/CASE_ENGINE_TECHNICAL_RESEARCH.md`، `13/tools/check_case.py`)
9. **حقوق كريستي تختلف بحسب السوق:** ملك عام في لبنان والإمارات والأردن وقطر والسعودية في 1 يناير 2027؛ في مصر انقضت في 12 يناير 2026 (الاحتساب من تاريخ الوفاة)؛ محمية في المملكة المتحدة والاتحاد الأوروبي حتى نهاية 2046 [ATH-SRC-1076][ATH-SRC-1077][ATH-SRC-1009]. والتوصية: قضايا أصلية ببنى مستعارة فقط.
10. **ادعاءات «تدريب الدماغ» تخضع للإنفاذ:** تسوية FTC مع Lumosity [ATH-SRC-0639] — سجل الادعاءات في `07/EDUCATIONAL_VALIDATION_PLAN.md` يجب أن يحكم كل تسويق.

## 7. أهم النتائج غير المؤكدة أو الضعيفة
- هل يجد المراهقون العرب القضايا الآمنة غير العنيفة ممتعة؟ (لا دليل؛ اختبار K1 في `MVP_SCOPE.md`)
- هل هناك طلب على الغموض السردي تحديداً؟ صدارة «الألغاز» في متاجر الخليج ومصر تخص الألعاب العرضية غالباً.
- عدالة التصحيح الآلي للنص العربي بين الفصحى واللهجات: لم يُعثر على أي دراسة.
- أحجام أثر التلميحات وصعوبة اللعب مأخوذة من ألعاب رياضيات لا من قضايا سردية.
- أي رقم لحجم السوق الإقليمي؛ كلفة تأليف القضية الفعلية؛ كلفة الذكاء الاصطناعي بالعربية (تقدير نحو 3 أضعاف رموز الإنجليزية). «(AUDIT-W2)» صُحح في الدفعة الثانية: ≈1.2× في المرمّزات الحالية، و«3×» تخص cl100k القديم وحده (C1؛ `10/ARABIC_TOKEN_COST_MEASUREMENT.md`).
- بعض ادعاءات محتوى الأعمال النظرية (Todorov وGinzburg وSternberg) من معرفة سابقة، موسومة بثقة متوسطة.
- 92 سجلاً أساسها ويكيبيديا للبيانات الببليوغرافية فقط (أعمال أدبية وألعاب)، لا لحقائق علمية.

## 8. التعارضات بين المكتبات
عشرة تعارضات سُجلت وحُسمت مؤقتاً بالقاعدة الأشد أماناً في `CROSS_LIBRARY_RECONCILIATION.md` (أبرزها: لا وفاة لفئة 13–15؛ سلم تلميحات من 5 مستويات؛ الحوار بالنموذج اللغوي مطفأ افتراضياً).

## 9. أهم عشر فجوات متبقية (التفاصيل والخطوات التالية في `RESEARCH_GAPS.md`)
| # | الفجوة | الأثر |
|---|---|---|
| G01 | نصوص حماية البيانات العربية الناقصة، سن الأهلية، نقل حوار القاصر إلى مزوّد ذكاء اصطناعي أجنبي | **يمنع الإطلاق** في الخليج ومصر ولبنان وقطر |
| G02 | انطباق التصنيف العمري الرسمي على تطبيق تعليمي تفاعلي | **يمنع الإطلاق** في السعودية والإمارات |
| G03 | سلوك شخصيات الذكاء الاصطناعي بالعربية مع القاصرين | يمنع ميزة الشخصيات الحوارية |
| G04 | عدالة التصحيح الآلي بين الفصحى واللهجات | يمنع عرض أي درجة على نص حر |
| G05 | مراجعة علمية جنائية + مسرد عربي | يمنع نشر المحتوى الجنائي |
| G06 | لا محك خارجي عربي مقنن لمهارات الاستدلال (13–18) | يمنع أي ادعاء تعليمي |
| G07 | لا دليل على التعلم أو الانتقال لدى مراهقين عرب | يمنع الادعاءات التسويقية |
| G08 | لا بيانات تمثيلية عن المراهقين العرب 13–17 ولا عن الطلب | يمنع قرار الاستثمار |
| G09 | الفصحى المبسطة مقابل الحوار اللهجي لدى المراهقين | يمنع قرار خط إنتاج المحتوى |
| G10 | مخرجات مقرر التفكير الناقد السعودي ومسار الشراء المدرسي | يمنع قرار المسار المدرسي |

## 10. توصيات الانتقال إلى تصميم المنتج
(التفصيل في `14_PRODUCT_RESEARCH_SYNTHESIS/FINAL_STRATEGIC_REPORT.md` و`MVP_SCOPE.md`)
1. **موّلوا مرحلة تحقق مدتها 6–9 أشهر، لا بناءً كاملاً** «(AUDIT-W2)» عُدّلت المدة في الدفعة الثانية إلى **9–12 شهراً** (D4 في `14/FINAL_STRATEGIC_REPORT.md`؛ C17)، بنقاط إيقاف محددة مسبقاً: المتعة (K1)، ثبات التقييم ≥ 0.70 (K2)، التزام مدرسي مدفوع خلال 12 شهراً (K3).
2. **التموضع:** «قضايا عربية للمراهقين والمدارس تُظهر كيف تفكر، لا فقط من الجاني»؛ احذفوا «الأول» و«الذكاء الاصطناعي» من الرسائل.
3. **النسخة الأولى بلا نموذج لغوي وقت اللعب:** حقيقة ثابتة مؤلفة، شاشة حجة منظمة تُصحَّح حتمياً، فاحص عدالة قبل النشر؛ الذكاء الاصطناعي لمساعدة الكتّاب فقط.
4. **التجارب الثلاث الأولى:** اختبار متعة على نموذج نصي؛ A/B لشاشة الحجة مقابل الاتهام وحده؛ تجربة صفية في 4–6 صفوف تنتهي بطلب التزام مدفوع.
5. **الموسم الأول:** ARC-01 وARC-03 وARC-04 وARC-08 وARC-21، كلها غير عنيفة للفئة 13–15، بجهد تقديري 1,100–2,200 ساعة `[افتراض تصميمي]`. ملاحظة: نسبة القضايا بلا جانٍ (37.5%) أعلى من الهدف (20–30%) — تُراجع.
6. **قبل أي إطلاق:** إغلاق G01 وG02 برأي محامين محليين؛ مراجعة خبير جنائي (G05)؛ اعتماد `CONTENT_AND_SAFETY_GOVERNANCE.md`.
7. **أدوات الإنتاج جاهزة للبدء:** `CASE_TEMPLATE.md` + `case_schema.json` + `tools/check_case.py` + قوائم الفحص الثلاث + `CASE_PRODUCTION_PIPELINE.md`.

## 11. طريقة الاستيراد إلى قاعدة بيانات أو نظام RAG

**الخيار الأسرع — SQLite الجاهز:** `athar_library.sqlite` (في جذر المكتبة) يحتوي الجداول:
- `sources` — كل حقول الفهرس (القوائم مخزنة JSON نصاً)
- `knowledge_objects` + `ko_sources` (ربط كل وحدة بمصادرها)
- `doc_chunks` — 1,735 مقطعاً من كل الوثائق مع مسار العناوين والمصادر المذكورة
- `search` — فهرس بحث نصي كامل FTS5 عبر المصادر والوحدات والمقاطع

```sql
-- مثال: كل المصادر من الدرجة A عن التحيز المعرفي
SELECT source_id, title, year FROM sources
WHERE evidence_grade='A' AND topics LIKE '%bias%';
-- مثال: بحث نصي كامل
SELECT kind, ref_id, title FROM search WHERE search MATCH 'transfer' LIMIT 20;
-- مثال: الوحدات المعرفية المبنية على مصدر محدد
SELECT k.ko_id, k.name FROM knowledge_objects k JOIN ko_sources s USING(ko_id)
WHERE s.source_id='ATH-SRC-0301';
```

**PostgreSQL / Supabase مع pgvector:**
1. أنشئ جداول تعكس أعمدة `sources_master.csv` و`knowledge_objects` (عمود `jsonb` للسجل كاملاً) و`doc_chunks(chunk_id, file, library, heading_path, text, source_ids jsonb, embedding vector)`.
2. حمّل `01_SOURCE_CATALOG/sources_master.csv` بـ `\copy` (الترميز UTF-8 مع BOM)، وحمّل ملفات JSONL سطراً سطراً إلى أعمدة `jsonb`.
3. للاسترجاع الدلالي: أنشئ تضمينات (embeddings) لحقل `text` في `12_KNOWLEDGE_OBJECTS/rag_chunks.jsonl` (المقاطع ≤ 3,500 حرف، مقسمة على العناوين) ولحقل `summary_ar` في وحدات المعرفة، واحتفظ بـ `source_ids` بيانات وصفية ليُستشهد بها في كل إجابة.
4. **قاعدة حقوق إلزامية في RAG:** لا تُدخل نصاً كاملاً إلا لما حقوقه تسمح (`rights_register.csv` → `rule_may_use_in_rag`). الوثائق التحليلية في المكتبة من تأليف المشروع ويجوز إدخالها.

**إعادة البناء بعد أي إضافة:**
```
python3 -I 00_PROJECT_CONTROL/tools/merge_catalog.py . --rewrite-aliases
python3 -I 00_PROJECT_CONTROL/tools/library_stats.py .
```
(المصادر الجديدة تُضاف إلى `<المكتبة>/_data/sources.jsonl` بالمعرّف التالي ضمن كتلة المكتبة — انظر `RESEARCH_PROTOCOL.md` §3.)

## 12. الملفات التي ينبغي إرسالها إلى ChatGPT لاستكمال تطوير ATHAR
جُمعت في حزمة منفصلة **`ATHAR_CONTEXT_PACK.zip`** بهذا الترتيب (أرسلها بهذا الترتيب؛ الثلاثة الأولى تكفي لمحادثة استراتيجية):

| # | الملف | لماذا |
|---|---|---|
| 1 | `14_PRODUCT_RESEARCH_SYNTHESIS/FINAL_STRATEGIC_REPORT.md` | الإجابات عن الأسئلة العشرين والقرارات المطلوبة |
| 2 | `14_PRODUCT_RESEARCH_SYNTHESIS/MVP_SCOPE.md` | النسخة الأولى والتجارب الثلاث ونقاط الإيقاف |
| 3 | `00_PROJECT_CONTROL/CROSS_LIBRARY_RECONCILIATION.md` | القواعد المعتمدة عند التعارض |
| 4 | `14_PRODUCT_RESEARCH_SYNTHESIS/FIRST_SEASON_RECOMMENDATIONS.md` | الموسم الأول |
| 5 | `14_PRODUCT_RESEARCH_SYNTHESIS/EDUCATIONAL_FRAMEWORK.md` | نموذج التعلم والتقييم وسجل الادعاءات |
| 6 | `14_PRODUCT_RESEARCH_SYNTHESIS/PRODUCT_DIFFERENTIATION.md` | التمايز وما يجب التوقف عن ادعائه |
| 7 | `13_CASE_DESIGN_REFERENCE/CASE_DESIGN_BIBLE.md` | دستور كتابة القضايا |
| 8 | `13_CASE_DESIGN_REFERENCE/CASE_TEMPLATE.md` | قالب القضية |
| 9 | `13_CASE_DESIGN_REFERENCE/SAMPLE_CASE_001.md` + `sample_case_001.json` | مثال كامل صالح للمخطط |
| 10 | `13_CASE_DESIGN_REFERENCE/CASE_ARCHETYPES.md` | 25 نمط قضية |
| 11 | `10_TECHNICAL_ARCHITECTURE/case_schema.json` + `CASE_SCHEMA_PROPOSAL.md` + `AI_CHARACTER_GUARDRAILS.md` | الهندسة والقيود |
| 12 | `08_ARAB_AUDIENCE_AND_CULTURE/AGE_APPROPRIATE_CONTENT_POLICY.md` + `ARABIC_LANGUAGE_AND_DIALECT_STRATEGY.md` | السلامة واللغة |
| 13 | `02_DETECTIVE_LITERATURE/FAIR_PLAY_MYSTERY_RULEBOOK.md` | قواعد العدالة القابلة للاختبار |
| 14 | `07_LEARNING_SCIENCE/EVIDENCE_CENTERED_ASSESSMENT_MODEL.md` | نموذج التقييم |
| 15 | `14_PRODUCT_RESEARCH_SYNTHESIS/CORE_REFERENCES_V1.md` | المراجع الأساسية |
| 16 | `00_PROJECT_CONTROL/RESEARCH_GAPS.md` | ما لم يُحسم بعد |

لطلب تحليلات تتطلب الفهرس كاملاً: أرسل `01_SOURCE_CATALOG/sources_master.csv` أو `12_KNOWLEDGE_OBJECTS/*.jsonl`.

## 13. الملفات التي أُنشئت فعلياً
الجرد الكامل لكل ملف ومساره وحجمه: `00_PROJECT_CONTROL/FILE_INVENTORY.csv`. الملفات الرئيسية:

- **00_PROJECT_CONTROL:** README (في الجذر)، RESEARCH_MASTER_PLAN، RESEARCH_PROTOCOL، PROGRESS_LOG، RESEARCH_GAPS، CROSS_LIBRARY_RECONCILIATION، FINAL_HANDOFF_MANIFEST، FILE_INVENTORY.csv، MASTER_PROMPT_ORIGINAL، tools/ (merge_catalog.py، library_stats.py، manual_merges.csv)
- **01_SOURCE_CATALOG:** sources_master.csv/.jsonl، bibliography.md، rights_register.csv، id_aliases.csv، merge_report.json، verification_sample.csv، verification_log.md
- **02:** DETECTIVE_LITERATURE_ATLAS (50 مبدأ)، MYSTERY_PLOT_PATTERNS (26 نمطاً)، FAIR_PLAY_MYSTERY_RULEBOOK (59 قاعدة)، LITERARY_RIGHTS_REGISTER.csv (54 صفاً)
- **03:** INTERACTIVE_MYSTERY_DESIGN_BIBLE، GAME_MECHANICS_PATTERN_LIBRARY (39 آلية)، EVIDENCE_BOARD_UX_RESEARCH، HINT_AND_DIFFICULTY_SYSTEM، INTERACTIVE_STORY_COMPETITOR_MATRIX.csv
- **04:** FORENSIC_SCIENCE_KNOWLEDGE_ATLAS (16 تخصصاً)، FORENSIC_METHOD_VALIDITY_MATRIX.csv (24 طريقة)، SAFE_VIRTUAL_LABS_CATALOG (30 مختبراً، أفضل 10)، CSI_MYTHS_AND_SCIENTIFIC_CORRECTIONS، FORENSIC_EXPERT_REVIEW_CHECKLIST
- **05:** INVESTIGATIVE_REASONING_FRAMEWORK، EVIDENCE_EVALUATION_GUIDE، COMMON_REASONING_ERRORS، ETHICAL_INVESTIGATION_PRINCIPLES
- **06:** REASONING_SKILLS_TAXONOMY (24 مهارة)، COGNITIVE_BIAS_CASE_LIBRARY (17 تحيزاً)، CRITICAL_THINKING_ASSESSMENT_FRAMEWORK، LEARNING_TRANSFER_RESEARCH
- **07:** ATHAR_LEARNING_SCIENCE_FOUNDATION، EVIDENCE_CENTERED_ASSESSMENT_MODEL، LEARNER_MASTERY_MODEL، LEARNING_OUTCOMES_TO_GAMEPLAY_MAP.csv، EDUCATIONAL_VALIDATION_PLAN
- **08:** ARAB_AUDIENCE_RESEARCH، ARABIC_MYSTERY_WORLD_BUILDING، AGE_APPROPRIATE_CONTENT_POLICY، ARABIC_LANGUAGE_AND_DIALECT_STRATEGY، LOCAL_STORY_OPPORTUNITIES (25 فكرة)، ARABIC_LANGUAGE_RESEARCH_EVIDENCE
- **09:** GLOBAL_ و ARAB_COMPETITOR_INTELLIGENCE، FEATURE_GAP_MATRIX.csv، INNOVATION_COMPETITOR_CHECK.csv، WHITE_SPACE_OPPORTUNITIES، ATHAR_DEFENSIBILITY_ANALYSIS، _data/competitors_global.csv و competitors_arab.csv
- **10:** CASE_ENGINE_TECHNICAL_RESEARCH، CASE_SCHEMA_PROPOSAL + case_schema.json، AI_CHARACTER_GUARDRAILS، NARRATIVE_AUTHORING_TOOLS_COMPARISON، ASSESSMENT_ENGINE_TECHNICAL_MODEL، TECHNICAL_RISKS_AND_MITIGATIONS، prototypes/
- **11:** INTELLECTUAL_PROPERTY_RESEARCH، SOURCE_RIGHTS_REGISTER.csv، COMMERCIAL_USE_DECISION_MATRIX، CHILD_AND_TEEN_PRIVACY_REQUIREMENTS، CONTENT_AND_SAFETY_GOVERNANCE
- **12:** سبعة ملفات وحدات معرفة + rag_chunks.jsonl + orphan_references.json
- **13:** CASE_DESIGN_BIBLE، CASE_TEMPLATE، SAMPLE_CASE_001 (.md + .json)، CASE_ARCHETYPES (.md + .jsonl)، FAIR_PLAY_CHECKLIST، SCIENTIFIC_REVIEW_CHECKLIST، AGE_APPROPRIATENESS_CHECKLIST، CASE_PRODUCTION_PIPELINE، tools/check_case.py
- **14:** ATHAR_VISION_RECOMMENDATIONS، PRODUCT_DIFFERENTIATION، EDUCATIONAL_FRAMEWORK، INNOVATION_DIRECTIONS (15 اتجاهاً × 11 حقلاً)، FINAL_STRATEGIC_REPORT، FIRST_SEASON_RECOMMENDATIONS، MVP_SCOPE، OPEN_QUESTIONS_FOR_NEXT_PHASE (~90 سؤالاً)، CORE_REFERENCES_V1 (.md + .csv)
- **99:** README + 9 نصوص في الملك العام
- **الجذر:** athar_library.sqlite

## 14. حدود هذه الدفعة (للأمانة)
- حصة بحث مشتركة بين الفرق نفدت مبكراً في الجولة الأولى؛ عُوّضت جزئياً بجلب الصفحات الرسمية وسجلات DOI وبجولة سد فجوات كاملة.
- لا وصول إلى قواعد بيانات مدفوعة (Scopus، JSTOR، تقارير السوق المدفوعة)؛ كثير من المقالات قُرئ ملخصها لا نصها الكامل.
- مواقع حجبت الجلب الآلي: GDC Vault، PEGI، بعض مواقع الجهات الرسمية الخليجية، Instagram.
- أعيد تشغيل الحاوية مرة واحدة أثناء العمل دون فقدان ملفات.
- لا شيء في المكتبة رأي قانوني أو علمي نهائي؛ المحتوى الجنائي والقانوني يحتاج مراجعة خبير مستقل قبل أي استخدام عام.
