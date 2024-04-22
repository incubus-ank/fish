# -*- coding: utf-8 -*-
#   Developed by Alexander Kraynikov krajnikov.a@edu.narfu.ru
import os
import sys

from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, \
    QPushButton, QHBoxLayout, QComboBox, QLineEdit
from PyQt5.QtGui import QPixmap, QDoubleValidator
from PyQt5.QtCore import pyqtSignal, Qt, QThread

import numpy as np
import onnxruntime as ort
import cv2 as cv
import random
import time

from YOLOv8 import YOLOv8

from deep_sort.deep_sort.tracker import Tracker as DeepSortTracker
from deep_sort.tools import generate_detections as gdet
from deep_sort.deep_sort import nn_matching
from deep_sort.deep_sort.detection import Detection
import numpy as np


class Tracker:
    tracker = None
    encoder = None
    tracks = None

    def __init__(self, max_cosine_distance, max_iou_distance, max_age, n_init):
        nn_budget = None

        encoder_model_filename = 'deep_sort/resources/networks/mars-small128.pb' #'model_data/mars-small128.pb'
        

        metric = nn_matching.NearestNeighborDistanceMetric("cosine", max_cosine_distance, nn_budget)
        self.tracker = DeepSortTracker(metric, 
                                       max_iou_distance=max_iou_distance,
                                       max_age=max_age,
                                       n_init=n_init)
        self.encoder = gdet.create_box_encoder(encoder_model_filename, batch_size=1)

    def update(self, frame, detections):

        if len(detections) == 0:
            self.tracker.predict()
            self.tracker.update([])  
            self.update_tracks()
            return

        bboxes = np.asarray([d[:-1] for d in detections])
        bboxes[:, 2:] = bboxes[:, 2:] - bboxes[:, 0:2]
        scores = [d[-1] for d in detections]

        features = self.encoder(frame, bboxes)

        dets = []
        for bbox_id, bbox in enumerate(bboxes):
            dets.append(Detection(bbox, scores[bbox_id], features[bbox_id]))

        self.tracker.predict()
        self.tracker.update(dets)
        self.update_tracks()

    def update_tracks(self):
        tracks = []
        for track in self.tracker.tracks:
            if not track.is_confirmed() or track.time_since_update > 1:
                continue
            bbox = track.to_tlbr()

            id = track.track_id

            tracks.append(Track(id, bbox))

        self.tracks = tracks


class Track:
    track_id = None
    bbox = None

    def __init__(self, id, bbox):
        self.track_id = id
        self.bbox = bbox

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self, model_name, conf, iuo, path=0, record=False):
        self.model_name = model_name
        self.conf = conf
        self.iuo = iuo
        self.record = record
        self.path = path

        self.colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for j in range(20)]
        self.count = 0
        self.font = cv.FONT_HERSHEY_SIMPLEX 
        self.thickness = 2

        # параметры


        self.detection_threshold = 0.1 # Порог, выше которого объект считается подтвержденным.
        max_cosine_distance = 2 # Порог соответствия. Образцы с большим расстоянием считаются недействительным совпадением.
        max_iou_distance = 2 # 0.7 Порог ворот. Ассоциации со стоимостью, превышающей это значение, игнорируются.
        max_age = 30 # 30 Максимальное количество пропущенных промахов перед удалением трека
        n_init = 10 # 5 Количество последовательных обнаружений до подтверждения трека

        self.tracker = Tracker(max_cosine_distance, max_iou_distance, max_age, n_init)

        if self.record:
            fourcc = cv.VideoWriter_fourcc(*'XVID')
            self.out = cv.VideoWriter("./videos/" + \
                                    time.strftime("%Y-%m-%d_%H-%M-%S") + \
                                    ".mp4",  
                            fourcc,
                            10.0, (640, 480)) 

        super().__init__()
        self.is_run = True

    def run(self):
        # cap = cv.VideoCapture(int(self.path))
        cap = cv.VideoCapture('D:\\dis\\test-data\\test2-video.mp4')

        self.detector = YOLOv8("models/" + self.model_name,
                               self.conf,
                               self.iuo)
        map = dict()
        stop_list = []
        self.fishcounter = 0
        while self.is_run:
            ret, frame = cap.read()
            if ret:

                boxes, scores, class_ids = self.detector(frame)

                # print(boxes)

                # combined_img = self.detector.draw_detections(frame)
                
                detections = []
                frame_center = 1280/2
                for box, class_id, score in zip(boxes, class_ids, scores):
                    x1, y1, x2, y2 = box.astype(int)
                    class_id = int(class_id)
                    if score > self.conf:
                        detections.append([x1, y1, x2, y2, score])
                print(self.fishcounter)

                self.tracker.update(frame, detections)

                for track in self.tracker.tracks:
                    bbox = track.bbox
                    x1, y1, x2, y2 = bbox
                    track_id = track.track_id

                    if str(track_id) in map:
                        if float(map[str(track_id)]) > frame_center and int(x1) < frame_center and track_id not in stop_list:
                            self.fishcounter += 1
                            stop_list.append(track_id)
                    else:
                        map[str(track_id)] = str(x1)

                    # img_tmp = frame

                    # cv.rectangle(img_tmp, (int(x1), int(y1)), (int(x2), int(y2)), (self.colors[track_id % len(self.colors)]), -1)
                    # frame = cv.addWeighted(img_tmp, 0.3, frame, 1 - 0.3, 0)

                    frame = cv.putText(frame, str(track_id), (int(x1), int(y1) - 30), self.font,  
                        1, self.colors[track_id % len(self.colors)], self.thickness, cv.LINE_AA) 
                    cv.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (self.colors[track_id % len(self.colors)]), 2)
                    

                if self.record:
                    # print("record")
                    self.out.write(cv.resize(frame, (640, 480)))

                self.change_pixmap_signal.emit(frame)
        cap.release()

    def stop(self):
        self.is_run = False
        self.wait()



