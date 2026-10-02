import time
from src.hand_control.hand_move import open_finger, OpenHandFull
from src.hand_control.params import UDP_DATA_PORT, ControlSpeed, MaxSpeed, CONTROL_TIME, ALPHA
from src.hand_control.receiver import UDPReceiver
from src.hand_control.prox_state_machine import States
from src.hand_control.ServoBoard import start_servo_board_right
from src.hand_control.Fingers import Hand
from src.hand_control.hand_move import hand_show
from src.hand_control.data_processing import ema_2
from src.data_sender import DataSender


#recieve sensordata from pytuner, use the data to control the hand
def main():
#Inits:
    c=start_servo_board_right()
    udp_receiver=UDPReceiver(UDP_DATA_PORT)

    hand = Hand(c, udp_receiver)

# #TCP to ui:
#     sender = DataSender(
#     host="127.0.0.1",
#     port=5010
# )

#     sender.connect()

    
    filtered_data = [0.0] * 4
    

    

#Starting Position
    OpenHandFull(c, ControlSpeed)
    time.sleep(2)

#Calibrate the baseline: has to be set before starting!
    hand.set_baseline()
    filtered_data = udp_receiver.wait_for_sensor_data()

    while True:
        t0 = time.monotonic()
        

        while time.monotonic() - t0 <= CONTROL_TIME: #hand goes to hand_show after this time

            #Recieving the data for all fingers and save in Hand
            data_1=udp_receiver.wait_for_sensor_data()

            for i in range(len(data_1)):
                filtered_data[i]=ema_2(filtered_data[i], data_1[i], ALPHA)

            hand.set_sensor_data(filtered_data)
            # sender.send(
            # raw=data_1,
            # filtered=filtered_data
            # )

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

        hand_show(c, MaxSpeed, loops=2)        # hand_show(c, MaxSpeed, loops=2)
        #shows hand movement without touching: no hand controlling during this (takes appr. t = loops * 2sec)
        









if __name__ == '__main__':
    main()



