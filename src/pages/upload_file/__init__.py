from flask import send_from_directory
from config import config


def upload_file_view(filename):
    return send_from_directory(config['UPLOAD_FOLDER'], filename)
