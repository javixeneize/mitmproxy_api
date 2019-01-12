FROM python:3.7-alpine3.8

RUN apk update \
    && apk add --no-cache g++ libffi libffi-dev openssl openssl-dev shadow python3-dev\
    && pip3 install mitmproxy flask \
    && apk del --purge g++ libffi-dev openssl-dev python3-dev\
    && rm -rf ~/.cache/pip

RUN useradd -ms /bin/bash -u 1001 mitmproxy_api
WORKDIR /home/mitmproxy/
RUN chown mitmproxy_api /home/mitmproxy/
COPY src .
COPY script.sh .
RUN chmod +x script.sh
USER 1001
VOLUME /home/mitmproxy/.mitmproxy
EXPOSE 8080 8081
CMD ./script.sh


