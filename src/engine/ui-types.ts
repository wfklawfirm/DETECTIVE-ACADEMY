import type { Id } from "./types";

/** Player-facing presentation sidecar (content/cases/<id>.ui.json). Safe to send to the browser. */
export interface TimeNormalizerLab {
  id: Id;
  type: "time_normalizer";
  title_ar: string;
  intro_ar: string;
  tolerance_min: number;
  /** Optional: day 0 = the day of t=0. */
  items: { evidence_id: Id; label_ar: string; day: number; hhmm: string; end_hhmm?: string; basis_ar?: string }[];
  /** Evidence granted when every item normalises to the same instant (or window) within tolerance. */
  grants_evidence_on_converge?: Id;
  /** Days labels so display never needs a calendar: index -> label. */
  day_labels_ar: string[];
  /** Epoch of t=0 expressed as UTC clock minute-of-day (e.g. 21:00 UTC => 1260) and the label shown. */
  epoch_utc_minute_of_day: number;
}

export type LabDef = TimeNormalizerLab;

export interface TransferOption { id: Id; text_ar: string }
export interface TransferTask {
  id: Id;
  title_ar: string;
  scenario_ar: string;
  documents: { title_ar: string; body_ar: string }[];
  prompt_ar: string;
  options: TransferOption[]; // multi-select of verification steps (valid + distractors); key is private
  free_text_prompt_ar: string;
}

export interface MenuItem { id: Id; label_ar: string }

export interface CaseUi {
  case_id: Id;
  tutorial?: boolean;
  /** Wall-clock meaning of timeline minute 0, shown to the player when placing evidence on the timeline. */
  clock: { epoch_hhmm: string; zone_label_ar: string };
  cover: { title_ar: string; tagline_ar: string; kicker_ar: string; glyph: string; accent: "amber" | "cyan" | "rose" | "green" };
  cold_open_ar: string[];
  labs: LabDef[];
  source_classes: { id: string; label_ar: string; help_ar: string }[];
  limit_menu: MenuItem[];
  mind_change_menu: MenuItem[];
  transfer?: TransferTask;
  skills: { skill_id: string; track: string }[];
  stage_hooks_ar: Record<string, string>; // machine state -> cliffhanger line shown on entering the stage
  character_glyphs?: Record<Id, string>;
}

/** Server-only scoring sidecar (content/cases/<id>.scoring.json). Never sent to clients. */
export interface ScoringSpec {
  case_id: Id;
  accepted_conclusions: Record<Id, { grade: number; note_ar: string }>;
  confidence_band: Record<Id, [number, number]>; // hypothesis -> allowed confidence range (0..100) for full calibration credit
  source_key: Record<Id, string>; // evidence -> SourceClass
  link_key: Record<Id, Record<Id, "supports" | "weakens" | "neutral">>; // hypothesis -> evidence -> direction
  required_limits: Id[]; // ids in ui.limit_menu that must be chosen
  valid_mind_changers: Id[]; // ids in ui.mind_change_menu that are genuinely discriminating
  invalid_limits: Id[];
  decisive_evidence: Id[]; // evidence that a sound final argument must cite
  lab_requirement: { lab_id: Id; must_converge: boolean } | null;
  timeline_requirement?: { evidence_id: Id; utc_minute: number; tol: number }[];
  refuted_hypotheses: Id[]; // hypotheses that decisive evidence refutes (for revision criterion)
  criteria_map: Record<Id, "source_typing" | "conflict_resolution" | "hypothesis_links" | "uncertainty" | "revision" | "elimination" | "justification_human">;
  transfer_key?: { valid: Id[]; invalid: Id[] };
  caps: { no_citations_max: number; no_conflict_resolution_max: number };
}
