FROM python:3.13-slim

ENV POETRY_HOME=/opt/poetry \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app


COPY pyproject.toml poetry.lock* ./

RUN python -m pip install poetry
RUN poetry install --no-root --no-interaction

COPY . .
