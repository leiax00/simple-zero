# !/usr/bin/env python
# -*- coding: utf-8 -*-
import re

import pypinyin
from peewee import *
from playhouse.postgres_ext import JSONField

from config import db
from extender.serial_extender import Serialize


class IBook(Serialize):
    def with_params(self, **kwargs):
        self.__dict__ = {**self.__dict__, **kwargs}
        return self


class Book(IBook):
    def __init__(self, **kwargs):
        self.bid = ''
        self.icon = ''
        self.name = ''
        self.author = ''
        self.type = ''
        self.update_time = 0
        self.latest_chapter = ''
        self.desc = ''
        self.__dict__ = {**self.__dict__, **kwargs}
        self.pinyin_name = self.get_pinyin_name()

    def get_pinyin_name(self):
        pinyin_name = '_'.join([item[0] for item in pypinyin.pinyin(self.name, style=pypinyin.NORMAL)])
        return re.sub(r'\W+', '', pinyin_name)


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


class DbBook(Model):
    bid = CharField(max_length=64, primary_key=True)
    name = CharField(max_length=128)
    author = CharField(max_length=128)
    type = CharField(max_length=32)
    icon = CharField(max_length=255)
    desc = TextField()
    update_time = CharField(max_length=64, column_name='update_time')
    last_read_chapter = JSONField(column_name='last_read_chapter')
    group_name = CharField(max_length=255, default='default')

    class Meta:
        database = db
        schema = 'novel'
        table_name = 'book'


if __name__ == '__main__':
    name = '_'.join([item[0] for item in pypinyin.pinyin('你好, 李焕英', style=pypinyin.NORMAL)])
    print(re.sub(r'\W+', '', name))
    # b = DbBook.create(bid='123', name='ass', author='dss', type='ddd', icon='fggg', desc='????',
    #                   update_time='2022-12-26T16:01', last_read_chapter={"cid": "dsdd", "name": "chapter"})
    # b.save()
    book = DbBook.select().where(DbBook.last_chapter['cid'] == 'dsdd').get()
    print(book.name)
    DbBook.delete().where(DbBook.bid == '1').execute()
    db.close()
