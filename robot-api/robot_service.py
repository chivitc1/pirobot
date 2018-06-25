import motor 
import distance


class RobotService:

    def __init__(self):        
        self.motor = motor.Motor()
        self.ir = distance.Ir()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(RobotService, cls).__new__(cls)
        return cls.instance

    def move_forward(self):
        self.motor.forward()
        print("MOVE FORWARD")        

    def move_backward(self):
        self.motor.back()
        print("MOVE BACKWARD")

    def turn_left(self):
        self.motor.left()
        print("TURN LEFT")

    def turn_right(self):
        self.motor.right()
        print("TURN RIGHT")

    def stop(self):
        self.motor.stop()
        print("STOP")

    def change_speed(self, sp):        
        real_speed = self.motor.set_speed(sp)
        print("AT SPEED: " + str(real_speed))
        return real_speed

    def get_distance(self):
        MEASURE_SLEEP = 0.005
        MEASURE_COUNT = 3
        samples = set()
        for i in range(MEASURE_COUNT):
            d = self.ir.get_distance()
            samples.add(d)
            self.ir.sleep(MEASURE_SLEEP)
        d = round(min(samples), 1)
        return d
    
    def cleanup(self):
        self.motor.cleanup()
