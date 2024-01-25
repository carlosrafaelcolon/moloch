from flask import Flask
from flask_cors import CORS

from server.config import Config
from server.db import db

from server.hooks import load_logged_in_user, handle_error


from server.routes import (
    auth_routes,
    conversation_routes,
    pdf_routes
)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    register_extensions(app)
    register_hooks(app)
    register_blueprints(app)
    return app

def register_extensions(app):
    db.init_app(app)
    
def register_blueprints(app):
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(pdf_routes.bp)
    app.register_blueprint(conversation_routes.bp)
    
def register_hooks(app):
    CORS(app)
    app.before_request(load_logged_in_user)
    app.register_error_handler(Exception, handle_error) 

