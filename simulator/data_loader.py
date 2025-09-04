import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "feh.db"
SCHEMA_PATH = Path(__file__).parent.parent / "data" / "schema.sql"

class FEHDatabase:
    def delete_unit(self, name):
        self.conn.execute("DELETE FROM units WHERE name = ?", (name,))
        self.conn.commit()

    def delete_weapon(self, name):
        self.conn.execute("DELETE FROM weapons WHERE name = ?", (name,))
        self.conn.commit()

    def delete_skill(self, name):
        self.conn.execute("DELETE FROM skills WHERE name = ?", (name,))
        self.conn.commit()
    def __init__(self, db_path=DB_PATH):
        self.db_path = str(db_path)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self):
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            schema = f.read()
        self.conn.executescript(schema)
        self.conn.commit()

    def get_units(self):
        cur = self.conn.execute("SELECT * FROM units")
        return [dict(row) for row in cur.fetchall()]

    def get_weapons(self):
        cur = self.conn.execute("SELECT * FROM weapons")
        return [dict(row) for row in cur.fetchall()]

    def get_skills(self):
        cur = self.conn.execute("SELECT * FROM skills")
        return [dict(row) for row in cur.fetchall()]

    def add_unit(self, unit):
        cur = self.conn.execute(
            """
            INSERT INTO units (name, hp, atk, spd, defense, res, unit_type, image_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (unit["name"], unit["hp"], unit["atk"], unit["spd"], unit["defense"], unit["res"], unit.get("unit_type"), unit.get("image_url"))
        )
        self.conn.commit()
        return cur.lastrowid

    def add_weapon(self, weapon):
        cur = self.conn.execute(
            """
            INSERT INTO weapons (name, might, color, range, weapon_type, effective_against)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (weapon["name"], weapon["might"], weapon.get("color"), weapon.get("range"), weapon.get("weapon_type"), weapon.get("effective_against"))
        )
        self.conn.commit()
        return cur.lastrowid

    def add_skill(self, skill):
        cur = self.conn.execute(
            """
            INSERT INTO skills (name, description, skill_type, effect_json)
            VALUES (?, ?, ?, ?)
            """,
            (skill["name"], skill.get("description"), skill.get("skill_type"), skill.get("effect_json"))
        )
        self.conn.commit()
        return cur.lastrowid

    def close(self):
        self.conn.close()
