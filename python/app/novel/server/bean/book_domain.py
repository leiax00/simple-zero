# !/usr/bin/env python
# -*- coding: utf-8 -*-
import re

import pypinyin

from extender.serial_extender import Serialize


class IBook(Serialize):
    def to_dict_4_redis(self):
        # 保证只有第一级可以反序列化为字典, 第二级对象为字符串
        return self.__dict__

    def with_params(self, **kwargs):
        self.__dict__ = {**self.__dict__, **kwargs}
        return self


class Book(IBook):
    def __init__(self, **kwargs):
        self.bid = ''
        self.icon = b''
        self.name = ''
        self.icon = ''
        self.author = ''
        self.type = ''
        self.update_time = 0
        self.latest_chapter = ''
        self.desc = ''
        self.__dict__ = {**self.__dict__, **kwargs}
        self.pinyin_name = self.get_pinyin_name()

    def get_pinyin_name(self):
        pinyin_name = '_'.join([item[0] for item in pypinyin.pinyin(self.name, style=pypinyin.NORMAL)])
        return re.sub(r'[^\w\d]+', '', pinyin_name)


class BookCatalog(IBook):
    def __init__(self, **kwargs):
        self.bid = ''
        self.catalogs: list[BookChapterBase] = []
        self.__dict__ = {**self.__dict__, **kwargs}


class BookChapterBase(IBook):
    def __init__(self, **kwargs):
        self.bid = ''
        self.cid = ''
        self.name = ''
        self.__dict__ = {**self.__dict__, **kwargs}

    def is_none(self):
        return self.bid == ''


class BookChapter(BookChapterBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.content = ''
        self.prev = ''
        self.next = ''
        self.__dict__ = {**self.__dict__, **kwargs}


if __name__ == '__main__':
    name = '_'.join([item[0] for item in pypinyin.pinyin('你好, 李焕英', style=pypinyin.NORMAL)])
    print(re.sub(r'[^\w\d]+', '', name))
