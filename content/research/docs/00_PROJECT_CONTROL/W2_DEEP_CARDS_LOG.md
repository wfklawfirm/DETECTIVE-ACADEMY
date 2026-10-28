# سجل بطاقات التحليل العميق للدفعة الثانية (W2 Deep Cards) — 2026-10-27

**المهمة:** كتابة بطاقات تحليل عميق (البروتوكول §7) لأهم مصادر الدفعة الثانية في القرارات، من ملفات الفرق المنتهية فقط. ثم تعيين حقل `deep_card` في السجلات، وتصحيح أي سجل يخالف محتوى مصدره.

**النتيجة:** **39 بطاقة**، كلها بين 515 و781 كلمة (عُدّت بـ`str.split`)، **و4 تصحيحات لسجلات** الكتالوج.

## 1. المنهج
- **الترتيب:** رُتّبت المصادر بسكربت Python يجمع ثلاثة عناصر:
  - درجة الدليل (A وB أولاً).
  - الصلة (high).
  - وزن «أثر القرار»: كلمات تتعلق بالموافقة والأهلية والبيانات الشخصية والعلامات والتراخيص والأمان والعربيزي واللهجات والتقييم والطلب والرموز وRTL والتراث الاستدلالي.
- **التوازن والاستبعاد:** ثم اختيار يدوي يوازن بين المكتبات، بحد أدنى 3 لكل ملف مؤهل، وبطاقة واحدة لملف الصور. واستُبعد كل سجل له `deep_card` (لم يكن أي منها كذلك).
- **قاعدة التحقق:** لم تُكتب أي بطاقة من السجل وحده. أُعيد فتح كل مصدر في هذه الجلسة:
  - نص رسمي (legiliban، USPTO TSDR، misa.gov.sa، ca3.uscourts.gov، ai.google.dev، support.google.com، unodc.org).
  - أو ملخص ونص كامل (ACL Anthology، PMC E-utilities، Frontiers، springeropen).
  - أو Crossref وOpenAlex للملخصات.
  - أو الملفات المحفوظة في `99_LEGAL_SOURCE_ASSETS/` لنصوص التراث والأدب الملك العام.
  - أو إعادة تشغيل واجهات Apple للبيانات.
  - User-Agent موحد: «ATHAR-Research-Library/2.0 (non-commercial research)».
- **استبدالان أثناء العمل:** اختيرت ATH-SRC-1925 و1926 أولاً، ثم تبيّن أنهما تكرار بـDOI للسجلين 0256 و0255 في الدفعة الأولى، ولهما بطاقة مدمجة (`03/cards/ATH-SRC-0256.md`). فاستُبدل بهما **1940** (Cowan) و**1924** (W3C ALReq)، وكلاهما تحقق منه.
- **ما لم يُقرأ كاملاً:** 1370 و1371 و1375 و1940 و1942 قُرئت بالملخص أو بالصفحة الأولى فقط (مدفوعة). وذُكر ذلك صراحة في كل بطاقة. ونص 1636 العربي مرمَّز بخط غير قابل للاستخراج، فاعتُمد الملخص الإنجليزي.
- **تعديل السجلات:** أعيدت كتابة الملفات الـ7 بـPython مع الحفاظ على ترتيب الأسطر والمفاتيح. ونسخ احتياطية في مجلد scratchpad. ثم التحقق: 401 سجلاً، و39 حقلاً `deep_card` كلها تشير إلى ملفات موجودة، ولا تغيير في أي سطر آخر (diff = 39 سطراً).

## 2. البطاقات (source_id ← المسار ← سبب الاختيار)

