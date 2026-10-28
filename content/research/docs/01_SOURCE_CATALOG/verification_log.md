# سجل التحقق المستقل من الفهرس — ATHAR Source Verification Log

- **التاريخ:** 2026-10-27 · **المدقق:** مدقق مستقل (لم يشارك في إنتاج المكتبة) · **الحالة:** FINAL — Parts 1–4 complete
- **النطاق:** عينة 76 سجلاً من `verification_sample.csv` (عينة طبقية عشوائية لكل مكتبة، وكل سجل تحقق بنتيجة بحث فقط، وسجلات أساسها ويكيبيديا)، ثم تدقيق الاقتباسات والسلامة والاتساق الداخلي.

## 1. المنهج

1. قرأت `00_PROJECT_CONTROL/RESEARCH_PROTOCOL.md` (المخطط وقواعد عدم الاختلاق والاقتباس والسلامة).
2. لكل سجل: فحص آلي لكل `url` و`verification_url` (HTTP عبر curl مع متابعة التحويل)، وحلّ كل DOI عبر doi.org، وجلب بيانات Crossref (العنوان، المؤلفون، المجلد/العدد/الصفحات، السنة، الترخيص). ثم فحص محتوى موجّه واحد لكل سجل: ملخص OpenAlex/PubMed/ERIC، أو نص PDF الرسمي، أو نص ويكيبيديا الخام (`action=raw`)، أو واجهات Steam/iTunes/GitHub عند حجب صفحات المتجر للزواحف، ومقارنة نتيجة رئيسية واحدة على الأقل بالنص المصدر.
3. عند حجب الموقع الأصلي (Wiley/SAGE/T&F/Annual Reviews 403، وبوابة تشريعات الإمارات خلف Cloudflare، وGDC Vault في صيانة، وarablit 403) استُخدم مصدر بديل مستقل وذُكر في الجدول.
4. التصنيف: **PASS** سليم؛ **MINOR** خطأ صغير في البيانات أو الحقوق أو الرابط مع بديل؛ **MAJOR** عمل خاطئ، أو سنة خاطئة بأكثر من سنة، أو نتيجة غير مدعومة، أو رابط ميت بلا بديل؛ **FABRICATED** لا أثر له؛ **UNCHECKABLE** محجوب.
5. الإصلاحات تُطبَّق في ملف المكتبة المالكة `_data/sources*.jsonl` فقط. **لم يُعدَّل** `sources_master.jsonl`/`.csv` (خارج صلاحية التدقيق)، فيجب إعادة توليده بخطوة الدمج.

## 2. نتائج العينة (76 سجلاً)

