### Описание:
API проект, позволяющий добавлять произведения в категории и жанры, так же оставлять обзоры и комментарии к ним
### Технологии
Python 3.9, Django 2.2.16
### Запуск проекта в dev-режиме
Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/pozarnik/api_yamdb.git
```
```
cd api_yamdb
```
Cоздать и активировать виртуальное окружение:
```
python -m venv venv
```
```
source venv/Scripts/activate
```
```
python -m pip install --upgrade pip
```
Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
Выполнить миграции:
```
cd api_yamdb
```
```
python manage.py migrate
```
Запустить проект:
```
python manage.py runserver
```
### Документация по API
Запустите сервер и перейдите по адресу:
```
http://127.0.0.1:8000/redoc/
```
### Авторы
[pozarnik][link]

## License

MIT

   [link]: <https://github.com/pozarnik/>
