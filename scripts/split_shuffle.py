import os
from random import shuffle
from shutil import copyfile

split_group = ['train', 'test', 'valid']
split_size = [0.7, 0.2, 0.1]
counter = 0

images = os.listdir('images')
labels = os.listdir('labels')
shuffle(images)

images_len = len(images)
labels_len = len(labels)

train_len = int(images_len * split_size[0])
test_len = int(images_len * split_size[1])
val_len = int(images_len * split_size[2])

train_len += images_len - test_len - val_len - train_len

print('train:', train_len)
print('test:', test_len)
print('val:', val_len)
print('src:', images_len)
print('sum:', train_len + test_len + val_len)

train = images[:train_len]
test = images[train_len:train_len+test_len]
valid = images[train_len+test_len:]
groups = [train, test, valid]

i = 0
for group in split_group:
    for image in groups[i]:
        copyfile(f'images/{image}', 
                 f'fishes/{group}/images/{image}')
        
        copyfile(f'labels/{image.replace(".jpg", ".txt")}', 
                 f'fishes/{group}/labels/{image.replace(".jpg", ".txt")}')

        counter += 1
        print('Progress:', counter, '/', images_len, end='\r')
    i += 1