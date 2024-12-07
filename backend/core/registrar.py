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
from backend.core.path_conf import STATIC_DIR
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

    # 静态文件
    register_static_file(app)

    # 中间件
    register_middleware(app)

    return app


def register_logger() -> None:
    """
    系统日志注册
    :return:
    """
    setup_logging()
    set_customize_logfile()


def register_static_file(app: FastAPI):
    """
    静态文件交互开发模式, 生产将自动关闭，生产必须使用 nginx 静态资源服务

    :param app:
    :return:
    """
    if settings.FASTAPI_STATIC_FILES:
        from fastapi.staticfiles import StaticFiles

        app.mount('/static', StaticFiles(directory=STATIC_DIR), name='static')


def register_middleware(app: FastAPI):
    """
    中间件，执行顺序从下往上

    :param app:
    :return:
    """
    # Access log: 请求日志中间件
    if settings.MIDDLEWARE_ACCESS:
        from backend.middleware.access_middleware import AccessMiddleware
        app.add_middleware(AccessMiddleware)

    # CORS: 必须放在最后
    if settings.MIDDLEWARE_CORS:
        from fastapi.middleware.cors import CORSMiddleware

        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.CORS_ALLOWED_ORIGINS,
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
            expose_headers=settings.CORS_EXPOSE_HEADERS,
        )
