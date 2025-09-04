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

# Create a Blueprint to group related routes
# This keeps our app modular and easier to scale
main = Blueprint("main", __name__)

# Temporary hardcoded unit examples
sample_units = [
    Unit("Marth", hp=40, atk=30, spd=34, defense=25, res=20, weapon_mt=16),
    Unit("Tiki", hp=45, atk=32, spd=25, defense=35, res=28, weapon_mt=16),
]

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
    result = None  # Placeholder for battle outcome text

    # Check if form was submitted
    if request.method == "POST":
        attacker_name = request.form.get("attacker")
        defender_name = request.form.get("defender")

        # Look up selected units by name
        attacker = next((u for u in sample_units if u.name == attacker_name), None)
        defender = next((u for u in sample_units if u.name == defender_name), None)

        # Run calculation only if both units are valid
        if attacker and defender:
            dmg = calculate_damage(attacker, defender)
            result = f"{attacker.name} deals {dmg} damage to {defender.name}!"

    # Render template with available units and (optional) result
    return render_template("index.html", units=sample_units, result=result)
