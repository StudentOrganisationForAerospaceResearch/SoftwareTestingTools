def encode(input_bytes):
    input_bytes_eff = memoryview(input_bytes)
    finalDel = True
    output_bytes = bytearray()
    index = 1
    for byte in input_bytes_eff:
        if byte == 0:
            output_bytes.append(index)
            output_bytes += input_bytes_eff[0:index-1]
            break
        index += 1
    for i in range(index)  
    for search_index in range(index, len(input_bytes_eff)):
        if input_bytes_eff[search_index] == 0:
            output_bytes.append(search_index + 1)
            finalDel == True
        search_index += 1

    return bytes(output_bytes)

encoded = encode(b'\x45\x00\x00\x2C\x4C\x79\x00\x00\x40\x06\x4F\x37')
print(encoded)