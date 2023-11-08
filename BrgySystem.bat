@echo off
call C:\Users\christian\Documents\GitHub\Brgy\venv\Scripts\activate
start python manage.py runserver
timeout /t 5 /nobreak >nul
start http://127.0.0.1:8000/