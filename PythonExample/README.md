# Hardware
## Servo power supply 

The servo driver board requires a **5 V / 2 A power supply**.

Connect the power supply to the servo driver board as follows:

```text
       -       +
       |       |
       |       |
   +---|-------|---+
   |               |
   |  Servo Driver |
   |     Board     |
   |   (top view)  |
   |               |
   |               |
   |               |
   +-------|-------+
           |
          USBC

```
Using the AH power supply cable:
* red -> +
* black -> -

# Sensor Touch Demo

A customized sensor-touch demonstration based on the [AmazingHand](https://github.com/telegrapher/AmazingHand) project.

The demo receives sensor data via UDP and uses the data to control the AmazingHand system.

## Requirements

* Python 3
* [`uv`](https://docs.astral.sh/uv/)
* AmazingHand hardware and software setup
* A UDP source providing the required sensor data

## Usage

Before starting the demo, make sure that a UDP data transmission is running on the configured port.

Then start the demo with:

```bash
uv run AmazingHand_Sensor_Touch_Demo.py
```

The demo will listen for incoming sensor data and use it for the sensor-touch control logic.

## Configuration

The UDP port can be configured in:

```text
src/hand_control/params.py
```

Adjust the port configuration to match the port used by the UDP data source.

## Data Flow

The basic data flow is:

```text
Sensor Data Source
        │
        │ UDP
        ▼
Sensor Touch Demo
        │
        ▼
AmazingHand Control
        │
        ▼
Servo Motors
```

## Project Structure

```text
.
├── AmazingHand_Sensor_Touch_Demo.py
├── src/
│   └── hand_control/
|       └── ...
├── set_pose.py
├── README.md
└── ...
```

## Set_pose
Sets the left (possibly right) hand to a set position.

## Sensor_touch_demo

This project is a customized version of the original AmazingHand project and is intended specifically for sensor-based touch and proximity control. The fingers will move based on the Sensor data trying to reach a goal data. Using this with our capacitive-distance-sensors the hand will keep a constant distance to a object.

## Calibration
After building the AH, each finger had to be calibrated. For this the motor-IDs of bouth hands were configured as described in the AH repo.
### RIGHT HAND
* ID1: MiddlePos_1 = 8
* ID2: MiddlePos_2 = -10
* ID3: MiddlePos_1 = 10
* ID4: MiddlePos_2 = 0
* ID5: MiddlePos_1 = 4
* ID6: MiddlePos_2 = -5
* ID7: MiddlePos_1 = 6
* ID8: MiddlePos_2 = -8

```bash
MiddlePos = [8, -10, 10, 0, 4, -5, 6, -8]
```


### LEFT HAND

* ID11: MiddlePos_1 = -7
* ID12: MiddlePos_2 = -5
* ID13: MiddlePos_1 = -5
* ID14: MiddlePos_2 = 8
* ID15: MiddlePos_1 = 8
* ID16: MiddlePos_2 = 0
* ID17: MiddlePos_1 = 0
* ID18: MiddlePos_2 = -6

```bash
MiddlePos = [-7, -5, -5, 8, 8, 0, 0, -6]
```

