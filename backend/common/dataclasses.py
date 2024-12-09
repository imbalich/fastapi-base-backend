#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fastapi-base-backend 
@File    ：dataclasses.py
@IDE     ：PyCharm 
@Author  ：imbalich
@Date    ：2024/12/9 15:17 
'''
import dataclasses
from datetime import datetime
from fastapi import Response
from backend.common.enums import StatusType

"""
为什么不使用schema而是使用内部类:
1.schema 通常用于定义 API 的输入输出模型，主要面向外部接口。
2.这些 dataclasses 看起来更像是内部使用的数据结构，用于应用程序的内部逻辑。
3.dataclasses 提供了更多的功能性，如默认值、后处理等。
4.schema（如 Pydantic 模型）更侧重于数据验证和序列化。
"""


# IP信息数据类
@dataclasses.dataclass
class IpInfo:
    ip: str
    country: str | None  # 使用 | 表示可以是 str 或 None，这是 Python 3.10+ 的新语法
    region: str | None
    city: str | None


# 用户代理信息数据类
@dataclasses.dataclass
class UserAgentInfo:
    user_agent: str
    os: str | None
    browser: str | None
    device: str | None


# 请求调用下一个处理器的结果数据类
@dataclasses.dataclass
class RequestCallNext:
    code: str
    msg: str
    status: StatusType
    err: Exception | None
    response: Response


# 新token信息数据类
@dataclasses.dataclass
class NewToken:
    new_access_token: str
    new_access_token_expire_time: datetime
    new_refresh_token: str
    new_refresh_token_expire_time: datetime


# 访问令牌数据类
@dataclasses.dataclass
class AccessToken:
    access_token: str
    access_token_expire_time: datetime


# 刷新令牌数据类
@dataclasses.dataclass
class RefreshToken:
    refresh_token: str
    refresh_token_expire_time: datetime


# 任务结果数据类
@dataclasses.dataclass
class TaskResult:
    result: str
    traceback: str
    status: str
    name: str
    args: list | None
    kwargs: dict | None
    worker: str
    retries: int | None
    queue: str | None
