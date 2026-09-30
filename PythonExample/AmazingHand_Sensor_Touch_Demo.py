import time
from rustypot import Scs0009PyController
from src.hand_control.hand_move import OpenHand,CloseHand, open_finger, close_finger, OpenHandFull
from src.hand_control.params import UDP_DATA_PORT, ControlSpeed, MaxSpeed
from src.hand_control.receiver import UDPReceiver
from src.hand_control.prox_state_machine import States
from src.hand_control.ServoBoard import start_servo_board
from src.hand_control.Fingers import Hand
from src.hand_control.hand_move import hand_show


#recieve sensordata from pytuner, use the data to control the hand
def main():
#Inits:
    c=start_servo_board()
    udp_receiver=UDPReceiver(UDP_DATA_PORT)

    hand = Hand(c, udp_receiver)

    
    sensor_data = []
    

    t0 = time.time()

#Starting Position
    OpenHandFull(c, ControlSpeed)
    time.sleep(2.5)

#Calibrate the baseline: has to be set before starting!
    hand.set_baseline()

    while True:
        t = time.time() - t0
        t_last_touch = t

        while t_last_touch < 30: #hand goes to hand_show after this time

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
                    t_last_touch = 0
                else:
                    open_finger(c, finger.name, MaxSpeed)

        hand_show(c, MaxSpeed, loops=2)
        #shows hand movement without touching: no hand controlling during this (takes appr. t = loops * 2sec)
        









if __name__ == '__main__':
    main()



