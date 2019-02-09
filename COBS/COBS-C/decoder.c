/**
 * **********************************************************
 * File Name        : decoder.c
 * ***********************************************************
 */

/* Externs --------------------------------------------------*/
#include "decoder.h"
/**
 * Performs decoding using Consistent Overhead Byte Stuffing (COBS)
 * @param *src is the source pointer
 * @param len is the anticipated length of the destination array
 * @param *dst is the destination array
 */
void cobs_dec(unsigned char *src, unsigned char len, unsigned char *dst)
{
    unsigned char *end = src + len;
    while (src < end)
    {
        unsigned char i, c = *src++;
        for (i = 1; i < c; i++)
            *dst++ = *src++;
        if (c < 0xff)
            *dst++ = 0;
    }
}

int main(void)
{
    //test data in testInput
    unsigned char testInput[12] = {0x03, 0x20, 0x41, 0x04, 0x22, 0x15, 0x17, 0x04, 0x39, 0x21, 0x05, 0x00};
    unsigned char output[sizeof(testInput) - 2];
    cobs_dec(testInput, sizeof(testInput), output);
    for (int i = 0; i < sizeof(output); i++)
    {
        printf("%02x ", output[i]);
    }
}