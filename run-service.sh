#!/bin/bash
THIS_DIR=$(dirname $(readlink -f $0))

sudo nohup python3 ${THIS_DIR}/src/main.py &
