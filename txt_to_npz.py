import numpy as np
import os
import sys

folder_path = "../wjh/"

def start():
    list1 = []
    list2 = []
    list3 = []
    file_list = os.listdir(folder_path)
    print(file_list)
    for i in file_list:
        f = open(folder_path+i, 'r')
        lines = f.readlines()
        lines = list(map(lambda s: s.strip(), lines))
        for line in lines:
            list1 = line.split(',')
            B = [float(x) for x in list1]
            list2.append(B)
            list1 = []
        f.close()
        list3.append(list2)
        list2 = []
    np.savez_compressed('data', data=list3)
if __name__ == "__main__":
    start()