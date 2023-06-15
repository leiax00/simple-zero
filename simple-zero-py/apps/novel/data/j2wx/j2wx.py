# !/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import json
import logging
import re

import aiohttp
import pypinyin
import requests

from bean.j2wx_book import J2RankDto, J2Rank
from data.j2wx import constructor
from data.j2wx.j2wx_parser import Collector
from utils.async_utils import get_loop
from utils.httpHelper import Api, HttpMethod


class J2wxApiManager:

    def __init__(self):
        self.domain = 'https://app-cdn.jjwxc.com'
        self.version = 10
        self.versionCode = 287
        self.base_header = {
            'Referer': f'http://android.jjwxc.net?v={self.versionCode}',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 12; Mi 10 Pro Build/SKQ1.211006.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/108.0.5359.128 Mobile Safari/537.36/JINJIANG-Android/287(Mi10Pro;Scale/2.75)',
            'Accept-Encoding': 'gzip, deflate',
        }

    def get_channel_home(self, channel_key):
        return Api(f'bookstore/getFullPageV1', HttpMethod.GET, self.domain).get_request_params(params={
            'channel': channel_key,
            'version': self.version
        })

    def get_channel_rank(self, rank_id, offset=0, limit=50):
        return Api(f'bookstore/getFullPageV1', HttpMethod.GET, self.domain).get_request_params(params={
            'channelBody': f'{{"{rank_id}":{{"offset":"{offset}","limit":"{limit}"}}}}',
            'channelMore': 1
        }, headers=self.base_header)

    def get_novel_base_info(self, novel_id):
        return Api(f'/androidapi/novelbasicinfo', HttpMethod.GET, self.domain).get_request_params(params={
            'novelId': novel_id
        }, headers={
            **self.base_header,
            'reload': 'true',
            'cacheShowed': 'true',
        })

    def get_novel_stat(self, novel_id):
        return Api(f'/androidapi/getnovelOtherInfo', HttpMethod.GET, self.domain).get_request_params(params={
            'versionCode': self.versionCode,
            'novelId': novel_id,
            'type': 'novelbasicinfo'
        }, headers={
            **self.base_header,
            'VERSIONTYPE': 'reading',
            'versiontype': 'reading',
            'source': 'android',
            'versionCode': f'{self.versionCode}',
            'Version-Code': f'{self.versionCode}',
        })


api = J2wxApiManager()


class J2wxPuller:
    def __init__(self):
        self.api = api
        self.channel_key = 'gywx'
        self.collector = Collector()

        self.lock = asyncio.Lock()
        self.loop = None

    def pull(self, channel_key):
        self.loop = get_loop()
        self._set_channel_key(channel_key)
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

    def pull_novel_info_by_batch(self, channel_key, novel_ids):
        async def async_pull():
            async with aiohttp.ClientSession() as session:
                semaphore = asyncio.Semaphore(10)
                tasks = []
                for novel_id in novel_ids:
                    tasks.append(self.pull_novel_info(session, semaphore, novel_id))
                await asyncio.gather(*tasks)

        self._set_channel_key(channel_key)
        self.loop = get_loop()
        self.loop.run_until_complete(asyncio.wait([self.loop.create_task(async_pull())]))
        self.loop.close()
        return self.collector

    def _set_channel_key(self, channel_key):
        if channel_key is not None:
            self.channel_key = channel_key

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
                        # 自然榜的数据
                        rank_name = f"{item1.get('channelName', '')}({'连载' if t == 'serial' else '完结'}.自然)"
                        rank_id = item1.get('channelMoreId', '')
                        tmps.append(J2RankDto(rank_id, rank_name, rank_type))
                        # 首页数据中的榜单数据
                        rank_name_2 = f"{item1.get('channelName', '')}({'连载' if t == 'serial' else '完结'})"
                        tmps.append(J2RankDto(self.get_pinyin_name(rank_name_2), rank_name_2, rank_type,
                                              [item2.get('novelId') for item2 in item1.get('data', [])]))
            elif rank_type == 'rankings':
                for item in data.get('data'):
                    rank_name = item.get('channelName', '')
                    rank_id = item.get('more').get('channelMoreId', '')
                    # 首页数据中的榜单数据
                    tmps.append(
                        J2RankDto(self.get_pinyin_name(rank_name), rank_name, rank_type,
                                  [item1.get('novelId') for item1 in item.get('list', [])])
                    )
                    if rank_id != '':
                        # 自然榜的数据
                        tmps.append(J2RankDto(rank_id, f'{rank_name}.自然', rank_type))
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
        retry = 3
        while retry > 0:
            try:
                async with semaphore:
                    stat_p = self.api.get_novel_stat(novel_id)
                    stat_resp = await session.request(**stat_p, ssl=False)
                    stat_data = await stat_resp.text()
                    stat_data = json.loads(stat_data)
                    params = self.api.get_novel_base_info(novel_id)
                    resp = await session.request(**params, ssl=False)
                    data = await resp.text()
                    data = json.loads(data)
                    book = constructor.construct_j2book(data, novel_id)
                    if book is None:
                        continue
                    async with self.lock:
                        self.collector.novel_list.add(book)
                        stat_info = constructor.construct_j2stat(
                            data,
                            stat_data,
                            self.collector.now,
                            self.channel_key,
                            novel_id
                        )
                        self.collector.stat_list.add(stat_info)
                    if retry < 3:
                        logging.info(f'retry to pull novel: {novel_id} success')
                    logging.info(book.to_camel_dict())
                    logging.info(stat_info.to_camel_dict())
                    break
            except Exception as e:
                retry -= 1
                logging.error(f'Failed to get novel info, id: {novel_id}, remaining retry_count: {retry}, err: {e}',
                              stack_info=True, exc_info=True)
        else:
            logging.error(f'Failed to get novel info, id: {novel_id}')

    @staticmethod
    def get_pinyin_name(name):
        pinyin_name = '_'.join([item[0] for item in pypinyin.pinyin(name, style=pypinyin.NORMAL)])
        return re.sub(r'[^\w\d]+', '', pinyin_name)

    def pull_novel_base_info(self, novel_ids):
        novels = []
        with requests.session() as req:
            for novel_id in novel_ids:
                resp = requests.request(**self.api.get_novel_base_info(novel_id))
                data = resp.json()
                book = constructor.construct_j2book(data, novel_id)
                if book is None:
                    continue
                novels.append(book)
        return novels


j2wx_puller = J2wxPuller()

if __name__ == '__main__':
    import os

    os.chdir(os.path.join(os.path.dirname(__file__), '../..'))
    J2wxPuller().pull('gywx')
