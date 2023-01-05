First time using (Windows):
<br>
1.using Redis-x64-3.0.504.msi install Redis backend to act as a message broker for websocket protocal. restart sevice if it need.
<br>
2.install python version above 3.7
<br>
3.create a virtual environment name myenv: 
<br>
    -open cmd in root folder
    <br>
    -run command: "python -m venv myenv"
    <br>
    -run command: "myenv\scripts\activate.bat"
    <br>
    -install require package
    <br>
    -run command: "python -m pip install -r requirements.txt"
    <br>
4.double click StartServer.bat to run sever.
<br>
or using command:
<br>
    -myenv\scripts\activate.bat
    <br>
    -cd mysite
    <br>
    -python manage.py runserver 0.0.0.0:81
    <br>
5.Open webbrowser and type:  localhost:81 . 
<br>
or type external ip of this PC instead of localhost
<br>

Some funtion still not add yet. For example to add new machine type need to add it using database admin management. access "localhost:81/admin". Super user: datdq  ; pass: will04010098 
