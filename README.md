# База данных сотовых телефонов

# Репозиторий команды проекта "Создание базы данных сотовых телефонов"

## Программное обеспечение

Требуемые модули Python:
  - django
  - openpyxl

Приложение написано на Django:
  - Официальный сайт проекта Django - https://www.djangoproject.com
  - Исходный код - https://github.com/django/django

На фронте использованы Bootstrap 5.0
  - Официальный сайт фреймворка Bootstrap 5.0 - https://getbootstrap.com
  - Исходный код - https://github.com/twbs/bootstrap

и bootstrap-select:
  - Исходный код - https://github.com/snapappointments/bootstrap-select

## СУБД

Разработка и тестирование проводились на СУБД MySQL. Фреймворк Django также поддерживает по умолчанию MySQL, PostgreSQL, MariaDB, Oracle и SQLite (подробнее: https://docs.djangoproject.com/en/4.0/ref/databases/). 

Настройка СУБД осуществляется правкой параметра `DATABASES` в конфиг-файле `magnitdb/magnitdb/setting.py`

## Развертывание

Django приложение представляет из себя `wsgi` приложение. Процесс развертывания состоит в настройке сервера для исполнения Python кода как `wsgi` приложения. Например, для сервера Apache требуется установить модуль `mod_wsgi` и настроить его (подробнее: https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/modwsgi/). Имя приложения задается параметром `WSGI_APPLICATION` в конфиг-файле `magnitdb/magnitdb/setting.py` и установлено по умолчанию `magnitdb.wsgi.application`.
