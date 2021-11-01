import RPi.GPIO as GPIO
import threading
from move_util import motor_control as mc
from tts import Speaker
import time
import cv2


class self_drive():
    def __init__(self,is_follow):
        self.is_follow = is_follow
        self.m_con = mc(18, 22, 27, 23, 25, 24)
        self.go_speed = 70
        self.speed = 40
        self.back_speed = 60

        self.move_time = 180

        self.trig = 16
        self.echo = 20

        self.end_move = 0

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)

        if is_follow == 1:
            self.camera = cv2.VideoCapture(0)
            self.camera.set(3, 640)
            self.camera.set(4, 480)
            self.model = cv2.dnn.readNetFromTensorflow('weight/frozen_inference_graph.pb',
                                                  'weight/ssd_mobilenet_v2_coco_2018_03_29.pbtxt')
    def main(self):
        self.start_time = time.time()
        if self.is_follow == 0:
            self.solo()
        else:
            self.follow()

    def solo(self):
        start_t = time.time()
        try:
            solo_start_time = time.time()
            GPIO.output(self.trig, False)
            while True:
                if self.end_move == 1:
                    break

                if time.time() - solo_start_time > 30:
                    self.end_move = 1
                    break
                time.sleep(0.2)

                distance = self.get_distance()

                if time.time() - start_t > 1:
                    start_t = time.time()

                if distance <= 20:
                    self.m_con.motor_back(self.back_speed)
                    time.sleep(2)

                elif 20 < distance <= 30:
                    self.m_con.motor_left(80)
                    time.sleep(0.1)

                else:
                    self.m_con.motor_go(self.go_speed)

        except KeyboardInterrupt:
            self.end_move = 1
            pass

        finally:
            GPIO.cleanup()

    def get_distance(self):
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
        return distance

    def follow(self):
        while True:
            st = time.time()
            ret, image = self.camera.read()
            keValue = cv2.waitKey(1)
            if not ret:
                break

            if time.time() - self.start_time > 30:
                break

            if keValue == ord('q') or keValue == ord('Q'):
                break
            imagednn = image
            image_height, image_width, _ = imagednn.shape
            self.model.setInput(cv2.dnn.blobFromImage(imagednn, size=(300, 300), swapRB=True))
            output = self.model.forward()
            self.m_con.motor_go(self.go_speed)

            for detection in output[0, 0, :, :]:
                confidence = detection[2]
                if confidence > 0.5:
                    class_id = detection[1]
                    if class_id == 1:
                        box_x = detection[3] * image_width
                        box_w = detection[5] * image_width
                        distance = self.get_distance()
                        if distance < 100:
                            print('stop')
                            self.m_con.motor_stop()
                        # img = cv2.rectangle(image, (int(box_x), int(box_y)), (int(box_w), int(box_h)), (0, 0, 255), 2)
                        if (box_x + box_w) / 2 > (image_width / 2) * 1.2:
                            print('GO')
                            # cv2.putText(img,'RIGHT',(int(box_x), int(box_y)),cv2.FONT_HERSHEY_PLAIN,2,(0,0,255),2)
                            self.m_con.motor_left(self.speed)
                        elif (box_x + box_w) / 2 < (image_width / 2) * 0.8:
                            print('RIGHT')
                            # cv2.putText(img,'LEFT',(int(box_x), int(box_y)),cv2.FONT_HERSHEY_PLAIN,2,(0,0,255),2)
                            self.m_con.motor_right(self.speed)
                        else:
                            print('LEFT')
                            # cv2.putText(img,'GO',(int(box_x), int(box_y)),cv2.FONT_HERSHEY_PLAIN,2,(0,0,255),2)
                            self.m_con.motor_go(self.go_speed)
                        time.sleep(0.5)
                        break
                        # time.sleep(0.2)
            # cv2.imshow('123',img)
            print(time.time() - st,'sec')


if __name__ == '__main__':
    speaker = Speaker()
    while True:
        speech = speaker.get_text()
        if not speech:
            continue
        speech = speech.replace(' ','')
        print(speech)
        
        if '빵빵' in speech:
            speaker.speak('네')
            break

    while True:
        speech = speaker.get_text()
        if not speech:
            continue
        speech = speech.replace(' ','')
        print(speech)
        if '혼자' in speech:
            is_follow = 0
            speaker.speak('네. 전원을 뽑고 바닥에 두고 버튼을 눌러주세요. 2분간 움직일 수 있어요. 2분 동안 명령을 들을 수 없어요.')
            time.sleep(5)
            speaker.speak('네 지금부터 혼자 움직일께요.')
            break
        elif '따라와' in speech:
            is_follow = 1
            speaker.speak('네. 전원을 뽑고 바닥에 두고 버튼을 눌러주세요. 2분간 움직일 수 있어요. 2분 동안 명령을 들을 수 없어요.')
            time.sleep(5)
            speaker.speak('네 지금부터 따라 다닐께요.')
            break

    s = self_drive(is_follow)
    s.main()
    speaker.speak('끝났어요. 충전해 주세요.')