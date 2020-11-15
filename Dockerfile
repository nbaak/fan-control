FROM k3nny0r/rpi-python

COPY /src /pwm_control

ENTRYPOINT ["/pwm_control/main.py"]