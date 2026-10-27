# خريطة من البحث إلى المنتج — RESEARCH_TO_PRODUCT_MAP (المرحلة 0)

**تاريخ الإعداد:** 2026-10-27 (لقطة الشفرة الساعة 21:42 بتوقيت الخادم) · **المدخلات:** `KNOWLEDGE_EXTRACTION_MATRIX.md` ومدخلاته، وقراءة مباشرة لملفات `/home/claude/athar/{src,content,migrations,scripts}`.

> **تنبيه حول الحالة:** الشفرة قيد التطوير أثناء كتابة هذه الوثيقة (ظهرت ملفات جديدة بين قراءتين). التصنيف أدناه يعني «الملف أو الحقل **موجود** في اللقطة»، لا أنه **مُختبَر**: لم أشغّل `npm run verify` ولا الاختبارات، ومجلدا `tests/unit` و`tests/e2e` فارغان لحظة الفحص، ومجلد `src/ai` فارغ. أي «منفَّذ» هنا يحتاج تأكيداً بالتشغيل.

**مفتاح الحالة:** ✔ منفَّذ (موجود في اللقطة) · ◐ جزئي · ○ مخطط/لم يُبدأ · ⛔ ممنوع عمداً (قيد تصميم يُنفَّذ بغياب الميزة).

## 1. بنية المستودع الفعلية (لقطة)

| المسار | الدور |
|---|---|
| `content/schema/case_schema.json` | سكيما القضية (نسخة مأخوذة من `10_TECHNICAL_ARCHITECTURE/case_schema.json`) |
| `content/cases/c000_lost_notebook.{json,ui.json,scoring.json}` | قضية تمهيد (12 دقيقة، `age_band: all`، 7 أدلة) |
| `content/cases/c001_last_observation.{json,ui.json,scoring.json}` | قضية «الرصد الأخير» (40 دقيقة، `16-18`، 16 دليلاً، 4 فرضيات) |
| `content/hooks/global.json` · `riddles.json` | 26 خطاف دخول و12 لغزاً قصيراً |
| `content/knowledge/ko_names.json` | 22 اسم KO بالعربية للعرض |
| `content/tracks/tracks.json` | 6 مسارات A–F، 3 دروس لكل مسار (18 درساً) |
| `migrations/001_init.sql` | 10 جداول (منها `schema_migrations`): `users`، `sessions`، `case_versions`، `case_reviews`، `play_states`، `review_tickets`، `audit_log`، `content_reports`، `hook_events` |
| `src/engine/*.ts` | محرك نقي (حالة، حوار، تقييم، تحقق، تسرب) |
| `src/server/*.ts` · `src/app/api/**` | طبقة الخادم وواجهات API |
| `src/app/**` · `src/components/**` | الصفحات: start، home، cases، case/[id]، play/[id]، academy، challenges، profile، account، privacy، report، review/[code]، studio |
| `scripts/*.ts` | `check-cases` · `check-tracks` · `leak-scan` · `qa-case` · `smoke` · `setup` · `migrate` · `seed` |

## 2. الخريطة

### 2.1 منهج الاستدلال والتقييم

