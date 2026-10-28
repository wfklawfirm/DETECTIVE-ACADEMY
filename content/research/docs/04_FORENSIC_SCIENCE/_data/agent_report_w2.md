# Agent report — W2-FORENSIC-AR (wave 2, Library 04)

Date: 2026-10-27 · Team block: ATH-SRC-1700…1799 (used 1700–1764) · KO code: 04B · Gaps: G05 (Arabic glossary, Arab institutions), G16 (bias-lab ethics for minors), G23 support.

## Counts

- **Sources verified:** 65 new records (ATH-SRC-1700…1764).
  - 55 `verified` and 10 `needs_expert_review`.
  - Grades: A 11 / B 25 / C 22 / D 7.
  - Languages: 24 Arabic-language, 39 English, 2 multilingual.
- **Reused existing IDs (not re-catalogued):** 57.
  - Wave-1 forensic: 0300–0358.
  - 04xx/05xx/06xx/07xx: 0400, 0409, 0425, 0517, 0518, 0523, 0560, 0645, 0726, 0784.
  - W2-LEGAL: 1820–1830.
- **Knowledge objects:** 11.
  - 8 FC: KO-FC-04B-001…008.
  - 3 LA: KO-LA-04B-001…003.
- **Glossary:** 248 terms.
  - Sourced: 170 total, made of 131 `sourced` and 39 `sourced-variant`.
  - `proposed`: 78 (no authoritative Arabic source found).
  - By source tier: 155 tier-1 official (UN/WHO/INTERPOL/legal), 7 tier-2 Arab academic, 8 tier-3 institutional usage.
- **Deep cards:** none written. Not required by the brief; deep_card = null.

## Files produced / changed (only my files)

- `04_FORENSIC_SCIENCE/_data/sources_w2.jsonl` (65 lines, validated)
- `04_FORENSIC_SCIENCE/_data/knowledge_objects_w2.jsonl` (11 lines, validated)
- `04_FORENSIC_SCIENCE/_data/agent_report_w2.md` (this file)
- `04_FORENSIC_SCIENCE/ARABIC_FORENSIC_GLOSSARY.md` (method, 5 terminology decisions, regional table, open questions, 248-row table)
- `04_FORENSIC_SCIENCE/arabic_forensic_glossary.csv`
  - Encoding: UTF-8 with BOM, for Excel.
  - Columns: term_id, term_en, term_ar, alternatives_ar, definition_ar, discipline, teen_level, status, source_ids, source_tier, concept_source_ids, usage_note_ar.
- `04_FORENSIC_SCIENCE/ARAB_FORENSIC_INSTITUTIONS_AND_EDUCATION.md`
- `04_FORENSIC_SCIENCE/BIAS_LAB_ETHICS_FOR_MINORS.md`
- `04_FORENSIC_SCIENCE/SAFE_VIRTUAL_LABS_CATALOG.md`
  - Appended section "## إضافة الدفعة الثانية" only.
  - Nothing above it was changed.

## Method

- **Discovery:** WebSearch in Arabic and English.
- **Verification sources:** Crossref API (AJFSFM ISSN 1658-6794 full list, 291 works scanned), PubMed E-utilities, publisher and official pages via WebFetch.
- **Terminology was harvested programmatically from three authoritative databases:**
  - **UNODC Arabic QA glossary PDF** (ST/NAR/26/Rev.1). The text is legacy font-encoded; extracted with pdftotext and read manually.
  - **WHO-EMRO Unified Medical Dictionary search endpoint** (~230 queries). Each entry carries a "موحد" flag and regional notes.
  - **UNTERM public search API** (~190 queries). Records show validation status and the contributing UN body.
- **Rate limits:** ≥1–3 s between requests; Crossref returned 429 several times and was retried slowly.
- **Downloads:** saved in the scratchpad only. Nothing stored in 99_LEGAL_SOURCE_ASSETS. All relevant PDFs are copyrighted or not clearly licensed.

## Interpretations made while the owner was away

1. **"Authoritative Arabic source":** read as UN/WHO/INTERPOL Arabic texts, official Arab legal texts, the NAUSS regional journal, and Arab institutional usage.
   - The glossary records which tier applies to each term.
   - "Proposed" = no Arabic attestation found in these sources, not "wrong".
2. **ALECSO / Arabization Bureau:**
   - The official list of 42 unified dictionaries (to 2015) contains no forensic or forensic-medicine dictionary.
   - The bureau's term bank was not searchable by script.
   - Recorded as a negative finding, not as a source record.
3. **Glossary size:** a 272-term draft was trimmed to 248 to stay within the 150–250 brief, dropping narrow lab-chemistry/statistics terms.
4. **Wave-1 terminology errors** (LR = «نسبة الأرجحية»; «سلسلة الحيازة»):
   - Flagged with a replacement list.
   - **Not edited in wave-1 files**, which are outside my file set.
5. **Bias-lab ethics:** ATHAR is not research, but I applied the stricter research standards (APA/SRCD/BPS) by analogy and designed three grades.
   - (A) transparent.
   - (B) authorized surprise.
   - (C) classic deception, deferred to 18+ after season 1.
6. **Jordan:** the brief's "National Institute of Forensic Medicine" is called **National Forensic Medicine Center** in official Petra/MoH sources; used that name.

## Blockers

- **NAUSS journal site (journals.nauss.edu.sa):** returned 404 to curl and to most DOI landing pages.
  - Two PDFs were read through WebFetch.
  - Arabic abstracts/keywords of AJFSFM LR/interpretation papers (1716, 1717) could not be read.
