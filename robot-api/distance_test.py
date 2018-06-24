import distance
import time

ir = distance.Ir()

def test_distance():
    samples = set()
    for i in range(3):
        d = ir.get_distance()
        samples.add(d)
        time.sleep(0.005)
    print('Final distance value: %.0f cm' % min(samples))
test_distance()