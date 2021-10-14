FROM python

ENV PYTHONUNBUFFERED=1

WORKDIR /stocks_products

COPY ./stocks_products/logistic ./logistic
COPY ./stocks_products/stocks_products ./stocks_products
COPY ./stocks_products/__init__.py .
COPY ./stocks_products/manage.py .
COPY ./stocks_products/requirements.txt .

RUN pip install -r /stocks_products/requirements.txt
RUN python ./manage.py migrate

CMD ["python", "./manage.py", "runserver"]