| الرؤية البحثية | المصدر | الميزة/الوحدة في المنتج | المسار | الحالة |
|---|---|---|---|---|
| الإجابة = بنية استنتاج (فرضية + أدلة مذكورة + حدود + ما يغيّر رأيك) لا اسم الجاني | Golden Idol (bench)، `LA-07-002`، ECD O10 | نموذج `Submission` وواجهة «Deduce» | `src/engine/types.ts` (`Submission`)، `src/components/play/Deduce.tsx` | ✔ |
| تقييم حتمي معلن المعايير، والنص الحر لا يُصحَّح آلياً بل يُحال إلى مراجع بشري | `ARABIC_ASSESSMENT_AND_AI_EVIDENCE.md`، κ≈0.46 | `assess()` تُنتج درجة «مبدئية» مع إخلاء مسؤولية وتذكرة مراجعة | `src/engine/assess.ts`؛ جدول `review_tickets`؛ `src/app/api/studio/tickets`، `src/app/review/[code]` | ✔ |
| معيار rubric بسبعة معايير (مصدر، تناقض، روابط، عدم يقين، مراجعة، استبعاد، تبرير) | تضارب الأوزان (GAP_AND_CONFLICT_REPORT §1) | `rubric.criteria` + `criteria_map` في ملف التسجيل | `content/cases/*.scoring.json` | ◐ (أوزان 15/25/15/15/10/10/10 قرار مؤقت، خامس مجموعة أوزان في المشروع) |
| سجل فرضيات قابل للمراجعة: ثقة 0–100، موقف (مفتوح/متقدم/مستبعد)، روابط دعم/إضعاف، سجل تعديلات | `CM-10-006`، `05/INVESTIGATIVE_REASONING_FRAMEWORK.md` | `HypothesisEntry.revisions` وعمليات `hyp_add/conf/stance/link` | `src/engine/types.ts`، `src/engine/ops.ts`، `src/server/play.ts` | ✔ |
| معايرة الثقة بنطاق مقبول لكل فرضية | `KO-RS-06-021`، `LA-05-003` | `confidence_band` | `src/engine/ui-types.ts` (`ScoringSpec`) | ✔ (دون Brier) |
| قائمة «حدود ما تثبته الأدلة» وقائمة «ما قد يغيّر رأيي» بخيارات صالحة وغير صالحة | `05/EVIDENCE_EVALUATION_GUIDE`، `what_evidence_could_not_show_ar` | `limit_menu` و`mind_change_menu` | `content/cases/c001_last_observation.ui.json` | ✔ |
| لا كشف كذب من لغة الجسد | `KO-RS-05-007`، `ATH-SRC-0413` | خيار حدود غير صالح `l_invalid_demeanor` يُعاقب | `c001…ui.json`، `scoring.json` (`invalid_limits`) | ✔ |
| تسمية «الأدلة غير كافية» مخرجاً مشروعاً مقيَّماً | `CSI_MYTHS`، فجوة بياض في bench | خيار استنتاج مستقل | — (لا خيار في الفرضيات الأربع لـc001؛ السكيما لا تفرضه) | ○ |
| تأكيد الاستنتاجات على دفعات (Obra Dinn) لمنع التخمين | `bench_feature_gap` (Adopt P1) | — | — | ○ |
| تخمين صحيح ≠ استنتاج صحيح؛ تقييم الاستشهاد | `LA-07-002` | إلزام ذكر دليل واحد على الأقل (حتى 12) وفحص ملكيته | `validateSubmission` في `assess.ts` | ✔ |
| سقوف عند غياب الاستشهاد أو حل التعارض | تصميم المنتج | `caps.no_citations_max`، `no_conflict_resolution_max` | `ScoringSpec.caps` | ✔ |
| نموذج إتقان BKT + Beta وحالات insufficient/emerging/developing/secure | `07/LEARNER_MASTERY_MODEL.md` | — | لا جدول مهارات ولا حساب إتقان في `migrations/001_init.sql` | ○ |
| مصحح عربي صغير مضبوط + اختبار «الحجة الفصيحة الفارغة» | ECD v2 | `ATHAR_AI_PROVIDER=local` فقط؛ `src/ai` فارغ | `src/server/env.ts`، `.env.example` | ○ |

### 2.2 اللعب العادل ومحرك القضية

| الرؤية | المصدر | الميزة | المسار | الحالة |
|---|---|---|---|---|
| حقيقة القضية حتمية والمخفي لا يغادر الخادم | `CASE_ENGINE_TECHNICAL_RESEARCH.md`، `AI_CHARACTER_GUARDRAILS.md` | عرض اللاعب يُسقَط من الحقيقة (`projectView`)؛ `play_states` لا تحوي حقيقة | `src/engine/project.ts`، تعليق `migrations/001_init.sql` | ✔ |
| الأدلة قابلة للوصول؛ ≥2 مساري إثبات منفصلين | `FAIR_PLAY_MYSTERY_RULEBOOK`، `check_case.py` | `reachableSets` و`QAReport` (`proof_paths`، `unreachable_evidence`) | `src/engine/validate.ts`، `scripts/check-cases.ts` | ◐ (إعادة تنفيذ تقريبية؛ لا ASP/clingo؛ c000 يشترط مسارًا واحداً) |
| لا تسرب للحل في النصوص المقروءة قبل الكشف (4-gram/Jaccard) | X05/X09 | فاحص تسرب | `src/engine/leak.ts`، `scripts/leak-scan.ts` | ✔ |
| بوابة نشر: سبع مراجعات ببصمة المحتوى، وأربع أعين (الكاتب لا يعتمد ولا ينشر) | `CONTENT_AND_SAFETY_GOVERNANCE` G1–G6، `check_case.py` A9 | `case_reviews.role` بسبع قيم، `publish()` | `migrations/001_init.sql`، `src/server/studio.ts`، `src/app/api/studio/*` | ✔ |
| لا قضية تُنشر قبل مراجعة بشرية؛ وضع المعاينة مُعلَن | حزمة V1: «لا إطلاق عام» | `ATHAR_ALLOW_PREVIEW` مع لافتة PREVIEW | `src/server/env.ts` (`allowPreview`)، `.env.example` | ◐ (`.env.example` يضع `true` بينما `env.ts` يقارن بالقيمة `"1"` تماماً: عدم اتساق يجب حسمه؛ ويجب تعطيله قبل أي إطلاق) |
| `expert_review` بحالة pending لكل الأدوار | `SAMPLE_CASE_001` | القضيتان بلا اعتماد (`content_hash: "unbound"`) | `content/cases/c00*.json` | ✔ (والأهم: لا مراجعة بشرية جرت) |
| `fairness_test.runs` فارغ | `check_case.py` | لم يُسجَّل تشغيل | `content/cases/*.json` | ○ |

