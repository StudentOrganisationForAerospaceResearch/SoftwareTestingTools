class DecodeError(Exception):
    pass


def _get_buffer_view(in_bytes):
    mv = memoryview(in_bytes)
    if mv.ndim > 1 or mv.itemsize > 1:
        raise BufferError('object must be a single-dimension buffer of bytes.')
    try:
        mv = mv.cast('c')
    except AttributeError:
        pass
    return mv


def encode(in_bytes):
    """Encode a string using Consistent Overhead Byte Stuffing (COBS).

    Input is any byte string or byte array. Output is a byte string.

    Encoding guarantees no zero bytes in the output, except for a delimiter
    byte at the end that signals the end of the packet. The output
    string will be expanded by 2 for the overhead (starting) byte and the
    delimiter byte at the end.

    An empty string is encoded to '\\x01'
    """

    # Type checking code (must be bytearray or byte string)
    if isinstance(in_bytes, bytes):
        in_bytes_mv = _get_buffer_view(in_bytes)
    elif not isinstance(in_bytes, bytearray):
        if isinstance(in_bytes, str):
            raise TypeError('Unicode-objects must be encoded as bytes first')
        else:
            raise TypeError(
                'Input error: Expected byte string or bytearray object')

    final_zero = True
    out_bytes = bytearray()
    idx = 0
    search_start_idx = 0
    for in_char in in_bytes_mv:
        if in_char == b'\x00':
            final_zero = True
            out_bytes.append(idx - search_start_idx + 1)
            out_bytes += in_bytes_mv[search_start_idx:idx]
            search_start_idx = idx + 1
        else:
            # Overflow check
            if idx - search_start_idx == 0xFD:
                final_zero = False
                out_bytes.append(0xFF)
                out_bytes += in_bytes_mv[search_start_idx:idx+1]
                search_start_idx = idx + 1
        idx += 1
    if idx != search_start_idx or final_zero:
        out_bytes.append(idx - search_start_idx + 1)
        out_bytes += in_bytes_mv[search_start_idx:idx]
    # add delimiter byte
    out_bytes.append(0)
    return bytes(out_bytes)


def decode(in_bytes):
    """Decode a string using Consistent Overhead Byte Stuffing (COBS).

    Input should be a byte string or a bytearray object that has been
    COBS encoded. Output is a byte string.

    This output performs error checking to ensure that the incoming
    byte string has no zeroes."""

    # Type checking code (must be bytearray or byte string)
    if isinstance(in_bytes, bytes):
        in_bytes_mv = _get_buffer_view(in_bytes)
    elif not isinstance(in_bytes, bytearray):
        if isinstance(in_bytes, str):
            raise TypeError('Unicode-objects must be encoded as bytes first')
        else:
            raise TypeError(
                'Input error: Expected byte string or bytearray object')

    out_bytes = bytearray()
    length = len(in_bytes_mv)
    index = 0
    if length <= 0:
        raise DecodeError("error with input: empty")
    # Check for zeroes in the input, except for the final delimiter byte.
    for loop_idx, in_char in enumerate(in_bytes[:-1]):
        if in_char == 0:
            raise DecodeError("error with input: zero byte found")

        # Handle COBS decode logic
        if(loop_idx == index):
            # Convert byte string to integer
            next = int.from_bytes(
                in_bytes_mv[index], byteorder='big', signed=False)
            if not index == 0:
                out_bytes.append(0)
            out_bytes += in_bytes_mv[index + 1:index + next]
            index += next

    # If the input is encoded correctly, the index should be on the last element of
    # the input (the delimiter). Otherwise, throw an error.
    if(index != length - 1):
        raise DecodeError(
            "error with input: not enough input bytes for length code")
    return out_bytes
