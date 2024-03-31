FROM python:3.12-bullseye
LABEL authors="dusty"
WORKDIR /src

RUN apt-get install bash make curl

COPY requirements.txt /src/requirements.txt

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -U setuptools \
    && pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH /src
ENV PYTHONUNBUFFERED 1

COPY manage.py /src
COPY hotel_crm /src

CMD set -xe; \
    python manage.py migrate --noinput; \
    python manage.py runserver 0.0.0.0:8000
