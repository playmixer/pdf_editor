import os

config = {
    # Только для дев сервера
    "DEV_DEBUG": True,
    "DEV_HOST": "localhost",
    "DEV_PORT": 5000,
    #

    "ALLOWED_EXTENSIONS": ['pdf'],
    "TEMPLATES": os.path.join("src", "templates"),
    "STATIC": os.path.join("src", "static"),
    "UPLOAD_FOLDER": os.path.abspath(os.path.join(os.path.dirname(__file__), "upload")),
    "MAX_SIZE_FILE": 100,
    "FILE_NAME_LENGTH": 20,
    "FILE_STORAGE_TIME": 600,  # 60 = 1 мин,
    "PDF_SHOW_REAL_PAGE_IMAGE": False,  # большая нагрузка
}
