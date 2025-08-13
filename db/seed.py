import csv, sqlite3, os

DB_PATH = "coach.db"
CSV_PATH = "data/exercices_master.csv"
SCHEMA_PATH = "db/schema.sql"

def ensure_db():
    with sqlite3.connect(DB_PATH) as conn, open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        conn.executescript(f.read())

def import_csv():
    if not os.path.exists(CSV_PATH):
        print(f"[seed] CSV not found: {CSV_PATH} — skip")
        return
    with sqlite3.connect(DB_PATH) as conn, open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        conn.execute("DELETE FROM exercises")
        for r in rows:
            conn.execute("""
            INSERT OR REPLACE INTO exercises (
              exercise_id, name, primary_muscle, secondary_muscles, movement_pattern, equipment,
              unilateral, plane, category, level, default_rep_range, default_sets, default_rest_sec,
              avg_rep_time_sec, cues, contraindications, tags, variants_of, image_path
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
              r["exercise_id"], r["name"], r["primary_muscle"], r["secondary_muscles"], r["movement_pattern"],
              r["equipment"], 1 if r["unilateral"].strip().lower() in ("1","true","yes") else 0,
              r["plane"], r["category"], r["level"], r["default_rep_range"],
              int(r["default_sets"] or 0), int(r["default_rest_sec"] or 0),
              float(r["avg_rep_time_sec"] or 2.5), r["cues"], r["contraindications"], r["tags"],
              r.get("variants_of") or None, r.get("image_path") or None
            ))
        conn.commit()
    print(f"[seed] Imported {len(rows)} exercises.")

if __name__ == "__main__":
    ensure_db()
    import_csv()
