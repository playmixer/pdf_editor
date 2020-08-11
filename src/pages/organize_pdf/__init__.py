from flask import render_template, request, redirect
import os
from config import config
from src.utils.pdf import PdfEditor
from src.services import uploading_file
from src.const.status import status

GENERATE_IMG = config['SHOW_REAL_PAGE_IMAGE']


def organize_pdf_view():
    template = 'organize_pdf.html'

    if request.method == 'POST':
        ACTION = request.values.get('action')
        if ACTION is None:
            return uploading_file(request, template, generate_img=GENERATE_IMG)

        if ACTION == status['ORGANIZE']:
            sort_pages = [int(x) for x in request.values.getlist('sort_pages')]
            filename = request.values.get('f')
            file_ = os.path.join(config['UPLOAD_FOLDER'], '.'.join([filename, 'pdf']))
            pdf = PdfEditor(file_)
            pdf.movePages(sort_pages)

            return render_template(template,
                                   upload_file_name=filename,
                                   status=status['COMPLETED'],
                                   )

    if len(request.values) > 0:
        return redirect(request.path)
    return render_template(template, status=status['NOFILE'], settings=config)
