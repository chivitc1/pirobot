#!/usr/bin/python

from flask import request, jsonify
from flask_api import FlaskAPI
from flask_cors import CORS

import time
import RPi.GPIO as GPIO

######################### COMMON
ON = 1; OFF = 0;
# Set pin numbering by board
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


######################### PINS
# Motor control pins
FORWARD_A = 18; BACK_A = 16; ENABLE_A = 12;
FORWARD_B = 13; BACK_B = 15; ENABLE_B = 33;

GPIO.setup(FORWARD_A, GPIO.OUT)
GPIO.setup(BACK_A, GPIO.OUT)
GPIO.setup(ENABLE_A, GPIO.OUT)

GPIO.setup(FORWARD_B, GPIO.OUT)
GPIO.setup(BACK_B, GPIO.OUT)
GPIO.setup(ENABLE_B, GPIO.OUT)
    
# Define pins out/int for SRC04 distance sensor
PIN_TRIGGER = 7
PIN_ECHO = 11

GPIO.setup(PIN_TRIGGER, GPIO.OUT)
GPIO.setup(PIN_ECHO, GPIO.IN)

IR_RETRIES = 5
IR_MAX = 70
IR_MIN = 0
######################### MOTOR SETTINGS ###############

PINS = [FORWARD_A, FORWARD_B, BACK_A, BACK_B]
# Move action states
MOVE_FWD = [ON, ON, OFF, OFF]
MOVE_BACK = [OFF, OFF, ON, ON]
TURN_LEFT = [OFF, ON, ON, OFF]
TURN_RIGHT = [ON, OFF, OFF, ON]
STOP = [OFF, OFF, OFF, OFF]

# Speed control settings
# How many times to turn the pin on and off each second.(should fixed)
# warning: too high (100) or too low (10) will not move the motor
FREQUENCY = 50
# How long the pin stays on each cycle: 50 => 50% of cycle is on; 100 => always on
DUTY_CYCLE_A = 30.0
DUTY_CYCLE_B = 30.0

DEFAULT_SPEED = 30
MAX_SPEED = 50
MIN_SPEED = 15

speed = DEFAULT_SPEED
# Set frequency for motor driver pins
motorA = GPIO.PWM(ENABLE_A, FREQUENCY)
motorB = GPIO.PWM(ENABLE_B, FREQUENCY)
# Start software PWM with duty cycle 0 (not moving)
motorA.start(0)
motorB.start(0)


################################# IR distance setting #############

DISTANCE_SLEEP = 0.05
TOO_CLOSE_THRESHOLD_TIME = 0.04

# Speed of sound as cm/s
SPEED_OF_SOUND = 34326


##################################### motor func ###########

# Turn all motors off
def stop_motors():
    motorA.ChangeDutyCycle(0)
    motorB.ChangeDutyCycle(0)
    drive(STOP)


# Drive motor A, B by set 4 pins status
def drive(statusList):
    motorA.ChangeDutyCycle(DUTY_CYCLE_A)
    motorB.ChangeDutyCycle(DUTY_CYCLE_A)
    for idx, pin in enumerate(PINS):
        GPIO.output(pin, statusList[idx])


# Turn both motors forwards to go forward
def forward():
    drive(MOVE_FWD)


# Turn both motors backward to go back
def back():
    drive(MOVE_BACK)


# Turn left
def left():
    drive(TURN_LEFT)


# Turn right
def right():
    drive(TURN_RIGHT)


def set_speed(sp):
    if MIN_SPEED <= sp <= MAX_SPEED:
        speed = sp
    else:
        speed = DEFAULT_SPEED
    DUTY_CYCLE_A = sp
    DUTY_CYCLE_B = sp
    return speed
##################################### END motor func ###########

##################################### IR distance func #########

def get_distance():
    """get obstacle distance
    """
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(PIN_TRIGGER, GPIO.OUT)
    GPIO.setup(PIN_ECHO, GPIO.IN)
        
    # Wait sensor to settle
    time.sleep(1)
    # Send 10us pulse to trigger pin
    GPIO.output(PIN_TRIGGER, ON)
    time.sleep(0.00001)
    GPIO.output(PIN_TRIGGER, OFF)

    # Start the timer
    start_time = time.time()
    start = start_time
    stop = start_time

    # start time is reset until Echo pin is high
    while GPIO.input(PIN_ECHO) == 0 and start < start_time + 2:
        start = time.time()

    # Stop when Echo pin is no longer high
    while GPIO.input(PIN_ECHO) == 1 and stop < start_time + 2:
        stop = time.time()
    
    # Calculate puls length
    elapsed_time = stop - start
    distance = (elapsed_time * SPEED_OF_SOUND) / 2
    return distance

##################################### END IR distance func #########
##################################### Web API ################
app = FlaskAPI(__name__)
CORS(app)

@app.route('/api/forward', methods=['GET'])
def move_forward():
    forward()
    response = jsonify({'action': 'forward'})
    return response


@app.route('/api/backward')
def move_backward():
    back()
    return jsonify({'action': 'backward'})


@app.route('/api/left')
def turn_left():
    left()
    return jsonify({'action': 'turn_left'})


@app.route('/api/right')
def turn_right():
    right()
    return jsonify({'action': 'turn_right'})


@app.route('/api/stop')
def stop():
    stop_motors()
    return jsonify({'action': 'stop'})


@app.route('/api/distance')
def distance():    
    for i in range(IR_RETRIES):
        d = get_distance()
        if (d > IR_MIN and d < IR_MAX):
            break;
        # time.sleep(0.005)
    if (d <= IR_MIN or d >= IR_MAX):
        raise ValueError('Bad thing happened to IR. Could not measure distance')
    return jsonify({'distance': d})


@app.route('/api/speed', methods=['POST'])
def change_speed():
    sp = request.get_json().get('speed')
    print('Request speed at: ' + str(sp))
    real_speed = set_speed(sp)
    print('Current real speed: ' + str(real_speed))
    return jsonify({'speed': real_speed})


################################### END Web API################

##################### MAIN


try:
    GPIO.setwarnings(False)
    if __name__ == "__main__":
        app.run(host='0.0.0.0', port=8090, threaded=True, debug=False)
finally:
    GPIO.cleanup()
