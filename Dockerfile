FROM python:3.9-slim

ENV POETRY_HOME=/opt/poetry POETRY_VIRTUALENVS_CREATE=false PYTHONPATH=/app

COPY poetry.lock pyproject.toml /app/

WORKDIR /app/

RUN curl -fsS -o install-poetry.py https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py && \
  python install-poetry.py -y && . $POETRY_HOME/env && \
  poetry install --no-dev --no-interaction --no-root

COPY src/ /app

CMD python /app/main.py
