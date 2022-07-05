import os, sys


# please locate images folder at ../
# you should have ../images/00000.png

fw = open('img_path.txt', 'w')
dir_path = '../images'
cnt = 0
for (root, directories, files) in os.walk(dir_path):
    for file in files:
        cnt += 1
        file_path = os.path.join('../images', file)
        fw.write(file_path + '\n')
fw.close()
print(cnt)
