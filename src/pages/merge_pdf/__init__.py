from flask import render_template, request, redirect
import os
from config import config
from src.utils.pdf import PdfEditor
from src.services import uploading_file
from src.const.status import Status
from src.const.messages import messages
from src.logger import logger
from src.pages import exceptions


def merge_pdf_view():
    template = 'merge_pdf.html'
    err_message = ''

    try:
        if request.method == 'POST':
            ACTION = request.values.get('action')
            if ACTION is None:
                return uploading_file(request, template)

            if ACTION == Status.merge:
                files = request.values.getlist('sorted_files')
                if not len(files):
                    logger.error("Merge page: No have select file")
                    raise exceptions.NoHaveSelectFiles(messages['no_have_select_file'].get('title'))

                files_title = request.values.getlist('sorted_files_title')
                file_ = PdfEditor(os.path.join(config['UPLOAD_FOLDER'], '.'.join([files[0], 'pdf'])))
                for i in range(1, len(files)):
                    file_for_merge = os.path.join(config['UPLOAD_FOLDER'], '.'.join([files[i], 'pdf']))
                    if not os.path.exists(file_for_merge):
                        logger.error("Merge page: Not found file " + files[i])
                        raise exceptions.FileNotFound("Исходный файл не найден")
                    try:
                        file_.merge(file_for_merge)
                    except ValueError:
                        logger.error(f"Merge page: Fail {files_title[i]} corrupted")
                        raise exceptions.FileCorrupted(f"Файл {files_title[i]} поврежден")

                extract_filename = file_.getFileName().split('.')[0]
                logger.info("Merge " + str(len(files)) + " files: " + ", ".join(files))
                return render_template(template,
                                       upload_file_name=extract_filename,
                                       status=Status.completed,
                                       )

        if len(request.values) > 0:
            return redirect(request.path)
        return render_template(template, status=Status.nofile, settings=config)
    except (exceptions.NoHaveSelectFiles, exceptions.FileCorrupted, exceptions.FileNotFound) as err:
        err_message = str(err)
    except Exception as err:
        err_message = 'Ошибка ' + str(err)
        logger.error("Merge page Exception: " + str(err))

    return render_template("message.html", message={
        'title': err_message,
        'description': ''
    })
