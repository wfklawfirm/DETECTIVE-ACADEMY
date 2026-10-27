-- ATHAR schema v1. Hidden case truth lives only in case_versions (server-side); play_states never contain it.
CREATE TABLE IF NOT EXISTS schema_migrations (version TEXT PRIMARY KEY, applied_at TEXT NOT NULL);

CREATE TABLE users (
  id            TEXT PRIMARY KEY,
  email         TEXT NOT NULL UNIQUE COLLATE NOCASE,
  pass_hash     TEXT NOT NULL,
  display_name  TEXT,
  role          TEXT NOT NULL DEFAULT 'player' CHECK (role IN ('player','editor','reviewer','admin')),
  adult_confirmed INTEGER NOT NULL DEFAULT 0 CHECK (adult_confirmed IN (0,1)),
  gentle_hooks  INTEGER NOT NULL DEFAULT 0 CHECK (gentle_hooks IN (0,1)),
  created_at    TEXT NOT NULL,
  deleted_at    TEXT
);

CREATE TABLE sessions (
  id_hash    TEXT PRIMARY KEY,
  user_id    TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  created_at TEXT NOT NULL,
  expires_at TEXT NOT NULL,
  ip_hash    TEXT
);
CREATE INDEX idx_sessions_user ON sessions(user_id);

CREATE TABLE case_versions (
  case_id      TEXT NOT NULL,
  version      TEXT NOT NULL,
  content_hash TEXT NOT NULL,
  status       TEXT NOT NULL DEFAULT 'draft' CHECK (status IN ('draft','in_review','approved','published','retired')),
  core_json    TEXT NOT NULL,
  ui_json      TEXT NOT NULL,
  scoring_json TEXT NOT NULL,
  qa_json      TEXT,
  created_by   TEXT,
  created_at   TEXT NOT NULL,
  PRIMARY KEY (case_id, version)
);

CREATE TABLE case_reviews (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  case_id      TEXT NOT NULL,
  version      TEXT NOT NULL,
  role         TEXT NOT NULL CHECK (role IN ('narrative_editor','scientific_reviewer','learning_designer','age_appropriateness','cultural_reviewer','legal_rights','safety')),
  reviewer_id  TEXT NOT NULL REFERENCES users(id),
  status       TEXT NOT NULL CHECK (status IN ('pending','changes_requested','approved')),
  content_hash TEXT NOT NULL,
  notes        TEXT,
  created_at   TEXT NOT NULL,
  FOREIGN KEY (case_id, version) REFERENCES case_versions(case_id, version) ON DELETE CASCADE
);
CREATE INDEX idx_reviews_case ON case_reviews(case_id, version);

CREATE TABLE play_states (
  user_id    TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  case_id    TEXT NOT NULL,
  state_json TEXT NOT NULL,
  machine    TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  PRIMARY KEY (user_id, case_id)
);

CREATE TABLE review_tickets (
  code          TEXT PRIMARY KEY,
  user_id       TEXT REFERENCES users(id) ON DELETE SET NULL,
  case_id       TEXT NOT NULL,
  case_version  TEXT NOT NULL,
  justification TEXT NOT NULL,
  deterministic_json TEXT NOT NULL,
  status        TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending','reviewed','dismissed')),
  reviewer_id   TEXT REFERENCES users(id),
  level         INTEGER CHECK (level BETWEEN 0 AND 4),
  feedback_ar   TEXT,
  created_at    TEXT NOT NULL,
  reviewed_at   TEXT
);
CREATE INDEX idx_tickets_status ON review_tickets(status, created_at);

CREATE TABLE audit_log (
  id        INTEGER PRIMARY KEY AUTOINCREMENT,
  at        TEXT NOT NULL,
  actor_id  TEXT,
  action    TEXT NOT NULL,
  target    TEXT,
  detail    TEXT,
  ip_hash   TEXT
);
CREATE INDEX idx_audit_at ON audit_log(at);

CREATE TABLE content_reports (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id    TEXT REFERENCES users(id) ON DELETE SET NULL,
  case_id    TEXT,
  kind       TEXT NOT NULL CHECK (kind IN ('safety','rights','error','other')),
  body       TEXT NOT NULL,
  status     TEXT NOT NULL DEFAULT 'open' CHECK (status IN ('open','triaged','closed')),
  created_at TEXT NOT NULL
);

CREATE TABLE hook_events (
  id       INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id  TEXT REFERENCES users(id) ON DELETE CASCADE,
  hook_id  TEXT NOT NULL,
  surface  TEXT NOT NULL,
  shown_at TEXT NOT NULL
);
CREATE INDEX idx_hook_user ON hook_events(user_id, shown_at);
