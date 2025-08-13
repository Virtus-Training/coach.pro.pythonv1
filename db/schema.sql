CREATE TABLE IF NOT EXISTS exercises (
  exercise_id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  primary_muscle TEXT,
  secondary_muscles TEXT,
  movement_pattern TEXT,
  equipment TEXT,
  unilateral INTEGER,
  plane TEXT,
  category TEXT,
  level TEXT,
  default_rep_range TEXT,
  default_sets INTEGER,
  default_rest_sec INTEGER,
  avg_rep_time_sec REAL,
  cues TEXT,
  contraindications TEXT,
  tags TEXT,
  variants_of TEXT,
  image_path TEXT
);
CREATE TABLE IF NOT EXISTS sessions (
  session_id TEXT PRIMARY KEY,
  mode TEXT NOT NULL,             -- COLLECTIF / INDIVIDUEL
  label TEXT,
  duration_sec INTEGER,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS session_blocks (
  block_id TEXT PRIMARY KEY,
  session_id TEXT NOT NULL REFERENCES sessions(session_id) ON DELETE CASCADE,
  type TEXT,
  duration_sec INTEGER,
  rounds INTEGER,
  work_sec INTEGER,
  rest_sec INTEGER,
  title TEXT,
  locked INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS session_items (
  item_id INTEGER PRIMARY KEY AUTOINCREMENT,
  block_id TEXT NOT NULL REFERENCES session_blocks(block_id) ON DELETE CASCADE,
  exercise_id TEXT,
  prescription TEXT,  -- JSON (clé=valeur)
  notes TEXT
);

