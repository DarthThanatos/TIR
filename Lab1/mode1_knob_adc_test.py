import lib.GPIO_Intel as GPIO
import time, sys, os

Gpio = GPIO.Intel()
Gpio.setup('IO2','in')
Gpio.setup('IO3','in')
Gpio.setup('IO4')
Gpio.setup('IO5')
Gpio.setup('A0')


Gpio.output('IO4', '1')
Gpio.output('IO5', '1')

try:
        while True:
                Gpio.output('IO4', Gpio.input('IO2'))
                Gpio.output('IO5', Gpio.input('IO3'))

                print Gpio.input('A0')

                time.sleep(1)


except KeyboardInterrupt:
        Gpio.cleanup()
