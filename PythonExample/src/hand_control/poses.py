from src.hand_control.hand_move import move_finger_left
import time
import numpy as np


def material_classifier_pose_1(c, speed):
    """This pose is implemented for the left hand"""

    for finger in ["index","middle","ring"]:
        move_finger_left(c, finger, 0, 0, speed)

    move_finger_left(c, "thumb", 0, 0, speed)