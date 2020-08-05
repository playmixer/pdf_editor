PDF Editor



**Ubuntu**

**Виртуальная среда:**
1. sudo apt install -y python3-venv
2. cd pdf_editor
3. python3 -m venv env
4. source env/bin/activate
5. pip3 install -r requirements.txt

**Выйти из вируальной среды**
>  $ deactivate

**Prod server**
1. sudo apt install gunicorn3
2. cd pdf_editor
2. pip3 install -r requirements.txt
3. изменить настройки в gunicorn.config.py
3. gunicorn3 wsgi:app

**Dev server**
1. cd pdf_editor
2. source env/bin/activate
3. pip3 install -r requirement ***Только при первом запуске***
3. python3 main.py