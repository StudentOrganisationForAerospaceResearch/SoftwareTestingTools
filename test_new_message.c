#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

#define IMU_SERIAL_MSG_SIZE (36+1)
#define START_FLAG (0xF0)
#define END_FLAG (0XF0)
#define F0_ESCAPE (0xF1F2)
#define F1_ESCAPE (0xF1F3)

static const int8_t IMU_HEADER_BYTE = 0x31;

uint8_t* Encode(uint8_t* message, int length);
void writeInt32ToArray(uint8_t* array, int startIndex, int32_t value);

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
	uint32_t crc = 0xABCD1234;

	uint8_t message[IMU_SERIAL_MSG_SIZE] = { 0 };
	int messageindex = 0;
	writeInt32ToArray(message, messageindex, IMU_HEADER_BYTE); messageindex++;
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
		if (n % 4 == 0)
			printf("\noriginal message at [%d to %d]:", n, n + 4);
		printf("%x", message[n]);
	}
	int encoded_message_length = IMU_SERIAL_MSG_SIZE;
	for (int i = 0; i < IMU_SERIAL_MSG_SIZE; i++)
	{
		if (message[i] == 0xF0 || message[i] == 0xF1)
		{
			encoded_message_length++;
		}
	}
	printf("\nExpected encoded message length = %d\n", encoded_message_length);
	uint8_t* encoded_message = Encode(message, encoded_message_length);

	for (int m = 1; m < encoded_message_length; m++)
		{
			if ((m-1) % 4 == 0)
				printf("\nencoded message at [%d to %d]:", m-1, m + 4 -1);
			printf("%x", encoded_message[m]);
		}

	
	uint8_t* buffer = malloc((encoded_message_length+2)* sizeof(uint8_t));
	buffer[0] = START_FLAG;
	for (int i = 0; i < encoded_message_length; i++)
	{
		buffer[1+i] = encoded_message[i];
	}
	buffer[encoded_message_length + 1] = END_FLAG;

	printf("\nfinal  buffer:\n");
	for (int o = 0; o < encoded_message_length+2; o++)
	{
		printf("%x", buffer[o]);
		if (o % 10 == 0)
			printf("\n");
	}
	

	return 0;
}

uint8_t* Encode(uint8_t* message, int length)
{
	uint8_t* buffer = malloc(sizeof(uint8_t) * length);
	int bufferindex = 0;
	for (int i = 0; i < length; i++)
	{
		//printf("Encoding %x ...\n", message[i]);
		if (message[i] == 0xF0)
		{
			buffer[bufferindex++] = 0xF0;
			buffer[bufferindex++] = 0xF1;
		}
		else if (message[i] == 0xF1)
		{
			buffer[bufferindex++] = 0xF1;
			buffer[bufferindex++] = 0xF2;
		}
		else
		{
			buffer[bufferindex++] = message[i];
		}
	}
	return buffer;
}

void writeInt32ToArray(uint8_t* array, int startIndex, int32_t value)
{
	//printf("Writing %d ...\n", value);

	//printf("Writing %d to index+0\n", (value >> 24) & 0xFF);
	array[startIndex + 0] = (value >> 24) & 0xFF;

	//printf("Writing %d to index+1\n", (value >> 16) & 0xFF);
	array[startIndex + 1] = (value >> 16) & 0xFF;

	//printf("Writing %d to index+2\n", (value >> 8) & 0xFF);
	array[startIndex + 2] = (value >> 8) & 0xFF;

	//printf("Writing %d to index+3\n", value & 0xFF);
	array[startIndex + 3] = (uint8_t)(value & 0xFF);
}