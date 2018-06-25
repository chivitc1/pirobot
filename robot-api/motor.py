import time
import RPi.GPIO as GPIO

ON = 1; OFF = 0;

# Motor control pins
FORWARD_A = 18; BACK_A = 16; ENABLE_A = 12;
FORWARD_B = 13; BACK_B = 15; ENABLE_B = 33;
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


class Motor:
    def __init__(self):
        self.speed = DEFAULT_SPEED
        self.motorA = None
        self.motorB = None
        self.setup()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Motor, cls).__new__(cls)
        return cls.instance

    def setup(self):
        # Set pin numbering by board
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        # Set the pins to be output pins
        GPIO.setup(FORWARD_A, GPIO.OUT)
        GPIO.setup(BACK_A, GPIO.OUT)
        GPIO.setup(ENABLE_A, GPIO.OUT)

        GPIO.setup(FORWARD_B, GPIO.OUT)
        GPIO.setup(BACK_B, GPIO.OUT)
        GPIO.setup(ENABLE_B, GPIO.OUT)

        # Set frequency for motor driver pins
        self.motorA = GPIO.PWM(ENABLE_A, FREQUENCY)
        self.motorB = GPIO.PWM(ENABLE_B, FREQUENCY)    
        # Start software PWM with duty cycle 0 (not moving)
        self.motorA.start(0)
        self.motorB.start(0)

    # Turn all motors off
    def stopMotors(self):
        self.motorA.ChangeDutyCycle(0)
        self.motorB.ChangeDutyCycle(0)
        self.drive(STOP)

    # Drive motor A, B by set 4 pins status
    def drive(self, statusList):
        self.motorA.ChangeDutyCycle(DUTY_CYCLE_A)
        self.motorB.ChangeDutyCycle(DUTY_CYCLE_A)
        for idx, pin in enumerate(PINS):
            GPIO.output(pin, statusList[idx])
        
    # Turn both motors forwards to go forward
    def forward(self):
        self.drive(MOVE_FWD)

    # Turn both motors backward to go back
    def back(self):
        self.drive(MOVE_BACK)

    # Turn left
    def left(self):
        self.drive(TURN_LEFT)
        
    # Turn right
    def right(self):
        self.drive(TURN_RIGHT)
        
    def set_speed(self, sp):        
        if self.MIN_SPEED <= sp <= self.MAX_SPEED:
            self.speed = sp
        else:
            self.speed = self.DEFAULT_SPEED
        DUTY_CYCLE_A = sp
        DUTY_CYCLE_B = sp
        return self.speed
    
    def set_speed_a(self, sp):
        DUTY_CYCLE_A = sp
    
    def set_speed_b(self, sp):
        DUTY_CYCLE_B = sp
        
    def sleep(self, seconds):
        time.sleep(seconds)
        
    def cleanup(self):
        GPIO.cleanup()

