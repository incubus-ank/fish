import os

labels = os.listdir('labels')

counter = 0
for label in labels:
    text = open('labels/'+label).readlines()
    counter += len(text)

print(counter)