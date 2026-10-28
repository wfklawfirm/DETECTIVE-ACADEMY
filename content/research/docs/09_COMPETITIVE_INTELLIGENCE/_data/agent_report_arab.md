# Agent report — 09A Competitive Intelligence (Arab/MENA)

Date: 2026-10-27 · Source block: ATH-SRC-1100…1199 (used 1100–1152) · KO code: 09A

## Counts
- Sources verified: **53** (`_data/sources_arab.jsonl`, all lines validated as JSON)
  - Evidence grades: A = 1 (Saudi MoE primary news), C = 42 (official product, store and organization pages), D = 10 (news, listicles, curated lists).
  - Relevance: high = 9, medium = 28, low = 16.
- Competitor and entity rows: **34** (`_data/competitors_arab.csv`). Every `source_ids` reference resolves to the catalog.
- Deep cards: **4** (ATH-SRC-1104 Circle of Suspicion, 1107 CrimeBot, 1120 Saudi critical-thinking course, 1131 PraxiLabs)
- Knowledge objects: **7** product opportunities (KO-PO-09A-001…007)

## Files produced
- `09_COMPETITIVE_INTELLIGENCE/ARAB_COMPETITOR_INTELLIGENCE.md`
- `09_COMPETITIVE_INTELLIGENCE/_data/sources_arab.jsonl`
- `09_COMPETITIVE_INTELLIGENCE/_data/competitors_arab.csv`
- `09_COMPETITIVE_INTELLIGENCE/_data/knowledge_objects_arab.jsonl`
- `09_COMPETITIVE_INTELLIGENCE/_data/agent_report_arab.md`
- `09_COMPETITIVE_INTELLIGENCE/cards/ATH-SRC-1104.md`, `ATH-SRC-1107.md`, `ATH-SRC-1120.md`, `ATH-SRC-1131.md`

## Search strategy
1. **Arabic searches in extended mode:** detective games, and boxed or paper case files.
2. **English searches:** publishers, Steam, escape rooms, EdTech incumbents, Saudi policy.
3. **Direct WebFetch** of about 70 official pages, store listings and Apple Podcasts genre pages. This step confirmed each record and captured prices and ratings with dates.
4. **Arabic availability of global detective games:** checked on Steam and App Store language tables (Obra Dinn, Disco Elysium, Golden Idol, Shadows of Doubt, Criminal Case, CrimeBot).

## Blockers
- **Shared WebSearch budget exhausted** after 13 successful searches by this team: 200 per turn, shared by all agents. No further searches were possible.
- **Shared WebFetch budget exhausted:** 800 per hour, shared by all agents. The last attempts were refused (Escape Hunt UAE page, PhET licensing, itch.io mystery tag, arabic.games).
- **Fetch refused (robots or site errors):** instagram.com/closedcase.sa, amazon.ae, kitabsawti.com, qatardebate.org, goviralgame.com, ekb.eg, abwaab.com, Duskwood App Store page.
- **Not reached at all because the budget ran out:**
  - Telco gaming and education platforms (stc, e&, Zain, Orange)
  - Classroom escape kits in Arabic
  - Arabic AI character and story apps beyond Humain and Jais
  - Saudi major studios (Savvy, Manga Productions)
  - Lebanese and Gulf podcast networks beyond Sowt, Kerning Cultures and Thmanyah
  - Egyptian Knowledge Bank simulations
  - Qatar Foundation programmes

## Unverified candidates (NOT in catalog)
| Candidate | Why not verified |
|---|---|
| Humain Chat / ALLaM (Saudi, PIF) | Only a Wikipedia page was confirmed; humain.com returned metadata only. The protocol allows Wikipedia only for bibliographic facts of works or games. Facts seen: PIF-owned, founded May 2025, Riyadh, free Arabic-first chat app. Needs an official page. |
| Jais LLM (Core42/G42, MBZUAI, Cerebras) | Wikipedia only (Aug 2023, Apache 2.0). Needs official model card. |
| PhET Arabic simulations and licence | Arabic page did not confirm translations; licensing page fetch blocked by budget. |
| Qadiyati (قضيتي) crime puzzle game | Only a third-party APK mirror found; no official store link. |
| "قضية مغلقة" closedcase.sa (Saudi case-file seller?) | Instagram fetch refused. |
| University Games "Murder Mystery Case Files" sold on Amazon.ae with Arabic listing | Amazon fetch refused; game content language unknown. |
| Escape Hunt country pages (UAE/QA/KW), detective rooms, school programmes | Budget exhausted. |
| Wattpad Arabic support | Homepage did not state supported languages. |
| Storytel Arabic mystery originals; Kitab Sawti | Landing page lacked category data; Kitab Sawti fetch refused. |
| QatarDebate (Qatar Foundation) | Fetch refused. |
| Abwaab product and pricing | Site fetch failed. Only Wamda news is cataloged. |
| Status of the Saudi critical-thinking course in 2026 | Only 2018–2019 sources were found. A 2022 Asharq Al-Awsat back-to-school article did not mention it. |
| Hill Agency: PURITYdecay; Detective – The Test; Yakuza: Like a Dragon | Surfaced in searches but are non-Arab or not relevant. Excluded. |

