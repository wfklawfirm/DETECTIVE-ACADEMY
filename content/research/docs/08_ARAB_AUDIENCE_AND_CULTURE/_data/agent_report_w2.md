# Agent Report — W2-AUDIENCE (08_ARAB_AUDIENCE_AND_CULTURE, wave 2)

**Date:** 2026-10-27 · **ID block:** ATH-SRC-1500 … 1599 (used 1500–1559, contiguous; 1560–1599 free) · **KO code:** 08B

## Counts

| Item | Count |
|---|---|
| New verified source records (`sources_w2.jsonl`) | **60**: 56 `verified` and 4 `needs_expert_review` (1510, 1527, 1536, 1543) |
| Evidence grades | A 3 · B 9 · C 24 · D 23 · E 1 (1543, kept only to document a conflicting number) |
| Types | 29 news, 7 journal, 6 report, 6 website, 5 dataset, 2 conference, 2 market report, 1 guideline, 1 book chapter, 1 thesis |
| Languages | en 48 · ar 9 · fr 3 |
| Knowledge objects (`knowledge_objects_w2.jsonl`) | **8**: 6 PO, 1 NP, 1 CD. 2 of them (NP, CD) are `design_hypothesis` |
| Dated store snapshot | `_data/app_store_snapshot_2026-10-27.csv`: **3,259 rows**. Apple App Store 2,627 (54 queries, 623 unique apps); Apple Podcasts top-100 charts 600 (6 storefronts); Google Play 20; Steam 12 (11 tags plus a baseline) |
| Deep cards | 0. Not requested in the brief; the analysis lives in `DEMAND_AND_MARKET_EVIDENCE.md` |

## Files produced or edited (only this team's files)

- NEW `08_ARAB_AUDIENCE_AND_CULTURE/DEMAND_AND_MARKET_EVIDENCE.md` (Arabic; G08/G09/G10/G17/G26, demand verdict, bottom-up sizing method, data to buy)
- NEW `08_ARAB_AUDIENCE_AND_CULTURE/_data/sources_w2.jsonl`, `_data/knowledge_objects_w2.jsonl`, `_data/agent_report_w2.md`, `_data/app_store_snapshot_2026-10-27.csv`
- APPENDED a section `## إضافة الدفعة الثانية` to `ARAB_AUDIENCE_RESEARCH.md` (an update table for §8 plus 4 revised conclusions) and to `ARABIC_LANGUAGE_AND_DIALECT_STRATEGY.md` (diglossia in teens, BAREC replaces the 20-word rule, dubbing evidence, voice-pack decision). Existing text was not altered.

## Validation

- All JSONL lines parse. Every enum matches the protocol. The OPEN_LICENSE and PUBLIC_DOMAIN fields are complete.
- Every `supports`, `conflicts_with` and KO `source_ids` reference exists in the master catalog or a w2 file.
- Every `[ATH-SRC-…]` cited in the three Markdown files exists, and all 60 new records are cited at least once.
- The duplicate check against `sources_master.jsonl` and the other `sources*w2*.jsonl` files (by title, URL and DOI) found 3 items that were caught and fixed:
  - Ajel 2021 duplicated 1177. The record was removed and 1177 is cited instead.
  - GSMA MENA 2025 duplicated 0975. The record was removed and 0975 is cited instead.
  - The Steam tag record shared a URL with 0893. It was re-pointed to the baseline URL and marked as extending 0893.
  - ID 1554 was reused for the next new record, so the block stays contiguous.

## Method

- **Store data:** curl calls to the iTunes Search API (country=sa/ae/eg/kw/jo/ma, entity=software, limit=50, 1.5 s spacing); iTunes legacy RSS `toppodcasts` (chart dated 2026-10-26); Steam `search/results` `total_count` with and without `supportedlang=arabic`; public Google Play listing HTML (gl=SA) for install bands. The scripts are in the session scratchpad (/tmp/claude-0/-home-claude/2ded373e-5136-57b6-b445-94edef16b335/scratchpad/w2aud/: apple_snapshot.py, build_csv.py, build_csv2.py, steam_counts.py, gplay.py) and are described in the CSV `method_note` column so the run can be repeated monthly.
- **Official statistics:**
  - CST *Saudi Internet 2024*: PDF downloaded, text extracted, and chart pages read as images.
  - Jordan MoDEE/DoS *Household ICT Survey 2024*: 195-page analytical PDF.
  - UNESCO UIS public data API (indicators 20064/20070, Feb 2026 release).
  - Saudi MoE pages (Madrasati, Etimad).
- **Academic records:** Crossref API (9 DOIs) and PubMed/PMC E-utilities, including the full text of the Saudi national gaming study, read via XML because the PMC page is behind reCAPTCHA.
- **Discovery:** about 45 WebSearch queries in Arabic and English (extended mode for niche queries) and about 60 WebFetch calls. OpenAlex was not used (over quota).

## Interpretations recorded (owner away)

1. "Demand verdict" is split into five sub-hypotheses because a single verdict hides the key distinction. Appetite for Arabic crime/mystery *narrative* is **supported**. Demand for Arabic mystery *games* is **weak**. Teen (13–17) demand specifically is **unknown**. The overall verdict on the central thesis is **weak**, which I read as "untested", not "absent".
2. App-store rating counts are treated as a weak proxy and never converted into download estimates.
3. "Mystery/detective" classification in the CSV is keyword-based (`heuristic_category`). Totals are deduplicated per storefront. A double-count of one Arabic title (initially 1,730) was found and corrected to 865 in all files.
4. The UIS licence was not verified, so record 1511 has rights `UNKNOWN`.
5. The bottom-up sizing section gives the **method plus verified inputs and unit arithmetic only**. No conversion rates or market totals were invented.

