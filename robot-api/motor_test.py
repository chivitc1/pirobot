import motor
from motor import Motor

SLEEP = 0.3        
# Test robot
def test():
    motor = Motor()
    try:
        motor.forward()
        motor.sleep(SLEEP) # pause

##        left()
##        time.sleep(SLEEP) # pause for 0.5 second
    
##        forward()
##        time.sleep(SLEEP)
    
##        right()
##        time.sleep(SLEEP)
##    
##        back()
##        time.sleep(SLEEP)

        motor.stopMotors()
    finally:
        # reset GPIO to origin
        motor.cleanup()
    
# call functions to test
test()