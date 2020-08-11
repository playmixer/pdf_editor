from flask import Flask, render_template
from config import config
from src.pages import merge_pdf, remove_pages, organize_pdf, download, index, upload_file

app = Flask(__name__,
            template_folder=config['TEMPLATES'],
            static_folder=config['STATIC'],
            )

app.config['UPLOAD_FOLDER'] = config['UPLOAD_FOLDER']
app.config['MAX_CONTENT_LENGTH'] = config['MAX_SIZE_FILE'] * 1024 * 1024

app.add_url_rule('/home', view_func=index.index_view)
app.add_url_rule('/', view_func=index.index_view)
app.add_url_rule('/remove_pages', view_func=remove_pages.remove_pages_view, methods=['GET', 'POST'])
app.add_url_rule('/merge_pdf', view_func=merge_pdf.merge_pdf_view, methods=['GET', 'POST'])
app.add_url_rule('/organize_pdf', view_func=organize_pdf.organize_pdf_view, methods=['GET', 'POST'])
app.add_url_rule('/download/<filename>', view_func=download.download_view)
app.add_url_rule('/uploads/<filename>', view_func=upload_file.upload_file_view)


@app.errorhandler(404)
def page_not_found_view(e):
    return render_template('404.html')


if __name__ == '__main__':
    app.run(debug=config['DEV_DEBUG'],
            use_reloader=True,
            host=config['DEV_HOST'],
            port=config['DEV_PORT']
            )
