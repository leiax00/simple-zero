# !/usr/bin/env python
# -*- coding: utf-8 -*-
import re

import unicodedata
from bs4 import BeautifulSoup

from bean.book_domain import Book, BookCatalog, BookChapterBase


class BiQuHtmlParser:
    def __init__(self, html: str = None):
        self.bid = -1
        self.html = html

    def with_html(self, html: str):
        self.html = html
        return self

    def get_book_id_by_search_rst(self):
        bs = BeautifulSoup(self.html, features='lxml')
        item = bs.select('table tr')[1]
        book_dict = {
            "bid": item.select('td>a')[0]['href'].strip('/\\'),
            "name": item.select('td>a')[0].string.strip(),
            # "icon": item.select('img.result-game-item-pic-link-img')[0]['src'],
            "author": item.select('td')[2].string,
            "update_time": item.select('td')[4].string,
            "latest_chapter": self.parse_chapter_item(item.select('td>a')[1]),
            # "desc": item.select('.result-game-item-desc')[0].string
        }
        self.bid = book_dict.get('bid', -1)
        return self.bid

    def parse_chapter_item(self, item):
        uri_infos = item['href'].rsplit('/', 2)
        if len(uri_infos) > 2:
            bid = uri_infos[1].strip()
            cid = re.match(r'([\d_]*).html', uri_infos[2]).group(1) if uri_infos[2] != '' else -1
        elif len(uri_infos) == 2:
            bid = self.bid if uri_infos[1] == '' else uri_infos[0]
            cid = re.match(r'([\d_]*).html', uri_infos[1]).group(1)
        elif len(uri_infos) == 1:
            bid = self.bid
            cid = re.match(r'([\d_]*).html', uri_infos[0]).group(1)
        else:
            bid = self.bid
            cid = -1
        return BookChapterBase(bid=bid, cid=cid, name=item.string)

    def parse_book_info(self):
        bs = BeautifulSoup(self.html, features='lxml')
        book = self.get_book(bs)
        catalog = self.get_catalog(bs)
        return book, catalog

    def get_book(self, bs):
        book_bs = bs.select('div#maininfo')[0]
        book_dict = {
            'bid': self.bid, 'name': book_bs.select('#info>h1')[0].string.strip(),
            'author': book_bs.select('#info>p')[0].string.split(':', 1)[1],
            'type': book_bs.select('#info>p')[1].string.split(':', 1)[1],
            'update_time': book_bs.select('#info>p')[2].string.split(':', 1)[1],
            'latest_chapter': self.parse_chapter_item(book_bs.select('#info>p')[3].select('a')[0]).cid,
            'desc': self.clean_content(book_bs.select('#intro>p')[0].contents),
            'icon': bs.select('div#fmimg>img')[0].get('src')
        }
        return Book(**book_dict)

    def get_catalog(self, bs):
        item_bs = bs.select('div.box_con dl dd>a')
        catalog_list = [self.parse_chapter_item(item) for item in item_bs]
        return BookCatalog(bid=self.bid, catalogs=catalog_list)

    def parse_book_chapter(self):
        bs = BeautifulSoup(self.html, features='lxml')
        chapter = {
            'name': bs.select('.bookname>h1')[0].string,
            'prev': self.parse_chapter_item(bs.select('.bookname .bottem1 a')[1]).cid,
            'next': self.parse_chapter_item(bs.select('.bookname .bottem1 a')[3]).cid,
            'content': self.clean_content(bs.select('div#content')[0].contents)
        }
        return chapter

    def clean_content(self, contents):
        tmp = []
        for item in contents:
            item = self.filter_by_keyword(item)
            if item is False:
                continue
            # 将\xa0、\u3000转为空格, 其他空格换行替换为空串
            tmp.append(unicodedata.normalize('NFKC', re.sub(r'[\s ]', '', item.__str__())))

        text = ''.join(tmp)
        if text.startswith('go'):
            text = text[2:]
        if text.endswith('over'):
            text = text[:-4]
        return re.sub(r'(<br/?>)+', '\n', text)

    @staticmethod
    def filter_by_keyword(obj):
        drop_list = ['爱阅小说app', '爱阅app']
        rep_list = ['Ｍ.bΙＱμＧètν.còＭ']
        for item in drop_list:
            if item in obj:
                return False
        for item in rep_list:
            if item in obj:
                return obj.__str__().replace(item, '')
        return obj


if __name__ == '__main__':
    # resp = requests.get('https://www.xbiquwx.la/files/article/image/4/4280/4280s.jpg')
    # print(resp.content)
    pass
