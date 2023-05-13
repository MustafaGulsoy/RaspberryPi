import time
import numpy as np
import serial  # Module needed for serial communication

# Set USB Port for serial communication
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ser.flush()
send_binary = ''


def send_data_to_engines(powers):
    global send_binary
    if powers is None:
        return
    for data in powers:
        data = str("{:08b}".format(data, 'b'))

        if data[0] == '-':
            data = '1' + data[1:]
        else:
            pass
        send_binary += str(data)

        # Send the string. Make sure you encode it before you send it to the Arduino.
    ser.write(send_binary.encode('utf-8'))

    send_binary = ''
    # Do nothing for 500 milliseconds (0.5 seconds)
    time.sleep(0.5)

    # Receive data from the Arduino
    receive_string = ser.readline().decode('utf-8').rstrip()

    # Print the data received from Arduino to the terminal
    print("------------")
    print(powers)
    print(receive_string)
