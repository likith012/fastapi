FROM python:3.10-slim-buster

LABEL maintainer="Likith Reddy"

# Prevent docker build get stopped by requesting user interaction
ENV DEBIAN_FRONTEND=noninteractive

# Python byte-code
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Encoding
ENV PYTHONIOENCODING=UTF-8
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Variables
ARG ROOT=/root

RUN mkdir -p ${ROOT}/src

WORKDIR ${ROOT}/src

COPY requirements.txt .

RUN python -m venv venv \
    && venv/bin/pip install --no-cache-dir -r requirements.txt \
    && echo 'source venv/bin/activate' >> ${ROOT}/.bashrc

COPY . .

RUN chmod +x scripts/docker_run.sh

CMD ["/bin/bash", "-c", "source ~/.bashrc && scripts/docker_run.sh"]
