# units.py
"""
units.py
--------
Contains the Unit class representing heroes/units in Fire Emblem Heroes.
"""

from weapon import Weapon  # Importing the Weapon class from the weapon module

class Unit:
    """
    Represents a hero/unit in Fire Emblem Heroes.

    Attributes:
        name (str): Name of the unit.
        hp (int): Maximum hit points.
        atk (int): Base attack stat.
        spd (int): Speed stat.
        defense (int): Defense stat.
        res (int): Resistance stat.
        weapons (list[Weapon]): List of possible weapons.
        equipped_weapon (Weapon): Currently equipped weapon.
    """
    def __init__(self, name, hp, atk, spd, defense, res, weapons=None):
        self.name = name
        self.hp = hp
        self.atk = atk
        self.spd = spd
        self.defense = defense
        self.res = res
        self.weapons = weapons if weapons else []
        self.equipped_weapon = self.weapons[0] if self.weapons else None

    def equip_weapon(self, weapon_name):
        """
        Equip a weapon by its name.

        Args:
            weapon_name (str): Name of the weapon to equip.
        """
        for w in self.weapons:
            if w.name == weapon_name:
                self.equipped_weapon = w
                return True
        return False

    def get_visible_atk(self):
        # TODO: Add buffs/debuffs if needed
        weapon_might = self.equipped_weapon.might if self.equipped_weapon else 0
        return self.atk + weapon_might

    def get_visible_def(self):
        # TODO: Add buffs/debuffs if needed
        return self.defense

    def get_visible_res(self):
        # TODO: Add buffs/debuffs if needed
        return self.res

    def get_advantage_mod(self, defender):
        # TODO: Implement weapon triangle logic
        return 0.0

    def get_effective_mod(self, defender):
        # TODO: Implement effectiveness logic
        return 0.0

    def get_staff_mod(self):
        # TODO: Implement staff mod logic
        if self.equipped_weapon and self.equipped_weapon.type == 'staff':
            return 0.5
        return 1.0

    def get_special_damage(self, base_damage):
        # TODO: Implement special damage logic
        return 0

    def get_fixed_damage(self, defender):
        # TODO: Implement fixed damage logic
        return 0

    def get_percent_reduction(self):
        # TODO: Implement percent reduction logic
        return 0.0

    def get_fixed_reduction(self):
        # TODO: Implement fixed reduction logic
        return 0

    @property
    def adaptive_damage(self):
        # Flag for adaptive damage (e.g., sword using lower of def/res)
        # Set this property as needed for units/weapons that use adaptive damage
        return getattr(self, '_adaptive_damage', False)

    @adaptive_damage.setter
    def adaptive_damage(self, value):
        self._adaptive_damage = value