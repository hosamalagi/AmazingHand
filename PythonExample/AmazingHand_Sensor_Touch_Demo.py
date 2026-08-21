import time
import socket
import numpy as np
import json

from rustypot import Scs0009PyController

#Side
Side = 1 # 1=> Right Hand // 2=> Left Hand


#Speed
MaxSpeed = 7
CloseSpeed = 3

#Fingers middle poses
MiddlePos = [8, -10, 10, 0, 4, -5, 6, -8] # replace values by your calibration results # our calibrated values

#Parameters for the Data
MAX_UDP_PACKET_SIZE = 4096  # Maximum size of UDP packet to receive
TOUCH_THRESHOLD=4000  # Threshold for touch detection
WIDGET_COUNT = 4
SENSOR_COUNT = 4  # Number of sensors expected in the data
TOUCH_STATES=[False] * WIDGET_COUNT  # Initialize touch states for each widget


c = Scs0009PyController(
        serial_port="/dev/serial/by-id/usb-1a86_USB_Single_Serial_5B42139153-if00",
        baudrate=1000000,
        timeout=0.5,
    )


#recieve sensordata from pytuner, use the data to control the hand
def main():

    #Initialize UDP socket to receive data from the pytuner
    sock_pytuner = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_pytuner.bind(("127.0.0.1", 5000))
    sock_pytuner.setblocking(False)
    
    # c.write_torque_enable(1, 1)  #1 = On / 2 = Off / 3 = Free
    t0 = time.time()
    OpenHand()
    time.sleep(1)

    while True:
        t = time.time() - t0
       

        sensor_data = get_sensor_data(sock_pytuner)
        touch_states = check_touch(sensor_data)

        #Close the hand if any of the touch sensors are activated
        if any(touch_states):
            print("TOUCH DETECTED:", sensor_data)

            CloseHand()

            time.sleep(3)

            OpenHand()

            time.sleep(3)



def get_sensor_data(sock: socket.socket) -> list[int]:
    # Receive sensor data from the UDP socket and return it as a list of integers
    latest_data = None

 
    while True:   #Drain the socket to get the latest data packet
        try:
            data, address = sock.recvfrom(MAX_UDP_PACKET_SIZE)
            latest_data = data
        except BlockingIOError:
            break

    if latest_data is None:
        return []

    message = json.loads(latest_data.decode())
    return message["values"]

def check_touch(sensor_values: list[int]) -> list[bool]:
    # Check if the sensor values exceed the touch threshold
    return [value > TOUCH_THRESHOLD for value in sensor_values]

def OpenHand():
    Move_Index (-35,35, MaxSpeed)
    Move_Middle (-35,35, MaxSpeed)
    Move_Ring (-35,35, MaxSpeed)
    Move_Thumb (-35,35, MaxSpeed)

def CloseHand():
    Move_Index (90,-90, CloseSpeed)
    Move_Middle (90,-90, CloseSpeed)
    Move_Ring (90,-90, CloseSpeed)
    Move_Thumb (90,-90, CloseSpeed+1)

def OpenHand_Progressive():
    Move_Index (-35,35, MaxSpeed-2)
    time.sleep(0.2)
    Move_Middle (-35,35, MaxSpeed-2)
    time.sleep(0.2)
    Move_Ring (-35,35, MaxSpeed-2)
    time.sleep(0.2)
    Move_Thumb (-35,35, MaxSpeed-2)

def SpreadHand():
    if (Side==1): # Right Hand
        Move_Index (4, 90, MaxSpeed)
        Move_Middle (-32, 32, MaxSpeed)
        Move_Ring (-90, -4, MaxSpeed)
        Move_Thumb (-90, -4, MaxSpeed)  
  
    if (Side==2): # Left Hand
        Move_Index (-60, 0, MaxSpeed)
        Move_Middle (-35, 35, MaxSpeed)
        Move_Ring (-4, 90, MaxSpeed)
        Move_Thumb (-4, 90, MaxSpeed)  
  
def ClenchHand():
    if (Side==1): # Right Hand
        Move_Index (-60, 0, MaxSpeed)
        Move_Middle (-35, 35, MaxSpeed)
        Move_Ring (0, 70, MaxSpeed)
        Move_Thumb (-4, 90, MaxSpeed)  
  
    if (Side==2): # Left Hand
        Move_Index (0, 60, MaxSpeed)
        Move_Middle (-35, 35, MaxSpeed)
        Move_Ring (-70, 0, MaxSpeed)
        Move_Thumb (-90, -4, MaxSpeed)
  
def Index_Pointing():
    Move_Index (-40, 40, MaxSpeed)
    Move_Middle (90, -90, MaxSpeed)
    Move_Ring (90, -90, MaxSpeed)
    Move_Thumb (90, -90, MaxSpeed)
  
def Nonono():
  Index_Pointing()
  for i in range(3) :
        time.sleep(0.2)
        Move_Index (-10, 80, MaxSpeed)
        time.sleep(0.2)
        Move_Index (-80, 10, MaxSpeed)
  
  Move_Index (-35, 35, MaxSpeed)
  time.sleep(0.4)
  
