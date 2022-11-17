# !/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from data.bi_qu_ge.puller import BiQuPuller


class NovelService(object):
    def __init__(self):
        self.puller = None
        self.init_puller()

    def init_puller(self):
        with BiQuPuller() as puller:
            self.puller = puller

    def get_book_by_name(self, book_name):
        book, catalog = self.puller.get_book_by_name(book_name)
        return {'book': book, 'catalogs': catalog.catalogs}

    def get_book_by_id(self, bid):
        book, catalog = self.puller.get_book_by_id(bid)
        return {'book': book, 'catalogs': catalog.catalogs}

    def get_chapter(self, bid, cid):
        return self.puller.get_book_chapter(bid, cid)


if __name__ == '__main__':
    book = NovelService().get_book_by_name('择日飞升')
    print(book)
