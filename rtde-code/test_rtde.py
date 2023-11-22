#!/usr/bin/env python

# ToDO: args to choose values of variables such as poses, time per output, etc

### Imports ###
import sys
sys.path.append("..")
import logging, time
import rtde.rtde as rtde
import rtde.rtde_config as rtde_config
from picknplace import PickNPlace as PNP

### Functions ###
def setp_to_list(sp):
    sp_list = []
    for i in range(0, 6):
        sp_list.append(sp.__dict__["input_double_register_%i" % i])
    return sp_list

def list_to_setp(sp, list):
    for i in range(0, 6):
        sp.__dict__["input_double_register_%i" % i] = list[i]
    return sp

### Robot configs ###
ROBOT_HOST = "..." #! insert ip of the robot or ursim
ROBOT_PORT = 30004
config_filename = "configuration.xml"
logging.getLogger().setLevel(logging.INFO)

# keep_running = True

conf = rtde_config.ConfigFile(config_filename)
state_names, state_types = conf.get_recipe("state") # Define recipe to access robot's output (joints, tcp, actual states, etc)
setp_names, setp_types = conf.get_recipe("setp")    # Define recipe of inputs to the robot
watchdog_names, watchdog_types = conf.get_recipe("watchdog")

### Robot connection ###
con = rtde.RTDE(ROBOT_HOST, ROBOT_PORT)
connection_state = con.connect()

# Connect to robot loop
while connection_state != 0:
    time.sleep(0.5)
    connection_state = con.connect()
print("Robot connected")

# get controller version
con.get_controller_version()

### Setup recipes ###
TIME = 0.5 #seconds
FREQUENCY = 1/TIME # Read data 
con.send_output_setup(state_names, state_types, frequency=FREQUENCY) # Receive output from the robot: every X seconds, get values 
setp = con.send_input_setup(setp_names, setp_types)
watchdog = con.send_input_setup(watchdog_names, watchdog_types)

setp.input_double_register_0 = 0
setp.input_double_register_1 = 0
setp.input_double_register_2 = 0
setp.input_double_register_3 = 0
setp.input_double_register_4 = 0
setp.input_double_register_5 = 0

# The function "rtde_set_watchdog" in the "rtde_control_loop.urp" creates a 1 Hz watchdog
watchdog.input_int_register_0 = 0

# start data synchronization
if not con.send_start():
    sys.exit()

# Setpoints to move the robot to
start_pose = [-0.12, -0.43, 0, 0, 3.11, 0.04] # box's init pose # (x, y, z, r_x, r_y, r_z) 
drop_zone = [-0.12, -0.51, 0, 0, 3.11, 0.04] # box's drop zone (r_z axis is flipped 180 degre)

state = con.receive()
print(state.actual_TCP_pose) # read position and orientation of the robot

### Pick And Place ###
pnp = PNP()
watchdog.input_int_register_0 = 1
con.send(watchdog)  # sending mode == 1
list_to_setp(setp, start_pose)  # changing initial pose to setp
con.send(setp) # sending initial pose
pnp.pick()
pnp.goto(drop_zone)
pnp.place(drop_zone, state.actual_TCP_pose)

# while True:
#     print('Waiting for movej() to finish')
#     state = con.receive()
#     con.send(watchdog)
#     if state.output_bit_registers0_to_31 == False:
#         print('Proceeding to mode 2\n')
#         break


# ### Control loop ###
# while True:
#     # receive the current state
#     state = con.receive()
#     state.actual_TCP_pose() # read position and orientation of the robot

#     if state is None:
#         break

#     if state.output_int_register_0 != 0:
#         list_to_setp(setp, drop_zone)
        
#         con.send(setp) # send new setpoint


#     # kick watchdog
#     con.send(watchdog)

con.send_pause()
con.disconnect()
