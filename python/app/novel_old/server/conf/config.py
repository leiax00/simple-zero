# !/usr/bin/env python
# -*- coding: utf-8 -*-
from urllib.parse import quote, unquote

# import etcd3
import yaml


class Config:
    def __init__(self):
        self.etct = ''
        self.app_name = 'cn.leiax00.novel'
        self.host = '0.0.0.0'
        self.port = 13000
        self.url_prefix = '/novel/v1'
        self.db_mongo = 'mongodb://127.0.0.1:27017/'

    def load(self, conf_p='/data/conf/config.yaml'):
        with open(conf_p, 'r', encoding='utf-8') as rf:
            data = yaml.load_all(rf, yaml.SafeLoader)
            for item in data:
                self.__dict__ = {**self.__dict__, **item}

    def load_by_etcd(self):
        # etcd3.client()
        pass


