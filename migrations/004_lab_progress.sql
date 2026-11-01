CREATE TABLE IF NOT EXISTS lab_progress (
  user_id    TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  lab_id     TEXT NOT NULL,
  done_at    TEXT NOT NULL,
  PRIMARY KEY (user_id, lab_id)
);
CREATE INDEX IF NOT EXISTS idx_labp_user ON lab_progress(user_id);
