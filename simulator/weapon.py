# weapon.py
"""
weapon.py
--------
Contains the Weapon class representing weapons in Fire Emblem Heroes.
"""

class Weapon:
    """
    Represents a weapon in Fire Emblem Heroes.

    Attributes:
        name (str): Name of the weapon.
        might (int): Attack power of the weapon.
        color (str): Color of the weapon (red, blue, green, or colorless).
        range (int): Range of the weapon (1 for melee, 2 for ranged).
    """
    def __init__(self, name, might, color, range=1):
        self.name = name
        self.might = might
        self.color = color
        self.range = range