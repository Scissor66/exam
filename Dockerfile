FROM python:3.6-buster
MAINTAINER syukhno
ENV PYTHONUNBUFFERED 1

RUN mkdir /app && mkdir /var/log/exam
WORKDIR /app
COPY requirements.txt /app/
COPY exam/ /app/exam/
COPY manage.py /app/
RUN pip install -r /app/requirements.txt
