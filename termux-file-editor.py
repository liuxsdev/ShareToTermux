#!/data/data/com.termux/files/usr/bin/python
import os
import sys

from bcover import BilibiliCover
from common import getAllFileContent,delFile
from common import termux_open,termux_dialog_radio

file_argv=sys.argv[1]
saveFolder="/sdcard/BilibiliCovers/"

if not os.path.exists(saveFolder):
    os.mkdir(saveFolder)



def nano(filepath):
    os.system('nano %s' % filepath)

def biliCover(fp):
    content=getAllFileContent(fp)
    bc=BilibiliCover(content)
    termux_open(bc.downloadCover(saveFolder))


#print('\n'*8)
#print("选择一个操作:")
#print("1\tBilibili:获取封面")
#print("2\t用nano编辑")
#print("\n")

choose = termux_dialog_radio("请选择一个操作","1. Bilibili:获取封面,2. 用nano编辑")['index'] + 1

# choose=int(input("请选择: "))
s={
    1:biliCover,
    2:nano,
}


funDo=s.get(choose,"错误的选择")
if(hasattr(funDo, '__call__')):
    funDo(file_argv)
else:
    print(funDo)

input("任意键退出")
