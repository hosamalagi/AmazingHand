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
│       └── params.py
|       └── ...
├── README.md
└── ...
```

## Notes

This project is a customized version of the original AmazingHand project and is intended specifically for sensor-based touch and proximity control. The fingers will move based on the Sensor data trying to reach a goal data. Using this with our capacitive-distance-sensors the hand will keep a constant distance to a object.

