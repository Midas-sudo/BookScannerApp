from ctypes import sizeof
import subprocess
import shutil
import os
import cv2

main_DIR = "F:/Desktop/Programação/Python/BookScanner"

def checkFiles():
    phone_PATH = "/sdcard/Documents/vFlat"
    p1 = subprocess.Popen(f'adb.exe shell "cd {phone_PATH} && ls"',stdout=subprocess.PIPE)
    res = p1.stdout.read().decode('ascii').split('\n')
    print(res)
    if len(res) < 3:
        return False
    else:
        return res

def pullFiles(project_path, n_chap_1=-1, n_chap_2=-1, n_page=-1, n_trigger=0):
    phone_PATH = "/sdcard/Documents/vFlat"
    temp_PATH = "/Pages/vFlat/"
    p1 = subprocess.Popen(f'adb.exe pull -a {phone_PATH} "{project_path}/Pages/"',stdout=subprocess.PIPE)
    p1.wait()
    res = p1.stdout.read().decode('ascii')
    print(res)
    print(f'All good: {True if res.find("0 skipped") != -1 else False}')
    
    files = os.listdir(project_path + temp_PATH)
    if(len(files) == 2):
        True if os.path.isdir(f'{project_path}/Pages/Chap {n_chap_1}') else os.mkdir(f'{project_path}/Pages/Chap {n_chap_1}')
        True if os.path.isdir(f'{project_path}/Pages/Chap {n_chap_2}') else os.mkdir(f'{project_path}/Pages/Chap {n_chap_2}')
        shutil.move(project_path + temp_PATH + files[0], project_path + f'/Pages/Chap {n_chap_1}/Page-{n_page}.jpg')
        n_page = n_page + 1
        shutil.move(project_path + temp_PATH + files[1], project_path + f'/Pages/Chap {n_chap_2}/Page-{n_page}.jpg')
        return [project_path + f'/Pages/Chap {n_chap_1}/Page-{n_page-1}.jpg', project_path + f'/Pages/Chap {n_chap_2}/Page-{n_page}.jpg']
    else:
        if n_trigger == 1:
            print('Last Pages Scanned Incorrectly')
            return ['ERROR']
        for file in files:
            os.remove(project_path + temp_PATH + file)
        n_trigger = 1
        pullFiles(project_path, n_chap_1, n_chap_2, n_page, n_trigger)
    return ['ERROR']

def sendInput(x=553, y=1633):
    subprocess.Popen(f'adb.exe shell input tap {x} {y}')
    pass

def bulkPull (project_path, cur_chap=-1, last_new_chap=False, cur_page=-1):
    phone_PATH = "/sdcard/Documents/vFlat"
    temp_PATH = "/Pages/vFlat/"
    p1 = subprocess.Popen(f'adb.exe pull -a {phone_PATH} "{project_path}/Pages/"',stdout=subprocess.PIPE)
    p1.wait()
    res = p1.stdout.read().decode('ascii')
    print(res)

    files = os.listdir(project_path + temp_PATH)
    if last_new_chap:
        files.pop()
    for file in files:
        True if os.path.isdir(f'{project_path}/Pages/Chap {cur_chap}') else os.mkdir(f'{project_path}/Pages/Chap {cur_chap}')
        shutil.move(project_path + temp_PATH + file, project_path + f'/Pages/Chap {cur_chap}/Page-{cur_page}.jpg')
        cur_page += 1
    return [cur_page, project_path + f'/Pages/Chap {cur_chap}/Page-{cur_page-1}.jpg', project_path + f'/Pages/Chap {cur_chap}/Page-{cur_page}.jpg']
    
def removeFiles():
    p1 = subprocess.Popen('adb shell rm -f /sdcard/Documents/vFlat/*.jpg',stdout=subprocess.PIPE)
    p1.wait()
    return True

        


print(checkFiles())


# phone_PATH = "/sdcard/Documents/vFlat"

# p1 = subprocess.Popen('adb.exe shell',shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
# time.sleep(0.5)
# #p1.communicate(input=f'cd {phone_PATH}\n\n'.encode())
# p1.stdin.write(f'ls'.encode())
# p1.stdin.flush()
# teste = p1.stdout.read()
# # # print(teste.decode('ascii'))
# # # time.sleep(1)
# # # p1.stdin.write(f'ls\n\n'.encode())
# # # p1.stdin.flush()
# # # #p1.communicate(input=f'ls\n'.encode())
# # # time.sleep(1)
# # # teste = p1.stdout.read()
# print(teste.decode('ascii'))
# while(1):
#     ch = cv2.waitKey(22) & 0xFF

#     if ch == ord('1'):
#         os.system(adb shell input tap 553 1633)
#     elif ch == ord('2'):
#     elif ch == ord('3'):
#     elif ch == ord('4'):
#     elif ch == ord('5'):di
