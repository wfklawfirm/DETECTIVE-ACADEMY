# تقرير الوكيل — المكتبة 03: السرد وتصميم الألعاب الاستنتاجية

- **التاريخ:** 2026-10-27
- **نطاق المعرّفات:** ATH-SRC-0200 … ATH-SRC-0268 (69 سجلاً مستخدماً من الكتلة 0200–0299)
- **رمز المكتبة لوحدات المعرفة:** 03

## 1. الأعداد

| البند | العدد | الهدف |
|---|---|---|
| سجلات مصادر متحقق منها في `sources.jsonl` | **69** (65 بحالة `verified`، و4 بحالة `needs_expert_review`) | 40–55 |
| — منها ألعاب | 25 | — |
| — مقابلات ومحاضرات وتقارير ما بعد الإطلاق للمطورين | 12 | — |
| — أوراق محكّمة (مجلات ومؤتمرات) وأطروحة | 16 | — |
| — كتب | 4 | — |
| — أخرى (مدونات خبراء، أدوات، قاعدة بيانات، تقارير، أخبار) | 12 | — |
| درجات الدليل | B: 16 · C: 39 · D: 14 | — |
| بطاقات تحليل معمقة (`cards/`) | **13** (بين 544 و859 كلمة) | 8–10 |
| وحدات معرفة: آليات قضايا (CM) | **39** | 30–40 |
| وحدات معرفة: أنماط سردية (NP) | **10** | 8–12 |
| آليات مقيّمة في مكتبة الأنماط | 39 (لكل منها 4 درجات) | ≥ 30 |
| صفوف مصفوفة المنافسين | 27 | جميع العناوين في الموجز |

**ملاحظة على تجاوز الأهداف:** لم يُضَف أي سجل للحشو. كل سجل إضافي يقدم معلومة تغيّر قراراً: حد النتائج الخمس في Her Story، ونقل Pope اللغز من سبب الموت إلى الهوية، ومنهج اختبار Golden Idol، ونتائج تجارب التلميحات والتحدي.

## 2. الملفات المنتجة

- `INTERACTIVE_MYSTERY_DESIGN_BIBLE.md`: تصنيف العناوين حسب الآلية، وإجابات الأسئلة الأربعة عشر، والمبادئ العشرة، وقائمة ما يجب تجنبه، والفجوات.
- `GAME_MECHANICS_PATTERN_LIBRARY.md`: 39 آلية بدرجات (تعلّم، وإثارة، وكلفة، وهاتف) وأمثلة ومخاطر، مع توصيات للنسخة الأولى.
- `EVIDENCE_BOARD_UX_RESEARCH.md`: مقارنة ملفات القضايا، وبديل الهاتف للوحة الخيوط (قالب الادعاء)، وبنية "الهاتف داخل الهاتف"، واختبار الفرضيات، والقياس.
- `HINT_AND_DIFFICULTY_SYSTEM.md`: جدول الأدلة، وسلّم خماسي، والتعافي من الأخطاء، ومنحنى الموسم، وقائمة العدالة بإحدى عشرة نقطة، ومؤشرات الإحباط، وخطة تجارب (H1–H5).
- `INTERACTIVE_STORY_COMPETITOR_MATRIX.csv`: 27 صفاً و16 عموداً كما في الموجز.
- `cards/`: ATH-SRC-0200، 0201، 0203، 0208، 0213، 0214، 0234، 0235، 0241، 0246، 0249، 0256، 0257.
- `_data/sources.jsonl` (69) · `_data/knowledge_objects.jsonl` (49) · `_data/agent_report.md`.

## 3. استراتيجية البحث

1. **العناوين:** بحث ويب قياسي لكل عنوان، ثم جلب صفحة ويكيبيديا (للبيانات الببليوغرافية فقط وفق البروتوكول) أو صفحة المتجر الرسمية (Steam وApp Store) للسعر واللغات والمنصات.
2. **أدب التصميم:** صفحات الناشرين (Routledge)، ومواقع المؤلفين (theoryoffun.com، وgrumpygamer.com، وemshort.blog، وscottnicholson.com)، وقوائم مراجع صفحات ويكيبيديا للوصول إلى مقابلات المطورين الأصلية ثم جلبها مباشرة.
3. **الأوراق المحكّمة:** التحقق الببليوغرافي عبر Crossref API، **وإعادة بناء الملخصات من OpenAlex (abstract_inverted_index)**. قُرئت الملخصات فقط لا النصوص الكاملة.
4. **التحقق من الادعاءات:** كل ادعاء في الوثائق موسوم ومربوط بمعرّف. ما لم يُقرأ مصدره موسوم [تفسير بحثي] أو `needs_expert_review`.

## 4. العوائق

