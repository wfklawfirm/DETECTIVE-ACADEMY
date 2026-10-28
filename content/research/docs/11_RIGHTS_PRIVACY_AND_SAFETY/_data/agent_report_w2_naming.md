# Agent report — W2-NAMING (wave 2)

Date: 2026-10-27 · Block: ATH-SRC-2500 … 2549 (used 2500–2528) · KO code 11N

> Preliminary name and trademark research for a product-naming decision, not legal advice. Every conclusion requires review by licensed counsel in each target jurisdiction.

## Counts

- **Sources:** 29 verified records in `_data/sources_w2_naming.jsonl` (ATH-SRC-2500–2528, sequential, no gaps).
  - Validated with python: 29 unique IDs, schema enums valid, no dangling cross-references.
  - Grades: A 5 · B 1 · C 13 · D 10.
  - Review status: 28 verified · 1 needs_expert_review (2526).
  - Existing record reused (not re-cataloged): ATH-SRC-1719 (Dubai Police crime-scene article, forensic team).
- **Knowledge objects:** 2 in `_data/knowledge_objects_w2_naming.jsonl`.
  - KO-PO-11N-001: distinctive brand name.
  - KO-PO-11N-002: non-affiliation and religious-sensitivity copy guardrails.
- **Deep cards:** none (not requested).
- **Trademark register:** 15 rows appended to `TRADEMARK_AND_LICENSE_REGISTER.csv` (33 → 48 data rows). The original 33 rows were left byte-identical (verified by diff).

## Files produced or edited

- **New:** `11_RIGHTS_PRIVACY_AND_SAFETY/NAME_CLEARANCE_ATHAR.md` (Arabic). Sections:
  - Findings.
  - The Dubai Police platform.
  - Usage map.
  - Database status.
  - Linguistic and religious notes.
  - Risk per jurisdiction.
  - Options with 12 screened alternatives.
  - Counsel steps.
  - Limits.
- **New:** `_data/sources_w2_naming.jsonl`, `_data/knowledge_objects_w2_naming.jsonl`, and this report.
- **Appended:** `TRADEMARK_AND_LICENSE_REGISTER.csv` (append only).

## Method (all searches on 2026-10-27)

All requests used the addendum User-Agent, with at least 1 s between requests to the same host.

**Discovery:** about 30 WebSearch calls and about 20 WebFetch calls. Topics:
- Dubai Police «أثر».
- UAE, KSA and Egypt uses.
- Trademark office procedures.
- Lexicon and hadith terminology.

**App stores:**
- Apple iTunes Search API:
  - Software in AE, SA, EG, KW, QA, JO and LB.
  - Queries: athar, أثر, athr, "athar game", "athar education", "athar mystery", "أثر لغز".
  - Podcasts in SA and EG.
  - Lookup of the Dubai Police developer catalogue.
- Google Play: search HTML (gl=AE, SA) and detail pages.
- Steam: storesearch API and appdetails.

**Trademarks:**
- **USPTO:** tmsearch JSON backend; wordmark, pseudo-mark, transliteration and translation fields; live/dead status.
- **WIPO Madrid Monitor:** select.jsp with the site's own LZ-compressed state.
  - Control queries validated the method: SHERLOCK and holder "conan" returned hits.
  - Arabic control queries (الجزيرة, دبي, المراعي) returned zero, so Arabic-script zeros there are **not** evidence of absence.

**Domains and handles:** a plain HTTPS GET of home pages, reading only the page title and description. No WHOIS or paid tools were used.

**Alternative names:**
- 26 candidates screened on Apple (AE+SA, Latin and Arabic).
- 16 candidate groups screened on USPTO and Madrid.
- About 18 .com/.app home pages checked.
- Google Play SA spot-checks for 8 names.

## Blockers

- **WIPO Global Brand Database:** ALTCHA proof-of-work challenge. Not bypassed.
- **TMview API and EUIPO eSearch:** empty reply from server.
- **UK IPO trade mark search:** CAPTCHA "security check". Not bypassed. This matters for checking Siraaj Studios.
- **SAIP ipsearch.saip.gov.sa:** robots disallowed (WebFetch), and the connection was reset to curl. Not retried.
- **UAE Ministry of Economy:** the moet.gov.ae and moec.gov.ae portals timed out. The official search is a paid AED 350 inquiry.
- **uaelegislation.gov.ae:** returned 403. The English text of Decree-Law 36/2021 was read from FAOLEX instead (PDF stored in the scratchpad only, not in the library).
- **Egypt ITDA:** no public trademark search found.
- **Wikisource:** 429 (rate limit). **OpenAlex:** daily budget exhausted.
- **Instagram:** 429. Handle availability for @athar is not determined.

