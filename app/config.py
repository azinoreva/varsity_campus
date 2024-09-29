"""Database configuration"""
import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'  # Use SQLite for simplicity
    SQLALCHEMY_TRACK_MODIFICATIONS = False
