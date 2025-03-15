from flask import Blueprint
from controllers.user_controller import user_bp

def init_routes(app):
    app.register_blueprint(user_bp, url_prefix='/api/users')