## Top 5 findings that should change ATHAR's design
1. **"First Arabic detective game / AI assistant / generated cases" is not a valid claim.** The following already exist:
   - Circle of Suspicion (Gemini hint assistant) [1104]
   - Case File 1000 [1106]
   - CrimeBot, fully Arabic-localized with generated cases and 1M+ Play installs [1107/1108]

   Positioning must rest on **reasoning assessment + evidence-linked science**.
2. **Every verified Arabic product checks only the final answer.** The mechanisms are barcode, limited attempts, hints or an "IQ" score. A structured argument screen with a published rubric is the main whitespace and must be in the MVP core loop.
3. **Policy hooks exist.** The Saudi MoE launched a Critical Thinking & Philosophy course for secondary schools (2018; 200 schools, 200+ teachers trained) [1120], and Jordan has a national MIL strategy with MoE as a partner [1135]. Arab EdTech incumbents show no reasoning content. Build class-length cases with teacher kits.
4. **Arab case-file buyers pay but get no feedback.** Prices run from SAR 19 (PDF) to LE 450 or MAD 209 per physical case [1100–1103]. A hybrid of print for groups plus an app for argument scoring is a later-stage opportunity. It is easy for these sellers to copy the answer-check part.
5. **Arabic crime and mystery audio is a strong attention competitor.** It takes 4 of the 7 top Saudi true-crime podcast slots [1140]. Teens' taste is being shaped toward real crimes, so ATHAR needs a compelling fictional, ethical alternative and could use audio trailers through partners such as Sowt [1138].

## Top 5 open questions / gaps for human or expert review
1. Status of the Saudi critical-thinking course in 2026: track, grade, syllabus, materials owner, and the procurement route for supplementary digital content.
2. Install and revenue share of CrimeBot and Criminal Case in Arab countries. This needs store-intelligence tools.
3. Is there an Arabic prebunking or misinformation game? Possibly a third-party adaptation of Bad News or Go Viral!. The official list shows none.
4. PraxiLabs: Arabic in-sim UI, forensics lab content accuracy, API/LTI licensing terms; PhET Arabic coverage and licence.
5. Telco and super-app distribution (stc, e&, Zain, Orange, Careem/Jahez kids sections) and Arabic AI-character apps were not researched because of the budget. A follow-up search pass is recommended.

## Gap-fill round (2026-10-27)

**Agent:** gap-filling researcher (second pass). **Method:**
- About 12 WebSearch calls, shared with the global pass.
- Store and data endpoints instead of the shared WebFetch quota:
  - Apple iTunes Search and Lookup API across the SA, AE, QA and EG storefronts, plus App Store listing pages for in-app purchase prices.
  - Steam `appdetails`, store pages and Arabic-filtered tag search.
  - Hugging Face model API and README files.
- Official pages fetched with curl.

Nothing was deleted. Updated rows had a source ID appended.

### Counts
- New sources: **27**, ATH-SRC-1153 … ATH-SRC-1179 (block 1180–1199 still free). All 80 IDs are contiguous, unique and valid JSON.
- New entity rows: **12**, COMP-A-035 … COMP-A-046. The CSV now has 46 rows; all have 24 columns and every reference resolves.
- Rows updated: COMP-A-014 Tamatem (+1176), COMP-A-018 Abwaab (+1179: grades 4–12, SAR prices, rating), COMP-A-028 Dubai escape rooms (+1178), COMP-A-033 Saudi critical-thinking course (+1177).
- New KO: **KO-PO-09A-008**, "Teen-safe, school-ready Arabic investigation in a market where Arabic AI-interrogation games already exist" (must, defensibility 3).

