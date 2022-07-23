import shutil
import os


# pcd 파일들이 담긴 폴더 경로 설정해주기
path_dir = '/home/wjh/gangnam2_pcd'
 
file_list = os.listdir(path_dir)
file_list.sort()

total = len(file_list)


if os.path.exists("pcds_sort"):
    shutil.rmtree("pcds_sort")

os.mkdir("pcds_sort")

for i in range(total):
    shutil.copy(path_dir+"/"+file_list[i], "./pcds_sort")
    os.renames("./pcds_sort/"+file_list[i], "./pcds_sort/"+str(i+1)+".pcd")


# # 기존 디렉터리가 있으면 지워주기
# if os.path.exists("10pcds"):
#     shutil.rmtree("10pcds")


# # pcd 파일을 10개씩 담을 디렉터리 생성
# os.mkdir("10pcds")


# dir_count = 0  # 디렉터리 번호
# dir_fill = 0  # 디렉터리에 10개 찼는지 확인하기 위한 변수

# for i in range(total):
#     for j in range(3):
#         if(dir_fill == 0):  # 디렉터리가 텅 비어있으면 새 폴더 생성
#             os.mkdir("./10pcds/" + str(dir_count))
        
#         if(dir_fill == 10): # 꽉 찼으면 중단
#             break
        
#         shutil.copy(path_dir+"/"+file_list[i], "./10pcds/"+str(dir_count))
#         os.renames("./10pcds/"+str(dir_count)+"/"+file_list[i], "./10pcds/"+str(dir_count)+"/"+file_list[i]+str(dir_fill)+".pcd")
#         dir_fill += 1
    
#         if(dir_fill == 10):
#             dir_fill = 0
#             dir_count += 1
    

# ============================

# dir_c = 0
# count = 0
# for i in range(total):
#     dir_c = 0
#     count = 0
#     while(dir_c < 10 and count < 3):
#         shutil.copy(path_dir+"/"+file_list[i], "./10pcds/"+str(i//10))
#         os.renames("./10pcds/"+str(i//10)+"/"+file_list[i], "./10pcds/"+str(i//10)+"/"+str(i)+".pcd")
#         count += 1
#         dir_c += 1



# 2. 처음에는 제목이 1인 폴더 생성
# 3. count는 0부터 계속 올라가면서 폴더 하나에 파일 10개씩 저장
# 4. 근데 pcd 파일이 3개씩 복사되면서 저장되어야 함


# ############## 복사 #######################

# # 현재 디렉터리에서 파일 복사하기 후 다른 폴더로 저장
# shutil.copy('./test.txt', './copyfolder')   # test.txt 파일을 -> copyfolder 라는 폴더로 복사후 이동.

# # 절대경로를 이용해 저장하기
# shutil.copy('C:/Users/jay/PycharmProjects/pythonProject1/test.txt', 'C:/Users/jay/PycharmProjects/pythonProject1/copyfolder')   # 절대경로에있는 파일 -> 절대경로 폴더로 저장

# # 같은 디렉터리에서 파일 사본 만들기. (파일명이 서로 같으면 오류 발생)
# shutil.copy('./test.txt', './newcopyTest.txt')  # test.txt 파일의 내용물이 -> newcopyTest.txt 라는 이름으로 그대로 복사.

# # 전체 디렉터리(폴더)를 전체 복사
# shutil.copytree('./copyfolder', './copyfolder_copy')    # copyfolder의 모든 내용물과 함께, copyfolder_copy에 모든것이 그대로 복사.

# ################# 이동 ##########################

# # test.txt 파일을  movetest 라는 폴더로 이동
# shutil.move('./test.txt', './movetest')