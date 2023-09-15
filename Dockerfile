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

WORKDIR /data/esphomedocs
RUN curl -o pagefind-v1.0.2-x86_64-unknown-linux-musl.tar.gz https://github.com/CloudCannon/pagefind/releases/download/v1.0.2/pagefind-v1.0.2-x86_64-unknown-linux-musl.tar.gz -L
RUN tar xzf pagefind-v1.0.2-x86_64-unknown-linux-musl.tar.gz
RUN rm pagefind-v1.0.2-x86_64-unknown-linux-musl.tar.gz
RUN mv pagefind /usr/local/bin

EXPOSE 8000

CMD ["make", "live-html"]
