import COBS
import binascii
import serial

def printSignal(in_bytes):
    hex = binascii.hexlify(in_bytes)
    print(b" ".join(hex[i:i+2] for i in range(0, len(hex), 2)))


def testSignal(in_bytes):
    print("Input: ")
    printSignal(in_bytes)

    encoded = COBS.encode(in_bytes)
    print("Encoded: ")
    printSignal(encoded)

    decoded = COBS.decode(encoded)
    print("Decoded: ")
    printSignal(decoded)

# input1 = b'\x11\x22\x00\x33'
# input2 = b'\x45\x00\x00\x2c\x4c\x79\x00\x00\x40\x06\x4F\x37'

# testSignal(input1)
# testSignal(input2)


#"/dev/ttyACM0"
ser = serial.Serial("COM7", 9600)

# port output
print(ser.name)

while(True):
    # print(binascii.hexlify(ser.readline()))
    line = ser.read(11)
    print("Original: ")
    printSignal(line)
    decoded = COBS.decode(line)
    print("Decoded: ")
    printSignal(decoded)
