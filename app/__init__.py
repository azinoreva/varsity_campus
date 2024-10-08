"""Initialize app database"""

# app/__init__.py
from flask import Flask
from flask_login import LoginManager
from .db import db, migrate
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os
from .routes.auth import auth_bp
from .routes.posts import posts_bp
from .routes.communities import community_bp
from .routes.comments import comments_bp
from .routes.courses import courses_bp
from .routes.lectures import lectures_bp


login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # Configure the app
    app.config['SECRET_KEY'] = os.environ.get(
        'SECRET_KEY') or 'your_default_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL') or 'sqlite:///your_database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    with app.app_context():
        from . import models  # Import your models
        db.create_all()  # Create database tables if they don't exist

    # Register blueprints for route-s
    from .routes import auth, posts, communities, comments, courses, lectures
    app.register_blueprint(auth_bp)
    app.register_blueprint(comments_bp)
    app.register_blueprint(courses_bp)
    app.register_blueprint(lectures_bp)
    app.register_blueprint(posts_bp)
    app.register_blueprint(community_bp)

    return app
