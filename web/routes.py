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

from flask import Blueprint, render_template, request, redirect, url_for
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
            # Show only the part before the comma for names
            attacker_short = attacker.name.split(',')[0].strip()
            defender_short = defender.name.split(',')[0].strip()
            dmg, log = calculate_damage(attacker, defender)
            result = f"{attacker_short} deals {dmg} damage to {defender_short}!"

    return render_template("index.html", units=units_for_template, weapons=weapons, skills=skills, result=result)

@main.route("/admin", methods=["GET", "POST"])
def admin():
    db = FEHDatabase()
    units = db.get_units()
    weapons = db.get_weapons()
    skills = db.get_skills()
    message = None
    if request.method == "POST":
        form_type = request.args.get("type")
        if form_type == "unit":
            name = request.form.get("name")
            # Check for duplicate unit name
            if any(u['name'].lower() == name.lower() for u in units):
                message = f"Unit '{name}' already exists."
            else:
                unit = {
                    "name": name,
                    "hp": int(request.form.get("hp")),
                    "atk": int(request.form.get("atk")),
                    "spd": int(request.form.get("spd")),
                    "defense": int(request.form.get("defense")),
                    "res": int(request.form.get("res")),
                    "superboons": [s.strip() for s in request.form.get("superboons", "").split(",") if s.strip()],
                    "superbanes": [s.strip() for s in request.form.get("superbanes", "").split(",") if s.strip()],
                    "exclusive_skills": [s.strip() for s in request.form.get("exclusive_skills", "").split(",") if s.strip()],
                    "image_url": request.form.get("image_url"),
                    "unit_type": request.form.get("unit_type"),
                    "weapon_type": request.form.get("weapon_type")
                }
                db.add_unit(unit)
                message = f"Unit '{unit['name']}' added."
        elif form_type == "weapon":
            name = request.form.get("name")
            if any(w['name'].lower() == name.lower() for w in weapons):
                message = f"Weapon '{name}' already exists."
            else:
                effective_against_list = request.form.getlist("effective_against")
                weapon = {
                    "name": name,
                    "might": int(request.form.get("might")),
                    "color": request.form.get("color"),
                    "range": int(request.form.get("range")),
                    "weapon_type": request.form.get("weapon_type"),
                    "effective_against": ",".join(effective_against_list)
                }
                db.add_weapon(weapon)
                message = f"Weapon '{weapon['name']}' added."
        elif form_type == "skill":
            name = request.form.get("name")
            if any(s['name'].lower() == name.lower() for s in skills):
                message = f"Skill '{name}' already exists."
            else:
                skill = {
                    "name": name,
                    "description": request.form.get("description"),
                    "skill_type": request.form.get("skill_type"),
                    "effect_json": request.form.get("effect_json")
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
    return render_template("admin.html", units=units, weapons=weapons, skills=skills, message=message)

@main.route("/admin/units", methods=["GET"])
def admin_unit_list():
    db = FEHDatabase()
    units = db.get_units()
    db.close()
    search = request.args.get('search', '').strip().lower()
    if search:
        units = [u for u in units if search in u['name'].lower()]
    return render_template("unit_list.html", units=units, search=search)

@main.route("/admin/delete/unit/<unit_name>", methods=["POST"])
def admin_delete_unit(unit_name):
    db = FEHDatabase()
    db.delete_unit(unit_name)
    db.close()
    return redirect(url_for('main.admin_unit_list'))

@main.route("/admin/edit/unit/<unit_name>", methods=["GET", "POST"])
def admin_edit_unit(unit_name):
    db = FEHDatabase()
    units = db.get_units()
    unit = next((u for u in units if u['name'] == unit_name), None)
    message = None
    if not unit:
        db.close()
        return render_template("edit_unit.html", unit=None, message="Unit not found.")
    if request.method == "POST":
        # Update unit fields from form
        unit["name"] = request.form.get("name")
        unit["hp"] = int(request.form.get("hp"))
        unit["atk"] = int(request.form.get("atk"))
        unit["spd"] = int(request.form.get("spd"))
        unit["defense"] = int(request.form.get("defense"))
        unit["res"] = int(request.form.get("res"))
        unit["superboons"] = [s.strip() for s in request.form.get("superboons", "").split(",") if s.strip()]
        unit["superbanes"] = [s.strip() for s in request.form.get("superbanes", "").split(",") if s.strip()]
        unit["exclusive_skills"] = [s.strip() for s in request.form.get("exclusive_skills", "").split(",") if s.strip()]
        unit["image_url"] = request.form.get("image_url")
        unit["unit_type"] = request.form.get("unit_type")
        unit["weapon_type"] = request.form.get("weapon_type")
        db.update_unit(unit_name, unit)
        message = f"Unit '{unit['name']}' updated."
        unit_name = unit["name"]
    db.close()
    return render_template("edit_unit.html", unit=unit, message=message)

@main.route('/admin/weapons')
def weapon_list():
    from simulator.data_loader import get_all_weapons
    weapons = get_all_weapons()
    return render_template('weapon_list.html', weapons=weapons)

@main.route('/admin/edit/weapon/<name>', methods=['GET', 'POST'])
def edit_weapon(name):
    from simulator.data_loader import get_weapon_by_name, update_weapon, get_weapon_types
    weapon = get_weapon_by_name(name)
    weapon_types = get_weapon_types()
    if request.method == 'POST':
        new_name = request.form['name']
        might = int(request.form['might'])
        color = request.form['color']
        range_ = int(request.form['range'])
        weapon_type = request.form['weapon_type']
        effective_against = request.form['effective_against']
        update_weapon(name, new_name, might, color, range_, weapon_type, effective_against)
        return redirect(url_for('web.weapon_list'))
    return render_template('edit_weapon.html', weapon=weapon, weapon_types=weapon_types)

@main.route('/admin/delete/weapon/<name>', methods=['POST'])
def delete_weapon(name):
    from simulator.data_loader import delete_weapon
    delete_weapon(name)
    return redirect(url_for('main.weapon_list'))