- **Saudi Bureau of Experts (laws.boe.gov.sa):** robots-blocked. Read a university-hosted copy instead (1757).
- **QCC Abu Dhabi PDF (ISO 17025 Arabic):** connection reset to curl; read via WebFetch only.
- **UNODC ST/NAR/39 Arabic** ("crime scene awareness for non-forensic personnel"):
  - Its existence is confirmed by catalogue (1763).
  - No Arabic file link was found on unodc.org or the UN Digital Library.
- **OHCHR Arabic Minnesota Protocol PDF:** downloaded, but text extraction is garbled (font encoding). Not catalogued.
- **Lebanon:** no official public page describing the ISF forensic laboratory or its accreditation.

## Unverified candidates (not in sources_w2.jsonl)

| Candidate | Why not verified |
|---|---|
| UNODC Arabic "Crime scene and physical evidence awareness" full text | Catalogue only (kept as 1763 with needs_expert_review); file not found |
| Minnesota Protocol (2016), Arabic (OHCHR HR/PUB/17/4) | PDF obtained but unreadable text layer; not used |
| ALECSO unified term bank entries for الإحصاء/علم الوراثة/القانون | Bank not machine-searchable; dictionaries are print/priced |
| INTERPOL Arabic fact sheet "تحديد البصمة الوراثية" (2015) | Seen and read, but superseded by web page 1703; not catalogued separately |
| UNODC "Guide for the development of forensic document examination capacity" (ST/NAR/42) Arabic | UNODC page lists Arabic; UN DL lists English only; UNTERM gives Arabic title; no file |
| Saudi Public Security forensic-evidence department official page | Not found in session |
| Egyptian EGAC accreditation scopes for Forensic Medicine Authority | Only press (1722); register not checked |
| BERA 2024, ERIC compendium, CIOMS English | Catalogued concurrently by the 07 pilot team (2101–2103) — cite those IDs |

## Concurrency / duplicates (for the merge step)

- **ATH-SRC-1739 (SRCD 2021) duplicates ATH-SRC-2104** (07 pilot team, same URL), catalogued concurrently after my pre-check. Merge should alias.
- **ATH-SRC-1757** (Saudi research-ethics law, Arabic text) is a related edition of **2110/2111** (official English translation and regulations, 07 pilot).
- **ATH-SRC-1760** (CIOMS Arabic translation) is a related edition of **2101** (CIOMS English).
- **ATH-SRC-0313** (ISO 17025 English) vs **1704** (Arabic translation): separate editions, linked via `supports`.

## Top 5 findings that should change ATHAR's design

1. **"نسبة الأرجحية" is the unified Arabic term for *odds ratio*, not for *likelihood ratio*.** The LR is «نسبة الترجيح» in the WHO Unified Medical Dictionary [1701]. Wave-1 files use the wrong term in ≥15 places. Fix before any Arabic UI ships.
2. **Arabic handwriting has no measured examiner error rates.**
   - What exists: regional class characteristics (4-country PhD, overlapping groups) and two 4-examiner signature pilots [1734–1736].
   - Lab #6 must not show Latin black-box rates as Arabic.
   - An Arabic version should teach class characteristics with fictional regions only.
3. **Bias labs are ethically acceptable for minors only in "transparent" or "authorized surprise" form, with a process debrief and a competence-restoring LSU round.**
   - Debriefing often fails to undo ego-threat and ostracism effects [1745–1747].
   - Adolescents are highly sensitive to social evaluation [1754].
   - So: no false self-feedback, no exclusion, no public "who was fooled", and one surprise lab per unit at most.
   - Default for 13–15 is the transparent version unless a parent or teacher opts in.
4. **Three institutional models exist in the region.**
   - Police labs: UAE, Jordan, Morocco, Kuwait.
   - Ministry of Justice forensic medicine and forgery: Egypt, Lebanon in a different form.
   - Ministry of Health forensic medicine and toxicology: KSA and Jordan (Iraq likely, not explicitly sourced).
   - Accreditation splits into ISO/IEC 17025 (labs) and ISO/IEC 17020 + ILAC G19 (scene and forensic-medicine units).
   - Stories set in a named country must route evidence correctly; otherwise use the composite city.
5. **Arab professional bodies themselves say terminology and region-wide accreditation are not yet unified** [1707, 1708]. A NAUSS/ASFSFM terminology workshop is both necessary and a credible partnership entry point. Pair each police-affiliated reviewer with a university reviewer.

## Top 5 open questions / gaps for human or expert review

1. **Terminology workshop (NAUSS/AJFSFM)** should rule on:
   - The 78 proposed terms.
   - The ENFSI verbal scale in Arabic.
   - proposition vs hypothesis.
   - «المضاهاة».
   - Fingerprint pattern names (طراز/نمط; منحدر/مستدير unverified).
   - «الإيضاح اللاحق» for debriefing.
2. **Lebanon:** structure and accreditation of the ISF forensic laboratory, and how forensic doctors are appointed (MoJ directory exists, rules not described). The owner, a Lebanese lawyer, is best placed to ask the MoJ/Bar.
3. **Child-protection reviewer + Arab university ethics committee:**
   - Is parental opt-in for grade-B labs at 13–15 the right default?
   - When does product analytics become "research" under KSA/UAE/Lebanese rules [1757]?
4. **Arab parents' acceptance** of "temporarily hidden information" wording: untested; refer to 08 for a small parent survey.
5. **Naming:** Dubai Police runs a forensic digital platform named «أثر» [1719]. Refer to team 11 for a trademark/confusion check.