class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ONNX viewer")

        self.select_model = QComboBox()
        self.select_model.addItems(os.listdir("models"))
        self.select_model.currentIndexChanged.connect(self.changemodel)

        self.thread = VideoThread(os.listdir("models")[0],
                                  0.7,
                                  0.5)
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()

        self.image_width = 1280
        self.image_height = 720

        self.record = False

        self.image_label = QLabel(self)
        self.image_label.resize(self.image_width, self.image_height)

        self.button_record = QPushButton("Запись")
        self.button_record.clicked.connect(self.start_record)
        self.button_change = QPushButton("Перезапустить")
        self.button_change.clicked.connect(self.changemodel)

        self.label_confidence = QLabel()
        self.label_confidence.setText("confidence:")
        self.line_confidence = QLineEdit()
        self.line_confidence.setValidator(QDoubleValidator(0.01,1.00,2))
        self.line_confidence.setText("0.70")

        self.label_iuo = QLabel()
        self.label_iuo.setText("iuo:")
        self.label_path = QLabel()
        self.label_path.setText("path:")
        self.line_path = QLineEdit()
        self.line_path.setText('0')
        self.line_iuo = QLineEdit()
        self.line_iuo.setValidator(QDoubleValidator(0.01,1.00,2))
        self.line_iuo.setText("0.50")

        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()

        self.hbox.addWidget(self.image_label)
        self.vbox.addWidget(self.button_record)
        self.vbox.addWidget(self.select_model)

        self.vbox.addWidget(self.label_confidence)
        self.vbox.addWidget(self.line_confidence)
        self.vbox.addWidget(self.label_iuo)
        self.vbox.addWidget(self.line_iuo)
        self.vbox.addWidget(self.label_path)
        self.vbox.addWidget(self.line_path)
        self.vbox.addWidget(self.button_change)
        self.vbox.addStretch()

        self.hbox.addLayout(self.vbox)
        
        self.setLayout(self.hbox)

    def start_record(self):
        self.record = not self.record
        self.changemodel()

    def changemodel(self):
        self.line_iuo.text

        self.thread.stop()
        self.thread = VideoThread(self.select_model.currentText(),
                                  float(self.line_confidence.text()),
                                  float(self.line_iuo.text()),
                                  self.record,
                                  self.line_path.text())
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()


    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    def update_image(self, cv_img):
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)
    
    def convert_cv_qt(self, cv_img):
        rgb_image = cv.cvtColor(cv_img, cv.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, 
                                            w, 
                                            h, 
                                            bytes_per_line, 
                                            QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.image_width, 
                                        self.image_height, 
                                        Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
    
if __name__=="__main__":
    app = QApplication(sys.argv)
    a = App()
    a.show()
    sys.exit(app.exec_())