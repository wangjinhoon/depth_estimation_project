
import pcl
import struct
import os

folder_path = "/home/wjh/MonoDEVSNet/pcds_sort/"
save_path = "/home/wjh/MonoDEVSNet/bin"

if not os.path.isdir(save_path):
    os.mkdir(save_path)
    
def XYZ_to_XYZRGB(XYZ_cloud, color):
    XYZRGB_cloud = pcl.PointCloud_PointXYZRGB()
    points_list = []

    float_rgb = rgb_to_float(color)

    for data in XYZ_cloud:
        points_list.append([data[0], data[1], data[2], float_rgb])

    XYZRGB_cloud.from_list(points_list)
    return XYZRGB_cloud

def rgb_to_float(color):
    hex_r = (0xff & color[0]) << 16
    hex_g = (0xff & color[1]) << 8
    hex_b = (0xff & color[2])

    hex_rgb = hex_r | hex_g | hex_b
    float_rgb = struct.unpack('f', struct.pack('i', hex_rgb))[0]
    return float_rgb

def start():
    file_list = os.listdir(folder_path)
    file_list = [str(i+1)+".pcd" for i in  range(len(file_list))]
    
    n = 0 
    for i in file_list:
        n+=1
        pc = pcl.load(folder_path+i) # "pc.from_file" Deprecated
        pc_rgb=XYZ_to_XYZRGB(pc,[0,0,0] )
        pa = pc_rgb.to_array()
        os.chdir(save_path)
        pa.tofile(str(n)+'.bin')

if __name__ == "__main__":
    start()