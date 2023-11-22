import rtde_control
import rtde_receive
import math
import time

rtde_frequency = 500.0
rtde_c = rtde_control.RTDEControlInterface("", rtde_frequency) # add ip
blend_1 = 0.0
blend_2 = 0.02
blend_3 = 0.0
velocity = 0.5
acceleration = 0.3
pos1 = [-0.143, 0.835, 0.20, -0.001, 3.12, 0.04, velocity, acceleration, blend_1]
pos2 = [-0.5, 0, 0.20, -0.001, 3.12, 0.04, velocity, acceleration, blend_2]
pos3 = [-0.143, -0.835, 0.20, -0.001, 3.12, 0.04, velocity, acceleration, blend_3]
path = [pos1, pos2, pos3]
#rtde_c.moveJ([0, -math.pi/2, -math.pi/2, math.pi, 0, 0], 0.5, 0.3)
rtde_c.moveL(path)

# Read values
rtde_r = rtde_receive.RTDEReceiveInterface("") # ToDo : add ip
actual_q = rtde_r.getActualQ()
print(actual_q)
