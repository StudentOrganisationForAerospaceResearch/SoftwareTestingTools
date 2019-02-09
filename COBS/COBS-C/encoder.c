/**
 * **********************************************************
 * File Name        : decoder.c
 * ***********************************************************
 */
/* Externs --------------------------------------------------*/
#include "encoder.h"

/**
 * Performs encoding through consistent overhead byte stuffing (COBS)
 */
void cobs_cod(char *src, unsigned char len, char *dst)
{
    char *s = src, *end = src + len;
    do
    {
        while (*src != '0')
            src++;
        int len = (src - s);
        *dst++ = (len + 1) + '0';
        strcpy(dst, s);
        dst += len;
        s = ++src;
    } while (src <= end);
}

int main(void)
{
    char arr[] = "5988088910"; //must have a zero at the end to work
    char dest[sizeof(arr) - 1];
    cobs_cod(arr, sizeof(arr), dest);
    for (int i = 0; i < sizeof(dest); i++)
    {
        printf("%c", dest[i]);
    }
}