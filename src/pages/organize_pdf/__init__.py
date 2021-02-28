from flask import render_template, request, redirect
import os
from config import config
from src.utils.pdf import PdfEditor
from src.services import uploading_file
from src.const.status import Status
from src.logger import logger
from src.pages import exceptions

GENERATE_IMG = config['SHOW_REAL_PAGE_IMAGE']


def organize_pdf_view():
    template = 'organize_pdf.html'
    err_message = ''

    try:
        if request.method == 'POST':
            ACTION = request.values.get('action')
            if ACTION is None:
                return uploading_file(request, template, generate_img=GENERATE_IMG)

            if ACTION == Status.organize:
                sort_pages = [int(x) for x in request.values.getlist('sort_pages')]
                filename = request.values.get('f')
                path = os.path.join(config['UPLOAD_FOLDER'], '.'.join([filename, 'pdf']))
                if not os.path.exists(path):
                    logger.error("Organize page Exception: Not found file " + filename)
                    raise exceptions.FileNotFound

                file_ = os.path.join(config['UPLOAD_FOLDER'], '.'.join([filename, 'pdf']))
                pdf = PdfEditor(file_)
                pdf.movePages(sort_pages)

                logger.info("Organize file " + filename)
                return render_template(template,
                                       upload_file_name=filename,
                                       status=Status.completed,
                                       )

        if len(request.values) > 0:
            return redirect(request.path)
        return render_template(template, status=Status.nofile, settings=config)
    except exceptions.FileNotFound:
        err_message = "Исходный файл не найден"
    except Exception as err:
        err_message = str(err)
        logger.error("Organize page Exception: " + str(err))

    return render_template("message.html", message={
        'title': err_message,
        'description': ''
    })
