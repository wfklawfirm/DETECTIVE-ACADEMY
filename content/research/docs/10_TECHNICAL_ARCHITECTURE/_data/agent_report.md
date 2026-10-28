# Agent report — 10_TECHNICAL_ARCHITECTURE

Date: 2026-10-27 · Source ID block used: ATH-SRC-0900 … 0969 · KO lib code: 10

## Counts
- **Sources verified:** 70 (`_data/sources.jsonl`, ATH-SRC-0900–0969; all lines are valid JSON and pass the allowed-value checks)
  - By grade: A = 7 (OWASP, W3C SCXML, NIST AI 600-1, NIST SP 800-226, IEEE xAPI, 1EdTech LTI, 1EdTech Caliper); B = 26 (peer-reviewed); C = 29 (official docs/tools/vendor guidance); D = 8 (preprints, journalism)
  - 1 record marked `needs_expert_review` (ATH-SRC-0944 Character-LLM: venue and mechanism not confirmed)
- **Deep cards:** 6 (0924 Versu, 0926 ASP for PCG, 0934 Generative Agents, 0943 TimeChara, 0945 LLM-as-a-Judge, 0952 OWASP LLM Top 10 2025)
- **Knowledge objects:** 15. That is 7 CM (case mechanics), 5 CD (AI-character knowledge patterns) and 3 LA. Every object cites catalog sources, or is a design_hypothesis with an explanation.

## Files produced
- `CASE_ENGINE_TECHNICAL_RESEARCH.md`: architecture, plus answers to all 9 critical questions
- `CASE_SCHEMA_PROPOSAL.md` + `case_schema.json` (JSON Schema 2020-12). The schema is checked with jsonschema 4.26 (`check_schema` OK), and an example case validates with 0 errors.
- `AI_CHARACTER_GUARDRAILS.md`
- `NARRATIVE_AUTHORING_TOOLS_COMPARISON.md`
- `ASSESSMENT_ENGINE_TECHNICAL_MODEL.md`
- `TECHNICAL_RISKS_AND_MITIGATIONS.md` (20 risks)
- `cards/` × 6
- `prototypes/`: `case_example_minimal.json` (fictional, non-violent toy case), `fairness_check.py` (integrity, reachability, minimal evidence sets, disjoint paths), and `asp/*.lp` (ASP encodings tested on clingo 5.8.2, installed temporarily in the scratchpad)
- `_data/sources.jsonl`, `_data/knowledge_objects.jsonl`, `_data/agent_report.md`

## Search strategy
- I went to primary and official pages first: GitHub repositories and license pages for tools, vendor documentation for structured outputs, caching and batching, and ACL Anthology, JAIR, AAAI OJS, NeurIPS, ICLR proceedings and Crossref API records for papers. I used arXiv only when no venue record was reachable.
- I cross-checked venues and DOIs via Crossref where the publisher blocked fetching (Harel 1987, ACM UIST/CCS/AISec, ACM Computing Surveys).
- Where an abstract page did not state a claim, I fetched the full text (e.g. the Generative Agents limitations and cost, and the tokenizer premium for Arabic).

## Blockers
- **The shared WebSearch budget (200/turn) was exhausted** partway through. After that I verified only via WebFetch on known authoritative URLs.
- **The shared WebFetch budget (800/hour) was then exhausted** near the end. I could not fetch: the Zheng et al. PDF (position-swap figures), the Wang et al. PDF (names of calibration methods), and the Character-LLM PDF.
- Fetching was blocked by robots or client errors for ScienceDirect, ACM DL, adlnet.gov, OpenReview and the GitHub locale tree of twinejs.
- Pages without the needed detail: Godot TextServer and HTML docs were truncated (resolved via the godot-docs GitHub source); Ren'Py RTL support was not found in the translation, text or config docs; the ITU Facts & Figures page gave no Arab-States figures; the articy paid pricing page and Stately Studio pricing were not fetched.

## Unverified candidates (NOT in sources.jsonl)
- **Ren'Py RTL support:** I believe Ren'Py has RTL/Arabic text support, but I could not find it in the docs pages I fetched.
- **ADL xAPI project page / xAPI Profiles / cmi5:** adlnet.gov blocked fetching. xAPI is covered instead by IEEE 9274.1.1-2023 and the xapi.com overview.
- **Unity's own 2023 Runtime Fee announcement post:** only third-party journalism (ATH-SRC-0909) and Unity's 2024 cancellation post were verified.
- **ITU regional connectivity statistics for Arab States:** I need figures for the low-bandwidth assumptions; deferred to library 08.
- **Twine 2 UI Arabic locale:** not verified.
- **Character-LLM "protective experiences" mechanism and EMNLP 2023 venue:** the abstract page did not confirm either, so the record is flagged `needs_expert_review`.
- **Calibration method names in Wang et al. 2024** (e.g. "balanced position calibration"): not visible on the landing page and not asserted in any document.
- **Ink/Inky RTL editing; Yarn Spinner RTL; Arcweave RTL:** not mentioned on the official pages.
- **Stately Studio and articy:draft paid pricing:** not fetched.
- **NIST SP 800-226 privacy-hazard list:** only the landing page was read.

