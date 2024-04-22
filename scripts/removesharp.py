import os

files = os.listdir('datasets/fishes/test/labels/')

print(len(files))

for file in files:
    if '#' in file:
        os.remove('datasets/fishes/test/labels/' + file)