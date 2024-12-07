#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fastapi-base-backend 
@File    ：access_middleware.py
@IDE     ：PyCharm 
@Author  ：imbalich
@Date    ：2024/12/7 17:40 
'''
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from backend.common.log import log
from backend.utils.timezone import timezone


class AccessMiddleware(BaseHTTPMiddleware):
    """
    请求日志中间件
    这个中间件用于记录每个 HTTP 请求的访问日志，包括请求时间、客户端 IP、请求方法、
    响应状态码、请求路径和处理时间。
    """

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """
        处理每个进入的 HTTP 请求。

        :param request: 当前的 HTTP 请求对象
        :param call_next: 调用链中的下一个中间件或最终的请求处理函数
        :return: HTTP 响应对象
        """
        # 记录请求开始时间
        start_time = timezone.now()

        # 调用下一个中间件或路由处理函数，获取响应
        # 这里使用 await 是因为 call_next 是一个异步函数
        response = await call_next(request)

        # 记录请求结束时间
        end_time = timezone.now()

        # 计算请求处理时间（毫秒）
        process_time = round((end_time - start_time).total_seconds(), 3) * 1000.0

        # 构建并记录日志信息
        log.info(
            f'{request.client.host: <15} | '  # 客户端 IP 地址，左对齐，宽度 15
            f'{request.method: <8} | '        # HTTP 请求方法，左对齐，宽度 8
            f'{response.status_code: <6} | '  # HTTP 响应状态码，左对齐，宽度 6
            f'{request.url.path} | '          # 请求的 URL 路径
            f'{process_time}ms'               # 请求处理时间（毫秒）
        )

        # 返回响应对象
        return response
