# !/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import time

one_second = 1 * 1000
one_minute = 60 * one_second
one_hour = 60 * one_minute
one_day = 24 * one_hour


def now():
    return datetime.datetime.now()


def today_zero():
    """
    获取今日零点的时间
    :return:
    """
    now_date = now()
    return now_date - datetime.timedelta(
        hours=now_date.hour,
        minutes=now_date.minute,
        seconds=now_date.second,
        microseconds=now_date.microsecond
    )


def current_hour():
    """
    获取当前准点时间, 忽略分秒毫秒
    :return:
    """
    now_date = now()
    return now_date - datetime.timedelta(
        minutes=now_date.minute,
        seconds=now_date.second,
        microseconds=now_date.microsecond
    )


def datetime_2_num(date):
    return int(time.mktime(date.timetuple()) * 1000)


def format_datetime(date, time_formatter="%Y-%m-%d %H:%M:%S"):
    return date.strftime(time_formatter)


def format_time(time_num: int, time_formatter="%Y-%m-%d %H:%M:%S"):
    """
    毫秒值时间格式化
    """
    return time.strftime(time_formatter, time.localtime(time_num / 1000))


def parse_time(time_str, time_formatter="%Y-%m-%d %H:%M:%S"):
    """
    获取时间字符串的毫秒值
    """
    return int(time.mktime(time.strptime(time_str, time_formatter)) * 1000)


def parse_str_2_date(date_str, time_formatter="%Y-%m-%d %H:%M:%S"):
    """
    获取时间字符串的毫秒值
    """
    return datetime.datetime.strptime(date_str, time_formatter)


def compare_time_by_ymd(time1, time2=today_zero()):
    """
    通过年月日，比较时间，是否是同一天
    :param time1: 秒值
    :param time2: 秒值
    :return:
    """
    return 0 <= time1 - time2 < one_day


if __name__ == '__main__':
    print(datetime_2_num(now()))
    print(format_datetime(now()))
    print(format_time(1677120436 * one_second))
