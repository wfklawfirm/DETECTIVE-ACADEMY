# Agent report — W2-PILOT-ETHICS (wave 2) — 2026-10-27

## Counts
- **Sources verified:** 52 new records in `07_LEARNING_SCIENCE/_data/sources_w2_pilot.jsonl`.
  - The ID block runs from ATH-SRC-2100 to 2153. **2104 and 2110 were removed as duplicates** (see Interpretations 1).
  - Evidence grades: A 13, B 19, C 18, D 2.
  - Language: en 45, ar 7.
  - Rights: COPYRIGHTED_RESTRICTED 22, UNKNOWN 19, OPEN_LICENSE 8, PUBLIC_DOMAIN 3.
  - Review status: 44 `verified`, 8 `needs_expert_review`. The 8 are 2102, 2111, 2113, 2115, 2120, 2123, 2125 and 2128.
- **Knowledge objects:** 7 in `_data/knowledge_objects_w2_pilot.jsonl`.
  - LA: KO-LA-07P-001 to 005.
  - PO: KO-PO-07P-001 and 002.
  - Status: 3 evidence_based, 3 design_hypothesis, 1 expert_practice.
- **Deep cards:** none written. The brief did not ask for them. `deep_card` is null in every record.
- **Validation:**
  - Both JSONL files parse.
  - IDs are unique and inside the block.
  - All enumerations match the protocol.
  - Every PUBLIC_DOMAIN record has a jurisdiction, and every OPEN_LICENSE record has a licence.
  - Every supports/conflicts reference and every KO `source_ids` entry resolves against the master catalogue plus all `*/_data/sources*.jsonl`.
  - Every ATH-SRC and KO citation in the 7 Markdown files resolves.
  - Every new record is cited at least once.
- **Reused, not re-catalogued:**
  - From wave 1 and W2-LEGAL: 1034, 1049, 1050, 1053, 1055, 1058, 1060, 1061, 1062, 1800, 1801, 1804, 1805, 1807, 1808, 1809, 1813, 0251, 0248 and 0437.
  - From W2-FORENSIC-AR: 1739 (SRCD), 1757 (Saudi research-ethics law, Arabic) and 1760 (CIOMS Arabic translation).

## Files produced (all new; no other team's files edited)
- `07_LEARNING_SCIENCE/PILOT_STUDY_ETHICS_AND_PERMISSIONS.md` (Arabic). Contents:
  - The research vs product-test definitions and decision table.
  - The unified minimum standard and 12 red lines.
  - Data minimisation, recording and retention rules.
  - A per-country permission path for each of the 3 experiments, for SA, AE, LB, JO, EG, KW and QA.
  - A revised timeline and open legal questions.
- `07_LEARNING_SCIENCE/TEEN_USER_RESEARCH_PLAYBOOK.md` (Arabic). Contents:
  - The safeguarding protocol and moderation in Arabic dialects.
  - Full session designs for Experiments 1–3.
  - Sample-size computations: Wilson CIs, a kappa simulation and TOST equivalence.
  - A day-of-session checklist.
- `07_LEARNING_SCIENCE/templates/` contains 5 bilingual drafts. Each is marked DRAFT and requires counsel and ethics-committee review:
  - `parental_consent_ar_en.md`
  - `teen_assent_ar_en.md`
  - `school_permission_request_ar_en.md`
  - `debrief_script_ar_en.md`
  - `data_handling_summary_ar_en.md`
- `_data/sources_w2_pilot.jsonl`, `_data/knowledge_objects_w2_pilot.jsonl` and this report.

## Search strategy
- **WebSearch** (about 45 queries, Arabic and English) to discover ministry services, ethics regulations and committee pages for the 7 countries, plus international codes and UX/GUR literature.
- **Official texts** read in full via curl/pdftotext:
  - The Saudi law and its 2016 implementing regulations (KSU-hosted English translation).
  - The Egypt Law 214/2020 English translation on the EDA site.
  - The Jordan PDPL official translation.
  - The BERA 2024 PDF.
  - The CIOMS 2016 full text (university-hosted copy).
  - The ESOMAR/GRBN 2018 guideline and the ICC/ESOMAR 2025 Code PDF.
  - The DHA DSREC checklist (docx).
  - The USJ school letter template (docx).
