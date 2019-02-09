/**
 * **********************************************************
 * File Name        : decoder.c
 * ***********************************************************
 */

/* Externs --------------------------------------------------*/
#include "decoder.h"
/**
 * Performs decoding using Consistent Overhead Byte Stuffing (COBS)
 */
void cobs_dec(char *src, char len, char *dst)
{
    char *end = src + len;
    while (src < end)
    {
        char i, c = *src++;
        for (i = 1; i < c; i++)
            *dst++ = *src++;
        if (c < 0xff)
            *dst++ = 0;
    }
}

int main(void)
{
    //test data in testInput
    char testInput[12] = {0x03, 0x20, 0x41, 0x04, 0x22, 0x15, 0x17, 0x04, 0x39, 0x21, 0x05, 0x00};
    char output[sizeof(testInput) - 2];
    cobs_dec(testInput, sizeof(testInput), output);
    for (int i = 0; i < sizeof(output); i++)
    {
        printf("%02x ", output[i]);
    }
}