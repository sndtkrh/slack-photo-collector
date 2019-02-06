# Python
FROM ubuntu:18.04

ENV DEBIAN_FRONTEND noninteractive
  
RUN apt-get update \
  && apt-get install --yes --no-install-recommends \
    build-essential \
    python3-dev \
    python3-pip \
    python3-setuptools \
  && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install slackbot

COPY . /slack-photo-collector
WORKDIR /slack-photo-collector
CMD python3 run.py