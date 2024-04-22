import os

dataset_path = '.'
labels = os.listdir('labels')

labels_len = len(labels)
counter_img = 0
counter_dub = 0
counter_over = 0
counter_nf = 0
fin_line = []
to_remove = []

for label in labels:
    label_file = open(f'labels/' + label, 'r')
    lines = label_file.readlines()
    old_len = len(lines)
    lines = list(set(lines))
    new_len = len(lines)
    if new_len < old_len:
        counter_dub += 1
    for line in lines:
        if len(line.split(' ')) > 5:
            fin_line.append(' '.join(line.split(' ')[:5]))
            fin_line.append('0 ' + ' '.join(line.split(' ')[5:]))
            counter_over += 1

        elif line[0] != '0':
            counter_nf += 1
        else:
            fin_line.append(line)
    label_file.close()

    label_file = open(f'labels/' + label, 'w')
    label_file.writelines(fin_line)
    label_file.close()

    to_remove = []  
    fin_line = []
    counter_img += 1
    print(f'Progress: {counter_img}/{labels_len} over:{counter_over} nf:{counter_nf}', end='\r')

print(f'Progress: {counter_img}/{labels_len} over:{counter_over} nf:{counter_nf}')
