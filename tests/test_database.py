import unittest
import os
from simulator.data_loader import FEHDatabase, DB_PATH

class TestFEHDatabase(unittest.TestCase):
    def setUp(self):
        # Use a temporary DB for testing
        self.test_db_path = str(DB_PATH).replace('feh.db', 'test_feh.db')
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
        self.db = FEHDatabase(db_path=self.test_db_path)

    def tearDown(self):
        self.db.close()
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)

    def test_add_and_get_unit(self):
        unit = {
            "name": "TestUnit",
            "hp": 40,
            "atk": 30,
            "spd": 35,
            "defense": 25,
            "res": 20,
            "unit_type": "infantry",
            "image_url": "http://example.com/unit.png"
        }
        unit_id = self.db.add_unit(unit)
        units = self.db.get_units()
        self.assertTrue(any(u["id"] == unit_id and u["name"] == "TestUnit" for u in units))

    def test_add_and_get_weapon(self):
        weapon = {
            "name": "TestSword",
            "might": 10,
            "color": "red",
            "range": 1,
            "weapon_type": "sword",
            "effective_against": "dragon",
            "image_url": "http://example.com/weapon.png"
        }
        weapon_id = self.db.add_weapon(weapon)
        weapons = self.db.get_weapons()
        self.assertTrue(any(w["id"] == weapon_id and w["name"] == "TestSword" for w in weapons))

    def test_add_and_get_skill(self):
        skill = {
            "name": "TestSkill",
            "description": "A test skill.",
            "skill_type": "special",
            "effect_json": "{}"
        }
        skill_id = self.db.add_skill(skill)
        skills = self.db.get_skills()
        self.assertTrue(any(s["id"] == skill_id and s["name"] == "TestSkill" for s in skills))

if __name__ == "__main__":
    unittest.main()
