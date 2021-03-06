#!usr/bin/python
# -*- coding:utf-8 -*-
"""
@author:shenchen
@file: spider2
@time: 2018/11/19
"""

import requests
import random
from lxml import etree
from django.conf import settings
import re
import urllib.request
import urllib.parse
import os
import time
import json
from user.models import *
from index.models import *

USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5"
]

headers = {
    "Cookie": "JSESSIONID=ABAAABAAAFCAAEG6030A9EEED05C0E5EA2D3785F76C5BC7; _ga=GA1.2.272369013.1542555584; user_trace_token=20181118233944-2c173783-eb48-11e8-8956-5254005c3644; LGUID=20181118233944-2c173b92-eb48-11e8-8956-5254005c3644; _gid=GA1.2.138802209.1542555585; index_location_city=%E5%85%A8%E5%9B%BD; TG-TRACK-CODE=index_hotsearch; SEARCH_ID=486745db98794718bb8a11f1e6fbba73; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1542555584,1542556551; X_HTTP_TOKEN=503aee9bc0a6fc9800603de25634804c; LGSID=20181119013432-35b81455-eb58-11e8-a693-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fpassport.lagou.com%2Flogin%2Flogin.html%3Fmsg%3Dvalidation%26uStatus%3D2%26clientIp%3D124.64.225.29; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216727e362c266e-0032caea2d13ca-35667407-1024000-16727e362c36ce%22%2C%22%24device_id%22%3A%2216727e362c266e-0032caea2d13ca-35667407-1024000-16727e362c36ce%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; LGRID=20181119013959-f889f22e-eb58-11e8-a693-525400f775ce; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1542562799" ,
    "Host": "www.lagou.com",
    "Upgrade-Insecure-Requests": "1",
    'Origin': "https://www.lagou.com",
    'User-Agent': '{0}'.format(random.sample(USER_AGENT_LIST, 1)[0]),
}


class GaLouPosition:
    def __init__(self, url: str):
        self.url = url

    def complete_position_info(self):
        i=1
        positions = PositionInfo.objects.all()
        for position in positions:
            # print(i)
            # i+=1
            tags_list = []
            desc_list = []
            url =''
            new_url = self.url.format(position.id)
            content = requests.get(new_url, headers=headers).text
            html = etree.HTML(content)
            # tags = html.xpath('/html/body/div[2]/div/div[1]/dd/ul/li')
            # spans = html.xpath('//*[@id="job_detail"]/dd[2]/div')
            # urls = html.xpath('//*[@id="job_company"]/dd/ul/li[5]/a/@href')
            address = html.xpath('//*[@id="job_detail"]/dd[3]/div[1]/a')

            final_addr = ''
            for a in address[:-1]:
                if a.text is not None:
                    final_addr+=a.text
                if a.tail is not None:
                    final_addr+=a.tail.strip()
                # city = a[0].text
                # distict = a[1].text
                # addr = a[1].tail.strip()
                # final_addr = city+' - '+distict+addr
            # b = address[-2].tail.strip()
            position.address = final_addr
            position.save()
            print(final_addr)
            print(position.id)



            # for tag in tags:
            #     tags_list.append(tag.text.strip())
            #
            # tag_str = ','.join(tags_list)
            #
            # for span in spans:
            #     ps = span.xpath('./p')
            #     if ps:
            #         for p in ps:
            #             if p.text and len(p.text) > 10:
            #                 desc_list.append(p.text)
            #             else:
            #                 brs = p.xpath('./br')
            #                 if brs:
            #                     for br in brs:
            #                         if br is not None:
            #                             if br.tail is not None:
            #                               desc_list.append(br.tail)
            #     else:
            #         desc_list.append(span.text)
            # desc_str = '=='.join(desc_list)
            #
            # if len(urls)>0:
            #     url = urls
            # position.tags = tag_str
            # if len(desc_str) < 1000:
            #     position.desc = desc_str
            # else:
            #     position.desc = desc_str[:1000]
            # position.org.url = url
            # position.save()
            # print(tag_str)
            # print(desc_str)
            # print(url)
            print("*"*80)
