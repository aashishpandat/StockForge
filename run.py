import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    # Debug mode must only be enabled explicitly in local development.
    debug_enabled = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug_enabled)
