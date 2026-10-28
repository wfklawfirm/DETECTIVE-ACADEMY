# Agent report — 05_INVESTIGATIVE_REASONING

Date: 2026-10-27 · Source ID block used: ATH-SRC-0400 … ATH-SRC-0450 · KO lib code: 05

## Counts

| Item | Count |
|---|---|
| Source records in `sources.jsonl` | **51** (45 `verified`, 6 `needs_expert_review`) |
| Evidence grades | A: 24 · B: 24 · C: 3 |
| Deep cards | **7** (0400, 0403, 0408, 0413, 0418, 0429, 0432). Three of them also cover companion sources: 0407/0409, 0419 and 0430/0431, 0433. |
| Knowledge objects | **24**: 14 RS (reasoning_skill), 5 LA (learning_assessment), 5 CD (character_design_pattern) |

The target was 25–35 sources. We verified 51 records. All were confirmed this session through official, publisher, DOI, or catalog pages. The six `needs_expert_review` records exist bibliographically, but we could not read their abstract or content this session, so their content claims are flagged.

## Files produced

- `05_INVESTIGATIVE_REASONING/INVESTIGATIVE_REASONING_FRAMEWORK.md`
- `05_INVESTIGATIVE_REASONING/EVIDENCE_EVALUATION_GUIDE.md`
- `05_INVESTIGATIVE_REASONING/COMMON_REASONING_ERRORS.md`
- `05_INVESTIGATIVE_REASONING/ETHICAL_INVESTIGATION_PRINCIPLES.md`
- `05_INVESTIGATIVE_REASONING/cards/ATH-SRC-0400.md`, `0403.md`, `0408.md`, `0413.md`, `0418.md`, `0429.md`, `0432.md`
- `05_INVESTIGATIVE_REASONING/_data/sources.jsonl` (51 lines, validated JSON; all cross-references resolve)
- `05_INVESTIGATIVE_REASONING/_data/knowledge_objects.jsonl` (24 lines, validated; every `source_ids` entry exists in the catalog)
- `05_INVESTIGATIVE_REASONING/_data/agent_report.md`

## Search strategy

1. **Official pages first.** We fetched these directly:
   - College of Policing APP pages: investigation process, investigative interviewing, and the intelligence report (3x5x2).
   - APT (Méndez Principles).
   - OHCHR and UN pages: UDHR, ICCPR, CRC, Berkeley Protocol.
   - ODNI ICD 203.
   - CIA CSI: Heuer, the Tradecraft Primer, Kent.
   - National Academies (2014 eyewitness report; 2003 polygraph report).
   - legislation.gov.uk (CPIA s.23).
   - GOV.UK (Achieving Best Evidence).
2. **Peer-reviewed articles** were checked on the publisher page where reachable (Springer, Annual Reviews, APS, Cold Spring Harbor). Otherwise we used DOI metadata from the Crossref API and abstracts reconstructed from the OpenAlex API.
3. **Shared WebSearch budget exhausted early.** The 200-call per-turn limit was shared across all agents and ran out after about 20 searches. After that, verification ran only through direct fetches of known official and DOI endpoints. WebFetch also hit its hourly rate limit once; we waited for the reset, then continued.

## Blockers

- **WebSearch budget** ran out early (shared limit), so we could not search Arabic-language sources or niche items. Arabic-language investigative-reasoning literature is therefore **not covered**. This is the largest gap.
- **WebFetch hourly rate limit** was hit once.
- **Heuer, Chapter 8 (ACH):** every PDF copy we could fetch (CIA, govinfo, Apache corpus, CREST) was truncated around page 43, so we could not read the ACH chapter text. We took the ACH step descriptions from the CIA Tradecraft Primer (0431) and the experimental test (0430).
- **APA abstracts withheld** in Crossref, Semantic Scholar, and OpenAlex for O'Brien 2009 (0425), Lord et al. 1984 (0450), and Fisher & Geiselman 2010 (0406). Content claims for these are flagged.
- **Pages not reached:**
  - PubMed and scinapse returned CAPTCHAs; altmetric and doi.org (APA) were blocked by robots.txt.
  - OHCHR and UN docs pages for General Comment No. 32 did not return content.
  - The CPIA Code of Practice PDF was not reachable.