### 2.3 الشخصيات والحوار

| الرؤية | المصدر | الميزة | المسار | الحالة |
|---|---|---|---|---|
| شخصيات بحدود معرفة (knows/hides/believes) لا تكشف ما تجهله | `AI_CHARACTER_GUARDRAILS`، `CD-10-001` | `character_knowledge` + مواضيع `topics` + سطور مؤلَّفة | `src/engine/dialogue.ts`، `src/engine/types.ts` | ✔ |
| الشخصية تردّ بسطر مؤلَّف احتياطي عند ما يتجاوز المعرفة (`deflect_unknown`، `refuse_secret`، `safety_exit`) | الحاجز الحتمي | `AuthoredLine.purpose` | `src/engine/types.ts` | ✔ |
| `llm_enabled=false` وقت اللعب | FSR D3 | حوار قواعدي بمطابقة مواضيع (تطبيع عربي) بحد أقصى 3 أسطر | `dialogue.ts` (`MAX_LINES = 3`)، `src/lib/arabic.ts` | ✔ (لا نموذج لغوي موصول) |
| تقديم دليل لشخصية يفتح اعترافاً/حقيقة | `CM-03-008` | `presentEvidence` | `src/engine/present.ts` | ✔ |
| مفتاح إيقاف الذكاء الاصطناعي لكل سوق (مصر/قطر/لبنان) | `ARAB_MARKET_LAUNCH_COMPLIANCE_MATRIX` | — | — | ○ (لا نموذج، فلا حاجة بعد) |
| شارة «هذه آلة» دائمة على شخصيات الذكاء الاصطناعي | `CONTENT_AND_SAFETY_GOVERNANCE` | — | — | ○ |

### 2.4 الجذب والاحتفاظ (فضول لا خسارة)

| الرؤية | المصدر | الميزة | المسار | الحالة |
|---|---|---|---|---|
| خطاف واحد لكل دخول بلا عدّاد خسارة ولا لوم على الغياب، قابل للتخفيف | `ATHAR_DIFFERENTIATION_STRATEGY` §6 | `hooks.ts` + `gentle_hooks` + `hook_events` | `src/engine/hooks.ts`، `src/components/EntryHook.tsx`، `content/hooks/global.json` | ✔ |
| ألغاز قصيرة أصلية؛ الإجابة تُفحص في الخادم | — | `/api/riddle` | `content/hooks/riddles.json`، `src/app/api/riddle/route.ts` | ✔ |
| «شريط فضول» يتراكم ولا يُصفَّر | bench (Adapt P1) | — | `src/app/challenges` موجودة؛ لا آلية سلسلة في المخطط | ○ |
| لا مؤقتات ولا ترتيب علني ولا تلميحات مدفوعة ولا عملات | PO-09C-006 | غيابها | لا جداول أو واجهات لها | ⛔ |
| خروج آمن/إيقاف ذاتي («يمكنك التوقف وسنحفظ كل شيء») | bench §6-10 | حفظ حالة اللعب لكل (مستخدم، قضية) | `play_states`، `src/server/progress.ts` | ◐ |
| حفظ حالة الجهاز بتوكن موقّع بدل حساب | PWA/خصوصية | `signToken/verifyToken` ووضع «device mode» | `src/server/crypto.ts`، `src/server/play.ts` (`token`) | ✔ |

