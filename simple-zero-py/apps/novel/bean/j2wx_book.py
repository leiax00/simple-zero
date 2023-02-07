# !/usr/bin/env python
# -*- coding: utf-8 -*-

from peewee import *

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


class J2Channel(BaseModel):
    rank_id = CharField(max_length=32)
    channel = CharField(primary_key=True)
    type = CharField(max_length=32)
    more_id = CharField(max_length=32)

    def __hash__(self):
        return hash(f'{self.rank_id}:{self.channel}:{self.type}')

    def __eq__(self, other):
        return self.rank_id == other.rank_id and self.channel == other.channel and self.type == other.type

    class Meta:
        table_name = 'j2wx_channel'


class J2Stat(BaseModel):
    id = CharField(max_length=32)
    time = DateTimeField()
    favorite_count = IntegerField()
    ticket_count = IntegerField()

    def __hash__(self):
        return hash(f'{self.id}:{self.time}')

    def __eq__(self, other):
        return self.id == other.id and self.time == other.time

    class Meta:
        table_name = 'j2wx_stat'
        primary_key = CompositeKey('id', 'time')


class J2BookChannel(BaseModel):
    id = IntegerField(primary_key=True)
    novel_id = CharField(max_length=32)
    channel = CharField()

    def __hash__(self):
        return hash(f'{self.novel_id}:{self.channel}')

    def __eq__(self, other):
        return self.novel_id == other.novel_id and self.channel == other.channel

    class Meta:
        table_name = 'j2wx_book_channel'
