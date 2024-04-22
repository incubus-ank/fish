import cv2 
import os

for file in os.listdir("labels_old"):

    image = cv2.imread("images/" + file.split('.')[0] + ".jpg")
    labels = open("labels_old/" + file).readlines()
    writeFile = open('labels/' + file, 'a+')

    iw = image.shape[1]
    ih = image.shape[0]
    

    for label in labels:
        label = label.split(' ')

        w = int(label[3]) - int(label[1])
        h = int(label[4]) - int(label[2])

        cx, cy = int(label[1]) + w/2, int(label[2]) + h/2

        writeFile.write("0 " + str(cx/iw) + " " + str(cy/ih) + " " + str(w/iw) + " "+ str(h/ih) + "\n")

    frame = cv2.rectangle(image, (59, 73), (500, 228), (255, 255, 0),  3) 

    # cv2.imwrite("frame.jpg", frame)

    # cv2.imshow("frame.jpg", frame)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
