# !/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Optional, Any

from pydantic import BaseModel, Field


class API(BaseModel):
    url: Optional[str] = None
    method: Optional[str] = Field(default='GET', pattern='GET|POST|PUT|DELETE')
    headers: dict = None
    json_: Any = Field(default=None, alias='json')
    data: Any = None
    params: Any = None

    def model_dump(self, **kwargs):
        rst = super().model_dump(by_alias=True)
        return rst


if __name__ == '__main__':
    test_api = API(url='/api/test', method='GET')
    api = test_api.model_copy(update={
        'json_': {'A': 1, 'BV': 2},
        'data': {'c': 3},
        'params': {'d': 4},
        'headers': {'user-agent': 'xxxxxx'}
    })
    print(api.model_dump())
