from object_detector import *
import numpy as np
class movement_detector():
    def __init__(self, threshold=0.45, nms_threshold=0.5, objects=[]):
        self.camera = cv2.VideoCapture(0)
        self.camera.set(3,640)
        self.camera.set(4,480)
        self.od = object_detector(threshold=0.5, nms_threshold=0.2)
        self.result_table = {}
        self.prev_result_table = {}
        self.target_object = objects
    
    def check_appear(self):
        for item in self.result_table.keys():
            if item not in self.prev_result_table.keys():
                print("%s appear!" % item)

    def check_disappear(self):
        for item in self.prev_result_table.keys():
            if item not in self.result_table.keys():
                print("%s disappear!" % item)

    def check_movement(self, position_thres = 100):
        for item in self.prev_result_table.keys():
            if item in self.result_table.keys():
                prev_box_position = self.prev_result_table[item]
                curr_box_position = self.result_table[item]
                if np.sum(np.abs(np.subtract(prev_box_position, curr_box_position))) > position_thres:
                    print("%s is moving" % item)


    def store_result(self, objectInfo):
        self.prev_result_table = self.result_table.copy()
        self.result_table = {}
        for object in objectInfo:
            self.result_table[object[1]] = object[0]

    def run(self, show=True):
        success, img = self.camera.read()
        result, objectInfo = self.od.getObjects(img, draw=True, objects=self.target_object)
        self.store_result(objectInfo)
        self.check_appear()
        self.check_disappear()
        self.check_movement()
        if show:
            cv2.imshow("Output", result)
            cv2.waitKey(1)
        else:
            return img

if __name__ == "__main__":
    m = movement_detector(threshold=0.5, nms_threshold=0.2, objects=[])
    while(True):
        m.run()