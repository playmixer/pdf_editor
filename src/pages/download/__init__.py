from flask import send_from_directory, render_template
from config import config
import os
from src.utils.pdf import PdfEditor
from src.const.messages import messages


def download_view(filename):
    full_path = os.path.join(config['UPLOAD_FOLDER'], '.'.join([filename, 'pdf']))
    if not os.path.exists(full_path):
        return render_template('message.html', message=messages['file_not_found'])

    return send_from_directory(config['UPLOAD_FOLDER'], filename='.'.join([filename, 'pdf']), as_attachment=True)
