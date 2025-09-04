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
            weapons=[]
        )
        if weapon:
            unit_obj.weapons.append(weapon)
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

    if request.method == "POST":
        attacker_name = request.form.get("attacker")
        defender_name = request.form.get("defender")
        attacker = next((u for u in units if u.name == attacker_name), None)
        defender = next((u for u in units if u.name == defender_name), None)
        if attacker and defender:
            dmg = calculate_damage(attacker, defender)
            result = f"{attacker.name} deals {dmg} damage to {defender.name}!"

    return render_template("index.html", units=units, result=result)

@main.route("/admin", methods=["GET", "POST"])
def admin():
    message = None
    db = FEHDatabase()
    form_type = request.args.get("type")
    if request.method == "POST":
        if form_type == "unit":
            unit = {
                "name": request.form.get("name"),
                "hp": int(request.form.get("hp")),
                "atk": int(request.form.get("atk")),
                "spd": int(request.form.get("spd")),
                "defense": int(request.form.get("defense")),
                "res": int(request.form.get("res")),
                "unit_type": request.form.get("unit_type"),
                "image_url": request.form.get("image_url"),
            }
            db.add_unit(unit)
            message = f"Unit '{unit['name']}' added."
        elif form_type == "weapon":
            weapon = {
                "name": request.form.get("name"),
                "might": int(request.form.get("might")),
                "color": request.form.get("color"),
                "range": int(request.form.get("range")),
                "weapon_type": request.form.get("weapon_type"),
                "effective_against": request.form.get("effective_against"),
                "image_url": request.form.get("image_url"),
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
    db.close()
    return render_template("admin.html", message=message)