### 11_RIGHTS_PRIVACY_AND_SAFETY/_data/sources_w2.jsonl (W2-LEGAL) — 10
| source_id | البطاقة | سبب الاختيار |
|---|---|---|
| ATH-SRC-1801 | 11_RIGHTS_PRIVACY_AND_SAFETY/cards/ATH-SRC-1801.md | القانون اللبناني 81/2018 (A): يحسم مسار الامتثال في لبنان (تصريح أو إعفاء، والحبس عقوبةً) |
| ATH-SRC-1800 | 11_RIGHTS_PRIVACY_AND_SAFETY/cards/ATH-SRC-1800.md | قانون قطر 13/2016 (A): بيانات الأطفال «ذات طبيعة خاصة» تحتاج تصريحاً، وغرامة 5 ملايين، وشرط م17 للألعاب |
| ATH-SRC-1804 | 11_RIGHTS_PRIVACY_AND_SAFETY/cards/ATH-SRC-1804.md | لائحة مصر 816/2025: أساس حكم «حوار الذكاء الاصطناعي محجوب في مصر» (C3). درجة D، لكنه أعلى أثراً في قرار الإطلاق |
| ATH-SRC-1808 | 11_RIGHTS_PRIVACY_AND_SAFETY/cards/ATH-SRC-1808.md | المعاملات المدنية السعودية (A): رشد 18 **هجرية**، أي حد موافقة الولي (C2) |
| ATH-SRC-1833 | 11_RIGHTS_PRIVACY_AND_SAFETY/cards/ATH-SRC-1833.md | علامات تركة كونان دويل في USPTO (A): يمنع «فكّر مثل شرلوك» تسويقياً (C4) |
| ATH-SRC-1841 | 11_RIGHTS_PRIVACY_AND_SAFETY/cards/ATH-SRC-1841.md | Thomson Reuters ضد ROSS، الاستئناف (A): أول حكم استئنافي في تدريب الذكاء الاصطناعي (C5) |
| ATH-SRC-1836 | 11_RIGHTS_PRIVACY_AND_SAFETY/cards/ATH-SRC-1836.md | شروط Gemma (A): تحدد اختيار النموذج والتزامات التوزيع المستضاف |
| ATH-SRC-1847 | 11_RIGHTS_PRIVACY_AND_SAFETY/cards/ATH-SRC-1847.md | تصنيفات Google Play/IARC (C): «تصوير الجريمة» يعني 16+، ورفض التصنيف يحذف التطبيق إقليمياً. يحدد قواعد الكتابة |
| ATH-SRC-1820 | 05_INVESTIGATIVE_REASONING/cards/ATH-SRC-1820.md | الإجراءات الجزائية اللبنانية (A، المكتبة 05): واقعية الأدوار، وبطلان الإكراه، وشهادة القاصر |
| ATH-SRC-1829 | 05_INVESTIGATIVE_REASONING/cards/ATH-SRC-1829.md | قانون UNODC/UNICEF النموذجي (A، المكتبة 05): قاعدة «لا يقابل اللاعب طفلاً شاهداً» |

### 02_DETECTIVE_LITERATURE/_data/sources_w2_heritage.jsonl (W2-HERITAGE) — 5
| source_id | البطاقة | سبب الاختيار |
|---|---|---|
| ATH-SRC-1201 | 02_DETECTIVE_LITERATURE/cards/ATH-SRC-1201.md | الطرق الحكمية (A): الأساس المذهبي لـ«الأمارات» و«تفريق الشهود»، ونقد القيافة |
| ATH-SRC-1200 | 02_DETECTIVE_LITERATURE/cards/ATH-SRC-1200.md | أخبار الأذكياء (A): المنبع الرئيسي لقضايا التراث القصيرة (السكة، والشجرة، والخروع، والبعير) |
| ATH-SRC-1205 | 02_DETECTIVE_LITERATURE/cards/ATH-SRC-1205.md | كليلة ودمنة، باب الفحص (A): قالب «حلقة المحاكمة» ونقد الفراسة |
| ATH-SRC-1202 | 02_DETECTIVE_LITERATURE/cards/ATH-SRC-1202.md | أخبار القضاة (A): أقدم طبقة لقصص إياس، وتمرين نقد المصادر |
| ATH-SRC-1228 | 02_DETECTIVE_LITERATURE/cards/ATH-SRC-1228.md | مارزولف عن حنا دياب (B): بطاقة أصل HS-061 «علي خواجه» (C7) |

### 02_DETECTIVE_LITERATURE/_data/sources_w2_worldlit.jsonl (W2-WORLDLIT) — 6
| source_id | البطاقة | سبب الاختيار |
|---|---|---|
| ATH-SRC-1329 | 02_DETECTIVE_LITERATURE/cards/ATH-SRC-1329.md | زديج، الفصل 3 (A، ملك عام): قضية الافتتاح للفئة 13–15، وجسر مع حكاية نزار |
| ATH-SRC-1338 | 02_DETECTIVE_LITERATURE/cards/ATH-SRC-1338.md | 棠陰比事 (A): منهج حالات قديم لتدريب القضاة، ومقدمة «الاعتراف الخاطئ» |
| ATH-SRC-1340 | 02_DETECTIVE_LITERATURE/cards/ATH-SRC-1340.md | 狄公案 (A): مبدأ «حقق ولا تعذّب» من خارج التراث الغربي، وآلية التنكر |
| ATH-SRC-1370 | 02_DETECTIVE_LITERATURE/cards/ATH-SRC-1370.md | Mystery Appeal (B): عدم اليقين والفضول ونوع الحل، فالحلول متدرجة |
| ATH-SRC-1371 | 02_DETECTIVE_LITERATURE/cards/ATH-SRC-1371.md | Murder for Pleasure (B): التعقيد المتوسط افتراضياً |
| ATH-SRC-1375 | 02_DETECTIVE_LITERATURE/cards/ATH-SRC-1375.md | Iskander 1993 (B): الدراسة المحكّمة الوحيدة المقارنة للقيم في الأدب البوليسي العربي والأمريكي لليافعين |

