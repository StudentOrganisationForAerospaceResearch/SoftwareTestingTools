import crccheck


crcmpeg = crccheck.crc.Crc32Mpeg2()


if __name__ == "__main__":
	data = bytearray.fromhex('0000102120423063408450a560c670e79129a14ab16bc18cd1ade1cef1ef123132732252')
	crchex = crcmpeg.calchex(data)
	print('0x'+crchex)