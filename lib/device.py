from machine import unique_id
from ubinascii import hexlify
import ubinascii, uhashlib

def hexbytes(bytesarr):
    return int(hexlify(bytesarr), 16)

def quersum(number):
    result = 0
    for n in str(number):
        result += int(n)
    return result


MACHINE_ID = unique_id()
MACHINE_ID_HEX = hexbytes( MACHINE_ID )
MACHINE_ID_QSUM = quersum( MACHINE_ID_HEX )