### 07_LEARNING_SCIENCE/_data/sources_w2.jsonl (W2-LEARN-AI) — 6
| source_id | البطاقة | سبب الاختيار |
|---|---|---|
| ATH-SRC-1608 | 07_LEARNING_SCIENCE/cards/ATH-SRC-1608.md | كسر الحماية بالعربيزي (B): أساس «العربيزي تتجاوز الحماية» (C9) |
| ATH-SRC-1602 | 07_LEARNING_SCIENCE/cards/ATH-SRC-1602.md | الرفض الانتقائي (B): مقياسا H وB، والحراس ليسوا ترقية موحدة |
| ATH-SRC-1618 | 07_LEARNING_SCIENCE/cards/ATH-SRC-1618.md | AraSafe (B): المعيار العربي الطبيعي، وأداء النماذج قريب من التخمين |
| ATH-SRC-1604 | 07_LEARNING_SCIENCE/cards/ATH-SRC-1604.md | انحياز ضد الصعيدية (B): اختبار إنصاف باللهجات الفرعية |
| ATH-SRC-1628 | 07_LEARNING_SCIENCE/cards/ATH-SRC-1628.md | تصحيح عابر للموجّهات (B): مسار المصحّح الصغير وبوابة الصلة |
| ATH-SRC-1636 | 07_LEARNING_SCIENCE/cards/ATH-SRC-1636.md | مفتاح واطسون-جليسر المصري (B): لا محك عربي قديم بلا فحص (C9) |

### 08_ARAB_AUDIENCE_AND_CULTURE/_data/sources_w2.jsonl (W2-AUDIENCE) — 6
| source_id | البطاقة | سبب الاختيار |
|---|---|---|
| ATH-SRC-1554 | 08_ARAB_AUDIENCE_AND_CULTURE/cards/ATH-SRC-1554.md | المسح المدرسي السعودي (B): أنواع الألعاب لدى 13–18، فالتموضع «مغامرة» لا «ألغاز» (C6) |
| ATH-SRC-1503 | 08_ARAB_AUDIENCE_AND_CULTURE/cards/ATH-SRC-1503.md | إنترنت السعودية 2024 (A): المنصات والقنوات للفئة 10–19 |
| ATH-SRC-1551 | 08_ARAB_AUDIENCE_AND_CULTURE/cards/ATH-SRC-1551.md | قوائم Apple Podcasts: أقوى إشارة طلب سردي (C6) |
| ATH-SRC-1500 | 08_ARAB_AUDIENCE_AND_CULTURE/cards/ATH-SRC-1500.md | لقطة App Store: «الطلب على ألعاب الغموض العربية ضعيف» (C6) |
| ATH-SRC-1524 | 08_ARAB_AUDIENCE_AND_CULTURE/cards/ATH-SRC-1524.md | BAREC (B): أهداف مقروئية رقمية لكل فئة عمرية |
| ATH-SRC-1526 | 08_ARAB_AUDIENCE_AND_CULTURE/cards/ATH-SRC-1526.md | مراجعة الازدواجية (B): الفصحى ليست عائقاً قرائياً بعد 13، والتشكيل الانتقائي |

### 10_TECHNICAL_ARCHITECTURE/_data/sources_w2.jsonl (W2-DESIGN-TECH) — 5
| source_id | البطاقة | سبب الاختيار |
|---|---|---|
| ATH-SRC-1914 | 10_TECHNICAL_ARCHITECTURE/cards/ATH-SRC-1914.md | Ahia 2023 (B): الإطار الأصلي لكلفة الرموز، وتحديثه بقياس 2026 (C1) |
| ATH-SRC-1922 | 10_TECHNICAL_ARCHITECTURE/cards/ATH-SRC-1922.md | UAX #9 (A): الأساس المعياري لقاعدة `<bdi>` والعزل (C10) |
| ATH-SRC-1924 | 10_TECHNICAL_ARCHITECTURE/cards/ATH-SRC-1924.md | W3C ALReq (B): الأرقام، وأشكال العرض، وU+FEFF، والمُطبِّع قبل ink |
| ATH-SRC-1940 | 03_NARRATIVE_AND_GAME_DESIGN/cards/ATH-SRC-1940.md | Cowan 2001 (A، المكتبة 03): سقف 3–4 عناصر في شاشة الحجة |
| ATH-SRC-1942 | 03_NARRATIVE_AND_GAME_DESIGN/cards/ATH-SRC-1942.md | Delgado 2018 (A، المكتبة 03): لا مؤقتات على قراءة الأدلة |

### 15_STORY_MEDIA_AND_ASSETS/_data/sources_w2_images.jsonl (W2-IMAGES) — 1
| source_id | البطاقة | سبب الاختيار |
|---|---|---|
| ATH-SRC-1401 | 15_STORY_MEDIA_AND_ASSETS/cards/ATH-SRC-1401.md | مجموعة ماتسون (A): أكبر أصل بصري مخزَّن (78 صورة) وبيان حقوقه يحتاج تفسيراً للأسواق العربية |

**التوزيع حسب مجلد البطاقة:** 11 = 8، و05 = 2، و02 = 11، و07 = 6، و08 = 6، و10 = 3، و03 = 2، و15 = 1.

