import distance
import time
from threading import Thread
import RPi.GPIO as GPIO

ir = distance.Ir()

def test_distance():
    samples = set()
    for i in range(10):
        d = ir.get_distance()
        samples.add(d)
        time.sleep(0.005)
        print(d)
    print('Final distance value: %.0f cm' % min(samples))
def test_distance2():
    while True:
        d = ir.get_distance()
        time.sleep(0.01)
        print(d)
    
try:
    th = Thread(target=test_distance2, args=())
    th.start()
    print('Outer')
    time.sleep(1)
finally:
    GPIO.cleanup()
