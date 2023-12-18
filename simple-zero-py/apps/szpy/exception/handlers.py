# !/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from fastapi import status as http_status, FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exception_handlers import websocket_request_validation_exception_handler as fastapi_websocket_handler
from fastapi.exceptions import RequestValidationError, WebSocketRequestValidationError
from fastapi.utils import is_body_allowed_for_status_code
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from starlette.websockets import WebSocket

from szpy.entity.schema.resp import RBase, R
from szpy.exception.model import *


def add_exception_handler(app: FastAPI):
    @app.exception_handler(HTTPException)
    async def handle_http_err(request: Request, exc: HTTPException) -> Response:
        return await http_exception_handler(request, exc)

    @app.exception_handler(SzBaseException)
    async def handle_http_err(request: Request, exc: SzBaseException) -> Response:
        return await base_exception_handler(request, exc)

    @app.exception_handler(RequestValidationError)
    async def handle_http_err(request: Request, exc: RequestValidationError) -> Response:
        return await request_validation_exception_handler(request, exc)


async def base_exception_handler(request: Request, exc: SzBaseException) -> Response:
    headers = getattr(exc, "headers", None)
    return JSONResponse(
        status_code=http_status.HTTP_400_BAD_REQUEST,
        headers=headers,
        content=RBase(code=exc.code(), msg=jsonable_encoder(exc.errors())).model_dump()
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> Response:
    headers = getattr(exc, "headers", None)
    if not is_body_allowed_for_status_code(exc.status_code):
        return Response(status_code=exc.status_code, headers=headers)
    return JSONResponse(
        RBase(code=status.STATUS_10000_FAIL, msg=exc.detail).model_dump(), status_code=exc.status_code, headers=headers
    )


async def request_validation_exception_handler(
        request: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content=R(code=status.STATUS_10001_VALIDATION_ERR, data=jsonable_encoder(exc.errors())).model_dump()
    )


async def websocket_request_validation_exception_handler1(
        websocket: WebSocket, exc: WebSocketRequestValidationError
) -> None:
    await fastapi_websocket_handler(websocket, exc)
