import time
import serial

ser = serial.Serial('/dev/ttyS0', 38400, timeout=1)

ser.write(chr(128 + 16 + 8))

while True:
	cc = ser.read(1)
	if len(cc)>0:
		ch = ord(cc)
		print ch
	if ch ==194:
		ser.write(chr(32))
		if ch == 195:
			print "button 1 clicked"
			ser.write(chr(33))
			if ch == 196:
				ser.write(chr(64))
			if ch == 197:
				print "button 2 clicked"
				ser.write(chr(64+32+1 +4+1 + 1))

	    
           
