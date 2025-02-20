FROM neuralhydrology:v1.11.0

RUN mkdir -p /experiments/.scratch

COPY . /demo1
WORKDIR /demo1
