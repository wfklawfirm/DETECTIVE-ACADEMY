CREATE TABLE IF NOT EXISTS lesson_progress (
  user_id    TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  lesson_id  TEXT NOT NULL,
  done_at    TEXT NOT NULL,
  PRIMARY KEY (user_id, lesson_id)
);
CREATE INDEX IF NOT EXISTS idx_lp_user ON lesson_progress(user_id);
