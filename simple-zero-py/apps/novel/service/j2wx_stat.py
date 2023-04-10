# !/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from playhouse.shortcuts import model_to_dict

from bean.j2wx_book import *
from config import db, c_redis, REDIS_KEY_PREFIX
from data.j2wx.j2wx import j2wx_puller


class J2wxStat:
    def __init__(self):
        self.puller = j2wx_puller

    def pull(self, param=None):
        logging.info(f'start to pull j2wx info. channel key / param is: {param}')
        channel_key = param
        collector = self.puller.pull(channel_key)
        with db.atomic() as tcn:
            self._save_rank(collector)
            self._save_book(collector)
            self._save_rank_stat(channel_key, collector)
        return True

    @staticmethod
    def _save_rank(collector):
        channel_list = list(collector.channel_list)
        for i in range(0, len(channel_list), 200):
            batch = channel_list[i:i + 200]
            J2Rank.insert_many(
                [model_to_dict(item) for item in batch]
            ).on_conflict(
                conflict_target=[J2Rank.rank_id],
                preserve=[J2Rank.type, J2Rank.channel_key, J2Rank.rank_name]
            ).execute()

    @staticmethod
    def _save_book(collector):
        novel_list = list(collector.novel_list)
        logging.info(f'book count: {len(novel_list)}')
        for i in range(0, len(novel_list), 200):
            batch = novel_list[i:i + 200]
            J2Book.insert_many(
                [model_to_dict(item) for item in batch]
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
                    J2Book.status
                ]
            ).execute()
        stat_list = list(collector.stat_list)
        for i in range(0, len(stat_list), 200):
            batch = stat_list[i:i + 200]
            J2Stat.insert_many(
                [model_to_dict(item) for item in batch]
            ).on_conflict(
                conflict_target=[J2Stat.id, J2Stat.time],
                preserve=[
                    J2Stat.favorite_count,
                    J2Stat.ticket_count,
                    J2Stat.chapter_count,
                    J2Stat.newest_date
                ]
            ).returning().execute()  # returning()表示设置返回模型, 否则会返回主键元组, 在shardingsphere分表情况下, 无法正确获取分表名

    @staticmethod
    def _save_rank_stat(channel_key, collector):
        # 插入榜单统计信息, redis记录最新一次榜单的数据, 便于页面获取数据; 数据库记录每次的快照
        rank_stat_list = []
        for k, v in collector.mapping.items():
            key = f'{REDIS_KEY_PREFIX}/j2wx/rank/{k}'
            new_key = f'{REDIS_KEY_PREFIX}/j2wx/rank/{k}/new'
            c_redis.zadd(new_key, {v[i]: i + 1 for i in range(len(v))})
            c_redis.rename(new_key, key)
            rank_stat_list.append(J2RankStat(id=k, time=collector.now, channel_key=channel_key, novel_ids=v))

        for i in range(0, len(rank_stat_list), 200):
            batch = rank_stat_list[i:i + 200]
            J2RankStat.insert_many(
                [model_to_dict(item) for item in batch]
            ).on_conflict(
                conflict_target=[J2RankStat.id, J2RankStat.time],
                preserve=[
                    J2RankStat.novel_ids,
                ]
            ).returning().execute()


j2wx = J2wxStat()
