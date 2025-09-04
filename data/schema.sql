-- SQLite schema for FEH simulator

CREATE TABLE IF NOT EXISTS units (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    hp INTEGER NOT NULL,
    atk INTEGER NOT NULL,
    spd INTEGER NOT NULL,
    defense INTEGER NOT NULL,
    res INTEGER NOT NULL,
    unit_type TEXT,
    image_url TEXT
);

CREATE TABLE IF NOT EXISTS weapons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    might INTEGER NOT NULL,
    color TEXT,
    range INTEGER,
    weapon_type TEXT,
    effective_against TEXT, -- comma-separated types
    image_url TEXT
);

CREATE TABLE IF NOT EXISTS skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    skill_type TEXT,
    effect_json TEXT -- for flexible effect storage
);

-- Link tables for unit-weapons and unit-skills
CREATE TABLE IF NOT EXISTS unit_weapons (
    unit_id INTEGER,
    weapon_id INTEGER,
    FOREIGN KEY(unit_id) REFERENCES units(id),
    FOREIGN KEY(weapon_id) REFERENCES weapons(id)
);

CREATE TABLE IF NOT EXISTS unit_skills (
    unit_id INTEGER,
    skill_id INTEGER,
    FOREIGN KEY(unit_id) REFERENCES units(id),
    FOREIGN KEY(skill_id) REFERENCES skills(id)
);
