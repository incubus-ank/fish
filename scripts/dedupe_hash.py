import os
import hashlib 

# split_group_list = ['test', 'train', 'valid']
split_group_list = ['images']    
dataset_path = '.'
complited = 0
num_images = len(os.listdir(f'{dataset_path}/{split_group_list[0]}'))

for group in split_group_list:
    directory = f'{dataset_path}/{group}'
    
    hashes = set()
    
    del_num = 0
    # в датасете есть дубликаты с другим именем изображения
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        
        #хэшируем image
        digest = hashlib.sha1(open(path,'rb').read()).digest()
        
        if digest not in hashes:
            # если не дубликат, то добавляем в hashes
            hashes.add(digest)
        
        else:
            # удаляем image
            os.remove(path)
            
            label_name = filename.replace('.jpg','.txt')
            label_path = f'{dataset_path}/labels/{label_name}'
            # удаляем label
            os.remove(label_path)
            
            del_num += 1
        complited += 1
        print(f'Выполнено: {complited} / {num_images}', end='\r')

    print(f'{group}: удалено {del_num} изображений')
    
print('Дубликаты удалены')