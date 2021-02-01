import os
import sys
import re
import json
import requests
import argparse
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
def getBiggestImage(images):
    width = 0
    for img in images:
        if img['width'] > width:
            width = img['width']
            imgUrl = img['url']
    return imgUrl

def validateTitle(title):
    pattern = r'[\\/:*?"<>|\r\n]+'
    newTitle = re.sub(pattern, "_", title)
    return newTitle

def download(url, filename, retry_times = 3):
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        if os.path.exists(filename):
            os.remove(filename)
        with open(filename, 'wb') as file:
            file.write(requests.get(url, headers=HEADERS, timeout=20).content)
        if os.path.getsize(filename) < 1024: # 小于1024字节认为下载失败, 1024字节=1KB
            if retry_times > 0:
                print("下载失败，正在尝试重新下载... (还剩余尝试%s次)" % retry_times)
                download(url, filename, retry_times - 1)
            else:
                #print('重新尝试下载全部失败 filename=%s, 可手动去浏览器使用填写地址:%s来下载' % (filename, url))
                print("下载失败, 请检查网络再尝试重新下载！")
                sys.exit(1)
    except Exception:
        pass

def DoParse(url, output_path):
    try:
        print('Pending...\n')
        page = requests.get(url, headers=HEADERS, timeout=20).text
        soup = BeautifulSoup(page, 'html.parser')
        data = unescape(soup.find(id = 'js-dom-data-prefetched-data').string)
        data = json.loads(data)
        modelId =urlparse(url).path.split('/')[2].split('-')[-1]
        model_name = url[url.rindex('/')+1:url.rindex('-')].replace('-','') 
        #去除中间空格
        name = ''.join(model_name.split()).lower()
        # 缩略图文件(下载最大分辨率的那张)
        thumbnailData = data['/i/models/' + modelId]['thumbnails']['images']
        thumbnail = getBiggestImage(thumbnailData)
        # osgjs文件
        osgjsUrl = data['/i/models/' + modelId]['files'][0]['osgjsUrl']
        # model文件
        modelFile = osgjsUrl.replace('file.osgjs.gz', 'model_file.bin.gz') # 是sketchfab私有的名字 model_file.bin.gz
        # texture文件
        texturesData = data['/i/models/' + modelId + '/textures?optimized=1']['results']
        textures = []
        save_dir_path = os.path.join(output_path, name)
        print('开始下载缩略图...')
        download(thumbnail, os.path.join(save_dir_path, 'thumbnail.jpg'))
        print('开始下载模型...')
        download(osgjsUrl, os.path.join(save_dir_path, 'file.osgjs'))
        download(modelFile, os.path.join(save_dir_path, 'model_file.bin.gz'))
        cnt = 0
        for texture in texturesData:
            print('开始下载贴图... (%s/%s)' % (cnt, len(texturesData)))
            textureUrl = getBiggestImage(texture['images'])
            download(textureUrl, os.path.join(save_dir_path, 'texture', validateTitle(texture['name'])))
            cnt = cnt + 1
    except AttributeError:
        raise
        return False

def main(args):
    if args.url:
        cwd = os.getcwd()
        os.chdir(args.output)
        DoParse(args.url, args.output)
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