## 3. سجلات خالفت محتوى مصدرها (صُحّحت)
| source_id | ما كان في السجل | ما وجدناه في المصدر | الإصلاح |
|---|---|---|---|
| ATH-SRC-1338 | «تعليقات Wu Na تقارن **كل قضية** بمواد قانون مينغ» | عبارة «謹按《大明律》» تظهر 5 مرات فقط، تحت القضايا الخمس الأولى. وملاحظة الفهرس تقول «首五條，辯析律意» | `key_findings[1]` أعيدت صياغته، وأُضيف قيد في `limitations` |
| ATH-SRC-1401 | «**43** صورة موسومة rights_review:post1930» | `IMAGE_ASSET_REGISTER.csv` فيه **42**، و`VISUAL_REFERENCE_GUIDE.md` يقول 42 | `limitations[2]` صُحّح إلى 42 |
| ATH-SRC-1526 | النتيجة عن التشكيل منسوبة إلى «دراسة» مبهمة، و«لا بيانات مراهقين» | الدراسة هي Abu-Liel وزملاؤه 2021، على **77 طالباً في الصف الثامن (13–15 سنة)** | `key_findings[1]` و`limitations[0]` |
| ATH-SRC-1618 | «ترخيص البيانات يحتاج تأكيداً» | بيان الأخلاقيات في الورقة: البيانات متاحة **للاستعمال الأكاديمي غير التجاري**. والعينة: 84% فصحى، و⅔ من مصر | `limitations[0]` و`commercial_reuse_permission`: not_established ← **no** |

كل تصحيح موسوم داخل النص بـ«[Corrected/Clarified 2026-10-27 by deep-card review]». لم نجد هذه العبارات الخاطئة مكررة في ملفات التركيب، فلا حاجة لبند جديد في `WAVE2_CORRECTIONS_TO_PROPAGATE.md`.

## 4. ملاحظات تحقق لا تستدعي تعديل السجل
- **ATH-SRC-1551:** أُعيد تشغيل التغذية في 27/10. المراكز الأولى ثابتة («سوالف طريق» الأول في السعودية والإمارات والكويت، والثاني في الأردن). والمراكز الأدنى تحركت: المغرب 53 بدل 41، و«قصص من المحاكم» 17 بدل 15 في السعودية. وعدد العناوين العربية في الإمارات 30 بدل 36. هذا تغير يومي لا خطأ. ذُكر في البطاقة.
- **ATH-SRC-1500:** حقل اللغات في Apple غير موثوق: «لغز الجريمة» مسجل «JA» فقط. فعدّ «دعم العربية» من الحقل يقلل التقدير. ذُكر في البطاقة.
- **ATH-SRC-1228:** الملاحظة 14 في المقال تقول إن غالان «لم ينشر» حكاية علي خواجه، لكن طبعة لانغ (عن غالان) [ATH-SRC-1214] تتضمنها مع مشهد تجار الزيتون الخبراء. فالسجل محق في وصف المقال بأنه متناقض.
- **ATH-SRC-1205:** في ملف OpenITI تتكرر فقرة الشهادة الختامية مرتين (ص 174–175). وفي هذه النسخة النمر الذي سمع العتاب هو نفسه «صاحب القضاء». ذُكر الأمران في البطاقة.
- **ATH-SRC-1833:** صفحات TSDR تُظهر «Notice of Suit» بتاريخ 8/7/2026 على SHERLOCK HOLMES (6821237) وDR WATSON (7757723). موضوع الدعوى غير معروف. ذُكر في البطاقة سؤالاً مفتوحاً.
- **ATH-SRC-1503:** نسبة استعمال الذكاء الاصطناعي حسب الجنس: الإناث 27.7% والذكور 17%، مقروءة من أيقونات الرسم في ص 15. أُضيفت إلى البطاقة، ولا يذكرها السجل.

## 5. ما لم يُلمس
- `07_LEARNING_SCIENCE/_data/sources_w2_pilot.jsonl` وملفات الفرق غير المنتهية (FORENSIC-AR، وMEDIA-COMP، وBUSINESS، وGULF-IMAGES، وAUDIO) لم تُقرأ للكتابة ولم تُعدَّل.
- لم يُعدَّل `01_SOURCE_CATALOG/sources_master.jsonl`. تُنقل حقول `deep_card` والتصحيحات إليه في خطوة الدمج التالية (`00_PROJECT_CONTROL/tools/merge_catalog.py`).

---

# الدفعة الثانية من البطاقات — 2026-10-27

**المهمة:** بطاقات تحليل عميق (البروتوكول §7) لأهم مصادر الفرق التي انتهت لاحقاً:
- W2-FORENSIC-AR.
- W2-MEDIA-COMP (الإعلام والمنافسون).
- W2-BUSINESS.
- W2-PILOT-ETHICS.
- W2-NAMING.
- W2-AUDIO (بطاقة واحدة).

ملف `15/_data/sources_w2_images_gulf.jsonl` لم يُلمس، لأن الفريق ما زال يعمل.

