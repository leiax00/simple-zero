# !/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from bean.j2wx_book import *
from config import db, c_redis, REDIS_KEY_PREFIX
from utils.time_utils import today_zero


class J2wxServe:
    def __init__(self):
        self.db = db
        self.c_redis = c_redis

    @staticmethod
    def get_rank_list(channel_key):
        query = J2Rank.select().where(J2Rank.channel_key == channel_key)
        return [item.to_camel_dict() for item in query]

    def get_rank_info(self, channel_key, rank_id):
        logging.info(f'channel_key: {channel_key}, rank_id: {rank_id}')
        novel_ids = self.c_redis.zrange(f'{REDIS_KEY_PREFIX}/j2wx/rank/{rank_id}', 0, -1)
        with self.db.atomic() as tcn:
            zero = today_zero()
            rank_stat_list = list(
                J2RankStat.select()
                .where(J2RankStat.id == rank_id, J2RankStat.time >= zero)
            )
            stat_list = list(J2Stat.select().where(J2Stat.id in novel_ids, J2Stat.time >= zero))
            books = list(J2Book.select().where(J2Book.id in novel_ids))

            # { time: {novel_id: score}, .... }
            rank_stat_map = {item.time: item.to_map() for item in rank_stat_list}
            # { novel_id: [J2Stat] }
            stat_map = {}
            for item in stat_list:
                tmp = stat_map.get(item.id, [])
                tmp.append(item)
                stat_map[item.id] = tmp

            book_map = {item.id: item for item in books}
            novels = []
            for novel_id in novel_ids:
                book = book_map[novel_id]
                stat_dto_list = [
                    J2StatDto().
                    with_param(
                        item,
                        rank_stat_map.get(item.time, {}).get(book.id)
                    )
                    for item in stat_map.get(book.id, [])]
                novels.append(J2Data().with_param(book, stat_dto_list).to_camel_dict())

        logging.info(len(novels))
        return novels

    def get_book_list_by_rank(self):
        return []

    def get_stat_info(self, cond):
        return []


j2wx_serve = J2wxServe()
