/**
************************************************************
* File Name     : decoder.h
************************************************************
*/

/* Includes ------------------------------------------------*/
#include <stdio.h>
/* Prototypes -----------------------------------------------*/

/**
 * Performs decoding using Consistent Overhead Byte Stuffing (COBS)
 * @param *src is the source pointer
 * @param len is the anticipated length of the destination array
 * @param *dst is the destination array
 */
void cobs_dec(unsigned char *src, unsigned char len, unsigned char *dst);