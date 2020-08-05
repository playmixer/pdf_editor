from flask import render_template, request, redirect
from src.utils import allowed_file, rnd
from werkzeug.utils import secure_filename
import os
from config import config
from src.utils.pdf import PdfEditor
from src.services import uploading_file
from src.status import status


def merge_pdf_view():
    template = 'merge_pdf.html'

    if request.method == 'POST':
        ACTION = request.values.get('action')
        if ACTION is None:
            return uploading_file(request, template, config, status)

        if ACTION == status['MERGE']:
            files = request.values.getlist('sorted_files')
            file_ = PdfEditor(os.path.join(config['UPLOAD_FOLDER'], '.'.join([files[0], 'pdf'])))
            for i in range(1, len(files)):
                file_ = file_.merge(os.path.join(config['UPLOAD_FOLDER'], '.'.join([files[i], 'pdf'])))

            extract_filename = os.path.split(file_.getFileName())[1].split('.')[0]
            return render_template(template,
                                   upload_file_name=extract_filename,
                                   status=status['COMPLETED'],
                                   )

    if len(request.values) > 0:
        return redirect(request.path)
    return render_template(template, status=status['NOFILE'], settings=config)
