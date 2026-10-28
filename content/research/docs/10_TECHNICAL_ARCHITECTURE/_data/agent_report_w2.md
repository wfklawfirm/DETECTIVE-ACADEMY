# Agent report — W2-DESIGN-TECH (wave 2) — 2026-10-27

Source ID block: ATH-SRC-1900 … 1999 (used 1900–1954) · KO code: 10B

## Counts
- **Sources verified:** 55 new records in `10_TECHNICAL_ARCHITECTURE/_data/sources_w2.jsonl`.
  - Library: 35 × `10_TECHNICAL_ARCHITECTURE`, 20 × `03_NARRATIVE_AND_GAME_DESIGN`.
  - Grades: A 3, B 11, C 36, D 5.
  - Rights: OPEN_LICENSE 23, COPYRIGHTED_RESTRICTED 27, UNKNOWN 4, LICENSED 1.
  - Review status: 51 `verified`, 4 `needs_expert_review`. These are 1934 (FDG 2026 paper, content not readable), 1935 (Ingold GDC talk, only description read), 1939 (ThinkyCon talks, titles only) and 1954 (open TTS licences, dataset rights unclear).
- **Validation passed:**
  - JSONL parses, all required schema keys are present, and allowed values are respected.
  - IDs are unique and in range.
  - Every `supports`/`conflicts_with` reference resolves against the master catalog plus all `sources_w2*` files.
  - Every ATH-SRC citation in the 5 edited or created Markdown files resolves.
- **Knowledge objects:** 7 in `_data/knowledge_objects_w2.jsonl`. CM: KO-CM-10B-001…004. LA: KO-LA-10B-001…003. All validated, and all cite catalog IDs.
- **Deep cards:** none. The brief did not request them; analysis lives in the three new documents.
- **Existing catalog IDs reused, not re-catalogued:**
  - 0969, 0963, 0964, 0965, 0974, 0975.
  - 0900–0903, 0971, 0972, 1837.
  - 0200, 0201, 0206, 0226, 0235, 0246, 0247, 0249, 0255, 0256, 0265, 0267, 0269, 0270, 0888.
  - 1173–1175.

## Files produced or edited
- **New:**
  - `10_TECHNICAL_ARCHITECTURE/ARABIC_TOKEN_COST_MEASUREMENT.md`
  - `10_TECHNICAL_ARCHITECTURE/RTL_AUTHORING_TOOL_TESTS.md`. Its §8 also holds the task-4 remnants: fonts, Android share, PWA and TTS.
  - `03_NARRATIVE_AND_GAME_DESIGN/DESIGN_EVIDENCE_UPDATE_W2.md`
- **New data files in `10_TECHNICAL_ARCHITECTURE/_data/`:**
  - `token_test_set.jsonl`: 34 items in 18 parallel groups, original text.
  - `token_measurement_script.py`: run with `python3 -I`. It downloads tokenizer data files only, at pinned commits.
  - `token_measurement.csv`: 442 item × tokenizer rows.
  - `token_measurement_summary.csv`: 234 rows.
  - `token_measurement_manifest.json`: licence, gating and SHA-256 per tokenizer.
  - `rtl_test_fixtures/`: ink, Yarn, Twine, bidi and font scripts plus raw results (156 KB).
- **Edited:** marked sections «## إضافة الدفعة الثانية» appended to:
  - `03_NARRATIVE_AND_GAME_DESIGN/HINT_AND_DIFFICULTY_SYSTEM.md`
  - `10_TECHNICAL_ARCHITECTURE/NARRATIVE_AUTHORING_TOOLS_COMPARISON.md`
- **Files I did not touch (they still carry the old «~3×» wording):**
  - `CASE_ENGINE_TECHNICAL_RESEARCH.md`
  - `TECHNICAL_RISKS_AND_MITIGATIONS.md` (T8)
  - `14_PRODUCT_RESEARCH_SYNTHESIS/MVP_SCOPE.md` §4.1
  - `RESEARCH_GAPS.md` G28

  Wave C should update them from `ARABIC_TOKEN_COST_MEASUREMENT.md` §0.

