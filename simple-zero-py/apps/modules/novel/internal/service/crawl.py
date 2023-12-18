# !/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Type

from fastapi import BackgroundTasks
from sqlalchemy import and_
from sqlalchemy.orm import Session

from modules.novel.internal.engine.book import BookEngine
from modules.novel.internal.entity import models, schema


def __base_query(db, source):
    query = db.query(models.CrawlSource)
    if source.key is not None:
        query = query.filter(and_(models.CrawlSource.id == source.key))
    if source.name is not None:
        query = query.filter(and_(source.name in models.CrawlSource.source_name))
    return query


def get_crawl_source(source: schema.CrawSourceQuery, db: Session) -> list[Type[models.CrawlSource]]:
    query = __base_query(db, source)
    if source.status is not None:
        query = query.filter(models.CrawlSource.status == source.status)
    return query.all()


def get_crawl_source_by_id(key: int, db: Session):
    return db.query(models.CrawlSource).filter(and_(models.CrawlSource.id == key)).first()


def add_crawl_source(source: schema.CrawlSourceVO, db: Session):
    db_s = models.CrawlSource(**source.model_dump())
    db.add(db_s)
    db.commit()
    db.refresh(db_s)
    return db_s


def delete_crawl_source(key: int, db: Session):
    db.query(models.CrawlSource).filter(and_(models.CrawlSource.id == key)).delete()
    db.commit()


def update_crawl_source(source: schema.CrawlSourceVO, db: Session):
    count = db.query(models.CrawlSource).filter(and_(models.CrawlSource.id == source.id)).update(
        source.model_dump(exclude_unset=True)
    )
    db.commit()
    return count


def get_bids_by_crawl(crawl_id: int, db: Session) -> set[str]:
    bid_list = db.query(models.CrawlBook.book_id).filter(and_(
        models.CrawlBook.crawl_id == crawl_id
    )).all()
    return set([item[0] for item in bid_list])


async def crawl_by_source(bt: BackgroundTasks, key: int, db: Session):
    source = get_crawl_source_by_id(key, db)
    bids = get_bids_by_crawl(source.id, db)
    engine = BookEngine(schema.CrawlSourceVO.model_validate(source), bids)
    bt.add_task(engine.parse)

