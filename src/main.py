#!/usr/bin/env python3

from lib.Fan import Fan
import argparse

def str2bool(value):
    if isinstance(value, bool):
        return value
    
    if value.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif value.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

parser = argparse.ArgumentParser(description="Fan Controler")
parser.add_argument('--debug', dest='DEBUG', type=str2bool, default=True)

args = parser.parse_args()

DEBUG = args.DEBUG

fan = Fan(debug = DEBUG)
fan.start()



