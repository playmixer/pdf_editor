import logging
import os
from logging.handlers import TimedRotatingFileHandler

filename = 'app.log'

if not os.path.exists("logs/"):
    os.makedirs("logs/")

# logging.basicConfig(
#     level=logging.DEBUG,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# )

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')



# s_handler = logging.StreamHandler()
# s_handler.setLevel(logging.DEBUG)
# s_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

# f_handler = logging.FileHandler(os.path.join('logs', filename))
# f_handler.setLevel(logging.INFO)
# f_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

f_handler = TimedRotatingFileHandler(os.path.join('logs', filename), when="midnight", interval=1)
f_handler.suffix = "%Y-%m-%d"
f_handler.setLevel(logging.INFO)
f_handler.setFormatter(formatter)

logger = logging.getLogger("pdf")
logger.setLevel(logging.INFO)
# logger.addHandler(s_handler)
logger.addHandler(f_handler)
