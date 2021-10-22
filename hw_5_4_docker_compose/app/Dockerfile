FROM python:3

ENV PYTHONUNBUFFERED=1

WORKDIR /stocks_products

COPY ./stocks_products .

RUN pip install -r ./requirements.txt
#RUN chmod +x ./entrypoint.sh
#
#ENTRYPOINT ["./entrypoint.sh"]
