# Agent report — W2-LEARN-AI (wave 2) — 2026-10-27

## Counts
- **Sources verified:** 69 new records, ATH-SRC-1600 … ATH-SRC-1668 (`07_LEARNING_SCIENCE/_data/sources_w2.jsonl`). All `review_status: verified`.
  - Evidence grades: A = 4, B = 39, C = 20, D = 6.
  - Language: 61 English, 8 Arabic.
  - Rights: 32 OPEN_LICENSE, 20 UNKNOWN, 17 COPYRIGHTED_RESTRICTED.
  - Validation: JSONL parses; IDs are unique; every supports/conflicts reference resolves; every ATH-SRC and KO citation in the four edited or created Markdown files resolves.
- **Existing catalog items reused, not re-catalogued:** ATH-SRC-0772 (also surfaced in Shamaa as ID 224731), 0773–0777, 0567–0571, 0574, 0603, 0604, 0623, 0630, 0432–0434, 0650, 0943, 0955.
- **Knowledge objects:** 12 (`_data/knowledge_objects_w2.jsonl`).
  - LA: 9 (KO-LA-07B-001…009)
  - RS: 1 (KO-RS-07B-001)
  - CD: 2 (KO-CD-07B-001 evidence_based; KO-CD-07B-002 design_hypothesis)
- **Helpline register:** 18 rows covering 10 countries (`11_RIGHTS_PRIVACY_AND_SAFETY/YOUTH_HELPLINE_REGISTER.csv`).
  - 8 `verified_official`
  - 6 `verified_directory` (Child Helpline International)
  - 3 `secondary_only`
  - 1 `needs_live_test`
- **Deep cards:** none written. The brief asked for the evidence file and KOs. `deep_card` is null in every record.

## Files produced or edited
- NEW `07_LEARNING_SCIENCE/ARABIC_ASSESSMENT_AND_AI_EVIDENCE.md`: per-gap answers (known, confidence, implication, decision change) for G03, G04, G06, G07, G18 and G19.
- NEW `07_LEARNING_SCIENCE/_data/sources_w2.jsonl`, `_data/knowledge_objects_w2.jsonl`, `_data/agent_report_w2.md`.
- NEW `11_RIGHTS_PRIVACY_AND_SAFETY/YOUTH_HELPLINE_REGISTER.csv`.
- EDITED (appended "## إضافة الدفعة الثانية" only):
  - `07_LEARNING_SCIENCE/EDUCATIONAL_VALIDATION_PLAN.md`: stages 2, 3, 4 and 6, plus claims C11, C12 and B10.
  - `10_TECHNICAL_ARCHITECTURE/AI_CHARACTER_GUARDRAILS.md`: Arabic-specific section.
  - `06_COGNITIVE_SCIENCE/CRITICAL_THINKING_ASSESSMENT_FRAMEWORK.md`: Arabic instruments section.

## Search strategy
- **ACL Anthology.** Scraped the volume listings of ArabicNLP 2023, 2024, 2025 (main and shared tasks) and 2026 (main and shared tasks) with keyword filters. Read the abstracts from paper pages (citation_* meta tags).
- **Shamaa (Arab Educational Information Network).** Wave 1 listed it as blocked. It turned out to be scriptable through `?page=Search&SearchValueTBX=` plus the `FullRecord` and `endnotes` pages. About 20 Arabic queries covered CT instruments, CRT, Cornell, Watson-Glaser, game-based learning, inquiry, meta-analysis and probability expressions.
- **Crossref** for DOIs and abstracts. **PubMed/PMC** for the Heliyon and PLOS ONE abstracts. **Hugging Face API** for dataset and model licences and languages.
- **Official pages:** Child Helpline International, Bahrain national portal, Qatar MSDF Yusr, Saudi MOH, ADPolice, UNICEF Oman, Embrace, himaya.
- **WebSearch** (about 40 queries, Arabic and English, some in extended mode) for discovery. **WebFetch** for arXiv abstracts and pages that curl could not reach.

## Interpretations made (owner absent)
1. **Scope of "verified" for helplines.**
   - `verified_official` = an operator or government page read today.
   - `verified_directory` = the Child Helpline International profile only.
   - Neither status replaces a live test call. KO-LA-07B-003 makes the test call a shipping condition.
   - I did not invent any number. Rows whose only source is the press are marked `secondary_only` (UAE 800-HOPE, Egypt 105, Morocco 2511).
2. **"Child/youth helpline".** I included both child-protection lines and national mental-health or suicide lines where verified (Saudi 920033360, Lebanon 1564), because ATHAR's crisis exit needs both kinds.
3. **The 2018–2026 window for G19.** I added Templin & Bradshaw (2013) and Almond et al. (2015). They are older, but they are the direct answer to "reliability with few tasks" and to the Bayes-net option.
4. **Preprints and blogs** were catalogued with a C or D grade and confidence medium or low: Safe-Child-LLM, SproutBench, PolyGuard, AraGen blog. They were not used for any `[حقيقة موثقة]` claim except a descriptive one ("benchmark X exists and reports Y").
5. **ACL 2025–2026 papers without a DOI on the page** (2026 volumes) have `doi: null`. Their URL is the Anthology page.
6. **ACL paper licence.** Recorded as CC BY 4.0 for the paper text, per the Anthology footer for post-2016 material. Storage is set to yes and commercial reuse to not_established, because datasets and code carry separate licences.

