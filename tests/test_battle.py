import unittest
from simulator.units import Unit
from simulator.weapon import Weapon
from simulator.battle import simulate_battle, BattleResult

class TestBattleSimulation(unittest.TestCase):
    def setUp(self):
        # Basic sword and tome weapons
        self.sword = Weapon(name="Iron Sword", might=10, color="red", range=1, weapon_type="sword")
        self.tome = Weapon(name="Fire", might=8, color="blue", range=2, weapon_type="tome")

        # Attacker: fast sword unit
        self.attacker = Unit(name="Eliwood", hp=40, atk=30, spd=40, defense=25, res=20, weapons=[self.sword])
        self.attacker.equip_weapon("Iron Sword")

        # Defender: slow mage
        self.defender = Unit(name="Lute", hp=35, atk=32, spd=25, defense=15, res=30, weapons=[self.tome])
        self.defender.equip_weapon("Fire")

    def test_basic_attack(self):
        # No follow-ups, no brave, just a single round
        result: BattleResult = simulate_battle(self.attacker, self.defender)
        self.assertEqual(result.round_summary[0].attacker, "Eliwood")
        self.assertEqual(result.round_summary[0].defender, "Lute")
        self.assertTrue(result.round_summary[0].damage > 0)
        self.assertEqual(result.round_summary[0].phase, "init")

    def test_speed_follow_up(self):
        # Attacker should get a speed-based follow-up
        result: BattleResult = simulate_battle(self.attacker, self.defender)
        phases = [r.phase for r in result.round_summary]
        self.assertIn("follow_up", phases)

    def test_brave_attack(self):
        # Attacker gets brave effect
        self.attacker.has_brave_attack = lambda: True
        result: BattleResult = simulate_battle(self.attacker, self.defender)
        # Should have two hits in init phase
        init_hits = [r.hit_damages for r in result.round_summary if r.phase == "init"]
        self.assertTrue(any(len(hits) == 2 for hits in init_hits))

    def test_guaranteed_follow_up(self):
        # Attacker gets guaranteed follow-up
        self.attacker.has_guaranteed_follow_up = lambda foe=None: True
        result: BattleResult = simulate_battle(self.attacker, self.defender)
        phases = [r.phase for r in result.round_summary]
        self.assertIn("follow_up", phases)

    def test_follow_up_denied(self):
        # Defender denies foe's follow-up
        self.defender.denies_foe_follow_up = lambda foe=None: True
        result: BattleResult = simulate_battle(self.attacker, self.defender)
        phases = [r.phase for r in result.round_summary]
        self.assertNotIn("follow_up", phases)

if __name__ == "__main__":
    unittest.main()
