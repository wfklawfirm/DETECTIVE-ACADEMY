# Agent report — W2-MEDIA-COMP (media references + competitor monitoring), 2026-10-27

## 1. Counts
- **Sources verified: 83**, IDs ATH-SRC-2000…2082. The sequence is contiguous and every ID is unique; IDs 2083–2099 are unused.
  - Media: **60** in `15_STORY_MEDIA_AND_ASSETS/_data/sources_w2_media.jsonl` (2000–2058, 2082).
  - Competitors: **23** in `09_COMPETITIVE_INTELLIGENCE/_data/sources_w2.jsonl` (2059–2081).
  - By grade: A 1, C 66, D 16. None is `needs_expert_review`.
- **Existing catalog IDs reused (not re-cataloged), 31:** 0116, 0118, 0136, 0138, 0139, 0143, 0183, 0737–0741, 0745, 0763–0766, 1107, 1131, 1136, 1138, 1141–1143, 1155–1159, 1551, 1552.
- **Media reference register:** `MEDIA_REFERENCE_REGISTER.csv`, 69 rows (MR-001…069). Every `source_id` resolves to the catalog.
- **Competitor rows appended (no existing rows changed):**
  - `competitors_arab.csv`: COMP-A-047…051 (Detective Dana; Fax; Wesh al-Salfa; telco kids offers; Dubai Police course).
  - `competitors_global.csv`: GC-066…072 (Case Mind; ColdTrace; Inquest; Detective AI; Chat of Deduction; Interrogation Room; Judge SIM 2).
  - Both CSVs keep 24 columns, and the original bytes are intact (checked with diff).
- **Knowledge objects: 9.**
  - 15M (6): KO-PO-15M-001…003 and KO-NP-15M-001…003.
  - 09B (3): KO-PO-09B-001…003.
  - Every `source_id` resolves.
- **Deep cards:** none. They were not requested in the brief, and the analysis sits in the two Markdown deliverables.

## 2. Files produced or touched
- New:
  - `15_STORY_MEDIA_AND_ASSETS/MEDIA_REFERENCE_REGISTER.csv`
  - `15_STORY_MEDIA_AND_ASSETS/MEDIA_AND_FORMAT_LESSONS.md` (Arabic, 20 lessons)
  - `09_COMPETITIVE_INTELLIGENCE/COMPETITOR_WATCHLIST_2026-10.md` (Arabic; changes, threat ranking, monthly protocol)
  - `15/_data/sources_w2_media.jsonl`, `15/_data/knowledge_objects_w2_media.jsonl`, `15/_data/agent_report_w2_media.md`
  - `09/_data/sources_w2.jsonl`, `09/_data/knowledge_objects_w2.jsonl`
- Appended: `09/_data/competitors_arab.csv`, `09/_data/competitors_global.csv`.
- Not touched: everything else. The W2-BUSINESS team writes `sources_w2_business.jsonl` in the same folder; there is no URL or ID overlap with it.

## 3. Method
- **Store and catalogue endpoints (curl, descriptive User-Agent, at least 1 s between requests):**
  - Apple iTunes Lookup/Search for apps and podcasts (SA, EG, AE, US).
  - Public RSS feeds for 20 podcasts (episode counts, median duration, date ranges computed with Python).
  - Netflix title pages, SA and US storefronts (maturity label, seasons, runtimes, subtitles).
  - BBFC release pages (`__NEXT_DATA__` JSON: classification and short-form insight).
  - Wikidata SPARQL (one batched query each for IDs, durations and episode counts; the REST entity API returned 429, so SPARQL was used).
  - Google Play listing and search pages (gl=SA).
  - Steam appdetails, store search and the ISteamNews API.
  - YouTube channel `/about` pages and channel RSS feeds.
  - Khan Academy Help Center JSON API, the PraxiLabs WordPress REST API, getbadnews.com, and Hidden Door HTML.
- **WebSearch, about 30 queries in Arabic and English, for discovery only.** WebFetch was used about 8 times where curl was blocked (Al-Fanar, Arabic Post, Arab News, Book Riot, Kuwait Times, The Bookseller).
- **Reuse.** The app-store snapshot (`08/_data/app_store_snapshot_2026-10-27.csv`) was used as the baseline for ratings, the podcast chart and Steam tags; we did not scrape it again. Visual references in `COPYRIGHTED_VISUAL_REFERENCES.csv` (CVR-11…14) were cross-linked, not duplicated.

