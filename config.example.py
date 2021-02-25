import os

config = {
    "SUBDIRECTORY": "",  # должен начинаться с '/', "" = без поддиректории
    "STATIC_URL_PATH": "/static",
    "ALLOWED_EXTENSIONS": ['pdf'],
    "TEMPLATES": os.path.join("src", "templates"),
    "STATIC": os.path.join("src", "static"),
    "UPLOAD_FOLDER": os.path.abspath(os.path.join(os.path.dirname(__file__), "upload")),
    "MAX_SIZE_FILE": 50,
    "FILE_NAME_LENGTH": 20,
    "FILE_STORAGE_TIME": 600,  # секунд,
    "SHOW_REAL_PAGE_IMAGE": True,  # большая нагрузка
    "LONG_TIME_LOADING_REAL_IMAGES": 10,
    "IMAGE_RESOLUTION": 70
}
