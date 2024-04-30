VERSION 0.8
FROM python:3.12
WORKDIR /code

ARG --global APP_NAME = "blat-cli"
ARG --global USERNAME = "blat"

RUN apt-get update && apt-get install -y libnss3 libnspr4 libdbus-1-3 libatk1.0-0 \
        libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libatspi2.0-0 libxcomposite1 \
        libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2 x11vnc xvfb fluxbox wmctrl

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
    SAVE IMAGE blat/$APP_NAME:latest
