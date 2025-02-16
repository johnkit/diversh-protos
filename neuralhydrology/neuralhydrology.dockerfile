FROM python:3.12-slim

# System packages
# (none)

# Python packages
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install -U pip
RUN pip install neuralhydrology==1.11.0

# Aliases
RUN echo "alias ll='ls -al'" >> /root/.bashrc

CMD ["/bin/bash", "-l"]
