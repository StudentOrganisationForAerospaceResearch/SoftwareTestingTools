#define START (0xFFFF)
#define XOR_OUT (0xFFFF)
#include <stdio.h>
unsigned int frameData(unsigned char *dataToEncode, unsigned long length, unsigned char *frameData);
unsigned int stuffData(unsigned char *dataToEncode, unsigned long length, unsigned char *encodedData);

// FINISH_BLOCK used for stuffData
#define FINISH_BLOCK(X)           \
    {                             \
        *code_ptr = (X);          \
        code_ptr = encodedData++; \
        code = 0x01;              \
    }

unsigned int frameData(unsigned char *dataToEncode, unsigned long length, unsigned char *frameData)
{
    unsigned int lengthOfFramedData = stuffData(dataToEncode, length, frameData);
    frameData[lengthOfFramedData++] = 0x00;
    return lengthOfFramedData;
}

unsigned int stuffData(unsigned char *dataToEncode, unsigned long length, unsigned char *encodedData)
{
    unsigned int lengthOfEncodedData = length + 1;
    unsigned char *end = dataToEncode + length;
    unsigned char *code_ptr = encodedData++;
    unsigned char code = 0x01;

    while (dataToEncode < end)
    {
        if (*dataToEncode == 0)
        {
            FINISH_BLOCK(code);
        }
        else
        {
            *encodedData++ = *dataToEncode;
            code++;

            if (code == 0xFF)
            {
                FINISH_BLOCK(code);
            }
        }

        dataToEncode++;
    }

    FINISH_BLOCK(code);
    return lengthOfEncodedData;
}

int main(void)
{
    //test data in testInput
    unsigned char testInput[10] = {0x20, 0x41, 0x00, 0x22, 0x15, 0x17, 0x00, 0x39, 0x21, 0x05};
    unsigned char output[sizeof(testInput) + 2];
    frameData(testInput, sizeof(testInput), output);
    for (int i = 0; i < sizeof(output); i++)
    {
        printf("%02x ", output[i]);
    }
}