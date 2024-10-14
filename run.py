"""Entry point"""

from app import create_app
import os

# Create the Flask application instance
app = create_app()

# Main entry point for the application
if __name__ == "__main__":
    # Set the host and port if needed; default is 127.0.0.1:5000
    app.run(host=os.getenv('FLASK_RUN_HOST', '127.0.0.1'),
            port=int(os.getenv('FLASK_RUN_PORT', 8000)),
            debug=os.getenv('FLASK_DEBUG', True))
