# !/usr/bin/env python
# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, Path, Body, BackgroundTasks
from sqlalchemy.orm import Session

from modules.novel.internal import service
from modules.novel.internal.entity import schema
from szpy.entity.schema.resp import R, RBase
from szpy.modules.db import sqlalchemy

router = APIRouter(prefix='/crawl', tags=['crawl'])


@router.get(
    '/list',
    response_model=R[list[schema.CrawlSourceVO]],
    response_model_exclude_none=True
)
async def get_crawl_source_by_cond(
        source: schema.CrawSourceQuery = Depends(),
        db: Session = Depends(sqlalchemy.client.session)
):
    crawl_list = service.get_crawl_source(source, db)
    return R(data=crawl_list)


@router.get(
    '/{crawl_id}',
    response_model=R[schema.CrawlSourceVO],
    response_model_exclude_none=True
)
async def get_crawl_source_by_id(
        crawl_id: int = Path(description="主键ID"),
        db: Session = Depends(sqlalchemy.client.session)
):
    crawl = service.get_crawl_source_by_id(crawl_id, db)
    return R(data=crawl)


@router.post(
    '/add',
    response_model=R[schema.CrawlSourceVO],
    response_model_exclude_none=True
)
async def add_crawl_source(
        source: schema.CrawlSourceVO = Body(description="新增的爬虫源"),
        db: Session = Depends(sqlalchemy.client.session)
):
    crawl = service.add_crawl_source(source, db)
    return R(data=crawl)


@router.delete(
    '/delete/{crawl_id}',
    response_model=RBase,
    response_model_exclude_none=True
)
async def delete_crawl_source(
        crawl_id: int = Path(description="主键ID"),
        db: Session = Depends(sqlalchemy.client.session)
):
    service.delete_crawl_source(crawl_id, db)
    return R()


@router.put(
    '/update',
    response_model=R[int],
    response_model_exclude_none=True
)
async def update_crawl_source(
        source: schema.CrawlSourceVO = Body(description="修改后的爬虫源"),
        db: Session = Depends(sqlalchemy.client.session)
):
    count = service.update_crawl_source(source, db)
    return R(data=count)


@router.get(
    '/run/{crawl_id}',
    response_model=RBase,
    response_model_exclude_none=True
)
async def update_crawl_source(
        bt: BackgroundTasks,
        crawl_id: int = Path(description="主键ID"),
        db: Session = Depends(sqlalchemy.client.session)
):
    await service.crawl_by_source(bt, crawl_id, db)
    return R()
