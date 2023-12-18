# !/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Sequence, Any

from szpy.constants import status
from szpy.exception.model import SzBaseException


class ServiceException(SzBaseException):
    def __init__(self, errors: Sequence[Any], *, code: int = status.STATUS_10000_FAIL) -> None:
        super().__init__(errors, code=code)
