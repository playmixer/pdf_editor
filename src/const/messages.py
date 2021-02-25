class Message:
    title = None
    description = None

    def __init__(self, title, description):
        self.title = title
        self.description = description


messages = {
    'file_not_found': {
        'title': 'Файл не найден',
        'description': 'Возможно прошло слишком много времени'
    },
    'file_corrupted': {
        'title': '{filename} поврежден',
        'description': 'Если вы уверены что файл в нормальном состояний, попробуйте "организовать" его, и использовать новый скачанный файл.'
    },
    'no_have_select_file': {
        'title': 'Нет выбранных файлов',
        'description': ''
    }
}
