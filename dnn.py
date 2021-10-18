from typing import KeysView
import cv2
import threading


class video(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        # Pretrained classes in the model
        self.classNames = {0: 'background',
                    1: 'person', 2: 'bicycle', 3: 'car', 4: 'motorcycle', 5: 'airplane', 6: 'bus',
                    7: 'train', 8: 'truck', 9: 'boat', 10: 'traffic light', 11: 'fire hydrant',
                    13: 'stop sign', 14: 'parking meter', 15: 'bench', 16: 'bird', 17: 'cat',
                    18: 'dog', 19: 'horse', 20: 'sheep', 21: 'cow', 22: 'elephant', 23: 'bear',
                    24: 'zebra', 25: 'giraffe', 27: 'backpack', 28: 'umbrella', 31: 'handbag',
                    32: 'tie', 33: 'suitcase', 34: 'frisbee', 35: 'skis', 36: 'snowboard',
                    37: 'sports ball', 38: 'kite', 39: 'baseball bat', 40: 'baseball glove',
                    41: 'skateboard', 42: 'surfboard', 43: 'tennis racket', 44: 'bottle',
                    46: 'wine glass', 47: 'cup', 48: 'fork', 49: 'knife', 50: 'spoon',
                    51: 'bowl', 52: 'banana', 53: 'apple', 54: 'sandwich', 55: 'orange',
                    56: 'broccoli', 57: 'carrot', 58: 'hot dog', 59: 'pizza', 60: 'donut',
                    61: 'cake', 62: 'chair', 63: 'couch', 64: 'potted plant', 65: 'bed',
                    67: 'dining table', 70: 'toilet', 72: 'tv', 73: 'laptop', 74: 'mouse',
                    75: 'remote', 76: 'keyboard', 77: 'cell phone', 78: 'microwave', 79: 'oven',
                    80: 'toaster', 81: 'sink', 82: 'refrigerator', 84: 'book', 85: 'clock',
                    86: 'vase', 87: 'scissors', 88: 'teddy bear', 89: 'hair drier', 90: 'toothbrush'}
        self.camera = cv2.VideoCapture(-1)
        self.camera.set(3,640)
        self.camera.set(4,480)

        w = round(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = round(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = self.camera.get(cv2.CAP_PROP_FPS)

        fourcc = cv2.VideoWriter_fourcc(*'DIVX')

        delay = round(1000/fps)

        record_video_file = 'record/'

        ret, self.image = self.camera.read()
        self.image_ok = 0
        self.record = 0


    def id_class_name(self, class_id, classes):
        for key, value in classes.items():
            if class_id == key:
                return value

    def run(self):
        task1 = threading.Thread(target=self.opencvdnn_thread)
        task1.start()
        self.main()
        cv2.detroyAllWindows()

    def opencvdnn_thread(self):
        model = cv2.dnn.readNetFromTensorflow('weight/frozen_inference_graph.pb','weight/ssd_mobilenet_v2_coco_2018_03_29.pbtxt')

        while True:
            if self.image_ok == 1:
                imagednn = self.image
                image_height, image_width, _ = imagednn.shape
                
                model.setInput(cv2.dnn.blobFromImage(imagednn, size=(300,300),swapRB=True))
                output = model.forward()

                for detection in output[0, 0, :, :]:
                    confidence = detection[2]
                    if confidence > 0.5:
                        class_id = detection[1]
                        class_name = id_class_name(class_id, classNames)
                        print(str(str(class_id) + ' ' + str(detection[2]) + class_name))
                        if class_name == 'person':
                            self.record = 1


    def main(self):
        try:
            while True:
                keValue = cv2.waitKey(1)
                if keValue == ord('q') or keValue == ord('Q'):
                    break

                image_ok = 0
                _, image = self.camera.read()
                self.image_ok = 1
                cv2.imshow('image',image)

        except KeyboardInterrupt:
            pass
if __name__ == "__main__":
    vi = video()
    vi.start()