| source_id | library | basis | verdict | issue / evidence | fix applied |
|---|---|---|---|---|---|
| ATH-SRC-0119 | 02 | random | MINOR | Metadata/claims OK (Collins 6 Nov 1939; Dodd Mead Jan 1940; 100M+ copies by 2007; UK title change 1985). rights_jurisdiction still applies repealed SA 2003 Art.19 ('ended Jan 2026'); library's current position is M/169 Art.22 -> PD 1 Jan 2027 (Gregorian), counsel. | rights_jurisdiction SA clause aligned with LITERARY_RIGHTS_REGISTER; same clause fixed in all 10 Christie records 0113-0122 (02 file) — **applied** |
| ATH-SRC-0106 | 02 | random | PASS | Strand Dec 1892; Memoirs 1893; dog-in-the-night-time clue confirmed (Wikipedia). | — |
| ATH-SRC-0116 | 02 | random | MINOR | Metadata/claims OK (Collins 1 Jan 1934; US 'Murder in the Calais Coach'; Lindbergh echo; two solutions). Same stale SA Art.19 rights clause. | rights_jurisdiction SA clause aligned — **applied** |
| ATH-SRC-0124 | 02 | random | PASS | 1929; Collins/Doubleday Doran; six solutions; Brand 1979 + Edwards 2016; Barzun & Taylor critique; Berkeley d. 9 Mar 1971 confirmed. | — |
| ATH-SRC-0184 | 02 | random | MINOR | Knopf 1939 and 'no idea who killed the chauffeur' anecdote confirmed. rights_jurisdiction says Chandler death 'not fetched': he died 26 Mar 1959, so UK/EU life+70 runs to end-2029 and life+50 Arab jurisdictions expired ~2009/2010 - record understated Arab-market status. | rights_jurisdiction completed (counsel caveat kept) — **applied** |
| ATH-SRC-0152 | 02 | random | MINOR | Essay exists (The New Yorker, 20 Jan 1945; New Yorker page title confirmed). Record url/verification_url pointed to a Wikipedia genre page and publisher was 'from general knowledge'. Claim (crossword-puzzle put-down) supported by secondary quote. | url -> newyorker.com article; publisher confirmed; edition date added — **applied** |
| ATH-SRC-0212 | 03 | random | PASS | Takumi (orig.)/Maruyama (2023 remaster); 4-minute rewind/checkpoint mechanic; mobile remaster 28 Mar 2024; 81,325 JP physical by Dec 2010; reviewers' trial-and-error/linearity critique - all confirmed. | — |
| ATH-SRC-0229 | 03 | random | PASS | GameBanshee, ValH, 5 Jan 2023; alibi system cut ('rule people in'), motive focus, murderers never identified beyond doubt - confirmed. | — |
| ATH-SRC-0203 | 03 | random | PASS | 271 clips; 100k+ sold (60k Windows/40k iOS); BAFTA Game Innovation + Mobile & Handheld; IGF Seumas McNally; L.A. Noire/Ace Attorney/Serial influences - confirmed. | — |
| ATH-SRC-0269 | 03 | random | PASS | GDC Vault still in maintenance (HTTP 200 but no content). Talk independently confirmed by Thumbsticks report (16 Mar 2016) and search listing; record already discloses Vault limitation. | — |
| ATH-SRC-0265 | 03 | random | PASS | Game Developer, Bryant Francis, 26 Nov 2018; how-they-died -> identity shift, feature matrix, 4->60 characters (+~1 year) - confirmed verbatim in interview. | — |
| ATH-SRC-0254 | 03 | random | PASS | Crossref/OpenAlex: CHI PLAY '14 pp.181-190, 5 authors; abstract matches skill-introduction finding. | — |
| ATH-SRC-0326 | 04 | random | PASS | Crossref: Letter to the Editor, JFS 60(4):1111-1112, 7 authors. (OpenAlex lists a green CC BY repository copy - rights could be upgraded after checking.) | — |
| ATH-SRC-0335 | 04 | random | PASS | Crossref: FSI Synergy 5:100273, CC BY-NC-ND 4.0; abstract confirms inconclusives/error-rate framing. | — |
| ATH-SRC-0352 | 04 | random | MINOR | Metadata OK (Digital Investigation 6:S2-S11). Crossref VOR licence CC BY-NC-ND 4.0 (since 2019) and OpenAlex hybrid OA - record said COPYRIGHTED_RESTRICTED/paywalled. | rights_status OPEN_LICENSE, license CC BY-NC-ND 4.0, access open_access, storage yes, commercial no — **applied** |
| ATH-SRC-0302 | 04 | random | PASS | PDF: approved 6 Jan 2017; 400+ papers; INTERPOL summaries; closed-set designs underestimate error - confirmed. | — |
| ATH-SRC-0305 | 04 | random | PASS | NIST IR 8352 (Mar 2023), 4 authors; three premises unsupported; 39 analysts / 8% of cases reached 90% agreement - confirmed in PDF. | — |
| ATH-SRC-0346 | 04 | random | MINOR | Cited URL returns 404. Current page innocenceproject.org/misapplication-of-forensic-science/ states misapplied forensics contributed to 'more than half' of IP cases and 'nearly a quarter' of all exonerations since 1989, and lists hair, arson, CBLA - consistent with the 52%/24% finding. | url/verification_url/title updated to live page; limitation added — **applied** |
| ATH-SRC-0429 | 05 | random | PASS | CIA PDF: ISBN 1-929667-00-0; articles 1978-86; satisficing; 'least evidence against it'; ACH Steps 1-8; Persistence of Impressions section - confirmed. | — |
| ATH-SRC-0415 | 05 | random | PASS | Crossref Annu Rev Psychol 70:295-317; abstract confirms 'faint and unreliable' cues and mediocre lie catchers. | — |
| ATH-SRC-0433 | 05 | random | PASS | CIA PDF: 'serious possibility' read as 20-80 to 80-20 odds; 93%/75% chart; 'chances about even' - confirmed. | — |
| ATH-SRC-0450 | 05 | random | PASS | Crossref/OpenAlex JPSP 47(6):1231-1243; abstract matches. | — |
| ATH-SRC-0448 | 05 | random | PASS | Crossref PCL 19(10):921-931 (2013; online 2012); abstract: N=29, 42% incorrect, clothing-only improvement - confirmed. | — |
| ATH-SRC-0414 | 05 | random | PASS | Psych Bull 137(4):643-659; abstract: lack of valid cues, eye contact r=-.15, perceived/actual cue covariation r=.59/.72 - confirmed. | — |
| ATH-SRC-0532 | 06 | random | PASS | RER 86(2) 2016 (online 2015); abstract confirms both findings. | — |
| ATH-SRC-0549 | 06 | random | PASS | Crossref ACP 26(5):721-729; abstract: n=50/48/35, r=-.38 - confirmed. | — |
| ATH-SRC-0522 | 06 | random | MINOR | Metadata/claims confirmed (5 videos; 6 RCTs n=6,464; YouTube n=22,632). Article is gold OA under CC BY 4.0 (Europe PMC PMC9401631; OpenAlex) - record said UNKNOWN/not_established. | rights_status OPEN_LICENSE, license CC BY 4.0, storage yes, commercial yes (attribution) — **applied** |
| ATH-SRC-0525 | 06 | random | PASS | ERIC: six 50-min lessons, matched control n=271 vs 228, significant growth - confirmed. | — |
| ATH-SRC-0562 | 06 | random | MINOR | Claims confirmed (training/teaming/tracking; best forecasts 2 years). MASTER record is a bad merge with alias 0443: 14 authors with Barbara Mellers duplicated (Crossref lists 13), duplicated key_findings and limitations. Owning 06 record is clean. | none needed in owning file (clean) — **no owning-file change; master regeneration required** |
| ATH-SRC-0541 | 06 | random | PASS | Annu Rev Psychol 64:135-168; abstract confirms 3 core EFs and stress/sleep/loneliness/exercise effects. | — |
| ATH-SRC-0658 | 07 | random | MINOR | Abstract confirms 0.94->0.98 Spearman. arXiv lists 'COLM 2024' (peer-reviewed venue) and CC BY 4.0 licence; record said UNKNOWN and 'not confirmed as peer-reviewed'. | rights OPEN_LICENSE CC BY 4.0; publisher notes COLM 2024; limitation corrected (grade left at C for owner to review) — **applied** |
| ATH-SRC-0616 | 07 | random | PASS | Assessment in Education 5(1):7-74; PDF (Glasgow-hosted reproduction) confirms substantial gains and ego- vs task-involving feedback. | — |
| ATH-SRC-0669 | 07 | random | PASS | ERIC/Crossref EMIP 45(2) 2026; 10 LLMs; caution against ranking - confirmed. | — |
| ATH-SRC-0623 | 07 | random | PASS | Crossref UMUAI 27(3-5):313-350. No abstract available; generic summary consistent with title. | — |
| ATH-SRC-0662 | 07 | random | MINOR | PubMed abstract confirms findings (priming twice as large within L1; LA ~ Hebrew). MASTER record is a bad merge with alias 0705: third key_finding says abstract 'not retrieved... to be confirmed', contradicting the others. Owning 07 record is clean. | none needed in owning file (clean) — **no owning-file change; master regeneration required** |
| ATH-SRC-0620 | 07 | random | PASS | OpenAlex abstract: 607 ES, 23,663 obs, d=.41, >1/3 decreased - confirmed. | — |
| ATH-SRC-0712 | 08 | random | PASS | All figures matched page (34.4M/99.0%, 38.6M, 29.6, YouTube 27.5M/79.2%, Snapchat 25.3M/72.9%, TikTok 38.6M 18+, +17.7%; published 8 Nov 2025). | — |
| ATH-SRC-0701 | 08 | random | PASS | Crossref Appl Psycholinguist 24(3):431-451; abstract confirms. | — |
| ATH-SRC-0716 | 08 | random | PASS | All 11 figures matched page. | — |
| ATH-SRC-0785 | 08 | random | PASS | Kill Screen, Priestman, 10 Nov 2016; Light Studio (5 women, Qatif), Aldubaisi, Wojdan, Indiegogo - confirmed. | — |
| ATH-SRC-0728 | 08 | random | PASS | Media Psychology 1(2):97-116; abstract (90% reported enduring reactions; 26.1% residual anxiety) consistent. | — |
| ATH-SRC-0735 | 08 | random | PASS | Index page lists Memory of Modern Egypt and Manuscripts Museum; record already low-confidence/needs_expert_review. | — |
| ATH-SRC-0884 | 09 | random | MINOR | Release 11 Apr 2023, 15 langs incl. Arabic, age gate 13, content notes, 81% of 1,157 confirmed. '$3.99' is a 90% sale price (regular $39.99) - record omitted the discount caveat. | key_finding price annotated (regular $39.99) — **applied** |
| ATH-SRC-1160 | 09A | random | PASS | iTunes lookup: released 13 Jul 2026; AR/EN; 1,355 cases/10 volumes; IAP SAR 4.99-12.99; 3 ratings - confirmed. | — |
| ATH-SRC-1154 | 09A | random | PASS | Site meta description matches. | — |
| ATH-SRC-1176 | 09A | random | PASS | iTunes lookup: Tamatem Inc., 2021, 9+, 4.36 from 9,991 ratings; 20+ stories; IAP 9.99-89.99 - confirmed. | — |
| ATH-SRC-0853 | 09 | random | PASS | Page confirms question-guiding tutor, up to 10 children under 18, district-only classroom access. | — |
| ATH-SRC-0875 | 09 | random | PASS | 'six million students and 150,000 teachers'; Games for Change and Japan Prize - confirmed. | — |
| ATH-SRC-0821 | 09 | random | PASS | Steam API: 23 Mar 2024, $9.99, English only; 9 reviews - confirmed. | — |
| ATH-SRC-0883 | 09 | random | PASS | 15 Nov 2021; 16 langs incl. Arabic; $4.49 (90% sale of $44.99, record already says 'may be discounted'); 75% of 1,718. Note: Steam age gate 17 + sexual-violence descriptor not in record (relevant to teen positioning). | — |
| ATH-SRC-0919 | 10 | random | PASS | GitHub README: Apache-2.0, v1.8.0 badge, PostgreSQL 11-18, openCypher - confirmed (github.com HTML 403s to bots). | — |
| ATH-SRC-0968 | 10 | random | PASS | arXiv: authors, 3 strategy families, 98% cost / +4% accuracy - confirmed. | — |
| ATH-SRC-0950 | 10 | random | MINOR | Claims confirmed (0.514; pp.2511-2522; LLM-text bias). ACL Anthology licenses papers CC BY 4.0 - record said UNKNOWN. | rights OPEN_LICENSE CC BY 4.0, storage yes, commercial yes — **applied** |
| ATH-SRC-0941 | 10 | random | MINOR | Claims confirmed (WikiBio, grey-box baselines, pp.9004-9017). ACL Anthology CC BY 4.0 - record said UNKNOWN. | rights OPEN_LICENSE CC BY 4.0, storage yes, commercial yes — **applied** |
| ATH-SRC-0947 | 10 | random | PASS | arXiv abstract confirms GPT-4 prefers longer answers + proposed metric. | — |
| ATH-SRC-0912 | 10 | random | MINOR | Crossref SCP 8(3):231-274 confirmed. Article is in Elsevier's free open archive (OpenAlex bronze OA; Elsevier open-access user licence in Crossref) - record said paywalled. | legal_text_access -> open_access (free-to-read archive, still COPYRIGHTED_RESTRICTED) — **applied** |
| ATH-SRC-1049 | 11 | random | PASS | SDAIA PDF header shows M/19 (9/2/1443H) and M/148 (5/9/1444H); Art.35 SAR 3M/2 years and Art.36 SAR 5M confirmed in text. | — |
| ATH-SRC-1072 | 11 | random | PASS | Dkt 598 filed 06/25/25; thirteen authors; market dilution - confirmed. | — |
| ATH-SRC-1077 | 11 | random | PASS | Umm al-Qura page dated 1448-2-17 = 31-07-2026; Art.17, Art.30 (AI copying) and Art.85 (six conditions, 48 working hours, repeat-infringer policy) confirmed. | — |
| ATH-SRC-1041 | 11 | random | PASS | Mirror text of Art.28(1)-(4) matches record; EUR-Lex returns bot challenge (202). | — |
| ATH-SRC-1045 | 11 | random | PASS | Press release lists SB 243, AB 1043, AB 56 - confirmed. | — |
| ATH-SRC-1055 | 11 | random | MINOR | Official portal blocks automated access (Cloudflare 403). ICMEC 2019 compilation of the official translation confirms Arts. 1, 13, 26, 29, 42; Art.42(2) names 'educators, physicians, social specialists', not 'custodians' as the record says. | key_finding Art.42(2) wording corrected; limitation notes secondary verification — **applied** |
| ATH-SRC-0145 | 02 | search_only | PASS | Kirkus: Neem Tree Press, tr. Sawad Hussain, ISBN 9781911107859, US pub 7 May 2024 (UK Feb 2024), Abbasid Baghdad, Algeria; The Bookseller: English PEN Translates Award 2021. (arablit URL 403s to bots.) | — |
| ATH-SRC-0147 | 02 | search_only | PASS | UMSL page: American Magazine, Sept. 1928; rules on servants, secret societies, the dog that does not bark - confirmed. | — |
| ATH-SRC-0320 | 04 | search_only | MINOR | legislation.gov.uk confirms Act and code-of-practice duty. Site states content is under Open Government Licence v3.0 - record said UNKNOWN. | rights OPEN_LICENSE OGL v3.0, storage yes, commercial yes — **applied** |
| ATH-SRC-0413 | 05 | search_only | PASS | Crossref PSPR 10(3):214-234; article abstract: 206 documents, 24,483 judges, 54%, 47% lies / 61% truths, audio > visual - confirmed. | — |
| ATH-SRC-0501 | 06 | search_only | PASS | Denver catalog record lists ISBN 9780374275631 (hc) alongside the 2013 paperback; FSG confirmed. | — |
| ATH-SRC-0707 | 08 | search_only | MINOR | Method (3,600, 18 states, 53 cities, SixthFactor), news 61%/45%, 74%, platform split, GCC/Levant/NA 53/39/37 confirmed on cited pages. Identity figures (religion 27%, family/tribe 27%, nationality 15%, language 11%, 54% Arabic less important) are NOT on the cited pages; found in Daily News Egypt 14 Aug 2023. | limitation added with the supporting URL — **applied** |
| ATH-SRC-0760 | 08 | search_only | PASS | Aggregator text confirms 72/48 periods; record already E-grade/needs_expert_review. | — |
| ATH-SRC-1048 | 11 | search_only | PASS | KSAT/AP article fetched: 30 Dec 2022, last Holmes stories enter US PD 1 Jan 2023. | — |
| ATH-SRC-0742 | 08 | wikipedia | PASS | Wikipedia: 1956-2020, Tanta, physician, Ray of Death -> Malaf al-Mostaqbal - confirmed. | — |
| ATH-SRC-0140 | 02 | wikipedia | PASS | EN/AR Wikipedia: ~300 books, 'Godfather', 1931-24 Feb 2013; 1968 Nadia Nashat suggestion, Five Find-Outers, Maadi, TV same year - confirmed. | — |
| ATH-SRC-0739 | 08 | wikipedia | PASS | 11 Jun 2020, 8 episodes, Saudi Netflix original (writer-director Hana Alomair; authors field empty). | — |
| ATH-SRC-0121 | 02 | wikipedia | MINOR | Dodd Mead Mar 1949 / UK May 1949; 12-year-old Josephine; Christie favourite - confirmed. Same stale SA Art.19 rights clause. | rights_jurisdiction SA clause aligned — **applied** |
| ATH-SRC-0104 | 02 | wikipedia | PASS | Lippincott's Feb 1890; Spencer Blackett Oct 1890; Tonga - confirmed. | — |
| ATH-SRC-0135 | 02 | wikipedia | PASS | Raven/Bloomsbury 2018; eight hosts; Costa First Novel 2018 - confirmed. | — |

