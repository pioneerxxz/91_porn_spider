#coding=utf-8

class ProgressBar(object):
    def __init__(self, title, count=0.0, run_status=None, fin_status=None, total=100.0,    unit='', sep='/', chunk_size=1.0):
        super(ProgressBar, self).__init__()
        self.info = "[%s] %s %.2f %s %s %.2f %s"
        self.title = title
        self.total = total
        self.count = count
        self.chunk_size = chunk_size
        self.status = run_status or ""
        self.fin_status = fin_status or " " * len(self.statue)
        self.unit = unit
        self.seq = sep
 
    def __get_info(self):
        # 【名称】状态 进度 单位 分割线 总数 单位
        _info = self.info % (self.title, self.status, self.count/self.chunk_size, self.unit, self.seq, self.total/self.chunk_size, self.unit)
        return _info
 
    def refresh(self, count=1, status=None):
        self.count += count
        # if status is not None:
        self.status = status or self.status
        end_str = "\r"
        if self.count >= self.total:
            end_str = '\n'
            self.status = status or self.fin_status
            
 
        """
        没搞懂 print(end="")的用法
        ,在eric中打印的东西看不到
        ,在window控制台下单条语句刷新并不添加新的行
        """  
        # print(,end="")的用法,可能会出现打印看不到的情况
        print(self.__get_info(), end=end_str, )


# 这个地方要设置一下本地socks5代理
import requests
proxies = {
  'http' : 'socks5://127.0.0.1:1080',
  'https': 'socks5://127.0.0.1:1080'
}

from contextlib import closing
import os,re,time,random

def download_mp4(url,dir):
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36Name','Referer':'http://93.91p24.space'}
    #req=requests.get(url=url )
    
    with closing(requests.get(url=url, stream=True,proxies=proxies)) as response:
        chunk_size = 1024 # 单次请求最大值
        content_size = int(response.headers['content-length']) # 内容体总大小
        progress = ProgressBar('xxxxx', total=content_size, unit="KB", chunk_size=chunk_size, run_status="正在下载", fin_status="下载完成")
        filename=str(dir)+'/1.mp4'
        with open(filename, "wb") as file:
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
                progress.refresh(count=len(data))
           
           
    #filename=str(dir)+'/1.mp4'
    #with open(filename,'wb') as f:
        #f.write(req.content)
def download_img(url,dir):
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36Name','Referer':'http://93.91p24.space'}
    req=requests.get(url=url )
    with open(str(dir)+'/thumb.png','wb') as f:
        f.write(req.content)
def random_ip():
    a=random.randint(1,255)
    b=random.randint(1,255)
    c=random.randint(1,255)
    d=random.randint(1,255)
    return(str(a)+'.'+str(b)+'.'+str(c)+'.'+str(d))
flag=1
while flag<=3:
    tittle=[]
    base_url='http://93.91p24.space/view_video.php?viewkey='
    page_url='http://93.91p24.space/video.php?category=rf&page='+str(flag)
    get_page=requests.get(url=page_url )
    viewkey=re.findall(r'<a target=blank href="http://93.91p24.space/view_video.php\?viewkey=(.*)&page=.*&viewtype=basic&category=.*?">\n                    <img ',str(get_page.content,'utf-8',errors='ignore'))
    for key in viewkey:
        headers={'Accept-Language':'zh-CN,zh;q=0.9','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36','X-Forwarded-For':random_ip(),'referer':page_url,'Content-Type': 'multipart/form-data; session_language=cn_CN'}
        video_url=[]
        img_url=[]
        base_req=requests.get(url=base_url+key,headers=headers )
        video_url=re.findall(r'<source src="(.*?)" type=\'video/mp4\'>',str(base_req.content,'utf-8',errors='ignore'))
        tittle=re.findall(r'<div id="viewvideo-title">(.*?)</div>',str(base_req.content,'utf-8',errors='ignore'),re.S)
        img_url=re.findall(r'poster="(.*?)"',str(base_req.content,'utf-8',errors='ignore'))
        try:
            t=tittle[0]
            tittle[0]=t.replace('\n','')
            t=tittle[0].replace(' ','')
        except IndexError:
            pass
       # 这个地方要设置本地保存路径
        if os.path.exists("/disk/hdd/mov/latest/"+str(t))==False:
            try:
                os.makedirs("/disk/hdd/mov/latest/"+str(t))
                print('开始下载:'+str(t))
                download_img(str(img_url[0]),"/disk/hdd/mov/latest/"+str(t))
                download_mp4(str(video_url[0]),"/disk/hdd/mov/latest/"+str(t))
                print('下载完成')
            except:
                pass
        else:
            print('已存在文件夹,跳过')
            time.sleep(1)
    time.sleep(1)        
    flag=flag+1
    print('此页已下载完成，下一页是'+str(flag))
