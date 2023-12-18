# !/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, BIGINT, VARCHAR, TEXT, CHAR, INTEGER
from sqlalchemy.dialects.postgresql import TIMESTAMP

from szpy import constants
from szpy.modules.db.sqlalchemy import SQLBase
from .base import PGBase


class Book(PGBase, SQLBase):
    """
    PO: 书籍信息
    """
    __table_args__ = {'schema': 'novel'}
    __tablename__ = 'book'

    id = Column(BIGINT, primary_key=True, index=True)
    book_id = Column(VARCHAR(24))
    book_type = Column(VARCHAR(64))
    cover = Column(VARCHAR(255))
    book_name = Column(VARCHAR(64))
    author_id = Column(BIGINT)
    author_name = Column(VARCHAR(64))
    book_desc = Column(TEXT)
    finished = Column(CHAR(1), default='N')
    score = Column(VARCHAR(32))
    count = Column(BIGINT)
    word_count = Column(BIGINT)
    comment_count = Column(INTEGER)
    last_chapter_id = Column(BIGINT)
    last_chapter_name = Column(VARCHAR(64))
    last_chapter_time = Column(TIMESTAMP)
    sign_status = Column(CHAR(1), default='N')
    book_status = Column(CHAR(1))
    status = Column(CHAR, default='0')


class BookIndex(SQLBase, PGBase):
    __table_args__ = {'schema': 'novel'}
    __tablename__ = 'book_index'

    id = Column(BIGINT, primary_key=True, index=True)
    book_id = Column(VARCHAR(24))
    index_num = Column(VARCHAR(24))
    index_name = Column(VARCHAR(64))
    word_count = Column(INTEGER, default=0)
    status = Column(CHAR, default=constants.BookIndexStatus.FREE.value)


class BookContent(SQLBase, PGBase):
    __table_args__ = {'schema': 'novel'}
    __tablename__ = 'book_content'

    id = Column(BIGINT, primary_key=True, index=True)
    book_id = Column(VARCHAR(24))
    index_num = Column(VARCHAR(24))
    content = Column(TEXT)
