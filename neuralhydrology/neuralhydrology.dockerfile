FROM python:3.12-slim

# Version must be passed in
ARG version
RUN if [ -z "$version" ]; then echo "version is required" && exit 1; fi

# System packages
# (none)

# Python packages
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install -U pip

RUN pip install neuralhydrology==${version}

# Aliases
RUN echo "alias ll='ls -al'" >> /root/.bashrc

CMD ["/bin/bash", "-l"]
