"""
calculations.py
---------------
Contains the mathematical logic for battle damage calculations.
This is where FEH rules are implemented step-by-step.

For now, this is a simple damage calculation:
    Damage = max(0, Attacker's Effective ATK - Defender's DEF or RES)
"""

def calculate_damage(attacker, defender, weapon_type=None, terrain=None, adaptive_damage=False):
    """
    Calculate FEH battle damage following official structure.

    Args:
        attacker (Unit): The attacking unit.
        defender (Unit): The defending unit.
        weapon_type (str): Weapon type (e.g., 'sword', 'tome', 'staff').
        terrain (str): Terrain type (e.g., 'defensive', None).

    Returns:
        int: Final damage dealt (minimum 0).
    """
    # 1. Visible stats
    atk = attacker.get_visible_atk()
    # Adaptive damage: use lower of Def or Res if flag is set
    if adaptive_damage:
        defense_stat = min(defender.get_visible_def(), defender.get_visible_res())
    else:
        if weapon_type in ['tome', 'dragon', 'staff']:
            defense_stat = defender.get_visible_res()
        else:
            defense_stat = defender.get_visible_def()

    # 2. Weapon triangle advantage
    advantage_mod = attacker.get_advantage_mod(defender)
    atk = apply_advantage_mod(atk, advantage_mod)

    # 3. Effectiveness
    effective_mod = attacker.get_effective_mod(defender)
    atk = apply_effective_mod(atk, effective_mod)

    # 4. Terrain
    terrain_mod = get_terrain_mod(terrain)
    defense_stat = apply_terrain_mod(defense_stat, terrain_mod)

    # 5. Staff modifier
    staff_mod = attacker.get_staff_mod()

    # 6. Base damage
    base_damage = atk - defense_stat

    # 7. Special damage
    special_damage = attacker.get_special_damage(base_damage)
    base_damage += special_damage

    # 8. Fixed damage
    fixed_damage = attacker.get_fixed_damage(defender)
    base_damage += fixed_damage

    # 9. Percent reduction
    percent_reduction = defender.get_percent_reduction()
    base_damage = apply_percent_reduction(base_damage, percent_reduction)

    # 10. Fixed reduction
    fixed_reduction = defender.get_fixed_reduction()
    base_damage -= fixed_reduction

    # 11. Staff mod (applied after all additions/reductions)
    base_damage = int(base_damage * staff_mod)

    # 12. Floor/ceil and set negative to zero
    damage = max(0, int(base_damage))
    return damage

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
