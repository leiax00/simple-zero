# !/usr/bin/env python
# -*- coding: utf-8 -*-
from conf.source import mongo_ct


class NovelService(object):
    def __init__(self, db=None):
        self.novel = db or mongo_ct

    def get_book_list(self):
        iters = self.novel['books'].find()
        return [item for item in iters]

    def get_book_by_id(self, bid):
        book = self.novel['books'].find_one({'bid': bid})
        catalogs = self.novel[f'catalog_{bid}'].find()
        book['catalog'] = [item for item in catalogs]
        return book

    def get_catalog_by_bid(self, bid):
        catalogs = self.novel[f'catalog_{bid}'].find()
        return [item for item in catalogs]

    def get_chapter_by_cid(self, bid, cid):
        chapter = self.novel[f'chapter_{bid}'].find_one({'cid': cid})
        return chapter


if __name__ == '__main__':
    service = NovelService()
    book_list = service.get_book_list()
    for item1 in book_list:
        print(item1)
