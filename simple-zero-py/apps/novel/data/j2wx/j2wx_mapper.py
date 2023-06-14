# !/usr/bin/env python
# -*- coding: utf-8 -*-
from playhouse.shortcuts import model_to_dict

from bean.j2wx_book import *
from config import db, c_redis, REDIS_KEY_PREFIX
from utils.time_utils import today_zero


class J2wxMapper:
    def __init__(self):
        self.db = db
        self.c_redis = c_redis
        self.one_batch = 200

    @staticmethod
    def get_rank_list(channel_key):
        return J2Rank.select().where(J2Rank.channel_key == channel_key)

    @staticmethod
    def get_rank_stat_in_today(rank_id, zero=None):
        if zero is None:
            zero = today_zero()
        return list(J2RankStat.select().where(J2RankStat.id == rank_id, J2RankStat.time >= zero))

    @staticmethod
    def get_stat_info_in_today_by_ids(novel_ids, zero=None):
        if zero is None:
            zero = today_zero()
        return list(J2Stat.select().where(J2Stat.id.in_(novel_ids), J2Stat.time >= zero))

    @staticmethod
    def get_novel_info_by_ids(novel_ids):
        return list(J2Book.select().where(J2Book.id.in_(novel_ids)))

    def add_novel_by_batch(self, novels):
        for i in range(0, len(novels), self.one_batch):
            batch = novels[i:i + self.one_batch]
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

    def add_rank_by_batch(self, rank_list):
        for i in range(0, len(rank_list), self.one_batch):
            batch = rank_list[i:i + self.one_batch]
            J2Rank.insert_many(
                [model_to_dict(item) for item in batch]
            ).on_conflict(
                conflict_target=[J2Rank.rank_id],
                preserve=[J2Rank.type, J2Rank.channel_key, J2Rank.rank_name]
            ).execute()

    def add_stat_by_batch(self, stat_list):
        for i in range(0, len(stat_list), self.one_batch):
            batch = stat_list[i:i + self.one_batch]
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

    def add_rank_stat_by_batch(self, rank_stat_list):
        for i in range(0, len(rank_stat_list), self.one_batch):
            batch = rank_stat_list[i:i + self.one_batch]
            J2RankStat.insert_many(
                [model_to_dict(item) for item in batch]
            ).on_conflict(
                conflict_target=[J2RankStat.id, J2RankStat.time],
                preserve=[
                    J2RankStat.novel_ids,
                ]
            ).returning().execute()

    @staticmethod
    def get_custom_rank_by_id(rank_id):
        return J2CustomRank.get_by_id(rank_id)

    @staticmethod
    def save_custom_rank(data):
        return J2CustomRank.create(**data)

    @staticmethod
    def del_custom_rank(rank_ids):
        return J2CustomRank.delete().where(J2CustomRank.id.in_(rank_ids)).execute()

    def add_novel_2_custom_rank(self, rank_id, novel_ids) -> J2CustomRank:
        with self.db.atomic() as tcn:
            rank = self.get_custom_rank_by_id(rank_id)
            new_ids = novel_ids + rank.novel_ids
            rank.novel_ids = list(set(new_ids))
            rank.save()
        return rank

    def remove_novel_from_custom_rank(self, rank_id, novel_ids) -> J2CustomRank:
        with self.db.atomic() as tcn:
            rank = self.get_custom_rank_by_id(rank_id)
            new_ids = set(rank.novel_ids) - set(novel_ids)
            rank.novel_ids = list(new_ids)
            rank.save()
            return rank

    #  ====================== redis ============================
    def get_novel_ids_by_rank_id(self, rank_id):
        return self.c_redis.zrange(f'{REDIS_KEY_PREFIX}/j2wx/rank/{rank_id}', 0, -1)

    @staticmethod
    def update_rank__4_novel_list(mapping, now, channel_key):
        rank_stat_list = []
        for k, v in mapping.items():
            key = f'{REDIS_KEY_PREFIX}/j2wx/rank/{k}'
            new_key = f'{REDIS_KEY_PREFIX}/j2wx/rank/{k}/new'
            c_redis.zadd(new_key, {v[i]: i + 1 for i in range(len(v))})
            c_redis.rename(new_key, key)
            rank_stat_list.append(J2RankStat(id=k, time=now, channel_key=channel_key, novel_ids=v))
        return rank_stat_list


j2wx_mapper = J2wxMapper()
