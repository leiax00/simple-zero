# !/usr/bin/env python
# -*- coding: utf-8 -*-
import abc
import asyncio
import datetime
import re

import httpx
from bs4 import BeautifulSoup
from sqlalchemy import and_
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
from starlette import status

from modules.novel.internal import service
from modules.novel.internal.entity import schema, models
from szpy import utils, constants
from szpy.config.app_config import app_conf
from szpy.config.data_source import ProxyConfig
from szpy.modules.db import sqlalchemy


class BookEngine:
    """
    小说的解析引擎
    """
    source: schema.CrawlSourceVO
    bids: set[str] = {}
    proxy_index: int = 0
    origin_data: dict = {}  # 原始数据集, url: data, 便于原始数据共享

    def __init__(self, source: schema.CrawlSourceVO, bids: set[str] = None):
        self.source = source
        self.bids = bids or {}
        self.proxy_index = 0

    def proxy_conf(self) -> ProxyConfig:
        if app_conf.proxy is None:
            return ProxyConfig(**{"maxThreadCount": 1, "maxRetryCount": 3, "retryPeriod": 2})
        return app_conf.proxy

    def proxy(self, url: str):
        proxy_conf = self.proxy_conf()
        self.proxy_index, req_proxy = proxy_conf.req_proxy(self.proxy_index)
        return req_proxy

    async def add_data(self, url: str, data):
        async with asyncio.Lock():
            self.origin_data[url] = data

    async def release(self):
        async with asyncio.Lock():
            self.origin_data = {}
            self.proxy_index = 0

    async def parse(self):
        """ engine解析入口 """
        rule = self.source.crawl_rule
        for bid in self.bids:
            print(f'{datetime.datetime.now()} -- start to pull book: {bid}')
            book_info = await self.parse_info(rule.info, bid)
            if book_info is None:
                continue
            print(f'{datetime.datetime.now()} -- start to pull book index: {bid}')
            index_list = await self.parse_index(rule.index, bid)
            if index_list is None:
                continue
            print(f'{datetime.datetime.now()} -- start to pull book content: {bid}')
            content_list = await self.parse_content(rule.content, bid, index_list)
            print(f'{datetime.datetime.now()} -- end to pull book: {bid}')
        await self.release()

    async def parse_info(self, rule: schema.ItemRule, bid):
        data = await self.get_html(rule, bid)
        if data is not None:
            html_parser = self.get_html_parser()
            return await InfoDataParser().with_bid(bid).with_html_parser(html_parser).parse(rule, data)
        print(f'Rule: {self.source.id}, Failed to get book: {bid} information')
        return None

    async def parse_index(self, rule: schema.ItemRule, bid):
        data = await self.get_html(rule, bid)
        if data is not None:
            html_parser = self.get_html_parser()
            return await IndexDataParser().with_bid(bid).with_html_parser(html_parser).parse(rule, data)
        print(f'Rule: {self.source.id}, Failed to get book: {bid} index information')
        return None

    async def parse_content(self, rule: schema.ItemRule, bid, index_list):
        with sqlalchemy.client.context() as db:  # type: Session
            has_pulled_ids = service.has_pulled_content_ids(bid, db)
            need_pulled = set([item.get('index_num') for item in index_list]) - has_pulled_ids

        print(f'Need to pull content count: {len(need_pulled)}, list: {need_pulled}')
        html_parser = self.get_html_parser()

        semaphore = asyncio.Semaphore(self.proxy_conf().maxThreadCount)

        async def fn(cid):
            async with semaphore:
                print(f'Processing pull content:{bid}-{cid}')
                data = await self.get_html(rule, bid, cid)
                if data is not None:
                    return await ContentDataParser().with_bid(
                        bid
                    ).with_cid(
                        cid
                    ).with_html_parser(
                        html_parser
                    ).parse(rule, data)

        tasks = [fn(index) for index in need_pulled]
        content_list = [x for x in await asyncio.gather(*tasks) if x is not None]

        return content_list

    async def get_html(self, rule: schema.ItemRule, bid, cid=None):
        async def fn():
            d, ok = None, False
            try:
                proxy = self.proxy(url)
                async with httpx.AsyncClient(base_url=self.source.crawl_rule.domain, proxies=proxy) as c:
                    resp = await c.get(url=url)
                    if resp.status_code == status.HTTP_200_OK:
                        d, ok = resp.text, True
            except Exception as e:
                pass
            return d, ok

        url = rule.url.replace('{bid}', bid)
        if cid is not None:
            url = url.replace('{cid}', cid)

        data = self.origin_data.get(url)
        if data is None:
            proxy_conf = self.proxy_conf()
            count = proxy_conf.maxRetryCount
            while count > 0:
                data, success = await fn()
                if success:
                    await self.add_data(url, data)
                    break

                count -= 1
                await asyncio.sleep(proxy_conf.retryPeriod)
                if count <= 0:
                    print(f'Failed to pull bid: {bid}, cid: {cid}')

        return data

    def get_html_parser(self):
        html_parser_map = {
            'bs': BSHtmlParser(),
            'xpath': XpathHtmlParser()
        }
        return html_parser_map.get(self.source.crawl_rule.parse_type)


