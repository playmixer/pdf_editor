import random
import string
from config import config


def get_random_string(name_length=None):
    length = name_length or config['FILE_NAME_LENGTH']
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str
