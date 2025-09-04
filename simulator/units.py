# units.py
"""
units.py
--------
Contains the Unit class representing heroes/units in Fire Emblem Heroes.
"""

from .weapon import Weapon  # Importing the Weapon class from the weapon module

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
        superboons (list[str]): List of stats with superboons.
        superbanes (list[str]): List of stats with superbanes.
        exclusive_skills (list[str]): List of exclusive skill names.
        image_url (str): Link to unit image.
        unit_type (str): Movement type (infantry, armor, flier, cavalry).
        weapon_type (str): Weapon type for filtering (sword, lance, axe, etc.).
    """
    def __init__(
        self,
        name,
        hp,
        atk,
        spd,
        defense,
        res,
        superboons=None,
        superbanes=None,
        exclusive_skills=None,
        image_url="",
        unit_type="",
        weapon_type=""
    ):
        self.name = name
        self.hp = hp
        self.atk = atk
        self.spd = spd
        self.defense = defense
        self.res = res
        self.superboons = superboons if superboons else []
        self.superbanes = superbanes if superbanes else []
        self.exclusive_skills = exclusive_skills if exclusive_skills else []
        self.image_url = image_url
        self.unit_type = unit_type
        self.weapon_type = weapon_type  # Added for filtering purposes


    def __repr__(self):
        return f"<Unit {self.name}>"