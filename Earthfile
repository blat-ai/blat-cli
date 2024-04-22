VERSION 0.8
FROM python:3.11
WORKDIR /code

ARG --global APP_NAME = "blat-cli"
ARG --global USERNAME = "blat"

RUN groupadd --gid 1001 $USERNAME
RUN useradd --create-home --no-log-init --uid 1001 --gid 1001 $USERNAME

USER $USERNAME

ENV HOME ${HOME:-/home/$USERNAME}
ENV PATH $HOME/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN pip install "poetry>=1.6,<1.7"

lock-deps:
    COPY pyproject.toml poetry.lock .
    RUN poetry lock
    SAVE ARTIFACT poetry.lock AS LOCAL poetry.lock

build:
    COPY pyproject.toml poetry.lock ./
    RUN poetry install --no-root
    COPY . .
    SAVE IMAGE blat/$APP_NAME:latest
