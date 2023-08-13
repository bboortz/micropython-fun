#!/usr/bin/env python

#
# imports
#
import serial



#
# global variables
#
DEV = "/dev/ttyUSB0"
BAUD = 115200
CONTROL_C_CHAR = b'\x03' # ctrl-c
CONTROL_D_CHAR = b'\x04' # ctrl-d
NUMBER_WRITES = 5



#
# program
#
ser = serial.Serial(DEV, BAUD, timeout=2)
print(ser.portstr)
print(ser)

#send data via serial port
#serialcmd=('^C')
#ser.write(serialcmd.encode())

i = 0
while i < NUMBER_WRITES:
    ser.write(CONTROL_C_CHAR)
    i = i+1
ser.write(CONTROL_D_CHAR)
ser.close()

