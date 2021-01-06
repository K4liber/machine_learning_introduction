FROM python:3-alpine
# Update & Install dependencies
RUN apk update
RUN apk add --no-cache --update \
    openssl \
    ca-certificates \
    bzip2-dev \
    zlib-dev \
    readline-dev \
    build-base \
    linux-headers
RUN apk add cmake
RUN apk add --no-cache python3=3.8.5-r0
RUN python3 -m pip install --upgrade pip
RUN apk --update add gcc libgcc musl-dev jpeg-dev zlib-dev
#TODO CMD, Entrypoint - how it should look like?
#TODO How to allow the FTP communation?