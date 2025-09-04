"""
app.py
-------
Entry point for the Fire Emblem Heroes (FEH) Simulator web app.
This file creates and configures the Flask application, registers
routes, and runs the app locally (or on Raspberry Pi).
"""

from flask import Flask
from web.routes import main  # Import our main Blueprint (routes and logic)

def create_app():
    """
    Application factory pattern: Creates and configures the Flask app.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)         # Create a Flask app instance
    app.register_blueprint(main)  # Register routes from the 'web/routes.py' blueprint
    return app


if __name__ == "__main__":
    # Only run this block if app.py is executed directly (not imported)
    app = create_app()
    # Host '0.0.0.0' makes it accessible to other devices on the network
    # Port 5000 is the default Flask dev server port
    app.run(host="0.0.0.0", port=5000, debug=True)
