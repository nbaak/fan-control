#!/usr/bin/env python3

from flask import Flask
from lib.Fan import Fan
import argparse
import threading

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


app = Flask(__name__)

DEBUG = args.DEBUG

fan = Fan(debug = DEBUG)


def fan_worker():
    global fan
    fan.start()


@app.route("/start")
def start():
    if not fan.is_service_running():        
        t = threading.Thread(target=fan_worker)
        t.start()
        
        return "start"
        
    else:
        return "already running"

@app.route("/stop")
def stop():
    if fan.is_service_running():
        fan.stop()
        return "stop"
    else:
        return "not running"

@app.route("/status")
def status():
    return f"Service active: {fan.is_service_running()}<br>Fan running: {fan.is_fan_running()}<br>temperature: {fan.get_current_temperature()}<br>pwm signal: {fan.get_current_pwm_signal()}"

@app.route("/")
def main():
    return "MAIN"


if __name__ == "__main__":
    app.run(debug=DEBUG, host = '0.0.0.0', port=8888)
