import cv2
import os
import random
from shutil import copyfile

images_dir = 'old_images'
labels_dir = 'old_labels'
output_images_dir = 'images'
output_labels_dir = 'labels'

image_files = os.listdir(images_dir)
label_files = os.listdir(labels_dir)

num = [1, 4, 9]

total_images = len(image_files)
processed = 0
print('total images: ', total_images)

def label_scale(label, w, h, aw=0, ah=0):
    text = ''
    lbl_text =  open(os.path.join(labels_dir, label), 'r+').readlines()
    
    for line in lbl_text:         
        line = line.split(' ')
        
        out_text = ['0', 
                    str(float(line[1]) * w + aw),
                    str(float(line[2]) * h + ah),
                    str(float(line[3]) * w),
                    str(float(line[4]) * h)]
        text += ' '.join(out_text) + '\n'
        
    return text

def mosaic4(images, labels):
    salt = random.randint(3, 7) * 320
    w = [320 - int(salt/10), int(salt/10)]
    salt = random.randint(3, 7) * 320
    h = [320 - int(salt/10), int(salt/10)]

    img1 = cv2.resize(images[0], (w[0], h[0]), interpolation = cv2.INTER_AREA)
    img2 = cv2.resize(images[1], (w[1], h[0]), interpolation = cv2.INTER_AREA)
    img3 = cv2.resize(images[2], (w[0], h[1]), interpolation = cv2.INTER_AREA)
    img4 = cv2.resize(images[3], (w[1], h[1]), interpolation = cv2.INTER_AREA)

    label  = label_scale(labels[0], w[0]/320, h[0]/320)
    label += label_scale(labels[1], w[1]/320, h[0]/320, w[0]/320)
    label += label_scale(labels[2], w[0]/320, h[1]/320, 0, h[0]/320)
    label += label_scale(labels[3], w[1]/320, h[1]/320, w[0]/320, h[0]/320)

    layout = [[img1, img2],
              [img3, img4]]

    image = cv2.vconcat([cv2.hconcat(line) for line in layout])

    return image, label

def mosaic9(images, labels):
    salt1 = random.randint(25, 40) * 320
    salt2 = random.randint(25, 40) * 320
    w = [int(salt1/100), int(salt2/100), 320 - int(salt2/100) - int(salt1/100)]
    salt1 = random.randint(25, 40) * 320
    salt2 = random.randint(25, 40) * 320
    h = [int(salt1/100), int(salt2/100), 320 - int(salt2/100) - int(salt1/100)]

    img1 = cv2.resize(images[0], (w[0], h[0]), interpolation = cv2.INTER_AREA)
    img2 = cv2.resize(images[1], (w[1], h[0]), interpolation = cv2.INTER_AREA)
    img3 = cv2.resize(images[2], (w[2], h[0]), interpolation = cv2.INTER_AREA)
    img4 = cv2.resize(images[3], (w[0], h[1]), interpolation = cv2.INTER_AREA)
    img5 = cv2.resize(images[4], (w[1], h[1]), interpolation = cv2.INTER_AREA)
    img6 = cv2.resize(images[5], (w[2], h[1]), interpolation = cv2.INTER_AREA)
    img7 = cv2.resize(images[6], (w[0], h[2]), interpolation = cv2.INTER_AREA)
    img8 = cv2.resize(images[7], (w[1], h[2]), interpolation = cv2.INTER_AREA)
    img9 = cv2.resize(images[8], (w[2], h[2]), interpolation = cv2.INTER_AREA)

    label  = label_scale(labels[0], w[0]/320, h[0]/320)
    label += label_scale(labels[1], w[1]/320, h[0]/320, w[0]/320)
    label += label_scale(labels[2], w[2]/320, h[0]/320, w[0]/320+w[1]/320)
    label += label_scale(labels[3], w[0]/320, h[1]/320, 0, h[0]/320)
    label += label_scale(labels[4], w[1]/320, h[1]/320, w[0]/320, h[0]/320)
    label += label_scale(labels[5], w[2]/320, h[1]/320, w[0]/320+w[1]/320, h[0]/320)
    label += label_scale(labels[6], w[0]/320, h[2]/320, 0, h[0]/320+h[1]/320)
    label += label_scale(labels[7], w[1]/320, h[2]/320, w[0]/320, h[0]/320+h[1]/320)
    label += label_scale(labels[8], w[2]/320, h[2]/320, w[0]/320+w[1]/320, h[0]/320+h[1]/320)

    layout = [[img1, img2, img3],
              [img4, img5, img6],
              [img7, img8, img9]]

    image = cv2.vconcat([cv2.hconcat(line) for line in layout])

    return image, label

while len(image_files) > 10:
    func = random.choice(num)

    images = random.choices(image_files, k=func)

    for img in images:
        try:
            image_files.remove(img)
        except:
            print(img)

    if func == 1:
        copyfile(f'old_images/{images[0]}', 
                 f'images/{processed}.jpg')
        # copyfile(f'old_labels/{images[0].replace(".jpg", ".txt")}', 
        #         f'labels/lable_{processed}.txt')
        lbl_text =  open(f'old_labels/{images[0].replace(".jpg", ".txt")}', 'r+').readlines()
        # print(f'old_labels/{images[0].replace(".jpg", ".txt")}')
        # print(lbl_text)
        new_file = open(f'labels/{processed}.txt','w')
        for line in lbl_text:                    
            new_file.write(line)
            

        processed += 1

    if func == 4:
        file_images = []
        name_labels = []

        for img in images:
            file = cv2.imread(f'old_images/{img}')
            if file is None:
                print(img)
            name_labels.append(img.replace(".jpg", ".txt"))
            file_images.append(file)

        image, label = mosaic4(file_images, name_labels)

        cv2.imwrite(f'images/{processed}.jpg', image)
        with open(f'labels/{processed}.txt', 'w') as file:
            file.write(label)

        processed += 4
    
    if func == 9:
        file_images = []
        name_labels = []

        for img in images:
            file = cv2.imread(f'old_images/{img}')
            if file is None:
                print(img)
            name_labels.append(img.replace(".jpg", ".txt"))
            file_images.append(file)

        image, label = mosaic9(file_images, name_labels)

        

        cv2.imwrite(f'images/{processed}.jpg', image)
        with open(f'labels/{processed}.txt', 'w') as file:
            file.write(label)

        processed += 9

    print('Progress:', processed, '/', total_images, end='\r')

    
for image in image_files:
    copyfile(f'old_images/{image}', 
                 f'images/{processed}.jpg')
        
    lbl_text =  open(f'old_labels/{images[0].replace(".jpg", ".txt")}', 'r+').readlines()
    # print(f'old_labels/{images[0].replace(".jpg", ".txt")}')
    # print(lbl_text)
    new_file = open(f'labels/{processed}.txt','w')
    for line in lbl_text:                    
        new_file.write(line)

    processed += 1

    print('Progress:', processed, '/', total_images, end='\r')

print('finish')