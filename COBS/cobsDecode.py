class DecodeError(Exception):
    pass

def decode(data):
    data = bytearray.fromhex(data)
    length = len(data) 
    index = 0
    if length <= 0:
        raise DecodeError("error with input")
    while index < length - 2:
        next = data[index]
        data[index] = 0
        index += next
    del data[0]
    del data[length - 2]

    return bytearray.hex(data)