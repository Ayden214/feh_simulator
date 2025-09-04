def unit_to_dict(u):
    return {
        'name': u.name,
        'hp': u.hp,
        'atk': u.atk,
        'spd': u.spd,
        'defense': u.defense,
        'res': u.res,
        'superboons': u.superboons,
        'superbanes': u.superbanes,
        'exclusive_skills': u.exclusive_skills,
        'image_url': u.image_url,
        'unit_type': u.unit_type,
        'weapon_type': u.weapon_type
    }
"""
routes.py
---------
Defines the URL routes (pages) for the FEH simulator web app.
Handles rendering templates, receiving form data, and calling
battle calculation functions from the simulator module.
"""

from flask import Blueprint, render_template, request
from simulator.calculations import calculate_damage
from simulator.units import Unit
from simulator.data_loader import FEHDatabase

# Create a Blueprint to group related routes
# This keeps our app modular and easier to scale
main = Blueprint("main", __name__)


def get_units_from_db():
    db = FEHDatabase()
    units = db.get_units()
    weapons = db.get_weapons()
    db.close()
    # Map weapons to units (simple: first weapon)
    unit_objs = []
    for u in units:
        uw = [w for w in weapons if w['id'] in [u.get('weapon_id')] if u.get('weapon_id')]
        weapon = None
        if uw:
            weapon = uw[0]
        # Create Unit object
        unit_obj = Unit(
            name=u['name'],
            hp=u['hp'],
            atk=u['atk'],
            spd=u['spd'],
            defense=u['defense'],
            res=u['res'],
            superboons=u.get('superboons', []),
            superbanes=u.get('superbanes', []),
            exclusive_skills=u.get('exclusive_skills', []),
            image_url=u.get('image_url', ''),
            unit_type=u.get('unit_type', ''),
            weapon_type=u.get('weapon_type', '')
        )
        # Attach weapon info if available
        if weapon:
            unit_obj.equipped_weapon = weapon
        unit_objs.append(unit_obj)
    return unit_objs

@main.route("/", methods=["GET", "POST"])
def index():
    """
    Homepage route: Displays a form to select an attacker and defender,
    runs the battle simulation, and returns results.

    Methods:
        GET: Shows the empty form.
        POST: Processes the form, calculates damage, and displays results.

    Returns:
        HTML page rendered from templates/index.html with optional result data.
    """
    result = None
    units = get_units_from_db()
    # Convert Unit objects to dicts for template (for tojson)
    units_for_template = [unit_to_dict(u) for u in units]
    db = FEHDatabase()
    weapons = db.get_weapons()
    skills = db.get_skills()
    db.close()

    if request.method == "POST":
        attacker_name = request.form.get("attacker")
        defender_name = request.form.get("defender")
        attacker_weapon_name = request.form.get("attacker_weapon")
        defender_weapon_name = request.form.get("defender_weapon")
        attacker = next((u for u in units if u.name == attacker_name), None)
        defender = next((u for u in units if u.name == defender_name), None)
        attacker_weapon = next((w for w in weapons if w['name'] == attacker_weapon_name), None)
        defender_weapon = next((w for w in weapons if w['name'] == defender_weapon_name), None)
        # Skill slots
        skill_slots = ['assist', 'special', 'a', 'b', 'c', 'seal', 'x']
        for slot in skill_slots:
            attacker_skill_name = request.form.get(f'attacker_{slot}')
            defender_skill_name = request.form.get(f'defender_{slot}')
            attacker_skill = next((s for s in skills if s['name'] == attacker_skill_name), None)
            defender_skill = next((s for s in skills if s['name'] == defender_skill_name), None)
            if attacker and attacker_skill:
                if not hasattr(attacker, 'skills'):
                    attacker.skills = {}
                attacker.skills[slot] = attacker_skill
            if defender and defender_skill:
                if not hasattr(defender, 'skills'):
                    defender.skills = {}
                defender.skills[slot] = defender_skill
        from simulator.weapon import Weapon
        if attacker and attacker_weapon and attacker_weapon != 'None':
            attacker.weapons = [attacker_weapon]
            attacker.equipped_weapon = Weapon(
                name=attacker_weapon['name'],
                might=attacker_weapon['might'],
                color=attacker_weapon.get('color'),
                range=attacker_weapon.get('range', 1),
                weapon_type=attacker_weapon.get('weapon_type')
            )
        if defender and defender_weapon and defender_weapon != 'None':
            defender.weapons = [defender_weapon]
            defender.equipped_weapon = Weapon(
                name=defender_weapon['name'],
                might=defender_weapon['might'],
                color=defender_weapon.get('color'),
                range=defender_weapon.get('range', 1),
                weapon_type=defender_weapon.get('weapon_type')
            )
        if attacker and defender:
            dmg = calculate_damage(attacker, defender)
            result = f"{attacker.name} deals {dmg} damage to {defender.name}!"

    return render_template("index.html", units=units_for_template, weapons=weapons, skills=skills, result=result)

@main.route("/admin", methods=["GET", "POST"])
def admin():
    message = None
    db = FEHDatabase()
    units = db.get_units()
    weapons = db.get_weapons()
    skills = db.get_skills()
    form_type = request.args.get("type")
    if request.method == "POST":
        if form_type == "unit":
            superboons = request.form.get("superboons", "")
            superbanes = request.form.get("superbanes", "")
            exclusive_skills = request.form.get("exclusive_skills", "")
            unit = {
                "name": request.form.get("name"),
                "hp": int(request.form.get("hp")),
                "atk": int(request.form.get("atk")),
                "spd": int(request.form.get("spd")),
                "defense": int(request.form.get("defense")),
                "res": int(request.form.get("res")),
                "superboons": [s.strip() for s in superboons.split(",") if s.strip()],
                "superbanes": [s.strip() for s in superbanes.split(",") if s.strip()],
                "exclusive_skills": [s.strip() for s in exclusive_skills.split(",") if s.strip()],
                "image_url": request.form.get("image_url"),
                "unit_type": request.form.get("unit_type"),
                "weapon_type": request.form.get("weapon_type"),
            }
            db.add_unit(unit)
            message = f"Unit '{unit['name']}' added."
        elif form_type == "weapon":
            effective_against = request.form.getlist("effective_against")
            weapon = {
                "name": request.form.get("name"),
                "might": int(request.form.get("might")),
                "color": request.form.get("color"),
                "range": int(request.form.get("range")),
                "weapon_type": request.form.get("weapon_type"),
                "effective_against": ",".join(effective_against),
            }
            db.add_weapon(weapon)
            message = f"Weapon '{weapon['name']}' added."
        elif form_type == "skill":
            skill = {
                "name": request.form.get("name"),
                "description": request.form.get("description"),
                "skill_type": request.form.get("skill_type"),
                "effect_json": request.form.get("effect_json"),
            }
            db.add_skill(skill)
            message = f"Skill '{skill['name']}' added."
        elif form_type == "delete":
            delete_type = request.form.get("delete_type")
            delete_name = request.form.get("delete_name")
            if delete_type == "unit":
                db.delete_unit(delete_name)
                message = f"Unit '{delete_name}' deleted."
            elif delete_type == "weapon":
                db.delete_weapon(delete_name)
                message = f"Weapon '{delete_name}' deleted."
            elif delete_type == "skill":
                db.delete_skill(delete_name)
                message = f"Skill '{delete_name}' deleted."
    db.close()
    return render_template("admin.html", message=message, units=units, weapons=weapons, skills=skills)