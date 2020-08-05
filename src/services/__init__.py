from src.utils import allowed_file, rnd
import os
from src.utils.pdf import PdfEditor
from werkzeug.utils import secure_filename
from flask import render_template
from config import config
from time import time


def uploading_file(request, template, config, status):
    cleaning_upload_folder()
    files = request.files.getlist('upload_file')
    if files is None:
        return render_template(template, error="Файл не выбран", status=status['NOFILE'], settings=config)

    uploaded_files = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = rnd.get_random_string()
            filename_title = secure_filename(file.filename)
            path_to_file = os.path.join(config['UPLOAD_FOLDER'], '.'.join([filename, 'pdf']))
            file.save(path_to_file)
            pdf = PdfEditor(path_to_file)
            uploaded_files.append({
                'filename': filename,
                'title': filename_title,
                'page_count': pdf.pageCount()
            })

    if len(uploaded_files) == 0:
        return render_template(template,
                               error="Выберите pdf-файл",
                               status=status['NOFILE'],
                               settings=config
                               )

    return render_template(template,
                           files=uploaded_files,
                           status=status['UPLOADED'],
                           settings=config
                           )


def cleaning_upload_folder():
    files_of_upload = [os.path.join(config['UPLOAD_FOLDER'], f) for f in os.listdir(config['UPLOAD_FOLDER']) if
                       os.path.isfile(os.path.join(config['UPLOAD_FOLDER'], f))]
    for file_ in files_of_upload:
        if time() - os.stat(file_).st_ctime > config['FILE_STORAGE_TIME']:
            os.remove(file_)
