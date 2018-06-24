import robot_service
robot = robot_service.RobotService()

def test_get_distance():
    d = robot.get_distance()    
    print("Distance: %.1f cm" % d)
test_get_distance()    