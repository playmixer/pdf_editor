from flask import send_from_directory
from config import config


def download_view(filename):
    return send_from_directory(config['UPLOAD_FOLDER'], filename='.'.join([filename, 'pdf']), as_attachment=True)
