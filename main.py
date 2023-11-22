import rtde_control
import rtde_receive
from robotiq_gripper_control import RobotiqGripper
from picknplace import PickNPlace
import time
import argparse

# ** Petite note à prendre en compte **
# Le cube fait 0.04m en X,Y,Z. Donc sont point central est (0.02, 0.02, 0.02). 
# Le plus important à noter c'est sa hauteur (axe Z si je me trompe pas) car
# il faut que le TCP du robot soit bien centré à sa hauteur donc une chose est sûre :
# Si tout est au même niveau, le robot doit être à la hauteur 0.02m pour gripper et pour déposer.

### Constants ###
IP_ADDRESS = "192.168.1.21" # "localhost"
READ_FREQUENCY = 2 # every 500 ms

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Flexible inputs")
    parser.add_argument("--ip",
            help="IP address of the UR robot",
            type=str,
            default=IP_ADDRESS,
            metavar="<IP address of the UR robot>")
    parser.add_argument("--ip_gripper",
            help="IP address of the gripper",
            type=str,
            default=IP_ADDRESS,
            metavar="<IP address of the gripper>")
    parser.add_argument("--output",
            help="data output (.csv) file to write to (default is \"Vention_UR10e_TakeHome.csv\"",
            type=str,
            default="Vention_UR10e_TakeHome.csv",
            metavar="<data output file>")
    parser.add_argument("--frequency",
            help="the frequency at which the data is recorded",
            type=float,
            default=READ_FREQUENCY,
            metavar="<frequency>")
    
    args = parser.parse_args()

    # Connect to the Control and Receive panel (i/o) of the RTDE Interface
    rtde_c = rtde_control.RTDEControlInterface(args.ip)
    rtde_r = rtde_receive.RTDEReceiveInterface(args.ip, args.frequency)
    
    # Create gripper and connect
    gripper = RobotiqGripper(rtde_c)

    # Activate the gripper and initialize force and speed
    gripper.activate()  # returns to previous position after activation
    gripper.set_force(50)  # from 0 to 100 %
    gripper.set_speed(50)  # from 0 to 100 %

    # Define some poses to test out 
    robot_init = [-1.54, -1.83, -2.28, -0.59, 1.60, 0.023]
    pose_pick = [-0.143, 0.835, 0.02, -0.001, 3.12, 0.04]
    pose_drop = [0.0, -0.835, 0.02, -0.001, 3.12, 0.04]   

    # Initialising PickNPlace class
    pnp = PickNPlace(rtde_c, rtde_r, gripper)

    # Move to initial robot pose
    pnp.move(robot_init)

    actual_q = rtde_r.getActualQ()
    print(actual_q)

    # Pick N Place actions
    pnp.move(pose_pick)
    pnp.pick(pose_pick)
    pnp.move(pose_drop)
    pnp.place(pose_drop)

    # Stop the RTDE control script 
    rtde_c.stopScript()
