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

    def getObjects(self, img, draw=True, objects=[]):
        classIds, confs, bbox = self.net.detect(img, confThreshold=self.thres, nmsThreshold=self.nms_threshold)
        if len(objects) == 0:
            objects = self.classNames
        objectInfo = []
        if len(classIds) != 0:
            for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
                className = self.classNames[classId-1]
                if className in objects:
                    objectInfo.append([box, className])
                    if (draw):
                        cv2.rectangle(img,box,color=(0,255,0),thickness=2)
                        cv2.putText(img,className.upper(),(box[0]+10,box[1]+30),
                        cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                        cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
                        cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
        return img, objectInfo

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)
    od = object_detector()
    while True:
        success, img = cap.read()
        target_object = []
        result, objectInfo = od.getObjects(img, draw=True, objects=target_object)
        print(objectInfo)
        cv2.imshow("Output", result)
        cv2.waitKey(1)