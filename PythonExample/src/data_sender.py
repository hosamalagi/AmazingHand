import socket
import json


class DataSender:
    def __init__(self, host="127.0.0.1", port=5010):
        self.host = host
        self.port = port
        self.sock = None

    def connect(self):
        """Connect to the live-plot TCP server."""

        self.sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        print(f"Connecting to live plot at {self.host}:{self.port}...")

        self.sock.connect(
            (self.host, self.port)
        )

        print("Connected to live plot.")

    def send(self, **data):
        """
        Send arbitrary data to the live plot.

        Example:
            sender.send(
                raw=10.5,
                filtered=9.8
            )
        """

        if self.sock is None:
            raise RuntimeError("DataSender is not connected.")

        # Convert data to JSON
        message = json.dumps(data)

        # \n marks the end of one message
        message += "\n"

        # Send
        self.sock.sendall(
            message.encode("utf-8")
        )

    def close(self):
        """Close TCP connection."""

        if self.sock is not None:
            self.sock.close()
            self.sock = None