import rtde_control
import rtde_receive
from robotiq_gripper_control import RobotiqGripper
import numpy as np
import time

def log_info(gripper):
    print(f"Pos: {str(gripper.get_current_position()): >3}  "
          f"Open: {gripper.is_open(): <2}  "
          f"Closed: {gripper.is_closed(): <2}  ")

class PickNPlace:
    def __init__(self, rtde_c, rtde_r, gripper, eps=0.001):
        self.rtde_c = rtde_c
        self.rtde_r = rtde_r
        self.gripper = gripper
        self.eps = eps

    def pick(self, pose):
        """ This function is used to grab and object """
        # check if actual_pose and drop_zone are the same (or very close)
        # if true: grip
        # else: move until contact ?
        
        if abs(np.array(self.rtde_r.getActualQ()) - np.array(pose)) < self.eps:
            # Activate gripper (grab cube)
            self.gripper.close()
            time.sleep(1)
        else:
            # move to contact
            pass

    def place(self, pose):
        """ This function is used to place to grab and object """
        # check if actual_pose and drop_zone are the same (or very close)
        # if true: drop
        # else: raise "did not drop because not at drop zone"
        if abs(np.array(self.rtde_r.getActualQ()) - np.array(pose)) < self.eps:
            # Open gripper
            self.gripper.open()
            time.sleep(1)
        else:
            raise "Not close enough to drop zone"

    def move(self, desired_pose, mvmt="moveL"):
        """ This function is used to go to a desired position """
        if mvmt == "moveJ":
            print("Using moveJ function")
            self.rtde_c.moveJ(get_inverse_kin(desired_pose), 1, 1) # ToDo: check real fonction of inverse kinematics
        elif mvmt == "moveL":
            print("Using moveL function")
            self.rtde_c.moveL(desired_pose, 1, 1)
        elif mvmt == "servoJ":
            print("Using servoJ function")
            self.rtde_c.servoJ(get_inverse_kin(desired_pose), 1, 1) # ToDo: check real fonction of inverse kinematics
        elif mvmt == "gripper":
            self.gripper.move_and_wait_for_pos(255, 255, 255) # ToDo: change values here
            log_info(self.gripper) 
        