#!/usr/bin/env python3

from flask import Flask, render_template, request
from lib.Fan import Fan
import argparse
import threading
import logging

def str2bool(value):
    if isinstance(value, bool):
        return value
    
    if value.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif value.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

# Args
parser = argparse.ArgumentParser(description="Fan Controler")
parser.add_argument('--debug', dest='DEBUG', type=str2bool, default=True)

args = parser.parse_args()
DEBUG = args.DEBUG

  
# App
app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.diabled = True
log.setLevel(logging.ERROR)

app.logger.disabled = True


# Fan
fan = Fan(debug = DEBUG)
    

def t_fan_worker():
    global fan
    fan.start()
    
@app.route("/api/get/temperature")
def api_get_temperature():
    return str(fan.get_current_temperature())

@app.route("/api/get/start-temperature")
def api_get_start_temperature():
    return str(fan.get_start_temperature())

@app.route("/api/get/stop-temperature")
def api_get_stop_temperature():
    return str(fan.get_stop_temperature())


@app.route("/api/get/service-status")
def api_get_service():
    return str(fan.is_service_running())

@app.route("/api/get/fan-status")
def api_get_fan_status():
    return str(fan.is_fan_running())

@app.route("/api/get/pwm", methods=["GET"])
def api_get_pwm():        
    return str(fan.get_current_pwm_signal())

@app.route("/api/post/pwm", methods=["POST"])
def api_post_pwm():
    if request.method == "POST":
        pass

@app.route("/api/post/service", methods=["POST"])
def api_post_service():    
    if request.method == "POST":
        command = request.form["command"]
        
        if command == 'start':
            return start()
        elif command == 'stop':
            return stop()
            
        else:
            return 'ERROR'
        
        
@app.route("/api/post/start-stop-temperatures", methods=["POST"])
def api_post_start_stop_temperatures():
    if request.method == "POST":
        command = request.form["command"]
        value = request.form["value"]
        
        print (f"command: {command}, value: {value}")
        
        if command == "start":
            fan.set_start_temperature(value)
            return fan.START_TEMP
        elif command == "stop":
            fan.set_stop_temperature(value)
            return fan.STOP_TEMP
        else:
            return "ERROR"
    

def start():
    if not fan.is_service_running():        
        t = threading.Thread(target=t_fan_worker)
        t.start()
        
        return "start"
        
    else:
        return "already running"

def stop():
    if fan.is_service_running():
        fan.stop()
        return "stop"
    else:
        return "not running"
    
@app.route("/")
def main():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=DEBUG, host = '0.0.0.0', port=8888)
