# Connect usb to serial converter
# Run using python3 AvionicsMockData.py
# Enter serial port name

import binascii
import serial
import time

if __name__ == "__main__":
    port = input('Enter a Serial Port to connect to:') #Linux: /dev/ttyUSBx, Windows: COMx
    ser = serial.Serial(port, 9600, timeout=0)

    data = [	   
    b'\x31\x31\x31\x31\x00\x00\x00\x05\x00\x00\x01\x15\x00\x00\x03\xcf\xff\xff\xfa\x31\x00\x00\x26\x73\xff\xff\xfe\xd7\xff\xff\xff\xf9\xff\xff\xff\xf8\xff\xff\xff\xf7\x00',
    b'\x32\x32\x32\x32\x00\x01\x56\x4b\x00\x00\x09\x34\x00',
    b'\x33\x33\x33\x33\xff\xff\xff\xf3\xff\xff\xff\xf2\xff\xff\xff\xf1\xff\xff\xff\xf0\x00',
    b'\x34\x34\x34\x34\x00\x10\x57\x50\x00',
    b'\x35\x35\x35\x35\xff\xfe\x1a\x7a\x00',
    b'\x36\x36\x36\x36\x00\x00',
    b'\x37\x37\x37\x37\x00\x00',
    b'\x38\x38\x38\x38\x00\x00',
    b'\x39\x39\x39\x39\x00\x00'
    ]

    print("PARSED DATA")
    print("IMU – ACCEL:                     [5, 277, 975] mg")
    print("IMU – GYRO:                      [-1487, 9843, -297] mdps")
    print("IMU – MAG:                       [-7, -8, -9]")
    print("BAR – PRESS:                     87627 100*mbar")
    print("BAR – TEMP:                      2356 100*C")
    print("GPS – Altitude:                  -13")
    print("GPS – Time:                      -14")
    print("GPS – Latitude:                  -15")
    print("GPS – Longitude:                 -16")
    print("OXIDIZER TANK PRESSURE:          1070928 1000*psi")
    print("COMBUSTION CHAMBER PRESSURE:     -124294 1000*psi")
    print("FLIGHTPHASE:                     0 - PRELAUNCH")
    print("VENT_VALVE:                      0 - CLOSED")
    print("INJECTION_VALVE:                 0 - CLOSED")
    print("PROPULSION_VALVE_3:              0 - CLOSED\n")

    count = 0
    while(True):
    	if count>=9:
    		count = 0

    	ser.write(data[count])
    	time.sleep(1.0/10)
    	count+=1;



