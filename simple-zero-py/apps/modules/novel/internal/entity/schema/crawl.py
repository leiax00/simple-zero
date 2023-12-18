# !/usr/bin/env python
# -*- coding: utf-8 -*-
from enum import Enum
from typing import Optional

from fastapi import Query
from pydantic import Field, BaseModel

from modules.novel.internal.entity.schema.baseVo import BaseVO, Remark


class AttrEnum(str, Enum):
    HREF = 'href'
    SRC = 'src'
    TEXT = 'text'
    CONTENTS = 'contents'


class DataParserType(str, Enum):
    ORIGIN = 'origin'
    PATTERN = 'pattern'
    SCRIPT = 'script'


class HtmlParserType(str, Enum):
    BS = 'bs'
    XPATH = 'xpath'


class SelectorType(str, Enum):
    UNIQUE = 'unique',
    MULTI = 'multi'


class BookDataType(str, Enum):
    INFO = 'info'
    INDEX = 'index'
    CONTENT = 'content'


class ParseRule(BaseModel):
    field_name: Optional[str] = Field(description='字段名称')
    selector: Optional[str] = Field(default=None, description='选择器')
    attr: Optional[str] = Field(default=AttrEnum.TEXT.value, description='读取的属性类型',
                                pattern='href|src|text|contents')
    parser_type: Optional[str] = Field(default=DataParserType.ORIGIN.value, description='值的解析方式',
                                       pattern='origin|pattern|script')
    parser: Optional[str] = Field(default='(?P<val>.*)',
                                  description='解析方法, pattern时为正则表达式(读group("val")), '
                                              'script为python脚本(exec执行, 定义一个parse(val)方法, def或者lambda表达式均可)')


class ItemRule(BaseModel):
    url: Optional[str] = Field(default=None, description='索引的url - python format格式')
    root: Optional[str] = Field(default=None, description='对象的根选择器')
    rule_type: Optional[str] = Field(default=SelectorType.UNIQUE.value, description='规则类型: unique, multi',
                                     pattern='unique|multi')
    fields: list[ParseRule] = Field(default=[], description='字段读取, 最后得到一个字典或字典列表')


class CrawlRule(BaseModel):
    parse_type: Optional[str] = Field(default=HtmlParserType.BS.value, pattern='bs|xpath', description='解析类型')
    domain: Optional[str] = Field(default=None, description='域名')
    info: ItemRule = Field(description='书籍基本信息规则')
    index: ItemRule = Field(description='书籍目录信息规则')
    content: ItemRule = Field(description='书籍章节内容规则')


class CrawlSourceVO(BaseVO, Remark):
    id: Optional[int] = Field(default=None, description='主键ID')
    source_name: Optional[str] = Field(default=None, description='爬虫名称')
    crawl_rule: Optional[CrawlRule] = Field(description='爬虫规则')
    status: Optional[str] = Field(default='0', description='爬虫状态: 0关闭, 1开启, 2已删除')

    class Config:
        from_attributes = True


class CrawSourceQueryBase:
    def __init__(
            self,
            key: Optional[int] = Query(default=None, description='主键ID'),
            name: Optional[str] = Query(default=None, description='爬虫名称, 模糊查询'),
    ):
        self.key = key
        self.name = name


class CrawSourceQuery(CrawSourceQueryBase):
    def __init__(
            self,
            key: Optional[int] = Query(default=None, description='主键ID'),
            name: Optional[str] = Query(default=None, description='爬虫名称, 模糊查询'),
            status: Optional[str] = Query(default=None, description='爬虫状态'),
    ):
        super().__init__(key, name)
        self.status = status
