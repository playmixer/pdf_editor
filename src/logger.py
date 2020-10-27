import logging
import os

filename = 'app.log'

if not os.path.exists("logs/"):
    os.makedirs("logs/")

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger("pdf")

# s_handler = logging.StreamHandler()
# s_handler.setLevel(logging.DEBUG)
# s_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

f_handler = logging.FileHandler(os.path.join('logs', filename))
f_handler.setLevel(logging.INFO)
f_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

# logger.addHandler(s_handler)
logger.addHandler(f_handler)
