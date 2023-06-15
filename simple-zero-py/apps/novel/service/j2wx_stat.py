# !/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from config import db
from data.j2wx.j2wx import j2wx_puller
from data.j2wx.j2wx_mapper import j2wx_mapper


class J2wxStat:
    def __init__(self):
        self.puller = j2wx_puller
        self.mapper = j2wx_mapper

    def pull(self, param=None):
        logging.info(f'start to pull j2wx info. channel key / param is: {param}')
        channel_key = param
        collector = self.puller.pull(channel_key)
        with db.atomic() as tcn:
            self._save_rank(collector)
            self._save_book(collector)
            self._save_rank_stat(channel_key, collector)
        return True

    def pull_custom_rank(self, param=None):
        logging.info(f'start to pull custom rank info.')
        novel_ids = self.mapper.get_all_custom_rank_novels()
        if len(novel_ids) == 0:
            return
        collector = self.puller.pull_novel_info_by_batch(param, novel_ids)
        with db.atomic() as tcn:
            self._save_book(collector)

    def _save_rank(self, collector):
        channel_list = list(collector.channel_list)
        self.mapper.add_rank_by_batch(channel_list)

    def _save_book(self, collector):
        novel_list = list(collector.novel_list)
        logging.info(f'book count: {len(novel_list)}')
        self.mapper.add_novel_by_batch(novel_list)
        stat_list = list(collector.stat_list)
        self.mapper.add_stat_by_batch(stat_list)

    def _save_rank_stat(self, channel_key, collector):
        # 插入榜单统计信息, redis记录最新一次榜单的数据, 便于页面获取数据; 数据库记录每次的快照
        rank_stat_list = self.mapper.update_rank__4_novel_list(collector.mapping, collector.now, channel_key)
        self.mapper.add_rank_stat_by_batch(rank_stat_list)


j2wx = J2wxStat()
