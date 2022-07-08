import sys, os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import pandas as pd

folder_path = "/home/wjh/MonoDEVSNet/bin/"
save_path = "/home/wjh/MonoDEVSNet/gt"
if not os.path.isdir(save_path):
    os.mkdir(save_path)

if not os.path.isdir(save_path):
    os.mkdir(save_path)


def start():
    n = 0
    file_list = os.listdir(folder_path)
    img = f'/home/wjh/MonoDEVSNet/frame000000.png'
    for j in file_list:
        n+=1
        binary = folder_path + j
        print(binary)
        with open(f'/home/wjh/MonoDEVSNet/testing/calib/gn2.txt','r') as f:
            calib = f.readlines()

        # P2 (3 x 4) for left eye
        P2 = np.matrix([float(x) for x in calib[2].strip('\n').split(' ')[1:]]).reshape(3,4)
        R0_rect = np.matrix([float(x) for x in calib[4].strip('\n').split(' ')[1:]]).reshape(3,4)
        # Add a 1 in bottom-right, reshape to 4 x 4
        # R0_rect = np.insert(R0_rect,3,values=[0,0,0],axis=0)
        R0_rect = np.insert(R0_rect,3,values=[0,0,0,1],axis=0)
        Tr_velo_to_cam = np.matrix([float(x) for x in calib[5].strip('\n').split(' ')[1:]]).reshape(3,4)
        Tr_velo_to_cam = np.insert(Tr_velo_to_cam,3,values=[0,0,0,1],axis=0)

        # read raw data from binary
        scan = np.fromfile(binary, dtype=np.float32).reshape((-1,4))
        points = scan[:, 0:3] # lidar xyz (front, left, up)
        # TODO: use fov filter? 
        velo = np.insert(points,3,1,axis=1).T
        velo = np.delete(velo,np.where(velo[0,:]<0),axis=1)
        cam = P2 * R0_rect * Tr_velo_to_cam * velo 
        cam = np.delete(cam,np.where(cam[2,:]<0)[1],axis=1)
        # get u,v,z
        cam[:2] /= cam[2,:]
        print(cam)
        # do projection staff
        png = mpimg.imread(img)
        IMG_H,IMG_W = png.shape
        # restrict canvas in range
        plt.axis([0,IMG_W,IMG_H,0])
        plt.imshow(png)
        # filter point out of canvas
        u,v,z = cam
        u_out = np.logical_or(u<0, u>IMG_W)
        v_out = np.logical_or(v<0, v>IMG_H)
        outlier = np.logical_or(u_out, v_out)
        cam = np.delete(cam,np.where(outlier),axis=1)
        # generate color map from depth
        u,v,z = cam

        gt_list = np.array([[0]*2040 for i in range(1086)])
        for i in range(z[0].size):
            if pd.isnull(z[0,i]):
                pass
            else:
                gt_list[int(v[0,i])][int(u[0,i])] = z[0,i]
        os.chdir(save_path)
        np.savetxt(str(n)+'.txt',gt_list, fmt = '%2d', delimiter = ',')

if __name__ == "__main__":
    start()