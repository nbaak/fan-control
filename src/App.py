#!/usr/bin/env python3

from flask import Flask, render_template, request
from lib.Fan import Fan
from lib.Bird import Bird
from lib.Config import Config

import argparse
import threading
import logging
import time
import pathlib


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
parser.add_argument('--twitter', dest='TWITTER', type=str2bool, default=False)

args = parser.parse_args()
DEBUG = args.DEBUG
TWITTER = args.TWITTER
twitter_service = False
  
# App
app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.diabled = True
log.setLevel(logging.ERROR)

app.logger.disabled = True


# Fan
fan = Fan(debug = DEBUG)
    
# I choose a thread over a process because it runs the IO Pins plus
# we ask the object for a lot of informations. A Thread is better with
# IO and the Process is for Processor intense operations.
def t_fan_worker():
    print ("launch fan")
    global fan
    fan.start()
    
    
def t_bird():
    print ("launch bird")
    
    current_path = pathlib.Path(__file__).parent.absolute()
    config = Config(f'{current_path}/config.json')
    bird = Bird(config.Api_Key, config.Api_Secret, config.Access_Token, config.Access_Token_Secret)
    
    while TWITTER:
        runing = fan.is_fan_running()
        last_run = fan.get_last_run()
        temperature = fan.get_current_temperature()
        
        message = f"Fan running: {runing}, Current Temperature: {temperature}°C, last run: {last_run}"
        bird.twitter(message)
        print (message)
        
        time.sleep(30 *60)  # w8 N * 60 sec
        
    
    
@app.route("/api/get/last-run")    
def api_get_last_run():
    last_run = ""
    for run in fan.get_last_run():
        last_run += f'<div class="run">{run}</div>'
        
    return last_run
    
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
            return "start temperature updated"
        elif command == "stop":
            fan.set_stop_temperature(value)
            return "stop temperature updated"
        else:
            return "ERROR"
    

@app.route("/start-twitter")
def start_twitter():
    global twitter_service
    # start service
    if not twitter_service and TWITTER:
        t = threading.Thread(target=t_bird)
        t.start()
        twitter_service = True
        return "started"
    
    else:
        return "already started"


def start():
    if not fan.is_service_running():        
        t = threading.Thread(target=t_fan_worker)
        t.start()
        
        return "started"
        
    else:
        return "already running"

def stop():
    if fan.is_service_running():
        fan.stop()
        return "stoped"
    else:
        return "not running"
    
@app.route("/")
def main():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=DEBUG, host = '0.0.0.0', port=8888)
