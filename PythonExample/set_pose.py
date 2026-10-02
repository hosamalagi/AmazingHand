import time
from src.hand_control.poses import material_classifier_pose_1
from src.hand_control.params import MaxSpeed
from src.hand_control.ServoBoard import start_servo_board_left

"""Script for driving the LEFT hand in a set position. To use the right hand change the start_servo_board function.
This position will for now just be used for training the material classifier model."""

def main():
    c=start_servo_board_left()

    material_classifier_pose_1(c, MaxSpeed)
    time.sleep(4)






if __name__ == '__main__':
    main()
    