import os
import random
import cv2
import shutil
import sys

random.seed(42)

train_len = 0.7
test_len = 0.2
val_len = 0.1

print('get files')
images = os.listdir('summary/images')
labels = os.listdir('summary/labels')

images_len = len(images)
labels_len = len(labels)

print('images:', images_len)
print('labels:', labels_len)
print('images without lable:', images_len-labels_len)
print()

train_len = int(images_len * train_len)
test_len = int(images_len * test_len)
val_len = int(images_len * val_len)

train_len += images_len - test_len - val_len - train_len

print('calculate split and shiffle')
print('train:', train_len)
print('test:', test_len)
print('val:', val_len)
print('sum:', train_len + test_len + val_len)
print()

random.shuffle(images)

train = images[:train_len]
test = images[train_len:train_len+test_len]
val = images[train_len+test_len:]

print('split and check')
print('images:', images_len)
print('train:', len(train))
print('test:', len(test))
print('val:', len(val))
print('sum:', len(train + test + val))
print()

print('separete')
count = 0
count_not_labeled = 0

for file in train:
    name = ''.join(file.split('.')[:-1]).replace('#', '')
    new_name = name.replace('#', '')
    
    try:
        frame = cv2.imread('summary/images/' + file)
        frame = cv2.resize(frame, (640, 640), interpolation = cv2.INTER_AREA)
        cv2.imwrite('fishes/train/images/' + new_name + '.jpg', frame)  
    except:
        print('some error with:', file)
        sys.exit("Error message")

    label = name + '.txt'
    new_label = new_name + '.txt'

    if label in labels:
        pass
        shutil.copyfile('summary/labels/'+label, 'fishes/train/labels/'+new_label)
    else:
        open('fishes/train/labels/' + new_label, 'w')
        count_not_labeled += 1
    count += 1
    print('Progress:', count, '/', images_len, end='\r')
    

for file in test:
    name = ''.join(file.split('.')[:-1]).replace('#', '')
    new_name = name.replace('#', '')

    try:
        frame = cv2.imread('summary/images/' + file)
        frame = cv2.resize(frame, (640, 640), interpolation = cv2.INTER_AREA)
        cv2.imwrite('fishes/test/images/' + new_name + '.jpg', frame)
    except:
        print('some error with:', file)
        sys.exit("Error message")

    label = new_name + '.txt'

    if label in labels:
        pass
        shutil.copyfile('summary/labels/'+label, 'fishes/test/labels/'+new_label)
    else:
        open('fishes/test/labels/' + new_label, 'w')
        count_not_labeled += 1
    count += 1
    print('Progress:', count, '/', images_len, end='\r')
    

for file in val:
    name = ''.join(file.split('.')[:-1]).replace('#', '')
    new_name = name.replace('#', '')

    try:
        frame = cv2.imread('summary/images/' + file)
        frame = cv2.resize(frame, (640, 640), interpolation = cv2.INTER_AREA)
        cv2.imwrite('fishes/valid/images/' + new_name + '.jpg', frame)
    except:
        print('some error with:', file)
        sys.exit("Error message")

    label = new_name + '.txt'

    if label in labels:
        pass
        shutil.copyfile('summary/labels/'+label, 'fishes/valid/labels/'+new_label)
    else:
        open('fishes/valid/labels/' + new_label, 'w')
        count_not_labeled += 1
    count += 1
    print('Progress:', count, '/', images_len, end='\r')
