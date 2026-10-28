# Agent Report — 07_LEARNING_SCIENCE

**Date:** 2026-10-27 | **Source ID block used:** ATH-SRC-0600 … ATH-SRC-0666 | **KO lib code:** 07

## Counts

| Item | Count |
|---|---|
| Sources verified (`_data/sources.jsonl`) | **67** (target 40–50). Grades: A = 31, B = 33, C = 3 |
| … of which `review_status: needs_expert_review` | 4 (ATH-SRC-0620, 0636, 0647, 0650). Bibliographic record verified; key quantitative content not retrieved |
| Deep cards (`cards/`) | **8** (0600, 0603, 0606, 0610, 0628, 0630, 0631, 0639) |
| Knowledge objects (`_data/knowledge_objects.jsonl`) | **23** = 20 LA (KO-LA-07-001…020) + 3 PO (KO-PO-07-001…003) |
| Outcome rows in gameplay map CSV | 15 |

## Files produced

- `07_LEARNING_SCIENCE/ATHAR_LEARNING_SCIENCE_FOUNDATION.md`: evidence map, overstatement table, explicit answers to the brief's 10 deep questions, design "constitution".
- `07_LEARNING_SCIENCE/EVIDENCE_CENTERED_ASSESSMENT_MODEL.md`: student model (8 skills + knowledge nodes), 13 observables with evidence rules, task model, LLM-scoring design, 3 worked examples (including guess vs inference).
- `07_LEARNING_SCIENCE/LEARNER_MASTERY_MODEL.md`: BKT + Beta two-layer model with computed examples, uncertainty statuses, decay, mastery gates, learner and teacher display rules.
- `07_LEARNING_SCIENCE/LEARNING_OUTCOMES_TO_GAMEPLAY_MAP.csv`: 15 outcomes with the 11 required columns; all source IDs resolve.
- `07_LEARNING_SCIENCE/EDUCATIONAL_VALIDATION_PLAN.md`: 8 staged studies (0–7), LLM scorer acceptance protocol, sample-size arithmetic, and a claims register (6 allowed now / 9 need evidence / 10 never).
- `07_LEARNING_SCIENCE/cards/ATH-SRC-*.md`: 8 cards.
- `07_LEARNING_SCIENCE/_data/sources.jsonl`, `_data/knowledge_objects.jsonl`, `_data/agent_report.md`.

Validation: every line in both JSONL files parses, source IDs are unique, and every `ATH-SRC` cited in the Markdown/CSV/KOs exists in the catalog. Every catalog record is cited at least once.

## Search strategy

1. ~40 targeted WebSearch queries (standard mode) for the named canon: ECD, stealth assessment, game meta-analyses, the guidance debate, retrieval and spacing, feedback, formative assessment.
2. The **shared WebSearch budget for this turn ran out** (200 calls across all agents) early in the session. From then on, verification used WebFetch of authoritative records only:
   - **Crossref DOI records** (`api.crossref.org/works/<DOI>`) for bibliographic facts.
   - **OpenAlex DOI records** for abstracts (reconstructed from the abstract index).
   - Publisher, PubMed, ACL Anthology, arXiv and official pages (FTC, OECD, UNESCO, EEF, testingstandards.net).
   - Bibliographic searches restricted to the OECD DOI prefix, to locate PISA publication DOIs.
3. Where only metadata (not an abstract) was retrievable, findings drawn from reviewer knowledge are labelled in `limitations`, and/or the record is marked `needs_expert_review` with `confidence: medium`.

## Blockers

