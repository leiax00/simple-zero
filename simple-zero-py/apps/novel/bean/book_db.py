# !/usr/bin/env python
# -*- coding: utf-8 -*-
from peewee import *
from playhouse.shortcuts import model_to_dict

from bean.base import BaseModel


class Book(BaseModel):
    bid = CharField(max_length=64, primary_key=True)
    name = CharField(max_length=128)
    author = CharField(max_length=128)
    type = CharField(max_length=32)
    icon = CharField(max_length=255)
    desc = TextField()
    update_time = CharField(max_length=64, column_name='update_time')
    group_name = CharField(max_length=255, default='default')


class BookCatalog(Model):
    id = IntegerField(primary_key=True)
    bid = CharField(max_length=64)
    cid = CharField(max_length=64)
    name = CharField()
    prev_cid = CharField(max_length=64)
    next_cid = CharField(max_length=64)


class BookChapter(Model):
    id = IntegerField(primary_key=True)
    content = TextField()


if __name__ == '__main__':
    b = Book()
    print(model_to_dict(b))
