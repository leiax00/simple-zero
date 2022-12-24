# !/usr/bin/env python
# -*- coding: utf-8 -*-
import pymongo

from conf.config import Config

mongo_ct = pymongo.MongoClient(Config.db_mongo)['py_novel']
