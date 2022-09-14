# Dockerfile
# Docker multistage build with poetry venv
FROM python:3.10-slim-buster as python-base

ENV GUNICORN_VERSION=20.1.0 \
    GEVENT_VERSION=21.12.0

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \ 
    PIPX_HOME="/opt/pipx" \
    PIPX_BIN_DIR="/usr/local/bin" \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

# adding env path
ENV PATH="${POETRY_HOME}/bin:${VENV_PATH}/bin:$PATH"

# builder-base is used to build dependencies
FROM python-base as builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    curl \
    build-essential

RUN pip3 install pipx-in-pipx && pipx install poetry
# RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

# We copy our Python requirements here to cache them 
# and install only runtime deps using poetry
WORKDIR $PYSETUP_PATH
COPY ./poetry.lock ./pyproject.toml ./
RUN poetry install --no-dev
# RUN poetry add gunicorn==${GUNICORN_VERSION}
# RUN poetry add gevent==${GEVENT_VERSION}

# Production Base
FROM python-base as production

COPY --from=builder-base $VENV_PATH $VENV_PATH

# This is a special case. We need to run this script as an entry point:
COPY ./gunicorn.sh ./gunicorn_config.py ./
RUN chmod +x '/gunicorn.sh'

COPY . /app
WORKDIR /app

EXPOSE 3001
ENTRYPOINT ["/gunicorn.sh"]