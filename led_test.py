import RPi.GPIO as GPIO
import time


led1 = 20
led2 = 21
led3 = 26
led4 = 16

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(led1,GPIO.OUT)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(led2,GPIO.OUT)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(led3,GPIO.OUT)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(led4,GPIO.OUT)

try:
    while True:
        GPIO.output(led1,GPIO.HIGH)
        GPIO.output(led2,GPIO.HIGH)
        GPIO.output(led3,GPIO.HIGH)
        GPIO.output(led4,GPIO.HIGH)
        time.sleep(1)
        GPIO.output(led2,GPIO.LOW)
        GPIO.output(led1,GPIO.LOW)
        GPIO.output(led3,GPIO.LOW)
        GPIO.output(led4,GPIO.LOW)
        time.sleep(1)

except KeyboardInterrupt:
    pass

GPIO.cleanup()
