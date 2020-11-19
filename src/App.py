#!/usr/bin/env python3

from flask import Flask, render_template, request
from lib.Fan import Fan
import argparse
import threading
from aiohttp.client import request

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
    
@app.route("/api/get/temperature")
def api_get_temperature():
    return str(fan.get_current_temperature())

@app.route("/api/get/service-status")
def api_get_service():
    return str(fan.is_service_running())

@app.route("/api/get/fan-status")
def api_get_fan_status():
    return str(fan.is_fan_running())

@app.route("/api/get/pwm", methods=["GET"])
def api_pwm():
    if request.method == "GET":        
        return str(fan.get_current_pwm_signal())
    
    else:
        pass
    

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
    
@app.route("/test")
def test():
    return render_template("index.html")

@app.route("/")
def main():
    return f"Service active: {fan.is_service_running()}<br>Fan running: {fan.is_fan_running()}<br>temperature: {fan.get_current_temperature()}<br>pwm signal: {fan.get_current_pwm_signal()}"


if __name__ == "__main__":
    app.run(debug=DEBUG, host = '0.0.0.0', port=8888)
