# src/data_ui/live_plot.py

import socket
import json
from collections import deque

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# ============================================================
# Configuration
# ============================================================

HOST = "127.0.0.1"
PORT = 5010

NUM_SENSORS = 4
MAX_SAMPLES = 100


# ============================================================
# TCP Server
# ============================================================

server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

server.setsockopt(
    socket.SOL_SOCKET,
    socket.SO_REUSEADDR,
    1
)

server.bind((HOST, PORT))
server.listen(1)

print(f"Waiting for controller on {HOST}:{PORT}...")

connection, address = server.accept()

print(f"Controller connected: {address}")

# Don't block matplotlib while waiting for data
connection.setblocking(False)


# ============================================================
# Data storage
# ============================================================

# One history/deque per sensor
raw_data = [
    deque(maxlen=MAX_SAMPLES)
    for _ in range(NUM_SENSORS)
]

filtered_data = [
    deque(maxlen=MAX_SAMPLES)
    for _ in range(NUM_SENSORS)
]

# TCP receive buffer
buffer = ""


# ============================================================
# Receive data
# ============================================================

def receive_data():
    global buffer

    # Read everything currently available from TCP
    try:
        while True:

            data = connection.recv(4096)

            if not data:
                break

            buffer += data.decode("utf-8")

    except BlockingIOError:
        pass

    # Process complete JSON messages
    while "\n" in buffer:

        message, buffer = buffer.split("\n", 1)

        if not message:
            continue

        try:
            values = json.loads(message)

            raw = values["raw"]
            filtered = values["filtered"]

            # Make sure we received four sensor values
            if len(raw) != NUM_SENSORS:
                print("Wrong number of raw sensor values:", raw)
                continue

            if len(filtered) != NUM_SENSORS:
                print("Wrong number of filtered sensor values:", filtered)
                continue

            # Store each sensor separately
            for i in range(NUM_SENSORS):

                raw_data[i].append(
                    raw[i]
                )

                filtered_data[i].append(
                    filtered[i]
                )

        except (json.JSONDecodeError, KeyError) as error:
            print("Invalid TCP message:", error)


# ============================================================
# Matplotlib
# ============================================================

fig, ax = plt.subplots()

raw_lines = []
filtered_lines = []


# Create raw + filtered line for every sensor
for i in range(NUM_SENSORS):

    raw_line, = ax.plot(
        [],
        [],
        linestyle="--",
        label=f"Sensor {i + 1} Raw"
    )

    filtered_line, = ax.plot(
        [],
        [],
        label=f"Sensor {i + 1} Filtered"
    )

    raw_lines.append(raw_line)
    filtered_lines.append(filtered_line)


ax.set_title("Live Sensor Data")
ax.set_xlabel("Sample")
ax.set_ylabel("Sensor Value")

ax.grid(True)
ax.legend()


# ============================================================
# Plot update
# ============================================================

def update(frame):

    # Get newest TCP data
    receive_data()

    # No data yet
    if len(raw_data[0]) == 0:
        return raw_lines + filtered_lines

    number_samples = len(raw_data[0])

    x = range(number_samples)

    # --------------------------------------------------------
    # Update lines
    # --------------------------------------------------------

    for i in range(NUM_SENSORS):

        raw_lines[i].set_data(
            x,
            list(raw_data[i])
        )

        filtered_lines[i].set_data(
            x,
            list(filtered_data[i])
        )

    # --------------------------------------------------------
    # X axis
    # --------------------------------------------------------

    ax.set_xlim(
        0,
        max(10, number_samples - 1)
    )

    # --------------------------------------------------------
    # Y axis
    # --------------------------------------------------------

    all_values = []

    for i in range(NUM_SENSORS):

        all_values.extend(
            list(raw_data[i])
        )

        all_values.extend(
            list(filtered_data[i])
        )

    if all_values:

        minimum = min(all_values)
        maximum = max(all_values)

        margin = max(
            (maximum - minimum) * 0.1,
            1
        )

        ax.set_ylim(
            minimum - margin,
            maximum + margin
        )

    return raw_lines + filtered_lines


# ============================================================
# Start live plot
# ============================================================

animation = FuncAnimation(
    fig,
    update,
    interval=50,
    cache_frame_data=False
)

plt.tight_layout()
plt.show()


# ============================================================
# Cleanup
# ============================================================

connection.close()
server.close()