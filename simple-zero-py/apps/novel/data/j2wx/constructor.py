# !/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import re

from bean.j2wx_book import *
from utils.time_utils import parse_str_2_date


def construct_j2book(data, novel_id=None):
    if data.get('code') == '1062':  # {'code': '1062', 'message': '1062:该文已被屏蔽，无法查看'}
        logging.warning(f'The article has been blocked and cannot be viewed, novel_id: {novel_id}')
        return None
    return J2Book(
        id=novel_id or data.get('novelId'),
        name=data.get('novelName'),
        author_id=data.get('authorId'),
        author_name=data.get('authorName'),
        cover=data.get('novelCover'),
        size=int(data.get('novelSize', '0').replace(',', '')),
        tags=data.get('novelTags'),
        type=data.get('novelClass'),
        status=data.get('novelStep')
    )


def construct_j2stat(book_data, stat_data, now, channel_key, novel_id=None):
    ticket = re.sub(r'\D', '', stat_data.get('ranking', '0'))
    favorite = re.sub(r'\D', '', stat_data.get('novelbefavoritedcount', '0'))
    chapter = re.sub(r'\D', '', book_data.get('novelChapterCount', '0'))
    return J2Stat(
        id=novel_id or book_data.get('novelId'),
        time=now,
        channel_key=channel_key,
        favorite_count=int(favorite) if favorite != '' else 0,
        ticket_count=int(ticket) if ticket != '' else 0,
        chapter_count=int(chapter) if chapter != '' else 0,
        newest_date=parse_str_2_date(book_data.get('renewDate'))
    )


def construct_j2data(books, stat_list, rank_stat_list=None):
    if rank_stat_list is None:
        rank_stat_list = []
    # { time: {novel_id: score}, .... }
    rank_stat_map = {item.time: item.to_map() for item in rank_stat_list}
    # { novel_id: [J2Stat] }
    stat_map = {}
    for item in stat_list:
        tmp = stat_map.get(item.id, [])
        tmp.append(item)
        stat_map[item.id] = tmp
    novels = []
    for book in books:
        stat_dto_list = [
            J2StatDto().
            with_param(
                item,
                rank_stat_map.get(item.time, {}).get(book.id, 0)
            )
            for item in stat_map.get(book.id, [])]
        novels.append(J2Data().with_param(book, stat_dto_list).to_camel_dict())
    return novels