- **WebSearch budget exhausted.** Arabic-language and 2025–2026 literature searches (extended mode) could not be run. This is the main gap.
- **WebFetch hourly budget hit once.** It was resumed after reset.
- **Refused or blocked sites:** ScienceDirect (robots), Springer link pages (client error), several OECD project pages, the UNESDOC record (empty render), and ETS research pages for some items. PMC returned a captcha.
- **Abstracts unavailable:** Kluger & DeNisi 1996 (abstract elided by publisher), Alfieri et al. 2011 (OpenAlex abstract mis-linked to another study), and Steiss et al. 2024.
- **Shared scratchpad collision.** Another team's agent wrote `build_sources.py` into the shared scratchpad and overwrote my script of the same name. I then ran that file once by mistake. It rewrote `05_INVESTIGATIVE_REASONING/_data/sources.jsonl` from that team's own script, which held 43 records at that moment. **The 05 team should check that its `sources.jsonl` is complete.** I moved my scripts to `scratchpad/ls07_learning/`. My own catalog was not affected.

## Unverified candidates (not in sources.jsonl)

| Candidate | Why not verified |
|---|---|
| PISA 2025 Learning in the Digital World framework, construct details (SRL, computational/inquiry practices) | The publication (ATH-SRC-0650) is verified, but the construct description was not retrieved. Do not cite construct details yet. |
| UNESCO MIL curriculum, Arabic edition and licence | Arabic availability and licence of the 2nd edition not confirmed; the UNESDOC page did not render. |
| OECD critical-thinking/creativity rubric texts | Report verified (0652); rubric content not retrieved. |
| Slavin (1987) critique of mastery learning effects | No search budget left. |
| Kolb (1984) *Experiential Learning*, primary book | Not catalogued; critique (0663) catalogued instead. |
| Wiliam & Thompson / Wiliam (2011) *Embedded Formative Assessment* | No search budget left. |
| Zimmerman (2002) SRL overview; Winne & Hadwin | Covered via Panadero (0624) only. |
| Recent (2023–2026) peer-reviewed studies of LLM rubric scoring in Arabic, or across Arabic dialects | Could not search. **No such study was found by this team, which is a gap, not evidence of absence.** |
| Recent GBL meta-analyses (e.g., post-2018 on critical thinking in games) | Could not search. |
| Baker, Corbett & Aleven (2008) contextual guess/slip | Not searched. |
| Mayer (2004) "Should there be a three-strikes rule against pure discovery learning?" | Not searched. |
| Ericsson / deliberate practice; Bjork "desirable difficulties" | Owned more naturally by 06; not searched. |
| Messick (1989) "Validity" chapter in *Educational Measurement* | 1995 article used instead. |
| EEF Toolkit methodology critiques (months-of-progress conversion) | Not searched; noted as unverified in 0648 limitations. |

## Top 5 findings that should change ATHAR's design

1. **The correct culprit is weak evidence.** With N suspects, a guess hits about 1/N of the time. Mastery must rest on process observables that are hard to produce by chance (planted-contradiction detection, disconfirming-clue citation, belief revision), and the final answer should carry a high guess parameter [0600, 0622].
2. **One case cannot measure a skill.** Task sampling dominates measurement error [0630], and the best stealth assessment reached only r ≈ 0.4 after about 3 hours [0603]. Plan 6–10 cases per skill across 3 or more contexts, and always show uncertainty, including an honest "insufficient evidence" state.
3. **Guidance is a core feature, not a crutch.** Guided inquiry clearly beats unguided inquiry [0610, 0647]. Problem-first sequencing helps older learners but favours instruction-first for younger learners and for domain-general skills [0645], which is directly relevant to ATHAR's 13–15 band. A/B test the sequence by age.
4. **An LLM scorer is an instrument that must pass acceptance tests.** Documented verbosity, position, temporal-drift, dialect and Arab-culture biases [0633, 0658, 0664, 0634, 0637, 0660] make "extract the argument, then score by rule" plus adversarial audits (length, dialect, eloquent-but-empty) mandatory. MSA load is a likely construct-irrelevant variance source [0662].
5. **Motivation and transfer claims are the main legal and credibility risk.** Games were not more motivating than conventional instruction [0605]. Entertainment value did not drive learning [0607]. Completion rewards undermine intrinsic motivation [0665]. Far transfer is rare [0640, 0641]. And the FTC v. Lumos Labs settlement shows these claims are enforceable [0639]. The claims register in the validation plan must gate all marketing.

