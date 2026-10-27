// Core types for the ATHAR case engine. Mirrors content/schema/case_schema.json (library 10_TECHNICAL_ARCHITECTURE).
// The engine is pure TypeScript: no Next.js, no DB, no network.

export type Id = string;

export type Guard =
  | { has_evidence: Id }
  | { fact_unlocked: Id }
  | { presented: { evidence_id: Id; to_character: Id } }
  | { in_state: string }
  | { trust_at_least: { character_id: Id; level: number } }
  | { all: Guard[] }
  | { any: Guard[] }
  | { not: Guard }
  | { always: true };

export interface Fact {
  id: Id;
  statement_ar: string;
  kind: "event" | "state" | "attribute" | "relation" | "absence";
  subject_ids: Id[];
  time?: { start_min: number; end_min?: number; precision?: "exact" | "approx" | "unknown" };
  location_id?: Id;
  spoiler_level: 0 | 1 | 2 | 3;
  science_ko_refs?: string[];
}

export interface Claim {
  id: Id;
  statement_ar: string;
  kind: "lie" | "honest_mistake" | "rumour" | "half_truth";
  held_by: Id[];
  true_fact_id?: Id;
  contradicted_by_evidence_ids: Id[];
  unresolved_by_design?: boolean;
}

export interface AuthoredLine {
  line_id: Id;
  purpose:
    | "greeting"
    | "deflect_unknown"
    | "deflect_offtopic"
    | "refuse_secret"
    | "reveal"
    | "lie"
    | "break_down"
    | "farewell"
    | "safety_exit";
  text_ar: string;
  fact_ids?: Id[];
  claim_ids?: Id[];
}

export interface Character {
  id: Id;
  name_ar: string;
  aliases_ar?: string[];
  role: "suspect" | "witness" | "victim" | "expert" | "assistant" | "authority" | "bystander";
  age_descriptor_ar?: string;
  persona_ar: string;
  motives_ar: string[];
  speech_constraints?: {
    register?: "msa" | "msa_light_dialect" | "dialect";
    max_sentences_per_turn?: number;
    forbidden_topics_ar?: string[];
  };
  authored_lines?: AuthoredLine[];
}

export interface NamedEntity {
  id: Id;
  name_ar: string;
  name_en?: string;
  aliases_ar?: string[];
  description_ar?: string;
}

export interface EvidenceItem {
  id: Id;
  title_ar: string;
  kind: "physical" | "documentary" | "testimonial" | "digital" | "lab_result" | "observation";
  content_ar: string;
  media?: { uri: string; alt_ar: string; bytes?: number }[];
  acquired_by_action_ids: Id[];
  location_id?: Id;
  supports_fact_ids: Id[];
  contradicts_claim_ids?: Id[];
  reliability: "strong" | "moderate" | "weak";
  limits_ar: string;
  is_red_herring?: boolean;
  forensic_ko_ref?: string;
}

export interface Inference {
  id: Id;
  premises: { ref_type: "evidence" | "fact" | "inference" | "general_knowledge"; ref_id: string }[];
  conclusion: { ref_type: "fact" | "hypothesis" | "claim"; ref_id: Id };
  relation: "supports" | "establishes" | "refutes" | "rules_out" | "contradicts_claim";
  strength?: "conclusive" | "strong" | "suggestive";
  rule_ar: string;
  skill_ko_refs: string[];
}

export interface KnowledgeScope {
  character_id: Id;
  knows: {
    fact_id: Id;
    access: "witnessed" | "told_by" | "inferred" | "common_knowledge" | "professional";
    source_character_id?: Id;
    certainty?: "certain" | "fairly_sure" | "unsure";
    available_from_state?: string;
  }[];
  hides: { fact_id: Id; reveal_when: Guard; cover_claim_id: Id | null; reveal_line_id?: Id }[];
  believes: { claim_id: Id; stance: "sincere" | "deliberate_lie" }[];
  opinions_ar?: string[];
}

export interface Hypothesis {
  id: Id;
  statement_ar: string;
  is_true: boolean;
  plausibility_at_start: "high" | "medium" | "low";
  suspect_id?: Id;
}

export interface RedHerring {
  id: Id;
  points_to_hypothesis_id: Id;
  planted_via_ar: string;
  evidence_ids?: Id[];
  refuted_by_inference_ids: Id[];
  fairness_note_ar: string;
}

export interface LearningObjective {
  id: Id;
  statement_ar: string;
  skill_ko_ref: string;
  observable_behaviors_ar: string[];
  evidence_sources: string[];
}

export type ActionType =
  | "examine"
  | "search_location"
  | "interview"
  | "present_evidence"
  | "request_lab_test"
  | "compare_evidence"
  | "place_on_timeline"
  | "link_on_board"
  | "submit_hypothesis"
  | "rule_out"
  | "final_accusation"
  | "request_hint";

export interface Effect {
  op: "grant_evidence" | "unlock_fact" | "raise_trust" | "lower_trust" | "emit_event" | "advance_time";
  ref_id?: string;
  amount?: number;
}

export interface Action {
  id: Id;
  type: ActionType;
  label_ar: string;
  target_id?: Id;
  precondition: Guard;
  effects: Effect[];
  time_cost_units?: number;
  telemetry_code?: string;
}

export interface SmState {
  description_ar?: string;
  type?: "atomic" | "compound" | "parallel" | "final" | "history";
  initial?: string;
  states?: Record<string, SmState>;
  on?: Record<string, { target: string; guard?: Guard }>;
}

export interface Topic {
  id: Id;
  label_ar: string;
  example_questions_ar?: string[];
  fact_ids: Id[];
  claim_ids?: Id[];
}

