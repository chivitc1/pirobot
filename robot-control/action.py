import apiproxy
import time
from random import randint

STEP_SLEEP = 0.5
ROTATE_SLEEP = 0.5
BACK_SLEEP = 1


def forward(duration):
    start_time = time.time()
    while True:
        apiproxy.forward()
        time.sleep(STEP_SLEEP)
        apiproxy.stop()
        d = apiproxy.get_distance()
        print(d)
        eslape_time = time.time() - start_time
        print('eslaped time: %f'%eslape_time)
        if eslape_time >= duration:
            apiproxy.stop()
            break

        if d <= 15:
            back(BACK_SLEEP)
            number = randint(1, 2)
            if number == 1:
                direction = 'LEFT'
            else:
                direction = 'RIGHT'
            rotate(direction)


def stop():
    apiproxy.stop()


def get_distance():
    return apiproxy.get_distance()


def rotate(direction):
    while True:
        if direction == 'LEFT':
            apiproxy.left()
        else:
            apiproxy.right()
        time.sleep(ROTATE_SLEEP)
        apiproxy.stop()
        d = apiproxy.get_distance()
        if d > 15:
            break


def back(duration):
    apiproxy.back()
    time.sleep(duration)
    apiproxy.stop