#!/bin/bash

docker rmi -f k3nny/fancontrol
docker build -t k3nny/fancontrol .