- **WebFetch** for:
  - WMA, eCFR (§46.102 and Subpart D), Belmont and the OHRP QI FAQ.
  - NN/g and Bentley UX pages.
  - The Saudi MoE Unaizah service, RAK DOK, Al Khaleej, AUB, QU, JUST and KU pages.
  - Retraction Watch, used for the PNAS expression of concern.
- **Metadata:** Crossref, OpenAlex (abstracts and OA licences) and PubMed / PMC E-utilities.
- **Within-team calculations:** Wilson CIs, problem-discovery curves, kappa Monte-Carlo (4,000 reps) and TOST sample sizes. The script is in the scratchpad (`pilot/ss.py`). These are team calculations, not sourced facts.

## Interpretations made (owner absent)
1. **Duplicates with W2-FORENSIC-AR.** Their `BIAS_LAB_ETHICS_FOR_MINORS.md` appeared mid-session.
   - SRCD 2021 was catalogued by both teams. I deleted my 2104 and re-pointed all citations to ATH-SRC-1739.
   - The Saudi research-ethics law was also catalogued by both. I deleted my 2110 (English translation) and re-pointed to ATH-SRC-1757 (Arabic official text). Its English article findings are kept in 2111 and in the Markdown.
   - IDs 2104 and 2110 are therefore unused gaps in the block.
2. **The 2016 Saudi regulations.** The current 3rd edition (25/9/1443H, 2022) exists per qanoniah.com, but it sits behind a login and the KAUST copy returned 404. I used the 2nd edition (2016) translation, marked the record `needs_expert_review`, and flagged that article numbers may differ.
3. **Research vs product test.** I adopted a 5-question gate built on 45 CFR 46.102, Belmont Part A and the OHRP QI FAQ, plus the Saudi definition, which is broader.
   - Experiments 1 and 2 are classed as research.
   - Experiment 3 is mixed. Teacher interviews are research, in-class play is educational practice, and the price offer is commercial and kept away from students.
   - Mixed activities default to research.
4. **Same-domain records.** The research exceptions in the Saudi and Jordanian PDPLs are catalogued as separate article-specific records (2114, 2129), even though the laws already exist as 1049 and 1058. The merge step may fold them in.
5. **Secondary sources.** The UAE MoE research service (2115) rests on an Al Khaleej report (grade D), because the official page was not found. The CAPMAS law (2120) rests on a parliamentary-news reproduction (grade D, low confidence). Both are flagged.
6. **Revised sample-size thresholds.** The kappa CI floor of 0.60, ≥100 double-coded sessions, and completion treated as descriptive are my proposals for a statistician to confirm. They are tagged `[افتراض تصميمي]`.
7. **Templates.** These are plain-language drafts with [●] placeholders. They make no legal claims beyond the sources, and each opens with a DRAFT banner and team notes to be deleted.

## Blockers
- **Access denied:**
  - Qatar MoPH research portal (research.moph.gov.qa).
  - The University of Jordan ethics page.
  - The Jordan MoE "كتاب تسهيل مهمة" page (robots disallowed).
  - The Jordan MoHE services guide (robots).
  - The PNAS page.
  - ACM DL pages.
- **Connection reset or other network failure:**
  - childethics.com (ERIC).
  - iau.edu.sa.
  - Kuwait MoE research portal (research.moe.edu.kw, empty reply).
  - fedu.bu.edu.eg.
  - qu.edu.qa static files (TLS hostname mismatch; not bypassed).
- **Other blockers:**
  - Europe PMC search returned 503.
  - The LBCI article URL was too long for WebFetch, and curl redirected to the homepage.
  - The UNICEF Innocenti ERIC page returned a client error.

