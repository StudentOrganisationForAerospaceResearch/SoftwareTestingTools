import COBS
import binascii
import serial
import time


def printSignal(in_bytes):
    """Print the signal to the console in a readable manner."""
    hex = binascii.hexlify(in_bytes)
    print(b" ".join(hex[i:i+2] for i in range(0, len(hex), 2)))


def testSignal(in_bytes):
    """Print original signal, encode, print again, decode, print."""
    print("Input: ")
    printSignal(in_bytes)

    encoded = COBS.encode(in_bytes)
    print("Encoded: ")
    printSignal(encoded)

    decoded = COBS.decode(encoded)
    print("Decoded: ")
    printSignal(decoded)

# Test code from hard-coded inputs


input1 = b'\x11\x22\x00\x33'
input2 = b'\x45\x00\x00\x2c\x4c\x79\x00\x00\x40\x06\x4F\x37'
input3 = b'\x11\x22\x00\x33\x11\x55\x00\x46\x00'
inputSend = b'\x45\x00\x00\x2c\x4c\x79\x00\x00\x40\x06\x37'

inputEncoded = b'\x03\x20\x41\x04\x22\x15\x17\x04\x39\x21\x05\x00'
inputEncoded2 = b'\x03\x07\x06\x04\x08\x09\x05\x04\x01\x02\x05\x00'

testSignal(input1)
testSignal(input2)
testSignal(input3)

# Test code to receive and decode encoded inputs

"/dev/ttyACM0"
ser = serial.Serial("COM7", 9600)

# port output
# print(ser.name)

# while(True):
#     # This should theoretically be a readline() method. However,
#     # the signal that is read is not terminated by a '\n' character.
#     # This should be modified in future code.
#     line = ser.read(11)

#     # Test
#     print("Original: ")
#     printSignal(line)
#     decoded = COBS.decode(line)
#     print("Decoded: ")
#     printSignal(decoded)

# Test code to encode and send serial outputs
while(True):
    printSignal(inputEncoded)
    ser.write(inputEncoded)  # size: 13
    time.sleep(1.0 / 100)
