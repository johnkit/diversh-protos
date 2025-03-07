FROM pytorch/pytorch:2.5.1-cuda12.1-cudnn9-runtime

# Setup verson env
COPY neuralhydrology.version.txt /tmp/version.txt
RUN VERSION=$(cat /tmp/version.txt) && \
    echo "export VERSION=\"$VERSION\"" > /tmp/version.env
RUN . /tmp/version.env && echo Building version ${VERSION}

# System packages
# (none)

# Python packages
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# RUN pip install -U pip

RUN . /tmp/version.env && pip install neuralhydrology==$VERSION

# Aliases
RUN echo "alias ll='ls -al'" >> /root/.bashrc

CMD ["/bin/bash", "-l"]
