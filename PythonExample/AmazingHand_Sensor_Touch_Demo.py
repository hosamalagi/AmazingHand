import time
from src.hand_control.hand_move import open_finger, OpenHandFull
from src.hand_control.params import UDP_DATA_PORT, ControlSpeed, MaxSpeed, CONTROL_TIME
from src.hand_control.receiver import UDPReceiver
from src.hand_control.prox_state_machine import States
from src.hand_control.ServoBoard import start_servo_board_right
from src.hand_control.Fingers import Hand
from src.hand_control.hand_move import hand_show


#recieve sensordata from pytuner, use the data to control the hand
def main():
#Inits:
    c=start_servo_board_right()
    udp_receiver=UDPReceiver(UDP_DATA_PORT)

    hand = Hand(c, udp_receiver)

    
    sensor_data = []
    

    

#Starting Position
    OpenHandFull(c, ControlSpeed)
    time.sleep(2)

#Calibrate the baseline: has to be set before starting!
    hand.set_baseline()
    

    while True:
        t0 = time.monotonic()

        while time.monotonic() - t0 <= CONTROL_TIME: #hand goes to hand_show after this time

            #Recieving the data for all fingers and save in Hand
            sensor_data=udp_receiver.wait_for_sensor_data()

            hand.set_sensor_data(sensor_data)

            #Control all fingers
            for finger in hand.fingers:
                finger.poscontroller.update(finger.calibrated_data)

                if finger.poscontroller.state != States.NO_OBJECT:
                #Control if there is an object:
                    finger.poscontroller.control_finger_pos(
                        finger,
                        finger.upper_th,
                        finger.calibrated_data
                    )
                    #Reset the timer
                    t0 = time.monotonic()
                else:
                    open_finger(c, finger.name, MaxSpeed)

        hand_show(c, MaxSpeed, loops=2)
        #shows hand movement without touching: no hand controlling during this (takes appr. t = loops * 2sec)
        









if __name__ == '__main__':
    main()



