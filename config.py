import os

config = {
    "DEBUG": True,
    "HOST": "localhost",
    "PORT": 5000,
    "ALLOWED_EXTENSIONS": ['pdf'],
    "TEMPLATES": os.path.join("src", "templates"),
    "STATIC": os.path.join("src", "static"),
    "UPLOAD_FOLDER": "upload",
    "MAX_SIZE_FILE": 100,
    "FILE_NAME_LENGTH": 20,
    "FILE_STORAGE_TIME": 3600,
}