**النتيجة:** **32 بطاقة**، طولها بين 548 و788 كلمة (عُدّت بـ`str.split`)، **و11 تصحيحاً لسجلات** الكتالوج. وأُضيف بند C19 إلى `WAVE2_CORRECTIONS_TO_PROPAGATE.md`.

## 1. المنهج
- **الترتيب:** سكربت Python (`scratchpad/cards2/rank.py`) يجمع درجة الدليل والصلة وكلمات «أثر القرار» لكل ملف:
  - المسرد والمؤسسات العربية وأخلاقيات مختبرات التحيز.
  - الموافقة والأذونات للتجارب.
  - الأسعار واقتصاديات الوحدة والتمويل.
  - تعارض الاسم.
  - الصيغ الإعلامية والمنافسون.
- **التوازن:** اختيار يدوي، بحد أدنى 3 لكل ملف مؤهل، وبطاقة واحدة لملف الصوت. ولم يكن لأي سجل مختار `deep_card` من قبل، ولا تكرار بـDOI أو بالعنوان في الكتالوج (فُحص بالسكربت).
- **قاعدة التحقق:** لم تُكتب أي بطاقة من السجل وحده. أُعيد فتح كل مصدر في هذه الجلسة بأحد الطرق التالية:
  - **نصوص رسمية كاملة:**
    - ملفات PDF: مسرد UNODC العربي، وSRCD 2021، ولائحة NCBE السعودية، وBERA 2024، وسياسة RAK DOK، وقانون العلامات الإماراتي، وأطروحة UCLan.
    - صفحات: نايف، وNeLC، وTAQADAM، وBreakout EDU، وMAGNiTT، وRevenueCat.
  - **eCFR API:** نص 45 CFR 46.
  - **واجهة بحث المعجم الطبي الموحد:** 10 مصطلحات.
  - **PubMed وPMC وOpenAlex وCrossref:** للملخصات والنصوص المفتوحة.
  - **إعادة تشغيل واجهات المتاجر:** iTunes Lookup في 8 متاجر للعبة Siraaj، وصفحات Google Play وApp Store، وSteam، وأسعار IAP.
  - **إعادة جلب:** تغذيات RSS وقوائم Apple Podcasts (السعودية والكويت)، وصفحات Netflix (السعودية والولايات المتحدة) وBBFC، وواجهة USPTO tmsearch.
  - User-Agent موحد: «ATHAR-Research-Library/2.0 (non-commercial research)».
- **استبدال واحد:** اختيرت ATH-SRC-2023 («القصة الكاملة»، أخبار اليوم) أولاً. لكن الموقع يعيد تحدي Cloudflare لـcurl، ويفشل WebFetch معه. فاستُبدل بها **ATH-SRC-2010** (كونان)، وتحققنا منه.
- **ما لم يُقرأ كاملاً**، وذُكر ذلك صراحة في كل بطاقة:
  - 1746 و2432: الملخص فقط، لأنهما مدفوعان.
  - 2239: الملخص العام لتقرير مدفوع.
  - 2219: صفحة الويب، لا ملف PDF.
  - 2148: نص الإشعار كاملاً، والمقال الأصلي بملخصه فقط.
  - 2061 و2083 و2066: صفحات المتاجر فقط، لم نلعبها.
- **تعديل السجلات:**
  - أُعيدت كتابة 7 ملفات JSONL بـPython، مع الحفاظ على ترتيب الأسطر والمفاتيح. والملفات كانت تتطابق بايتاً بايتاً مع `json.dumps(ensure_ascii=False)` قبل التعديل.
  - نسخ احتياطية في `scratchpad/cards2/backup/`.
  - التحقق: 326 سجلاً، و32 حقلاً `deep_card` كلها تشير إلى ملفات موجودة. وتغيّر 32 سطراً فقط، كلها في الحقول المسموح بها. ولا تغيير في ترتيب المفاتيح، ولا قيم خارج القوائم المسموح بها.

## 2. البطاقات (source_id ← المسار ← سبب الاختيار)

