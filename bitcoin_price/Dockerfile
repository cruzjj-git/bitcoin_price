# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster

ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux

WORKDIR /app

RUN apt-get update -yqq \
  && pip install --upgrade pip \
  && apt-get install python3-dev pkg-config graphviz-dev graphviz libgraphviz-dev gcc vim curl mlocate default-jdk -yqq
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .


