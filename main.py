from flask import Flask, send_from_directory, render_template
from config import config
from src.pages import merge_pdf, remove_pages, organize_pdf, download, index

app = Flask(__name__,
            template_folder=config['TEMPLATES'],
            static_folder=config['STATIC'],
            )

app.config['UPLOAD_FOLDER'] = config['UPLOAD_FOLDER']

app.add_url_rule('/', view_func=index.index_view)
app.add_url_rule('/remove_pages', view_func=remove_pages.remove_pages_view, methods=['GET', 'POST'])
app.add_url_rule('/merge_pdf', view_func=merge_pdf.merge_pdf_view, methods=['GET', 'POST'])
app.add_url_rule('/organize_pdf', view_func=organize_pdf.organize_pdf_view, methods=['GET', 'POST'])
app.add_url_rule('/download/<filename>', view_func=download.download_view)

if __name__ == '__main__':
    app.run(debug=config['DEV_DEBUG'],
                use_reloader=True,
                host=config['DEV_HOST'],
                port=config['DEV_PORT']
                )
