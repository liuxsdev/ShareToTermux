#!/data/data/com.termux/files/usr/bin/python
import os
import sys

from bcover import BilibiliCover
from common import getAllFileContent,delFile
from common import termux_open,termux_dialog_radio
from common import extractUrl

file_argv=sys.argv[1]
saveFolder="/sdcard/BilibiliCovers/"

if not os.path.exists(saveFolder):
    os.mkdir(saveFolder)



# 1.用nano编辑
def nano(filepath):
    os.system('nano %s' % filepath)

# 2.Bilibili:获取封面
def biliCover(fp):
    content=getAllFileContent(fp)
    bc=BilibiliCover(content)
    termux_open(bc.downloadCover(saveFolder))

# 3.尝试下载此视频
def downloadVideo(fp):
    url = extractUrl(getAllFileContent(fp))
    if url:
        print("使用 youtube-dl 进行下载")
        filename = saveFolder + "%(title)s.%(ext)s"
        CMD = 'youtube-dl "%s" --output "%s"' % (url,filename)
        os.system(CMD)
    else:
        print('未提取到url')
    input("按任意键退出")

choose = termux_dialog_radio("请选择一个操作","1. Bilibili:获取封面,2. 用nano编辑,3. 尝试下载此视频")['index'] + 1

# choose=int(input("请选择: "))
s={
    1:biliCover,
    2:nano,
    3:downloadVideo
}


funDo=s.get(choose,"错误的选择")
if(hasattr(funDo, '__call__')):
    funDo(file_argv)
else:
    print(funDo)


