FROM python:3.9-slim

RUN apt-get update && apt-get install -y --no-install-recommends curl

ENV POETRY_HOME=/opt/poetry POETRY_VIRTUALENVS_CREATE=false PYTHONPATH=/app

COPY poetry.lock pyproject.toml /app/

WORKDIR /app/

RUN curl -fsS -o install-poetry.py https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py && \
  python install-poetry.py -y && export PATH="/opt/poetry/bin:$PATH" &&  \
  poetry install --no-dev --no-interaction --no-root

COPY edtvelizydiscord/ /app

CMD ["python", "/app/main.py"]
