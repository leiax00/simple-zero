# !/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Sequence, Any

from szpy.constants import status


class SzBaseException(Exception):
    def __init__(self, errors: Sequence[Any], *, code: int = status.STATUS_10000_FAIL) -> None:
        self._errors = errors
        self._code = code

    def errors(self) -> Sequence[Any]:
        return self._errors

    def code(self) -> int:
        return self._code
