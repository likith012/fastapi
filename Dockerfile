FROM ubuntu:22.04

LABEL maintainer="Likith Reddy"

# Anaconda
ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"

# Prevent docker build get stopped by requesting user interaction
ENV DEBIAN_FRONTEND=noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN=true

# Python byte-code
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Encoding
ENV PYTHONIOENCODING=UTF-8
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Framework
ARG PYTHON_VERSION=3.10

# Linux dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ca-certificates \
    openssh-client \
    openssh-server \
    unzip \
    wget \
    nginx \
    supervisor

# Conda install
RUN cd /root \
    && wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && sh Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh \
    && conda install python=${PYTHON_VERSION} \
    && mkdir -p src

WORKDIR /root/src

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x scripts/docker_run.sh

CMD ["scripts/docker_run.sh"]