## Top 5 open questions / gaps for expert review

1. Which **Arabic, age-normed external criteria** exist for evidence evaluation and argument analysis (ages 13–18)? Without them, Stage 4 cannot run.
2. What **equivalence margin** defines a fair scorer across dialects, and what group sizes does DIF analysis need in practice?
3. Which **measurement model** fits best: BKT per skill, a Bayesian network, or multidimensional IRT? And how should local dependence within scenes be handled?
4. **Realistic effect size and ICC** for an Arab-school cluster RCT with an active control. This decides feasibility and cost of Stage 6.
5. Is **confidence calibration (S8)** in teens a stable skill worth reporting, or a noisy state? And do reasoning skills decay at rates resembling verbal memory?

## Notes for the merge step

- Canonical owner: ECD (Mislevy et al.) belongs to this library (0600, 0601).
- Likely overlaps:
  - Kahneman-style cognition and metacognition sources may also be in 06.
  - The FTC Lumos record (0639) may also be in 11.
  - The LLM bias papers (0633, 0637, 0660, 0664) may also be in 10.
  - The UNESCO MIL record (0653) may also be in 08.
- Deduplicate by DOI/URL.

## Gap-fill round (2026-10-27)

**New records (4):** ATH-SRC-0667–0670. Catalog now 71 records. **All 4 `needs_expert_review` records resolved**, so the count is now 0.

| ID | Source | Verification |
|---|---|---|
| 0667 | Bastani et al. 2025, *PNAS*: GPT-4 tutors for about 1,000 high-school students | PubMed. Unrestricted access → 17% lower grades once access was removed; guardrails mitigated this. |
| 0668 | Kestin et al. 2025, *Sci Rep*: RCT, pedagogically designed AI tutor beat in-class active learning | PubMed. University sample. |
| 0669 | Jiao, Song & Lee 2026, *EM:IP*: rater effects of 10 LLMs in essay scoring | ERIC + Crossref DOI |
| 0670 | Bui & Barrot 2024: ChatGPT vs human scoring of 200 essays | ERIC + Crossref DOI. Weak-to-moderate agreement, low repeat consistency. |

**Changed records (→ `verified`):**
- **0620** Kluger & DeNisi: OpenAlex abstract. d = .41, and over one-third of interventions reduced performance.
- **0636** Steiss et al.: abstract read. Humans better on all criteria except criteria-based, but the authors call the practical differences not substantial.
- **0647** Alfieri et al.: ERIC abstract, because the OpenAlex abstract is mis-linked to another study. d = −0.38 for explicit instruction vs unassisted discovery; d = 0.30 for enhanced discovery.
- **0650** PISA 2025 framework: official PDF read. LDW definition, the two-component competency model and the ECD basis added.

**Conclusions changed:**
1. The "LLM scores like a human" overstatement row now cites **counter-evidence on repeat-scoring stability** [0670] and model-specific rater effects [0669]. The validation plan gains a repeat-scoring / many-facet Rasch acceptance test.
2. **New constitution principle 13:** the AI must not think for the learner, and mastery is measured unassisted. The field evidence [0667] shows assisted performance can mask, and even reduce, learning.
3. The PISA 2025 LDW construct (self-regulated learning plus computational problem solving, measured in scaffolded units with ECD) is confirmed as the closest international framework. It contains no explicit "evidence reasoning" component.

**Deliverables edited:**
- `ATHAR_LEARNING_SCIENCE_FOUNDATION.md`: overstatement table, constitution, gaps section.
- `EDUCATIONAL_VALIDATION_PLAN.md`: scorer acceptance table.

**Still open:**
- **No peer-reviewed study of LLM scoring in Arabic or across Arabic dialects** was found. An ERIC query (2023–2026, peer-reviewed) returned 0 results. This is absence in that index, not evidence of absence.
- Arabic AI-tutor evidence for adolescents: none found.
- Slavin 1987, Wiliam 2011 and Baker et al. 2008 were not retried.