def Perfect():
  if (Side==1): #Right Hand
        Move_Index (50, -50, MaxSpeed)
        Move_Middle (0, -0, MaxSpeed)
        Move_Ring (-20, 20, MaxSpeed)
        Move_Thumb (65, 12, MaxSpeed)

  
  if (Side==2): #Left Hand
        Move_Index (50, -50, MaxSpeed)
        Move_Middle (0, -0, MaxSpeed)
        Move_Ring (-20, 20, MaxSpeed)
        Move_Thumb (-12, -65, MaxSpeed)
  
def Victory():
  if (Side==1): #Right Hand 
        Move_Index (-15, 65, MaxSpeed)
        Move_Middle (-65, 15, MaxSpeed)
        Move_Ring (90, -90, MaxSpeed)
        Move_Thumb (90, -90, MaxSpeed)

  
  if (Side==2): #Left Hand
        Move_Index (-65, 15, MaxSpeed)
        Move_Middle (-15, 65, MaxSpeed)
        Move_Ring (90, -90, MaxSpeed)
        Move_Thumb (90, -90, MaxSpeed)
  
def Pinched():
  if (Side==1): #Right Hand
        Move_Index (90, -90, MaxSpeed)
        Move_Middle (90, -90, MaxSpeed)
        Move_Ring (90, -90, MaxSpeed)
        Move_Thumb (0, -75, MaxSpeed)

  if (Side==2): #Left Hand
        Move_Index (90, -90, MaxSpeed)
        Move_Middle (90, -90, MaxSpeed)
        Move_Ring (90, -90, MaxSpeed)
        Move_Thumb (75, 5, MaxSpeed)

def Scissors():
  Victory();
  if (Side==1): #Right Hand
        for i in range(3):  
            time.sleep(0.2)
            Move_Index (-50, 20, MaxSpeed)
            Move_Middle (-20, 50, MaxSpeed)
            
            time.sleep(0.2)
            Move_Index (-15, 65, MaxSpeed)
            Move_Middle (-65, 15, MaxSpeed)
    

  if (Side==2): #Left Hand
        for i in range(3):
            time.sleep(0.2)
            Move_Index (-20, 50, MaxSpeed)
            Move_Middle (-50, 20, MaxSpeed)
            
            time.sleep(0.2)
            Move_Index (-65, 15, MaxSpeed)
            Move_Middle (-15, 65, MaxSpeed)

def Fuck():

  if (Side==1): #Right Hand
        Move_Index (90, -90, MaxSpeed)
        Move_Middle (-35, 35, MaxSpeed)
        Move_Ring (90, -90, MaxSpeed)
        Move_Thumb (0, -75, MaxSpeed)

  if (Side==2): #Left Hand
        Move_Index (90, -90, MaxSpeed)
        Move_Middle (-35, 35, MaxSpeed)
        Move_Ring (90, -90, MaxSpeed)
        Move_Thumb (75, 0, MaxSpeed)
  
def Move_Index (Angle_1,Angle_2,Speed):
    
    c.write_goal_speed(1, Speed)
    time.sleep(0.0002)
    c.write_goal_speed(2, Speed)
    time.sleep(0.0002)
    Pos_1 = np.deg2rad(MiddlePos[0]+Angle_1)
    Pos_2 = np.deg2rad(MiddlePos[1]+Angle_2)
    c.write_goal_position(1, Pos_1)
    c.write_goal_position(2, Pos_2)
    time.sleep(0.005)

def Move_Middle(Angle_1,Angle_2,Speed):    
    c.write_goal_speed(3, Speed)
    time.sleep(0.0002)
    c.write_goal_speed(4, Speed)
    time.sleep(0.0002)
    Pos_1 = np.deg2rad(MiddlePos[2]+Angle_1)
    Pos_2 = np.deg2rad(MiddlePos[3]+Angle_2)
    c.write_goal_position(3, Pos_1)
    c.write_goal_position(4, Pos_2)
    time.sleep(0.005)

def Move_Ring(Angle_1,Angle_2,Speed):    
    c.write_goal_speed(5, Speed)
    time.sleep(0.0002)
    c.write_goal_speed(6, Speed)
    time.sleep(0.0002)
    Pos_1 = np.deg2rad(MiddlePos[4]+Angle_1)
    Pos_2 = np.deg2rad(MiddlePos[5]+Angle_2)
    c.write_goal_position(5, Pos_1)
    c.write_goal_position(6, Pos_2)
    time.sleep(0.005)

def Move_Thumb(Angle_1,Angle_2,Speed):    
    c.write_goal_speed(7, Speed)
    time.sleep(0.0002)
    c.write_goal_speed(8, Speed)
    time.sleep(0.0002)
    Pos_1 = np.deg2rad(MiddlePos[6]+Angle_1)
    Pos_2 = np.deg2rad(MiddlePos[7]+Angle_2)
    c.write_goal_position(7, Pos_1)
    c.write_goal_position(8, Pos_2)
    time.sleep(0.005)


if __name__ == '__main__':
    main()



