import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

ON = 1; OFF = 0;
DISTANCE_SLEEP = 0.05
TOO_CLOSE_THRESHOLD_TIME = 0.04

# Speed of sound as cm/s
SPEED_OF_SOUND = 34326

# Define pins out/int for SRC04 distance sensor
PIN_TRIGGER = 7
PIN_ECHO = 11


class Ir:
    def __init__(self):
        self.setup()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Ir, cls).__new__(cls)
        return cls.instance

    def setup(self):
        GPIO.setup(PIN_TRIGGER, GPIO.OUT)
        GPIO.setup(PIN_ECHO, GPIO.IN)

    def sleep(self, seconds):
        time.sleep(seconds)
        
    def get_distance(self):
        """get obstacle distance
        """
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(PIN_TRIGGER, GPIO.OUT)
        GPIO.setup(PIN_ECHO, GPIO.IN)
        # Send 10us pulse to trigger pin
        GPIO.output(PIN_TRIGGER, ON)
        time.sleep(0.00001)
        GPIO.output(PIN_TRIGGER, OFF)
        
        # Start the timer
        startTime = time.time()
        stop = startTime
        start = startTime

        # start time is reset until Echo pin is high
        while GPIO.input(PIN_ECHO) == 0 and start < startTime + 2:
            start = time.time()

        # Stop when Echo pin is no longer high
        while GPIO.input(PIN_ECHO) == 1 and stop < startTime + 2:
            stop = time.time()
        elapsedTime = stop - start
        distance = (elapsedTime * SPEED_OF_SOUND) / 2
        return distance
        
