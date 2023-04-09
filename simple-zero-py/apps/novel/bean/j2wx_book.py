# !/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

from peewee import *
from playhouse.postgres_ext import ArrayField

from bean.base import BaseModel
from utils.common_utils import to_camel_dict

""" 晋江文学 - 数据统计相关bean """


class J2Book(BaseModel):
    id = CharField(max_length=32, primary_key=True)
    name = CharField()
    author_id = CharField(max_length=32)
    author_name = CharField()
    cover = CharField()
    size = IntegerField()
    type = CharField()
    tags = CharField()
    status = CharField()

    def __hash__(self):
        return hash(f'{self.id}')

    def __eq__(self, other):
        return self.id == other.id

    class Meta:
        table_name = 'j2wx_book'


class J2Rank(BaseModel):
    rank_id = CharField(max_length=32, primary_key=True)
    channel_key = CharField()
    rank_name = CharField()
    type = CharField(max_length=32)

    def __hash__(self):
        return hash(f'{self.rank_id}')

    def __eq__(self, other):
        return self.rank_id == other.rank_id

    class Meta:
        table_name = 'j2wx_rank'


class J2Stat(BaseModel):
    id = CharField(max_length=32)
    time = DateTimeField()
    channel_key = CharField()
    favorite_count = IntegerField(default=0)
    ticket_count = IntegerField(default=0)
    chapter_count = IntegerField(default=0)
    newest_date = DateTimeField()

    def __hash__(self):
        return hash(f'{self.id}:{self.time}')

    def __eq__(self, other):
        return self.id == other.id and self.time == other.time

    class Meta:
        table_name = 'j2wx_stat'
        primary_key = CompositeKey('id', 'time')


class J2RankStat(BaseModel):
    id = CharField(max_length=32)
    time = DateTimeField()
    channel_key = CharField()
    novel_ids = ArrayField(CharField)

    def to_map(self):
        rank_mapping = {}
        for score in range(len(list(self.novel_ids))):
            rank_mapping[self.novel_ids[score]] = score + 1
        return rank_mapping

    class Meta:
        table_name = 'j2wx_rank_stat'
        primary_key = CompositeKey('id', 'time')


class J2StatDto:
    def __init__(self):
        self.time = datetime.datetime.now()
        self.score = 0
        self.favorite_count = 0
        self.ticket_count = 0

    def with_param(self, stat: J2Stat = None, score: int = 0):
        if stat is not None:
            self.time = stat.time
            self.favorite_count = stat.favorite_count
            self.ticket_count = stat.ticket_count
        self.score = score
        return self


class J2Data:
    def __init__(self):
        self.book = J2Book()
        self.stat_list: [J2StatDto] = []

    def with_param(self, book: J2Book, stat_list: list[J2StatDto] = None):
        if stat_list is None:
            stat_list = []
        self.book = book
        self.stat_list = stat_list
        return self

    def to_camel_dict(self):
        tmp = {
            'book': self.book.to_camel_dict(),
            'stat_list': [item.__dict__ for item in self.stat_list]
        }
        return to_camel_dict(tmp)


class J2RankDto:
    def __init__(self,
                 rank_id: str = '',
                 rank_name: str = '',
                 rank_type: str = '',
                 novel_ids: list[str] = None
                 ):
        self.rank_id = rank_id
        self.rank_name = rank_name
        self.rank_type = rank_type
        self.novel_ids = novel_ids or []
