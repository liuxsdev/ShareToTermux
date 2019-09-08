from requests_html import HTMLSession
import re

USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.102 Safari/537.36 Vivaldi/2.0.1309.42"



class BilibiliCover(object):
    
    def __init__(self,url):
        self.url=url
        self.urlType=self.urlType()
        self.coverInfo=self.getCoverInfo()
        
    
    def urlType(self):
        '''判断url是哪种类型的
        0:未知
        1:投稿    http://www.bilibili.com/video/av34729739/    
        2:番剧    http://www.bilibili.com/bangumi/play/ep128595/
        3:国创    http://www.bilibili.com/bangumi/play/ss6159
        4:直播    http://live.bilibili.com/live/515251.html  or 新http://live.bilibili.com/515251
        '''
        if "video" and "av" in self.url:
            return 1
        elif "bangumi" and "ep" in self.url:
            return 2
        elif "bangumi" and "ss" in self.url:
            return 3
        elif "live.bilibili.com" in self.url:
            return 4
        else:
            return 0

    def getWebContent(self,url):
        s=HTMLSession()
        r=s.get(url,headers={'user-agent':USER_AGENT})
        return r

    def avInfo(self):
        r = self.getWebContent(self.url)
        imgurl = r.html.find('[itemprop="image"]',first=True).attrs['content']
        title = r.html.find('title',first=True).text.replace('_哔哩哔哩 (゜-゜)つロ 干杯~-bilibili','')
        return imgurl,title

    def epInfo(self):
        r = self.getWebContent(self.url)
        imgurl = r.html.find('[property="og:image"]')[0].attrs['content']
        title = r.html.find('title',first=True).text.replace('_番剧_bilibili_哔哩哔哩','')
        return imgurl,title
    
    def ssInfo(self):
        r = self.getWebContent(self.url)
        imgurl = r.html.find('[property="og:image"]')[0].attrs['content']
        title = r.html.find('title',first=True).text.replace('_国创_bilibili_哔哩哔哩','')
        return imgurl,title

    def liveInfo(self):
        r = self.getWebContent(self.url)
        imgurl = r.html.search('"user_cover":"{}","key')[0].replace(r"\u002F","/")
        title = r.html.find('title',first=True).text.replace('- 哔哩哔哩直播，二次元弹幕直播平台','')
        return imgurl,title

    def getCoverInfo(self):
        if self.urlType == 1:
            return self.avInfo()
        elif self.urlType == 2:
            return self.epInfo()
        elif self.urlType == 3:
            return self.ssInfo()
        elif self.urlType == 4:
            return self.liveInfo()
        else:
            return None
    
    def downloadCover(self,path):
        '''下载封面，参数为路径，返回路径+文件名'''
        r = self.getWebContent(self.coverInfo[0])
        num = self.url.split('?')[0].split('/')[-1]
        filename=num+".jpg"
        print("title:",self.coverInfo[1])
        print(filename,"will be download at",path+filename)
        with open(path+filename,"wb") as f:
            f.write(r.content)
        print("done")
        return path+filename



if __name__ == "__main__":
    test = ['https://www.bilibili.com/video/av66645142','http://www.bilibili.com/bangumi/play/ep128595/','http://www.bilibili.com/bangumi/play/ss6159','http://live.bilibili.com/515251']
    for i in test:
        b=BilibiliCover(i)
        print(b.coverInfo)