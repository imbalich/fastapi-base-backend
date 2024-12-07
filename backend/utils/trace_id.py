#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Project : PyCharm
@File    : trace_id.py
@IDE     : Pycharm
@Author  : imbalich
@Time    : 2024/12/8 2:35
'''
from fastapi import Request

from backend.core.conf import settings


def get_request_trace_id(request: Request) -> str:
    # 获取trace id,
    # 要么请求头中找,通过(from asgi_correlation_id import CorrelationIdMiddleware)获取到的
    # 要么就是设置默认值位'-'
    return request.headers.get(settings.TRACE_ID_REQUEST_HEADER_KEY) or settings.LOG_CID_DEFAULT_VALUE
