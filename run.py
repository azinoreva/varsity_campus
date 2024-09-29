""" Entry point to run the app"""

from app import create_app

# Create the Flask app
app = create_app()

# Run the app if this script is executed
if __name__ == '__main__':
    app.run(debug=True)  # Set debug=True for development; change to False in production
