# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline
import requests
import time
from BBS.baiduApi import basicGeneralUrl #标红但没错
import json


class BbsPipeline(object):
    def process_item(self, item, spider):
        with open('E:\\untitled\\homework_spider\\text\\bbs.txt','a',encoding='utf-8') as fp :
            data=dict(item)
            for values in data.values():
                if type(values) == list:
                    for i in values:
                         fp.write(i+'\n')
                elif values ==None:
                    fp.write('None' + '\n')
                else:
                    fp.write(values+'\n')
        self.save_to_png(data)
        return item

    def save_to_png(self,data):
        headers={
            'Host': 'bbs.sgcn.com',
            'Referer': 'https://bbs.sgcn.com/forum.php?gid=1163',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }
        if data['photo_url'] != None and len(data['photo_url'] ) > 15:
            response=requests.get(data['photo_url'],headers=headers,timeout=5)
            print(data['photo_url'])
            if response.status_code ==200 :
                # t=int(time.time())
                # with open(f'E:\\untitled\\图片\\{data["title"]+str(t)+".png"}','wb')as f:
                #     f.write(response.content)
                self.recognition_numberi(data['photo_url'])
    #识别图片
    def recognition_numberi(self,url):
        num=basicGeneralUrl(url)
        #提取号码
        phonenum=num['words_result'][0]['words']
        with open('E:\\untitled\\homework_spider\\text\\bbsphone.txt','a',encoding='utf-8') as fp :
              fp.write(phonenum+'\n')

class BbsImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        data = dict(item)
        if data['photo_url'] != None:
                return scrapy.Request(data['photo_url'])
        else:
            print('none')
            pass

    def file_path(self, request, response=None, info=None):
        file_name=request.url.split('/')[-1]
        return 'BBS%s.png'%file_name




