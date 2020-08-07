from flask import render_template, request, redirect
import os
from config import config
from src.utils.pdf import PdfEditor
from src.services import uploading_file
from src.const.status import status


def remove_pages_view():
    template = 'remove_pages.html'

    if request.method == 'POST':
        ACTION = request.values.get('action')
        if ACTION is None:
            return uploading_file(request, template, config, status)

        if ACTION == status['REMOVE']:
            filename = request.values.get('f')
            remove_page_list = [int(x) for x in request.values.get('form_page_list').split(',')]
            pdf = PdfEditor(os.path.join(config['UPLOAD_FOLDER'], '.'.join([request.values.get('f'), 'pdf'])))
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