- **Licences:**
  - College of Policing content is under a Non-Commercial College Licence (commercial reuse needs a separate licence).
  - Méndez Principles and UN instruments have no stated reuse licence.
  - US-government works (ICD 203, Tradecraft Primer, Kent) are assumed public domain in the US only.
  - Library 11 must confirm commercial reuse.

## Unverified candidates (not in sources.jsonl)

| Candidate | Why not verified |
|---|---|
| Admiralty / NATO source-reliability grading (A–F × 1–6; AJP-2.1 / STANAG 2511) | Only Wikipedia was reachable (not allowed for non-literary facts). FM 2-22.3 Appendix B was cut off in the fetch. The guide uses the verified UK 3x5x2 system instead. |
| UN Human Rights Committee, General Comment No. 32 (CCPR/C/GC/32, 2007) | The UN docs page returned no text. |
| CPIA Code of Practice (2020) para. 3.5, wording "towards or away from the suspect" | PDF not reachable. The same idea is verified in APP (0400). |
| Van Gelder 2008, "Can we do better than ACH?"; Thomason 2010 (ACH criticism) | Seen only as Wikipedia citations. |
| Marcoci et al. 2018, "ODNI as an analytic ombudsman" | Appeared in search results only; not fetched. |
| Kassin, Goldstein & Savitsky 2003, behavioural confirmation in interrogation | Not searched (budget). |
| Vrij et al. on verbal lie detection (e.g., cognitive load approaches) | Not searched (budget). We cite only Vrij et al. 2019 (0415). |
| Innocence Project figure on eyewitness misidentification (often quoted as ~69%) | The page we fetched gives no such figure. Do not use that number. |
| Bellingcat or First Draft verification guides | Not searched (budget). |
| Arabic-language sources: Arab investigative-interviewing training, Arabic translations of PEACE, Arab criminal-procedure presumption-of-innocence provisions | Not searchable (budget). |

## Top 5 findings that should change ATHAR's design

1. **Modify the OBSERVE→…→JUSTIFY model; do not replace it.**
   - OBSERVE becomes "observe & source".
   - HYPOTHESIZE becomes "generate competing hypotheses".
   - TEST becomes "diagnostic / disconfirming".
   - REVISE becomes "revise & log".
   - JUSTIFY becomes "justify & calibrate".
   - Two always-on guards are added: fairness / presumption of innocence, and a decision log.
   - The evidence: professional practice requires alternative hypotheses and decision rationale (0400). Merely showing an alternative does not help, while active evidence-rating does (0445).
2. **Never use demeanour as evidence.** Lie detection from behaviour is about 54% accurate, experts are no better (0413), and valid cues are scarce (0414, 0415). Training on cues raised confidence but lowered accuracy (0416), and experience biases judges toward calling people liars (0447). The safe alternative is statement-vs-evidence consistency (0423), taught as reasoning about evidence.
3. **Interview mechanics must be rapport-based.** Accusatorial methods increase false confessions (0420). Adolescents are especially vulnerable to false-evidence ploys and to wanting to escape the situation (0419, 0421). Coercive choices must never be rewarded (0403, Méndez; ICCPR art. 7 and 14(3)(g); Arab Charter art. 8 and 16(6)).
4. **Witness reliability depends on procedure.** First confidence, under pristine conditions, is diagnostic; later confidence is not (0408, 0407, 0409). Real-world descriptions can be badly wrong: in one archival study, 42% of described attributes were incorrect (0448). Store the first confidence statement and model contamination events.
5. **Show uncertainty as words plus numbers, measure calibration, and avoid a heavy ACH matrix.**
   - Verbal terms are misread even when ranges are given (0433, 0434), so show numbers next to the words.
   - Calibration is trainable (0443), and errors can run toward underconfidence (0444).
   - The full ACH matrix did not reliably debias professionals and may have added error (0430). Use a light hypothesis board instead, and A/B test it.

## Top 5 open questions / gaps for expert review

