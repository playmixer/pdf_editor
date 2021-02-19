import os


def copy_file(file_from, file_to):
    if not (os.path.exists(file_to) and os.path.isfile(file_to)):
        with open(file_from, 'r') as f:
            with open(file_to, 'w') as f_config:
                f_config.write(f.read())
        print(f'The {file_to} file has been created')
    else:
        print(f'{file_to} file exists')


# создаем дефолтные конфиги
copy_file('config.example.py', 'config.py')
