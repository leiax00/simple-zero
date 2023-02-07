# !/usr/bin/env python
# -*- coding: utf-8 -*-
import re

import pypinyin
from playhouse.shortcuts import dict_to_model

from bean import book_db
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

    def to_db(self) -> book_db.Book:
        return dict_to_model(book_db.Book, self.__dict__)


class BookCatalog(IBook):
    def __init__(self, **kwargs):
        self.bid = ''
        self.catalogs: list[BookChapterBase] = []
        self.__dict__ = {**self.__dict__, **kwargs}

    def to_db(self) -> list[book_db.BookCatalog]:
        tmp = []
        count = len(self.catalogs)
        for i in range(count):
            item = self.catalogs[i].to_db()
            if i > 0:
                item.prev_cid = self.catalogs[i - 1].cid
            if i < count - 1:
                item.next_cid = self.catalogs[i + 1].cid
            tmp.append(item)
        return tmp


class BookChapterBase(IBook):
    def __init__(self, **kwargs):
        self.bid = ''
        self.cid = ''
        self.name = ''
        self.__dict__ = {**self.__dict__, **kwargs}

    def is_none(self):
        return self.bid == ''

    def to_db(self) -> book_db.BookCatalog:
        return dict_to_model(book_db.BookCatalog, self.__dict__)


class BookChapter(BookChapterBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.content = ''
        self.prev = ''
        self.next = ''
        self.__dict__ = {**self.__dict__, **kwargs}


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
