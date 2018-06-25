from flask import Flask, jsonify, request
from flask_cors import CORS
import robot_service

app = Flask(__name__)
CORS(app)
robot = robot_service.RobotService()


@app.route('/api/forward', methods=['GET'])
def move_forward():
    robot.move_forward()
    response = jsonify({'action': 'forward'})
    # print(response)
    print(response.data)
    return response


@app.route('/api/backward')
def move_backward():
    robot.move_backward()
    return jsonify({'action': 'backward'})


@app.route('/api/left')
def turn_left():
    robot.turn_left()
    return jsonify({'action': 'turn_left'})


@app.route('/api/right')
def turn_right():
    robot.turn_right()
    return jsonify({'action': 'turn_right'})


@app.route('/api/stop')
def stop():
    robot.stop()
    return jsonify({'action': 'stop'})


@app.route('/api/distance')
def distance():
    d = robot.get_distance()
    return jsonify({'distance': d})


@app.route('/api/speed', methods=['POST'])
def change_speed():
    sp = request.get_json().get('speed')
    print('Request speed at: ' + str(sp))
    real_speed = robot.change_speed(sp)
    print('Current real speed: ' + str(real_speed))
    return jsonify({'speed': real_speed})

def cleanup():
    robot.cleanup()
if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=8090, threaded=True)
    # If you press CTRL + C, cleanup and stop
    except KeyboardInterrupt:
        # Reset GPIO settings
        cleanup()