class HtmlParser:
    @abc.abstractmethod
    async def deal(self, data, obj_rule: schema.ItemRule):
        pass

    # noinspection PyUnresolvedReferences
    @staticmethod
    def parse_data(field, val):
        if field.parser_type == schema.DataParserType.PATTERN.value:
            val = re.match(field.parser, val).group('val')
        if field.parser_type == schema.DataParserType.SCRIPT.value:
            exec(field.parser, globals())
            val = parse(val)  # parse方法定义在外部
        return val

    @staticmethod
    def get_selector_val(field_bs, attr_type: str):
        if attr_type == schema.AttrEnum.CONTENTS.value:
            return field_bs.contents
        if attr_type == schema.AttrEnum.TEXT.value:
            return field_bs.text
        return field_bs.get(attr_type)


class BSHtmlParser(HtmlParser):
    async def deal(self, data, obj_rule: schema.ItemRule):
        bs = BeautifulSoup(data, features='lxml')
        count = 1
        if obj_rule.root is not None:
            bs = bs.select(obj_rule.root)
            if obj_rule.rule_type == schema.SelectorType.UNIQUE.value:
                bs = bs[0]
            count = len(bs)

        rst = []
        if len(obj_rule.fields) > 0:

            async def parse_item(index):
                tmp = {}
                for field in obj_rule.fields:
                    if field.selector is None:
                        field_bs = bs if obj_rule.rule_type == schema.SelectorType.UNIQUE.value else bs[index]
                    else:
                        field_bs = bs.select(field.selector)[0]

                    val = self.get_selector_val(field_bs, field.attr)
                    tmp[field.field_name] = self.parse_data(field, val)
                return tmp

            tasks = [parse_item(i) for i in range(count)]
            rst = [x for x in await asyncio.gather(*tasks) if x is not None]
        return rst


class XpathHtmlParser(HtmlParser):
    async def deal(self, data, obj_rule: schema.ItemRule):
        pass


class DataParser:
    html_parser: HtmlParser
    bid = ''

    @abc.abstractmethod
    def parse(self, item: schema.ItemRule, data):
        raise NotImplementedError('Not Implemented!')

    def with_html_parser(self, parser: HtmlParser):
        self.html_parser = parser
        return self

    def with_bid(self, bid):
        self.bid = bid
        return self


class InfoDataParser(DataParser):
    async def parse(self, item: schema.ItemRule, data):
        info = (await self.html_parser.deal(data, item))[0]
        if info is not None:
            self.save(info)
        return info

    def save(self, info: dict):
        info['book_id'] = self.bid
        with sqlalchemy.client.context() as db:
            stmt = insert(models.Book).values(**info).on_conflict_do_update(
                index_elements=['book_id'],
                set_=info
            )
            db.execute(stmt)
            db.commit()


class IndexDataParser(DataParser):
    async def parse(self, item: schema.ItemRule, data):
        index_list = await self.html_parser.deal(data, item)
        if index_list is not None:
            self.save(index_list)
        return index_list

    def save(self, info: list[dict]):
        index_list = [{"book_id": self.bid, **item} for item in info]
        with sqlalchemy.client.context() as db:
            stmt = insert(models.BookIndex).values(index_list).on_conflict_do_nothing(
                index_elements=['book_id', 'index_num']
            )
            db.execute(stmt)
            db.commit()


class ContentDataParser(DataParser):
    cid = ''

    async def parse(self, item: schema.ItemRule, data):
        content = ''
        content_list = await self.html_parser.deal(data, item)
        if content_list is not None and len(content_list) > 0:
            content = utils.clean_content(content_list[0].get('content'))
        content_obj = {
            'content': content,
            'book_id': self.bid,
            'index_num': self.cid
        }
        self.save(content_obj)
        return content_obj

    def with_cid(self, cid):
        self.cid = cid
        return self

    def save(self, content_obj):
        with sqlalchemy.client.context() as db:  # type: Session
            stmt = insert(models.BookContent).values(content_obj).on_conflict_do_update(
                index_elements=['book_id', 'index_num'],
                set_={
                    "content": content_obj['content'],
                    "update_time": datetime.datetime.now()
                }
            )
            db.execute(stmt)

            if len(content_obj['content']) < 500:  # 认定为章节未解锁, 更新章节表
                db.query(models.BookIndex).filter(
                    and_(
                        models.BookIndex.book_id == self.bid,
                        models.BookIndex.index_num == self.cid
                    )
                ).update({'status': constants.BookIndexStatus.VIP.value})

            db.commit()
