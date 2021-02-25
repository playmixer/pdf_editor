from flask import render_template, request, redirect
import os
from config import config
from src.utils.pdf import PdfEditor
from src.services import uploading_file
from src.const.status import status
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

            if ACTION == status['MERGE']:
                files = request.values.getlist('sorted_files')
                if not len(files):
                    raise exceptions.NoHaveSelectFiles(messages['no_have_select_file'].get('title'))

                files_title = request.values.getlist('sorted_files_title')
                file_ = PdfEditor(os.path.join(config['UPLOAD_FOLDER'], '.'.join([files[0], 'pdf'])))
                for i in range(1, len(files)):
                    file_for_merge = os.path.join(config['UPLOAD_FOLDER'], '.'.join([files[i], 'pdf']))
                    try:
                        file_.merge(file_for_merge)
                    except ValueError:
                        raise exceptions.FileCorrupted(f"Файл {files_title[i]} поврежден")
                        # mess = dict(messages['file_corrupted'])
                        # mess['title'] = mess['title'].format(filename=files_title[i])
                        # logger.info(f"File corrupted {files_title[i]}")
                        # return render_template('message.html', message=mess)

                extract_filename = file_.getFileName().split('.')[0]
                return render_template(template,
                                       upload_file_name=extract_filename,
                                       status=status['COMPLETED'],
                                       )

        if len(request.values) > 0:
            return redirect(request.path)
        return render_template(template, status=status['NOFILE'], settings=config)
    except (exceptions.NoHaveSelectFiles, exceptions.FileCorrupted) as err:
        err_message = str(err)
        logger.error("merge page: " + str(err))
    except Exception as err:
        err_message = 'Ошибка ' + str(err)
        logger.error("merge page Exception: " + str(err))

    return render_template("message.html", message={
        'title': err_message,
        'description': ''
    })
