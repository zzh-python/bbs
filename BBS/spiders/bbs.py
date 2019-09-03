# -*- coding: utf-8 -*-
import scrapy
import re
from BBS.items import BbsItem  #标红但没错


class BbsSpider(scrapy.Spider):
    name = 'bbs'
    allowed_domains = ['sgcn.com']
    start_urls = ['https://bbs.sgcn.com/forum.php?gid=1163']

    def parse(self, response):
        classify={ }
        text=response.xpath('//tr/td/h2/a/text()').extract()
        url = response.xpath('//tr/td/h2/a/@href').extract()
        if len(text)!=0 :
            for i,j in zip(text,url):
                classify[i]=j
            while True:
                name=input('请输入你要查找的分类 \n')
                try:
                    url=classify[name]
                    break
                except:
                    print('请输入正确的分类,所有分类如下')
                    print(classify.keys())

            yield scrapy.Request(url ,callback=self.parse)
        else:
            page = response.xpath('//label/span/text()').extract()
            page = re.search('(\d+)', page[0])
            page = page[0]
            page = int(page) + 1
            print(page)
            # 店家
            title = response.xpath('//tr/th[@class="new"]/a[2]/text()').extract()
            # 地址
            next_url = response.xpath('//tr/th[@class="new"]/a[2]/@href').extract()
            if len(title) == 0:
                # 店家
                title = response.xpath('//table/tbody/tr/th/a[2]/text()').extract()
                # 地址
                next_url = response.xpath('//table/tbody/tr/th/a[2]/@href').extract()

            restaurant = {}
            for i, j in zip(title, next_url):
                restaurant[i] = j
                yield scrapy.Request(j, callback=lambda response, title=i: self.get_phone_url(response, title))
            print(restaurant)
            # 翻页实现
            if re.search('-1\.', response.url) != None:
                for i in range(1, page):
                    new_page_url = re.sub('-1\.', '-' + str(i) + '.', response.url)
                    yield scrapy.Request(new_page_url, callback=self.parse)

    def get_phone_url(self,response,title):
        phone_photo=re.search( "<img src='\.(/code\.php\?.*?)' />" ,response.text)
        if phone_photo != None:
            phone_photo='https://bbs.sgcn.com'+phone_photo.group(1)
        item=BbsItem()
        item['title']=title
        item['photo_url']=phone_photo
        yield item
