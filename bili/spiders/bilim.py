import scrapy
import re
import urllib
import json
import time
import datetime
from bili.items import VideoItem,CommentItem
from scrapy import Request
#selenium：是Python的一个第三方库，对外提供的接口可以操作浏览器，然后让浏览器完成自动化的操作。
# 谷歌无头浏览器
from selenium import webdriver
from scrapy_redis.spiders import RedisSpider
from time import sleep
# 导入指定包
from selenium.webdriver.chrome.options import Options

class BiliSpider(RedisSpider):
    name = 'Bili'
    keywords = u'小米智能家居'.encode('utf-8')
    page=15
    allowed_domains = ['bilibili.com',
                       'search.bilibili.com',
                       'api.bilibili.com']
    #self_url='https://search.bilibili.com/all?keyword={}'.format(urllib.parse.quote(keywords))
    #start_urls = [self_url+'&page={}'.format(page)]
    #print(start_urls)
    redis_key = "Bili:start_urls"
    bro = webdriver.Chrome(executable_path=r'D:\Workspaces\pyEnvs\bishe\chromedriver.exe')

    urls = []# 最终存放的就是5个板块对应的url

    def parse(self, response):
        video_urls = response.xpath('//li[@class="video-item matrix"]/a/@href').extract()
        print('sss')
        print(video_urls)
        print('ddd')
        for url in video_urls:
            url = 'https:'+url
            yield scrapy.Request(url=url,callback=self.parse_videos, dont_filter=True)
        #last_page = int(response.xpath('//li[@class="page-item last"]/button/text()').get())

        #now_page = int(response.xpath('//li[@class="page-item active"]/button/text()').get())
       # while now_page <= last_page:
           # keywords = u'小米家居'.encode('utf-8')
           # self_url = 'https://search.bilibili.com/all?keyword={}'.format(urllib.parse.quote(keywords))
            #now_page = now_page+1
            #now_page=1
            #url= self_url + '&page={}'.format(now_page)
            #time.sleep(3)
            #yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)
        

        #if next_page:
         #   yield scrapy.Request(url=self.self_url+'&page={}'.format(self.page+1),callback=self.parse)
    # 用来解析每一个查询对应的视频
    # 【视频的标题、制作者、】
    def parse_videos(self,response):
        #video
        item = VideoItem()
        item['video_title'] = response.xpath('//h1[@class="video-title"]/@title').get().replace('\n', '').replace('\r', '').replace(' ', '')

        video_like = response.xpath('//div[@class="ops"]/span[@class="like"]/text()').get()
        if video_like:
            if isinstance(video_like, int):
                item['video_like'] = video_like
            else:
                item['video_like'] = video_like.replace('\n', '').replace('\r', '').replace(' ', '')
        else:
            item['video_like'] ='0'

        video_coin = response.xpath('//div[@class="ops"]/span[@class="coin"]/text()').get()
        if video_coin:
            if isinstance(video_coin, int):
                item['video_coin'] = video_coin
            else:
                item['video_coin'] = video_coin.replace('\n', '').replace('\r', '').replace(' ', '')
        else:
            item['video_coin'] ='0'
        video_collect = response.xpath('//div[@class="ops"]/span[@class="collect"]/text()').get()
        if video_collect:
            if isinstance(video_collect, int):
                item['video_collect'] = video_collect
            else:
                item['video_collect'] = video_collect.replace('\n', '').replace('\r', '').replace(' ', '')
        else:
            item['video_collect'] ='0'
        video_share = response.xpath('//div[@class="ops"]/span[@class="share"]/text()').get()
        if video_share:
            if isinstance(video_share, int):
                item['video_share'] = video_share
            else:
                item['video_share'] = video_share.replace('\n', '').replace('\r', '').replace(' ', '')
        else:
            item['video_share'] ='0'
        video_comment = response.xpath('//span[@class="b-head-t results"]/text()').get()
        if video_comment:
            if isinstance(video_comment, int):
                item['video_comment'] = video_comment
            else:
                item['video_comment'] = video_comment.replace('\n', '').replace('\r', '').replace(' ', '')
        else:
            item['video_comment'] ='0'
        video_read = response.xpath('//span[@class="view"]/text()').get()
        if video_read:
            if isinstance(video_read, int):
                item['video_read'] = video_read
            else:
                item['video_read'] = video_read.replace('\n', '').replace('\r', '').replace(' ', '')
        else:
            item['video_read'] ='0'

        ctime=  response.xpath('//div[@class="video-data"]/span[last()]/text()').get().replace('\n', '').replace('\r', '')
        # 对异常进行捕获，若异常则默认设为当前的时间
        # try:
        #     create_date = datetime.datetime.strptime(ctime, "%Y/%m/%d").date()
        # except Exception as e:
        #     create_date = datetime.datetime.now().date()
        item['video_time'] = ctime
        oid = response.xpath('//meta[@itemprop="url"]/@content').get()
        video_oid = re.findall(r'\d+',oid) #compile TypeError: unsupported operand type(s) for &: 'str' and 'int'
        item['video_oid'] = video_oid
        yield item
        api = 'https://api.bilibili.com/x/v2/reply?&jsonp=jsonp&type=1&oid={}&sort=2&pn=1'.format(video_oid[0])
        time.sleep(6)
        yield scrapy.Request(url=api, callback=self.parse_comments, dont_filter=True)




    def parse_comments(self,response):
        #comment
        obj = json.loads(response.text)
        page = obj['data']['page']['acount']
        now = obj['data']['page']['num']
        list = obj['data']['replies']
        for comment in list:
            item = CommentItem()

            comment_zan = comment['like']
            if comment_zan:
                if isinstance(comment_zan,int):
                    item['comment_zan'] = comment_zan
                else:
                    item['comment_zan'] = comment_zan.replace('\n', '').replace('\r', '').replace(' ', '')
            else:
                item['comment_zan'] = '0'
            comment_reply = comment['rcount']

            if comment_reply:
                if isinstance(comment_reply,int):
                    item['comment_reply'] = comment_reply
                else:
                    item['comment_reply'] = comment_reply.replace('\n', '').replace('\r', '').replace(' ', '')
            else:
                item['comment_reply'] = '0'

            content= comment['content']['message'].replace('\n', '').replace('\r', '').replace(' ', '')
            replies = comment['replies']
            reply_content=""
            if replies:
                for reply in replies:
                    reply_content += reply['content']['message'].replace('\n', '').replace('\r', '').replace(' ', '')
            item['comment_content']=content +reply_content

            comment_level = comment['member']['level_info']['current_level']
            if isinstance(comment_level, int):
                item['comment_level'] = comment_level
            else:
                item['comment_level'] = comment_level.replace('\n', '').replace('\r', '').replace(' ', '')

            comment_oid = comment['oid']
            if isinstance(comment_oid, int):
                item['comment_oid'] = comment_oid
            else:
                item['comment_oid'] = comment_oid.replace('\n', '').replace('\r', '').replace(' ', '')

            item['sex'] = comment['member']['sex'].replace('\n', '').replace('\r', '').replace(' ', '')

            ctime = comment['ctime']
            timeArray = time.localtime(ctime)
            otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            # try:
            #     create_date = datetime.datetimestrptim.e(otherStyleTime, "%Y/%m/%d").date()
            # except Exception as e:
            #     create_date = datetime.datetime.now().date()
            item['ctime'] = ctime
            item['comment_time'] =  otherStyleTime
            yield item
            print(item)
        if int(now) <= int(page)/20:
            apix = 'https://api.bilibili.com/x/v2/reply?&jsonp=jsonp&type=1&oid={}&sort=2&pn='.format(comment['oid'])
            api = apix + str(int(now)+1)
            yield scrapy.Request(url=api, callback=self.parse_comments, dont_filter=True)




    def close(self,spider):
        # 当爬虫结束之后，调用关闭浏览器方法
        print('爬虫整体结束~~~~~~~~~~~~~~~~~~~')
        self.bro.quit()