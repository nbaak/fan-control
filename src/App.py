

from flask import Flask

app = Flask(__name__)

started = True
fan = None


@app.route("/start")
def start():
    global started
    if not started:
        started = True
        return "start"
        
    else:
        return "already running"

@app.route("/stop")
def stop():
    global started
    if started:
        started = False
        return "stop"
    else:
        return "not running"

@app.route("/status")
def status():
    return f"started: {started}"

@app.route("/")
def main():
    return "MAIN"


if __name__ == "__main__":
    app.run(debug=False, host = '0.0.0.0')