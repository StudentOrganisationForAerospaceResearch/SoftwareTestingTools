#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

#define IMU_SERIAL_MSG_SIZE (36+1)
#define START_FLAG (0xF0)
#define END_FLAG (0XF0)
#define F0_ESCAPE (0xF0)
#define F0_CHAR1 (0xF0)
#define F0_CHAR2 (0xF1)
#define F1_CHAR1 (0xF1)
#define F1_CHAR2 (0xF2)
#define F1_ESCAPE (0xF1)
#define FLAGS_AND_CRC_SIZE (6)
static const int8_t IMU_HEADER_BYTE = 0x31;

void Encode(uint8_t* message, int message_length, uint8_t* buffer);
void writeInt32ToArray(uint8_t* array, int startIndex, int32_t value);

uint32_t crc = 0xABCD1234;
int main()
{
	//use dummy data to test if encoding and construction of final send buffer are correct.
	int32_t accelX = 0x1234F0F1;
	int32_t accelY = 0xF1F2F3F1;
	int32_t accelZ = 0x98765432;
	int32_t gyroX = 0xF0F0F0F0;
	int32_t gyroY = 0xF1F1F1F1;
	int32_t gyroZ = 0xF3F2F1F0;
	int32_t magnetoX = 0xABCDEF71;
	int32_t magnetoY = 8;
	int32_t magnetoZ = 0xF0;

	uint8_t message[IMU_SERIAL_MSG_SIZE] = { 0 };
	int messageindex = 0;
	message[0] = IMU_HEADER_BYTE; messageindex++;
	writeInt32ToArray(message, messageindex, accelX); 		messageindex += 4;
	writeInt32ToArray(message, messageindex, accelY); 		messageindex += 4;
	writeInt32ToArray(message, messageindex, accelZ); 		messageindex += 4;
	writeInt32ToArray(message, messageindex, gyroX); 		messageindex += 4;
	writeInt32ToArray(message, messageindex, gyroY); 		messageindex += 4;
	writeInt32ToArray(message, messageindex, gyroZ); 		messageindex += 4;
	writeInt32ToArray(message, messageindex, magnetoX); 	messageindex += 4;
	writeInt32ToArray(message, messageindex, magnetoY); 	messageindex += 4;
	writeInt32ToArray(message, messageindex, magnetoZ); 	messageindex += 4;

	for (int n = 0; n < IMU_SERIAL_MSG_SIZE; n++)
	{
		printf("%x ", message[n]);
	}
	int encoded_message_length = IMU_SERIAL_MSG_SIZE;
	for (int i = 0; i < IMU_SERIAL_MSG_SIZE; i++)
	{
		if (message[i] == F0_CHAR1 || message[i] == F1_ESCAPE)
		{
			encoded_message_length++;
		}
	}
	int buffer_length = encoded_message_length + FLAGS_AND_CRC_SIZE;
	printf("\nExpected encoded message length = %d\n", encoded_message_length);
	uint8_t* buffer = malloc(buffer_length * sizeof(uint8_t));

	//@@@@@@@@@@@@@@@@@@@@@@@@@@@@
	Encode(message, IMU_SERIAL_MSG_SIZE, buffer);

	
	printf("\nfinal  buffer:\n");
	for (int o = 0; o < buffer_length; o++)
	{
		printf("%x", buffer[o]);
		if (o % 10 == 0)
			printf("\n");
	}
	
	free(buffer);
	return 0;
}

void Encode(uint8_t* message, int message_length, uint8_t* buffer)
{
	//printf("\nlength = %d\n", message_length);
	int bufferindex = 1;
	buffer[0] = START_FLAG;
	for (int i = 0; i < message_length; i++)
	{

		//printf("Encoding %x ... using bufferIndex %d, i = %d\n", message[i], bufferindex, i);
		if (message[i] == F0_ESCAPE)
		{
			buffer[bufferindex++] = F0_CHAR1;
			buffer[bufferindex++] = F0_CHAR2;
		}
		else if (message[i] == F1_ESCAPE)
		{
			buffer[bufferindex++] = F1_CHAR1;
			buffer[bufferindex++] = F1_CHAR2;
		}
		else
		{
			buffer[bufferindex++] = message[i];
		}
	}
	writeInt32ToArray(buffer, bufferindex, crc); bufferindex += 4;
	buffer[bufferindex] = END_FLAG;
	printf("\nfinal buffer index = %d\n", bufferindex);
}

void writeInt32ToArray(uint8_t* array, int startIndex, int32_t value)
{
	//printf("Writing %x ...\n", value);

	//printf("Writing %x to index+0\n", (value >> 24) & 0xFF);
	array[startIndex + 0] = (value >> 24) & 0xFF;

	//printf("Writing %x to index+1\n", (value >> 16) & 0xFF);
	array[startIndex + 1] = (value >> 16) & 0xFF;

	//printf("Writing %x to index+2\n", (value >> 8) & 0xFF);
	array[startIndex + 2] = (value >> 8) & 0xFF;

	//printf("Writing %x to index+3\n", value & 0xFF);
	array[startIndex + 3] = (uint8_t)(value & 0xFF);
}