### 04_FORENSIC_SCIENCE/_data/sources_w2.jsonl (W2-FORENSIC-AR) — 7
| source_id | البطاقة | سبب الاختيار |
|---|---|---|
| ATH-SRC-1701 | 04_FORENSIC_SCIENCE/cards/ATH-SRC-1701.md | المعجم الطبي الموحد (A): أساس «نسبة الترجيح» مقابل «نسبة الأرجحية» (C13) |
| ATH-SRC-1700 | 04_FORENSIC_SCIENCE/cards/ATH-SRC-1700.md | مسرد UNODC العربي (A): المرجع الرسمي لمصطلحات الجودة والاختبار و«لم تُكتشف ≠ سلبي» |
| ATH-SRC-1739 | 04_FORENSIC_SCIENCE/cards/ATH-SRC-1739.md | SRCD 2021 (A): اعتراض القاصر ملزم، والإيضاح يُعلن مسبقاً، ولا خداع مع ضيق متوقع (C14) |
| ATH-SRC-1746 | 04_FORENSIC_SCIENCE/cards/ATH-SRC-1746.md | Miketta وFriese 2019 (B): الإيضاح لا يمحو أثر تهديد الذات، فيُحظر أي تقييم كاذب للذات |
| ATH-SRC-1754 | 04_FORENSIC_SCIENCE/cards/ATH-SRC-1754.md | Somerville 2013 (B): حساسية المراهق للتقييم الاجتماعي، فلا لوحات صدارة لمختبرات التحيز |
| ATH-SRC-1706 | 04_FORENSIC_SCIENCE/cards/ATH-SRC-1706.md | الجمعية العربية لعلوم الأدلة الجنائية (C): خريطة المراجعين العرب ومجموعات العمل الست |
| ATH-SRC-1736 | 04_FORENSIC_SCIENCE/cards/ATH-SRC-1736.md | أطروحة الخط العربي (B): الصنفي مقابل الفردي، 94% للإقليم و71% للبلد، مع خطر التنميط |

### 07_LEARNING_SCIENCE/_data/sources_w2_pilot.jsonl (W2-PILOT-ETHICS) — 6
| source_id | البطاقة | سبب الاختيار |
|---|---|---|
| ATH-SRC-2111 | 07_LEARNING_SCIENCE/cards/ATH-SRC-2111.md | لائحة NCBE السعودية (A): القاصر <18، والمراجعة المعجّلة، واعتماد الإعلانات (C17) |
| ATH-SRC-2107 | 07_LEARNING_SCIENCE/cards/ATH-SRC-2107.md | 45 CFR 46 (A): اختبار «هل هو بحث؟»، والقبول الإيجابي، وإعفاءات الأطفال |
| ATH-SRC-2103 | 07_LEARNING_SCIENCE/cards/ATH-SRC-2103.md | BERA 2024 (A): حارس البوابة، وإفصاح الرعاية التجارية، وحدود السرية |
| ATH-SRC-2116 | 07_LEARNING_SCIENCE/cards/ATH-SRC-2116.md | RAK DOK (A): الوثيقة الإماراتية الوحيدة المنشورة لدخول الباحثين إلى المدارس الخاصة |
| ATH-SRC-2127 | 07_LEARNING_SCIENCE/cards/ATH-SRC-2127.md | Nakkash 2014 (B): موافقة 19.5% من الأهل في الدوحة، أساس حساب حجم العينة |
| ATH-SRC-2148 | 07_LEARNING_SCIENCE/cards/ATH-SRC-2148.md | إشعار PNAS/فيسبوك (B): لماذا تفشل حجة «اختبار منتج» عند النشر |

### 09_COMPETITIVE_INTELLIGENCE/_data/sources_w2_business.jsonl (W2-BUSINESS) — 6
| source_id | البطاقة | سبب الاختيار |
|---|---|---|
| ATH-SRC-2219 | 09_COMPETITIVE_INTELLIGENCE/cards/ATH-SRC-2219.md | RevenueCat 2026 (C): تحويل 2% وقيمة 22.82$ ومعايير الشرق الأوسط، أي مدخلات اقتصاديات الوحدة (C12) |
| ATH-SRC-2200 | 09_COMPETITIVE_INTELLIGENCE/cards/ATH-SRC-2200.md | لقطة أسعار App Store (C): نطاق 21–40 ريالاً، وفتح Golden Idol بـ20.99 |
| ATH-SRC-2233 | 09_COMPETITIVE_INTELLIGENCE/cards/ATH-SRC-2233.md | قواعد NeLC (A): ترخيص مسبق إذا مُنحت شهادات، فلا شهادات في الإصدار السعودي الأول |
| ATH-SRC-2214 | 09_COMPETITIVE_INTELLIGENCE/cards/ATH-SRC-2214.md | Breakout EDU (C): ترخيص صف بـ99$ ومدرسة بـ1,499$، الحد الأدنى للمسار المدرسي |
| ATH-SRC-2248 | 09_COMPETITIVE_INTELLIGENCE/cards/ATH-SRC-2248.md | TAQADAM (C): أنسب تمويل غير مخفف، والتقديم في أبريل، وشرط المنتج الأولي والتوسع السعودي |
| ATH-SRC-2239 | 09_COMPETITIVE_INTELLIGENCE/cards/ATH-SRC-2239.md | MAGNiTT H1 2026 (C): أدنى عدد صفقات في 5 سنوات، والمستثمر الإقليمي هو الجمهور |

### 15_STORY_MEDIA_AND_ASSETS/_data/sources_w2_media.jsonl (W2-MEDIA-COMP، إعلام) — 4
| source_id | البطاقة | سبب الاختيار |
|---|---|---|
| ATH-SRC-2031 | 15_STORY_MEDIA_AND_ASSETS/cards/ATH-SRC-2031.md | «جناية» (C): الثاني في السعودية، وحلقات «لعبة جناية»، ولعبة ورقية للأسرة 12+ (C16) |
| ATH-SRC-2046 | 15_STORY_MEDIA_AND_ASSETS/cards/ATH-SRC-2046.md | «سوالف طريق» على يوتيوب (C): 3.85 مليون مشترك، والصوت أولاً مع نشر متزامن |
| ATH-SRC-2004 | 15_STORY_MEDIA_AND_ASSETS/cards/ATH-SRC-2004.md | Wednesday (C): 18+ في السعودية مقابل TV-14، فالإطار مقبول والقوطية لا |
| ATH-SRC-2010 | 15_STORY_MEDIA_AND_ASSETS/cards/ATH-SRC-2010.md | كونان (C): قضية في 25 دقيقة، وBBFC 12A بعد حذف، والتحرير يحدد التصنيف (بديل 2023) |

### 09_COMPETITIVE_INTELLIGENCE/_data/sources_w2.jsonl (W2-MEDIA-COMP، منافسون) — 4
| source_id | البطاقة | سبب الاختيار |
|---|---|---|
| ATH-SRC-2061 | 09_COMPETITIVE_INTELLIGENCE/cards/ATH-SRC-2061.md | Case Mind (C): التهديد رقم 1، والمعمارية نفسها بالعربية على أندرويد (C15) |
| ATH-SRC-2083 | 09_COMPETITIVE_INTELLIGENCE/cards/ATH-SRC-2083.md | ColdTrace على Play (C): 1M+ تنزيل، فأندرويد يدخل الإصدار الأول |
| ATH-SRC-2066 | 09_COMPETITIVE_INTELLIGENCE/cards/ATH-SRC-2066.md | Inquest (C): محلّل العدالة ورهان الثقة صارا سلعة، والتميز في القياس المنشور |
| ATH-SRC-2074 | 09_COMPETITIVE_INTELLIGENCE/cards/ATH-SRC-2074.md | Bad News بالعربية (C): يصحح 1136، وATHAR ليس الأول في التحصين المسبق (C15) |

### 11_RIGHTS_PRIVACY_AND_SAFETY/_data/sources_w2_naming.jsonl (W2-NAMING) — 4
| source_id | البطاقة | سبب الاختيار |
|---|---|---|
| ATH-SRC-2504 | 11_RIGHTS_PRIVACY_AND_SAFETY/cards/ATH-SRC-2504.md | لعبة «Athar: Echoes of Time» (C): أقرب تعارض فعلي، وموجودة في المتجر السعودي أيضاً (C18) |
| ATH-SRC-2500 | 11_RIGHTS_PRIVACY_AND_SAFETY/cards/ATH-SRC-2500.md | منصة «أثر» لشرطة دبي (D): خطر الإيحاء بارتباط حكومي في الإمارات |
| ATH-SRC-2512 | 11_RIGHTS_PRIVACY_AND_SAFETY/cards/ATH-SRC-2512.md | قانون العلامات الإماراتي (A): المواد 3/1 و3/3 و3/5 و3/11، والحماية من تاريخ الطلب |
| ATH-SRC-2507 | 11_RIGHTS_PRIVACY_AND_SAFETY/cards/ATH-SRC-2507.md | USPTO (A): لا ATHAR حية للبرمجيات والألعاب، وعلامتان قريبتان في الفئة 41 |

### 15_STORY_MEDIA_AND_ASSETS/_data/sources_w2_audio.jsonl (W2-AUDIO) — 1
| source_id | البطاقة | سبب الاختيار |
|---|---|---|
| ATH-SRC-2432 | 15_STORY_MEDIA_AND_ASSETS/cards/ATH-SRC-2432.md | التحليل التلوي للموسيقى الخلفية (B): قاعدة «قبل لا أثناء» تجمعه مع 2430 و2431 |

**التوزيع حسب مجلد البطاقة:** 04 = 7، و07 = 6، و09 = 14، و15 = 5، و11 = 4.

