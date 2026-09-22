import time
import numpy as np
from src.hand_control.params import SIDE, MiddlePos, FINGER_MOTORS_R_DICT, MaxSpeed, ANGLE_MAX




# def incremental_finger_move(controller, finger, start: list[int, int], goal: list[int, int], Speed, steps):
#     steps+=1 # include the last step

#     #calculate a step size for each motor
#     step_size = [(goal[0] - start[0])/steps, (goal[1] - start[1])/steps]

#     #move the finger in incremental steps
#     for i in range(1, steps):
#         move_finger(finger, start[0] + i * step_size[0], start[1] + i * step_size[1], Speed)
#         time.sleep(0.1)

#     #last step:
#     move_finger(finger, goal[0], goal[1], Speed)

    
    
def move_finger(controller, finger, Angle_1, Angle_2, Speed):
    if SIDE == 0:
        motor_1, motor_2 = FINGER_MOTORS_R_DICT[finger]

    # else:     #TODO: implement left hand if needed
    #     motor_1, motor_2 = FINGER_MOTORS_L_DICT[finger]
    time.sleep(0.002) #added afterwards

    controller.write_goal_speed(motor_1, Speed)
    time.sleep(0.0002)

    controller.write_goal_speed(motor_2, Speed)
    time.sleep(0.0002)

    pos_1 = np.deg2rad(MiddlePos[motor_1 - 1] + Angle_1)
    pos_2 = np.deg2rad(MiddlePos[motor_2 - 1] + Angle_2)

    controller.write_goal_position(motor_1, pos_1)
    controller.write_goal_position(motor_2, pos_2)

    time.sleep(0.005)
    # print(MiddlePos[motor_1 - 1] + Angle_1)
    # print(f"soll pos 1 {Angle_1}")
    # print(np.rad2deg(controller.read_goal_position(motor_1))-MiddlePos[motor_1 - 1])
    # # print(MiddlePos[motor_2 - 1] + Angle_2)
    # print(f"soll pos 2 {Angle_2}")
    # print(np.rad2deg(controller.read_goal_position(motor_2))-MiddlePos[motor_2 - 1])
    # print(np.rad2deg(controller.read_present_position(motor_1))-MiddlePos[motor_1 - 1])



def OpenHand(c):
    move_finger (c, "index",-35,35, MaxSpeed)
    move_finger (c, "middle",-35,35, MaxSpeed)
    move_finger (c, "ring",-35,35, MaxSpeed)
    move_finger (c, "thumb",-35,35, MaxSpeed)

def CloseHand(c):
    move_finger (c, "index",35,-35, MaxSpeed)
    move_finger (c, "middle",35,-35, MaxSpeed)
    move_finger (c, "ring",35,-35, MaxSpeed)
    move_finger (c, "thumb",35,-35, MaxSpeed)    

def open_finger(c, finger, speed):
    move_finger(c, finger, -ANGLE_MAX, ANGLE_MAX, speed)

def close_finger(c, finger, speed):
    move_finger(c, finger, ANGLE_MAX, -ANGLE_MAX, speed)

def OpenHandFull(c, speed):
    for finger in ["index", "middle", "ring", "thumb"]:
        open_finger(c, finger, speed)