### 2.5 التعلم والمسارات والنقل

| الرؤية | المصدر | الميزة | المسار | الحالة |
|---|---|---|---|---|
| ستة مسارات A–F بدروس قصيرة (3–7 دقائق) ببطاقة مبدأ ومثال ومسألة اختيار من متعدد | `LEARNING_TRANSFER_RESEARCH` P2 | `TracksSchema` (zod)، `Practice` | `src/engine/tracks.ts`، `content/tracks/tracks.json`، `src/app/academy/**`، `src/components/Practice.tsx`، `scripts/check-tracks.ts` | ◐ (تعريف المسارات A–F غير موجود في المكتبة: اجتهاد المنتج) |
| ربط الدرس بالقضية (`case_link`) والمهارات ببطاقات KO | KO refs | `ko_refs` بنمط `KO-…` | `tracks.ts`، `content/knowledge/ko_names.json` | ✔ |
| مسبار نقل بسطح ومجال جديدين بعد القضية | `LEARNING_TRANSFER_RESEARCH`، Forage (bench) | `ui.transfer` (`tr_flood`) و`scoreTransfer` | `c001…ui.json`، `assess.ts` | ◐ (مهمة واحدة؛ لا قضية خفية بعد 6–8 أسابيع) |
| قضية خفية كل 6–8 أسابيع وإعادة مواجهة متباعدة | P5 | — | — | ○ |
| مختبر مصغّر ينتج دليلاً يدخل اللوحة (توحيد الأزمنة) | SAFE_LABS-01، bench (Adapt P2) | `time_normalizer` مع `grants_evidence_on_converge` | `c001…ui.json`، `src/engine/ops.ts` (`runLab`)، `src/components/play/Time.tsx` | ✔ |
| تصنيف المصدر (أصلي/معروض/قول/قالب/وثيقة) قبل تثبيت البطاقة | `KO-RS-05-001` | `tag` و`source_tags` | `ops.ts`، `src/components/play/Evidence.tsx` | ✔ |
| لوحة أدلة مترابطة | `EVIDENCE_BOARD_UX_RESEARCH` | `Board.tsx` + روابط دعم/إضعاف | `src/components/play/Board.tsx` | ◐ (ليست «5 تبويبات» كما في المواصفة؛ لم أتحقق من تطابق الواجهة) |
| دفتر ملاحظات اللاعب | `CM-10-006` | `journal` | `src/components/play/Journal.tsx`، `ops.ts` (`addJournal`) | ✔ |
| 39 مهارة KO/جدول مهارات وتتبع تقدم المهارة | `12/reasoning_skills.jsonl` | `ui.skills` تربط المهارة بمسار فقط | `c001…ui.json` | ○ |

### 2.6 السلامة والعمر والخصوصية

| الرؤية | المصدر | الميزة | المسار | الحالة |
|---|---|---|---|---|
| لا خدمة لمن هم دون سن الاستهداف؛ لا تخزين لتاريخ الميلاد | FSR، `CHILD_AND_TEEN_PRIVACY` | بوابة ناعمة: 16–17 / 18+ / أقل من 16 (لا تخزين) | `src/components/AgeGate.tsx`، `src/app/api/age/route.ts` | ◐ (تُطبّق قرار 16+؛ المكتبة تتحدث عن 13–15 أيضاً: انظر GAP) |
| ملاءمة القضية للعمر (`age_band`) | `AGE_APPROPRIATE_CONTENT_POLICY` | `ageAllows` عند الاختيار | `src/server/content.ts` | ✔ |
| لا موت/ضحية عنف؛ `content_flags` | AG-01، X19 | `meta.content_flags` (`no_violence`…) وفحص X19 لحالات 13–15 | `src/engine/validate.ts` (السطر ≈285)، القضيتان | ✔ |
| موافقة ولي موثقة لمن دون 18 وجدول أعمار لكل دولة | `CHILD_AND_TEEN_PRIVACY` | `users.adult_confirmed` فقط | `migrations/001_init.sql` | ○ (معلّق على رأي قانوني) |
| بيانات دنيا؛ حذف الحساب | GDPR/PDPL مبادئ | `/api/auth/delete`، `deleted_at` | `src/app/api/auth/delete/route.ts` | ✔ |
| حد معدل، تدقيق، IP مجزّأ، كلمات مرور بـscrypt | `aijur-skills-platform-tools.md` | `ratelimit.ts`، `audit_log`، `ip_hash` | `src/server/{ratelimit,audit,auth}.ts` | ✔ |
| بلاغ سلامة/حقوق/خطأ من اللاعب | `CONTENT_AND_SAFETY_GOVERNANCE` P0/P1/P2 | `content_reports` + `/api/report` + `studio/reports` | `src/app/report/page.tsx`، `src/app/api/report/route.ts` | ✔ (دون SLA) |
| خروج الأزمات + خطوط مساعدة موثقة | `YOUTH_HELPLINE_REGISTER` | `safety_exit` سطر مؤلَّف فقط | `types.ts` | ○ (لم تُشحن أرقام؛ لا اتصال اختباري) |
| صفحة خصوصية | — | `src/app/privacy/page.tsx` | | ◐ (النص لم يراجعه محامٍ) |

