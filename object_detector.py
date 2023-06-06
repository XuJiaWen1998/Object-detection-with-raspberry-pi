# Reference: https://github.com/opencv/opencv/wiki/TensorFlow-Object-Detection-API#use-existing-config-file-for-your-model
import cv2
import numpy as np

class object_detector():
    def __init__(self, threshold=0.45, nms_threshold=0.5):
        self.thres = threshold
        self.nms_threshold = nms_threshold
        self.classNames = []
        classFile = 'coco.names'
        with open(classFile, 'rt') as f:
            self.classNames = f.read().rstrip( '\n').split('\n')

        configPath = "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
        weightsPath = "frozen_inference_graph.pb"

        self.net = cv2.dnn_DetectionModel(weightsPath, configPath)
        self.net.setInputSize(320, 320)
        self.net.setInputScale(1.0/127.5)
        self.net.setInputMean((127.5, 127.5, 127.5))
        self.net.setInputSwapRB(True)

    def getObjects(self,img):
        classIds, confs, bbox = self.net.detect(img, confThreshold=self.thres)
        bbox = list(bbox)
        confs = list(np.array(confs).reshape(1,-1)[0])
        confs = list(map(float,confs))
        indices = cv2.dnn.NMSBoxes(bbox, confs, self.thres, nms_threshold=self.nms_threshold)
        for i in indices:
            box = bbox[i]
            x, y, w, h = box[0], box[1], box[2], box[3]
            cv2.rectangle(img, (x, y), (x+w, h+y), color=(0, 255, 0), thickness=2)
            cv2.putText(img,  self.classNames[classIds[i]-1].upper(), (box[0]+10,box[1]+30),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
        return img

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)
    od = object_detector()
    while True:
        success, img = cap.read()
        result = od.getObjects(img)
        cv2.imshow("Output", result)
        cv2.waitKey(1)