## 3. الإجماليات ومعدل الخطأ

| verdict | n | % of 76 |
|---|---|---|
| PASS | 58 | 76.3% |
| MINOR | 18 | 23.7% |
| MAJOR | 0 | 0.0% |
| FABRICATED | 0 | 0.0% |
| UNCHECKABLE | 0 | 0.0% |

| rate | k/n | point | Wilson 95% CI |
|---|---|---|---|
| MAJOR+FABRICATED — all 76 | 0/76 | 0.0% | 0.0% – 4.8% |
| MAJOR+FABRICATED — stratified-random part only | 0/62 | 0.0% | 0.0% – 5.8% |
| MINOR — all 76 | 18/76 | 23.7% | 15.5% – 34.4% |
| MINOR — stratified-random part only | 15/62 | 24.2% | 15.2% – 36.2% |

**قراءة النتيجة:** لم يُعثر على أي سجل مختلق أو خاطئ جوهرياً. الحد الأعلى لفترة Wilson عند 0/76 هو 4.8% (و5.8% للجزء العشوائي وحده، 0/62). أي أن معدل الأخطاء الجوهرية في الفهرس كله، إن وُجدت، يُرجَّح أن يكون دون 5%. **تحفظ:** العينة طبقية لكل مكتبة لا متناسبة مع حجمها، وأُضيفت إليها عمداً طبقات عالية الخطورة (بحث فقط، ويكيبيديا). لذلك فالتقدير تقريبي للفهرس (815 سجلاً)، لا تقدير موزون. وأخطاء MINOR شائعة (حوالي ربع العينة)، ومعظمها في **حقول الحقوق** لا في وجود المصدر.

