import RPi.GPIO as GPIO
import threading
from move_util import motor_control as mc
import time
import cv2

class move_function(threading.Thread):
    def __init__(self, is_follow):
        threading.Thread.__init__(self)
        self.is_follow = is_follow
        self.m_con = mc(18,22,27,23,25,24)
        self.go_speed = 70
        self.speed = 100
        self.back_speed = 60

        self.trig = 20
        self.echo = 21

        self.end_move = 0

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)

    def move_solo(self):
        try:
            solo_start_time = time.time()
            GPIO.output(self.trig, False)
            while True:
                if time.time() - solo_start_time > 300:
                    self.end_move = 1
                    break
                time.sleep(0.2)
                self.m_con.motor_go(self.go_speed)


                GPIO.output(self.trig, True)
                time.sleep(0.00001)
                GPIO.output(self.trig, False)

                while GPIO.input(self.echo) == 0:
                    pulse_start = time.time()

                while GPIO.input(self.echo) == 1:
                    pulse_end = time.time()

                pulse_duration = pulse_end - pulse_start
                distance = pulse_duration * 17000
                distance = round(distance, 2)
                if time.time() - start_t > 1:
                    start_t = time.time()

                if distance <= 20:
                    self.m_con.motor_back(self.back_speed)
                    time.sleep(2)

                elif 20 < distance <= 30:
                    self.m_con.motor_left(self.speed)
                    time.sleep(0.1)

                else:
                    self.m_con.motor_go(self.go_speed)

        except KeyboardInterrupt:
            pass

        finally:
            GPIO.cleanup()

    def move_follow(self):
        try:
            camera = cv2.VideoCapture(0)
            camera.set(3, 640)
            camera.set(4, 480)
            model = cv2.dnn.readNetFromTensorflow('weight/frozen_inference_graph.pb',
                                                  'weight/ssd_mobilenet_v2_coco_2018_03_29.pbtxt')
            m_s_time = time.time()
            while True:
                _, image = camera.read()
                keValue = cv2.waitKey(1)
                if time.time() - m_s_time > 300:
                    self.end_move = 1
                    break
                if keValue == ord('q') or keValue == ord('Q'):
                    break
                if not _:
                    break
                imagednn = image
                image_height, image_width, _ = imagednn.shape
                model.setInput(cv2.dnn.blobFromImage(imagednn, size=(300, 300), swapRB=True))
                output = model.forward()
                self.m_con.motor_go(self.go_speed)
                time.sleep(0.2)
                for detection in output[0, 0, :, :]:
                    confidence = detection[2]
                    if confidence > 0.5:
                        class_id = detection[1]
                        if class_id == 1:
                            box_x = detection[3] * image_width
                            box_y = detection[4] * image_width
                            box_w = detection[5] * image_width
                            box_h = detection[6] * image_width
                            print(box_x + (box_w/2), image_width)
                            if (box_x + box_w)/2 > (image_width/2) * 1.1:
                                print('right')
                                self.m_con.motor_left(self.speed)
                            elif (box_x + box_w)/2 < (image_width/2) * 0.9:
                                print('left')
                                self.m_con.motor_right(self.speed)
                            else:
                                print('go')
                                self.m_con.motor_go(self.go_speed)
                            # cv2.rectangle(imagednn,(int(box_x),int(box_y)),(int(box_w),int(box_h)),(0,0,255),thickness=1)
                            # cv2.imshow('person',imagednn)
                            time.sleep(0.2)
        except Exception as e:
            print(e)

        finally:
            GPIO.cleanup()

    def get_is_end(self):
        return self.end_move

    def run(self):
        if self.is_follow == 0:
            self.move_solo()
        else:
            self.move_follow()