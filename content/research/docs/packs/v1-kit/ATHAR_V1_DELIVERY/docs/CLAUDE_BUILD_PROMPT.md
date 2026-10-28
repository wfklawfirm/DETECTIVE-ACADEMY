# Claude — Implementation Prompt for ATHAR

أنت Principal Product Engineer + Interactive Narrative Architect + Learning Assessment Engineer. أمامك حزمة ATHAR_V1_DELIVERY تحتوي نموذجاً تفاعلياً يعمل محلياً ووثائق لتسع قضايا بحثية. اقرأ أولاً PRODUCT_BLUEPRINT.md وEDITORIAL_AND_SCIENCE_GATE.md ثم CASE_ENGINE_BLUEPRINT.md و05_CASE_01.md وprototype/index.html. لا تستنتج أن النموذج جاهز للنشر، ولا تُصلح مشكلة بتخليق دليل جديد.

## المهمة
حوّل النموذج المحلي إلى تطبيق ويب إنتاجي عربي RTL mobile-first يركز حصراً على قضية «الرصد الأخير» بوصفها vertical slice، مع بنية محتوى تقبل قضايا أخرى عبر ملفات بيانات، لا عبر نسخ واجهات. حافظ على التصميم التشويقي الاحترافي ودقة التقييم. ضع حدوداً واضحة بين محرك الحقيقة وقواعد واجهة اللعب والنص الحر.

## Architecture deliverables
1. TypeScript React أو Next.js مع تبرير الاختيار؛ مدخل قضايا مجدول بإصدارات، schema Zod للحقائق والأدلة والشخصيات والفرضيات والمهارات والمشاهد.
2. Components: CaseBrief, EvidenceViewer, SourceReliability, TimezoneLab, HypothesisBoard, FinalSubmission, AssessmentReport, TransferTask, TeacherReview (الأخير داخلي).
3. Simulated character dialogue optional/off by default؛ لا LLM بلا factual grounding وpermission filtering وguardrail tests.
4. Data layer: cases/001.json، assets مقتصرة على المواد الأصلية أو المرخصة، source provenance منفصل عن in-universe fictional document.
5. قواعد تقييم حتمية قابلة للتفسير، مع تدخل بشري لأي حكم على النص الحر. لا تصفها بمقياس نفسي معتمد.
6. Accessibility: keyboard navigation, aria-labels, readable contrast, mobile widths 320–1440, no media-only clues.
7. Tests: 20 unit tests for truth consistency and score, 10 UI flow tests, 12 LLM safety tests only if feature enabled.
8. Privacy-by-design: الحد الأدنى من البيانات، حساب ضيف، عدم جمع بيانات القاصرين دون إطار قانوني.
9. Telemetry schema with consent and anonymous cohorts; no invented user metrics.
10. Docs: developer setup, editor guide, content QA checklist, release checklist, known limitations.

## Acceptance tests
- يحل المستخدم القضية دون الحاجة إلى اختيار التبويب المسبق.
- كل توقيت يحوّل بطريقة صريحة ويحتفظ بتاريخه واليوم التالي.
- E1–E6 متطابقة مع مستند القضية؛ لا تظهر معلومة حاسمة خارج الملف.
- لا يساوي التقييم بين اختيار صحيح بالصدفة وحجة قابلة للتحقق.
- إجابة «لا يثبت التسريب» تقبل، لكن لا تؤدي إلى الجزم بنفي وجوده.
- لا تصدر ادعاءات فعالية تعليمية دون تحقق مستقل.
- أي صوت أو صورة أو مادة أصلها غير معروف لا تُدرج في build منشور.

ابدأ بمراجعة الملف الأصلي وأبلغني بالمشكلات التي اكتشفتها في المنطق والتقييم قبل كتابة الكود، ثم نفذ التطبيق والاختبارات وأعط قائمة ملفات قابلة للتشغيل وتعليمات التشغيل. لا تستبدل مهمة التنفيذ بتقرير نظري، ولا تدع اكتمالاً دون اختبارات.
