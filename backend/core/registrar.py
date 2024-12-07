#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fastapi-base-backend 
@File    ：registrar.py
@IDE     ：PyCharm 
@Author  ：imbalich
@Date    ：2024/12/7 16:47 
'''
import socketio

from fastapi import FastAPI

from backend.common.log import setup_logging, set_customize_logfile
from backend.core.conf import settings
from backend.utils.serializers import MsgSpecJSONResponse


def register_app():
    """
    注册 app 初始化启动
    """
    app = FastAPI(
        title=settings.FASTAPI_TITLE,
        version=settings.FASTAPI_VERSION,
        description=settings.FASTAPI_DESCRIPTION,
        docs_url=settings.FASTAPI_DOCS_URL,
        redoc_url=settings.FASTAPI_REDOCS_URL,
        openapi_url=settings.FASTAPI_OPENAPI_URL,
        default_response_class=MsgSpecJSONResponse,
        # TODO:后续完善生命周期检查方法
        # lifespan=register_init,
    )

    # TODO:后续增加socketio服务
    # register_socket_app(app)

    # 全局日志注册
    register_logger()

    return app


def register_logger() -> None:
    """
    系统日志注册
    :return:
    """
    setup_logging()
    set_customize_logfile()
