# !/usr/bin/env python
# -*- coding: utf-8 -*-
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import AppMgr
from routes import book, prop, crawl
from szpy.exception import handlers
from szpy.modules import xxl


# 定义 startup 事件处理程序，在应用程序启动时调用
@asynccontextmanager
async def lifespan(main: FastAPI):
    # 启动时执行初始化资源
    AppMgr.init()
    yield
    # 关闭时释放资源
    AppMgr.release()


app = FastAPI(lifespan=lifespan)

app.include_router(book.router)
app.include_router(crawl.router)
app.include_router(prop.router)
app.include_router(xxl.router)

handlers.add_exception_handler(app)


# 命令行: uvicorn apps.modules.novel.main:app --reload
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
