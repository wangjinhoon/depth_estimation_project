import csv
import numpy as np
f = open('../gt_data.csv', 'r', encoding='utf-8')
rdr = csv.reader(f)
n = 0
for line in rdr:
    if n == 1:
        list1 = line[25:-1]
        break
    n+=1

print(list1)
f.close() 
