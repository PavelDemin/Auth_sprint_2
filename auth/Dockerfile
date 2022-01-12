FROM python:3.9.7 AS base

ENV PYTHONUNBUFFERED 1

COPY requirements.txt ./
RUN pip install -r requirements.txt --no-cache-dir

FROM base AS prod

ADD ./src/app /code/app
ADD ./src/manage.py /code/manage.py
ADD ./src/migrations /code/migrations

WORKDIR /code

ENV PYTHONPATH=/code

CMD flask db upgrade && python manage.py runserver

FROM base AS tests

COPY src/tests/functional/requirements.txt ./
RUN pip install -r requirements.txt

ADD ./src /code
WORKDIR /code

ENV PYTHONPATH=/code

CMD flask db upgrade && pytest