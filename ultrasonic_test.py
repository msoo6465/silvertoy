import RPi.GPIO as GPIO
import time
 
trig = 16
echo = 20

 
print('start')
 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(trig,GPIO.OUT)
GPIO.setup(echo,GPIO.IN)

from move_util import motor_control

m_con = motor_control(18,22,27,23,25,24)
flag = 0
go_speed = 70
speed = 100
back_speed = 60
start_t = time.time()
def get_distance():
    GPIO.output(trig, True)
    time.sleep(0.00001)
    GPIO.output(trig, False)

    while GPIO.input(echo) == 0:
        pulse_start = time.time()
    
    while GPIO.input(echo) == 1:
        pulse_end = time.time()
    
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17000
    distance = round(distance, 2)
    return distance

try:
    GPIO.output(trig, False)
    while True:
        # print('roop')
        time.sleep(0.2)
        if flag == 0:
            # m_con.motor_go(go_speed)
            flag -= 1
        
        distance = get_distance()
        if time.time() - start_t > 1:
            print(distance)
            start_t = time.time()

        if distance <= 20:
            # m_con.motor_back(back_speed)
            time.sleep(2)
        
        elif 20 < distance <= 30:
            # m_con.motor_left(speed)
            time.sleep(0.5)

        # else:
        #     m_con.motor_go(go_speed)

except KeyboardInterrupt:
    pass
        
GPIO.cleanup()