## Method (short)
1. **Token measurement.**
   - **Test set:** I wrote 18 parallel Arabic/English groups myself: MSA narration (plain, partial and full diacritics), suspect/witness dialogue in MSA + Gulf + Egyptian + Levantine, student argument (formal, informal dialect, Arabizi), evidence card (Western vs Eastern digits), JSON (UTF-8 vs \u-escaped), system prompt, UI strings.
   - **Tooling:** tiktoken 0.14.0, tokenizers 0.23.3 and sentencepiece 0.2.2, from pip.
   - **Tokenizers:** 11 Hugging Face tokenizers checked through the HF API for gating and licence. Only `tokenizer.json`/`tokenizer.model` were fetched, at a pinned sha. No model code was run and no HF token was used.
   - **Gated, so skipped:** Llama 3.1/4, Gemma 2/3, Jais-2-8B, Command-R7B-Arabic, Aya-Expanse.
   - **Prices:** read 2026-10-27 from Anthropic and OpenAI pricing pages.
2. **RTL tests.**
   - inkjs 2.4.0: npm `--ignore-scripts`; compiled and ran Arabic stories plus 21 edge cases.
   - Yarn Spinner: ysc 3.2.2 from NuGet, run on the official .NET 9.0.22 runtime (SHA-512 verified).
   - Twine: 2.12.1 source plus the four story-format `format.js` files. I built stories via the publish substitution and rendered them in headless Chromium (Playwright, network blocked).
   - Inky: 0.15.2 source, plus a render of its bundled Ace 1.2.6 against Ace 1.43.4.
   - A programmatic bidi reading-order test: 9 cases × 4 modes.
3. **Design evidence.**
   - Full texts read from author/course-hosted copies: O'Rourke 2014 and Lomas 2013.
   - Abstract pages read for the 2022–2026 hint, onboarding and help-seeking papers.
   - Game claims from official Steam news (via the Steam API) and the GDC Vault session page.
   - Metadata confirmed via Crossref and PubMed.
4. **Fonts and devices.**
   - Google Fonts METADATA.pb and OFL.txt per family.
   - fontTools coverage and WOFF2 subset audit, and a Chromium render at 16 px.
   - StatCounter country pages (Sep 2026).
   - WebKit storage policy and OFL-FAQ.
   - Official Polly and Google TTS voice lists, and HF licence metadata for open TTS models.

## Interpretations made while the owner was away
- **Token measurement test set.** The brief asked for "about 20 paired items". I made 34 items in 18 groups, so that dialect variants share one English reference. The brief also named Llama 3 and Gemma. Their official repos are gated, and accepting licence terms needs an account. I treated that as outside my authority. Instead I used Fanar-1 (Gemma-2 base) and Fanar-2 (Gemma-3 base) as openly licensed proxies. That the tokenizers are identical is my inference, and it is labelled as such.
- **Cost section.** I gave verified prices plus an illustrative per-session computation. However, I did NOT multiply vendor prices by my ratios for models whose tokenizer is unpublished (Claude, gpt-6.x). The doc says so explicitly.
- **Task-4 remnants** (fonts, devices, PWA, TTS) were placed in `RTL_AUTHORING_TOOL_TESTS.md` §8 rather than a new file. The brief limited my files.
- **Mobile evidence-count question.** I reframed it from "20 or 40 evidence items" to a comparison-tray limit plus grouping. I also added a new hypothesis, H6, because no published optimum exists.
- **H1–H5 changes are proposals.** They were written as additions; the original §7 table was not altered.

## Incident (self-reported)
- One command's `cd` into a scratch folder failed silently. Nine Google Fonts `*.OFL.txt` files were therefore briefly written into the library root.
- I moved them to my scratchpad within the same minute.
- No other team's files were touched. The root listing was checked afterwards and is clean.

## Blockers
- **OpenAlex:** the daily budget was exhausted (HTTP 429). I used Crossref, PubMed and publisher pages instead.
- **Blocked automated fetch:**
  - ACM DL and researchr.org: the "Designed to Fail" FDG 2026 paper.
  - UCL Discovery: Iacovides 2015 full text (403).
  - GDC Vault: login.
  - pure.tudelft.nl: connection reset via curl. WebFetch worked.
