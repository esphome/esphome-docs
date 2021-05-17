FROM ubuntu:focal
ENV TZ=UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        python3 \
        python3-pip \
        python3-setuptools \
        python3-pygments \
        git \
        make \
        doxygen \
        openssh-client \
        software-properties-common \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/*

RUN pip3 install --no-cache-dir --no-binary :all: \
        sphinx

EXPOSE 8000
WORKDIR /data/esphomedocs

CMD ["make", "webserver"]

