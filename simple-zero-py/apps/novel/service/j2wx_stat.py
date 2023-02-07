# !/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from playhouse.shortcuts import model_to_dict

from bean.j2wx_book import *
from config import db
from data.j2wx.j2wx_puller import j2wx_puller


class J2wxStat:
    def __init__(self):
        self.puller = j2wx_puller

    def pull(self, param=None):
        collector = self.puller.pull(param)
        with db.atomic() as tcn:
            J2Channel.insert_many(
                [model_to_dict(item) for item in collector.channel_list]
            ).on_conflict(
                conflict_target=[J2Channel.channel],
                preserve=[J2Channel.rank_id, J2Channel.type, J2Channel.more_id]
            ).execute()

            logging.info(f'first novel: {model_to_dict(list(collector.novel_list)[0])}')
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
            ).execute()

            J2BookChannel.truncate_table()
            J2BookChannel.insert_many(
                [model_to_dict(item) for item in collector.mapping_list]
            ).execute()

        return True


j2wx = J2wxStat()
