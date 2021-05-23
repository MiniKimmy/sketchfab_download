# -*- coding: UTF8 -*-
import time
import datetime
import sys
import os
import subprocess
import shutil
import argparse
# ------------------------------------------
cp = os.path.dirname(os.path.abspath(__file__))               # 当前脚本目录
py = "\\../bin/py/python.exe"                                 # 已带有py环境
download_dir = cp                                             # 下载保存的目录
output_dir = os.path.join(os.path.expanduser('~'), "Desktop") # 最终保存到桌面
custom_dir = "sketchfab_outputs"                              # 如果下载完成没目录, 则默认创建该目录 "output_dir/custom_dir"
# ------------------------------------------
def call(cmd, retry_time = 1):
    while retry_time > 0:
        # print(cmd)
        returnCode = subprocess.call(cmd, shell=True)
        retry_time -= 1
        if returnCode != 0:
            print("err returnCode:", returnCode)
            if retry_time <= 0:
                os.system("color c")
                os.system("pause")
                sys.exit(returnCode)
        else:
            break

def get_blend_exe_path():
    return cp + os.sep + "\\..\\blender" + os.sep + "blender.exe"

def err_exit(msg, returnCode = 1):
    os.system(f"echo {chr(27)}[31m")
    print("++++++++++++++++++++++++++++++++++++++++++++")
    print(msg)
    print("++++++++++++++++++++++++++++++++++++++++++++")
    os.system(f"echo {chr(27)}[0m")
    os.system("color c")
    os.system("pause")
    sys.exit(returnCode)

def download_model(url):
    download_path = ""
    dst_path = ""
    # download start
    now = time.time()
    # downloading
    py_file = cp + os.sep + "sketchfab_download.py"
    cmd = "%s %s -u %s -o %s" % (cp + py, py_file, url, os.getcwd())
    call(cmd)
    # download complete
    fin_time = time.time()
    first_creat = fin_time + 666888
    files = os.listdir(cp)
    for file in files:
        abs_path = os.path.join(cp, file)
        if os.path.isdir(abs_path):
            dir_ctime = os.path.getmtime(abs_path)
            if dir_ctime >= now and dir_ctime <= fin_time and dir_ctime < first_creat:
                first_creat = dir_ctime
                download_path = abs_path
    if download_path == "":
        # 可能下载不保存到文件夹里
        list = []
        for file in files:
            abs_path = os.path.join(cp, file)
            if os.path.isdir(abs_path):
                dir_ctime = os.path.getmtime(abs_path)
                if dir_ctime >= now and dir_ctime <= fin_time :
                    list.append(file)
        if list:
            dst_path = os.path.join(output_dir, custom_dir)
        else:
            err_exit("下载模型失败")
    else:
        fn = os.path.basename(download_path).strip().replace(' ', '').lower()
        dst_path = os.path.join(output_dir, fn)
    print("save_dir_name=%s\nsave_abs_path=%s\n" % (fn, dst_path))
    if os.path.exists(dst_path):
        shutil.rmtree(dst_path)
    shutil.move(download_path, dst_path)
    return dst_path

def decode_model(osgjs_dir):
    py_path = cp + os.sep + "decode_osgjs.py"
    cmd = "%s -b -P %s --model_path %s" % (get_blend_exe_path(), py_path, osgjs_dir)
    call(cmd)

def export_fbx(blend_dir):
    blend_exe_path = get_blend_exe_path()
    files = os.listdir(blend_dir)
    blend_fn = ""
    for file in files:
        if file.endswith(".blend"):
            blend_fn = file
            break
    if blend_fn:
        blend_path = os.path.join(blend_dir, blend_fn)
        py_path = cp + os.sep + "blend2fbx.py"
        cmd = "%s %s -P %s --blend_fn %s" % (get_blend_exe_path(), blend_path, py_path, blend_path)
        call(cmd)
    else:
        err_exit("找不到.blend文件", blend_dir)

def main(url):
    print("step 1 ============ download model ============")
    output_path = download_model(url)
    print("step 2 ============ decode blend ============")
    decode_model(output_path)
    print("step 3 ============ export fbx ============")
    export_fbx(output_path)
    print("\noutput_path: %s\n" % output_path)

if __name__ == '__main__':
    os.chdir(cp) # .bat运行时 切换当前工作环境和脚本是同一个目录下
    print("请输入网址:")
    input_url = sys.stdin.readline()
    input_url = input_url.strip()
    if input_url and input_url.find('sketchfab') != -1:
        main(input_url)
    else:
        err_exit("invalid url:%s" % input_url)
        