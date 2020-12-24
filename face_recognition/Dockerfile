FROM python:3-alpine

RUN apk update
# Update & Install dependencies
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
RUN python3 --version
RUN python3 -m pip install --upgrade pip
RUN apk --update add gcc libgcc musl-dev jpeg-dev zlib-dev
COPY requirements.txt ./
RUN python3 -m pip install --no-cache-dir -r requirements.txt
# Do not change anything above
COPY main.py main.py

ENTRYPOINT [ "python", "./main.py" ]
