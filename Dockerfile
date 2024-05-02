FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        git \
        make \
        doxygen \
        openssh-client \
        software-properties-common \
        && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/*

RUN useradd -ms /bin/bash esphome

USER esphome

WORKDIR /workspaces/esphome-docs
ENV PATH="${PATH}:/home/esphome/.local/bin"

COPY requirements.txt ./
RUN pip3 install --no-cache-dir --no-binary :all: -r requirements.txt

EXPOSE 8000

CMD ["make", "live-html"]

LABEL \
        org.opencontainers.image.title="esphome-docs" \
        org.opencontainers.image.description="An image to help with ESPHomes documentation development" \
        org.opencontainers.image.vendor="ESPHome" \
        org.opencontainers.image.licenses="CC BY-NC-SA 4.0" \
        org.opencontainers.image.url="https://esphome.io" \
        org.opencontainers.image.source="https://github.com/esphome/esphome-docs" \
        org.opencontainers.image.documentation="https://github.com/esphome/esphome-docs/blob/current/README.md"
