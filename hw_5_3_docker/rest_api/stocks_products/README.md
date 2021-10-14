Лог контейнера
C:\Python\Модуль 5. Python в веб-разработке\hw\my-hw-py-web\hw_5_3_docker\rest_api>docker logs my-stocks
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
October 14, 2021 - 15:40:19
Django version 3.2.8, using settings 'stocks_products.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.


Команды
docker build --tag stocks_api:1.0 .

docker run -p 8000:80 -d --name my-stocks stocks_api:1.0


