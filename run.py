from flask import Flask # type: ignore
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

from app.routes.template import template_bp
app.register_blueprint(template_bp)

from app.routes.customization import customization_bp  # Import the customization blueprint
app.register_blueprint(customization_bp, url_prefix='/customize')

if __name__ == '__main__':
    app.run(debug=True)

from routes.customization import customization # type: ignore
app.register_blueprint(customization)

print("Registered Blueprints:", app.blueprints)

