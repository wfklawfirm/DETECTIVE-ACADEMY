# Agent report — W2-HERITAGE (classical Arabic inference heritage) — 2026-10-27

## Counts
- **Sources verified:** 55 new records, ATH-SRC-1200 … 1254 (`_data/sources_w2_heritage.jsonl`, JSONL validated, schema enums checked). The catalog was checked first (`sources_master.jsonl` plus every team's `sources*.jsonl`); existing IDs reused where relevant: 0139, 0356, 0410, 0413, 0414, 0418, 0419, 0421, 0423, 0451, 0453, 0510, 0539, 0731, 0732, 1024.
  - Breakdown: 14 primary texts/digital editions (Arabic premodern texts and PD translations), 33 scholarly items (journal articles, monographs, EI2 entries), 8 other (web overviews, news, licence/dataset records).
- **Knowledge objects:** 18 (13 NP `KO-NP-02H-001…013`, 5 CD `KO-CD-02H-001…005`); every source_id resolves.
- **Story index:** 67 anecdotes (HS-001…HS-067). Locations verified in the stored OpenITI texts by page marker, or in Lang's PG text. 58/67 are V0–V1 and 37 are rated 13–15.
- **Deep cards:** none written (not requested in the brief; the overview carries the analysis).
- **Texts stored:** 14 files, about 29 MB total. Each has a manifest row in `99_LEGAL_SOURCE_ASSETS/ASSET_MANIFEST_W2_TEXTS.csv` (TXT-H-001…013; appended only) with its sha256.
  - `OPEN_LICENSE/arabic_heritage/` (CC BY-NC-SA 4.0, OpenITI; an ATTRIBUTION.txt sits in each folder): Akhbar al-Adhkiya', al-Turuq al-hukmiyya, Akhbar al-qudat, Kalila wa-Dimna (Bulaq 1936 base), Akhbar al-hamqa, Nihayat al-rutba, al-Faraj ba'd al-shidda, Kitab al-Manazir I–III, Kashf al-zunun, Subh al-a'sha, Ma'alim al-qurba (11 texts).
  - `PUBLIC_DOMAIN_VERIFIED/arabic_heritage/`: Lang's *Arabian Nights Entertainments* (PG #128, header kept), and Knatchbull's 1819 English *Kalila and Dimna* (IA OCR, PDM 1.0; includes the Dimna investigation chapter).

## Files produced
- `02_DETECTIVE_LITERATURE/ARABIC_CLASSICAL_INFERENCE_HERITAGE.md` (overview, typology table, limits, rights caveats, brand framing, HER-01…HER-20, season-1 picks, open questions)
- `15_STORY_MEDIA_AND_ASSETS/HERITAGE_STORY_INDEX.csv`
- `02_DETECTIVE_LITERATURE/_data/sources_w2_heritage.jsonl`, `knowledge_objects_w2_heritage.jsonl`, this report
- Stored texts and manifest rows as listed above

## Method
- **Discovery:** WebSearch in Arabic and English (extended mode for Arabic qiyafa/qara'in queries).
- **Bibliographic verification:** Crossref API (bibliographic queries plus DOI lookups; an EI2 DOI scan located the Firasa and Kiyafa entries), Open Library, Zenodo API, Internet Archive metadata API, publisher pages via WebFetch.
- **Primary-text verification:**
  - Downloaded the OpenITI 2025.1.9 metadata TSV from Zenodo and located each text's version URI and quality tags.
  - Fetched texts from raw.githubusercontent.com/OpenITI.
  - Searched them with a local script that reports chapter heading and `PageV..P..` marker. Every HS row's `location_in_work` comes from that script output or from reading the passage.
- **Licence checks:**
  - OpenITI licence (CC BY-NC-SA 4.0) confirmed on Zenodo and in the KITAB FAQ, which also says in-copyright editorial apparatus is removed.
  - I checked each file for footnote markers before storing. Nishwar and Hayawan still carried them, so they are cataloged as links only.

## Interpretations made while the owner was away
1. **Folder choice:** OpenITI files go in `OPEN_LICENSE/`, not `PUBLIC_DOMAIN_VERIFIED/`, as the brief directs for licensed digitizations.
   - The premodern text itself is PD, but the files are CC BY-NC-SA 4.0, so `commercial_reuse_permission: no`.
   - Commercial ATHAR text must be our own retelling, or re-keyed from a PD print.
2. **Ibn al-Haytham:** the Würzburg source page shows a CC BY-SA 4.0 badge, while OpenITI redistributes the file as NC. I applied the stricter NC terms.
3. **Rating rule:** `violence_level` and `teen_suitability` rate the **story as told in the source**, not the adapted case. V3 originals are therefore forced to 18+. The Hunchback is rated V2 (16–18) because in the Arabic text the man turns out to be alive.
4. **Huxley duplicate:** W2-WORLDLIT had already cataloged and stored Huxley's essay (ATH-SRC-1330, TXT-W-032). My ATH-SRC-1246 is marked as a duplicate pointing to 1330. ATH-SRC-1330 was not found in any `sources*.jsonl` on disk at write time, so it is not cited in KOs. **Merge step should keep 1330 and drop 1246.**
5. **Brand framing:** the recommendation is to ground ATHAR in *qiyafat al-athar* (trace reading) and explicitly avoid *qiyafat al-bashar* (lineage reading).
6. **HER numbering:** HER-01 continues the Atlas as principle 51. I did not edit the Atlas itself; another team owns it.

## Blockers
- Brill reference pages (EI2) refused WebFetch. The Firasa and Kiyafa entries are verified by DOI only; their authors and content are not checked.
- Arabic Wikisource API returned HTTP 429, so no Wikisource texts were checked.
- The GitHub API is restricted in this session; raw.githubusercontent works.
- Crossref throttled (429) intermittently; retried slowly.
- The GITenberg mirror has no Burton *Nights* under the tried names.
- The Hindawi Nights edition (in OpenITI) has an unestablished licence, so it is linked, not stored.
- The Mahdi-based OpenITI Nights file is uncorrected OCR, so it is not stored.
- De Sacy's 1816 IA OCR contains no Arabic text (French OCR only), so it is not stored.
- No open text of al-Kindi's cryptanalysis treatise or of Ibn al-Haytham's *al-Shukuk* was found; their HS rows rely on secondary sources and are marked medium confidence.

## Unverified candidates (not cataloged)
- Ibn al-Haytham, *al-Shukuk 'ala Batlamyus*, ed. Sabra & Shehaby (Cairo 1971): edition details not confirmed this session.
- Ibn al-Durayhim, *Miftah al-kunuz*; Ibn 'Adlan's cryptology treatise: known only via ATH-SRC-1224, no edition record checked.
- Tashkopruzade, *Miftah al-sa'ada* (source of the qiyafa taxonomy): the OpenITI text located is a different *Miftah al-sa'ada* (Zaydi).
- Jurji Zaydan, *'Ilm al-firasa al-hadith* (OpenITI/Hindawi): relevant for the history of modern physiognomy in Arabic, but its licence was not checked.
- Talmudic and *Lamentations Rabbah* versions of the lost-camel motif: mentioned on Wikipedia only.
- A full-text reading of Malti-Douglas 1988 (Arabica) and of Johansen 2002: paywalled; cited at title/venue level, confidence medium.
- R. P. Buckley's translation: the series detail "JSS Supplement 9" is recalled, not seen; flagged in the record.

## Top 5 findings that should change ATHAR's design
1. **Ibn Qayyim's double warning** (neglecting signs loses rights; relying on them alone causes injustice) is a native statement of ATHAR's core rule: a clue opens a question, corroboration closes it (HER-01).
2. **Firasa has two faces.** Inference from traces is usable; reading character from faces and bodies is pseudoscience. The tradition itself critiques the latter: Dimna mocks the eye-shape accusation, and Kashf al-zunun calls lineage-reading conjecture (HER-02).
3. **The heritage corpus is mostly non-violent property and document disputes** (87% V0/V1). It is ideal for 13–15 cases in "Dar al-Sijil", the souk and the lab. The strongest season-1 seeds are the coin mint date, the comb and wool, the seal and blank space, the castor-root records trail, the planted meat, the child judge, and the hisba tests.
4. **Provenance needs honesty.** The Three Apples is solved by confession and chance. Ali Cogia's earliest witness is Hanna Diyab's oral telling of 1709. The lost-camel story is a pan-Eurasian motif. "First detective story" marketing must be avoided, and each story should carry an origin label (HER-18).
5. **Many anecdotes rest on coerced confession, beating, public shaming, slavery or gendered inference.** These must be stripped or turned into critique (HER-07, §4). Story migration between judges is itself a ready-made source-criticism exercise (HER-08).

## Top 5 open questions for experts
1. **Lawyer:** is internal storage of CC BY-NC-SA OpenITI files acceptable for a company whose product will be commercial (research stage only)? What is the status of Sabra-edition-based transcriptions?
2. **Islamic-law historian:** the framing of al-Turuq al-hukmiyya without sectarian or "endorsement" readings, and the handling of Companion-era stories (Ali, Umar).
3. **Arabian Nights specialist:** the manuscript-layer check (Mahdi edition) for the Three Apples and the Hunchback before any "heritage" labelling.
4. **Forensic library (04):** the validity of inferring stature and sex from footprints (the Robbins scale in the Naif course) before it is used in a tracking level.
5. **Audience team (08):** test whether teens prefer a contemporary frame with light heritage references or an explicit qadi/muhtasib heritage frame.