## 4. Interpretations made autonomously (owner away)
1. **"Official age rating."** For streaming titles we recorded the **platform maturity label per storefront** (Netflix SA and US) plus the **BBFC** classification where one exists. National Gulf regulator ratings (GCAM, Saudi GCAM/GEA) were not available online and are not claimed.
2. **"The podcast now #1 in KSA/UAE/Kuwait"** is سوالف طريق, already cataloged as ATH-SRC-1552. We reused that ID and added its YouTube channel (ATH-SRC-2046) and feed statistics. We also catalogued جناية (#2 KSA) because its October 2026 switch to a game-show format is directly relevant.
3. **Copyright.** Link-only. No stills, logos, transcripts or plot text. At most one short direct quote per source; after an automated check, extra quotes were paraphrased.
4. **Competitor CSVs.** Only products that are genuinely new (not already a row) were appended. Re-checks of existing rows (Homicide Desk, invsroom and others) went into new *source* records, and the existing CSV rows were not edited (append-only rule).
5. **Wikipedia** was used only through Wikidata structured data, for durations and episode counts. Facts tied to ratings and claims came from official pages.

## 5. Blockers
- **Wikidata entity API:** HTTP 429. SPARQL worked.
- **Sites that refused or failed:**
  - praxilabs.com home (403 to curl and WebFetch); the WordPress API worked.
  - crankyuncle.com (expired TLS certificate; not bypassed).
  - goviralgame.com (connection error).
  - alkhaleej.ae (403 to curl and WebFetch).
  - Kuwait Times (502 to curl; WebFetch worked).
  - shulalab.com (client-rendered; no text).
  - The Bookseller article (paywalled summary only).
- **Content loaded by JavaScript:** YouTube `/videos` grids. Channel RSS feeds were used instead.
- **No Gulf regulator rating database** was reachable.
- **Spacetoon:** the first Arabic broadcast year of Detective Conan is still unverified (G22).

## 6. Unverified candidates (not cataloged)
| Candidate | Why not |
|---|---|
| Common Sense Media age for Only Murders (14+) | Seen only via a Romper article; CSM page not fetched. Noted in the limitations of 2003 |
| Holly Jackson "two million sales" (The Bookseller, May 2023) | Page fetched, but series and BookTok link not visible behind the paywall |
| Arabic BookTok sales articles (Akhbarona, SNRT, AUS Media Hub 2022) | Student or secondary pieces; the Arab News/TikTok figure (2057) was preferred |
| Shahid Ramadan 2026 crime series list (Al Ain), «عين سحرية» | Not fetched; outside the time budget |
| Zain Kids current (2026) status | Only the 2022 article was verified |
| Ooredoo kids platform | Only a 2020 Oman tutorial app was found; not cataloged as current |
| Hulu/Disney+ MENA availability of Only Murders, Death on the Nile | Not verified |
| millionpodcasts.com Arab fiction charts | Third-party aggregator; not an official source |
| vling/vidIQ statistics for Arabic YouTube channels | Third-party analytics; replaced by official YouTube about pages |
| Detective Conan first Spacetoon airing (areq.net, MyAnimeList stack) | Not authoritative |

## 7. Top 5 findings that should change ATHAR's design
1. **Audio "play-along" is proven in the Gulf.** جناية (#2 KSA) now runs episodes where guests compete to solve a crime card by card. Meanwhile سوالف طريق (#1 KSA/UAE/KW) is audio-first and simulcast to a 3.85M-subscriber YouTube channel. → An audio pilot with pause points and conclusion submission, released on podcast and YouTube at once (KO-PO-15M-001).
2. **Gulf storefront ratings run 1–2 bands stricter than US ratings for the same mystery titles.**
   - Wednesday, AGGGTM and Sherlock: 18+ in SA.
   - Glass Onion and Conan: 16+.
   - Enola Holmes 2: 18+, against 13+ for the first film.
   → A per-case content-descriptor policy using BBFC vocabulary (KO-PO-15M-002).
3. **Three-session case plus a season meta-mystery** is the current Arab streaming format (القصة الكاملة: 5 stories × 3 episodes) and the classic one (Conan, Sherlock & Co.) (KO-NP-15M-001).
4. **Mechanics are commodity, now in Arabic too.**
   - Case Mind: authored truth plus LLM voices, 10K+, Arabic.
   - Inquest: fair-play solver and confidence wager, Arabic.
   - Detective Dana: Arabic voiced contradiction mechanic.
   → Position on published measurement, teen safety and school trust (KO-PO-09B-002).
5. **The 2026 Arabic AI-interrogation wave is iOS-only and has no traction** (0–8 ratings; absent from Play search). Android-first Egypt and Morocco are unserved (KO-PO-09B-001). An Arabic Bad News already exists, so for prebunking ATHAR should partner rather than rebuild (KO-PO-09B-003).

## 8. Top 5 open questions or gaps
1. Gulf regulator ratings (GCAM, Saudi media regulator) for the reference titles, and whether platform labels map to them. Needs a lawyer (G02).
2. Listener and viewer age data for Arabic crime podcasts and YouTube. Needs platform partner data (Sowt, Podeo, Mics) (G30).
3. Shu'la Lab funding and team; whether the iOS-only Arabic apps have Android builds under other package names (G25).
4. The Arabic quality of Case Mind, ColdTrace and Inquest localisations. A hands-on review of 30 minutes each is needed.
5. Year Detective Conan's Arabic dub first aired on Spacetoon; an official Maspero archive entry for «أغرب القضايا» (G22).
