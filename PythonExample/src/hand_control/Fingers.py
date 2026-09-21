from src.hand_control.prox_state_machine import StateMachine
from src.hand_control.params import (
    INDEX_UPPER_TH, INDEX_LOWER_TH,
    MIDDLE_UPPER_TH, MIDDLE_LOWER_TH,
    RING_UPPER_TH, RING_LOWER_TH,
    THUMB_UPPER_TH, THUMB_LOWER_TH,
    KP_INDEX, KP_MIDDLE, KP_RING, KP_THUMB
)
from src.hand_control.p_controller import PosPController
from src.hand_control.data_processing import calibrate_baseline
from src.hand_control.params import MiddlePos
import numpy as np


class Finger:
    """Class that contains information about the finger configuration."""

class Finger:
    """Class that contains information about the finger configuration."""

    def __init__(self, name, motor_1, motor_2, sensor_slot, upper_th, lower_th, KP, c):
        self.name = name
        self.motor_1 = motor_1
        self.motor_2 = motor_2
        self.sensor_slot = sensor_slot
        self.upper_th = upper_th
        self.lower_th = lower_th
        self.present_pos1 = 0
        self.present_pos2 = 0
        self.baseline = 0
        self.sensor_data = 0
        self.calibrated_data = 0
        self.poscontroller = PosPController(KP, upper_th, lower_th, c)


class Hand:
    """Contains all four fingers."""

    def __init__(self, c, udp):
        self.c = c
        self.udp_receiver = udp
        self.fingers = [
            Finger("index",  1, 2, 1, INDEX_UPPER_TH,  INDEX_LOWER_TH,  KP_INDEX,  c),
            Finger("middle", 3, 4, 2, MIDDLE_UPPER_TH, MIDDLE_LOWER_TH, KP_MIDDLE, c),
            Finger("ring",   5, 6, 3, RING_UPPER_TH,   RING_LOWER_TH,   KP_RING,   c),
            Finger("thumb",  7, 8, 0, THUMB_UPPER_TH,  THUMB_LOWER_TH,  KP_THUMB,  c),
        ]

    def set_baseline(self):
        print("Calibrating...")

        calibration_data = calibrate_baseline(self.udp_receiver)

        for finger in self.fingers:
            finger.baseline = calibration_data[finger.sensor_slot]

        print(
            "Calibration complete. Baseline values:",
            [finger.baseline for finger in self.fingers]
        )

    def set_sensor_data(self, sensor_data):
        for finger in self.fingers:
            finger.sensor_data = sensor_data[finger.sensor_slot]
            finger.calibrated_data = (
                finger.sensor_data - finger.baseline
            )

    def update_present_positions(self):
        for finger in self.fingers:
            finger.present_pos1 = (
                np.rad2deg(
                    self.c.read_present_position(finger.motor_1)[0]
                )
                - MiddlePos[finger.motor_1 - 1]
            )

            finger.present_pos2 = (
                np.rad2deg(
                    self.c.read_present_position(finger.motor_2)[0]
                )
                - MiddlePos[finger.motor_2 - 1]
            )