## Unverified candidates (not catalogued)
- KHDA (Dubai) and ADEK (Abu Dhabi) procedures for external research in private schools. No official page was found. The KHDA "annual activities" service does not mention research.
- The Lebanese MEHE / Directorate General of Education rule on questionnaires or research in public schools. Search results point to a DG warning about unauthorised forms, but the text could not be read.
- The CAPMAS prior-approval requirement for questionnaires (Egypt). Field practice is widely reported, but no decision text was located.
- The Egypt Ministry of Education procedure for school research.
- The Qatar MOEHE school research procedure, and the current MoPH "Policies, Regulations and Guidelines for Research Involving Human Subjects" (PDF access denied).
- The Kuwait MoE research facilitation details (portal down).
- The Saudi NCBE regulations, 3rd edition (2022) text.
- The ERIC compendium full text (only the catalogue record was read).
- Lebanon MoPH Decision 1/141 (2016), known only via the HDF page.
- Egypt PM Decree 927/2022 (executive regulation of Law 214), identified but not read.
- Hanna, Risden & Alexander (1997), "Guidelines for usability testing with children" (Interactions 4(5), DOI 10.1145/264044.264045). Crossref confirmed it, but the content could not be read (ACM DL blocked, no abstract), so it was left out.
- Wendler et al. (2002), "The ethics of paying for children's participation in research" (J Pediatr 141:166-171). PubMed confirmed it but has no abstract, so it was not catalogued and CIOMS 13 is used instead.

## Top 5 findings that should change ATHAR's design or plan
1. **Experiments 1 and 2 are research, and no session with a minor may happen before ethics-committee approval.** Calling them "product tests" does not help.
   - School access in KSA, the UAE and RAK runs through a university or research institution in any case (2113, 2115, 2116).
   - The PNAS/Facebook case (2148) shows what happens to findings published from product-test data.
2. **A university partner in each pilot country is a hard prerequisite.** Start the ethics file in month 0.
   - The realistic lead time to the first session is 6–10 weeks in KSA and 10–14 weeks in UAE government schools.
   - MVP_SCOPE assumed "one week of recruitment and consents" (2131, 2150, 2115, 2113).
3. **Recruitment yield will be low.** Only 19.5% of Doha parents granted permission (2127). Experiment 2's 120–200 teens may require inviting 400–800 families, and the self-selection must be reported (KO-LA-07P-004).
4. **Experiment 2's statistics need revision.**
   - 40–60 double-coded sessions give a kappa CI too wide to support a ≥0.70 decision. Plan ≥100, and more for rare codes.
   - A completion-equivalence test needs about 275+ per arm, so completion should be reported descriptively.
   - Enjoyment equivalence (margin 0.5) needs about 70–110 per arm (2146; team calculations).
5. **The safeguarding and data rules are non-negotiable.**
   - Two adults are always present (2135).
   - The teen's own spoken "yes", and "no" is binding (1739, 2101, 2133).
   - Audio only, with separate consent, deleted after transcription (2106).
   - No cloud or AI transcription (2103 ¶46).
   - Disclosure limits are written into the forms. The UAE has a mandatory reporting duty (1055).
   - The Saudi law requires a benefit to the minor and a justification for not using adults (1757, 2111).

## Top 5 open questions for human or expert review
1. Saudi counsel and the partner REC: the 2022 regulation text. Does expedited review apply to a company-funded, university-run playtest? Is the Education Department letter needed for private schools?
2. UAE: the KHDA and ADEK procedures for external research in private schools, and the official MoE service rules.
3. Qatar: the Art. 16 permit for processing children's data in Experiment 2, and the current MoPH research policy scope for non-health studies.
4. Egypt and Kuwait: whether CAPMAS questionnaire approval and the Data Protection Center licence apply to a small pilot, and what the Kuwait MoE facilitation and instrument-review process requires.
5. Statistician and child-protection reviewer:
   - Confirm the kappa and equivalence plans and the SD assumptions.
   - Confirm same-gender moderator norms, local mandatory-reporting routes, and the incentive value per country.
