"""
calculations.py
---------------
Contains the mathematical logic for battle damage calculations.
This is where FEH rules are implemented step-by-step.

For now, this is a simple damage calculation:
    Damage = max(0, Attacker's Effective ATK - Defender's DEF or RES)
"""

class SimulationContext:
    def __init__(self, attacker, defender):
        self.attacker = attacker
        self.defender = defender
        self.damage = 0
        self.log = []
        # Add other fields as needed (e.g., turn, phase, terrain, etc.)

    def add_log(self, message):
        self.log.append(message)

def calculate_damage(attacker, defender, weapon_type=None, terrain=None, adaptive_damage=False):
    """
    Calculate FEH battle damage following official structure.
    """
    context = SimulationContext(attacker, defender)

    # Apply weapon effects (attacker)
    if hasattr(attacker, 'equipped_weapon') and attacker.equipped_weapon:
        attacker.equipped_weapon.apply_effects(context)
    # Apply skill effects (attacker)
    if hasattr(attacker, 'equipped_skills'):
        for skill in attacker.equipped_skills.values():
            if skill:
                skill.apply_effects(context)
    # Apply weapon effects (defender)
    if hasattr(defender, 'equipped_weapon') and defender.equipped_weapon:
        defender.equipped_weapon.apply_effects(context)
    # Apply skill effects (defender)
    if hasattr(defender, 'equipped_skills'):
        for skill in defender.equipped_skills.values():
            if skill:
                skill.apply_effects(context)


    # 1. Visible stats
    atk = attacker.atk
    # Weapon might
    if hasattr(attacker, 'equipped_weapon') and attacker.equipped_weapon:
        atk += attacker.equipped_weapon.might

    # 2. Defensive stat
    if adaptive_damage:
        defense_stat = min(defender.defense, defender.res)
    else:
        # Use res for tome, dragon, staff; else defense
        wtype = weapon_type or (attacker.equipped_weapon.weapon_type if hasattr(attacker, 'equipped_weapon') and attacker.equipped_weapon else None)
        if wtype and wtype.lower() in ['tome', 'dragon', 'staff']:
            defense_stat = defender.res
        else:
            defense_stat = defender.defense

    # 3. Weapon triangle advantage (simple version)
    advantage_mod = 0
    if hasattr(attacker, 'equipped_weapon') and attacker.equipped_weapon and hasattr(defender, 'equipped_weapon') and defender.equipped_weapon:
        att_color = getattr(attacker.equipped_weapon, 'color', None)
        def_color = getattr(defender.equipped_weapon, 'color', None)
        triangle = {('red', 'green'): 0.2, ('green', 'blue'): 0.2, ('blue', 'red'): 0.2,
                    ('green', 'red'): -0.2, ('blue', 'green'): -0.2, ('red', 'blue'): -0.2}
        advantage_mod = triangle.get((att_color, def_color), 0)
    atk = int(atk * (1 + advantage_mod))

    # 4. Effectiveness (stub: always 0)
    effective_mod = 0
    atk = int(atk * (1 + effective_mod))

    # 5. Terrain
    terrain_mod = 0.3 if terrain == 'defensive' or getattr(defender, 'on_defensive_tile', False) else 0.0
    defense_stat = int(defense_stat * (1 + terrain_mod))

    # 6. Staff modifier (stub: always 1)
    staff_mod = 1

    # 7. Special damage (stub: always 0)
    special_damage = 0
    # Example: Moonbow
    if getattr(attacker, 'special', None) == 'Moonbow':
        defense_stat = int(defense_stat * 0.7)

    # 8. Fixed damage (stub: always 0)
    fixed_damage = 0

    # 9. Percent reduction (stub: always 0)
    percent_reduction = 0
    # 10. Fixed reduction (stub: always 0)
    fixed_reduction = 0

    # 11. Calculate base damage
    base_damage = atk - defense_stat + special_damage + fixed_damage
    base_damage = int(base_damage * staff_mod)
    base_damage = int(base_damage * (1 - percent_reduction))
    base_damage -= fixed_reduction

    # 12. Floor/ceil and set negative to zero
    damage = max(0, int(base_damage))

    # Hooks for healing/recoil (not implemented)
    # attacker.apply_healing(damage)
    # attacker.apply_recoil(damage)

    # At the end, set context.damage and return it
    context.damage = damage

    # For demonstration, just return context.damage and context.log
    return context.damage, context.log

# Helper functions (to be implemented)
def apply_advantage_mod(atk, mod):
    if mod > 0:
        return int(atk * (1 + mod))
    elif mod < 0:
        return int(atk * (1 + mod))
    return atk

def apply_effective_mod(atk, mod):
    if mod > 0:
        return int(atk * (1 + mod))
    return atk

def get_terrain_mod(terrain):
    if terrain == 'defensive':
        return 0.3
    return 0.0

def apply_terrain_mod(def_stat, mod):
    return int(def_stat * (1 + mod))

def apply_percent_reduction(damage, reduction):
    if reduction > 0:
        return int(damage * (1 - reduction))
    return damage