1. Arabic probability vocabulary: do terms like «مرجّح», «مستبعد» and «شبه مؤكد» map consistently to numeric ranges for teens across dialects? This needs a small comprehension study.
2. Transfer: does in-game hypothesis generation and calibration transfer to real-world reasoning, such as evaluating news? Design the transfer assessment with Library 07.
3. Arab legal context: how do APP and PEACE concepts map onto Arab criminal procedure (investigating judge or prosecutor led)? Is there Arabic research on false confessions or investigative interviewing? Not searched this session.
4. Validity of in-game behavioural metrics (incriminating-choice index, calibration score, justification rubric): reliability, and whether they can be gamed.
5. Commercial reuse rights for the College of Policing, APT/Méndez and US-government texts; and the age-appropriateness thresholds for confession and coercion themes (Library 11).

## Coordination notes for other teams

- College of Policing guidance is canonically owned by this library.
- Kahneman/Tversky-style biases belong to Library 06; we cite only their investigative forms.
- Lord et al. 1984 (0450) is cataloged for cross-reference; Library 06 is the natural owner.
- Library 04 (forensic) should reuse 0427 (forensic confirmation bias) and the "blind re-test" mechanic.
- Library 11 should review ETHICAL_INVESTIGATION_PRINCIPLES.md: content rules for 13–15, privacy, and real-case requests.

## Gap-fill round (2026-10-27)

**New records (3):** ATH-SRC-0451–0453. Catalog now 54 records. `needs_expert_review`: 6 → 2.

| ID | Source | Verification |
|---|---|---|
| ATH-SRC-0451 | UN Human Rights Committee, General Comment No. 32 (CCPR/C/GC/32, 2007) | Official UN ODS PDF (English). The official Arabic version also exists. Paras 30, 41 and 42–44 read. |
| ATH-SRC-0452 | UK MOD JDP 2-00, 4th ed. (2023) | Official GOV.UK PDF. Contains the NATO Intelligence Grading System, which the document says is "sometimes referred to as the Admiralty Code". Crown copyright with restrictive release terms. |
| ATH-SRC-0453 | UN Manual on Investigative Interviewing for Criminal Investigation (DPO/OHCHR/UNODC 2024) | Full PDF read. Same publication as 0404, kept as a content record. |

**Changed records:**
- **0404** → `verified`, now linked to the full-text read.
- **0406** (Fisher & Geiselman) → `verified`. PubMed abstract read; the component list is still to be taken from the full text.
- **0417** (NAS polygraph) → `verified`. Executive-summary conclusions added: well above chance but well below perfection for specific incidents, and screening accuracy is lower.
- **0450** (Lord et al. 1984) → `verified`. Abstract read via OpenAlex. It **confirms** the claim that "consider the opposite" outperformed "be fair and unbiased" instructions.
- **0429** (Heuer): Chapter 8 was read from the full CIA PDF. The eight ACH steps were added. Chapter 10's section on persistence of impressions based on discredited evidence was also confirmed. The limitation about the unreadable chapter was replaced.

**Deliverables edited:**
- `EVIDENCE_EVALUATION_GUIDE.md`: the Admiralty note was replaced. The decision now adds the two-axis A–F × 1–6 grading for 16+, alongside the existing 3x5x2 system.
- `COMMON_REASONING_ERRORS.md`: error #11 confidence raised from "unresolved" to "medium", with the definition updated.
- `ETHICAL_INVESTIGATION_PRINCIPLES.md`: GC32 paras 30, 41 and 42–44 added, plus the UN manual "red list". There is a new binding rule: no in-story official may publicly declare guilt before resolution.
- `cards/ATH-SRC-0429.md`: ACH steps added and items renumbered.
- `cards/ATH-SRC-0403.md`: UN manual content added.

**Still open:**
- ATH-SRC-0411 (Loftus & Palmer) and ATH-SRC-0425 (O'Brien 2009): no abstract in OpenAlex, PubMed or ERIC.
- CPIA Code of Practice and the Van Gelder / Thomason ACH critiques were not retried.
- Arabic-language sources remain a gap.
