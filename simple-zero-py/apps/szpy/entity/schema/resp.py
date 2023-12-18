# !/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import TypeVar, Generic, Optional

from pydantic import BaseModel

from szpy.constants import status

T = TypeVar('T')


class RCode(BaseModel):
    code: int = status.STATUS_0_OK


class RBase(RCode):
    msg: Optional[str] = None


class R(RBase, Generic[T]):
    data: Optional[T] = None
