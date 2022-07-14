import numpy as np
import cv2
import os
folder_path = "/home/wjh/image/"
save_path = "/home/wjh/MonoDEVSNet/calib_image/"

if not os.path.isdir(save_path):
    os.mkdir(save_path)


def start():
    file_list = os.listdir(folder_path)
    if "._1.png" in file_list:
        del file_list[file_list.index("._1.png")]
    file_list = [str(i+1)+".png" for i in  range(len(file_list))]
    n = 0
    for i in file_list:
        n+=1
        print(n)
        img = cv2.imread(folder_path+i, 0)
        height, width = img.shape
        int_param = np.array([[1365.4887468866116, 0.0, 1026.5997744850633],
                            [0.0, 1366.2954658193316, 468.9522311262687],
                            [0.0, 0.0, 1.0]])
        distortion = np.array([-0.3713184655742523, 0.1894083454473062, 0.0017443421254646307,
                                0.00037526691609012837,
                                -0.06081438434204424])
        int_param_scaling = np.array(
            [[1046.688720703125, 0.0, 1033.3313677806436, 0.0],
            [0.0, 1277.919921875, 460.2549448068021, 0.0],
            [0.0, 0.0, 1.0,  0.0]]
        ).reshape((3, 4))[:3, :3]

        rectification = np.eye(3)

        mapx, mapy = cv2.initUndistortRectifyMap(
            int_param,
            distortion,
            rectification,
            int_param_scaling,
            (width, height),
            cv2.CV_32FC1,
        )

        calibrated_img = cv2.remap(
            img,
            mapx,
            mapy,
            interpolation=cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_CONSTANT,
        )
        cv2.imwrite(save_path+ str(n) +'.png',calibrated_img)
        

if __name__ == "__main__":
    start()