#!usr/bin/python
#-*- coding:utf-8 -*-
"""
@author:shenchen
@file: utils
@time: 2018/11/21
"""
import datetime


def guess_your_love(positions,city,type,start_salary,end_salary):

    for position in positions:

        now = datetime.datetime.now()
        post_time = position.create_datetime
        timedelta = (now - post_time).days


        tags = position.org.tags.split(',')[:3]
        position.org.tags = tags

        point = 0
        if position.city == city:
            point +=34
        if position.type == type:
            point += 28
        if int(position.start_salary) > end_salary:
            point += 35
        if int(position.start_salary) > start_salary:
            point += 29
        position.point = point
        position.timedelta = timedelta