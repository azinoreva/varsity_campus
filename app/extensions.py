#Extensions (like db, login_manager)

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# Create instances of the extensions
db = SQLAlchemy()           # SQLAlchemy instance for database interactions
login_manager = LoginManager()  # LoginManager instance for user authentication
migrate = Migrate()        # Migrate instance for database migrations

# Set up the login_view for LoginManager
login_manager.login_view = 'auth.login'  # Redirect to login page for unauthorized access
