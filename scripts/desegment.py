import os

count = 0
count_broken = 0

labels = os.listdir('labels')
len_labels = len(labels)

for label in labels:
    label_file = open('labels/' + label, 'r')
    text = label_file.readlines()

    new_text = []
    for line in text:
        if len(line.split(' ')) > 5:
            new_text.append(' '.join(line.split(' ')[:5]) + '\n')
            new_text.append('0 ' + ' '.join(line.split(' ')[5:]))
            print(label)
            count_broken += 1
        else:
            new_text.append(line)
    
    label_file.close()

    label_file = open(f'labels/' + label, 'w')
    label_file.writelines(new_text)
    label_file.close()

    count += 1
    print('Progress:', count, '/', len_labels, 'br:', count_broken, end='\r')