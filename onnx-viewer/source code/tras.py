# -*- coding: utf-8 -*-
#   Developed by Alexander Kraynikov krajnikov.a@edu.narfu.ru
import sys

from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, Qt, QThread

import numpy as np
import onnxruntime as ort
import cv2 as cv
import onnx



class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    last_letter = None
    count_last = 0
    output_text = ' '
    finded = False
    classes = list('ABCDEFGHIKLMNOPQRSTUVWXY')

    onnx_model = ort.InferenceSession("signlanguage_v1.onnx")

    def __init__(self):
        super().__init__()
        self.is_run = True

    def run(self):
        cap = cv.VideoCapture(0)
        while self.is_run:
            ret, frame = cap.read()
            if ret:
                
                input = frame[50:330, 50:330]
                cv.rectangle(frame, (50, 50), (330, 330), color=(30, 30, 30), thickness=2)
                input = cv.cvtColor(input, cv.COLOR_RGB2GRAY)
                input = cv.resize(input, (28, 28))
                input = np.reshape(input, (1, 1, 28, 28))

                input_name = self.onnx_model.get_inputs()[0].name
                output_name = self.onnx_model.get_outputs()[0].name
                results = self.onnx_model.run([output_name], {'input': input.astype(np.float32)})

                letter = str(self.classes[int(results[0].argmax(axis=1))])

                for i in range(len(list(results[0][0]))):
                    if list(results[0][0])[i] > 500:
                        # print(self.classes[i], ':', list(results[0][0])[i])
                        self.finded = True

                # print('---')

                if self.last_letter == letter and self.finded:
                    self.count_last += 1
                    if self.count_last > 60 and letter != self.output_text[-1]:
                        self.count_last = 0
                        self.output_text += letter
                else :
                    self.count_last = 0

                self.last_letter = letter

                if not self.finded:
                    letter = ' '
                self.text_print = letter + ' >>>' + self.output_text

                self.finded = False

                # frame = cv.copyMakeBorder(frame, 0,50, 0,0, cv.BORDER_CONSTANT, value=(200, 200, 200))
                # cv.putText(frame, text_print, (10, 515), cv.FONT_HERSHEY_SIMPLEX, 1.0, (30, 30, 30), thickness=2)
                cv.putText(frame, 'bring your brush here', (50, 40), cv.FONT_HERSHEY_SIMPLEX, 0.7, (30, 30, 30), thickness=2)

                self.change_pixmap_signal.emit(frame)
        cap.release()

    def get_text_print(self):
        return self.text_print
    
    def clear_text(self):
        self.output_text = ' '

    def get_output_text(self):
        return self.output_text

    def stop(self):
        self.is_run = False
        self.wait()


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ASL Translation")

        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()

        self.image_width = 640
        self.image_height = 480
        self.image_label = QLabel(self)
        self.image_label.resize(self.image_width, self.image_height)

        self.text_label = QLabel('Тут будет полученный текст')
        self.final_text_label = QLabel('---')
        self.final_text = ''

        self.button_add = QPushButton("Добавить")
        self.button_clear = QPushButton("Отчисить")
        self.button_reset = QPushButton("Cбросить")

        self.button_add.clicked.connect(self.add_word)
        self.button_clear.clicked.connect(self.thread.clear_text)
        self.button_reset.clicked.connect(self.reser_final_text)
    

        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()

        self.hbox.addWidget(self.button_add)
        self.hbox.addWidget(self.button_clear)
        self.hbox.addWidget(self.button_reset)

        self.vbox.addWidget(self.image_label)
        self.vbox.addWidget(self.text_label)
        self.vbox.addWidget(self.final_text_label)
        self.vbox.addLayout(self.hbox)
        
        self.setLayout(self.vbox)

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    def update_image(self, cv_img):
        qt_img = self.convert_cv_qt(cv_img)
        self.text_label.setText(self.thread.get_text_print())
        self.image_label.setPixmap(qt_img)
    
    def convert_cv_qt(self, cv_img):
        rgb_image = cv.cvtColor(cv_img, cv.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.image_width, self.image_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
    
    def add_word(self):
        self.final_text += self.thread.get_output_text() + ' '
        self.final_text_label.setText(self.final_text)
        self.thread.clear_text()

    def reser_final_text(self):
        self.thread.clear_text()
        self.final_text = '---'
        self.final_text_label.setText(self.final_text) 
    
if __name__=="__main__":
    app = QApplication(sys.argv)
    a = App()
    a.show()
    sys.exit(app.exec_())