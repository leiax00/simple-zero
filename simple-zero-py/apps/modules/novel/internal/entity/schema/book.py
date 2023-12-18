# !/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Optional

from fastapi import Query
from pydantic import Field, BaseModel

from modules.novel.internal.entity.schema.baseVo import BaseVO


class BookVO(BaseVO):
    id: Optional[int] = Field(default=None, description='主键ID')
    book_id: Optional[str] = Field(default=None, description='原始书籍ID')
    book_type: Optional[str] = Field(default=None, description='类别')
    cover: Optional[str] = Field(default=None, description='封面url')
    book_name: Optional[str] = Field(default=None, description='书籍名称')
    author_id: Optional[int] = Field(default=None, description='作者ID')
    author_name: Optional[str] = Field(default=None, description='作者名称')
    book_desc: Optional[str] = Field(default=None, description='书籍简介')
    finished: Optional[str] = Field(default='N', description='完结状态: N连载中, Y已完结', pattern='N|Y')
    score: Optional[str] = Field(default=None, description='评分')
    count: Optional[int] = Field(default=None, description='收藏数/点击量等')
    word_count: Optional[int] = Field(default=None, description='总字数')
    comment_count: Optional[int] = Field(default=None, description='评论数')
    last_chapter_id: Optional[int] = Field(default=None, description='最新章节ID')
    last_chapter_name: Optional[str] = Field(default=None, description='最新章节名称')
    last_chapter_time: datetime = Field(default=None, description='最新更新时间')
    sign_status: Optional[str] = Field(default='Y', description='签约状态: N未签约, Y已签约')
    book_status: Optional[str] = Field(default='1', description='状态，0：入库，1：上架')
    status: Optional[str] = Field(default='0', description='本站状态: 0:可用, 1不可用, 2已删除')

    class Config:
        from_attributes = True


class BookIndexVO(BaseVO):
    id: Optional[int] = Field(default=None, description='主键ID')
    book_id: Optional[str] = Field(default=None, description='原始书籍ID')
    index_num: Optional[str] = Field(default=None, description='章节编号')
    index_name: Optional[str] = Field(default=None, description='章节名称')
    word_count: Optional[int] = Field(default=None, description='章节字数')
    status: Optional[str] = Field(default=None, description='章节状态')


class BookContentVO(BaseVO):
    id: Optional[int] = Field(default=None, description='主键ID')
    book_id: Optional[str] = Field(default=None, description='原始书籍ID')
    index_num: Optional[str] = Field(default=None, description='章节编号')
    content: Optional[str] = Field(default=None, description='章节内容')


class BookQuery:
    def __init__(
            self,
            key: Optional[int] = Query(default=None, description='书籍主键'),
            book_id: Optional[str] = Query(default=None, description='书籍原始ID'),
            name: Optional[str] = Query(default=None, description='书籍名称'),
    ):
        self.key: int = key
        self.book_id: str = book_id
        self.name: str = name
