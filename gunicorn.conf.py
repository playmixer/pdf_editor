# more settings
# https://docs.gunicorn.org/en/latest/settings.html#settings

# import multiprocessing

bind = "0.0.0.0:8000"
workers = 2
#workers = multiprocessing.cpu_count() * 2 + 1

