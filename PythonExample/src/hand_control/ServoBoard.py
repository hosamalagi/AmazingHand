from rustypot import Scs0009PyController



def start_servo_board():
    return Scs0009PyController(
        serial_port="/dev/serial/by-id/usb-1a86_USB_Single_Serial_5B42139153-if00",
        baudrate=1_000_000,
        timeout=0.5,
    )