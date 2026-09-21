import time
from src.hand_control.params import CALIBRATION_COUNT, SENSOR_COUNT, OFFSET


def calibrate_baseline(UDPReceiver):
        """This function collects a number of sensor readings from all sensors and averages them to create a calibration baseline."""
        calibration_data = [0] * SENSOR_COUNT

        for i in range(CALIBRATION_COUNT):
            sensor_data = UDPReceiver.wait_for_sensor_data()
            calibration_data = [a + b for a, b in zip(calibration_data, sensor_data)]
            time.sleep(0.01)  # wait 10 ms before the next reading

        calibration_data = [int(value) // CALIBRATION_COUNT for value in calibration_data]
        return [value - OFFSET for value in calibration_data]
        

      