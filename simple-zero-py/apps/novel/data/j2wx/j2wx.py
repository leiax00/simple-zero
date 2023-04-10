# !/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import json
import logging
import re

import aiohttp
import pypinyin
import requests

from bean.j2wx_book import J2RankDto, J2Rank, J2Book, J2Stat
from data.j2wx.j2wx_parser import Collector
from utils.async_utils import get_loop
from utils.httpHelper import Api, HttpMethod
from utils.time_utils import parse_str_2_date


class J2wxApiManager:

    def __init__(self):
        self.domain = 'https://app-cdn.jjwxc.com'
        self.version = 10

    def get_channel_home(self, channel_key):
        return Api(f'bookstore/getFullPageV1', HttpMethod.GET, self.domain).get_request_params(params={
            'channel': channel_key,
            'version': self.version
        })

    def get_channel_rank(self, rank_id, offset=0, limit=50):
        return Api(f'bookstore/getFullPageV1', HttpMethod.GET, self.domain).get_request_params(params={
            'channelBody': f'{{"{rank_id}":{{"offset":"{offset}","limit":"{limit}"}}}}',
            'channelMore': 1
        })

    def get_novel_base_info(self, novel_id):
        return Api(f'/androidapi/novelbasicinfo', HttpMethod.GET, self.domain).get_request_params(params={
            'novelId': novel_id
        })


class J2wxPuller:
    def __init__(self):
        self.api = J2wxApiManager()
        self.channel_key = 'gywx'
        self.collector = Collector()

        self.lock = asyncio.Lock()
        self.loop = None

    def pull(self, channel_key):
        self.loop = get_loop()
        self.channel_key = channel_key
        with requests.request(**self.api.get_channel_home(channel_key), verify=False) as resp:
            data_list = resp.json().get('data')
        self.collector = Collector()
        items = []

        # items.extend(self.pull_rank(data_list[0]))
        for item in data_list:
            items.extend(self.pull_rank(item))

        self.loop.run_until_complete(asyncio.wait([self.loop.create_task(self.fill_novel_ids(items))]))
        self.loop.run_until_complete(asyncio.wait([self.loop.create_task(self.pull_novel(items))]))
        self.loop.close()
        return self.collector

    def pull_rank(self, data):
        tmps = []

        rank_id = data.get('channelMoreId', '').strip()
        rank_type = data.get('type')

        if rank_type == 'starauthor':
            return tmps

        if rank_id == '':
            if rank_type == 'eightgod':
                for item in data.get('data'):
                    t = item.get('channelName', '')
                    for item1 in item.get('list'):
                        rank_name = f"{item1.get('channelName', '')}({'连载' if t == 'serial' else '完结'})"
                        rank_id = item1.get('channelMoreId', '')
                        tmps.append(J2RankDto(rank_id, rank_name, rank_type))
            elif rank_type == 'rankings':
                for item in data.get('data'):
                    rank_name = item.get('channelName', '')
                    rank_id = item.get('more').get('channelMoreId', '')
                    if rank_id == '':
                        tmps.append(
                            J2RankDto(self.get_pinyin_name(rank_name), rank_name, rank_type,
                                      [item1.get('novelId') for item1 in item.get('list')])
                        )
                        continue
                    tmps.append(J2RankDto(rank_id, rank_name, rank_type))
            else:
                ran_name = data.get('channelName')
                rank_id = data.get('rankid', '')
                rank_id = rank_id if rank_id != '' else self.get_pinyin_name(ran_name)
                tmps.append(J2RankDto(rank_id, ran_name, rank_type,
                                      [item.get('novelId') for item in data.get('data')]))
                return tmps
        else:
            ran_name = data.get('channelName')
            tmps.append(J2RankDto(rank_id, ran_name, rank_type,
                                  [item.get('novelId') for item in data.get('data')]))

        return tmps

    async def fill_novel_ids(self, rank_list: list[J2RankDto]):

        semaphore = asyncio.Semaphore(10)
        async with aiohttp.ClientSession() as session:
            tasks = []
            for item in rank_list:
                if item.rank_id == '' or item.rank_id == self.get_pinyin_name(item.rank_name):
                    continue
                tasks.append(self.pull_rank_list(session, semaphore, item))
            await asyncio.gather(*tasks)

    async def pull_rank_list(self, session, semaphore, rank_dto: J2RankDto):
        async with semaphore:
            p = self.api.get_channel_rank(rank_dto.rank_id)
            async with session.request(**p, ssl=False) as r:
                text = await r.text()
                d1 = json.loads(text).get('data')
                ids = [t1.get('novelId') for t1 in d1.get('data', {})]
                if len(rank_dto.novel_ids) <= len(ids):
                    rank_dto.novel_ids = ids

    async def pull_novel(self, rank_list: list[J2RankDto]):
        semaphore = asyncio.Semaphore(10)
        async with aiohttp.ClientSession() as session:
            tasks = []
            novel_ids = []
            for rank_item in rank_list:
                self.collector.mapping[rank_item.rank_id] = rank_item.novel_ids
                self.collector.channel_list.add(J2Rank(
                    rank_id=rank_item.rank_id,
                    rank_name=rank_item.rank_name,
                    channel_key=self.channel_key,
                    type=rank_item.rank_type
                ))
                for novel_id in rank_item.novel_ids:
                    if novel_id in novel_ids:
                        continue
                    novel_ids.append(novel_id)
                    tasks.append(self.pull_novel_info(session, semaphore, novel_id))
            await asyncio.gather(*tasks)

    async def pull_novel_info(self, session, semaphore, novel_id):
        try:
            async with semaphore:
                params = self.api.get_novel_base_info(novel_id)
                resp = await session.request(**params, ssl=False)
                data = await resp.text()
                data = json.loads(data)
                async with self.lock:
                    self.collector.novel_list.add(J2Book(
                        id=novel_id,
                        name=data.get('novelName'),
                        author_id=data.get('authorId'),
                        author_name=data.get('authorName'),
                        cover=data.get('novelCover'),
                        size=int(data.get('novelSize', '0').replace(',', '')),
                        tags=data.get('novelTags'),
                        type=data.get('novelClass'),
                        status=data.get('novelStep')
                    ))
                    ticket = re.sub(r'\D', '', data.get('ranking', '0'))
                    favorite = re.sub(r'\D', '', data.get('novelbefavoritedcount', '0'))
                    chapter = re.sub(r'\D', '', data.get('novelChapterCount', '0'))
                    self.collector.stat_list.add(J2Stat(
                        id=novel_id,
                        time=self.collector.now,
                        channel_key=self.channel_key,
                        favorite_count=favorite if favorite != '' else 0,
                        ticket_count=int(ticket) if ticket != '' else 0,
                        chapter_count=chapter if chapter != '' else 0,
                        newest_date=parse_str_2_date(data.get('renewDate'))
                    ))
        except Exception as e:
            logging.error(f'Failed to get novel info, id: {novel_id}, err: {e}')

    @staticmethod
    def get_pinyin_name(name):
        pinyin_name = '_'.join([item[0] for item in pypinyin.pinyin(name, style=pypinyin.NORMAL)])
        return re.sub(r'[^\w\d]+', '', pinyin_name)


j2wx_puller = J2wxPuller()

if __name__ == '__main__':
    import os

    os.chdir(os.path.join(os.path.dirname(__file__), '../..'))
    J2wxPuller().pull('gywx')
