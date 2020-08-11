PDF Editor

Используется Python3. Рекомендуется python 3.6+

**Windows**

***Виртуальная среда:***
1. cd pdf_editor
2. python -m venv env
3. env\Scripts\activate.bat
4. pip install -r requirements.txt

***Выйти из вируальной среды***
*  env\Scripts\deactivate.bat

***Prod server***
1.  cd pdf_editor
2.  pip install waitress
3.  python waitress_server.py

***Dev server***
1. cd pdf_editor
2. env/Scripts/activate.bat
3. pip install -r requirement
4. python main.py


**Ubuntu**


***Виртуальная среда:***
1. sudo apt install -y python3-venv
2. cd pdf_editor
3. python3 -m venv env 
4. source env/bin/activate
5. pip3 install -r requirements.txt

***Выйти из вируальной среды***
*  $ deactivate

***Prod server***
1. sudo apt install gunicorn3
2. cd pdf_editor
2. pip3 install -r requirements.txt
3. выставить настройки в gunicorn.config.py, кол-во воркеров, хост, порт
3. gunicorn3 wsgi:app

***Dev server***
1. cd pdf_editor
2. source env/bin/activate
3. pip3 install -r requirement
3. python3 main.py


**Дополнительный инструменты**

**При включенном параметре *PDF_SHOW_REAL_PAGE_IMAGE* в config.py**
>  Реальное изображение страниц PDF файла

*Для Ubuntu*

1.  sudo apt-get install libmagickwand-dev
2.  sudo vi etc/Imagemagick-6/policy.xml

Изменить строку
>  `<policy domain="coder" rights="none" pattern="PDF" />`

на
>  `<policy domain="coder" rights="read|write" pattern="PDF" />`

3.  sudo apt-get install ghostscript

*Для Windows*

*  Установить библиотеку [ImageMagick](https://imagemagick.org/download/binaries/ImageMagick-7.0.10-26-Q16-HDRI-x64-dll.exe)


**Инструкция по установке**

1. Установить python 3, Gunicorn и сопутствующие библиотеки
>  sudo apt-get install -y python3-pip python3-dev python3-venv gunicorn3 libmagickwand-dev ghostscript


2. Разрешение на редактирование PDF
>  sudo vi etc/Imagemagick-6/policy.xml

Изменить строку
>  `<policy domain="coder" rights="none" pattern="PDF" />`

на
>  `<policy domain="coder" rights="read|write" pattern="PDF" />`

2. Скопировать репозиторий
>  git clone https://gitlab.oilpc.local/Shkirya.NS/pdf_editor.git

3. Зайти в папку приложения
>  cd pdf_editor

4. Создаем виртуальное окружение и запускаем его
*  >  python3 -m venv env
*  >  source env/bin/activate

5. Установить завимости
>  pip install -r requirements.txt

6. Запустить сервер
>  gunicorn --bind 0.0.0.0:8800 --workers 3 wsgi:app


**Развернутакая инструкция**
>  https://medium.com/faun/deploy-flask-app-with-nginx-using-gunicorn-7fda4f50066a
