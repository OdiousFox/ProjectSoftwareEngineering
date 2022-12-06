# ProjectSoftwareEngineering

## How to run webserver
The webserver is running using Django framework. Therefore, you need to have python version 3.x to run. Dowload the python interpreter, then you need to create virtual environment in python. Run the following command
```python=
python -m venv "your project folder"
```
For example on Window system
```python=
D:\ACmeasure>python -m venv my_proj
```
New folder named "my_proj" will be created in directory "D:\ACmeasure". Go to "my_proj" directory then go to "Script" then activate "activate.bat" file
```cmd=

D:\ACmeasure>cd my_proj

D:\ACmeasure\my_proj>cd Scripts

D:\ACmeasure\my_proj\Scripts>activate.bat

(my_proj) D:\ACmeasure\my_proj\Scripts>
```
Then install django framework by running command
```cmd=
(my_proj) D:\ACmeasure\my_proj\Scripts>pip install Django
```
Then install paho-mqtt library bu running command
```cmd=
(my_proj) D:\ACmeasure\my_proj\Scripts>pip install paho-mqtt
```

On Linux or Mac OS, the process is the same just when you activate virtual environment, you need to run "source bin/activate"
```bash=
minh@DESKTOP-Q7J9KK5:/mnt/d/ACmeasure$ python3 -m venv my_pro
minh@DESKTOP-Q7J9KK5:/mnt/d/ACmeasure$ cd my_pro
minh@DESKTOP-Q7J9KK5:/mnt/d/ACmeasure/my_pro$
minh@DESKTOP-Q7J9KK5:/mnt/d/ACmeasure/my_pro$ source bin/activate
(my_pro) minh@DESKTOP-Q7J9KK5:/mnt/d/ACmeasure/my_pro$
```
after that the process to install Django and paho-mqtt is same as in the Window.

Now dowload the project as Zip file and unzip it
Then go to "my_server" directory then run command
```python=
python manage.py runserver
```
The django server now run at localhost, port 8000
To get the webpage, just go to web browser and type 
```
http://127.0.0.1:8000/webserver/
```
If you want get JSON api just type on web browser
```
http://127.0.0.1:8000/webserver/api/
```
If you want to end the server you need to exit the terminal running server.
