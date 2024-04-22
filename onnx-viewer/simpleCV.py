from ultralytics import YOLO
import onnxruntime as ort
import cv2 as cv
import numpy as np

onnx_model = ort.InferenceSession("yolov8n.onnx")
cap = cv.VideoCapture(0)


input_name = onnx_model.get_inputs()[0].name
output_name = onnx_model.get_outputs()[0].name
print("inputs:", input_name, len(onnx_model.get_inputs()))
print("outputs:", output_name, len(onnx_model.get_outputs()))

while True:
    ret, frame = cap.read()

    if ret:
        input = cv.resize(frame, (640, 640))
        input = np.reshape(input, (1, 3, 640, 640))

        results = onnx_model.run(
            [output_name], {input_name: input.astype(np.float32)})
        
        annotated_frame = frame
        cv.imshow("YOLOv8 Inference", annotated_frame)
        if cv.waitKey(1) == ord('q'):
            break
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()