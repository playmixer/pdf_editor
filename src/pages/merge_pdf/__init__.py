from flask import render_template, request, redirect
import os
from config import config
from src.utils.pdf import PdfEditor
from src.services import uploading_file
from src.const.status import status
from src.const.messages import messages


def merge_pdf_view():
    template = 'merge_pdf.html'

    if request.method == 'POST':
        ACTION = request.values.get('action')
        if ACTION is None:
            return uploading_file(request, template, config, status)

        if ACTION == status['MERGE']:
            files = request.values.getlist('sorted_files')
            if not len(files):
                return render_template("message.html", message=messages['no_have_select_file'])

            files_title = request.values.getlist('sorted_files_title')
            file_ = PdfEditor(os.path.join(config['UPLOAD_FOLDER'], '.'.join([files[0], 'pdf'])))
            for i in range(1, len(files)):
                file_for_merge = os.path.join(config['UPLOAD_FOLDER'], '.'.join([files[i], 'pdf']))
                try:
                    file_.merge(file_for_merge)
                except ValueError:
                    mess = dict(messages['file_corrupted'])
                    mess['title'] = mess['title'].format(filename=files_title[i])
                    return render_template('message.html', message=mess)

            extract_filename = file_.getFileName().split('.')[0]
            return render_template(template,
                                   upload_file_name=extract_filename,
                                   status=status['COMPLETED'],
                                   )

    if len(request.values) > 0:
        return redirect(request.path)
    return render_template(template, status=status['NOFILE'], settings=config)