### 2.7 المحتوى والأصول

| الرؤية | المصدر | الميزة | المسار | الحالة |
|---|---|---|---|---|
| قضية رأسية 16+ غير عنيفة، قصتها «تناقض ظاهري سببه توحيد الزمن» | `05_CASE_01.md` | `c001_last_observation` | `content/cases/c001*` | ◐ (مسودة بمساعدة الذكاء الاصطناعي، بلا مراجعة بشرية) |
| قضية تمهيد قصيرة | سلّم الأطوال (دليل يومي/جلسة) | `c000_lost_notebook` (12 د) | `content/cases/c000*` | ◐ |
| 9 قضايا Content v02 (02–09) | `athar_research/05_CASE_*` | — | — | ○ |
| 40 نمط قضية ARC | `case_archetypes.jsonl` | — | — | ○ |
| مولّد بذور تراثية | `HERITAGE_CASE_SEEDS` | — | — | ○ |
| صور (600 سجلاً) وصوت (165) وأيقونات (232) | `15/*_REGISTER.csv` | لا أصول مشحونة؛ الخطوط `@fontsource` فقط | `package.json` | ○ (الصور لم تُرَ أصلاً) |
| إسناد مولَّد من السجل لـCC BY | `SOUND_DESIGN_GUIDE` §6 | — | — | ○ |

### 2.8 وضع المعلم/المدرسة والقياس والمنافسة

| الرؤية | المصدر | الميزة | المسار | الحالة |
|---|---|---|---|---|
| أدوار: لاعب/محرر/مراجع/مدير | RBAC من AIJUR | `users.role` | `migrations/001_init.sql` | ✔ |
| وضع معلم/مدرسة: لوحة صف بلا ترتيب | `LA-07-019`، bench (خندق #5) | — | — | ○ |
| قياس الأثر (قبلي/بعدي + مجموعة ضابطة) | `EDUCATIONAL_VALIDATION_PLAN` | — | `progress.ts` يحفظ التقدم لا القياس البحثي | ○ (يتطلب لجنة أخلاقيات) |
| ملف لاعب | — | `src/app/profile`، `/api/profile` | | ✔ |
| أدوات صانع المحتوى (استوديو) | bench | `src/app/studio/page.tsx` + واجهات studio | | ◐ |

## 3. ما يظهر من الجرد

1. **المنفَّذ يغطي الطبقة التي تميّز المنتج**: سجل الفرضيات، الاستشهاد، الحدود، المعايرة، مختبر توحيد الأزمنة، تصنيف المصدر، حوار مقيد، بوابة مراجعة سباعية، فاحص تسرب.
2. **لا يوجد بعد**: «الأدلة غير كافية»، دفعات التأكيد، حساب إتقان المهارات، مصحح عربي، وضع المعلم، قضية خفية/إعادة مواجهة، قضايا 02–09، أصول، رأي قانوني، شريك أخلاقيات.
3. **اجتهادات المنتج دون سند صريح في المكتبة** (يلزم إقرار): المسارات A–F وأسماؤها، أوزان rubric السبعة، 16+ كحد أدنى للبوابة.
4. **لا اختبارات**: `tests/unit` و`tests/e2e` فارغان؛ الجودة الآن تعتمد على `scripts/check-cases.ts` و`check-tracks.ts` و`leak-scan.ts` (غير مشغّلة هنا).
