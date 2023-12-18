# !/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Optional

from sqlalchemy import and_, func, or_
from sqlalchemy.orm import Session

from modules.novel.internal.entity import models, schema


def get_book(data: schema.BookQuery, db: Session):
    query = db.query(models.Book)
    if data.book_id is not None:
        query = query.filter(and_(models.Book.book_id == data.book_id))
    if data.key is not None:
        query = query.filter(and_(models.Book.id == data.key))
    if data.name is not None:
        query = query.filter(and_(models.Book.id == data.key))
    return query.first()


def get_book_index_list(book_id: str, db: Session):
    query = db.query(models.BookIndex).filter(
        and_(models.BookIndex.book_id == book_id)
    ).order_by(models.BookIndex.index_num)
    return query.all()


def get_book_content(bid: str, cid: str, db: Session) -> Optional[models.BookContent]:
    return db.query(models.BookContent).filter(
        and_(
            models.BookContent.book_id == bid,
            models.BookContent.index_num == cid
        )
    ).first()


def has_pulled_content_ids(bid: str, db: Session) -> set[str]:
    """
        获取已经pull过内容的书籍章节ID
        需要更新的章节特征:  -- 取反
            1. 内容长度不小于500才算
            2. 章节标题第xx章
    """
    tmp_list = db.query(
        models.BookContent.index_num
    ).select_from(models.BookContent).join(
        models.BookIndex,
        and_(
            models.BookIndex.book_id == models.BookContent.book_id,
            models.BookIndex.index_num == models.BookContent.index_num,
        )
    ).filter(
        and_(models.BookContent.book_id == bid,
             or_(
                 ~models.BookIndex.index_name.regexp_match(r'^第.*章.*'),
                 func.length(models.BookContent.content) >= 500
             )
             )
    ).all()
    return set([item[0] for item in tmp_list])


def need_repull_content_ids(bid: str, db: Session) -> set[str]:
    """ 获取需要重新爬取章节内容的章节ID列表 """
    tmp_list = db.query(
        models.BookContent.index_num
    ).select_from(models.BookContent).join(
        models.BookIndex,
        and_(
            models.BookIndex.book_id == models.BookContent.book_id,
            models.BookIndex.index_num == models.BookContent.index_num,
        )
    ).filter(
        and_(models.BookContent.book_id == bid,
             models.BookIndex.index_name.regexp_match(r'^第.*章.*'),
             func.length(models.BookContent.content) < 500
             )
    ).all()
    return set([item[0] for item in tmp_list])


if __name__ == '__main__':
    from szpy.modules.db import sqlalchemy
    import datetime

    now = datetime.datetime.now()
    sqlalchemy.client.init(sqlalchemy.DBConfig(url='postgresql://postgres:lax4832.@10.1.0.3:5432/simple-zero'))
    with sqlalchemy.client.context() as tmp:  # type: Session
        print(has_pulled_content_ids('121_121681', tmp))

    print(f'cost: {datetime.datetime.now() - now}')
