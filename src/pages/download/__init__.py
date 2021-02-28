from flask import send_from_directory, render_template
from config import config
import os
from src.const.messages import messages
from src.logger import logger


def download_view(filename):
    filename_with_extension = '.'.join([filename, 'pdf'])
    full_path = os.path.join(config['UPLOAD_FOLDER'], filename_with_extension)
    if not os.path.exists(full_path):
        return render_template('message.html', message=messages['file_not_found'])

    logger.info("Download " + filename)
    return send_from_directory(config['UPLOAD_FOLDER'], filename=filename_with_extension, as_attachment=True)
