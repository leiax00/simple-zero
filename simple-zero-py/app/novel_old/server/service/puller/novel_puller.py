# !/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import platform
import re
import time

import aiohttp
import pymongo
from aiohttp import ClientSession

from bean.book_domain import BookCatalog, BookChapter
from server.api import Api, Domain, ICookie, IApiManager, ApiMap, HttpMethod
from service.puller.html_parser import BiQuHtmlParser

Api.default_domain = Domain.BI_QU_GE


class Cookie(ICookie):

    def get_cookies(self):
        return {}


class ApiManager(IApiManager):
    def __init__(self):
        super().__init__()
        self.cookie = Cookie()
        self.apis = ApiMap()
        self.init_api_list()

    def init_api_list(self):
        api_map = {
            'search': Api('/modules/article/search.php', HttpMethod.GET),
            'book_catalog': Api('/{book_id}/', HttpMethod.GET),
            'book_chapter': Api('/{book_id}/{chapter_id}.html', HttpMethod.GET)
        }
        self.apis.with_dict(**api_map)

    def get_cookie(self):
        return self.cookie.get_cookies()


# noinspection PyBroadException
class NovelPuller(object):
    def __init__(self, mongo_source='mongodb://127.0.0.1:27017/'):
        self.apiManager = ApiManager()
        self.parser = BiQuHtmlParser()
        self.novel = pymongo.MongoClient(mongo_source)['py_novel']

    async def pull_by_batch(self, book_list):
        async def pull_single_book(signal, book_name):
            async with signal:
                await self.pull(book_name)

        semaphore = asyncio.Semaphore(10)
        tasks = []
        for book in book_list:
            await self.pull(book)
        #     tasks.append(asyncio.create_task(pull_single_book(semaphore, book)))
        # if len(tasks) > 0:
        #     await asyncio.wait(tasks)

    async def pull(self, book_name):
        # current_app.logger.info(f'start pull book --- {book_name}')
        async with aiohttp.ClientSession() as ac:
            bid = await self.search_book_by_name(ac, book_name)
            book, catalog = await self.get_book_info(ac, bid)
            self.save_book_info(book, catalog)
            await self.pull_chapter_detail(ac, catalog)

    async def search_book_by_name(self, client: ClientSession, book_name):
        search_params = self.apiManager.apis.search.get_request_params(params={'searchkey': book_name})
        async with client.request(**search_params) as resp:
            return self.parser.with_html(await resp.text()).get_book_id_by_search_rst()

    async def get_book_info(self, client, bid):
        params = self.apiManager.apis.book_catalog.get_request_params(book_id=bid)
        async with client.request(**params) as resp:
            return self.parser.with_html(await resp.text()).parse_book_info()

    def save_book_info(self, book, catalog):
        self.novel['name'].update_one(
            {'name': book.pinyin_name},
            {'$set': {'name': book.pinyin_name, 'bid': book.bid}},
            True
        )
        self.novel['books'].update_one(
            {'bid': book.bid},
            {'$set': book.to_dict_4_redis()},
            True
        )
        self.novel[f'catalog_{book.bid}'].drop()
        self.novel[f'catalog_{book.bid}'].insert_many([x.to_dict() for x in catalog.catalogs])

    async def pull_chapter_detail(self, client: ClientSession, catalog: BookCatalog):
        async def pull_content(signal, self_id, chapter):
            async with signal:
                start = int(round(time.time() * 1000))
                count = 3  # 增加三次重试次数
                while count > 0:
                    try:
                        params = self.apiManager.apis.book_chapter.get_request_params(
                            book_id=chapter.bid,
                            chapter_id=chapter.cid
                        )
                        async with client.request(**params) as resp:
                            infos = self.parser.with_html(await resp.text()).parse_book_chapter()
                            chapter.with_params(**infos)
                            self.novel[f'chapter_{chapter.bid}'].update_one(
                                {'cid': chapter.cid},
                                {'$set': {'order': self_id, **chapter.to_dict()}},
                                True
                            )
                            print(
                                f'pull content: {chapter.bid} --- {chapter.cid} --- {chapter.name} '
                                f'--- cost: {int(round(time.time() * 1000)) - start}'
                            )
                            break
                    except Exception as e:
                        count -= 1
                        time.sleep(2)
                else:
                    print(f'FAILED: pull content: {chapter.bid} --- {chapter.cid} --- {chapter.name}')

        def need_pull_detail(d: dict):
            d = d or {}
            c = d.get('content', '')
            n = d.get('name', '')
            return len(c) < 500 and re.match(r'.*第.*章.*', n) is not None

        semaphore = asyncio.Semaphore(20)
        order = 0
        tasks = []
        for item in catalog.catalogs:
            order += 1
            # 存在且内容长度超过500
            data = self.novel[f'chapter_{item.bid}'].find_one({'cid': item.cid})
            if need_pull_detail(data):
                tasks.append(asyncio.create_task(
                    pull_content(semaphore, order, BookChapter().with_params(**item.__dict__)))
                )
        if len(tasks) > 0:
            await asyncio.wait(tasks)


if __name__ == '__main__':
    if 'win' in platform.system().lower():
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    puller = NovelPuller()

    # asyncio.run(puller.pull('我的治愈系游戏'))
    asyncio.run(puller.pull_by_batch(['神印王座', '择日飞升']))
