-- SQLite schema for optional SQL path
PRAGMA journal_mode=WAL;

CREATE TABLE IF NOT EXISTS registrations (
    id INTEGER PRIMARY KEY,
    date TEXT NOT NULL,                  -- ISO date (YYYY-MM-DD)
    vehicle_category TEXT NOT NULL,      -- 2W, 3W, 4W
    manufacturer TEXT NOT NULL,
    state TEXT,
    registrations INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_registrations_date ON registrations(date);
CREATE INDEX IF NOT EXISTS idx_registrations_cat ON registrations(vehicle_category);
CREATE INDEX IF NOT EXISTS idx_registrations_mfr ON registrations(manufacturer);