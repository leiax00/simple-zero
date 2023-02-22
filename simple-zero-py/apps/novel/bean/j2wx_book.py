# !/usr/bin/env python
# -*- coding: utf-8 -*-

from peewee import *
from playhouse.postgres_ext import ArrayField

from bean.base import BaseModel

""" 晋江文学 - 数据统计相关bean """


class J2Book(BaseModel):
    id = CharField(max_length=32, primary_key=True)
    name = CharField()
    author_id = CharField(max_length=32)
    author_name = CharField()
    cover = CharField()
    size = IntegerField()
    tags = CharField()
    type = CharField()

    def __hash__(self):
        return hash(f'{self.id}')

    def __eq__(self, other):
        return self.id == other.id

    class Meta:
        table_name = 'j2wx_book'


class J2Rank(BaseModel):
    id = CharField(max_length=32, primary_key=True)
    rank_id = CharField(max_length=32)
    channel_key = CharField()
    rank_name = CharField()
    type = CharField(max_length=32)

    def __hash__(self):
        return hash(f'{self.id}')

    def __eq__(self, other):
        return self.id == other.id

    class Meta:
        table_name = 'j2wx_rank'


class J2Stat(BaseModel):
    id = CharField(max_length=32)
    time = DateTimeField()
    channel_key = CharField()
    favorite_count = IntegerField(default=0)
    ticket_count = IntegerField(default=0)

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

    class Meta:
        table_name = 'j2wx_rank_stat'
        primary_key = CompositeKey('id', 'time')
