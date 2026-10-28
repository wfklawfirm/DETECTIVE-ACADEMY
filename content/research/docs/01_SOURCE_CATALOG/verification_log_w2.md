# سجل التحقق المستقل من الدفعة الثانية — ATHAR Source & Asset Verification Log (Wave 2)

- **التاريخ:** 2026-10-27 · **المدقق:** مدقق مستقل ثانٍ (لم يشارك في إنتاج الدفعة الثانية) · **الحالة:** FINAL — الأجزاء 1–3 مكتملة
- **النطاق:** (1) عينة 77 سجلاً من `verification_sample_w2.csv`: 71 طبقية عشوائية عبر ملفات الدفعة الثانية الخمسة عشر، و6 سجلات تحققت منها الفرق بنتيجة بحث فقط. (2) عينة 57 أصلاً محفوظاً من `asset_audit_sample_w2.csv`: 30 صورة و15 ملفاً صوتياً و12 نصاً. (3) فحوص الاقتباس والسلامة والاتساق على 174 ملف Markdown عُدّلت بعد 07:00.
- **المرجعية:** `00_PROJECT_CONTROL/RESEARCH_PROTOCOL.md` و`WAVE2_PROTOCOL_ADDENDUM.md`. الصيغة على نمط `verification_log.md` (الدفعة الأولى).

## 1. المنهج

