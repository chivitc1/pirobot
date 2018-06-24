import os, sys
path = sys.path
path1 = os.path.dirname(os.path.realpath('robot-control/__init__.py'))
path2 = os.path.dirname(os.path.realpath('robot-api/__init__.py'))
path.append(path1 + '/robot_service.py')
path.append(path1 + '/views.py')
path.append(path2 + '/motor.py')
print(path)