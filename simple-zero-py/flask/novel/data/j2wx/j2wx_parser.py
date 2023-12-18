# !/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import logging

from playhouse.shortcuts import model_to_dict

from bean.j2wx_book import *


class Collector:
    def __init__(self):
        self.now = datetime.datetime.now()
        self.channel_list = set([])
        self.novel_list = set([])
        self.stat_list = set([])
        self.mapping = {}  # { 'rank_id1': [...], 'rank_id2': [...] }

    def output(self):
        logging.info(f'{"=" * 40}开始输出解析结果{"=" * 40}')

        def output_set(data: set):
            for item in data:
                logging.info(f'{model_to_dict(item)}')

        output_set(self.channel_list)
        output_set(self.novel_list)
        output_set(self.stat_list)
        logging.info(self.mapping)
        logging.info(f'{"=" * 40}解析结果输出结束{"=" * 40}')


class CommonParser:
    def __init__(self, collector=Collector()):
        self.collector = collector

    def collect(self, data, channel_key):
        channel = J2Rank(
            rank_id=data.get('rankid'),
            rank_name=data.get('channelName'),
            channel_key=channel_key,
            type=data.get('type'),
        )
        if channel.id == '':
            return

        self.collector.channel_list.add(channel)
        tmp = data.get('data')
        rank_list = self.collector.mapping.get(channel.id, [])
        for item in tmp:
            self.collector.novel_list.add(J2Book(
                id=item.get('novelId'),
                name=item.get('novelname') or item.get('novelName'),
                author_id=item.get('authorId'),
                author_name=item.get('authorName'),
                cover=item.get('cover'),
                size=item.get('novelSize'),
                tags=item.get('tags'),
                type=item.get('novelClass'),
            ))
            self.collector.stat_list.add(J2Stat(
                id=item.get('novelId'),
                time=self.collector.now,
                channel_key=channel_key,
                favorite_count=item.get('novelbefavoritedcount'),
            ))
            rank_list.append(item.get('novelId'))
        self.collector.mapping[channel.id] = rank_list
        return self.collector

    def deal_novel(self, novel_list):
        pass

    def with_collector(self, collector: Collector):
        self.collector = collector
        return self


class J2wxParserFactory:
    def __init__(self):
        common_parser = CommonParser()
        self.parsers = {
            'default': common_parser,
            'img': common_parser,
            'text': common_parser,
            'taowen': common_parser,
        }

    def parser(self, channel_name='default', channel_type=None):
        if channel_type is None:
            return self.parsers.get(channel_name)
        return self.parsers.get(channel_type)
