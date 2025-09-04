"""
units.py
--------
Defines core data structures for units (heroes) in Fire Emblem Heroes.
Each Unit object holds stats, weapon details, and attributes.
"""

class Unit:
    """
    Represents a hero/unit in Fire Emblem Heroes.

    Attributes:
        name (str): Unit's display name.
        hp (int): Hit Points (max HP).
        atk (int): Base Attack stat.
        spd (int): Speed stat (affects follow-ups).
        defense (int): Defense stat.
        res (int): Resistance stat.
        weapon_mt (int): Weapon might (attack power of weapon).
        weapon_color (str): Color type (red, blue, green, colorless).
    """
    def __init__(self, name, hp, atk, spd, defense, res, weapon_mt=0, weapon_color=None):
        self.name = name
        self.hp = hp
        self.atk = atk
        self.spd = spd
        self.defense = defense
        self.res = res
        self.weapon_mt = weapon_mt
        self.weapon_color = weapon_color

    def effective_attack(self):
        """
        Calculate the effective attack stat by adding base attack
        to weapon might (ignores skills and bonuses for now).

        Returns:
            int: Total attack stat.
        """
        return self.atk + self.weapon_mt
