import binascii

def printSignal(in_bytes):
    """Print the signal to the console in a readable manner."""
    hex = binascii.hexlify(in_bytes)
    print(b" ".join(hex[i:i+2] for i in range(0, len(hex), 2)))

def addHeader(inputArr, headerByte):
    arr = bytearray()
    arr.extend(headerByte)
    arr.append(len(inputArr))
    arr.extend(inputArr)
    return bytes(arr)

arr = b'\x01\x02\x03'
headerByte = b'\x31'

arr = addHeader(arr, headerByte)

printSignal(arr)