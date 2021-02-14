FROM python:3.9.1-alpine
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
RUN python -m pip install --upgrade pip
RUN apk --update add gcc libgcc musl-dev jpeg-dev zlib-dev
COPY ./requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt
RUN python -m pip install https://test-files.pythonhosted.org/packages/ce/62/894ee913970408dd01d79bc48724971c122aaede1e0697775c42eb303604/balticlsc-0.0.5-py3-none-any.whl#sha256=ffb7a5327539b5a8868989a95905ab64d20d4d791eda595bdd4fae8dece46fe1
#Do not update anything above
WORKDIR app
COPY __init__.py module/__init__.py
COPY configs module/configs
COPY content module/content
ENV FLASK_APP='/app/module/content/processing.py'
RUN echo $FLASK_APP
# Expose the Flask port
EXPOSE 80
ENTRYPOINT [ "flask", "run", "--host=0.0.0.0", "--port=80"]
