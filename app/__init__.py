from flask import Flask
from app.config import TestingConfig, DevelopmentConfig, ProductionConfig
import os
# blueprints
from app.errors.handlers import errors
from app.home.views import home_blueprint

app = Flask(__name__)

def create_app():
    
    try:
        app.config.from_object(DevelopmentConfig if os.environ.get("PRODUCTION").lower() == 'true' else DevelopmentConfig)
    except:
        app.config.from_object(DevelopmentConfig)

    from app.errors.handlers import errors
    from app.home.routes import home

    app.register_blueprint(home_blueprint)
    app.register_blueprint(errors)

    return app
