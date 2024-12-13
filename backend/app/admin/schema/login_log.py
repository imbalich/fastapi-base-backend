#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fastapi-base-backend 
@File    ：login_log.py
@IDE     ：PyCharm 
@Author  ：imbalich
@Date    ：2024/12/13 16:30 
'''
from datetime import datetime

from pydantic import ConfigDict

from backend.common.schema import SchemaBase


class LoginLogSchemaBase(SchemaBase):
    user_uuid: str
    username: str
    status: int
    ip: str
    country: str | None
    region: str | None
    city: str | None
    user_agent: str
    browser: str | None
    os: str | None
    device: str | None
    msg: str
    login_time: datetime


class CreateLoginLogParam(LoginLogSchemaBase):
    pass


class UpdateLoginLogParam(LoginLogSchemaBase):
    pass


class GetLoginLogListDetails(LoginLogSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_time: datetime