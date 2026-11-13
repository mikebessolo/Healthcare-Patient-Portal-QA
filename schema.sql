CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS providers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id),
    provider_id INTEGER NOT NULL REFERENCES providers(id),
    visit_date TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'scheduled' CHECK(status IN ('scheduled','cancelled'))
);
-- Deliberately simplified capacity: one appointment per provider per day.
CREATE UNIQUE INDEX IF NOT EXISTS provider_capacity
ON appointments(provider_id, visit_date) WHERE status='scheduled';
INSERT OR IGNORE INTO patients VALUES(1,'Fictional Patient A'),(2,'Fictional Patient B');
INSERT OR IGNORE INTO providers VALUES(1,'Fictional Provider A'),(2,'Fictional Provider B');