### Unverified candidates — resolution
| Candidate | Result |
|---|---|
| Humain Chat / ALLaM | **Verified**. humain.com is behind a Cloudflare challenge, so the official App Store listing (developer HUMAIN, support chat.humain.ai) and the SDAIA/HUMAIN Hugging Face model card were used instead → 1172, 1173 |
| Jais | **Verified**: official Inception42 Hugging Face card for Jais 3 (29 Sep 2026; Apache-2.0; 512K context) → 1174. Catalogued as AI infrastructure for Arabic characters. Fanar 2 (QCRI) added on the same basis → 1175 |
| PhET Arabic and licence | **Abandoned**: the licensing page is client-rendered and returned no text. Previously one failure, now two |
| Qadiyati (قضيتي) | **Resolved as not a game**: the App Store app with that name is a lawyers' case-management tool. No official detective game found |
| closedcase.sa | **Abandoned**: proxy 502 here, Instagram refused earlier |
| Amazon.ae Murder Mystery Case Files | Not retried (Amazon refused earlier) |
| Escape Hunt country pages | **Dubai verified** → 1178 (print-and-play murder mysteries; no school/Arabic offer seen). QA and KW not checked |
| Wattpad Arabic | **Resolved**: the SA App Store listing includes Arabic among 19 languages. Not catalogued as a separate record (low relevance) |
| Storytel Arabic originals; Kitab Sawti | Storytel iOS lists Arabic (19 languages); mystery originals not checked. Kitab Sawti has no matching App Store app; abandoned |
| QatarDebate | **Abandoned**: timeout here, refused earlier |
| Abwaab product/pricing | **Verified** via App Store → 1179 |
| Saudi critical-thinking course status | **Partly**: a 2021 Ajel report says it was added to intermediate and secondary curricula → 1177. A 2025 homework-help site references a first-secondary "Critical Thinking" textbook for 1447 AH (not catalogued; low-grade source). The 2026 timetable and owner are still unverified |

### Never-searched areas (task 2) — what was found
- **Telecom operators:**
  - Vodafone Qatar Shater: kids catalogue in Arabic and English with parental control, QR40 per month → 1162.
  - stc play: an esports social platform, not edutainment (TradeArabia; the stc product page returned 404) → 1163.
  - Zain Kuwait: Gizer esports via carrier billing (2022) → 1164.
  - **Not found or not verified:** e& (UAE), Ooredoo (Qatar/Kuwait) and Vodafone Egypt kids or edutainment platforms. One App Store search each returned only account apps; abandoned for budget. The Ooredoo Tunisia "Ooredoo EZ" gaming article timed out.
- **Arabic classroom escape kits:** only a 2025 Arabic AI-literacy escape kit for grades 1–3 from the Israeli Ministry of Education (1165, low relevance). No Gulf, Egyptian or Levantine school mystery kit was found. Gulf forensic camps and workshops were found instead: Dadu Qatar 2025 → 1166, Sharjah SCRF 2019 → 1167.
- **Arabic AI character and story apps:** the most important result of the round. A wave of Arabic or bilingual investigation apps launched July–October 2026: invsroom → 1155, BUSTED → 1156, المفتش فهلوي → 1157, القضية ٠٠١ → 1158, تهمة → 1159, Ultra Murdle → 1160 and Detective Files (SayGames, Arabic-localized) → 1161. On Steam, **Homicide Desk** (Iraqi studio Shu'la Lab, Sep 2026) has Arabic RTL, on-device LLM suspects bound to hand-written case facts, hands-on forensic puzzles and written deductions → 1153, 1154. Tamatem's Arabic choice-story app → 1176. Generic Arabic AI story apps for children (e.g., "AI Stories For Kids") were seen in search but not catalogued (generic, not mystery).
- **Saudi and Gulf studios and publishers:** Savvy Games Group (NGES champion) → 1168, Manga Productions (Arabic publishing of Nioh 3) → 1169, Ash Games ($1.5M seed; Azooma Escape) → 1170, 1171. None has a mystery or educational title. Semaphore's "Unearthed: Trail of Ibn Battuta" (older Saudi narrative game) was seen in search but not catalogued.

### Conclusions changed
1. **Crowding judgment**: "Arabic digital detective games" moves from **low** to **medium and rising fast**. There were seven launches in four months, four of them with free-text AI interrogation, but all have tiny user bases (0–94 reviews or ratings). The market is still early, but the **mechanics are commoditized**.
2. **Easy to copy vs takes years**: Arabic or dialect AI suspects, truth-bounded suspects, case-embedded forensic mini-lab UIs, contradiction confrontation and group rooms all move to **easy to copy**. Still hard: teen-safe reviewed case library, calibrated reasoning rubric, longitudinal learning data, scientific accuracy review, and school and parent trust.
3. **Positioning claim revised**: "first Arabic platform linking evidence to science" no longer holds (Homicide Desk). The remaining defensible claim is the teen- and school-designed Arabic investigation platform with published reasoning measurement (KO-PO-09A-008).
4. ARAB MD sections edited surgically: header, §1 items 3/3ب/6, §2 table and verdict, new §3.3ب and §3.3ج, §4 items 3/5/6, §5 rows, §6 rows 4/8 and the copy list, §7 log and §8 recs 2/2ب/2ج.

### Still open
- e&, Ooredoo and Vodafone Egypt kids platforms.
- Arabic school escape and mystery kits in Gulf, Egypt and Levant markets.
- Install figures (Google Play) for the 2026 Arabic AI-interrogation apps.
- Shu'la Lab team and funding.
- Saudi critical-thinking course status in 2026.
- PhET Arabic licence.
- Licence terms for ALLaM and Fanar (LICENSE files and Gemma base terms) before any commercial use, for team 10/11.
