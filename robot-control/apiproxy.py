import requests

BASE_URL = 'http://pi.my:8090/api/'
TIME_OUT = 5

def stop():
    requests.get(BASE_URL + 'stop', timeout=TIME_OUT)


def forward():
    requests.get(BASE_URL + 'forward', timeout=TIME_OUT)


def back():
    requests.get(BASE_URL + 'backward', timeout=TIME_OUT)


def left():
    requests.get(BASE_URL + 'left', timeout=TIME_OUT)


def right():
    requests.get(BASE_URL + 'right', timeout=TIME_OUT)


def change_speed(sp):
    payload = {'speed': sp}
    r = requests.post(BASE_URL + 'speed', json=payload, timeout=TIME_OUT)
    if r.status_code == 200:
        real_speed = r.json()['speed']
        return real_speed


def get_distance():
    r = requests.get(BASE_URL + 'distance', timeout=TIME_OUT)
    if r.status_code == 200:
        d = r.json()['distance']
        return d