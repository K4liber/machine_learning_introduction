#!/bin/bash
app="face_recognition"
docker build -t ${app} .
docker stop ${app}
docker rm ${app}
docker run -d -p 56733:80 \
  --name=${app} \
  -v $PWD:/app ${app}
