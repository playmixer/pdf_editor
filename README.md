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


***Dev server***
1. cd pdf_editor
2. env/Scripts/activate.bat
3. pip3 install -r requirement
4. python3 main.py


**Ubuntu**

**Дополнительный инструменты**

*  При включенном параметре *PDF_SHOW_REAL_PAGE_IMAGE* в config.py
>  Реальное отображение страниц PDF файла

1.  sudo apt-get install libmagickwand-dev
2.  sudo vi etc/Imagemagick-6/policy.xml

Изменить строку
>  `<policy domain="coder" rights="none" pattern="PDF" />`

на
>  `<policy domain="coder" rights="read|write" pattern="PDF" />`



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

