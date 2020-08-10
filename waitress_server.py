from waitress import serve
from wsgi import app

# import multiprocessing

serve(app,
      listen='*:8080',
      _quiet=True,
      threads=3,
      # threads=multiprocessing.cpu_count() * 2 + 1
      )
