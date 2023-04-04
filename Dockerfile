FROM python:3.9-slim

WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt .

RUN apt -y update && apt-get -y install default-libmysqlclient-dev

RUN pip install -r requirements.txt

COPY . /usr/src/app/

RUN apt -y update && apt install  -y vim

CMD python /usr/src/app/manage.py runserver 0.0.0.0:5000
