"""Utility"""
import os
import secrets
from flask import current_app
from datetime import datetime

def save_image(form_image):
    """Save an uploaded image and return the filename."""
    random_hex = secrets.token_hex(8)  # Generate a random hex string
    _, f_ext = os.path.splitext(form_image.filename)  # Get file extension
    image_filename = random_hex + f_ext
    image_path = os.path.join(current_app.root_path, 'static/images', image_filename)  # Path to save the image

    # Save the image to the filesystem
    form_image.save(image_path)
    return image_filename

def delete_file(file_path):
    """Delete a file if it exists."""
    if os.path.isfile(file_path):
        os.remove(file_path)

def generate_random_string(length=12):
    """Generate a random string of fixed length."""
    return secrets.token_urlsafe(length)  # Generates a URL-safe text string

def send_notification(user, message):
    """Send a notification to the user."""
    # Implement your notification logic (e.g., email or messaging)
    # For example, using Flask-Mail for email notifications
    from flask_mail import Message
    from flask import render_template
    from app.extensions import mail  # Assuming you have a mail instance in extensions.py

    msg = Message('New Notification',
                  sender='noreply@yourapp.com',
                  recipients=[user.email])
    msg.body = render_template('notification_email.txt', message=message)  # Render email template
    mail.send(msg)

def log_event(user, action):
    """Log user actions for auditing."""
    timestamp = datetime.utcnow()
    with open('app.log', 'a') as f:
        f.write(f"{timestamp} - User: {user.username} performed action: {action}\n")
