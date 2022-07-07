
import pcl
import struct

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


pc = pcl.load("/home/wjh/gangnam2_pcd/1656481494.537210464.pcd") # "pc.from_file" Deprecated
pc_rgb=XYZ_to_XYZRGB(pc,[0,0,0] )
pa = pc_rgb.to_array()

pa.tofile('./1540261303.747807979.bin')