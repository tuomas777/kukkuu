FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN mkdir /code

COPY requirements.txt requirements-dev.txt /code/

WORKDIR /code

RUN pip install --upgrade pip \
    && pip install -r /code/requirements.txt \
    && pip install -r /code/requirements-dev.txt \
    && pip install pip-tools

COPY . /code