export interface RubricCriterion {
  id: Id;
  name_ar: string;
  objective_ids: Id[];
  scored_by: "deterministic" | "llm_judge" | "llm_judge_with_human_moderation" | "human";
  weight?: number;
  levels: { score: number; descriptor_ar: string; anchor_examples_ar?: string[] }[];
}

export interface Hint {
  id: Id;
  level: 1 | 2 | 3 | 4 | 5;
  kind: "metacognitive" | "focus_area" | "pointer" | "partial_reveal" | "full_reveal";
  text_ar: string;
  trigger: Guard;
  targets_inference_id?: Id;
  assessment_weight?: number;
}

export interface Review {
  role:
    | "narrative_editor"
    | "scientific_reviewer"
    | "learning_designer"
    | "age_appropriateness"
    | "cultural_reviewer"
    | "legal_rights"
    | "safety";
  reviewer: string;
  status: "pending" | "changes_requested" | "approved";
  content_hash: string;
  date: string;
  notes_ar?: string;
}

export interface CaseFile {
  schema_version: string;
  case_id: Id;
  case_version: string;
  meta: {
    title_ar: string;
    title_en?: string;
    age_band: "13-15" | "16-18" | "18+" | "all";
    locale: string;
    dialogue_register?: "msa" | "msa_light_dialect" | "dialect";
    estimated_minutes: number;
    difficulty: number;
    content_flags: string[];
    authors: string[];
    knowledge_object_refs?: string[];
  };
  premise: {
    hook_ar: string;
    player_role_ar: string;
    setting_ar: string;
    public_fact_ids: Id[];
    assumed_general_knowledge_ar?: string[];
  };
  entities: {
    characters: Character[];
    locations: NamedEntity[];
    objects: NamedEntity[];
    organizations?: NamedEntity[];
  };
  truth: {
    solution: { culprit_ids: Id[]; summary_ar: string; key_fact_ids: Id[] };
    facts: Fact[];
    claims?: Claim[];
  };
  timeline: {
    id: Id;
    description_ar: string;
    time: { start_min: number; end_min?: number; precision?: string };
    location_id?: Id;
    actor_ids: Id[];
    witness_ids?: Id[];
    fact_ids: Id[];
    motivated_by_ar?: string;
    caused_by_event_ids?: Id[];
  }[];
  evidence: EvidenceItem[];
  evidence_graph: { inferences: Inference[] };
  character_knowledge: KnowledgeScope[];
  hypotheses: Hypothesis[];
  misdirection_plan?: RedHerring[];
  learning_objectives: LearningObjective[];
  mechanics: { time_budget_units?: number; actions: Action[] };
  state_machine: { id: string; initial: string; type?: string; states: Record<string, SmState> };
  dialogue?: { max_turns_per_interview?: number; llm_enabled?: boolean; topics?: Topic[] };
  rubric: { reference_answer_ar: string; criteria: RubricCriterion[] };
  hint_ladder: Hint[];
  fairness_test: {
    requirements: Record<string, unknown>;
    runs: { run_at: string; content_hash: string; tool: string; result: "pass" | "fail" | "error"; proof_paths_found?: number; failures?: string[]; simulated_conversations?: number; critical_violations?: number }[];
  };
  ending_explanation: {
    steps: { order: number; text_ar: string; uses_evidence_ids: Id[]; inference_id: Id }[];
    alternative_paths_ar?: string[];
    what_evidence_could_not_show_ar?: string[];
    science_notes_ar?: string[];
  };
  expert_review: Review[];
}

// ---- play state (what the server keeps per player per case; contains NO hidden truth) ----

export type SourceClass = "primary_record" | "redisplay" | "claim" | "template" | "public_document";
export type LinkDirection = "supports" | "weakens" | "neutral";

export interface HypothesisEntry {
  confidence: number | null; // 0..100, null = unset
  stance: "open" | "leading" | "ruled_out";
  links: Record<Id, LinkDirection>;
  revisions: { seq: number; kind: "added" | "confidence" | "stance" | "link"; detail: string; evidence_count: number }[];
  ruled_out_with?: Id[];
}

export interface TimelinePlacement {
  evidence_id: Id;
  utc_minute: number; // minutes since case epoch (t=0) in the player's normalised timeline
  note?: string;
}

export interface LabRun {
  seq: number;
  lab_id: Id;
  inputs: Record<string, number | string>;
  output: Record<string, unknown>;
  converged: boolean;
}

export interface Submission {
  conclusion_hypothesis_id: Id;
  confidence: number;
  cited: { evidence_id: Id; role: "supports" | "limits" | "rules_out" }[];
  limit_choice_ids: string[];
  would_change_mind_ids: string[];
  justification: string;
  seq: number;
}

export interface PlayState {
  v: 1;
  case_id: Id;
  case_version: string;
  machine: string; // top-level state
  sub: string | null;
  evidence: Id[];
  facts: Id[];
  trust: Record<Id, number>;
  events: string[];
  presented: { evidence_id: Id; to: Id }[];
  seq: number;
  log: { seq: number; action: string; target?: string }[];
  hypotheses: Record<Id, HypothesisEntry>;
  source_tags: Record<Id, SourceClass>;
  timeline: TimelinePlacement[];
  lab_runs: LabRun[];
  hints: { seq: number; hint_id: Id; level: number }[];
  journal: { seq: number; text: string }[];
  interviews: Record<Id, { turns: number; asked: Id[] }>;
  transcript: { seq: number; char_id: Id; topic_id: Id; line_ids: Id[] }[];
  submission?: Submission;
  transfer?: { picked: string[]; free_text: string; seq: number };
  review_ticket?: string;
  started_at: string;
  updated_at: string;
}
