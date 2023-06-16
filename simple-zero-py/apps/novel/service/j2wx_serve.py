# !/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from bean.j2wx_book import *
from config import db
from data.j2wx import constructor
from data.j2wx.j2wx import j2wx_puller
from data.j2wx.j2wx_mapper import j2wx_mapper
from utils.time_utils import today_zero


class J2wxServe:
    def __init__(self):
        self.mapper = j2wx_mapper
        self.puller = j2wx_puller

    def get_rank_list(self, channel_key):
        return [item.to_camel_dict() for item in self.mapper.get_rank_list(channel_key)]

    def get_rank_info(self, channel_key, rank_id):
        logging.info(f'channel_key: {channel_key}, rank_id: {rank_id}')
        novel_ids = self.mapper.get_novel_ids_by_rank_id(rank_id)
        with db.atomic() as tcn:
            zero = today_zero()
            rank_stat_list = self.mapper.get_rank_stat_in_today(rank_id, zero)
            stat_list = self.mapper.get_stat_info_in_today_by_ids(novel_ids, zero)
            books = self.mapper.get_novel_info_by_ids(novel_ids)
            novels = constructor.construct_j2data(novel_ids, books, stat_list, rank_stat_list)

        logging.info(len(novels))
        return novels

    def get_custom_rank_info(self, rank_id):
        logging.info(f'start to query custom rank, rank id is: {rank_id}')
        with db.atomic() as tcn:
            rank = self.mapper.get_custom_rank_by_id(rank_id)
            zero = today_zero()
            zero = zero - datetime.timedelta(days=7)
            stat_list = self.mapper.get_stat_info_in_today_by_ids(rank.novel_ids, zero)
            books = self.mapper.get_novel_info_by_ids(rank.novel_ids)
            novels = constructor.construct_j2data(rank.novel_ids, books, stat_list)
        return novels

    def save_custom_rank(self, data):
        return self.mapper.save_custom_rank(data).to_camel_dict()

    def get_custom_rank_by_key(self, key):
        rank = self.mapper.get_custom_rank_by_key(key)
        return rank.to_camel_dict() if rank is not None else None

    def del_custom_rank(self, rank_ids: list[int]):
        return self.mapper.del_custom_rank(rank_ids)

    def add_novel_2_custom_rank(self, rank_id, novel_ids: list):
        with db.atomic() as tcn:
            rank = self.mapper.add_novel_2_custom_rank(rank_id, novel_ids)
            novels = self.puller.pull_novel_base_info(novel_ids)
            self.mapper.add_novel_by_batch(novels)

            return rank.to_camel_dict()

    def remove_novel_from_custom_rank(self, rank_id, novel_ids: list):
        return self.mapper.remove_novel_from_custom_rank(rank_id, novel_ids).to_camel_dict()

    def get_book_list_by_rank(self):
        return []

    def get_stat_info(self, cond):
        return []


j2wx_serve = J2wxServe()
