"""Initialize app database"""

# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize the database
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # Configure the app
    app.config['SECRET_KEY'] = os.environ.get(
        'SECRET_KEY') or 'your_default_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL') or 'sqlite:///your_database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        from . import models  # Import your models
        db.create_all()  # Create database tables if they don't exist

    # Register blueprints for routes
    from .routes import auth, posts, community
    app.register_blueprint(auth.bp)
    app.register_blueprint(posts.bp)
    app.register_blueprint(community.bp)

    return app
