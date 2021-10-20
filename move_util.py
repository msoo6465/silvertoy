import RPi.GPIO as GPIO

class motor_control():
    def __init__(self,pwma,ain1,ain2,pwmb,bin1,bin2) -> None:
        self.ain1 = ain1
        self.ain2 = ain2
        self.bin1 = bin1
        self.bin2 = bin2

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(pwma,GPIO.OUT)
        GPIO.setup(ain1,GPIO.OUT)
        GPIO.setup(ain2,GPIO.OUT)

        GPIO.setup(pwmb,GPIO.OUT)
        GPIO.setup(bin1,GPIO.OUT)
        GPIO.setup(bin2,GPIO.OUT)
        
        self.L_Motor = GPIO.PWM(pwma,500)
        self.L_Motor.start(0)

        self.R_Motor = GPIO.PWM(pwmb,500)
        self.R_Motor.start(0)

    def motor_back(self,speed):
        GPIO.output(self.ain1,0)
        GPIO.output(self.ain2,1)
        self.L_Motor.ChangeDutyCycle(speed)
        GPIO.output(self.bin1,0)
        GPIO.output(self.bin2,1)
        self.R_Motor.ChangeDutyCycle(speed)

    def motor_go(self,speed):
        GPIO.output(self.ain1,1)
        GPIO.output(self.ain2,0)
        self.L_Motor.ChangeDutyCycle(speed)
        GPIO.output(self.bin1,1)
        GPIO.output(self.bin2,0)
        self.R_Motor.ChangeDutyCycle(speed)

    def motor_left(self,speed):
        GPIO.output(self.ain1,0)
        GPIO.output(self.ain2,1)
        self.L_Motor.ChangeDutyCycle(speed)
        GPIO.output(self.bin1,1)
        GPIO.output(self.bin2,0)
        self.R_Motor.ChangeDutyCycle(speed)

    def motor_right(self,speed):
        GPIO.output(self.ain1,1)
        GPIO.output(self.ain2,0)
        self.L_Motor.ChangeDutyCycle(speed)
        GPIO.output(self.bin1,0)
        GPIO.output(self.bin2,1)
        self.R_Motor.ChangeDutyCycle(speed)

    def motor_stop(self):
        GPIO.output(self.ain1,0)
        GPIO.output(self.ain2,1)
        self.L_Motor.ChangeDutyCycle(0)
        GPIO.output(self.bin1,0)
        GPIO.output(self.bin2,1)
        self.R_Motor.ChangeDutyCycle(0)
