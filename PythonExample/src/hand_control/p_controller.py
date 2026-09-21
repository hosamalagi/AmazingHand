"""Implementation of proportional controlling"""

from src.hand_control.prox_state_machine import States, StateMachine
from src.hand_control.params import ANGLE_MAX, ControlSpeed, MiddlePos
from src.hand_control.hand_move import move_finger
import numpy as np


class PController:
    """Classic P-Controller, could be expanded to PID later."""

    def __init__(self, kp, upper_th, lower_th):
        self.kp = kp
        self.max_value = kp * (upper_th - lower_th)

    def solve(self, goal, actual):
        return self.kp * (goal - actual)
        
# class SpeedPController:
#     """Controls servo speed using a PController and manages state."""

#     def __init__(self, kp, upper_th, lower_th):
#         self.solve = PController(kp)
#         self.state_machine = [ #all fingers
#             StateMachine(upper_th, lower_th),
#             StateMachine(upper_th, lower_th),
#             StateMachine(upper_th, lower_th),
#             StateMachine(upper_th, lower_th),
#         ]

#     def update(self, i, actual):
#         self.state_machine[i].update(actual)

#     @property
#     def state(self, i):
#         return self.state_machine[i].state

#     def calc_speed(self, goal, actual):

#         speed = MaxSpeed *abs(self.controller.solve(goal, actual))/self.controller.max_value

#         if speed>MaxSpeed:
#             speed=MaxSpeed
#         elif speed < MinSpeed:
#             speed=MinSpeed

#         return round(speed, 1)

class PosPController:
    """Controls servo position for one finger."""

    def __init__(self, kp, upper_th, lower_th, scs):
        self.controller = PController(kp, upper_th, lower_th)
        self.state_machine = StateMachine(upper_th, lower_th)
        self.scs = scs

    def update(self, actual):
        self.state_machine.update(actual)

    @property
    def state(self):
        return self.state_machine.state

    def present_pos(self, finger):
        motor_1 = finger.motor_1
        motor_2 = finger.motor_2

        present_pos1 = (
            np.rad2deg(self.scs.read_present_position(motor_1)[0])
            - MiddlePos[motor_1 - 1]
        )

        present_pos2 = (
            np.rad2deg(self.scs.read_present_position(motor_2)[0])
            - MiddlePos[motor_2 - 1]
        )

        return present_pos1, present_pos2

    def control_finger_pos(self, finger, goal, actual):
        value_p = self.controller.solve(goal, actual)

        pp = self.present_pos(finger)

        new_pos1 = value_p + pp[0]
        new_pos2 = -value_p + pp[1]

        # Cap the positions
        new_pos1 = max(-ANGLE_MAX, min(ANGLE_MAX, new_pos1))
        new_pos2 = max(-ANGLE_MAX, min(ANGLE_MAX, new_pos2))

        move_finger(
            self.scs,
            finger.name,
            new_pos1,
            new_pos2,
            ControlSpeed
        )


        

    




        
        
    