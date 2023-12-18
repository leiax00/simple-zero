# !/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from data.j2wx.j2wx_parser import J2wxParserFactory, Collector
from utils.httpHelper import *

domain = 'https://app-cdn.jjwxc.com/'


class APIS(Enum):
    # 古言app首页
    gywx_home = Api('/bookstore/getFullPageV1?channel=gywx&version=9', HttpMethod.GET)
    #  https://app-cdn.jjwxc.com/bookstore/getFullPageV1?channelBody={"1":{"offset":"0","limit":"2"}}&channelMore=1
    rank = Api('/bookstore/getFullPageV1', HttpMethod.GET)


class J2wxPuller:
    def __init__(self):
        self.client = HttpSession(domain)
        self.parse_factory = J2wxParserFactory()

    def pull(self, channel_key) -> Collector:
        param = APIS.gywx_home.value.get_request_params()
        with self.client.request(**param, verify=False) as resp:
            data_list = resp.json().get('data')

        collector = Collector()
        for item in data_list:
            self.pull_rank(item)

            parser = self.parse_factory.parser(item.get('channelName'), item.get('type'))
            if parser is not None:
                parser.with_collector(collector).collect(item, channel_key)

        return collector

    def pull_rank(self, data):
        rank_id = data.get('channelMoreId', '').strip()
        if rank_id == '':
            return
        page = {rank_id: {'offset': 0, 'limit': 50}}
        params = APIS.rank.value.get_request_params(
            params={'channelBody': json.dumps(page), 'channelMore': rank_id}
        )
        with self.client.request(**params, verify=False) as resp:
            resp_data = resp.json()
            if resp_data.get('code') == '200':
                data['data'] = resp_data.get('data', {'data': {}}).get('data')


j2wx_puller = J2wxPuller()
