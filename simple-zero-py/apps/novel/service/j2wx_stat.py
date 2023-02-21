# !/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from playhouse.shortcuts import model_to_dict

from bean.j2wx_book import *
from config import db, c_redis, REDIS_KEY_PREFIX
from data.j2wx.j2wx_puller import j2wx_puller


class J2wxStat:
    def __init__(self):
        self.puller = j2wx_puller

    def pull(self, param=None):
        logging.info(f'param is: {param}')
        channel_key = param
        collector = self.puller.pull(channel_key)
        with db.atomic() as tcn:
            J2Rank.insert_many(
                [model_to_dict(item) for item in collector.channel_list]
            ).on_conflict(
                conflict_target=[J2Rank.id],
                preserve=[J2Rank.rank_id, J2Rank.type, J2Rank.channel_key, J2Rank.rank_name]
            ).execute()

            J2Book.insert_many(
                [model_to_dict(item) for item in collector.novel_list]
            ).on_conflict(
                conflict_target=[J2Book.id],
                preserve=[
                    J2Book.name,
                    J2Book.author_id,
                    J2Book.author_name,
                    J2Book.cover,
                    J2Book.size,
                    J2Book.tags,
                    J2Book.type,
                ]
            ).execute()

            J2Stat.insert_many(
                [model_to_dict(item) for item in collector.stat_list]
            ).on_conflict(
                conflict_target=[J2Stat.id, J2Stat.time],
                preserve=[
                    J2Stat.favorite_count,
                    J2Stat.ticket_count,
                ]
            ).returning().execute()  # returning()表示设置返回模型, 否则会返回主键元组, 在shardingsphere分表情况下, 无法正确获取分表名
            for k, v in collector.mapping.items():
                c_redis.zadd(f'{REDIS_KEY_PREFIX}/j2wx/rank/{k}', {v[i]: i + 1 for i in range(len(v))})
        return True


j2wx = J2wxStat()