## Unverified candidates (not cataloged)

- **"Athar" non-profit, Rusifeh, Jordan:** VRScout article on VR employment education; Mercy Corps sub-grantee. The article has no date and current activity was not verified.
- **Dubai Police primary page for «أثر»:** none found. Coverage comes only from the press.
- **Siraaj Studios LTD:** company registration (Companies House) and any UK or EU trademark filing were not checked, because the UK IPO is CAPTCHA-blocked.
- **ATHAR EDUCATIONAL LLC:** jurisdiction and filings unknown.
- **Atharism:** a Wikipedia REST summary was read, but the record was dropped because it is outside the protocol's allowed Wikipedia use. A scholarly reference (Abrahamov, ATH-SRC-2526) is cataloged instead at catalog level.
- **Muqaddimat Ibn al-Salah, Nawa' 7:** the Wikisource page could not be fetched. The Khurasani athar/hadith distinction is sourced from a modern commentary (ATH-SRC-2525) instead.
- **Current Nice Classification edition (NCL 13-202x):** the WIPO page did not render. The memo therefore does not state an edition.

## Top 5 findings that should change ATHAR's design

1. **Do not launch with bare «أثر/ATHAR» as the brand.**
   - A UK studio's mobile game "Athar: Echoes of Time" (Siraaj Studios, 14 Aug 2026) already markets "ATHAR" in at least 7 Arab-relevant storefronts. It has the same product type and an overlapping audience [2504].
2. **Dubai Police's «أثر» is an internal forensic evidence platform, not a consumer product.**
   - It dates from GITEX 2022 and is still named in Oct 2026 [2500][2501][2502].
   - The risk for a forensic-mystery «أثر» in the UAE is perceived affiliation with a security authority and possible Art. 3(3) issues, rather than a store clash.
3. **The word is crowded and descriptive.**
   - At least 36 Athar apps exist, 22 of them religious [2503].
   - Other users include AUC's ATHAR teacher hub (cl.41-type, Egypt) [2515], Cairo University [2516], the Saudi Athar Festival [2517], Athr Gallery [2518], and Abu Dhabi's Athar+ [2519].
   - The Athr spelling is not a cleaner alternative.
4. **The public registers are clean, but the Arab registers are unknown.**
   - USPTO and Madrid show no live ATHAR mark for software, games or entertainment. The nearest is THE ATHAR FOUNDATION (US Reg. 6775046, cl.41 education) [2507][2508].
   - The UAE, KSA and Egypt registers, the decisive ones, were not searchable [2511][2513][2514].
5. **Cleaner alternatives exist.**
   - «قيافة» (Qiyafa) and «مقتفي الأثر» (Muqtafi) had zero app, USPTO and Madrid hits, and their .com domains are parked or for sale [2527].
   - Recommended path: a distinctive main brand, with «الأثر» kept as in-product vocabulary.
   - Also add a marketing copy guardrail on hadith connotations and the "Athari" label [2524][2525][2526].

## Top 5 open questions for counsel or experts

1. **UAE MoE paid inquiry (AED 350):** are there any filings for «أثر»/ATHAR, or for the chosen alternative, in classes 9/16/28/35/38/41/42? Do Dubai Police, Ma'an or Atharcom FZC hold marks?
2. **Siraaj Studios:** does it have a UK, EU or other filing? What is the strength of its prior use in Arab markets? Is there passing-off risk?
3. **UAE Decree-Law 36/2021:** do Art. 3(3) (State/institution symbols) and 3(5) (religious symbols) apply to «أثر» given the Dubai Police platform and the hadith sense? Review the official Arabic text and the executive regulation.
4. **KSA and Egypt:** manual SAIP search, and a check of the EAIP/ITDA register by a local agent.
5. **Religious-scholar review:** does a detective game named «أثر», or the alternatives, raise sensitivities in Gulf markets? Does Qiyafa's lineage-determination heritage create any issue for teen marketing?
