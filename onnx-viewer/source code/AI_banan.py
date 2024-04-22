#!/usr/bin/env python

import sys
import rospy
import cv2
from sensor_msgs.msg import CompressedImage
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge, CvBridgeError
from ultralytics import YOLO

class yolo_detector:
    def __init__(self):
        self.model = YOLO('best_openvino_model/')
        self.model = YOLO('yolov8n.pt')  # load an official detection model
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/usb_cam/image_raw/compressed", CompressedImage, self.callback)
        rospy.sleep(3)
        rospy.Timer(rospy.Duration(0.1), self.timer_callback)

    def callback(self,data):
        try:
            self.cv_image = self.bridge.compressed_imgmsg_to_cv2(data, "passthrough")
        except CvBridgeError as e:
            print(e)

    def timer_callback(self, _):
        self.processing(self.cv_image)

    def processing(self, img):
        results = self.model(img)
        annotated_frame = results[0].plot()
        cv2.imshow("YOLOv8 Inference", annotated_frame)
        cv2.waitKey(1)

def main(args):
    rospy.init_node('image_converter', anonymous=True)
    yolo = yolo_detector()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)