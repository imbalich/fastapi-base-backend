#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fastapi-base-backend 
@File    ：state_middleware.py
@IDE     ：PyCharm 
@Author  ：imbalich
@Date    ：2024/12/9 15:00 
'''
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from backend.utils.request_parse import parse_ip_info, parse_user_agent_info


class StateMiddleware(BaseHTTPMiddleware):
    """
    请求 state 中间件
    这个中间件用于在每个请求中添加额外的状态信息，如 IP 地址、地理位置、用户代理等。
    """

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """
        处理每个进入的 HTTP 请求

        :param request: FastAPI 的 Request 对象，包含了当前 HTTP 请求的所有信息
        :param call_next: 调用下一个中间件或路由处理函数的方法
        :return: HTTP 响应对象
        """
        # 解析 IP 信息，涉及 IP 地理位置查询
        ip_info = await parse_ip_info(request)
        # 解析用户代理信息，涉及解析 User-Agent 字符串
        ua_info = parse_user_agent_info(request)

        # 设置附加请求信息到 request.state
        # request.state 是 FastAPI 提供的一个属性，用于在请求的整个生命周期内存储数据
        request.state.ip = ip_info.ip          # 客户端 IP 地址
        request.state.country = ip_info.country  # 客户端所在国家
        request.state.region = ip_info.region    # 客户端所在地区
        request.state.city = ip_info.city        # 客户端所在城市
        request.state.user_agent = ua_info.user_agent  # 完整的用户代理字符串
        request.state.os = ua_info.os            # 客户端操作系统
        request.state.browser = ua_info.browser  # 客户端浏览器
        request.state.device = ua_info.device    # 客户端设备类型

        # 调用下一个中间件或路由处理函数
        response = await call_next(request)

        return response