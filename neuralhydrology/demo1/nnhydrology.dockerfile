FROM python:3.12-slim

# System packages
RUN apt-get update && \
    apt-get install --no-install-recommends --yes \
    vim && \
    rm -rf /var/lib/apt/lists/*

# Python packages
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install -U pip
RUN pip install neuralhydrology

# Aliases
RUN echo "alias ll='ls -al'" >> /root/.bashrc

WORKDIR /experiments
CMD ["/bin/bash", "-l"]
