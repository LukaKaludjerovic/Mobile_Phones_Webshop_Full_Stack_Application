@echo off
if exist staticfiles (
    rmdir /s /q staticfiles
)
python manage.py collectstatic
python manage.py runserver