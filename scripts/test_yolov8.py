import cv2 
import random
import os

# image = cv2.imread('./images/00b5b5ac-46f3-4fb1-9321-7f3ff13db1ad.jpg')
# labels = open("./labels/00b5b5ac-46f3-4fb1-9321-7f3ff13db1ad.txt").readlines()
cv2.namedWindow("Detected Objects", cv2.WINDOW_NORMAL)

labels_files = os.listdir("labels")
random.shuffle(labels_files)

for file in labels_files:
    image = cv2.imread('./images/' + file.split('.')[0] + ".jpg")

    image_w = image.shape[1]
    image_h = image.shape[0]
    labels = open("./labels/" + file).readlines()

    print(file)
    for label in labels:
        label = label.split(' ')

        w = float(label[3]) * image_w
        h = float(label[4]) * image_h

        min_x = int(float(label[1]) * image_w - w/2)
        min_y = int(float(label[2]) * image_h - h/2)
        max_x = int(float(label[1]) * image_w + w/2)
        max_y = int(float(label[2]) * image_h + h/2)

        frame = cv2.rectangle(image, (min_x, min_y), (max_x, max_y), (0, 0, 255),  2) 

    cv2.imshow("Detected Objects", frame)
    # time.sleep(1)
    
    if cv2.waitKey(200) == ord('q'):
        break
cv2.destroyAllWindows()