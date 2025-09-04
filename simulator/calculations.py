"""
calculations.py
---------------
Contains the mathematical logic for battle damage calculations.
This is where FEH rules are implemented step-by-step.

For now, this is a simple damage calculation:
    Damage = max(0, Attacker's Effective ATK - Defender's DEF or RES)
"""

def calculate_damage(attacker, defender, magical=False):
    """
    Calculate the damage dealt by one unit to another.

    Args:
        attacker (Unit): The attacking unit.
        defender (Unit): The defending unit.
        magical (bool): If True, damage uses defender's Resistance (RES).
                        If False, uses Defense (DEF).

    Returns:
        int: Final damage dealt (minimum 0).
    """
    atk = attacker.effective_attack()
    defense_stat = defender.res if magical else defender.defense
    damage = max(0, atk - defense_stat)
    return damage
