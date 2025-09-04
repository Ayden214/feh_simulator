class Skill:
    def __init__(self, name, skill_type, description="", effect_json=None, movement_restrictions=None, weapon_restrictions=None, refinable=False):
        """
        Args:
            name (str): Name of the skill.
            skill_type (str): Slot/type (A, B, C, Seal, Assist, Special, X, etc).
            description (str): Human-readable description.
            effect_json (dict or str): Structured effect data (for advanced logic).
            movement_restrictions (list[str]): Allowed movement types (e.g. ["infantry", "armor"])
            weapon_restrictions (list[str]): Allowed weapon types (e.g. ["Sword", "Tome"])
        """
    self.name = name
    self.skill_type = skill_type
    self.description = description
    self.effect_json = effect_json if effect_json is not None else {}
    self.movement_restrictions = movement_restrictions if movement_restrictions is not None else []
    self.weapon_restrictions = weapon_restrictions if weapon_restrictions is not None else []
    self.refinable = refinable

    def is_usable_by(self, unit_movement, unit_weapon_type):
        """
        Returns True if the skill can be used by a unit with the given movement and weapon type.
        """
        if self.movement_restrictions and unit_movement not in self.movement_restrictions:
            return False
        if self.weapon_restrictions and unit_weapon_type not in self.weapon_restrictions:
            return False
        return True

    def __repr__(self):
        return f"<Skill {self.name} ({self.skill_type})>"