**أنماط الأخطاء الصغيرة (MINOR):**
- **الحقوق محافظة أكثر من اللازم أو قديمة أو ناقصة (11 سجلاً):** مصادر مفتوحة فعلياً (CC BY في ACL Anthology وScience Advances وarXiv، وCC BY-NC-ND لدى Elsevier، وOGL v3 لموقع legislation.gov.uk، والأرشيف المفتوح لـElsevier) سُجلت `UNKNOWN` أو `paywalled`. وثلاث روايات لكريستي (من العينة) ما زالت تحمل بند السعودية وفق نظام 2003 الملغى، وسجل شاندلر لم يذكر تاريخ الوفاة ولا وضع الأسواق العربية.
- **دمج معيب في الفهرس الرئيسي (2 في العينة؛ 18 على الأقل في الفهرس كله):** عند دمج المكررات أُلحقت نتائج وحدود السجل البديل بالسجل الأصلي دون تنقيح، فتكررت الأسماء (Mellers مرتين في 0562) أو تناقضت النتائج (0662 فيه نتيجة تقول إن الملخص «لم يُسترجع»). سجلات المكتبات المالكة سليمة؛ الخلل في `sources_master.jsonl` فقط.
- **روابط وأسعار وأصل الأرقام:** رابط Innocence Project ميت (له بديل حي يدعم الأرقام)؛ سعر Steam مخفّض 90% دون تنبيه؛ أرقام الهوية في مسح الشباب العربي مأخوذة من صفحة غير المذكورة؛ مقال Edmund Wilson كان مربوطاً بصفحة ويكيبيديا عامة.

