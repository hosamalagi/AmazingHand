SIDE_DICT = {
    "right": 0,
    "left": 1,}

#Right Hand Finger-IDs
FINGER_MOTORS_R_DICT = {
    "thumb": (7, 8),
    "index": (1, 2),
    "middle": (3, 4),
    "ring": (5, 6)
}

#Left Hand Finger-IDs
FINGER_MOTORS_L_DICT = {
    "thumb": (17, 18),
    "index": (15, 16),
    "middle": (13, 14),
    "ring": (11, 12),

}

INDEX_UPPER_TH = 720
INDEX_LOWER_TH = 60

MIDDLE_UPPER_TH = 700
MIDDLE_LOWER_TH = 120

RING_UPPER_TH = 700
RING_LOWER_TH = 60

THUMB_UPPER_TH = 1000
THUMB_LOWER_TH = 300

KP_INDEX = 0.03
KP_MIDDLE = 0.03
KP_RING = 0.03
KP_THUMB = 0.03
#be careful of the motor accruacy


#Data receiver Params for the UDP packets sent by the pytuner
MAX_UDP_PACKET_SIZE = 4096  # Maximum size of UDP packet to receive
UDP_DATA_PORT = 5003  # Port to receive data from the pytuner
SENSOR_COUNT = 4  # Number of sensors
WAIT_TIMEOUT = 1000
OFFSET=0 #Avoid negative values

#Data Processing Params
CALIBRATION_COUNT = 100  # Number of readings to average for 
HYST = 0


# Hand control Params
FINGER_COUNT = 4
MaxSpeed = 1.5
MinSpeed = 0.5
ControlSpeed = 1
MiddlePos = [8, -10, 10, 0, 4, -5, 6, -8] #RIGHT
#MiddlePos = [-7, -5, -5, 8, 8, 0, 0, -6] #LEFT
ANGLE_MAX=80
SIDE=SIDE_DICT["right"] #"left" or "right", left not implemented yet