- **نفدت ميزانية البحث على الويب (200 استعلام مشترك بين كل الوكلاء)** بعد نحو 30 استعلاماً من هذا الفريق، فتوقف البحث بمحركات البحث تماماً. واصلنا بالجلب المباشر لروابط ظهرت في نتائج سابقة أو في قوائم مراجع.
- **نفدت ميزانية الجلب بالساعة (800 مشتركة)** مرة واحدة لنحو 20 دقيقة.
- **مواقع رفضت الجلب:** gdcvault.com (robots)، وmitpress.mit.edu (robots)، وjesperjuul.net، وifcomp.org، وodr.chalmers.se، وlink.springer.com، وdl.acm.org، وdevelop-online.net (robots)، وpolygon.com وrockpapershotgun.com (محجوبة)، وscottkim.com (صفحة المقال)، وstore.steampowered.com/app/1626640 (صفحة تسجيل دخول).
- **جدران الدفع:** النصوص الكاملة لأوراق ACM وElsevier وSpringer وTaylor & Francis غير متاحة، فاقتصرنا على الملخصات.
- **ملخصات غير متاحة في OpenAlex:** Ryan وRigby وPrzybylski 2006 (PENS)، وJohnson وGardner وPerry 2018.

## 5. مرشحون غير متحقق منهم (لم يدخلوا الفهرس)

| المرشح | السبب |
|---|---|
| محاضرات GDC لـ Lucas Pope عن Obra Dinn | لا توجد في قوائم مراجع ويكيبيديا. GDC Vault يمنع الجلب. موقع Pope الرسمي يذكر نسخة عرض GDC 2016 فقط، لا محاضرة |
| محاضرة GDC لـ Sam Barlow عن Her Story | لم نجد محاضرة GDC موثقة. المرجع الأقرب خطاب Fantastic Arcade 2015 على Vimeo، ولم يُجلب |
| محاضرة GDC لـ Color Gray Games | لم يُعثر عليها قبل نفاد ميزانية البحث |
| Scott Kim — "What is a Puzzle?" وورشة GDC لتصميم الألغاز | صفحة المقال لم تُجلب، والصفحة الرئيسية لا تذكرها |
| Rock Paper Shotgun، "How a book binds the Return of the Obra Dinn" (2018) | الموقع محجوب عن الجلب |
| Alex Beachum، أطروحة USC (2013) | صفحة المكتبة الرقمية أعادت محتوى فارغاً |
| Mobius Digital، "Demaking Outer Wilds" | الجلب فشل |
| Csikszentmihalyi، *Flow* (1990) | البحث في Crossref أعاد فصولاً ومراجعات لا الكتاب نفسه، والمرجع العلمي للتدفق من اختصاص مكتبة 06 |
| بيانات تنزيل Duskwood وإيراداتها | صفحة الصحافة لم تعرض الجدول |
| Danganronpa، وTangle Tower بسجل مستقل، وThe Mermaid Mask | ذُكرت ضمن مصادر أخرى ولم تُفحص بسجل مستقل |
| مسابقات وتجارب القصص التفاعلية العربية | لم يُتح البحث بعد نفاد الميزانية. **فجوة مهمة** تُحال إلى مكتبتي 08 و09A |

## 6. أهم خمس نتائج يجب أن تغيّر تصميم ATHAR

1. **التلميحات ومقاييس الانخراط ليست محايدة.** في تجربة بنحو 50 ألف طالب، خفّضت أربعة تصاميم تلميحات الأداء مقارنة بغيابها [ATH-SRC-0256]. وفي تجربتين بنحو 80 ألف لاعب، أبقت النسخ الأسهل اللاعبين أطول لكنها علّمت أبطأ [ATH-SRC-0255]. ← نظام التلميحات ذراع تجريبي (بما فيه ذراع بلا تلميحات صريحة)، ولا يُحسَّن المنتج بمدة اللعب وحدها. (السياق ألعاب رياضيات، والتعميم يحتاج اختباراً.)
2. **المعادلة الرابحة في ألعاب الاستنتاج:** مشهد أو أرشيف مكثف + إجابة يبنيها المستخدم من فضاء مقيد + تحقق يجعل التخمين مكلفاً (دفعات أو مقاطع) [ATH-SRC-0200][ATH-SRC-0201][ATH-SRC-0226]. وهي في الوقت نفسه **أداة تقييم جاهزة**: "رواية الحدث" بالخانات مرتبطة بالمهارات.
3. **المنافسة على جودة الآلية قوية ورخيصة:** Golden Idol بجزأيها على الهاتف عبر Netflix [ATH-SRC-0201][ATH-SRC-0202]، وObra Dinn تدعم العربية نصاً على Steam [ATH-SRC-0200]. ← تميّز ATHAR يجب أن يكون: محتوى عربي أصيل مناسب للعمر، وقياس حقيقي للاستدلال، ومسار مدرسي (المعلم كمدير لعبة، كما يفعل 82% من غرف الهروب [ATH-SRC-0257]).
4. **الحرية مع حقيقة ثابتة، والأرشفة آلية، والحكم يُراجَع:** ألغت Paradise Killer الفرز اليدوي لعدم عمليته، ولا تؤكد الصواب [ATH-SRC-0227]. ← ملف هاتف بأرشفة وصفية آلية + "قالب ادعاء" بدل الخيوط + مراجعة ما بعد الحكم (فجوة لم يملأها أي منافس مدروس).
5. **القياس:** GEQ، الأوسع استخداماً، لم تصمد بنيته العاملية في دراسة تحقق على 633 مشاركاً، ولم يُنشر في منشور محكّم [ATH-SRC-0250]. وPXI متحقق منه في خمس دراسات [ATH-SRC-0251]. والتعلم المُدرَك يختلف عن الفعلي [ATH-SRC-0259]. ← قياس سلوكي من مخطط الاعتمادية + نبضة لحظية + بنود PXI بعد تحقق عربي، ولا GEQ، ولا ادعاءات تعليمية مبنية على الإدراك الذاتي.

