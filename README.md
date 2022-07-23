# ACELAP Project

# 프로젝트 목표
이미지와 LiDAR 데이터가 들어있는 bagfile에서 이미지 데이터에 대한 monocular depth estimation을 진행한 후, LiDAR 데이터로 estimated depth를 평가하는 것. 

## 프로젝트 개요
![image](https://user-images.githubusercontent.com/54730375/180582510-8460029b-6683-4267-a9f1-99eb9e7bed0d.png)  

- rosbag파일로부터 image & LiDAR data 추츌.
- 선정모델을 통해 추출된 image inference.
- LiDAR data를 사용 가능한 gt data로 가공.
- 가공된 gt data와 model inference값을 이용해 에러 계산.

<br><br>

# 선정모델
MONODELSNet: https://github.com/HMRC-AEL/MonoDEVSNet

<br>

## 특징
Real World data 비지도학습 + Virtual World data 지도학습을 통해 비지도학습만 있을 때 야기되는 문제점들을 극복.  





<br>

## 선정이유
- LiDAR 데이터를 GT로 사용
- 성능향상 요소존재
    - Depth threshold 조정.
    - Backbone model 변경이 용이하도록 모듈화.
- Input Image 크기와 상관 없이 적용가능.
- KITTI Eigen 밴치마크에서 우수한 성능을 보임. (4등)
![image](https://user-images.githubusercontent.com/54730375/180582972-d7b1a26e-2961-421c-a076-1c0211cc3fe7.png)

- 논문목적이 도로위에서의 traffic depth 추정을 목표로 함. (프로젝트와 방향성 유사)
- fps 수치가 높음. → 실시간성 고려. (하드웨어 성능에 따라 변동 가능.)  
![image](https://user-images.githubusercontent.com/54730375/180583054-69aade91-96a7-4026-afaf-04f928af0549.png)

<br><br>

# 개선사항
## 전처리 & 후처리
1. rosbag 파일에서 이미지&PCD파일 추출
    - pointcloud2topcl.py
    - get_frame.py
2. LiDAR msg: image = 371: 1104 -> LiDAR 갯수에 맞게 image 3개당 1개 추출.
    - choose_img.py
3. 추출한 PCD파일을 npz파일로 변환 & outlier 제거
    - pcd_to_bin.py
    - proj_lidar2cam.py(이미지에 라이다 projection)
    - create_gt_txt.py(outlier 제거포함)
    - txt_to_npz.py
4. 이미지 캘리브레이션
    - calib_image.py

5. 평가에 참여한 픽셀만 보여주는 히트맵 생성
    - image2cv.py

<br>

## evaluation 코드 수정
1. gt_data 받아오기

```python
 gt_depth = self.gt_depths[iter_l]
                gt_height, gt_width = gt_depth.shape
                pred_disp = cv2.resize(pred_disp, (gt_width, gt_height), cv2.INTER_NEAREST)
                pred_depth = self.opt.syn_scaling_factor / pred_disp.copy()
```

2. depth filter(0.1m < d < 120m) & Hitmap 생성코드 추가

```python
gt_depth[gt_depth < self.opt.min_depth] = self.opt.min_depth
                gt_depth[gt_depth > self.opt.max_depth] = self.opt.max_depth
                pred_depth[pred_depth < self.opt.min_depth] = self.opt.min_depth
                pred_depth[pred_depth > self.opt.max_depth] = self.opt.max_depth

plat_gt_depth = gt_depth.reshape(-1)
plat_pred_depth = pred_depth.reshape(-1)

new_gt_depth, new_pred_depth = [], []
hitmap = np.zeros((gt_height, gt_width, 3), dtype=np.uint8)
for idx, item in enumerate(plat_gt_depth):
    if item > 0.1 and item < 80:
        new_gt_depth.append(item)
        new_pred_depth.append(plat_pred_depth[idx])
        hitmap[idx//gt_width, idx % gt_width] = [255,255,255]


img = Image.fromarray(hitmap, 'RGB')
img.save('mytest.png')
img.show()
```

3. error 계산

```python
errors_absolute.append(compute_errors(np.array(new_gt_depth), np.array(new_pred_depth)))
print('avg_FPS: {}' .format(1/avg_time))
        errors_absolute = np.array(errors_absolute).mean(0)
        print("/n")
        print("  " + ("{:>8} | " * 7).format("abs_rel", "sq_rel", "rmse", "rmse_log", "a1", "a2", "a3"))
        print(("&{: 8.4f}  " * 7).format(*errors_absolute.tolist()) + "\\\\")
        print('time taken for network model {}-{}: {}'.format(self.opt.models_fcn_name['encoder'], self.opt.num_layers, 1 / np.mean(time_for_each_frame)))
```

<br><br>


# 사용법

## 1. 모델 빌드
MONODELSNet git 참고
https://github.com/HMRC-AEL/MonoDEVSNet

## 2. bag파일에서 이미지와 라이다 데이터 추출.
- pointcloud2topcl.py 내 bag파일 경로 & 토픽이름 설정.
    ```python
    for topic, msg, t in rosbag.Bag('/demo.bag').read_messages():
    if topic == "/velodyne_points":
        pc_np, pc_pcl = convert_pc_msg_to_np(msg)
    ```
- get_frame.py 실행 (이미지 저장)
    ```
    python get_frame.py --bag_file [bagfile경로] --output_dir [output dir경로] --image_topic [토픽이름]
    ```
<br>

## 3. gt값 가공
 - pcd_to_bin.py (save path, pcd file path 설정필요)
 - create_gt_txt.py (file path 설정필요)
 ```python
 folder_path = "/home/wjh/MonoDEVSNet/bin/"   # binfile path
save_path = "/home/wjh/MonoDEVSNet/gt"        # save file path
if not os.path.isdir(save_path):
    os.mkdir(save_path)

if not os.path.isdir(save_path):
    os.mkdir(save_path)


def start():
    n = 0
    file_list = os.listdir(folder_path)
    file_list = [str(i+1)+".bin" for i in  range(len(file_list))]
    img = f'/home/wjh/MonoDEVSNet/1.png'       # sample input image path 
    for j in file_list:
        n+=1
        binary = folder_path + j
        # calibration txt file path
        with open(f'/home/wjh/MonoDEVSNet/testing/calib/gn2.txt','r') as f:
```
 - txt_to_npz.py (txt 파일 path 설정 필요)


## 4. pretrained weight 다운로드
https://drive.google.com/drive/folders/1LZuBsG6XFjYnVwkELMENHjwfyRyRvjEs


## 5. evaluation 진행
- evaluation.py 에 class evaluation init에 gt npz파일 수정.

```python
gt_path = os.path.join(os.path.dirname(__file__), "splits", "eigen", "[gt npz파일 경로]")
```
- 명령어 실행
```
python3 evaluation.py --dataset any --models_fcn_name encoder ResNet_18 --num_layers 18 --image_folder_path ../gt20_image/ --load_weights_folder ../MonoDELSNet_ResNet_18_HR/
```

## 6. 결과 확인
![image](https://user-images.githubusercontent.com/54730375/180585137-c93cdffc-6e92-412a-ac82-8d0c1c0a0987.png)

<br>

프로젝트 노션 페이지 https://prgrms.notion.site/ACE-61fde8dbf704436a944ed07b31cb2b07