## Blockers
- **OpenAlex:** the shared daily budget was exhausted (HTTP 429, "$0 remaining"). Getting a key requires the user's email, so I did not request one. Crossref was used instead.
- **Operator sites unreachable** through the proxy:
  - nfsp.org.sa (502), dfwac.ae and sssd.shj.ae (connection reset), nccm.gov.eg and kncpp.moh.gov.kw (503), atfalouna.gov.lb (502).
  - 2511.ma failed TLS hostname verification (not bypassed).
  - u.ae child-safety page returned 404.
- **oecd.org** returned 403 to curl. WebFetch returned metadata only, so PISA item licence terms and the country-note scores were not read.
- **qspace.qu.edu.qa, fis.uni-bamberg.de (curl) and dsr.ju.edu.jo:** connection reset. Metadata came via WebFetch or the Shamaa record.
- **No full texts** behind paywalls (Elsevier, Springer, IEEE, IGI). Most B-grade records rest on the abstract only.

## Unverified candidates (not catalogued)
- "Cultural Benchmarking of LLMs in Standard and Dialectal Arabic Dialogues" (arXiv 2605.00119, Al Kautsar et al., 2026). The abstract was read: the MSA–dialect gap persists. Not catalogued because it is a preprint with no numbers in the abstract. Worth adding later.
- "Beyond MCQ: An Open-Ended Arabic Cultural QA Benchmark with Dialect Variants" (arXiv 2510.24328). Abstract only. The judging method is unclear.
- "Evaluating Arabic LLMs: A Survey of Benchmarks, Methods, and Gaps" (arXiv 2510.13430). Its abstract flags multi-turn dialogue as a gap. It is a preprint.
- CHARM: Character Hallucination for Multicultural Role Play (arXiv 2609.01352). Arabic inclusion is unconfirmed.
- "Evaluating Multilingual Safety Benchmarks for Low-Resource Languages in the Majority World" (J. Online Trust & Safety, 2026, DOI 10.54501/jots.v3i3.330, CC BY-NC-SA). Verified by Crossref, but not catalogued for lack of time. It is relevant: it recommends native data, disaggregated reporting and dialect coverage.
- "Standardizing the critical thinking skills test for university students" (Iraq, Wasit Journal of College of Education 48(1), 2022). PDF read: 30 items from a US commercial prep book, 400 university students. Excluded because it is not an adolescent instrument and the item rights are doubtful.
- Al-Jallad et al. E-CONAN Arabic NLI benchmarks (IEEE Access 2026, DOI 10.1109/access.2026.3732060). Crossref verified, but there was no abstract, so it was not catalogued.
- "Advancing Arabic AES through cross-encoder BERT…" (Scientific Reports 2026, DOI 10.1038/s41598-026-51068-y). No abstract was retrieved.
- AraScore short-answer scoring (Array 2022, DOI 10.1016/j.array.2021.100109). No abstract was retrieved.
- Shamaa Arabic studies seen but not catalogued, because they are weak or off-target:
  - Egyptian gamification and CT theses (IDs 207829, 330127): no abstract.
  - Teacher-perception study of digital stories and CT (ID 409601): not an outcome study.
  - Primary-school play and CT (ID 441824).
- MSDF/Masrawy Egypt mental-health hotline 105: press only.
- UAE 800-HOPE, Itma'en and Sakina: press only.

## Top 5 findings that should change ATHAR's design
1. **Llama Guard 3/4 do not list Arabic.** R13 must use an Arabic-capable guard (PolyGuard, Qwen3Guard or similar), benchmarked on AraSafe, ArGuard and a teen slice.
2. **Arabizi and transliteration, not MSA, are the main jailbreak surface.** No model reached 90% harmful-refusal on Arabizi. Red-team sets need separate Arabizi and dialect slices, and input normalisation.
3. **Safety must be scored as two numbers** (missed harm and over-refusal) per register. Refusal-only tuning collapses into refusing everything, which would kill crime-themed content.
4. **The scoring pipeline:** fine-tuned small Arabic model scores; the LLM only words the feedback; a leniency check and an off-topic gate come first. Arabic LLM judges agree with humans only moderately (kappa about 0.46).
5. **The confidence UI shows the numeric band inline with every Arabic likelihood word.** This is robust across 17 languages. Measurement defaults to 3-level mastery states with task-first reliability rather than fine scores.

## Top 5 open questions / gaps for human or expert review
1. **Test calls and official confirmation** for the helpline rows. Priority: Kuwait 147 (documented 2019 outage), UAE 116111 current status, Saudi 116111 hours, and the three press-only rows.
2. **An Arabic minors' safety benchmark and an Arabic role-play/persona benchmark** do not exist. ATHAR must build them with child-protection experts. This is both a publication opportunity and a release blocker for free interview.
3. **MSA vs dialect scoring bias among 13–18** is still unstudied. The Phase 3 study is required, and dialect margins need a measurement expert.
4. **Human search of Al-Manhal, Dar Al-Mandumah and e-Marefa** to confirm the absence of an adolescent-normed Arabic CT instrument. Also needed: Insight Assessment's Arabic CCTST licence terms and OECD PISA item terms.
5. **An Arabic verbal-probability lexicon study** (100–200 teens per age band across dialect regions) before the Arabic likelihood terms are fixed. A measurement expert also needs to set the thresholds for split-half and classification consistency.
