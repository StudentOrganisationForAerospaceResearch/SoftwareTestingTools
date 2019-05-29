# Connect usb to serial converter
# Run using python3 AvionicsMockData.py
# Enter serial port name

import binascii
import serial
import time

def launch(ser):
    ser.write(b'\x20\x00')
    time.sleep(1)
    print('Launch Command Sent\n')

def arm(ser):
    ser.write(b'\x21\x00')
    time.sleep(1)
    print('Arm Command Sent\n')

def heartbeat(ser):
    ser.write(b'\x46\x00')
    time.sleep(1)

def openINJ(ser):
    ser.write(b'\x2A\x00')
    time.sleep(1)
    print('INJ Opened\n')

def closeINJ(ser):
    ser.write(b'\x2B\x00')
    time.sleep(1)
    print('INJ Closed\n')

def abort(ser):
    ser.write(b'\x2F\x00')
    time.sleep(1)
    print('Abort Command Sent\n')

def reset(ser):
    ser.write(b'\x4F\x00')
    time.sleep(1)
    print('Reset Command Sent\n')

def receive(ser):
    print(binascii.hexlify(ser.read(256)))

def help():
    print('Commands:')
    print('launch')
    print('arm')
    print('openINJ')
    print('closeINJ')
    print('abort')
    print('reset')
    print('receive\n')

if __name__ == "__main__":
    port = input('Enter a Serial Port to connect to:') #Linux: /dev/ttyUSBx, Windows: COMx
    ser = serial.Serial(port, 9600, timeout=0)

    while(True):
        heartbeat(ser)

        comm = input("Enter command (enter help for list of commands):")
        if(comm == 'launch'): launch(ser)
        elif(comm == 'arm'): arm(ser)
        elif(comm == 'openINJ'): openINJ(ser)
        elif(comm == 'closeINJ'): closeINJ(ser)            
        elif(comm == 'abort'): abort(ser)
        elif(comm == 'reset'): reset(ser)
        elif(comm == 'help'): help()
        elif(comm == 'receive'): receive(ser)

        time.sleep(1.0)
