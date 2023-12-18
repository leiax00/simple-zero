# !/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, BIGINT, VARCHAR, CHAR, SMALLINT
from sqlalchemy.dialects.postgresql import JSONB

from modules.novel.internal.entity.models.base import PGBase, Remark
from szpy.modules.db.sqlalchemy import SQLBase


class CrawlSource(SQLBase, PGBase, Remark):
    """ 小说爬虫源站表 """
    __table_args__ = {'schema': 'novel'}
    __tablename__ = 'crawl_source'

    id = Column(BIGINT, primary_key=True, index=True)
    source_name = Column(VARCHAR(64))
    crawl_rule = Column(JSONB)
    status = Column(CHAR(1), default='0')


class CrawlRecord(SQLBase, PGBase):
    """ 小说爬虫爬取记录表 """
    __table_args__ = {'schema': 'novel'}
    __tablename__ = 'crawl_record'

    id = Column(BIGINT, primary_key=True, index=True)
    source_id = Column(BIGINT)
    source_book_id = Column(BIGINT)
    status = Column(CHAR(1), default='0')
    exec_count = Column(SMALLINT)
    index_count = Column(SMALLINT)


class CrawlBook(SQLBase, PGBase):
    """ 爬虫源和小说原始ID的映射表 """
    __table_args__ = {'schema': 'novel'}
    __tablename__ = 'crawl_book'

    id = Column(BIGINT, primary_key=True, index=True)
    crawl_id = Column(BIGINT)
    book_id = Column(VARCHAR(24))
