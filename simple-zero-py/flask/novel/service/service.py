# !/usr/bin/env python
# -*- coding: utf-8 -*-
from bean.book_db import Book
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

    def subscribe_book(self, bid, cid=None):
        return self.puller.subscribe_book(bid, cid)

    def get_book_list(self, group_name):
        books = Book.select().where(Book.group_name == group_name)
        self.puller.fetch_book_list(books)

        return

    def update_bookshelf(self):
        pass


novel = NovelService()

if __name__ == '__main__':
    book = novel.get_book_by_name('择日飞升')
    print(book)
