from requests_html import HTMLSession
import re

USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.102 Safari/537.36 Vivaldi/2.0.1309.42"



class BilibiliCover(object):
    
    def __init__(self,urlText):
        self.urlText=urlText
        self.urlType=self.urlType()
        self.url=self.correctUrl()
        self.coverInfo=self.getCoverInfo()
        
    
    def urlType(self):
        '''判断url是哪种类型的
        0:未知
        1:投稿    http://www.bilibili.com/video/av34729739/
        2:番剧    http://www.bilibili.com/bangumi/play/ep128595/
        3:国创    http://www.bilibili.com/bangumi/play/ss6159
        4:直播    http://live.bilibili.com/live/515251.html
        '''
        if "video" and "av" in self.urlText:
            return 1
        elif "bangumi" and "ep" in self.urlText:
            return 2
        elif "bangumi" and "ss" in self.urlText:
            return 3
        elif "live.bilibili.com" in self.urlText:
            return 4
        else:
            return 0

    def correctUrl(self):
        '''对包含url的文本格式化，返回正确的url,num'''
        if self.urlType == 1:
            _m = re.search('av[0-9][0-9]{3,}',self.urlText)
            av_num = _m.group(0)
            return 'https://www.bilibili.com/video/%s/' % av_num,av_num
        elif self.urlType == 2:
            _m = re.search('ep[0-9][0-9]{3,}',self.urlText)
            ep_num = _m.group(0)
            return 'https://www.bilibili.com/bangumi/play/%s/' % ep_num,ep_num
        elif self.urlType == 3:
            _m = re.search('ss[0-9][0-9]{3,}',self.urlText)
            ss_num = _m.group(0)
            return 'https://www.bilibili.com/bangumi/play/%s/' % ss_num,ss_num
        elif self.urlType == 4:
            _m = re.search('live/(\d+).html',self.urlText)
            live_num = _m.group(1)
            return 'https://live.bilibili.com/live/%s.html' % live_num,live_num
        else:
            return "未知类型"

    def getWebContent(self,url):
        s=HTMLSession()
        r=s.get(url,headers={'user-agent':USER_AGENT})
        return r

    def avInfo(self):
        r = self.getWebContent(self.url[0])
        imgurl = r.html.find('[itemprop="image"]',first=True).attrs['content']
        title = r.html.find('title',first=True).text.replace('_哔哩哔哩 (゜-゜)つロ 干杯~-bilibili','')
        return imgurl,title

    def epInfo(self):
        r = self.getWebContent(self.url[0])
        imgurl = r.html.find('[property="og:image"]')[0].attrs['content']
        title = r.html.find('title',first=True).text.replace('_番剧_bilibili_哔哩哔哩','')
        return imgurl,title
    
    def ssInfo(self):
        r = self.getWebContent(self.url[0])
        imgurl = r.html.find('[property="og:image"]')[0].attrs['content']
        title = r.html.find('title',first=True).text.replace('_国创_bilibili_哔哩哔哩','')
        return imgurl,title

    def liveInfo(self):
        r = self.getWebContent(self.url[0])
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
        r = self.getWebContent(self.coverInfo[0])
        filename=self.url[1]+".jpg"
        print("title:",self.coverInfo[1])
        print(filename,"will be download at",path+filename)
        with open(path+filename,"wb") as f:
            f.write(r.content)
        print("done")
        return path+filename



