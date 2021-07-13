FROM python:3.8-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        git \
        make \
        doxygen \
        openssh-client \
        software-properties-common \
        && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/*

COPY requirements.txt .
RUN pip3 install --no-cache-dir --no-binary :all: -r requirements.txt

EXPOSE 8000
WORKDIR /data/esphomedocs

CMD ["make", "webserver"]
