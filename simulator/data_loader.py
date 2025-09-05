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
        cur = self.conn.execute("SELECT * FROM units ORDER BY name COLLATE NOCASE ASC")
        return [dict(row) for row in cur.fetchall()]

    def get_weapons(self):
        cur = self.conn.execute("SELECT * FROM weapons ORDER BY name COLLATE NOCASE ASC")
        return [dict(row) for row in cur.fetchall()]

    def get_skills(self):
        cur = self.conn.execute("SELECT * FROM skills ORDER BY name COLLATE NOCASE ASC")
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

    def update_unit(self, old_name, unit):
        self.conn.execute(
            """
            UPDATE units SET
                name = ?,
                hp = ?,
                atk = ?,
                spd = ?,
                defense = ?,
                res = ?,
                unit_type = ?,
                weapon_type = ?,
                image_url = ?
            WHERE name = ?
            """,
            (
                unit["name"],
                unit["hp"],
                unit["atk"],
                unit["spd"],
                unit["defense"],
                unit["res"],
                unit.get("unit_type"),
                unit.get("weapon_type"),
                unit.get("image_url"),
                old_name
            )
        )
        self.conn.commit()

    def get_all_weapons(self):
        cur = self.conn.execute('SELECT * FROM weapons ORDER BY name ASC')
        return [dict(row) for row in cur.fetchall()]

    def get_weapon_by_name(self, name):
        cur = self.conn.execute('SELECT * FROM weapons WHERE name = ?', (name,))
        return dict(cur.fetchone()) if cur.fetchone() else None

    def update_weapon(self, old_name, weapon):
        self.conn.execute(
            """
            UPDATE weapons SET
                name = ?,
                might = ?,
                color = ?,
                range = ?,
                weapon_type = ?,
                effective_against = ?
            WHERE name = ?
            """,
            (
                weapon["name"],
                weapon["might"],
                weapon.get("color"),
                weapon.get("range"),
                weapon.get("weapon_type"),
                weapon.get("effective_against"),
                old_name
            )
        )
        self.conn.commit()

    def get_weapon_types(self):
        # List of all weapon types for dropdown
        return [
            "Sword", "Lance", "Axe", "Staff", "RedBow", "BlueBow", "GreenBow", "ColorlessBow",
            "RedDagger", "BlueDagger", "GreenDagger", "ColorlessDagger",
            "RedTome", "BlueTome", "GreenTome", "ColorlessTome",
            "RedBeast", "BlueBeast", "GreenBeast", "ColorlessBeast",
            "RedBreath", "BlueBreath", "GreenBreath", "ColorlessBreath"
        ]

    def close(self):
        self.conn.close()

def get_all_weapons():
    db = FEHDatabase()
    weapons = db.get_all_weapons()
    db.close()
    return weapons

def get_weapon_by_name(name):
    db = FEHDatabase()
    weapon = db.get_weapon_by_name(name)
    db.close()
    return weapon

def update_weapon(old_name, new_name, might, color, range_, weapon_type, effective_against):
    db = FEHDatabase()
    weapon = {
        "name": new_name,
        "might": might,
        "color": color,
        "range": range_,
        "weapon_type": weapon_type,
        "effective_against": effective_against
    }
    db.update_weapon(old_name, weapon)
    db.close()

def get_weapon_types():
    db = FEHDatabase()
    types = db.get_weapon_types()
    db.close()
    return types

def delete_weapon(name):
    db = FEHDatabase()
    db.delete_weapon(name)
    db.close()
