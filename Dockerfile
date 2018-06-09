FROM ubuntu:xenial

RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        python3 \
        python3-pip \
        python3-setuptools \
        python3-pygments \
        git \
        make \
        doxygen \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/*

RUN pip3 install --no-cache-dir --no-binary :all: \
        sphinx \
        breathe

RUN curl -sL https://deb.nodesource.com/setup_7.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g html-minifier

VOLUME /data/esphomedocs
VOLUME /data/esphomelib
EXPOSE 8000
WORKDIR /data/esphomedocs

CMD ["make", "webserver"]
