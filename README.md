First time using (Windows):
1.using Redis-x64-3.0.504.msi install Redis backend to act as a message broker for websocket protocal. restart sevice if it need.
2.install python version above 3.7
3.create a virtual environment name myenv: 
    -open cmd in root folder
    -run command: "python -m venv myenv"
    -run command: "myenv\scripts\activate.bat"
    -install require package
    -run command: "python -m pip install -r requirements.txt"
4.double click StartServer.bat to run sever.
or using command:
    -myenv\scripts\activate.bat
    -cd mysite
    -python manage.py runserver 0.0.0.0:81
5.Open webbrowser and type:  localhost:81 . 
or type external ip of this PC instead of localhost

Some funtion still not add yet. For example to add new machine type need to add it using database admin management. access "localhost:81/admin". Super user: datdq  ; pass: will04010098 
