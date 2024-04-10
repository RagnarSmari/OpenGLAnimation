import math 
from Base3DObjects import *

class Bezier:
    def __init__(self):
        self.endTime = 0.0
        self.startTime = 0.0

    def lerp(self, control_point_array, t):
        bezier = Point(0.0, 0.0, 0.0)
        ctrl1 = control_point_array[0]
        ctrl2 = control_point_array[1]
        ctrl3 = control_point_array[2]
        ctrl4 = control_point_array[3]
        bezier.x = pow((1-t), 3) * ctrl1.x + 3 * pow((1-t), 2) * t * ctrl2.x + 3 * (1-t) * pow(t, 2) * ctrl3.x + pow(t, 3) * ctrl4.x
        bezier.y = pow((1-t), 3) * ctrl1.y + 3 * pow((1-t), 2) * t * ctrl2.y + 3 * (1-t) * pow(t, 2) * ctrl3.y + pow(t, 3) * ctrl4.y
        bezier.z = pow((1-t), 3) * ctrl1.z + 3 * pow((1-t), 2) * t * ctrl2.z + 3 * (1-t) * pow(t, 2) * ctrl3.z + pow(t, 3) * ctrl4.z
        return bezier

    def get_bezier_position(self, currentTime, ctrl_points, startTime=None, endTime=None):
        # print("time ", currentTime)
        bezier = Point(0.0, 0.0, 0.0)
        if currentTime < startTime:
            bezier = ctrl_points[0]
            return bezier
        elif currentTime > endTime:
            bezier = ctrl_points[-1]
            return bezier
        else:
            t = (currentTime - startTime) / (endTime - startTime)
            return self.lerp(ctrl_points, t)




