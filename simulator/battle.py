"""battle.py
Core battle simulation orchestration.

Provides simulate_battle which executes a single round of combat between two Units
and returns both a concise result and (optionally) a detailed step breakdown
aligned with the FEH damage calculation structure.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Callable, Tuple
from enum import Enum
class Phase(Enum):
    INIT = 'init'
    COUNTER = 'counter'
    FOLLOW_UP = 'follow_up'
    FOLLOW_UP_COUNTER = 'follow_up_counter'
    POTENT = 'potent'

@dataclass
class CombatContext:
    round_id: int = 0
    sequence_index: int = 0
    hit_index: int = 0
    is_first_attack: bool = False
    is_first_hit_of_unit: bool = False
    attacker: Any = None
    defender: Any = None
    phase: Phase = Phase.INIT
    trace: List['DamageStep'] = field(default_factory=list)

from .calculations import calculate_damage
from .units import Unit

@dataclass
class DamageStep:
    label: str
    value: Any
    note: str = ""

@dataclass
class AttackResult:
    attacker: str
    defender: str
    damage: int  # total damage of all hits in this attack sequence
    ko: bool
    hp_before: int
    hp_after: int
    hit_damages: List[int] = field(default_factory=list)  # individual hit damages
    steps: List[DamageStep] = field(default_factory=list)
    phase: str = ""  # e.g., 'init', 'counter', 'follow_up', 'follow_up_counter', 'potent'

@dataclass
class BattleResult:
    round_summary: List[AttackResult]
    winner: Optional[str]


def _as_bool_or_call(obj, *args):
    if callable(obj):
        return obj(*args)
    return bool(obj)



# --- Follow-up Determination Helpers ---
FOLLOW_UP_SPEED_THRESHOLD = 5  # Classic FEH threshold

def resolve_follow_ups(attacker: Unit, defender: Unit) -> Tuple[bool, bool]:
    """Unified follow-up resolution. Returns (attacker_follow_up, defender_follow_up)."""
    # Null Follow-Up style logic: guarantee > deny > speed
    att_guaranteed = _as_bool_or_call(getattr(attacker, 'has_guaranteed_follow_up', False), defender)
    def_guaranteed = _as_bool_or_call(getattr(defender, 'has_guaranteed_follow_up', False), attacker)
    att_denied = _as_bool_or_call(getattr(defender, 'denies_foe_follow_up', False), attacker)
    def_denied = _as_bool_or_call(getattr(attacker, 'denies_foe_follow_up', False), defender)
    att_spd = attacker.spd - defender.spd >= FOLLOW_UP_SPEED_THRESHOLD
    def_spd = defender.spd - attacker.spd >= FOLLOW_UP_SPEED_THRESHOLD

    attacker_follow_up = False
    defender_follow_up = False

    # Attacker follow-up
    if att_guaranteed:
        attacker_follow_up = True
    elif att_denied:
        attacker_follow_up = False
    elif att_spd:
        attacker_follow_up = True

    # Defender follow-up
    if def_guaranteed:
        defender_follow_up = True
    elif def_denied:
        defender_follow_up = False
    elif def_spd:
        defender_follow_up = True

    return attacker_follow_up, defender_follow_up

def _potent_extra(unit: Unit) -> bool:
    return getattr(unit, 'has_potent_follow_up', lambda: False)()


def simulate_battle(attacker: Unit, defender: Unit, options: Optional[Dict[str, Any]] = None) -> BattleResult:
    """Simulate a full combat round with all attack logic inside. Handles brave, follow-ups, potent, and context/trace."""
    if options is None:
        options = {}

    round_events: List[AttackResult] = []
    context = CombatContext(attacker=attacker, defender=defender)

    def do_attack(attacker, defender, phase):
        detailed = options.get("detailed", False)
        terrain = options.get("terrain")
        weapon_type = attacker.equipped_weapon.type if attacker.equipped_weapon else None
        adaptive = getattr(attacker, 'adaptive_damage', False)
        brave = _as_bool_or_call(getattr(attacker, 'has_brave_attack', False))
        steps: List[DamageStep] = []
        hit_damages: List[int] = []
        hp_before = defender.hp
        # First hit
        context.hit_index = 0
        dmg1 = calculate_damage(attacker, defender, weapon_type=weapon_type, terrain=terrain, adaptive_damage=adaptive)
        defender.hp = max(0, defender.hp - dmg1)
        hit_damages.append(dmg1)
        if detailed:
            steps.append(DamageStep(f"{phase.value}_Hit1", dmg1, "First hit damage"))
        context.trace.append(DamageStep(f"{phase.value}_Hit1", dmg1, "First hit damage"))
        # Brave second hit if defender survived
        if brave and defender.hp > 0:
            context.hit_index = 1
            dmg2 = calculate_damage(attacker, defender, weapon_type=weapon_type, terrain=terrain, adaptive_damage=adaptive)
            defender.hp = max(0, defender.hp - dmg2)
            hit_damages.append(dmg2)
            if detailed:
                steps.append(DamageStep(f"{phase.value}_Hit2", dmg2, "Second brave hit damage"))
            context.trace.append(DamageStep(f"{phase.value}_Hit2", dmg2, "Second brave hit damage"))
        total_damage = sum(hit_damages)
        if detailed:
            steps.append(DamageStep(f"{phase.value}_TotalDamage", total_damage, "Sum of all hits in sequence"))
        context.trace.append(DamageStep(f"{phase.value}_TotalDamage", total_damage, "Sum of all hits in sequence"))
        return AttackResult(
            attacker=attacker.name,
            defender=defender.name,
            damage=total_damage,
            ko=defender.hp == 0,
            hp_before=hp_before,
            hp_after=defender.hp,
            hit_damages=hit_damages,
            steps=steps,
            phase=phase.value,
        )

    # Initial attack
    first = do_attack(attacker, defender, Phase.INIT)
    round_events.append(first)

    # Defender counter if alive and (placeholder) can retaliate
    if not first.ko and defender.equipped_weapon:
        counter = do_attack(defender, attacker, Phase.COUNTER)
        round_events.append(counter)

    # Unified follow-up resolution
    att_follow_up, def_follow_up = resolve_follow_ups(attacker, defender)

    # Attacker follow-up
    if attacker.hp > 0 and defender.hp > 0 and att_follow_up:
        follow_up = do_attack(attacker, defender, Phase.FOLLOW_UP)
        round_events.append(follow_up)
        # Potent extra (attacker)
        if not follow_up.ko and defender.hp > 0 and _potent_extra(attacker):
            potent = do_attack(attacker, defender, Phase.POTENT)
            round_events.append(potent)

    # Defender follow-up
    if attacker.hp > 0 and defender.hp > 0 and def_follow_up:
        follow_up_counter = do_attack(defender, attacker, Phase.FOLLOW_UP_COUNTER)
        round_events.append(follow_up_counter)
        # Potent extra (defender)
        if not follow_up_counter.ko and attacker.hp > 0 and _potent_extra(defender):
            potent_def = do_attack(defender, attacker, Phase.POTENT)
            round_events.append(potent_def)

    # Determine winner (simple: whoever still has HP)
    winner = None
    if attacker.hp > 0 and defender.hp <= 0:
        winner = attacker.name
    elif defender.hp > 0 and attacker.hp <= 0:
        winner = defender.name

    return BattleResult(round_summary=round_events, winner=winner)

__all__ = [
    'simulate_battle',
    'simulate_attack',
    'BattleResult',
    'AttackResult',
    'DamageStep'
]
