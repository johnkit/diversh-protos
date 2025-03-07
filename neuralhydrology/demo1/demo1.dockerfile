ARG BASE_IMAGE=neuralhydrology:v1.11.0
FROM ${BASE_IMAGE}


RUN mkdir -p /experiments/.scratch

COPY . /demo1
WORKDIR /demo1