## 3. سجلات خالفت محتوى مصدرها (صُحّحت)
| source_id | ما كان في السجل | ما وجدناه في المصدر | الإصلاح |
|---|---|---|---|
| ATH-SRC-1701 | autopsy = «الصفة التشريحية» مدخلاً | لا مدخل مستقل لـautopsy. المقابلات الثلاثة من مداخل «autopsy data» | `key_findings[1]` |
| ATH-SRC-2111 | (أ) ترجمة «موسومة Draft of Translation». (ب) م10.20 تخص «ذوي الاحتياجات الخاصة» | (أ) لا وسم «Draft» في الملف المنزّل، لا في النص ولا في صور الصفحات. (ب) النص «الفئات المستضعفة»، ويشمل تعريفها القاصرين، فتعديلات المقابلات مع المراهقين تعود إلى اللجنة كاملة | `key_findings[2]`، `limitations[1]` |
| ATH-SRC-2116 | مشاركة النتائج قبل النشر (كأنها شرط) | النص «يُشجَّع»، وللدائرة حق منع النشر، وشرط «التصاريح الأمنية». وذيل الوثيقة يصفها بأنها سرية لا تُنسخ | `key_findings[2]`، و`limitations` (+1)، و`internal_storage_permission`: not_established ← **no** |
| ATH-SRC-2148 | قُرئ عبر Retraction Watch لأن صفحة PNAS «محجوبة» | نص الإشعار كاملاً في PMC. وPubMed يربطه بـDOI آخر هو «تصحيح» في Crossref، وDOI السجل صحيح | `limitations[0]`، `verification_method` ← fetched_official_page، `verification_url` ← PMC |
| ATH-SRC-2200 | فتح Golden Idol على الهاتف «أرخص بنحو 3 أضعاف» من Steam | 39.99 ÷ 20.99 = 1.9، أي نحو النصف. وملف التركيب يقول «نحو نصف» بشكل صحيح | `key_findings[0]` |
| ATH-SRC-2010 | Netflix السعودية 16+ (كأنه متاح) | الصفحة تقول «غير متاح حالياً للمشاهدة في بلدك»، والـ12A في BBFC جاء بعد حذف بطلب الموزع (والنسخة الكاملة 15) | `key_findings[0]`، `key_findings[2]` |
| ATH-SRC-2031 | الحلقات العادية «قضايا متخيلة قابلة للحل» | التغذية تقدّم البرنامج «قصصاً واقعية»، والشبكة تبيع لعبة ورق «جناية» (115 ريالاً، 3–6 لاعبين، 12+) | `key_findings[2]` |
| ATH-SRC-2500 | المتحدث «Brig.» (عميد) | النص «اللواء» (Maj. Gen.) | `key_findings[1]` |
| ATH-SRC-2504 | متاحة في 7 متاجر لا تشمل السعودية | Lookup اليوم: موجودة في **8 متاجر منها السعودية**، بالإنجليزية فقط، وتقييماتها 0–2 | `key_findings[0]` |
| ATH-SRC-2507 | قائمة العلامات الحية في الفئة 41 بلا ATHRÚ | ATHRÚ (تسجيل 7756081، الفئة 41: تدريب قيادي للشركات) حيّة | `key_findings[0]` (إضافة) |
| ATH-SRC-2432 | المؤلفان «Elizabeth» de la Mora Velasco و«Yuhui» Chen | Crossref: **Efrén** de la Mora Velasco و**Yuting** Chen | `authors[0..1]`، و`limitations` (+1) |

كل تصحيح موسوم داخل النص بـ«[Corrected/Clarified 2026-10-27 by deep-card review]». وما يمس ملفات التركيب جُمع في البند C19.

## 4. ملاحظات تحقق لا تستدعي تعديل السجل
- **ATH-SRC-2031:** في قائمة 27/10 «جناية» الثاني في السعودية كما في السجل، والثاني عشر في الكويت بدل العاشر (تغير يومي). وقائمتا الإمارات أعادتا 504 مرتين، فلم تُفحص.
- **ATH-SRC-2248:** تناقض داخل موقع TAQADAM نفسه: الصفحة الرئيسية تقول «800+ طلب وحتى 60 فريقاً»، والأسئلة الشائعة «1,000+ وحتى 30». ذُكر في البطاقة.
- **ATH-SRC-2004:** الصفحة السعودية تُظهر **دبلجة عربية مصرية** إلى جانب الترجمة، وحلقات الموسم الأول 48–60 دقيقة. أُضيف في البطاقة.
- **ATH-SRC-2107:** إعفاء «الممارسات التعليمية العادية» (d)(1) **يسري على الأطفال**، ولا يذكره السجل. وهو مهم للمسار الصفي. أُضيف في البطاقة.
- **ATH-SRC-2083:** في مراجعات صفحة Play المصرية لاعب يطلب «إضافة العربية». يؤكد أن دعم العربية على أندرويد غير مؤكد.
- **ATH-SRC-2074:** النص العربي مضمن في الصفحة بترميز يونيكود هارب (أكثر من 1,200 سلسلة)، فلا يظهر بالبحث النصي البسيط. هذا يفسر خطأ ATH-SRC-1136 في الدفعة الأولى.
- **ATH-SRC-2111:** صفحة اللجنة الدائمة في جامعة الملك سعود أعادت 403، لكن ملف PDF ما زال يُنزَّل من الرابط نفسه.
- **ATH-SRC-2148:** حجم عينة تجربة فيسبوك غير مذكور في الإشعار ولا في ملخص المقال الأصلي، فلم يُذكر رقم في البطاقة.

## 5. ما لم يُلمس
- `15_STORY_MEDIA_AND_ASSETS/_data/sources_w2_images_gulf.jsonl` (الفريق ما زال يعمل).
- لم يُعدَّل `01_SOURCE_CATALOG/sources_master.jsonl`. تُنقل حقول `deep_card` والتصحيحات إليه في خطوة الدمج التالية (`00_PROJECT_CONTROL/tools/merge_catalog.py`).
- لم تُعدَّل ملفات التركيب، والبنود التي تمسها في C19.
