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
        self.mapping_list = set([])

    def output(self):
        logging.info(f'{"=" * 40}开始输出解析结果{"=" * 40}')

        def output_set(data: set):
            for item in data:
                logging.info(f'{model_to_dict(item)}')

        output_set(self.channel_list)
        output_set(self.novel_list)
        output_set(self.stat_list)
        output_set(self.mapping_list)
        logging.info(f'{"=" * 40}解析结果输出结束{"=" * 40}')


class CommonParser:
    def __init__(self, collector=Collector()):
        self.collector = collector

    def collect(self, data):
        channel = J2Channel(
            rank_id=data.get('rankid'),
            channel=data.get('channelName'),
            type=data.get('type'),
            more_id=data.get('channelMoreId'),
        )
        self.collector.channel_list.add(channel)
        tmp = data.get('data')
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
                favorite_count=item.get('novelbefavoritedcount'),
            ))
            self.collector.mapping_list.add(J2BookChannel(
                id=len(self.collector.mapping_list) + 1,
                novel_id=item.get('novelId'),
                channel=channel.channel,
            ))
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

    def parse(self, data_list) -> Collector:
        collector = Collector()
        for item in data_list:
            parser = self.parser(item.get('channelName'), item.get('type'))

            if parser is not None:
                parser.with_collector(collector).collect(item)
        return collector
