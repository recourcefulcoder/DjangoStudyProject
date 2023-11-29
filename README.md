![pipeline](https://gitlab.crja72.ru/django_2023/projects/business-manager_14/badges/main/pipeline.svg)
# Инструкция по запуску проекта в dev-режиме
## Установка виртуального окружения
```sh
python -m venv venv
```
## Активация виртуального окружения
```sh
venv\Scripts\activate
```
## Установка зависимостей для работы с проектом
```sh
pip install -r requirements/dev.txt
```
Для корректной работы проекта в продакшен-среде достаточно установки prod.txt
```sh
pip install -r requirements/prod.txt
```
## Установка зависимостей для тестирования проекта
```sh
pip install -r requirements/test.txt
```
## Настройка переменных виртуального окружения
### Создайте файл ".env" в корневой директории вашего проекта. Скопируйте в этот файл переменные из ".env.template", изменив данные в них на свои. Этих переменных хватит для корректного запуска проекта.
## Компиляция сообщений для перевода:
```sh
django-admin makemessages -l en
django-admin makemessages -l ru
django-admin compilemessages
```
## Создание миграций и их применение:
```sh
python manage.py makemigrations
python manage.py migrate
```
## Запуск проекта в dev-режиме
```sh
python manage.py runserver
```