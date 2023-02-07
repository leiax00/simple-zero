# !/usr/bin/env python
# -*- coding: utf-8 -*-

from bean import book_db
from bean.book_domain import Book, BookCatalog
from data.bi_qu_ge import config
from utils.httpHelper import HttpSession, content


class BiQuPuller(object):
    def __init__(self):
        self.config = config

    def __enter__(self):
        self.client = HttpSession(self.config.domain)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.client is not None:
            self.client.close()

    def get_book_by_name(self, book_name):
        bid = self.get_book_id_by_name(book_name)
        book, catalog = self.get_book_by_id(bid)
        return book, catalog

    def get_book_by_id(self, bid) -> tuple[Book, BookCatalog]:
        param = self.config.APIS.catalog.value.get_request_params(book_id=bid)
        with self.client.request(**param) as resp:
            return self.config.parser.with_html(content(resp)).parse_book_info()

    def get_book_chapter(self, book_id, chapter_id):
        params = self.config.APIS.chapter.value.get_request_params(
            book_id=book_id,
            chapter_id=chapter_id
        )
        with self.client.request(**params) as resp:
            return self.config.parser.with_html(content(resp)).parse_book_chapter()

    def get_book_id_by_name(self, book_name):
        params = self.config.APIS.search.value.get_request_params(params={'searchkey': book_name})
        with self.client.request(**params) as resp:
            return self.config.parser.with_html(content(resp)).get_book_id_by_search_rst()

    def subscribe_book(self, bid, cid):
        tmp = book_db.Book.select().where(book_db.Book.bid == bid).first()
        if tmp is None:
            book, catalog = self.get_book_by_id(bid)
            db_book = book.to_db()
            db_catalogs = catalog.to_db()
        else:
            # 分组保存一条
            pass


if __name__ == '__main__':
    def main():
        with BiQuPuller() as puller:
            b, c = puller.get_book_by_name('择日飞升')
            print(b, c)
            ch = puller.get_book_chapter('4_4280', '34278231')
            print(ch)


    main()