### 3.1 ملفات عُدّلت في الجزء الأول

| file | records changed | nature |
|---|---|---|
| 02_DETECTIVE_LITERATURE/_data/sources.jsonl | 12 (0113–0122, 0152, 0184) | 10 Christie `rights_jurisdiction` SA/EG clause; 0152 url/publisher; 0184 Chandler term |
| 04_FORENSIC_SCIENCE/_data/sources.jsonl | 3 (0320, 0346, 0352) | OGL v3; dead link replaced; CC BY-NC-ND |
| 06_COGNITIVE_SCIENCE/_data/sources.jsonl | 1 (0522) | CC BY 4.0 |
| 07_LEARNING_SCIENCE/_data/sources.jsonl | 1 (0658) | CC BY 4.0; COLM 2024 venue |
| 08_ARAB_AUDIENCE_AND_CULTURE/_data/sources.jsonl | 1 (0707) | provenance of identity figures |
| 09_COMPETITIVE_INTELLIGENCE/_data/sources.jsonl | 1 (0884) | discount caveat |
| 10_TECHNICAL_ARCHITECTURE/_data/sources.jsonl | 3 (0912, 0941, 0950) | CC BY 4.0 ×2; open archive |
| 11_RIGHTS_PRIVACY_AND_SAFETY/_data/sources.jsonl | 1 (1055) | Art. 42(2) wording; secondary verification |

