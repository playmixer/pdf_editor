from flask import Flask, render_template
from config import config
from src.pages import merge_pdf, remove_pages, organize_pdf, download, index, upload_file
from src.logger import logger
from src.services import taskman, cleaning_upload_folder
from time import sleep
import atexit

SUBDIR = config['SUBDIRECTORY']


def task_clean_upload():
    try:
        while True:
            sleep(60)
            cleaning_upload_folder()
            print('Clean upload folder')
    except KeyboardInterrupt:
        return


def simple_app():
    app = Flask(
        __name__,
        template_folder=config['TEMPLATES'],
        static_folder=config['STATIC'],
        static_url_path=''.join([SUBDIR, config['STATIC_URL_PATH']])
    )

    app.config['UPLOAD_FOLDER'] = config['UPLOAD_FOLDER']
    app.config['MAX_CONTENT_LENGTH'] = config['MAX_SIZE_FILE'] * 1024 * 1024

    app.add_url_rule(f'{SUBDIR}/home', view_func=index.index_view)
    app.add_url_rule(f'{SUBDIR}/', view_func=index.index_view)
    app.add_url_rule(f'{SUBDIR}/remove_pages', view_func=remove_pages.remove_pages_view, methods=['GET', 'POST'])
    app.add_url_rule(f'{SUBDIR}/merge_pdf', view_func=merge_pdf.merge_pdf_view, methods=['GET', 'POST'])
    app.add_url_rule(f'{SUBDIR}/organize_pdf', view_func=organize_pdf.organize_pdf_view, methods=['GET', 'POST'])
    app.add_url_rule(f'{SUBDIR}/download/<filename>', view_func=download.download_view)
    app.add_url_rule(f'{SUBDIR}/uploads/<filename>', view_func=upload_file.upload_file_view)

    @app.errorhandler(404)
    def page_not_found_view(e):
        print(e)
        logger.info('Page not found')
        return render_template('404.html')

    taskman.add_task(task_clean_upload)

    return app


if __name__ == '__main__':
    simple_app().run(
        debug=True,
        use_reloader=True,
        host='localhost',
        port=5000
    )
