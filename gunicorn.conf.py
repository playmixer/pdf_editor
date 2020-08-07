# more settings
# https://docs.gunicorn.org/en/latest/settings.html#settings

# import multiprocessing

bind = "0.0.0.0:8000"
workers = 3
# workers = multiprocessing.cpu_count() * 2 + 1
timeout = 120
loglevel = 'info'