كل تعديل مُعلَّم داخل السجل ببند في `limitations` يبدأ بـ `AUDIT 2026-10-27:`. وكل الملفات أُعيد تحميلها بعد الكتابة سطراً سطراً للتأكد من صلاحية JSON، وبقي عدد الأسطر كما هو. **لم يُصنَّف أي سجل FABRICATED، فلم يُغيَّر أي `review_status`.**

## 4. الجزء الثاني: الاقتباسات وحقوق النشر

**الطريقة:** سكربت Python مسح 144 ملف `.md` (باستثناء `MASTER_PROMPT_ORIGINAL.md` و`99_LEGAL_SOURCE_ASSETS`) بحثاً عن مقاطع بين `"…"` و`“…”` و`«…»` و`‘…’` تتجاوز 15 كلمة، وعن معرّف مصدر يُقتبس منه أكثر من مرة في الملف نفسه، وعن اقتباسات كتلية (`>`). ثم فحص تكميلي: مقارنة نصية آلية (12-gram) بين ملفات المكتبة والنصوص الأصلية التي جلبتُها لـ26 مصدراً (ملخصات، ومقابلات، وصفحات ويكيبيديا للروايات).

**النتائج (8 مقاطع أطول من 15 كلمة، و10 حالات تكرار):**

| file:line | span | judgement |
|---|---|---|
| 06_COGNITIVE_SCIENCE/cards/ATH-SRC-0518.md:38 | 19 words | صياغة ATHAR لادعاء تسويقي مسموح، لا اقتباس من مصدر |
| 07_LEARNING_SCIENCE/EVIDENCE_CENTERED_ASSESSMENT_MODEL.md:151 | 18 | مثال حوار خيالي لمتعلم (بالعامية) |
| 07_LEARNING_SCIENCE/EDUCATIONAL_VALIDATION_PLAN.md:135 | 17 | صياغة ادعاء ATHAR المقترح |
| 07_LEARNING_SCIENCE/cards/ATH-SRC-0639.md:3 | 16 | عنوان بيان FTC الصحفي (بيانات ببليوغرافية) |
| 10_TECHNICAL_ARCHITECTURE/_data/agent_report.md:48 | 16 | قيود ASP كتبها الفريق نفسه |
| 05_INVESTIGATIVE_REASONING/EVIDENCE_EVALUATION_GUIDE.md:70, 77, 143 | 17–21 | نصوص ATHAR الموجهة للمراهق |
| 10 multi-quote hits (e.g. 09_.../ATHAR_DEFENSIBILITY_ANALYSIS.md:145, 04_.../FORENSIC_SCIENCE_KNOWLEDGE_ATLAS.md:256) | 2–7 words each | ادعاءات تسويقية مرفوضة، أو أرقام PCAST، أو عبارات يمنعها ATHAR؛ ليست اقتباسات متعددة من نص المصدر نفسه |

- اقتباسات مباشرة حقيقية من مصادر وجدتُها كلها **دون 15 كلمة**، مثل: «faint and unreliable» [0415]، وعبارة Kahneman ذات 7 كلمات في `06_.../COGNITIVE_BIAS_CASE_LIBRARY.md:173` [0502]، وتعريف Kane ذي 11 كلمة في `07_.../cards/ATH-SRC-0628.md:10`.
- المقارنة النصية: كل التطابقات الحرفية الطويلة **عناوين** في `bibliography.md` وحقول `title`، ولا تطابق في الملخصات أو النتائج.
- الروايات المحمية: لم أجد مقاطع أو حوارات أو أبيات من روايات كريستي أو شاندلر أو غيرهما؛ والملخصات تحليلية بصياغة الفريق.
- **الحكم:** لا مخالفة واضحة، و**لم أعدّل أي ملف .md في هذا الجزء.** ملاحظة صغيرة: تكررت عبارتان عربيتان مقتبستان من وصف منتج 1153 في ثلاثة ملفات من مكتبة 09، وهي ادعاءات تسويقية قصيرة (≤7 كلمات)، ولا تمثل خطراً.

## 5. الجزء الثالث: السلامة

**قراءة كاملة:** `SAFE_VIRTUAL_LABS_CATALOG.md`، و`CSI_MYTHS_AND_SCIENTIFIC_CORRECTIONS.md`، و`12_KNOWLEDGE_OBJECTS/forensic_concepts.jsonl` (32 كائناً)، و`AGE_APPROPRIATE_CONTENT_POLICY.md`، و`ETHICAL_INVESTIGATION_PRINCIPLES.md`.

