from flask import Flask # type: ignore
from app.routes.excel import excel_bp
from app.routes.customization import customization_bp


def create_app():
    # Make sure to include static_folder='static' here
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config['UPLOAD_FOLDER'] = 'uploads/'

    # Register routes
    app.register_blueprint(excel_bp, url_prefix='/api/excel')
    app.register_blueprint(customization_bp, url_prefix='/customize')

    return app
