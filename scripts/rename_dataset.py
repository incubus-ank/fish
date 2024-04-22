import os

dataset_path = '.'

images = os.listdir('images')
labels = os.listdir('labels')

num_images = len(images)
num_labels = len(labels)

counter = 0
cun_lab = 0

for image in images:
    os.rename(os.path.join(dataset_path, 'images', image), 
              os.path.join(dataset_path, 'images', f'{counter:06}' + '.jpg'))
    
    if image[:-4] + '.txt' in labels:
        os.rename(os.path.join(dataset_path, 'labels', image[:-4] + '.txt'), 
            os.path.join(dataset_path, 'labels', f'{counter:06}' + '.txt'))
        cun_lab += 1
    else:
        open(os.path.join(dataset_path, 'labels', f'{counter:06}' + '.txt'), 
             'a').close()
        pass

    counter += 1

    print(f'Process: {counter} / {num_images}, lebeled: {cun_lab}')