## 7. أهم خمسة أسئلة مفتوحة وفجوات للمراجعة البشرية أو الخبيرة

1. **لا دليل على التعلم القابل للانتقال** من أي لعبة تحقيق تجارية في عيّنتنا. يحتاج تصميم تجربة قبلية وبعدية بمجموعة ضابطة (مكتبة 07).
2. **النصوص الكاملة** لدراسات O'Rourke 2014 وLomas 2013 وIacovides 2015 وJohnson 2018: أحجام الأثر، وأي تصاميم التلميح أقل ضرراً، وأثر الواجهة على المبتدئين. مطلوبة قبل أي استشهاد خارجي.
3. **العربية:** كلفة البحث الحر (تجذيع ولهجات)، وكيف تُصاغ خانات "رواية الحدث" دون أن تكشف علامات التأنيث والعدد الإجابة. يحتاج لغوياً ومهندس معالجة لغة عربية (مكتبة 10).
4. **التحقق العربي للمقاييس** (PXI وPENS) على مراهقين من 13 إلى 18 عاماً. يحتاج مختصاً في القياس النفسي.
5. **المعايرة:** حجم دفعة التحقق، وعتبات مؤشرات الإحباط، وتوقيت التلميحات، وحد الأدلة على الشاشة. كلها افتراضات تحتاج بيانات الإطلاق التجريبي، مع موافقة أولياء الأمور وإطار خصوصية (مكتبة 11).

## 8. تحفظات منهجية
- ويكيبيديا استُخدمت فقط للبيانات الببليوغرافية للألعاب والكتب، وللوصول إلى روابط المقابلات الأصلية. الآليات الموصوفة منها معلومات أولية عن الألعاب، لا ادعاءات علمية.
- درجات الآليات (1–5) وكل محتوى موسوم [افتراض تصميمي] تقديرات خبير تحتاج معايرة.
- أرقام المبيعات مأخوذة كما وردت في المصادر (غالباً تصريحات المطورين أو الناشرين)، وغير مدققة.

## Gap-fill round (2026-10-27)

A separate gap-fill agent ran after the first round's search quota was exhausted. It used official pages plus catalog APIs (OpenAlex, Crossref, PubMed, ERIC).

**New records (3):** ATH-SRC-0269–0271. Catalog now 72 records (69 → 72). `needs_expert_review`: 4 → 3.

| ID | Source | Verification |
|---|---|---|
| ATH-SRC-0269 | Sam Barlow, "Making 'Her Story' - Telling a Story Using The Player's Imagination", GDC 2016 (Game Narrative Summit) | GDC Vault official session page (read via fetch tool; direct fetch shows a maintenance page). Talk video not viewed. |
| ATH-SRC-0270 | "GDC Live Q&A: Lucas Pope and Return of the Obra Dinn" (2018) | Official GDC YouTube channel metadata only. This is a live Q&A, not a formal GDC talk. Content not reviewed (grade D). |
| ATH-SRC-0271 | Thinky Games interview with Andrejs and Ernests Kļaviņš (Dec 2024) | Fetched article. Developer testimony (grade D). |

**Changed records:**
- ATH-SRC-0258 (Nicholson 2018) → `verified`. The one-sentence abstract was read via OpenAlex, and its key findings and limitations were rewritten from it. Still a practitioner article.

**Deliverables edited:** `INTERACTIVE_MYSTERY_DESIGN_BIBLE.md`
- Gap 3 was rewritten.
- New Golden Idol complexity-ceiling bullet (0271).
- Barlow GDC talk added to the Her Story bullet (0269).

**Still unverified / open:**
- **No formal GDC talk by Lucas Pope or by Color Gray Games** was found on the GDC channel, in GDC Vault search results, or in web search. Two attempts each, then abandoned.
- **ATH-SRC-0249** (Johnson et al. 2018): abstract still unavailable. OpenAlex has none, and the QUT eprint returned 403.
- **ATH-SRC-0267** (Beachum talk): content is still not reviewed. The official channel metadata was reconfirmed.
- **ATH-SRC-0240** (Koster): years still null.
- Rock Paper Shotgun, the Beachum USC thesis and Scott Kim were not retried.
