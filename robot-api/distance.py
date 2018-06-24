import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

ON = 1; OFF = 0;
DISTANCE_SLEEP = 0.05
TOO_CLOSE_THRESHOLD_TIME = 0.04

#Speed of sound as cm/s
SPEED_OF_SOUND = 34326

#Define pins out/int for SRC04 distance sensor
PIN_TRIGGER = 7
PIN_ECHO = 11

class Ir:
    def __init__(self):
        self.setup()
    def setup(self):
        GPIO.setup(PIN_TRIGGER, GPIO.OUT)
        GPIO.setup(PIN_ECHO, GPIO.IN)

    def sleep(self, seconds):
        time.sleep(seconds)
        
    def get_distance(self):
        """get obstacle distance
        """    
        # Set trigger to OFF (low)
        GPIO.output(PIN_TRIGGER, OFF)

        # Allow module to settle
        time.sleep(DISTANCE_SLEEP)

        # Send 10us pulse to trigger pin
        GPIO.output(PIN_TRIGGER, ON)
        time.sleep(0.00001)
        GPIO.output(PIN_TRIGGER, OFF)

        # Start the timer
        startTime = time.time()

        # start time is reset until Echo pin is high
        while GPIO.input(PIN_ECHO) == 0:
            startTime = time.time()

        # Stop when Echo pin is no longer high
        while GPIO.input(PIN_ECHO) == 1:
            stopTime = time.time()
            # If sensor is too close to object, pi cannot see the echo quickly enough
            # so it has to detect that problem and say what has happened
            if stopTime - startTime >= TOO_CLOSE_THRESHOLD_TIME:
                print("Hold on there! You're too close for me to see.")
                stopTime = startTime
                break
            
        # Calculate puls length
        elapsedTime = stopTime - startTime
        distance = (elapsedTime * SPEED_OF_SOUND) / 2
        return distance
        
