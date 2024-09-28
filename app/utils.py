import os
from werkzeug.utils import secure_filename


def save_image(image):
    # Set directory where images will be stored
    upload_folder = os.path.join(os.getcwd(), 'static/uploads')
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    # Secure the filename
    filename = secure_filename(image.filename)

    # Save the file
    file_path = os.path.join(upload_folder, filename)
    image.save(file_path)

    return file_path  # Return path to save in the database
