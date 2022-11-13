FROM python:3.10-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /var/www

COPY requirements.txt .

RUN apk update && apk add musl-dev gcc libpq-dev && pip install -r requirements.txt

COPY . .

EXPOSE 8000