#!/bin/bash

THIS_DIR=$(dirname $(readlink -f $0))

if [ ! -d ./data ]; then
    mkdir ${THIS_DIR}/data
fi

docker stop fan
docker rm fan
docker run -it --privileged \
    -p 8888:8888 \
    -v "${THIS_DIR}/src":/fan \
    --name fan \
    -d k3nny/fancontrol \
    python3.8 /fan/App.py --debug false
