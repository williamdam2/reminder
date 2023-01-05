@echo off
echo Starting Server

cmd /c "myenv\Scripts\activate.bat & python mysite\manage.py runserver 0.0.0.0:81"