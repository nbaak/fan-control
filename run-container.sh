#!/bin/bash

THIS_DIR=$(dirname $(readlink -f $0))

if [ ! -d ./data ]; then
    mkdir ${THIS_DIR}/data
fi

docker rm -f fan
docker run -it --privileged \
    -v "${THIS_DIR}/src":/fan_control \
    --name fan \
    -d k3nny/fancontrol