## Blockers

- **YouTube** channel pages render through JavaScript. Third-party stats sites (vidIQ, Social Blade, vling) do not meet the "official page or reputable press" bar, so **no YouTube channel metrics were recorded**.
- **Springer** link pages returned a client error, and **PMC** pages are behind reCAPTCHA (the E-utilities API worked). **DOAJ article pages** failed. The **WAM** article pages returned only site metadata.
- **GASTAT** publication PDFs (Household Culture & Entertainment 2023) return 404. Only press coverage of the 2024/2025 reading indicators is available.
- **Apple's new marketing RSS** (`rss.applemarketingtools.com`) returned empty bodies. The legacy iTunes RSS worked.
- **Newzoo and PwC Outlook** regional figures are behind paywalls or not on free pages. Only secondary press coverage exists (Savvy and PwC esports via Arab News).
- **Saudi Critical Thinking official learning outcomes or textbook:** only pirate and homework-aggregator sites host the textbook PDFs. These were **deliberately not used** (protocol: no piracy sites). iEN was not reachable via search.

## Unverified candidates (not catalogued)

| Candidate | Why |
|---|---|
| Arabic YouTube mystery and true-crime channels (e.g., the channel "محمد رشدي - المحقق" surfaced via vidIQ) | Only third-party analytics pages; YouTube page is JavaScript-only |
| Saudi CT textbook 1447 (grade 9) contents and units | Only available on unofficial homework/PDF sites (not used) |
| Newzoo MENA 2025 report; PwC Global E&M Outlook 2025–2029 ME figures | Paywalled; Khaleej Times story cites an unnamed study (catalogued as grade E for conflict documentation only) |
| GASTAT Household Culture & Entertainment full bulletin (gaming and reading by age) | PDF 404; landing page has no data |
| Morocco ANRT ICT survey 2023/2024 (youth and gaming tables) | data.gov.ma XLSX found (ODbL) but not downloaded or read; press coverage only for 2017 data |
| QRF full diglossia policy report (title/year) | Only the blog summary was located |
| Enterprise Egypt "100+ true-crime podcast episodes" (2023) | Article body not retrieved |
| Spotify Wrapped 2025 MENA podcast lists | Campaign ME coverage lists music only |
| Saudi "Prevalence of social media disorder and internet gaming disorder among high school students" (national school-based, 2026) | Seen only on ResearchGate; not verified at the publisher |
| ITU Arab States 15–24 internet-use figure | Not on fetched ITU pages (2022, 2024) |
| Egypt NCSCR 2024 report ("half of under-18s on social media") | Cited second-hand via Egyptian Streets/ABC; primary not found |

## Top 5 findings that should change ATHAR's design or business plan

1. **The strongest demand signal is audio, not games.** An Arabic story-led true-crime podcast is #1 overall on Apple Podcasts in Saudi Arabia, the UAE and Kuwait, and #2 in Jordan [1551]. Arabic mystery apps have near-zero traction: the largest has 865 ratings across six storefronts, against 373k for an Arabic word game in Saudi Arabia alone [1500]. Test demand with fictional-case audio episodes before building the full app.
2. **Saudi teens are console-first.** Among 10–19-year-olds, PlayStation is the top gaming platform at 54.8% [1503]. In a national school survey, adventure (42%) beats puzzle (27%) [1554]. Position ATHAR as a narrative adventure with deduction, with short phone sessions.
3. **The B2G route is concrete but gated.** Critical Thinking is taught 2 periods a week in grade 9 [1553], to about 1.57M intermediate students [1556]. Madrasati has a Games Room and an enrichment bank [1512]. However, Etimad tenders require a Saudi RHQ (since 2024) [1514], and in the UAE one incumbent covers 100% of public Cycle 2/3 schools [1515]. The realistic route is a local partner or a content partnership.
4. **The Arabic "language problem" is about quality, not language.** In the 2025 Ipsos survey, 71% of 18–25s prefer Arabic media but 67% find it dated [1532]. MSA decoding cost largely fades after primary school [1526]. Use BAREC for readability targets [1524], with an Egyptian voice pack first, following Disney's dual-register path [1530].
5. **Parents' fears are sexual content, violence and strangers, not mystery itself,** but regulators are tightening (Egypt 2026, Jordan and Iraq PUBG bans, Morocco CESE) [1555] [1539] [1548]. Never market ATHAR as a "crime game". Frame it as reasoning and verification skills, with consequences shown.

## Top 5 open questions or gaps for human review

1. Real conversion data: run a fake-door test and a pilot audio episode. Without these, G26 cannot be sized.
2. Buy or trial a store-intelligence tool, and the Niko and Newzoo age×genre reports.
3. Saudi Critical Thinking official outcomes, the 1448H plan, and how third parties enter the Madrasati enrichment bank. This needs a formal MoE request and a search of closed tenders on Etimad.
4. Parents' attitudes toward *fictional* crime/mystery content specifically, and the teen MSA/dialect A/B/C test. Both require focus groups.
5. Representative 13–17 data for Egypt and Morocco (time use, genres). These may be obtainable from the ANRT XLSX (ODbL) and from national reports of Disrupting Harm or NCCM when published.

## Notes for the merge step

- 1502 extends 0893 (Steam). 1541 relates to 1168 (Savvy annual report, 09A). 1515–1517 relate to 1121/1122 (Alef, 09A). 1554 is the Saudi national school gaming study (owner: 08B; possibly also 06/11). 1511 (UIS) and 1556 (Saudi MoE counts) are sizing inputs for library 14 synthesis.
- The `app_store_snapshot_2026-10-27.csv` should be re-run monthly with the same parameters (09A recommendation 2c).
