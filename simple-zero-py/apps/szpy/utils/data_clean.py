# !/usr/bin/env python
# -*- coding: utf-8 -*-
import re

import unicodedata


def clean_content(contents):
    tmp = []
    for item in contents:
        item = filter_by_keyword(item)
        if item is False:
            continue
        # 将\xa0、\u3000转为空格, 其他空格换行替换为空串
        tmp.append(unicodedata.normalize('NFKC', re.sub(r'[\s ]', '', item.__str__())))

    text = ''.join(tmp)
    if text.startswith('go'):
        text = text[2:]
    if text.endswith('over'):
        text = text[:-4]
    return re.sub(r'(<br/?>)+', '\n', text)


def filter_by_keyword(obj):
    drop_list = ['爱阅小说app', '爱阅app']
    rep_list = ['Ｍ.bΙＱμＧètν.còＭ']
    for item in drop_list:
        if item in obj:
            return False
    for item in rep_list:
        if item in obj:
            return obj.__str__().replace(item, '')
    return obj


def contain_one(origin, keywords):
    for keyword in keywords:
        if keyword in origin:
            return True
    return False
