docker build --tag stocks_api:1.0 .

docker run -p 8000:80 -d --name my-stocks stocks_api:1.0
