from flask import render_template, request, redirect
import os
from config import config
from src.utils.pdf import PdfEditor
from src.services import uploading_file
from src.const.status import status
from src.pages import exceptions
from src.logger import logger

GENERATE_IMG = config['SHOW_REAL_PAGE_IMAGE']


def remove_pages_view():
    template = 'remove_pages.html'
    err_message = ""

    try:
        if request.method == 'POST':
            ACTION = request.values.get('action')
            if ACTION is None:
                return uploading_file(request, template, generate_img=GENERATE_IMG)

            if ACTION == status['REMOVE']:
                filename = request.values.get('f')
                path = os.path.join(config['UPLOAD_FOLDER'], '.'.join([filename, 'pdf']))
                if not os.path.exists(path):
                    raise exceptions.FileNotFound

                remove_page_list = [int(x) for x in request.values.get('form_page_list').split(',')]
                pdf = PdfEditor(path)
                pdf.removePages(remove_page_list)
                return render_template(template,
                                       upload_file_name=filename,
                                       status=status['COMPLETED']
                                       )

            return render_template("message.html", message={
                'title': 'Что то пошло не так',
                'description': ''
            })

        if len(request.values) > 0:
            return redirect(request.path)
        return render_template(template, status=status['NOFILE'], settings=config)
    except exceptions.FileNotFound:
        err_message = "Исходный файл не найден"

    except Exception as err:
        err_message = 'Что то пошло не так'
        logger.error("remove page " + err)

    return render_template("message.html", message={
        'title': err_message,
        'description': ''
    })
