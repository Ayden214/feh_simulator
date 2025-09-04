"""
units.py
--------
Now includes Weapon class so units can switch weapons dynamically.
"""

class Weapon:
    """
    Represents a weapon in Fire Emblem Heroes.

    Attributes:
        name (str): Weapon name.
        might (int): Attack power of the weapon.
        color (str): Weapon color (red, blue, green, colorless).
        range (int): Weapon range (1 for melee, 2 for ranged).
    """
    def __init__(self, name, might, color, range=1):
        self.name = name
        self.might = might
        self.color = color
        self.range = range


class Unit:
    """
    Represents a hero/unit in Fire Emblem Heroes.

    Attributes:
        name (str): Unit's name.
        hp (int): Max hit points.
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

    def effective_attack(self):
        """
        Calculate attack stat with equipped weapon.
        Returns:
            int: Total attack value.
        """
        weapon_might = self.equipped_weapon.might if self.equipped_weapon else 0
        return self.atk + weapon_might
