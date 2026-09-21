"""Implementation of a state machine used for proximity servoing of the AH
"""

from enum import Enum

class States(Enum):
    NO_OBJECT=0
    OVER_TH=1
    UNDER_TH=2


class StateMachine():
    def __init__(self, upper_th, lower_th):
        """Initialize with state is no object"""

        self.UPPER_TH=upper_th
        self.LOWER_TH=lower_th
        self.state = States.NO_OBJECT
    
    def update(self, data):
        if data >= self.UPPER_TH:
            self.state = States.OVER_TH
        elif data < self.LOWER_TH:
            self.state = States.NO_OBJECT
        else:
            self.state = States.UNDER_TH

        return
            
            
        
    

