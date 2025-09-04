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
        weapon_type (str): Type of weapon (e.g., sword, tome, staff).
        effects (list[callable]): List of effect functions to apply during simulation.
    """
    def __init__(self, name, might, color, range=1, weapon_type=None, effects=None):
        self.name = name
        self.might = might
        self.color = color
        self.range = range
        self.type = weapon_type  # for compatibility with previous code
        self.effects = effects if effects is not None else []

    def apply_effects(self, context):
        """
        Apply all weapon effects to the simulation context.
        Each effect should be a function that takes the context and modifies it.
        """
        for effect in self.effects:
            effect(context)