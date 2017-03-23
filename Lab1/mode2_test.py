import time
import serial

ser = serial.Serial('/dev/ttyS0', 38400, timeout=1)

ser.write(chr(128+32+16+8+4+1))

while True:
        cc = ser.read(1)
        if len(cc)>0:
                ch = ord(cc)
                print ch
