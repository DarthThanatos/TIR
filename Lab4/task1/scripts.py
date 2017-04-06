import time
import serial

ser = serial.Serial('/dev/ttyS0', 38400, timeout=1)

ser.write(chr(128 + 16 + 8)) #subscribe 

while True:
	cc = ser.read(1)
	if len(cc)>0:
		ch = ord(cc)
		print ch
		if ch ==194: #128 + 64 + 2 -> button1 + 0 ->released
			ser.write(chr(32)) # 32 -> led1 + 0 -> turn off
		if ch == 195: # 128 + 64 + 2 -> button1 + 1 -> pressed
			print "button 1 clicked"
			ser.write(chr(33)) #32 -> led1 +1 -> turn on
		if ch == 196: #128 + 64 + 4 -> button2 + 0 -> released
			ser.write(chr(64)) # 64 -> led2 + 0 + 0 + 0 -> r =0, g =0, b =0 -> turn off
		if ch == 197: # 128 + 64 + 4 -> button2 + 1 -> pressed
			print "button 2 clicked"
			#ser.write(chr(64+32+1 +4+1 + 1)) #64 -> led2 +
			ser.write(chr(64+ 16 + 1 + 4 + 1 + 0 + 1)) #64 -> led2 + r = 1, g = 1, b = 1
	    
           