**فحص المكتبة كلها (grep إنجليزي وعربي):** أسماء سموم (cyanide، arsenic، ricin، thallium…/سيانيد، زرنيخ…)، وجرعات (mg/kg، LD50، «جرعة قاتلة»)، ومتفجرات وكواتم صوت وأسلحة غير قابلة للتتبع، وإخفاء الأدلة ومكافحة الأدلة (anti-forensics، «التخلص من الأدلة»، «مسح البصمات»)، وتقنيات استجواب قسري (Reid، الحرمان من النوم، false evidence ploy)، وأدوات التخفي (VPN، Tor، burner).

**النتائج:**
- كل ورود للمصطلحات (24 سطراً) جاء **داخل قاعدة منع** أو سؤال لخبير، مثل: «لا يُستخدم أي سيناريو "سم غير قابل للكشف"»، و«لا محتوى عن المسح أو التشفير لغرض الإخفاء».
- الذكر الوحيد لاسم مادة سامة: `02_DETECTIVE_LITERATURE/DETECTIVE_LITERATURE_ATLAS.md:352`، حيث يُذكر الزرنيخ بوصفه فرضية حبكة «سم قوي» (Sayers 1930)، مع التنبيه إلى أنها علم قديم خاطئ. لا جرعة ولا طريقة؛ **مقبول**.
- المختبرات: استُبعد مختبرا الأسلحة (#29) و«طريقة الوفاة» (#30)، وبطاقات السموم (#27) مسموحة بمراجعة خبير فقط. وكائن السموم KO-FC-04-020 يستخدم «المركب Z» الخيالي ولا يذكر أي مادة حقيقية.
- مبادئ الاستجواب: القسر ممنوع خطاً أحمر، ولا تُشرح تقنياته، والعدائية لا تُكافأ أبداً، وهذا متسق مع Méndez ودليل الأمم المتحدة.
- **الحكم:** لا محتوى تشغيلي ضار، و**لم أعدّل أي ملف في هذا الجزء.**
- **ملاحظة سلامة للمنتج (ليست خللاً في المكتبة):** صفحة Sherlock Holmes Chapter One على Steam تحمل حد عمر 17 ووصف «إشارة إلى عنف جنسي»، وهذا غير مذكور في السجل 0883 ولا في الصف المدمج GC-059 في `competitors_global.csv`. يجب ألا يُعرض كمرجع مناسب للمراهقين.

## 6. الجزء الرابع: الاتساق الداخلي

### 6.1 حقوق أغاثا كريستي

| الوثيقة | LB/AE/JO/QA/KW | السعودية | مصر | UK/EU | US |
|---|---|---|---|---|---|
| 02/LITERARY_RIGHTS_REGISTER.csv (12 صفاً) | PD 1/1/2027 | م/169 م22 → 1/1/2027 (ميلادي، مع تحفظ م24) | حرفياً 12/1/2026؛ برن 31/12/2026 | حتى 31/12/2046 | بحسب سنة النشر (≤1930 حر) |
| 11/INTELLECTUAL_PROPERTY_RESEARCH.md §1، §3 | نفسه | نفسه | نفسه | نفسه | نفسه |
| 99_LEGAL_SOURCE_ASSETS/README.md:33 | نفسه (لا يذكر الكويت) | نفسه | 12/1/2026 (يذكر الحاجة إلى محامٍ) | نفسه | «ما نُشر حتى 1930» |
| **02/_data/sources.jsonl (قبل التدقيق)** | PD 1/1/2027 | **«SA Art.19 → انقضت يناير 2026»** ✗ | حرفياً فقط | نفسه | نفسه |

- الوثائق الثلاث المطلوبة **متفقة في الجوهر**. فرق صغير: README في 99 لا يذكر الكويت ولا قراءة برن لمصر، لكنه يُحيل إلى ملف 11 ويشترط رأي محامٍ، فلا تعارض.
- **التعارض الحقيقي كان في السجلات المصدرية:** عشرة سجلات لكريستي (0113–0122) احتفظت بالحساب السعودي وفق نظام 2003 الملغى. **صُححت في ملف المكتبة المالكة.** لكن الصيغة القديمة باقية في الملفات المشتقة: `sources_master.jsonl/.csv`، و`rights_register.csv`، و`11/SOURCE_RIGHTS_REGISTER.csv`، و`athar_library.sqlite` (10 سجلات في كل منها). تُصحَّح بإعادة تشغيل خطوة الدمج، ولم أعدّلها لأنها خارج نطاق صلاحيتي.

### 6.2 مطابقة الادعاءات الرقمية (6 ادعاءات)

| claim (file:line) | cited record | source check | result |
|---|---|---|---|
| 46% من 1,027 محلّفاً توقعوا دليلاً علمياً؛ فرق في 4 من 13 سيناريو (04/CSI_MYTHS…md:7–11) | 0342 | NIJ article: «1,027», «46 percent», «Only 4 of 13 scenarios» | ✓ |
| بصمات: إيجابية كاذبة 0.1%، سلبية كاذبة 7.5% (04/CSI_MYTHS…md:47) | 0331 | PNAS abstract: 0.1% / 7.5% | ✓ |
| حدود PCAST العليا 1 من 306 و1 من 18 (04/CSI_MYTHS…md:48؛ ATLAS:256) | 0301 | PCAST 2016 PDF | ✓ |
| الشعر المجهري: 11% (9 من 80) من أشخاص مختلفين (04/CSI_MYTHS…md:66؛ ATLAS:293) | 0301 / 0302 / 0346 | PCAST 2016 PDF: «9 of 80 cases (11 percent)». الرقم في التقرير الرئيسي 0301 وبطاقته، لا في 0302 ولا 0346 ولا في `key_findings` لـ0301 | ✓ الرقم صحيح؛ الإسناد إلى 0302/0346 زائد |
| Kluger & DeNisi: d = 0.41 وأكثر من ثلث التدخلات أضرّت (07/ATHAR_LEARNING_SCIENCE_FOUNDATION.md:211) | 0620 | OpenAlex abstract | ✓ |
| Many Labs 2: 54% تكررت، والمتوسط من 0.60 إلى 0.15 (06/COGNITIVE_BIAS_CASE_LIBRARY.md:189) | 0561 | OpenAlex abstract: median d 0.60 → 0.15 | ✓ (المصدر يقول «الوسيط» والملف يقول «متوسط»؛ فرق لفظي طفيف) |
| 54% يرون العربية أقل أهمية (08/ARAB_AUDIENCE_RESEARCH.md:14 وغيره) | 0707 | Daily News Egypt (لا الصفحات المذكورة في السجل) | ✓ الرقم صحيح؛ أُضيف مصدره إلى السجل |

**الحكم:** كل الأرقام المفحوصة صحيحة. الضعف الوحيد في الإسناد: يُستشهد برقم الشعر 11% بمعرفات لا تحويه (0302، 0346). لم أعدّل الملفات لأن الرقم صحيح ومذكور في بطاقة 0301، لكن يُنصح بحذف [ATH-SRC-0346] من سطر الأسطورة 9.

## 7. التوصية

**الحكم: الفهرس صالح لدعم قرارات المنتج على مستوى وجود المصادر ومحتواها، مع شرطين قبل أي قرار حقوقي أو تجاري.**

1. **الوجود والدقة الببليوغرافية — موثوقة.** 0 من 76 مختلق أو خاطئ جوهرياً، والحد الأعلى لفترة الثقة 95% هو 4.8%. والطبقات الأكثر خطورة (بحث فقط، وويكيبيديا) سليمة أيضاً، 0/14. كل نتيجة رئيسية فُحصت طابقت المصدر، وكثير من الأرقام طابقته حرفياً.
2. **حقول الحقوق — لا تُعتمد دون مراجعة.** نحو ربع العينة يحتاج تصحيحاً صغيراً، وأغلبه حقوق: 126 سجلاً `UNKNOWN`، منها 25 من arXiv و6 من ACL Anthology، و52 سجلاً `open_access` لكنها مصنفة `UNKNOWN` أو `COPYRIGHTED_RESTRICTED`. الخطأ في اتجاه الحذر، فلا يسبب مخالفة، لكنه يحجب مواد يمكن تخزينها واستعمالها قانونياً (CC BY). **يُعاد فحص التراخيص آلياً** عبر Crossref/OpenAlex/arXiv/ACL لكل سجل `UNKNOWN` أو `open_access`.
3. **الفهرس الرئيسي والملفات المشتقة متأخرة عن ملفات المكتبات.** يجب إعادة تشغيل الدمج قبل الاعتماد على `sources_master`، و`rights_register`، و`athar_library.sqlite`، لثلاثة أسباب:
   - تعديلات هذا التدقيق (23 سجلاً).
   - 10 سجلات لكريستي تحمل الحساب السعودي الملغى.
   - **18 سجلاً مدمجاً على الأقل** فيها تكرار أو تناقض في المؤلفين والنتائج (كشف آلي): 0531، 0533، 0553، 0562، 0639، 0662، 0664، 0786، 0830، 0846، 0900، 0945، 1009، 1011، 1013، 1019، 1020، 1114. ويجب أن يزيل الدمج التكرار ويختار نسخة واحدة لا أن يلصق النسختين.
4. **إعادة فحص مقترحة:**
   - أي رقم سوقي أو سعر من المتاجر، فهي لقطات زمنية وقد تكون أسعار تخفيض.
   - الصفحات الرسمية المحجوبة عن الأداة: بوابة تشريعات الإمارات، وGDC Vault، وEUR-Lex.
   - السجلات الـ31 المعلّمة `needs_expert_review`.
   - كل حكم حقوقي على كريستي والسعودية ومصر عبر محامٍ، كما تقول المكتبة نفسها.
5. **الاقتباس والسلامة:** لا مخالفات، والقواعد متسقة بين المكتبات 04 و05 و08 و11.

