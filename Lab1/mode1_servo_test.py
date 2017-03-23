import time
import serial

ser = serial.Serial('/dev/ttyS0', 38400, timeout=1)

ser.write(chr(0))
time.sleep(1)
ser.write(chr(15))
time.sleep(1)
ser.write(chr(31))
time.sleep(1)
ser.close()
