# !/usr/bin/env python
# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from modules.novel.internal import service
from modules.novel.internal.entity import schema
from szpy.entity.schema.resp import R
from szpy.modules.db import sqlalchemy

router = APIRouter(prefix='/book', tags=['book'])


@router.get(
    '/get',
    response_model=R[schema.BookVO],
    response_model_exclude_none=True
)
async def get_book(
        query: schema.BookQuery = Depends(),
        db: Session = Depends(sqlalchemy.client.session)
):
    db_book = service.get_book(query, db)
    return R(data=db_book)


@router.get(
    '/index-list',
    response_model=R[list[schema.BookIndexVO]],
    response_model_exclude_none=True
)
async def get_book_index_list(
        bid=Query(..., description='书籍原始ID'),
        db: Session = Depends(sqlalchemy.client.session)
):
    index_list = service.get_book_index_list(bid, db)
    return R(data=index_list)


@router.get(
    '/content',
    response_model=R[schema.BookContentVO],
    response_model_exclude_none=True
)
async def get_book_index_list(
        bid=Query(..., description='书籍原始ID'),
        cid=Query(..., description='书籍章节编号'),
        db: Session = Depends(sqlalchemy.client.session)
):
    content = service.get_book_content(bid, cid, db)
    return R(data=content)


@router.get(
    '/repull-list',
    response_model=R[dict],
    response_model_exclude_none=True
)
async def get_need_repull_content_ids(
        bid: str,
        db: Session = Depends(sqlalchemy.client.session)
):
    id_list = service.need_repull_content_ids(bid, db)
    return R(data={"count": len(id_list), "idList": id_list})
