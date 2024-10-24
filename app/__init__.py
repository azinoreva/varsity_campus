"""Initialize app database"""

# app/__init__.py
from flask import Flask
from flask_login import LoginManager
from .db import db, migrate
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os
from cryptography.fernet import Fernet
from .routes.auth import auth_bp
from .routes.home import home_bp
from .routes.dashboard import dashboard_bp
from .routes.posts import posts_bp
from .routes.communities import community_bp
from .routes.courses import courses_bp
from .routes.lectures import lectures_bp
from .routes.message import message_bp
from .routes.library import library_bp
from .routes.manage_users import manage_users_bp

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # Configure the app
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'your_default_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///your_database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Configure Fernet key for encryption
    app.config['FERNET_KEY'] = os.environ.get('FERNET_KEY')
    if not app.config['FERNET_KEY']:
        raise ValueError("FERNET_KEY not set in environment variables. Please add it.")
    
    app.config['FERNET'] = Fernet(app.config['FERNET_KEY'])

    # Initialize the database and migration tools
    db.init_app(app)
    migrate.init_app(app, db)

    # Initialize the login manager
    login_manager.init_app(app)
    login_manager.login_view = 'auth_bp.login'

    with app.app_context():
        from . import models 
        db.create_all()

    # Register blueprints for route-s
    app.register_blueprint(home_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(courses_bp)
    app.register_blueprint(lectures_bp)
    app.register_blueprint(posts_bp)
    app.register_blueprint(community_bp)
    app.register_blueprint(message_bp)
    app.register_blueprint(library_bp)
    app.register_blueprint(manage_users_bp)

    return app

@login_manager.user_loader
def load_user(user_id):
    from .models import User  
    return User.query.get(int(user_id))
