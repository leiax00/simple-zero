# !/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Sequence, Any

from szpy.constants import status
from szpy.exception.model import SzBaseException


class TaskNoExist(SzBaseException):
    def __init__(self, errors: Sequence[Any], *, code: int = status.STATUS_11001_XXL_FAIL) -> None:
        super().__init__(errors, code=code)
