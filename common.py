import os
import requests
import subprocess
import json

def correctFilename(filename):
    rep='\/:*?"<>|`'
    for i in rep:
        file=filename.replace(i,"")
    return file

def downloadFileByUrl(url,path,filename=None):
    '''
    从形如http://i2.hdslb.com/bfs/archive/axx.jpg的链接下载文件
    '''
    if filename:
        filename=correctFilename(filename)
    else:
        filename=url.split('/')[-1]    #get filename from url
    if not os.path.exists(path):
        os.mkdir(path)
    r=requests.get(url)
    with open(path+filename,'wb') as f:
        f.write(r.content)

def downloadFileByUrlUseAria2(url):
    cmd="aria2c %s" %url
    print(cmd)
    os.system(cmd)

def getAllFileContent(path):
    with open(path,"r",encoding="utf-8") as f:
        return f.read()

def delFile(filepath):
    try:
        os.remove(filepath)
        return True
    except:
        return Fasle

def termux_open(filepath):
    os.system("termux-open %s" % filepath)

def termux_dialog_radio(title,options):
    s = 'termux-dialog radio -t {} -v {}'.format(title,options)
    a = subprocess.getoutput(s)
    print(s,a)
    return json.loads(a)
