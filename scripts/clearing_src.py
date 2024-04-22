import os
import cv2

images = os.listdir('images')
count_name_with_sharp = 0
count_images_complited = 0 

print(len(images))

for image in images:
    # if '#' in image:
    #     new_image = image.replace('#', '')
    #     os.rename('labels/' + image, 'labels/' + new_image)
    #     count_name_with_sharp += 1
    frame = cv2.imread('images/' + image)
    frame = cv2.resize(frame, (320, 320), interpolation = cv2.INTER_AREA)
    cv2.imwrite('images/' + image, frame)
    count_images_complited += 1
    print('Progress:', count_images_complited, '/', len(images), end='\r')


print(count_images_complited)  
# print(count_name_with_sharp)