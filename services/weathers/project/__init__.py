from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


db = SQLAlchemy()


def create_app(script_info=None):
    app = Flask(__name__)

    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    db.init_app(app)

    from project.api.weather import weather_blueprint
    app.register_blueprint(weather_blueprint)

    @app.shell_context_processor
    def ctx():
        return dict(app=app, db=db)

    return app
