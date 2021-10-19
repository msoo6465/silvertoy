import RPi.GPIO as GPIO
import threading

class button(threading.Thread):
    def __init__(self, sw1, sw2):
        threading.Thread.__init__(self)
        self.sw1 = sw1
        self.sw2 = sw2
        self.shutdown = 0

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.sw1, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.sw2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        self.press = 0

    def run(self):
        while True:
            if GPIO.input(self.sw1) == 1 or GPIO.input(self.sw2) == 1:
                self.press = 1
            if self.shutdown == 1:
                break

    def get_press(self):
        return self.press

    def reset(self):
        self.press = 0

    def close(self):
        self.shutdown = 1