
class RobotService:
    DEFAULT_SPEED = 30
    MAX_SPEED = 50
    MIN_SPEED = 15

    def __init__(self, speed=DEFAULT_SPEED):
        self.speed = speed

    def move_forward(self):
        print("MOVE FORWARD")

    def move_backward(self):
        print("MOVE BACKWARD")

    def turn_left(self):
        print("TURN LEFT")

    def turn_right(self):
        print("TURN RIGHT")

    def stop(self):
        print("STOP")

    def change_speed(self, sp):
        print("CHANGE SPEED")
        if self.MIN_SPEED <= sp <= self.MAX_SPEED:
            self.speed = sp
        else:
            self.speed = self.DEFAULT_SPEED
        return self.speed

    def get_distance(self):
        print("GET DISTANCE")
        return 20