## Top 5 findings that should change ATHAR's design
1. **Prompting cannot keep secrets or prevent invention.** Generative agents fabricate details (ATH-SRC-0934). Role-play models leak knowledge outside the character's point in time even at GPT-4o level (ATH-SRC-0943). OWASP treats system-prompt leakage as a top-10 risk (ATH-SRC-0952). So the truth must stay outside the model: per-character, per-state allowed sets; evidence issued only by the engine; and a deterministic validator on every turn with authored fallbacks.
2. **Fairness can be machine-checked before publishing.** ASP/clingo (MIT) expresses "every false hypothesis is refutable, the true one is supported, there are ≥N disjoint proof paths" as constraints (ATH-SRC-0926/0927). Our tested prototype flagged a deliberately unfair variant (`unrefuted_false(h_coach)`) and passed a legitimate red herring. No market authoring tool does this, which is an opening for ATHAR's own editor.
3. **LLM-as-judge is usable only with controls and Arabic calibration.** The documented problems are position, verbosity and self-preference bias and 12 bias types in total. Even the best correlations are moderate (G-Eval 0.514), while a rubric plus a reference raises agreement (Prometheus 0.897). Use absolute rubric scoring, a different model family from the dialogue model, deterministic checks on cited evidence, and formative feedback only until an Arabic rater study exists.
4. **Arabic costs more per turn.** cl100k_base uses about 3× the tokens for Arabic vs English (ATH-SRC-0969). Combine this with prompt caching at 0.1× for reads (ATH-SRC-0965/0966), batch at 50% (0967) and cascades (0968): cost design must start from measured Arabic token counts with the candidate vendors.
5. **Stay engine- and vendor-agnostic.** Unity's 2023 per-install fee and its 2024 reversal plus price rises show terms can change within a year (0908/0909). Godot 4 cannot export C# to the web (0907). Use a PWA + XState (MIT) + own JSON schema + PostgreSQL (with Apache AGE optional); avoid GPL/BSL graph databases as core dependencies.

## Top 5 open questions / gaps for human or expert review
1. Measured fabrication and leakage rates of the candidate models **in Arabic (MSA and dialect input)** with small allowed-fact packs. All the evidence we found is English or Chinese.
2. How accurate Arabic NLI or contradiction detection is (English SummaC is ~74% balanced accuracy), which decides how much human review the test pipeline needs.
3. Arabic token cost per turn for current vendors, and whether a self-hosted small judge model (Prometheus-style) reaches acceptable agreement in Arabic. This also bears on privacy for minors.
4. Usability of a form-based case editor (knowledge matrix, evidence board, timeline) for non-technical Arab writers and scientific reviewers. It needs a test with 5–8 writers.
5. clingo performance on realistic cases (30–80 evidence items, compound guards), plus a rule for encoding "assumed general knowledge" with cultural and age review. Also connectivity and device baselines for Arab markets (library 08) to set bundle-size budgets.

## Gap-fill round (2026-10-27)

**New records (6):** ATH-SRC-0970–0975. Catalog now 76 records. `needs_expert_review`: 1 → 0.

| ID | Source | Finding |
|---|---|---|
| 0970 | Ren'Py changelog and style docs | **RTL verified:** HarfBuzz Arabic shaping (8.3.7), RTL on by default (8.4.1/8.5.0), `reading_order` property |
| 0971 | Twine 2 source, `src/util/locales.ts` | The editor UI has 22 locales and **no Arabic or RTL locale** |
| 0972 | ink docs, "International character support in identifiers" | Arabic content unrestricted; Arabic identifiers allowed |
| 0973 | Arcweave localization docs | Team plan only; main language changeable; Arabic example in the docs; no RTL editor statement |
| 0974 | ITU Facts and Figures 2025 | Arab States: about 70% Internet use, about 13% 5G population coverage |
| 0975 | GSMA Mobile Economy MENA 2025 | 308m mobile-internet users (46%); GCC 71% vs 43% elsewhere; 30% still on 3G or feature phones; entry smartphone costs 18% of monthly GDP per capita (44% for the poorest 20%) |

**Changed records:**
- **0944** Character-LLM → `verified`. Confirmed as EMNLP 2023 main conference (ACL Anthology 2023.emnlp-main.814, pp. 13153–13187; DOI 10.18653/v1/2023.emnlp-main.814). The "protective experiences" mechanism was read in the PDF. Type changed to `conference_paper` and grade raised from D to B.

**Correction:** `NARRATIVE_AUTHORING_TOOLS_COMPARISON.md` said Godot was the only tool here documenting RTL. **That was wrong:** Ren'Py also documents it. The comparison table was updated for ink, Twine, Ren'Py and Arcweave. The overall conclusion is unchanged: no web authoring tool examined offers an Arabic-native editor, so ATHAR's own RTL editor is still justified.

**Deliverables edited:**
- `NARRATIVE_AUTHORING_TOOLS_COMPARISON.md`
- `CASE_ENGINE_TECHNICAL_RESEARCH.md`: the connectivity gap was replaced with ITU and GSMA figures, and two device/bandwidth profiles were added.
- `cards/ATH-SRC-0943.md`: Character-LLM line.

**Still open:**
- RTL behaviour of the Inky editor, the Yarn Spinner runtime and Twine story formats (Harlowe, SugarCube). Their official docs fetched in this round do not mention it. GitHub issue search was not available from this session.
- Per-country data prices and speeds (library 08).
- articy:draft and Stately paid pricing were not retried.