- **No API keys,** so these could not be measured:
  - Claude: `count_tokens` is free but needs a key.
  - gpt-6.x tokenizers: unpublished.
- **No GUI,** so these were not run interactively: the Inky Electron app and the Twine editor.
- **Azure TTS voice table** did not render.
- **Not read:** the dataset licence of Piper's Arabic voice (the GitHub repo states none) and the TTS vendors' output-rights terms.

## Unverified candidates (not catalogued)
- **Ahia et al. language list** for the 22 languages: the abstract does not list them.
- **Jais 2023 paper (arXiv 2308.16149):** fertility table. Crossref returned 404 for the arXiv DOI; only aggregator pages were seen.
- **Second Language (Arabic) Acquisition of LLMs via Progressive Vocabulary Expansion (arXiv 2412.12310)** and **Arabic Stable LM (arXiv 2412.04277):** seen in search results only.
- **Raza & Rasool 2025, "Beyond User Control: Exploring Hint System Design and Player Experience in Puzzle Games"** (IEEE ComTech, DOI 10.1109/comtech65062.2025.11034626): Crossref record exists, but there is no abstract and no readable page. Left out because no findings could be verified.
- **Teen-specific device ownership by OS in Arab countries:** no public survey found.

## Top 5 findings that should change ATHAR's design
1. **Arabic token premium ≈ 1.2×, not 3×.** That holds for current-generation tokenizers (o200k 1.18; Qwen/DeepSeek/Fanar 1.21–1.34; Mistral Tekken 1.09). Arabic-built tokenizers (Jais, ALLaM) reach 0.88×. The 2.3–2.6× premium survives only in 100k-class vocabularies (cl100k, phi-4). Model tier and context design dominate cost (~20× spread between price tiers).
2. **Formatting dominates language as a cost driver.** Full diacritics cost 2.3–5.9× and \u-escaped JSON costs 2.8–4.4×. Eastern digits add up to +60%. Hence the rules: UTF-8 raw JSON, Western digits in storage, no full vocalisation in model-facing text, and normalised player input.
3. **Engines accept Arabic; editors and templates do not.** inkjs and ysc handle Arabic identifiers and text. Inky (Ace 1.2.6) has no bidi, and Twine formats default to LTR, with Arabic variables broken in Harlowe and SugarCube. Yarn lets an undeclared, diacritic-mismatched variable run with a warning only. A mandatory normalisation gate is needed: no presentation forms, bidi marks or diacritics in identifiers.
4. **Bidi rules for the UI were tested:**
   - `<bdi>` around every inserted value: `dir="rtl"` alone misorders "Latin name + number".
   - `dir="rtl"`, never `auto`, on choices.
   - `nowrap` for IDs: `EV-014` broke across lines in 7 of 9 fonts.
5. **Hints should be offered, specific, and state-aware.**
   - The full texts show the negative O'Rourke effect is very small and concerns static, non-adaptive hints.
   - Newer evidence supports "point to the easiest available deduction" (Lynch 2024).
   - Developers ship penalty-free, solved-node-skipping ladders (Roottrees, Golden Idol Redux).
   - H1–H5 were refined and H6 (evidence-board density) was added.

## Top 5 open questions / gaps for human or expert review
1. Run `token_test_set.jsonl` through Claude `count_tokens` and one gpt-6.x call per item (needs keys). Re-measure on the real sample case and on real teen inputs after Experiment 1.
2. Accept the Llama and Gemma licence gates (owner decision), then re-run the script for those tokenizers.
3. **Human viewing and reading:**
   - Ingold's GDC 2022 "Burden of Proof" talk.
   - The ThinkyCon 2025 talks.
   - The FDG 2026 "Designed to Fail" paper (CC BY).
   - Iacovides 2015 full text.
   - Johnson 2018 (G21 remainder).
4. **Device tests:**
   - Inky desktop with Arabic.
   - iOS Safari and a low-end Android with the bidi fixtures and the font shortlist.
   - A 5–8 Arabic writer usability test of the form-based editor (G27).
5. **Arabic audio decision:** a human voice cast versus commercial TTS output-rights review (library 11). No open, commercially clear Arabic TTS model was found.
