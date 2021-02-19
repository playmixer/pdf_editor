from src.utils import allowed_file, rnd
import os
from src.utils.pdf import PdfEditor
from werkzeug.utils import secure_filename
from flask import render_template
from config import config
from time import time
from src.const.status import status
from src.logger import logger
from .task import taskman

UPLOAD_FOLDER = config['UPLOAD_FOLDER']
MAX_TIME_LOADING = config['LONG_TIME_LOADING_REAL_IMAGES'] if config['LONG_TIME_LOADING_REAL_IMAGES'] else 99999


def uploading_file(request, template, *args, **kwargs):
    GENERATE_IMG = kwargs.get('generate_img') if kwargs.get('generate_img') else False

    if not os.path.exists(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)

    # удаляем файл старше чем FILE_STORAGE_TIME
    # cleaning_upload_folder()

    files = request.files.getlist('upload_file')
    if files is None:
        return render_template(template, error="Файл не выбран", status=status['NOFILE'], settings=config)

    uploaded_files = []
    for file_ in files:
        if file_ and allowed_file(file_.filename):
            filename = rnd.get_random_string()
            filename_title = secure_filename(file_.filename)
            path_to_file = os.path.join(UPLOAD_FOLDER, '.'.join([filename, 'pdf']))
            file_.save(path_to_file)
            pdf = PdfEditor(path_to_file)
            images = generating_images(path_to_file) if GENERATE_IMG else ''

            uploaded_files.append({
                'filename': filename,
                'title': filename_title,
                'page_count': pdf.pageCount(),
                'images': images
            })

    if len(uploaded_files) == 0:
        return render_template(template,
                               error="Выберите pdf-файл",
                               status=status['NOFILE'],
                               settings=config
                               )

    logger.info(f'Upload files {", ".join([x["title"] + "(" + x["filename"] + ")" for x in uploaded_files])}')
    return render_template(template,
                           files=uploaded_files,
                           status=status['UPLOADED'],
                           settings=config
                           )


def cleaning_upload_folder():
    files_of_upload = [os.path.join(UPLOAD_FOLDER, f) for f in os.listdir(UPLOAD_FOLDER) if
                       os.path.isfile(os.path.join(UPLOAD_FOLDER, f))]
    for file_ in files_of_upload:
        if time() - os.stat(file_).st_ctime > config['FILE_STORAGE_TIME']:
            os.remove(file_)


def generating_images(filename):
    pdf = PdfEditor(filename)
    images = []
    start = time()
    for i in range(pdf.pageCount()):
        is_short_time = time() - start < MAX_TIME_LOADING
        img = pdf.pageToPng(i) if is_short_time else ''
        images.append(os.path.split(img)[1])

    return images