1. **آلياً لكل سجل:** فُحص كل `url` و`verification_url` عبر curl مع متابعة التحويل، بترويسة `User-Agent: ATHAR-Research-Library/2.0 (non-commercial research)`، وبفاصل ≥1.2 ث لكل مضيف. وحُلّ كل DOI عبر doi.org، وجُلبت بيانات Crossref (العنوان، والمؤلفون، والمجلد والعدد والصفحات، والتاريخ، والترخيص).
2. **فحص محتوى موجّه لكل سجل:** ملخصات OpenAlex، ونص PDF الرسمي (Scholastic، ESOMAR، Shute، O'Rourke، القانون المدني الكويتي، قانون الطفل المصري من أرشيف CRIN)، ونص ويكيبيديا الخام (`action=raw`)، وواجهات iTunes وSteam وHugging Face وLoC JSON وMet وWellcome وInternet Archive. وقورنت نتيجة رئيسية واحدة على الأقل بالنص المصدر، ومعظم السجلات بأكثر من نتيجة.
3. **عند الحجب:** ردّت مواقع OUP وSAGE وWiley/T&F وBrill وACM وLWW وIDEALS وOECD برمز 403 لـ curl. وردّت بوابة مجلة نايف (NAUSS OJS) برمز 404. وفرضت ويكيميديا كومنز حداً للطلبات (429) طوال الجلسة. **لم يُتجاوز أي حجب**؛ استُعملت Crossref وOpenAlex وDOAJ وEurope PMC، أو WebFetch أو WebSearch، كما يقضي الملحق §2.
4. **التصنيف:** **PASS** سليم؛ **MINOR** خطأ صغير في البيانات أو الحقوق أو الوصول أو الصياغة، مع بقاء الادعاء الرئيسي صحيحاً؛ **MAJOR** ادعاء رئيسي يناقضه المصدر، أو عمل خاطئ، أو سنة خاطئة بأكثر من سنة، أو رابط ميت بلا بديل؛ **FABRICATED** لا أثر له؛ **UNCHECKABLE** محجوب تماماً.
5. **الإصلاحات:** طُبقت في ملف المكتبة المالكة فقط (`*/_data/sources_w2*.jsonl`). وأُضيف إلى `limitations` في كل سجل معدّل بند يبدأ بـ `AUDIT-W2 2026-10-27:`. وأُعيد تحميل كل ملف بعد الكتابة سطراً سطراً: JSON صالح، وعدد الأسطر لم يتغير. **لم يُعدَّل** `sources_master.*` ولا `athar_library.sqlite`، فيلزم إعادة الدمج. النسخ الاحتياطية في مساحة العمل المؤقتة للجلسة.

## 2. نتائج عينة المصادر (77 سجلاً)

| source_id | file | basis | verdict | issue / evidence | fix applied |
|---|---|---|---|---|---|
| ATH-SRC-1245 | 02 heritage | random | PASS | Wellcome catalogue + Project MUSE: Todorov, Princeton UP 2017, ISBN 9780691167497. Finding consistent with the publisher blurb. | — |
| ATH-SRC-1239 | 02 heritage | random | MINOR | Crossref and arabist.hu: Ghersetti, *The Arabist* 17 (1996) pp.121–131, DOI OK. The journal page gives a free PDF download (HTTP 200, no login); the record said `paywalled`. | `legal_text_access` → free_official (rights unchanged) — **applied** |
| ATH-SRC-1221 | 02 heritage | random | PASS | Crossref/OpenAlex: Shabana, JIS 25(1):1–32, 2014. Abstract matches (qiyafa vs DNA paternity). OUP returned 403. | — |
| ATH-SRC-1217 | 02 heritage | random | PASS | Crossref: Malti-Douglas, JAL 19(2):108–127, 1988. No abstract available; title-level claim only, as the record discloses. Brill returned 403. | — |
| ATH-SRC-1241 | 02 heritage | random | PASS | Crossref: «Ḳiyāfa», EI2, DOI OK, no author or year in the metadata. The record already says the content was not verified. | — |
| ATH-SRC-1354 | 02 worldlit | random | PASS | Wikipedia raw: Dutton, 1 May 1978; Newbery; SLJ 2012 #9; 16 heirs, pairs, Turtle. | — |
| ATH-SRC-1357 | 02 worldlit | random | PASS | Wikipedia: 15 books 1943–1961, Peterswood, Mr Goon; *Burnt Cottage* published by Methuen 1943. | — |
| ATH-SRC-1305 | 02 worldlit | random | MINOR | PG #10556 text matches (preface Oct 1908, string, armchair format). But the first edition is **1908, Hodder & Stoughton** (Wikipedia, Open Library), not «Greening & Co. 1909». | publisher/year/rights_jurisdiction corrected; manifest TXT-W-007 note — **applied** |
| ATH-SRC-1368 | 02 worldlit | random | PASS | Wikipedia: 75 novels and 28 stories, 1930–1972; *Pietr* 1930; intuition over deduction. Simenon d.1989 is general knowledge, as the record says. | — |
| ATH-SRC-1328 | 02 worldlit | random | PASS | PG #564: 23 chapters. PG #70690: *Trial of John Jasper*, 7 Jan 1914, Chesterton as judge. Open Library reset the connection (the PG mirror suffices). | — |
| ATH-SRC-1337 | 02 worldlit | random | PASS | Wikipedia: Song origins, Ming/Qing peak, *Shi Gong'an* 1798, van Gulik 1949, ghosts, inverted structure, large casts. | — |
| ATH-SRC-1376 | 02 worldlit | random | PASS | PDF: YouGov, 6 Sep–4 Oct 2018, n=2,758; 36% / 30% / 27% character types; 52% «make me laugh». | — |
| ATH-SRC-1373 | 02 worldlit | random | PASS | Crossref/OpenAlex: SPPS 1(1):81–86. Abstract matches (Studies 1–2 and 3–5; evolutionary framing). | — |
| ATH-SRC-1708 | 04 | random | MINOR | Crossref/OpenAlex/DOAJ OK; WebFetch of the PDF confirms 8–9 Nov 2016, 166+ specialists, 16 countries, and the recommendations. **Rights:** the journal is CC BY-NC (DOAJ; PDF footer), not UNKNOWN. NAUSS OJS returned 404 to curl. | rights → OPEN_LICENSE CC BY-NC 4.0, open_access, storage yes, commercial no — **applied** |
| ATH-SRC-1731 | 04 | random | PASS | Hespress 14 Feb 2024: ISO/CEI 17025 by ANAB, Casablanca, all branches, «للمرة السادسة على التوالي». | — |
| ATH-SRC-1716 | 04 | random | MINOR | Crossref: AJFSFM 1(9):1286–1295, 2019. **An abstract exists** on OpenAlex (the record said none), and the licence is CC BY-NC (DOAJ/OpenAlex), not UNKNOWN. | rights + note — **applied** |
| ATH-SRC-1732 | 04 | random | PASS | UAEU page: 30 CH (21+9), 2 / 3 years, four core disciplines, collaboration with agencies. | — |
| ATH-SRC-1751 | 04 | random | MINOR | Crossref: ToP 20(1):33–35, Feb 1993; abstract matches. OpenAlex: closed, but the record said `free_official`. | `legal_text_access` → paywalled — **applied** |
| ATH-SRC-1742 | 04 | random | MINOR | OpenAlex/PubMed/Europe PMC: JDBP 36(2):75–85, 8 authors; abstract matches (n=94, mean 12.77 yr, 25.5% / 13.8%). Not OA, but the record said `free_official`. | `legal_text_access` → paywalled — **applied** |
| ATH-SRC-1652 | 07 | random | MINOR | PDF: 93 studies, 60 coded (42/4/14), 24 convergent. The DOI 10.22318/icls2023.395429 appears on the author's official publications page with pp.1977–1978, but the record left it null. | DOI added — **applied** |
| ATH-SRC-1647 | 07 | random | PASS | Crossref + Nature abstract: 25 samples, 24 countries, 17 languages; numerical ranges help. | — |
| ATH-SRC-1668 | 07 | random | PASS | Kuwait Times 11 Feb 2019: 147 not in service; «stopped and postponed». | — |
| ATH-SRC-1601 | 07 | random | PASS | ACL Anthology: 12 authors, 2,400 examples, the four models, 0.880 / 0.516, zero-shot, pp.130–150. | — |
| ATH-SRC-1636 | 07 | random | PASS | Shamaa: Abdel-Wahab; JoE 35(140) pt 2, Sep 2021; 459 Minia students; 14 doubtful items; Jabir and Hindam 1973. | — |
| ATH-SRC-1659 | 07 | random | PASS | Shamaa: Dirasat 50(2):527–547, 2023; 55 studies; random-effects d = 1.72. | — |
| ATH-SRC-2144 | 07 pilot | random | PASS | OpenAlex: CHI 2007, 4 authors; abstract matches. ACM returned 403. | — |
| ATH-SRC-2152 | 07 pilot | random | PASS | curl failed TLS (site chain); WebFetch confirms the ERC acts as the college IRB, with Kuwaiti law, MoH rules, Nuremberg, Belmont, Helsinki. | — |
| ATH-SRC-2106 | 07 pilot | random | PASS | PDF: © 2018 ESOMAR and GRBN copy/distribute notice; ≤12 = child, 13–17 = young person; school gatekeeper consent; age first; unidentifiable or delete. | — |
| ATH-SRC-2149 | 07 pilot | random | PASS | Crossref/OpenAlex: BERJ 33(6):927–942; abstract: Article 12, Space/Voice/Audience/Influence. Wiley returned 403. | — |
| ATH-SRC-2127 | 07 pilot | random | PASS | OpenAlex (gold, CC BY): 2308/4314 returned forms, 840/4314 granted; 40 schools; reasons; «first time asked». | — |
| ATH-SRC-1556 | 08 | random | PASS | Argaam 21 Oct 2024: 6,718.53k students; 513k teachers; 36,800 schools; intermediate 1,571.96k; secondary 1,457.65k. | — |
| ATH-SRC-1547 | 08 | random | PASS | Abjjad: «1483 كتاب»; first page has Qurban (005), Mourad, Christie, Hawkins, Turton. | — |
| ATH-SRC-1501 | 08 | random | PASS | Play (gl=SA): Criminal Case 100M+, 4.4, 4.26M reviews (spot-check of the lead title). | — |
| ATH-SRC-1530 | 08 | random | PASS | Al-Monitor (Marc Español): Egyptian dub after a ~10-year hiatus; fan-page admin cites demand + Disney Plus launch. | — |
| ATH-SRC-1526 | 08 | random | PASS | Crossref (CC BY): 12 studies; Abu-Liel 2021 n=77, grade 8; unvowelled fastest, vowelled best comprehension. | — |
| ATH-SRC-2070 | 09 | random | PASS | Steam API: release 1 Sep 2026; news 1 Sep (1,000 players; 1.3.8 all ten languages; 1.3.9 ollama/llama-server), 3 Sep Deck Verified, 6 Sep two cases, 1 Oct 35% off; SAR 15.99; DEJUS 12 / USK 16 / IGRS 18; content note as stated. | — |
| ATH-SRC-2078 | 09 | random | PASS | Al Bayan: «المتحري الواعد», ages 11–14, four days, MoE + KHDA partners, workshops + field activities. | — |
| ATH-SRC-2065 | 09 | random | PASS | iTunes SA: released 31 May 2026, v1.3.0 24 Oct, 9+, 13 languages incl. AR, 4.59 from 71. | — |
| ATH-SRC-2241 | 09 business | random | PASS | Wamda: $7.5B, 647 startups, +225%, $4B debt; KSA $5B/211; UAE $2B/218; Egypt $263M/89; early-stage $1.3B/486. | — |
| ATH-SRC-2237 | 09 business | random | PASS | Argaam: NCLE chairman, 16.5% all-time high. | — |
| ATH-SRC-2261 | 09 business | random | PASS | PwC: KSA 15% from 1 Jul 2020 (last reviewed 29 Jul 2026); Egypt 14%, SVRS (17 Aug 2026). | — |
| ATH-SRC-2246 | 09 business | random | PASS | dic.ae: four in5 centres; mentorship, networking, investor access. | — |
| ATH-SRC-2222 | 09 business | random | PASS | Moloco PR 15 Apr 2025: top 5% of US iOS high-value users = 0.02% of installs = 20% of revenue. (The second finding comes from a gamedevreports summary and was not re-fetched.) | — |
| ATH-SRC-2203 | 09 business | random | PASS | iTunes SA: Episode 12+, 18,149 ratings. IAP prices not re-scraped. | — |
| ATH-SRC-1930 | 10 | random | PASS | WebFetch of IDEALS (curl got 403): Ren-Jay Wang, M.S. 2017 (UIUC); abstract hints rated worse than none; choice did not matter. | — |
| ATH-SRC-1908 | 10 | random | **MAJOR** | Model card facts verified (gemma-2-9b base; 1T = 515B/410B/102B; Apache-2.0; not gated). **But the key finding «non-gated tokenizer — proxy for the gated Gemma-2 tokenizer family» is contradicted** by the published configs: Fanar-1 vocab_size 128,256 vs gemma-2-9b 256,000. The 1.24 ratio says nothing about Gemma-2. (Fanar-2 = Gemma-3 = 262,208, so that proxy holds.) | `review_status` → needs_expert_review + limitation; `10/ARABIC_TOKEN_COST_MEASUREMENT.md` annotated «(AUDIT-W2)» — **applied** |
| ATH-SRC-1925 | 10 | random | PASS | PDF: 79,895 players; baseline 89.45%; 192 vs 178 s; help button −12% / −15%, 31% clicked; «advice» rename. | — |
| ATH-SRC-1920 | 10 | random | PASS | GitHub raw: package.json 2.12.1, GPL-3.0; defaults.ts format list exact. | — |
| ATH-SRC-1914 | 10 | random | PASS | Crossref/OpenAlex (CC BY, hybrid OA): EMNLP 2023 pp.9904–9923; 22 languages; overcharged speakers. | — |
| ATH-SRC-1846 | 11 | random | PASS | IARC milestones: Gmedia (ex-GCAM) signs on 2024, starts rating 2026; Apple not listed. | — |
| ATH-SRC-1804 | 11 | random | PASS | Ibrachy & Dermarkar page: Decision 816/2025; licence + permit; consent before transfer; named states only; amendment for new destinations; transfer licence at 50% of the fee; guardian consent; 72-hour breach register. | — |
| ATH-SRC-1821 | 11 | random | PASS | Legiliban: Law 422 of 6 Jun 2002, OG no. 34, 13/06/2002. Arts 34 (social delegate), 40 (in camera), 42 (lawyer), 48 (publication ban) match. | — |
| ATH-SRC-1813 | 11 | random | PASS | ICNL PDF (printed 20/06/2016): Arts 86–88, 95, 96 (majority 21 Gregorian years) match verbatim. | — |
| ATH-SRC-1814 | 11 | random | PASS | CRIN .doc (2008 consolidation): Art. 2 (18); criminal responsibility from 12; 7–12 Child Court; lawyer; closed hearings; expert report. | — |
| ATH-SRC-2527 | 11 naming | random | MINOR | Re-screen (iTunes SA+AE) reproduces zero title hits for Qiyafa/قيافة/Muqtafi/مقتفي الأثر/Qarain. **But the Latin variant «Qeyafah» (قِيافه) is a live App Store app** (id 1508917144, menswear shop, updated 13 Jul 2026), so «zero app hits» is overstated. USPTO verification_url returned 502 (search UI, not a record). | limitation added; `11/NAME_CLEARANCE_ATHAR.md`, `14/ATHAR_VISION_RECOMMENDATIONS.md`, `14/PRODUCT_DIFFERENTIATION.md` annotated — **applied** |
| ATH-SRC-2500 | 11 naming | random | PASS | Emarat Al Youm 11 Oct 2022 (Mohammed Fouda): «أثر», GITEX 2022, ≥75%, four stages to one; Maj. Gen. Ahmed Thani bin Ghalita. | — |
| ATH-SRC-2515 | 11 naming | random | PASS | AUC news 25 Feb 2025: ATHAR teacher hub; acronym «meaning impact»; open-access free Arabic courses; digital badges. | — |
| ATH-SRC-2400 | 15 audio | random | PASS | kenney.nl: Interface Sounds 100 files CC0 (2020); RPG Audio 50 files CC0 (2014). | — |
| ATH-SRC-2415 | 15 audio | random | PASS | NASA page points to SoundCloud and usage guidelines; catalog only. | — |
| ATH-SRC-2431 | 15 audio | random | PASS | Crossref: Psychology of Music 39(4):424–448 (online 2010; print 2011). Abstract matches all claims. | — |
| ATH-SRC-1411 | 15 images | random | PASS | NIST page: Sept 2017 IARPA N2N; reviewed by the NIST RPO; no licence on the page. | — |
| ATH-SRC-1408 | 15 images | random | PASS | IA metadata: NOT_IN_COPYRIGHT, Routledge 1900, Henry. (The «1850–1931» author dates are not in the IA record; library catalogues give them.) | — |
| ATH-SRC-1402 | 15 images | random | MINOR | LoC item JSON: 17/23 stored photochroms say «No known restrictions on **publication**», but 6 Maghreb items (IMG-0380…0385) say «…on **reproduction**». The verification_url anchor no longer renders the statement. | limitation; register rows for the 6 corrected — **applied** |
| ATH-SRC-2301 | 15 gulf | random | PASS | LoC JSON for 2002714728: rights_advisory «No known restrictions on publication.»; Moritz 1916, Riemer. (HTML 403; JSON OK.) | — |
| ATH-SRC-2305 | 15 gulf | random | PASS | NASA brand page: not subject to US copyright; no endorsement; insignia protected; third-party material caveat; AI section. | — |
| ATH-SRC-2304 | 15 gulf | random | PASS | OGL v3 page: commercial use, attribution, exemptions (personal data, Royal Arms, insignia, third-party rights, IP, identity documents), non-endorsement. | — |
| ATH-SRC-2040 | 15 media | random | PASS | iTunes lookup: 51 tracks, last 26 May 2021, Drama, Clean, RSS feed listed. | — |
| ATH-SRC-2043 | 15 media | random | PASS | iTunes lookup: GZM Shows, 36 tracks, latest 2026-10-27 (rewind), Drama, Clean. | — |
| ATH-SRC-2046 | 15 media | random | PASS | YouTube channel HTML: «3.85M subscribers»; «سوالف طريق». The views/videos/joined figures need JS and were not re-read. | — |
| ATH-SRC-2032 | 15 media | random | PASS | iTunes: «فانز قصص رون», 915 tracks (record: 914, one episode added since), Drama. | — |
| ATH-SRC-2007 | 15 media | random | PASS | agathachristie.com: ITV 1989, almost 25 years, 200 countries, 13 series, 70 episodes, Suchet. | — |
| ATH-SRC-1246 | 02 heritage | search-only | PASS | PG #2627 page + text: Huxley, «On the Method of Zadig», chapter «Retrospective prophecy as a function of science». The record flags itself as a duplicate of 1330. | — |
| ATH-SRC-1381 | 02 worldlit | search-only | PASS | Complete Review: 2014 / Eng. 2022, Deeter, Pushkin, blackmail, «rather iffy». Wikipedia (TV): iQiyi 16 Jun 2020, Douban 8.9 / 619k, Variety #2, 1.12B Weibo posts. | — |
| ATH-SRC-1382 | 02 worldlit | search-only | PASS | Kirkus: Black Cat/Grove, 3 Jan 2017, Tiang, mid-1960s onward. Leeds: six sections in reverse order 2013…1967, «Eye of Heaven», Sonny Lok. | — |
| ATH-SRC-1643 | 07 | search-only | MINOR | OECD returned 403 to curl; WebFetch confirms the Saudi note «PISA 2025 Results (Volume I)», 8 Sep 2026. Swedish OECD delegation: 91 countries/economies. Petra: Jordan 375→407, 361→388, 342→363. «Computational problem solving» and the UAE/Morocco claims were not re-verified. | limitation (what is and isn't confirmed) — **applied** |
| ATH-SRC-2223 | 09 business | search-only | PASS | PPC Land + gamedevreports: CPI $0.56 (+30%); CPM $3.63→$4.34; paid/organic 2.07→3.33; MENA installs +2%, sessions +7%; D1 27%; top 5,000 apps, Jan 2024–Jan 2026, 23 genres, 6 regions, 21 countries. Adjust itself is gated. | — |
| ATH-SRC-2413 | 15 audio | search-only | PASS | MusicTech 30 Sep 2024: 33,000+ effects; non-commercial RemArc licence. Not stored (correct). | — |

## 3. الإجماليات ومعدل الخطأ

| verdict | n | % of 77 |
|---|---|---|
| PASS | 66 | 85.7% |
| MINOR | 10 | 13.0% |
| MAJOR | 1 | 1.3% |
| FABRICATED | 0 | 0.0% |
| UNCHECKABLE | 0 | 0.0% |

MINOR = 1239, 1305, 1708, 1716, 1751, 1742, 1652, 2527, 1402, 1643 · MAJOR = 1908. (Counts re-tallied by script from the table in §2.)

| rate | k/n | point | Wilson 95% CI |
|---|---|---|---|
| MAJOR+FABRICATED — all 77 | 1/77 | 1.3% | 0.2% – 7.0% |
| MAJOR+FABRICATED — stratified-random part only | 1/71 | 1.4% | 0.2% – 7.6% |
| MAJOR+FABRICATED — search-result-only part | 0/6 | 0.0% | 0.0% – 39.0% |
| MINOR — all 77 | 10/77 | 13.0% | 7.2% – 22.3% |
| any error (MINOR+MAJOR) — all 77 | 11/77 | 14.3% | 8.2% – 23.8% |

Search-result-only records (6): 5 PASS, 1 MINOR (1643). All 6 were re-verified against at least one primary or official page, so none needed to stay «search-only».

(Wilson intervals computed in Python with z = 1.96.)

**قراءة النتيجة:** لم يُعثر على أي سجل مختلق. الخطأ الجوهري الوحيد (1908) **استنتاج تقني** لا ببليوغرافيا: صحّة بطاقة النموذج سليمة، لكن ادعاء أن مرمّز Fanar-1 بديل لمرمّز Gemma-2 خاطئ. الحد الأعلى لمعدل الأخطاء الجوهرية في الفهرس قرابة 7%، أي أعلى قليلاً من الدفعة الأولى (4.8% عند 0/76)، وما يزال مقبولاً لمكتبة بحثية بشرط بقاء وسم المراجعة.

**أنماط الأخطاء الصغيرة:**
- **حقول الوصول والحقوق (5):** مجلة نايف (AJFSFM) بترخيص CC BY-NC، ووُسمت UNKNOWN في سجلين (1708، 1716)، بينما تحمل سجلات أخرى من المجلة نفسها في الملف 04 (مثل 1709–1715 و1759) الترخيص الصحيح؛ أي أن الخطأ عدم اتساق داخل الفريق. ومقالان مغلقان وُسما `free_official` (الملخص مجاني فقط). ومقال واحد مفتوح فعلياً وُسم `paywalled`.
- **بيانات ببليوغرافية (2):** ناشر الطبعة الأولى وسنتها لـ Orczy، وDOI ناقص لملخص ICLS.
- **صياغة مبالغة (2):** «صفر تطبيقات» لـ«قيافة» مع وجود «Qeyafah»؛ وعبارة حقوق LoC موحدة لمجموعة تتفاوت بنودها.
- **تحقق ثانوي (1):** PISA 2025 من صفحات حجبت الأدوات الآلية.

### 3.1 ملفات عُدّلت في الجزء الأول

| file | records changed | nature |
|---|---|---|
| 02_DETECTIVE_LITERATURE/_data/sources_w2_heritage.jsonl | 1 (1239) | legal_text_access |
| 02_DETECTIVE_LITERATURE/_data/sources_w2_worldlit.jsonl | 1 (1305) | publisher/year 1908 Hodder; rights_jurisdiction year |
| 04_FORENSIC_SCIENCE/_data/sources_w2.jsonl | 4 (1708, 1716, 1742, 1751) | CC BY-NC ×2; paywalled ×2 |
| 07_LEARNING_SCIENCE/_data/sources_w2.jsonl | 2 (1643, 1652) | verification note; DOI |
| 10_TECHNICAL_ARCHITECTURE/_data/sources_w2.jsonl | 1 (1908) | needs_expert_review + MAJOR limitation |
| 11_RIGHTS_PRIVACY_AND_SAFETY/_data/sources_w2_naming.jsonl | 1 (2527) | Qeyafah caveat |
| 15_STORY_MEDIA_AND_ASSETS/_data/sources_w2_images.jsonl | 1 (1402) | item-level rights variance |

## 4. الجزء الثاني: تدقيق تراخيص الأصول المحفوظة (57 أصلاً)

**المنهج:** حُسبت بصمة sha256 لكل ملف وقورنت بالسجل. ثم قورن نص الترخيص في السجل بالمصدر الرسمي عبر واجهة Met (`isPublicDomain`)، وLoC JSON (`rights_advisory` / `rights_information`)، وWellcome catalogue API (`locations.license`)، وInternet Archive metadata (`licenseurl`، `possible-copyright-status`)، وصفحات Kenney وOpenGameArt، وCommons API. وللنصوص: سنة وفاة المؤلف وسنة النشر وصيغة الملف وترويسة الترخيص. **ورُئيت 10 صور بالعين** (+ ورقتا معاينة) لفحص مرشّح السلامة.

**فحص إضافي خارج العينة:** طابقت بصمة **كل** الأصول المسجلة (600 صورة، و165 صوتاً، و84 نصاً = 849 ملفاً، 290.6 MB): **0 مفقود و0 بصمة مخالفة**. والحجم ضمن ميزانية 600 MB.

| asset_id | kind | source check | sha256 | verdict | note / fix |
|---|---|---|---|---|---|
| IMG-0546 | image | LoC/WDL: «unaware of any copyright… free to use and reuse» ✓ | ✓ | OK | **Viewed.** A man smoking a cigarette; children in the background (historical, non-sexual, not graphic). Not UNSAFE, but tagged `sensitivity:tobacco_depiction…` (avoid in 13–15). Residual unpublished-work risk already flagged by the producers. |
| IMG-0548 | image | WDL statement ✓ | ✓ | OK | |
| IMG-0176 | image | Met isPublicDomain true ✓ | ✓ | OK | |
| IMG-0460 | image | Commons API (after 429 back-off): CC BY-SA 4.0, attribution «Diego Delso», own work, 2024 ✓ | ✓ | OK | **Viewed.** Empty souq square, no people. Attribution and ShareAlike recorded. Modern architecture: FoP in KW is a lawyer question (already flagged). |
| IMG-0534 | image | WDL statement ✓ | ✓ | OK | |
| IMG-0397 | image | Wellcome API: cc-by ✓ | ✓ | OK | **Viewed.** Arabic medical manuscript page (heart/lung text). Attribution recorded. Basmala handling rule present. |
| IMG-0297 | image | LoC: «No known restrictions on publication» (Matson) ✓ | ✓ | OK | |
| IMG-0315 | image | LoC Matson ✓ | ✓ | OK | **Viewed.** Scouts' prize-giving, 1920–40, small figures. Not UNSAFE. Post-1930 / identifiable-person residual risk is already tagged `rights_review:post1930`. |
| IMG-0105 | image | Met PD ✓ | ✓ | OK | |
| IMG-0231 | image | LoC Matson ✓ | ✓ | OK | |
| IMG-0096 | image | Met PD ✓ | ✓ | OK | |
| IMG-0681 | image | Commons API (third retry after 8-min back-off): `{{self\|cc-by-sa-4.0}}`, author/uploader Wadimaktoob, own work, 2020-01-19 ✓ | ✓ | OK | **Viewed.** Wind tower, sky, no people. Attribution + ShareAlike recorded. |
| IMG-0199 | image | Met PD ✓ | ✓ | OK | **Viewed.** 1870s rug merchants, adults, posed commercial scene. |
| IMG-0538 | image | WDL ✓ | ✓ | OK | |
| IMG-0267 | image | LoC Matson ✓ | ✓ | OK | |
| IMG-0611 | image | WDL ✓ | ✓ | OK | |
| IMG-0135 | image | Met PD ✓ | ✓ | OK | |
| IMG-0654 | image | LoC calligraphy selection: «public domain or no known copyright restrictions… free to use and reuse» ✓ | ✓ | OK | |
| IMG-0094 | image | Wellcome API: cc-by ✓ | ✓ | OK | **Viewed.** Bertillon plate 55: ear shapes only, not graphic, no faces. Meets the filter (instrument/document type). |
| IMG-0352 | image | IA: NOT_IN_COPYRIGHT, Henry 1900 ✓ | ✓ | OK | **Viewed.** Fingerprint pattern diagram (Fig. 26). |
| IMG-0400 | image | Wellcome API: cc-by ✓ | ✓ | OK | |
| IMG-0465 | image | Commons API: «Public domain», {{PD-old}}, author unknown, own work (scan), uploaded 2026 ✓ | ✓ | OK | **Viewed.** Manuscript page with a tree diagram. The source of the scan is not given on Commons («own work»); provenance is thin, so get counsel before commercial use (not a mismatch). |
| IMG-0608 | image | WDL ✓ | ✓ | OK | |
| IMG-0581 | image | Met PD ✓ | ✓ | OK | |
| IMG-0248 | image | Met PD ✓ | ✓ | OK | |
| IMG-0412 | image | Wellcome API: pdm ✓ | ✓ | OK | |
| IMG-0285 | image | LoC Matson ✓ | ✓ | OK | |
| IMG-0539 | image | WDL ✓ | ✓ | OK | |
| IMG-0380 | image | LoC item: «No known restrictions on **reproduction**.» ✗ (register said «…publication.») | ✓ | **LICENCE-MISMATCH** (string) | **Viewed.** Constantine market, adults, not UNSAFE. Register corrected for IMG-0380…0385 (the 5 unsampled siblings share the same advisory). PD conclusion unchanged (photochrom c.1899). **Not quarantined:** the PD basis holds, only the quoted string was wrong. |
| IMG-0020 | image | Met PD ✓ | ✓ | OK | |
| AUD-0103 | audio | IA: PDM 1.0 ✓ (uploader radio@aporee.org; creator «OR poiesis») | ✓ | OK | PDM on a 2013 recording is a voluntary mark, not a waiver; the register says so. |
| AUD-0125 | audio | IA: CC0 1.0 (Musopen) ✓ | ✓ | OK | |
| AUD-0130 | audio | IA: CC0 1.0 ✓ | ✓ | OK | |
| AUD-0139 | audio | OGA: «License(s): CC0», StarNinjas ✓ | ✓ | OK | |
| AUD-0110 | audio | IA: PDM 1.0 ✓ | ✓ | OK | The creator field holds a truncated e-mail («damir.kustic@gma…»), as do AUD-0091/0106/0118. That is third-party personal data copied from IA metadata, so replace it with a name or handle. **Reported, not changed.** |
| AUD-0059 | audio | Kenney Impact Sounds: CC0 ✓ | ✓ | OK | |
| AUD-0018 | audio | Kenney RPG Audio: CC0 ✓ | ✓ | OK | |
| AUD-0053 | audio | Kenney: CC0 ✓ | ✓ | OK | |
| AUD-0040 | audio | Kenney Interface Sounds: CC0 ✓ | ✓ | OK | |
| AUD-0129 | audio | IA: CC0 1.0 ✓ | ✓ | OK | |
| AUD-0079 | audio | IA: PDM 1.0 (Frank Schulte, 2012) ✓ | ✓ | OK | Not auditioned by ear (producer's caveat stands: check for incidental speech or adhan). |
| AUD-0141 | audio | OGA: «License(s): CC0», unicaegames ✓ | ✓ | OK | |
| AUD-0093 | audio | IA: PDM 1.0 (Chris Weaver, 2016) ✓ | ✓ | OK | |
| AUD-0065 | audio | Kenney: CC0 ✓ | ✓ | OK | |
| AUD-0078 | audio | IA: PDM 1.0 (Benjamin Trimoreau, 2018) ✓ | ✓ | OK | Producer flagged a loudness jump. |
| TXT-W-000d | text | Doyle d.1930; *Memoirs* 1894 → US PD, life+70 ended 2000, life+50 ended 1980; PG header present ✓ | ✓ | OK | |
| TXT-W-036 | text | Mason d.1948; 1910 → PD in all three regimes; PG header ✓ | ✓ | OK | |
| TXT-W-058 | text | Okamoto d.1939 (Aozora author card); 1917 *Bungei Kurabu* → PD in all regimes; Aozora colophon ✓ | ✓ | OK | |
| TXT-W-007 | text | Orczy d.1947; stored file byte-identical to PG mirror #10556 (sha256 085ea0b8…) ✓; first book edition **1908** (manifest said 1909) | ✓ | OK | Manifest year corrected (not licence-relevant). |
| TXT-W-019 | text | Gaboriau d.1873; French original 1866 ✓; English translation correctly NOT stored | ✓ | OK | |
| TXT-W-020 | text | Zangwill d.1926; PG text reproduces the 1895 Rand McNally edition ✓ | ✓ | OK | |
| TXT-W-054 | text | Ranpo d.1965; first published 1925 (*Shashin Hōchi*) per Aozora colophon ✓. JP 50-year term ended 2015, non-retroactive 2018 extension; US pre-1931; EU/UK rule of the shorter term | ✓ | OK | The rule-of-the-shorter-term reasoning is sound but needs counsel (EU Art. 7(1) applies to non-EU authors). |
| TXT-W-060 | text | Okamoto ✓ | ✓ | OK | |
| TXT-W-038 | text | Poe d.1849; Standard Ebooks imprint: CC0 dedication ✓ | ✓ | OK | |
| TXT-W-008 | text | Orczy; byte-identical to PG mirror #72581 ✓; 1910; illustrator Cuneo d.1916 | ✓ | OK | |
| TXT-W-047 | text | Ranpo; first published Apr 1923 (*Shinseinen*) per Aozora colophon ✓ | ✓ | OK | Same counsel note as 054. |
| TXT-W-037 | text | Poe; Standard Ebooks CC0 ✓ | ✓ | OK | |

**ملاحظة جانبية على النصوص التراثية:** الترخيص CC BY-NC-SA 4.0 لمستودع OpenITI مؤكد عبر Zenodo (record 3082463)، وملف ATTRIBUTION لكل نص موجود ويقيّد الاستعمال بالبحث الداخلي.

**الإجماليات (57):**

| class | n / 57 | % | Wilson 95% CI |
|---|---|---|---|
| OK | 56 | 98.2% | 90.7% – 99.7% |
| LICENCE-MISMATCH | 1 (IMG-0380; 5 out-of-sample siblings IMG-0381…0385 had the same error and were also corrected) | 1.8% | 0.3% – 9.3% |
| ATTRIBUTION-MISSING | 0 | 0% | 0.0% – 6.3% |
| UNSAFE | 0 | 0% | 0.0% – 6.3% |
| FILE-MISSING | 0 | 0% | 0.0% – 6.3% |

By kind: images 29 OK + 1 mismatch (of 30); audio 15/15 OK; texts 12/12 OK. Commons returned HTTP 429 for most of the session; the three sampled Commons images were confirmed through the API only after long back-offs (no bypass).

**الحجر الصحي (`_QUARANTINE/`):** **لم يُنقل أي ملف.** لا ملف غير آمن في العينة، ولا ترخيص خاطئ في الجوهر (خطأ IMG-0380 في صياغة عبارة LoC فقط، والأساس القانوني صحيح). ولم يُنشأ مجلد `_QUARANTINE` لأنه لم يلزم.

**مرشّح السلامة (10 صور مرئية + ورقتا معاينة):** لا دماء ولا جثث ولا أسلحة مستعملة ولا محتوى جنسي ولا صور شخصية مقرّبة لأفراد. الملاحظتان الوحيدتان: تدخين في IMG-0546 (وسم أضيف)، ووجود أطفال عرضاً في صور تاريخية من 1915–1920. وفي ورقتي المعاينة (Photochrom؛ Matson ص2) لم تظهر صور مستبعدة؛ والحالة الحدية IMG-0373 (عمال حجارة، بالغون) آمنة.

**ملفات غير مسجلة:** 318 ملفاً في `99_LEGAL_SOURCE_ASSETS/` ليست في سجلات الصور والصوت والنصوص. منها 238 أيقونة يغطيها `ICON_AND_UI_ASSET_REGISTER.csv` على مستوى الحزمة لا الملف، و44 ورقة معاينة (`_contact_sheet*.jpg`) مشتقة من الصور المسجلة، و36 ملف ترخيص أو إسناد. لا شيء مجهول المصدر، لكن أوراق المعاينة تعيد نشر صور CC BY-SA وCC BY في مجمّعات بلا إسناد مضمّن، فلا تُوزَّع خارج الفريق.

### 4.1 ملفات عُدّلت في الجزء الثاني

| file | rows | change |
|---|---|---|
| 15_STORY_MEDIA_AND_ASSETS/IMAGE_ASSET_REGISTER.csv | 7 (IMG-0380…0385, IMG-0546) | licence string «…reproduction.» + AUDIT-W2 note in `pd_basis` for the six photochroms; sensitivity tag for IMG-0546. 600 rows kept; the other 593 are byte-identical. |
| 99_LEGAL_SOURCE_ASSETS/ASSET_MANIFEST_W2_TEXTS.csv | 1 (TXT-W-007) | 1909 → 1908 + AUDIT-W2 note. 84 rows kept. |

## 5. الجزء الثالث: فحوص الاقتباس والسلامة والاتساق (174 ملف Markdown بعد 07:00)

### 5.1 الاقتباسات وحقوق النشر
- **فحص آلي** لكل مقطع بين «» أو "" أو “” (عدا الشيفرة): 22 مقطعاً تتجاوز 15 كلمة. **كلها ليست اقتباسات من مصادر محمية.** هي عناوين أعمال (4)، ونصوص من صياغة ATHAR (قوالب الموافقة والإيضاح، وأسئلة المرشد، وأحكام التركيب)، وحوار من القضية النموذجية المؤلَّفة، ونص التفويض من المالك.
- **مقطع واحد يحتاج تدقيقاً:** `04/BIAS_LAB_ETHICS_FOR_MINORS.md` §الخطوة 4 بند 2 يضع بين «» نصاً عربياً من 25 كلمة متبوعاً بـ [ATH-SRC-0325]. وهو من صياغة ATHAR لنص الإيضاح الموجّه للمتعلم، لا ترجمة لمقطع من المصدر (المصدر بالإنجليزية وبترخيص CC BY-NC-ND). **لا تعديل؛** يُستحسن نقل الإحالة خارج علامتي التنصيص لئلا يُظن اقتباساً.
- **التكرار من المصدر نفسه:** المقاطع المتكررة المرتبطة بمعرّف واحد (1153، 2061، 2066، 1104) شعارات ATHAR المرفوضة أو أوصاف متاجر قصيرة، لا اقتباسات. وفي البطاقات المعمقة الجديدة لم يتجاوز أي مصدر اقتباساً إنجليزياً حرفياً واحداً (الأربعة التي ظهرت فيها مقطعان: عناوين أعمال أو أسماء وثائق).
- **الحكم:** لا خرق لقاعدة «اقتباس واحد أقل من 15 كلمة لكل مصدر».

### 5.2 السلامة (الأذى التشغيلي)
- بحث بالكلمات (جرعات ووحدات mg، وأسماء سموم، وسلاح، وطلق، وإخفاء أدلة، ومبيض، ونوافذ كشف، وتقنية Reid، وتعذيب، وتصيّد) في الملفات الـ 174، **مع قراءة المجلد 13 دون تعديله**.
- **النتيجة: 0 محتوى تشغيلي.** كل الإشارات قواعد منع (`AGE_APPROPRIATE_CONTENT_POLICY` §1، و`FORENSIC_EXPERT_REVIEW_CHECKLIST` أ1، و`SCIENTIFIC_REVIEW_CHECKLIST` أ1)، أو استبعادات صريحة (FINAL_STRATEGIC_REPORT: الأسلحة النارية ومكافحة الأدلة)، أو وصف تاريخي نقدي (الإكراه في التراث موسوم HER-07 «خيارات الإكراه غير متاحة»؛ التعذيب في «الگونگ آن» «لا يُنقل»).
- ذِكر «الزرنيخ» في `02/DETECTIVE_LITERATURE_ATLAS.md` تحليل لحبكة رواية بلا جرعة أو طريقة.
- لا نصوص استجواب قسرية؛ وتجاوز الخداع في مختبرات التحيز مضبوط بموافقة وإيضاح لاحق (C14).

### 5.3 الاتساق بين الملفات

| البند | الحالة | التفاصيل | الإصلاح |
|---|---|---|---|
| **كلفة الرموز ≈1.2× (لا «3×» غير مقيد)** | ✔ في كل ملفات الدفعة الثانية؛ ✖ في 3 ملفات قديمة | كل «3×» في ملفات الدفعة الثانية مقيدة بـ cl100k. وبقيت 3 صيغ غير مقيدة: `00/FINAL_HANDOFF_MANIFEST.md` §7، و`00/RESEARCH_GAPS.md` G28، و`14/CORE_REFERENCES_V1.md` المرجع 44. | الأول **صُحح** «(AUDIT-W2)». والآخران **لم يُلمسا** (يحررهما فريق آخر) — **يجب تحديثهما**. |
| **تواريخ ملكية كريستي العامة** | ✔ متسقة | UK/EU حتى نهاية 2046؛ LB/AE/JO/QA/KW، والسعودية بموجب م/169، من 1 يناير 2027؛ مصر حرفياً 12 يناير 2026 مع تحفظ المحامي. والمتسق نفسه في `LITERARY_RIGHTS_REGISTER.csv` (12 صفاً). الإشارة الوحيدة إلى «2047» في `11/INTELLECTUAL_PROPERTY_RESEARCH.md` تعني «الإتاحة من 2047» وهي متسقة. ملاحظة: `02/_data/agent_report.md` (الدفعة الأولى، 02:15) ما يزال يقول «EG and SA… ended Jan 2026» — تقرير تاريخي، صُحح في السجلات. | — |
| **التسمية: «أثر» المجرد غير موصى به** | ✔ متسقة في 09/11/14/00؛ ⚠ واحدة | `02/ARABIC_CLASSICAL_INFERENCE_HERITAGE.md` §5 يقترح «اسم العلامة يُفسَّر بقيافة الأثر» ويحيل القرار إلى W2-LEGAL دون ذكر الحكم اللاحق. | أُضيف بند 5 «(AUDIT-W2)» بالحكم وإحالة C18. |
| **قيد مصر على الحوار الذكي** | ✔ متسقة | «محجوب عملياً حتى الترخيص وتصريح النقل» في 09 و10 و11 و14 بلا تناقض. والاختلاف الوحيد لفظي («ممنوع عملياً» / «محجوب» / «يمنع النقل»). | — |
| **مدة التحقق 9–12 شهراً** | ✖ 5 مواضع قديمة | `14/FINAL_STRATEGIC_REPORT.md` (الحكم + D4) و`14/MVP_SCOPE.md` §0 يقولان 9–12. وبقيت «6–9» في: `14/ATHAR_VISION_RECOMMENDATIONS.md` البند 10، و`14/MVP_SCOPE.md` السطر 307، و`00/FINAL_HANDOFF_MANIFEST.md` §10، و`09/FUNDING_AND_PARTNERSHIP_LANDSCAPE.md` («0–9 أشهر»). | الأربعة **صُححت** «(AUDIT-W2)». و`14/OPEN_QUESTIONS_FOR_NEXT_PHASE.md` §8.2 مُحال إليه من ATHAR_VISION ولم يُفحص لتعديله (محمي). |

### 5.4 ملفات Markdown عُدّلت في الجزء الثالث (وسم «(AUDIT-W2)»)
`10/ARABIC_TOKEN_COST_MEASUREMENT.md` (Fanar-1 ليس Gemma-2) · `00/FINAL_HANDOFF_MANIFEST.md` (3× و6–9) · `14/ATHAR_VISION_RECOMMENDATIONS.md` (6–9؛ Qeyafah) · `14/MVP_SCOPE.md` (السطر 307) · `14/PRODUCT_DIFFERENTIATION.md` (Qeyafah) · `09/FUNDING_AND_PARTNERSHIP_LANDSCAPE.md` (0–9) · `11/NAME_CLEARANCE_ATHAR.md` (Qeyafah) · `02/ARABIC_CLASSICAL_INFERENCE_HERITAGE.md` (حكم التسمية).
**تنبيه:** أثناء التدقيق (15:15–15:19) كتب محرر آخر في `14/MVP_SCOPE.md` و`14/FINAL_STRATEGIC_REPORT.md` و`14/FIRST_SEASON_RECOMMENDATIONS.md`. توقفت عن تعديل 14 بعد ذلك. تحقّق أن تعديلاتي في 14 بقيت بعد آخر حفظ لهم.

### 5.5 قضايا في الملفات المحظور تعديلها (للتبليغ فقط)
1. **`00_PROJECT_CONTROL/RESEARCH_GAPS.md` G28:** «علاوة الرموز تصل إلى نحو 3× في مرمّز شائع (أرقام 2023)» — يحتاج قيد ≈1.2× (C1).
2. **`14/CORE_REFERENCES_V1.md` المرجع 44 (ATH-SRC-0969):** «فالعلاوة تصل إلى نحو 3× في مرمّز شائع» — كذلك.
3. **`14/OPEN_QUESTIONS_FOR_NEXT_PHASE.md` §8.2:** يُحال إليه كمصدر «مرحلة تحقق 6–9 أشهر»؛ يجب توحيده على 9–12.
4. **`13_CASE_DESIGN_REFERENCE/`:** لم يُعثر فيه على خرق سلامة أو «3×» أو مدد متعارضة. يشير `CASE_DESIGN_BIBLE.md` إلى أن «3×3» في ARC-18 لم تكن كلفة رموز.
5. **ATH-SRC-1908 في أي تركيب:** لم يستعمل أي ملف 14 نسبة Fanar-1 دليلاً على Gemma-2، فالأثر محصور في جدول القياس.

## 6. الحكم على الصلاحية (Fitness verdict)

**صالحة للاستعمال البحثي ولتصميم المنتج، مع ثلاثة شروط قبل التسليم v2:**
1. **إعادة الدمج:** تعديلات `sources_w2*.jsonl` لا تظهر في `sources_master.*` ولا في `athar_library.sqlite` حتى يُعاد تشغيل أداة الدمج.
2. **إغلاق التعارضات الثلاثة الباقية** في الملفات المحمية (5.5 البنود 1–3).
3. **الأصول:** فحص دفعي بطيء لتراخيص كل صور Commons خارج العينة (70 صورة، 60 منها CC BY/BY-SA) لأن Commons حجب الطلبات معظم الجلسة، فلم يُفحص منها إلا 3؛ واستبدال البريد الإلكتروني المقتطع في حقل `creator` لأربعة تسجيلات صوتية (AUD-0091/0106/0110/0118) باسم أو لقب، لأنه بيانات شخصية لطرف ثالث.

**المصادر:** لا اختلاق (0/77). خطأ جوهري واحد (1.3%، فترة Wilson 0.2%–7.0%) في استنتاج تقني، و10 أخطاء صغيرة أغلبها في حقول الوصول والحقوق، وكلها صُححت.
**الأصول:** 849/849 ملفاً موجوداً ومطابق البصمة. ولا ملف غير آمن في العينة (0/57؛ الحد الأعلى 6.3%). وخطأ ترخيص صياغي واحد (عائلة من 6 صور) صُحح دون حجر.
**الخطر الأكبر:** ليس الاختلاق، بل **الثقة الزائدة في الاستنتاجات التقنية والقانونية المشتقة** (بديل Gemma، و«صفر نتائج» لاسم بديل، وقاعدة المدة الأقصر لنصوص يابانية، و67 صورة Commons لم يُعَد فحصها)، و**تباعد ملفات الدفعة الأولى المحمية عن تصحيحات الدفعة الثانية**.
