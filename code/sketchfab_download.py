import os
import sys
import re
import json
import requests
import argparse
import shutil
from urllib.parse import urlparse
from html.parser import HTMLParser
from html import unescape
from bs4 import BeautifulSoup
from subprocess import Popen
# ------------------------------------------
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.25 Safari/537.36',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh-TW;q=0.8,zh;q=0.6,en;q=0.4,ja;q=0.2',
    'cache-control': 'max-age=0'
}
# ------------------------------------------
def _get_image_url(images):
    width = 0
    for img in images:
        if img['width'] > width:
            width = img['width']
            imgUrl = img['url']
    return imgUrl

def _download(url, filename, retry_times = 3):
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        if os.path.exists(filename):
            os.remove(filename)
        with open(filename, 'wb') as file:
            print("Downloading Url:", url)
            file.write(requests.get(url, headers=HEADERS, timeout=30).content)
        if os.path.getsize(filename) < 10: # 小于10字节认为下载失败
            if retry_times > 0:
                print("下载失败，正在尝试重新下载... (还剩余尝试%s次)" % retry_times)
                return _download(url, filename, retry_times - 1)
            else:
                print("Failed Download url:" + url)
                return False
        return True
    except Exception:
        pass

def parse(url, output_path):
    url = url + "/embed?autostart=1" # fix issue #6
    try:
        print('Pending...\n')
        page = requests.get(url, headers=HEADERS, timeout=30).content
        soup = BeautifulSoup(page, "html.parser")
        data = unescape(soup.find(id = 'js-dom-data-prefetched-data').string)
        data = json.loads(data)
        modelId = urlparse(url).path.split('/')[2].split('-')[-1]
        model_name = modelId
        #保存目录的名字去除中间空格
        dir_name = ''.join(model_name.split()).lower()
        # 缩略图文件(下载最大分辨率的那张)
        thumbnailData = data['/i/models/' + modelId]['thumbnails']['images']
        thumbnail = _get_image_url(thumbnailData)
        # osgjs文件
        osgjsUrl = data['/i/models/' + modelId]['files'][0]['osgjsUrl']
        # model文件
        modelFile = osgjsUrl.replace('file.osgjs.gz', 'model_file.bin.gz') # 是sketchfab私有的名字 model_file.bin.gz
        # texture文件
        texturesData = data['/i/models/' + modelId + '/textures?optimized=1']['results']
        save_dir_path = os.path.join(output_path, dir_name)
        download_dir_path = save_dir_path + "_temp"
        failedDownLoadUrlList = []
        print('开始下载缩略图...')
        _download(thumbnail, os.path.join(download_dir_path, 'thumbnail.jpg'))
        print('开始下载模型数据...')
        _download(osgjsUrl, os.path.join(download_dir_path, 'file.osgjs'))
        print('开始下载模型...')
        _download(modelFile, os.path.join(download_dir_path, 'model_file.bin.gz'))
        cnt = 0
        for texture in texturesData:
            print('开始下载贴图... (%s/%s)' % (cnt, len(texturesData)))
            textureUrl = _get_image_url(texture['images'])
            fn = urlparse(textureUrl).path.split('/')[-1]
            ok = _download(textureUrl, os.path.join(download_dir_path, 'texture', fn))
            if not ok:
                failedDownLoadUrlList.append(textureUrl)
            cnt = cnt + 1
        if os.path.exists(save_dir_path):
            shutil.rmtree(save_dir_path)
        shutil.move(download_dir_path, save_dir_path)
        if failedDownLoadUrlList:
            print("=======================\nMaybe netWork problem, some textures download failed, you can download them manually:\n", failedDownLoadUrlList)
            print("\n========================================\n")
    except AttributeError:
        raise
        return False

def main(args):
    if args.url:
        cwd = os.getcwd()
        os.chdir(args.output)
        parse(args.url, args.output)
        os.chdir(cwd)
    else:
        print("未使用 -u 参数传入url")
        sys.exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='www.sketchfab.com 下载模型')
    parser.add_argument("-u",  "--url", help="sketchfab模型的网页链接")
    parser.add_argument("-o",  "--output", help="下载之后保存到本地的目录路径, 不传默认下载到当前脚本所处的目录")
    args = parser.parse_args()
    if not args.output:
        args.output = os.path.dirname(os.path.abspath(__file__))
    main(args)